from app.services.jobs import InMemoryScanJobQueue


def test_scan_job_queue_creates_queued_job() -> None:
    queue = InMemoryScanJobQueue()
    job = queue.enqueue("example.com")

    assert job.status == "queued"
    assert job.progress == 0
    assert queue.get(job.id) == job
