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
    echo=settings.DEBUG,
    connect_args=connect_args,
    **pool_kwargs,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
