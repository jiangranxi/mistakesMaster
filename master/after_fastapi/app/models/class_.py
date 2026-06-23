import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Text, UniqueConstraint, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

TZ = timezone(timedelta(hours=8))


class Class(Base, UUIDMixin):
    __tablename__ = "classes"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    code: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(TZ), nullable=False
    )

    # 关系
    teacher = relationship("User", back_populates="created_classes", foreign_keys=[teacher_id])
    students_rel = relationship("ClassStudent", back_populates="class_", cascade="all, delete-orphan")


class ClassStudent(Base, UUIDMixin):
    __tablename__ = "class_students"
    __table_args__ = (
        UniqueConstraint("class_id", "student_id", name="uq_class_student"),
    )

    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classes.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(TZ), nullable=False
    )

    # 关系
    class_ = relationship("Class", back_populates="students_rel")
