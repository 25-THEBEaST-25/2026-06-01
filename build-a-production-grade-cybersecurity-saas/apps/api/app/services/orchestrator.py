from datetime import UTC, datetime

from app.schemas.security import DomainScanRequest, ScanResponse
from app.services.asset_discovery import AssetDiscoveryService
from app.services.breach_monitor import BreachMonitoringService
from app.services.domain_monitor import DomainMonitor
from app.services.email_security import EmailSecurityAnalyzer
from app.services.header_scanner import SecurityHeaderScanner
from app.services.recommendations import RecommendationEngine
from app.services.risk_engine import RiskEngine


class ScanOrchestrator:
    def __init__(self) -> None:
        self.domain_monitor = DomainMonitor()
        self.header_scanner = SecurityHeaderScanner()
        self.email_analyzer = EmailSecurityAnalyzer()
        self.asset_discovery = AssetDiscoveryService()
        self.breach_monitor = BreachMonitoringService()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()

    async def scan_domain(self, request: DomainScanRequest) -> ScanResponse:
        findings = []
        for service in (
            self.domain_monitor,
            self.header_scanner,
            self.email_analyzer,
            self.asset_discovery,
            self.breach_monitor,
        ):
            findings.extend(await service.scan(request.domain))

        score = self.risk_engine.calculate(findings)
        recommendations = self.recommendation_engine.generate(findings)
        return ScanResponse(
            domain=request.domain,
            risk_score=score,
            findings=findings,
            recommendations=recommendations,
            scanned_at=datetime.now(UTC),
        )
