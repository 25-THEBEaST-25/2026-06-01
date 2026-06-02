from datetime import UTC, datetime

from app.schemas.security import AlertRead, AlertUpdateRequest


class AlertWorkflow:
    def __init__(self) -> None:
        self.alerts: dict[str, AlertRead] = {
            "alt_dmarc": AlertRead(
                id="alt_dmarc",
                asset="example.com",
                severity="high",
                title="DMARC policy missing enforcement",
                description="DMARC exists but does not enforce quarantine or reject.",
                status="open",
                created_at=datetime.now(UTC),
            )
        }

    def list(self) -> list[AlertRead]:
        return list(self.alerts.values())

    def update(self, alert_id: str, payload: AlertUpdateRequest) -> AlertRead | None:
        alert = self.alerts.get(alert_id)
        if not alert:
            return None
        updated = alert.model_copy(
            update={
                "status": payload.status,
                "resolution_note": payload.resolution_note,
                "updated_at": datetime.now(UTC),
            }
        )
        self.alerts[alert_id] = updated
        return updated


alert_workflow = AlertWorkflow()
