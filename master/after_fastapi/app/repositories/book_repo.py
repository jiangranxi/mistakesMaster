import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    model = Book

    async def get_list(self, page: int, page_size: int) -> tuple[list[Book], int]:
        offset = (page - 1) * page_size
        stmt = select(Book).offset(offset).limit(page_size).order_by(Book.updated_at.desc())
        count_stmt = select(func.count()).select_from(Book)
        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0

    async def get_with_chapters(self, book_id: uuid.UUID) -> Book | None:
        from sqlalchemy.orm import selectinload
        stmt = select(Book).options(selectinload(Book.chapters)).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
