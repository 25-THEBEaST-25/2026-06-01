from abc import ABC, abstractmethod

from app.schemas.security import Finding
from app.services.asset_discovery import AssetDiscoveryService
from app.services.breach_monitor import BreachMonitoringService
from app.services.domain_monitor import DomainMonitor
from app.services.email_security import EmailSecurityAnalyzer
from app.services.header_scanner import SecurityHeaderScanner


class Scanner(ABC):
    name: str

    @abstractmethod
    async def scan(self, domain: str) -> list[Finding]:
        raise NotImplementedError


class ScannerRegistry:
    def __init__(self) -> None:
        self._scanners: list[Scanner] = [
            DomainMonitor(),
            SecurityHeaderScanner(),
            EmailSecurityAnalyzer(),
            AssetDiscoveryService(),
            BreachMonitoringService(),
        ]

    @property
    def scanners(self) -> list[Scanner]:
        return self._scanners

    def register(self, scanner: Scanner) -> None:
        self._scanners.append(scanner)
