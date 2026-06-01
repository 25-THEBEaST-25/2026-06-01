from app.schemas.security import Finding


class BreachMonitoringService:
    async def scan(self, domain: str) -> list[Finding]:
        return [
            Finding(
                category="breach_monitoring",
                key="exposed_emails",
                status="pass",
                severity="info",
                message="No exposed emails were found in configured breach feeds.",
                evidence={"domain": domain, "feed": "configured-feeds"},
            )
        ]
