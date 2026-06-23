import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.review_repo import ReviewRepository


class ReviewService:
    """讲评服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.review_repo = ReviewRepository(db)

    async def get_error_book_reports(self, teacher_id: uuid.UUID, page: int, page_size: int,
                                     report: str | None = None, book: str | None = None,
                                     start_time: str | None = None, end_time: str | None = None,
                                     subject: str | None = None, class_name: str | None = None,
                                     sort_field: str | None = None, sort_order: str | None = None) -> dict:
        items, total = await self.review_repo.get_reports(
            teacher_id=teacher_id, report_type="error_book",
            page=page, page_size=page_size,
            report=report, book=book,
            start_time=start_time, end_time=end_time,
            subject=subject, class_name=class_name,
            sort_field=sort_field, sort_order=sort_order,
        )
        return {
            "list": [self._to_dict(r) for r in items],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def get_homework_reports(self, teacher_id: uuid.UUID, page: int, page_size: int,
                                   report: str | None = None, book: str | None = None,
                                   start_time: str | None = None, end_time: str | None = None,
                                   subject: str | None = None, class_name: str | None = None,
                                   sort_field: str | None = None, sort_order: str | None = None) -> dict:
        items, total = await self.review_repo.get_reports(
            teacher_id=teacher_id, report_type="homework",
            page=page, page_size=page_size,
            report=report, book=book,
            start_time=start_time, end_time=end_time,
            subject=subject, class_name=class_name,
            sort_field=sort_field, sort_order=sort_order,
        )
        return {
            "list": [self._to_dict(r, include_extra=True) for r in items],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    @staticmethod
    def _to_dict(r, include_extra: bool = False) -> dict:
        d = {
            "id": str(r.id),
            "seq": r.seq,
            "date": r.date.isoformat() if r.date else None,
            "report": r.report,
            "book": r.book,
            "max": r.max,
            "min": r.min,
            "avg": float(r.avg) if r.avg else None,
            "median": r.median,
            "mode": r.mode,
        }
        if include_extra:
            d["subject"] = r.subject
            d["className"] = r.class_name
        return d
