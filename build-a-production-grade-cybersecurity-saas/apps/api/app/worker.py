from urllib.parse import urlparse

from arq.connections import RedisSettings

from app.core.config import settings


async def run_domain_scan(ctx: dict, domain: str, organization_id: str) -> dict:
    from app.schemas.security import DomainScanRequest
    from app.services.orchestrator import ScanOrchestrator

    scan = await ScanOrchestrator().scan_domain(DomainScanRequest(domain=domain))
    return scan.model_dump(mode="json") | {"organization_id": organization_id}


class WorkerSettings:
    parsed_redis = urlparse(settings.REDIS_URL)
    redis_settings = RedisSettings(
        host=parsed_redis.hostname or "redis",
        port=parsed_redis.port or 6379,
        database=int((parsed_redis.path or "/0").lstrip("/") or "0"),
    )
    functions = [run_domain_scan]
