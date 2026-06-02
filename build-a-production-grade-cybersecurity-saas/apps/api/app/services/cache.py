import time
from dataclasses import dataclass
from typing import Generic, TypeVar

from app.core.config import settings

T = TypeVar("T")


@dataclass
class CacheEntry(Generic[T]):
    value: T
    expires_at: float


class TTLCache:
    def __init__(self) -> None:
        self._values: dict[str, CacheEntry] = {}

    def get(self, key: str) -> object | None:
        entry = self._values.get(key)
        if not entry:
            return None
        if entry.expires_at <= time.time():
            self._values.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: object, ttl_seconds: int | None = None) -> None:
        ttl = ttl_seconds or settings.CACHE_DEFAULT_TTL_SECONDS
        self._values[key] = CacheEntry(value=value, expires_at=time.time() + ttl)


cache = TTLCache()
