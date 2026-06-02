from datetime import UTC, datetime


class AuditService:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def record(self, action: str, actor: str = "system", target: str | None = None, **metadata: object) -> None:
        self.events.append(
            {
                "action": action,
                "actor": actor,
                "target": target,
                "metadata": metadata,
                "created_at": datetime.now(UTC).isoformat(),
            }
        )

    def list(self) -> list[dict]:
        return self.events[-100:]


audit_service = AuditService()
