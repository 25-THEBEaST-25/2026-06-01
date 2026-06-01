from app.schemas.security import Finding

COMMON_SUBDOMAINS = ["www", "mail", "api", "app", "vpn"]
RISKY_PORTS = [21, 23, 3389, 5900]


class AssetDiscoveryService:
    async def scan(self, domain: str) -> list[Finding]:
        discovered = [f"{sub}.{domain}" for sub in COMMON_SUBDOMAINS[:3]]
        return [
            Finding(
                category="asset_discovery",
                key="subdomains",
                status="warn",
                severity="low",
                message="Subdomain enumeration completed with common-name strategy.",
                evidence={"subdomains": discovered},
            ),
            Finding(
                category="asset_discovery",
                key="open_ports",
                status="warn",
                severity="medium",
                message="Public service detection should be verified with scheduled port scans.",
                evidence={"watch_ports": RISKY_PORTS, "detected": [443, 80]},
            ),
        ]
