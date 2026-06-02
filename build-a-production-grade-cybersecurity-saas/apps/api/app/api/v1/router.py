from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.core.tenant import tenant_context
from app.schemas.security import (
    AlertRead,
    AlertUpdateRequest,
    BusinessImpactRequest,
    BusinessImpactResponse,
    DashboardResponse,
    DomainScanRequest,
    LoginRequest,
    MetricsResponse,
    ReportMetadata,
    RiskSimulationRequest,
    RiskSimulationResponse,
    ScanJobRead,
    ScanScheduleCreate,
    ScanScheduleRead,
    ScanResponse,
    TokenResponse,
)
from app.services.alerts import alert_workflow
from app.services.audit import audit_service
from app.services.business_impact import BusinessImpactEstimator
from app.services.cache import cache
from app.services.jobs import job_queue
from app.services.orchestrator import ScanOrchestrator
from app.services.report_store import report_store
from app.services.reporting import ReportService
from app.services.rate_limits import scan_rate_limiter
from app.services.risk_simulator import RiskImprovementSimulator
from app.services.schedules import schedule_service

api_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

DEMO_USERS = {
    "admin@cyberriskradar.dev": {
        "id": "usr_admin",
        "email": "admin@cyberriskradar.dev",
        "role": "admin",
        "hashed_password": hash_password("ChangeMe123!"),
    }
}

orchestrator = ScanOrchestrator()
report_service = ReportService()
risk_simulator = RiskImprovementSimulator()
business_impact_estimator = BusinessImpactEstimator()


