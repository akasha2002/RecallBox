import time
import logging
import sys
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

# Configure structured root logger
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("recallbox.access")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs each incoming HTTP request and response status
    with execution duration (latency in ms).
    Strictly avoids logging request bodies or authorization headers.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        
        # Process the request
        response = await call_next(request)
        
        process_time_ms = (time.perf_counter() - start_time) * 1000
        
        # Log clean access log line
        logger.info(
            "%s %s - %d (%0.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            process_time_ms,
        )
        
        # Add latency header for client debugging
        response.headers["X-Process-Time"] = f"{process_time_ms:.2f}ms"
        return response
