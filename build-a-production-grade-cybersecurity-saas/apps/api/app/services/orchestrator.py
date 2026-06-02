from datetime import UTC, datetime

from app.schemas.security import DomainScanRequest, ScanResponse
from app.services.asset_discovery import AssetDiscoveryService
from app.services.breach_monitor import BreachMonitoringService
from app.services.domain_monitor import DomainMonitor
from app.services.email_security import EmailSecurityAnalyzer
from app.services.header_scanner import SecurityHeaderScanner
from app.services.recommendations import RecommendationEngine
from app.services.risk_engine import RiskEngine
from app.services.cache import cache
from app.services.scanner_registry import ScannerRegistry


class ScanOrchestrator:
    def __init__(self) -> None:
        self.domain_monitor = DomainMonitor()
        self.header_scanner = SecurityHeaderScanner()
        self.email_analyzer = EmailSecurityAnalyzer()
        self.asset_discovery = AssetDiscoveryService()
        self.breach_monitor = BreachMonitoringService()
        self.scanner_registry = ScannerRegistry()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()

    async def scan_domain(self, request: DomainScanRequest) -> ScanResponse:
        cache_key = f"scan:{request.domain}"
        cached = cache.get(cache_key)
        if isinstance(cached, ScanResponse):
            return cached

        findings = []
        for service in self.scanner_registry.scanners:
            service_findings = await service.scan(request.domain)
            findings.extend(service_findings)

        score = self.risk_engine.calculate(findings)
        recommendations = self.recommendation_engine.generate(findings)
        response = ScanResponse(
            domain=request.domain,
            risk_score=score,
            findings=findings,
            recommendations=recommendations,
            scanned_at=datetime.now(UTC),
        )
        cache.set(cache_key, response, ttl_seconds=300)
        return response
