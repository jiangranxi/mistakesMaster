import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, BigInteger, Boolean, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin

TZ = timezone(timedelta(hours=8))


class LessonPlan(Base, UUIDMixin):
    """教案"""
    __tablename__ = "lesson_plans"

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    is_cloud: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(TZ), nullable=False
    )
