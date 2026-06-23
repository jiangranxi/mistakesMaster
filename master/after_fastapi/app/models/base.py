import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

TZ = timezone(timedelta(hours=8))


class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类"""
    pass


class UUIDMixin:
    """UUID 主键混入"""
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    """创建/更新时间戳混入"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(TZ), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(TZ),
        onupdate=lambda: datetime.now(TZ),
        nullable=True,
    )
