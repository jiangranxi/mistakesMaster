from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.services.review_service import ReviewService

router = APIRouter(prefix="/review", tags=["教师端-讲评"])


@router.get("/error-book")
async def get_error_book_reports(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    report: str | None = Query(default=None),
    book: str | None = Query(default=None),
    startTime: str | None = Query(default=None),
    endTime: str | None = Query(default=None),
    subject: str | None = Query(default=None),
    class_: str | None = Query(default=None, alias="class"),
    sortField: str | None = Query(default=None),
    sortOrder: str | None = Query(default=None),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """错题本讲评"""
    service = ReviewService(db)
    return await service.get_error_book_reports(
        current_user.id, page, pageSize,
        report=report, book=book,
        start_time=startTime, end_time=endTime,
        subject=subject, class_name=class_,
        sort_field=sortField, sort_order=sortOrder,
    )


@router.get("/homework")
async def get_homework_reports(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    report: str | None = Query(default=None),
    book: str | None = Query(default=None),
    startTime: str | None = Query(default=None),
    endTime: str | None = Query(default=None),
    subject: str | None = Query(default=None),
    class_: str | None = Query(default=None, alias="class"),
    sortField: str | None = Query(default=None),
    sortOrder: str | None = Query(default=None),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """作业讲评"""
    service = ReviewService(db)
    return await service.get_homework_reports(
        current_user.id, page, pageSize,
        report=report, book=book,
        start_time=startTime, end_time=endTime,
        subject=subject, class_name=class_,
        sort_field=sortField, sort_order=sortOrder,
    )
