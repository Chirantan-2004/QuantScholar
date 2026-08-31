"""
QuantumScholar - API Logging Middleware
Logs incoming queries, retrieval latencies, and execution telemetry.
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [QuantumScholar] %(message)s")
logger = logging.getLogger("quantumscholar")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs API requests, response status codes, and execution duration."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path
        method = request.method
        
        try:
            response: Response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            logger.info(f"{method} {path} -> {response.status_code} ({duration:.2f}ms)")
            return response
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"{method} {path} FAILED: {str(e)} ({duration:.2f}ms)")
            raise e
