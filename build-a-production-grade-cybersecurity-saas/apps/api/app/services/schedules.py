from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.schemas.security import ScanScheduleCreate, ScanScheduleRead


class ScheduleService:
    def __init__(self) -> None:
        self.schedules: dict[str, ScanScheduleRead] = {}

    def create(self, payload: ScanScheduleCreate, organization_id: str = "demo-org") -> ScanScheduleRead:
        schedule = ScanScheduleRead(
            id=str(uuid4()),
            organization_id=organization_id,
            domain=payload.domain,
            cadence=payload.cadence,
            enabled=True,
            next_run_at=self._next_run(payload.cadence),
        )
        self.schedules[schedule.id] = schedule
        return schedule

    def list(self) -> list[ScanScheduleRead]:
        return list(self.schedules.values())

    def _next_run(self, cadence: str) -> datetime:
        days = {"daily": 1, "weekly": 7, "monthly": 30}.get(cadence, 1)
        return datetime.now(UTC) + timedelta(days=days)


schedule_service = ScheduleService()
