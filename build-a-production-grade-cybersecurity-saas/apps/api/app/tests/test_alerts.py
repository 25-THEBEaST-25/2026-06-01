from app.schemas.security import AlertUpdateRequest
from app.services.alerts import AlertWorkflow


def test_alert_workflow_updates_status() -> None:
    workflow = AlertWorkflow()
    alert = workflow.update(
        "alt_dmarc",
        AlertUpdateRequest(status="acknowledged", resolution_note="Owner assigned"),
    )

    assert alert is not None
    assert alert.status == "acknowledged"
