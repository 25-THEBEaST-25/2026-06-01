from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.security import ReportMetadata


class ReportStore:
    def __init__(self) -> None:
        self.reports: dict[str, ReportMetadata] = {}

    def save_metadata(self, domain: str, report_type: str = "executive") -> ReportMetadata:
        report = ReportMetadata(
            id=str(uuid4()),
            domain=domain,
            report_type=report_type,
            storage_uri=f"memory://reports/{domain}/{uuid4()}.pdf",
            created_at=datetime.now(UTC),
        )
        self.reports[report.id] = report
        return report

    def list(self) -> list[ReportMetadata]:
        return list(self.reports.values())


report_store = ReportStore()