def require_role(*roles: str):
    async def dependency(token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except JWTError as exc:
            raise HTTPException(status_code=401, detail="Invalid authentication token") from exc
        if payload.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return payload

    return dependency


@api_router.get("/health", tags=["system"])
async def health() -> dict:
    return {"status": "ok", "service": "cyber-risk-radar-api"}


@api_router.get("/metrics", response_model=MetricsResponse, tags=["system"])
async def metrics(_: dict = Depends(require_role("admin"))) -> MetricsResponse:
    return MetricsResponse(
        uptime="process",
        queued_jobs=len(job_queue.jobs),
        active_alerts=len([alert for alert in alert_workflow.list() if alert.status == "open"]),
        cache={"backend": "in_memory_ttl", "entries": len(cache._values)},
    )


@api_router.post("/auth/login", response_model=TokenResponse, tags=["auth"])
async def login(payload: LoginRequest) -> TokenResponse:
    user = DEMO_USERS.get(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    audit_service.record("auth.login", actor=user["email"])
    return TokenResponse(
        access_token=create_access_token(subject=user["email"], role=user["role"]),
        refresh_token=create_refresh_token(subject=user["email"], role=user["role"]),
    )


@api_router.get("/dashboard", response_model=DashboardResponse, tags=["dashboard"])
async def dashboard(_: dict = Depends(require_role("admin", "analyst", "viewer"))) -> DashboardResponse:
    sample_scan = await orchestrator.scan_domain(DomainScanRequest(domain="example.com"))
    return DashboardResponse(
        risk_score=sample_scan.risk_score,
        trend=[
            {"date": "2026-05-26", "score": 84},
            {"date": "2026-05-27", "score": 82},
            {"date": "2026-05-28", "score": 79},
            {"date": "2026-05-29", "score": 81},
            {"date": "2026-05-30", "score": sample_scan.risk_score},
        ],
        active_alerts=[
            {
                "severity": "high",
                "title": "DMARC policy missing enforcement",
                "asset": "example.com",
                "created_at": "2026-05-30T08:00:00Z",
            },
            {
                "severity": "medium",
                "title": "CSP header not configured",
                "asset": "app.example.com",
                "created_at": "2026-05-29T16:20:00Z",
            },
        ],
        recommendations=sample_scan.recommendations[:4],
    )


@api_router.post("/scans/domain", response_model=ScanResponse, tags=["scans"])
async def scan_domain(
    payload: DomainScanRequest,
    organization_id: str = Depends(tenant_context),
    _: dict = Depends(require_role("admin", "analyst")),
) -> ScanResponse:
    if not scan_rate_limiter.allowed(organization_id):
        raise HTTPException(status_code=429, detail="Hourly scan limit exceeded for this organization")
    audit_service.record("scan.sync", target=payload.domain)
    return await orchestrator.scan_domain(payload)


@api_router.post("/scans/domain/jobs", response_model=ScanJobRead, tags=["scans"])
async def enqueue_domain_scan(
    payload: DomainScanRequest,
    background_tasks: BackgroundTasks,
    organization_id: str = Depends(tenant_context),
    _: dict = Depends(require_role("admin", "analyst")),
) -> ScanJobRead:
    if not scan_rate_limiter.allowed(organization_id):
        raise HTTPException(status_code=429, detail="Hourly scan limit exceeded for this organization")
    job = job_queue.enqueue(payload.domain, organization_id=organization_id)
    background_tasks.add_task(job_queue.run, job.id)
    audit_service.record("scan.enqueue", target=payload.domain, job_id=job.id)
    return job


@api_router.get("/scans/jobs/{job_id}", response_model=ScanJobRead, tags=["scans"])
async def scan_job_status(
    job_id: str,
    _: dict = Depends(require_role("admin", "analyst", "viewer")),
) -> ScanJobRead:
    job = job_queue.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan job not found")
    return job


@api_router.post("/risk/simulate", response_model=RiskSimulationResponse, tags=["risk"])
async def simulate_risk_improvement(
    payload: RiskSimulationRequest,
    _: dict = Depends(require_role("admin", "analyst", "viewer")),
) -> RiskSimulationResponse:
    return risk_simulator.simulate(
        findings=payload.findings,
        selected_finding_keys=payload.selected_finding_keys,
        current_score=payload.current_score,
    )


@api_router.post(
    "/business-impact/estimate",
    response_model=BusinessImpactResponse,
    tags=["business-impact"],
)
async def estimate_business_impact(
    payload: BusinessImpactRequest,
    _: dict = Depends(require_role("admin", "analyst", "viewer")),
) -> BusinessImpactResponse:
    return business_impact_estimator.estimate(payload)


@api_router.get("/alerts", response_model=list[AlertRead], tags=["alerts"])
async def list_alerts(_: dict = Depends(require_role("admin", "analyst", "viewer"))) -> list[AlertRead]:
    return alert_workflow.list()


@api_router.patch("/alerts/{alert_id}", response_model=AlertRead, tags=["alerts"])
async def update_alert(
    alert_id: str,
    payload: AlertUpdateRequest,
    _: dict = Depends(require_role("admin", "analyst")),
) -> AlertRead:
    alert = alert_workflow.update(alert_id, payload)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    audit_service.record("alert.update", target=alert_id, status=payload.status)
    return alert


@api_router.post("/schedules", response_model=ScanScheduleRead, tags=["schedules"])
async def create_schedule(
    payload: ScanScheduleCreate,
    _: dict = Depends(require_role("admin", "analyst")),
) -> ScanScheduleRead:
    schedule = schedule_service.create(payload)
    audit_service.record("schedule.create", target=payload.domain, cadence=payload.cadence)
    return schedule


@api_router.get("/schedules", response_model=list[ScanScheduleRead], tags=["schedules"])
async def list_schedules(_: dict = Depends(require_role("admin", "analyst", "viewer"))) -> list[ScanScheduleRead]:
    return schedule_service.list()


@api_router.post("/reports/domain", tags=["reports"])
async def domain_report(
    payload: DomainScanRequest,
    _: dict = Depends(require_role("admin", "analyst", "viewer")),
) -> Response:
    scan = await orchestrator.scan_domain(payload)
    pdf = report_service.build_pdf(scan)
    report_store.save_metadata(payload.domain)
    audit_service.record("report.generate", target=payload.domain)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{payload.domain}-risk-report.pdf"'},
    )


@api_router.get("/reports", response_model=list[ReportMetadata], tags=["reports"])
async def reports(_: dict = Depends(require_role("admin", "analyst", "viewer"))) -> list[ReportMetadata]:
    return report_store.list()


@api_router.get("/audit", tags=["admin"])
async def audit_log(_: dict = Depends(require_role("admin"))) -> list[dict]:
    return audit_service.list()


@api_router.get("/admin/users", tags=["admin"])
async def admin_users(_: dict = Depends(require_role("admin"))) -> list[dict]:
    return [
        {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
        }
        for user in DEMO_USERS.values()
    ]
