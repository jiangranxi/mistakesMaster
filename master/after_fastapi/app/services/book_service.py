import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFound
from app.repositories.book_repo import BookRepository


class BookService:
    """习题集服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repo = BookRepository(db)

    async def get_list(self, page: int, page_size: int) -> dict:
        items, total = await self.book_repo.get_list(page, page_size)
        return {
            "list": [
                {
                    "id": str(b.id),
                    "name": b.name,
                    "cover": b.cover,
                    "price": float(b.price) if b.price else 0,
                    "subject": b.subject,
                    "publisher": b.publisher,
                    "version": b.version,
                    "gradeTerm": b.grade_term,
                    "updateTime": b.updated_at.strftime("%Y-%m-%d %H:%M:%S") if b.updated_at else None,
                }
                for b in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def update_book(self, book_id: uuid.UUID, data: dict) -> dict:
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise NotFound("习题集不存在")
        await self.book_repo.update(book, **data)
        return {"id": str(book.id), "cover": book.cover, "message": "更新成功"}

    async def get_detail(self, book_id: uuid.UUID) -> dict:
        book = await self.book_repo.get_with_chapters(book_id)
        if not book:
            raise NotFound("习题集不存在")
        return {
            "id": str(book.id),
            "name": book.name,
            "cover": book.cover,
            "price": float(book.price) if book.price else 0,
            "subject": book.subject,
            "publisher": book.publisher,
            "version": book.version,
            "gradeTerm": book.grade_term,
            "description": book.description,
            "updateTime": book.updated_at.strftime("%Y-%m-%d %H:%M:%S") if book.updated_at else None,
            "chapters": [c.name for c in book.chapters] if book.chapters else [],
        }
