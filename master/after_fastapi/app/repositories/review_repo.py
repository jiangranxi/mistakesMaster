import uuid

from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review_report import ReviewReport
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[ReviewReport]):
    model = ReviewReport

    async def get_reports(
        self,
        teacher_id: uuid.UUID,
        report_type: str,
        page: int, page_size: int,
        report: str | None = None,
        book: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        subject: str | None = None,
        class_name: str | None = None,
        sort_field: str | None = None,
        sort_order: str | None = None,
    ) -> tuple[list[ReviewReport], int]:
        offset = (page - 1) * page_size
        stmt = select(ReviewReport).where(
            ReviewReport.teacher_id == teacher_id,
            ReviewReport.type == report_type,
        )
        count_stmt = select(func.count()).select_from(ReviewReport).where(
            ReviewReport.teacher_id == teacher_id,
            ReviewReport.type == report_type,
        )

        if report:
            stmt = stmt.where(ReviewReport.report.ilike(f"%{report}%"))
            count_stmt = count_stmt.where(ReviewReport.report.ilike(f"%{report}%"))
        if book:
            stmt = stmt.where(ReviewReport.book.ilike(f"%{book}%"))
            count_stmt = count_stmt.where(ReviewReport.book.ilike(f"%{book}%"))
        if start_time:
            stmt = stmt.where(ReviewReport.date >= start_time)
            count_stmt = count_stmt.where(ReviewReport.date >= start_time)
        if end_time:
            stmt = stmt.where(ReviewReport.date <= end_time)
            count_stmt = count_stmt.where(ReviewReport.date <= end_time)
        if subject:
            stmt = stmt.where(ReviewReport.subject == subject)
            count_stmt = count_stmt.where(ReviewReport.subject == subject)
        if class_name:
            stmt = stmt.where(ReviewReport.class_name.ilike(f"%{class_name}%"))
            count_stmt = count_stmt.where(ReviewReport.class_name.ilike(f"%{class_name}%"))

        order_col = ReviewReport.seq
        if sort_field == "date":
            order_col = ReviewReport.date
        elif sort_field == "report":
            order_col = ReviewReport.report
        elif sort_field == "book":
            order_col = ReviewReport.book
        elif sort_field == "max":
            order_col = ReviewReport.max
        elif sort_field == "min":
            order_col = ReviewReport.min
        elif sort_field == "avg":
            order_col = ReviewReport.avg
        elif sort_field == "median":
            order_col = ReviewReport.median
        elif sort_field == "mode":
            order_col = ReviewReport.mode
        elif sort_field == "subject":
            order_col = ReviewReport.subject

        stmt = stmt.order_by(asc(order_col) if sort_order == "asc" else desc(order_col))
        stmt = stmt.offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0
