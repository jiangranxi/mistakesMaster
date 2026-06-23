import uuid
from datetime import date

from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class ReviewReport(Base, UUIDMixin):
    """讲评报告"""
    __tablename__ = "review_reports"

    seq: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    report: Mapped[str | None] = mapped_column(String(256), nullable=True)
    book: Mapped[str | None] = mapped_column(String(256), nullable=True)
    max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avg: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    median: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    subject: Mapped[str | None] = mapped_column(String(32), nullable=True)
    class_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # 'error_book' | 'homework'
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
