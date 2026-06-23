import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Integer, Text, UniqueConstraint, ForeignKey
from sqlalchemy import Uuid as UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin

TZ = timezone(timedelta(hours=8))


class Homework(Base, UUIDMixin):
    """教师布置的作业"""
    __tablename__ = "homeworks"

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    source: Mapped[str | None] = mapped_column(String(128), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(32), nullable=True)
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False
    )
    book_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.id"), nullable=True
    )
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    deadline: Mapped[datetime | None] = mapped_column(nullable=True)
    total_score: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(TZ), nullable=False
    )


class StudentHomework(Base, UUIDMixin):
    """学生作业作答记录"""
    __tablename__ = "student_homeworks"
    __table_args__ = (
        UniqueConstraint("homework_id", "student_id", name="uq_student_homework"),
    )

    homework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("homeworks.id"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    submit_time: Mapped[datetime | None] = mapped_column(nullable=True)
    total_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    my_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submit_content: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ErrorItem(Base, UUIDMixin):
    """学生错题"""
    __tablename__ = "error_items"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    homework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("homeworks.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    source: Mapped[str | None] = mapped_column(String(128), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(32), nullable=True)
    error_seq: Mapped[int | None] = mapped_column(Integer, nullable=True)
    submit_time: Mapped[datetime | None] = mapped_column(nullable=True)
