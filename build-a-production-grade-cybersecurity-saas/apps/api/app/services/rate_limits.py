from collections import defaultdict, deque
from time import time

from app.core.config import settings


class ScanRateLimiter:
    def __init__(self) -> None:
        self.events: dict[str, deque[float]] = defaultdict(deque)

    def allowed(self, organization_id: str) -> bool:
        now = time()
        bucket = self.events[organization_id]
        while bucket and now - bucket[0] > 3600:
            bucket.popleft()
        if len(bucket) >= settings.SCAN_RATE_LIMIT_PER_HOUR:
            return False
        bucket.append(now)
        return True


scan_rate_limiter = ScanRateLimiter()
