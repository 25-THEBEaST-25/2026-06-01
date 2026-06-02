from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.security import DomainScanRequest, ScanJobRead
from app.services.orchestrator import ScanOrchestrator


class InMemoryScanJobQueue:
    def __init__(self) -> None:
        self.jobs: dict[str, ScanJobRead] = {}
        self.orchestrator = ScanOrchestrator()

    def enqueue(self, domain: str, organization_id: str = "demo-org") -> ScanJobRead:
        job = ScanJobRead(
            id=str(uuid4()),
            organization_id=organization_id,
            domain=domain,
            status="queued",
            progress=0,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        self.jobs[job.id] = job
        return job

    async def run(self, job_id: str) -> None:
        job = self.jobs[job_id]
        self.jobs[job_id] = job.model_copy(update={"status": "running", "progress": 20, "updated_at": datetime.now(UTC)})
        try:
            result = await self.orchestrator.scan_domain(DomainScanRequest(domain=job.domain))
            self.jobs[job_id] = self.jobs[job_id].model_copy(
                update={
                    "status": "completed",
                    "progress": 100,
                    "result": result,
                    "updated_at": datetime.now(UTC),
                }
            )
        except Exception as exc:
            self.jobs[job_id] = self.jobs[job_id].model_copy(
                update={"status": "failed", "error": str(exc), "updated_at": datetime.now(UTC)}
            )

    def get(self, job_id: str) -> ScanJobRead | None:
        return self.jobs.get(job_id)


job_queue = InMemoryScanJobQueue()
