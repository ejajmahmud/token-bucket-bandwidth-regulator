"""Core Token Bucket Bandwidth Regulator implementation."""
import time
from typing import Dict, Any, Optional


class TokenBucketBandwidthRegulator:
    def __init__(self, capacity: float, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.tokens = float(capacity)
        self.last_update = time.time()

    def _refill(self, now: Optional[float] = None):
        current = now if now is not None else time.time()
        elapsed = max(0.0, current - self.last_update)
        added = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + added)
        self.last_update = current

    def try_acquire(self, tokens_requested: float, now: Optional[float] = None) -> bool:
        self._refill(now)
        if self.tokens >= tokens_requested:
            self.tokens -= tokens_requested
            return True
        return False

    def get_wait_time(self, tokens_requested: float, now: Optional[float] = None) -> float:
        self._refill(now)
        if self.tokens >= tokens_requested:
            return 0.0
        deficit = tokens_requested - self.tokens
        return deficit / self.refill_rate
