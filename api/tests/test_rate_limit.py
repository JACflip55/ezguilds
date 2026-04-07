import time
from unittest.mock import patch

import pytest

from src.rate_limit import RateLimiter, RateLimitExceeded


def test_allows_under_limit():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    for _ in range(5):
        limiter.check("user-1", "generate")  # Should not raise


def test_blocks_over_limit():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    limiter.check("user-1", "generate")
    limiter.check("user-1", "generate")
    with pytest.raises(RateLimitExceeded):
        limiter.check("user-1", "generate")


def test_separate_users():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    limiter.check("user-1", "generate")
    limiter.check("user-2", "generate")  # Different user, should not raise


def test_separate_actions():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    limiter.check("user-1", "generate")
    limiter.check("user-1", "chat")  # Different action, should not raise
