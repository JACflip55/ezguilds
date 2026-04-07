import time
from collections import defaultdict

from fastapi import HTTPException


class RateLimitExceeded(Exception):
    pass


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def check(self, user_id: str, action: str) -> None:
        key = f"{user_id}:{action}"
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove expired entries
        self._requests[key] = [t for t in self._requests[key] if t > cutoff]

        if len(self._requests[key]) >= self.max_requests:
            raise RateLimitExceeded(
                f"Rate limit exceeded: max {self.max_requests} {action} requests per {self.window_seconds}s"
            )

        self._requests[key].append(now)


# Shared instances
generate_limiter = RateLimiter(max_requests=10, window_seconds=3600)  # 10/hour
chat_limiter = RateLimiter(max_requests=100, window_seconds=3600)  # 100/hour
