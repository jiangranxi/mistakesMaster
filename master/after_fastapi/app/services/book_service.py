import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFound
from app.repositories.book_repo import BookRepository
from app.utils.tree import build_chapter_tree


class BookService:
    """习题集服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repo = BookRepository(db)

    async def get_list(self, page: int, page_size: int) -> dict:
        items, total = await self.book_repo.get_list(page, page_size)

        # 批量获取所有习题集的章节 → 解决 N+1 查询
        book_ids = [b.id for b in items]
        chapters_by_book = await self.book_repo.get_chapters_by_book_ids(book_ids)

        result_list = []
        for b in items:
            flat_chapters = chapters_by_book.get(b.id, [])
            chapter_tree = build_chapter_tree(flat_chapters)
            result_list.append({
                "id": str(b.id),
                "name": b.name,
                "cover": b.cover,
                "price": float(b.price) if b.price else 0,
                "subject": b.subject,
                "publisher": b.publisher,
                "version": b.version,
                "gradeTerm": b.grade_term,
                "description": b.description,
                "updateTime": b.updated_at if b.updated_at else None,
                "chapters": chapter_tree,
            })

        return {
            "list": result_list,
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
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise NotFound("习题集不存在")

        flat_chapters = await self.book_repo.get_chapters_by_book_id(book_id)
        chapter_tree = build_chapter_tree(flat_chapters)

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
            "updateTime": book.updated_at if book.updated_at else None,
            "chapters": chapter_tree,
        }
