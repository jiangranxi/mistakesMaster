import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book, BookChapter
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

    async def get_chapters_by_book_id(self, book_id: uuid.UUID) -> list[dict]:
        """获取单个习题集的所有章节，返回完整字段供树构建使用"""
        stmt = (
            select(BookChapter)
            .where(BookChapter.book_id == book_id)
            .order_by(BookChapter.sort_order)
        )
        result = await self.db.execute(stmt)
        chapters = result.scalars().all()
        return [
            {
                "id": str(ch.id),
                "name": ch.name,
                "parent_id": str(ch.parent_id) if ch.parent_id else None,
                "sort_order": ch.sort_order,
            }
            for ch in chapters
        ]

    async def get_chapters_by_book_ids(self, book_ids: list[uuid.UUID]) -> dict[uuid.UUID, list[dict]]:
        """批量获取多个习题集的章节，一次性查询，按 book_id 分组返回"""
        if not book_ids:
            return {}

        stmt = (
            select(BookChapter)
            .where(BookChapter.book_id.in_(book_ids))
            .order_by(BookChapter.sort_order)
        )
        result = await self.db.execute(stmt)
        chapters = result.scalars().all()

        grouped: dict[uuid.UUID, list[dict]] = {bid: [] for bid in book_ids}
        for ch in chapters:
            grouped[ch.book_id].append({
                "id": str(ch.id),
                "name": ch.name,
                "parent_id": str(ch.parent_id) if ch.parent_id else None,
                "sort_order": ch.sort_order,
            })
        return grouped
