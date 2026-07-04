import logging
import time

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings

# MySQL 连接池参数 / SQLite 兼容
connect_args = {}
pool_kwargs = {}
if settings.DATABASE_URL.startswith("mysql"):
    connect_args = {"charset": "utf8mb4"}
    pool_kwargs = {"pool_size": 10, "max_overflow": 20, "pool_recycle": 3600}
elif settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **pool_kwargs,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# ── 慢查询检测 ──
SLOW_QUERY_THRESHOLD_MS = 500
_slow_query_logger = logging.getLogger("sqlalchemy.slow")


@event.listens_for(engine.sync_engine, "before_cursor_execute")
def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info["_query_start"] = time.perf_counter()


@event.listens_for(engine.sync_engine, "after_cursor_execute")
def _after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    start = conn.info.pop("_query_start", None)
    if start is None:
        return
    elapsed_ms = (time.perf_counter() - start) * 1000
    if elapsed_ms > SLOW_QUERY_THRESHOLD_MS:
        _slow_query_logger.warning(
            "慢查询 (%.0fms): %s | params=%s",
            elapsed_ms,
            statement[:200],
            parameters,
        )
