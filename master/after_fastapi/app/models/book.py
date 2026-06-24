import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Integer, Text, Numeric, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

TZ = timezone(timedelta(hours=8))


class Book(Base, UUIDMixin):
    """习题集"""
    __tablename__ = "books"

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    cover: Mapped[str | None] = mapped_column(String(512), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    subject: Mapped[str | None] = mapped_column(String(32), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(64), nullable=True)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    grade_term: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String(32), nullable=False)

    chapters = relationship("BookChapter", back_populates="book", cascade="all, delete-orphan")


class BookChapter(Base, UUIDMixin):
    """习题集章节（树形结构）"""
    __tablename__ = "book_chapters"

    book_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("book_chapters.id"), nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    book = relationship("Book", back_populates="chapters")
