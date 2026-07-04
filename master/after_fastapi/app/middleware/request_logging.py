"""
请求日志中间件 — 记录每个 HTTP 请求的方法、路径、耗时和用户身份。
通过 request.state.user_id 传递用户 ID（由 dependencies.py 中的 get_current_user 设置）。
"""

import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.access")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """记录请求方法、路径、状态码、耗时和用户身份"""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        user_id = getattr(request.state, "user_id", None) or "-"

        logger.info(
            "%s %s user=%s → %d (%.2fms)",
            request.method,
            request.url.path,
            user_id,
            response.status_code,
            duration_ms,
        )

        return response
