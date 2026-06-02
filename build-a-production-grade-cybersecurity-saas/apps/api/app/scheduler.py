import asyncio
import logging

from app.services.audit import audit_service
from app.services.schedules import schedule_service

logger = logging.getLogger("cyber-risk-radar.scheduler")


async def tick() -> None:
    for schedule in schedule_service.list():
        logger.info("schedule_checked", extra={"domain": schedule.domain, "cadence": schedule.cadence})
        audit_service.record("schedule.tick", target=schedule.domain, cadence=schedule.cadence)


async def main() -> None:
    while True:
        await tick()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
