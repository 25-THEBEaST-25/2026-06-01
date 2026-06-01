from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.security import DashboardResponse, DomainScanRequest, LoginRequest, ScanResponse, TokenResponse
from app.services.orchestrator import ScanOrchestrator
from app.services.reporting import ReportService

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


@api_router.post("/auth/login", response_model=TokenResponse, tags=["auth"])
async def login(payload: LoginRequest) -> TokenResponse:
    user = DEMO_USERS.get(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(subject=user["email"], role=user["role"]))


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
    _: dict = Depends(require_role("admin", "analyst")),
) -> ScanResponse:
    return await orchestrator.scan_domain(payload)


@api_router.post("/reports/domain", tags=["reports"])
async def domain_report(
    payload: DomainScanRequest,
    _: dict = Depends(require_role("admin", "analyst", "viewer")),
) -> Response:
    scan = await orchestrator.scan_domain(payload)
    pdf = report_service.build_pdf(scan)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{payload.domain}-risk-report.pdf"'},
    )


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
