from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    real_name: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)  # 'teacher' | 'student'
    job: Mapped[str | None] = mapped_column(String(32), nullable=True)  # 仅教师
    subject: Mapped[str | None] = mapped_column(String(32), nullable=True)  # 仅教师
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 关系
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    created_classes = relationship("Class", back_populates="teacher", foreign_keys="Class.teacher_id")
    orders = relationship("Order", back_populates="user")
    messages = relationship("Message", back_populates="user")
