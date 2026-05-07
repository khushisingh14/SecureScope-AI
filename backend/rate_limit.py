import time
from collections import defaultdict, deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import get_settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/health", "/"}:
            return await call_next(request)

        client = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.settings.rate_limit_window_seconds
        bucket = self.requests[client]

        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= self.settings.rate_limit_requests:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)

        bucket.append(now)
        return await call_next(request)
