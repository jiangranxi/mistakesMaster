import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.homework import SubmitHomeworkRequest
from app.services.homework_service import StudentHomeworkService

router = APIRouter(prefix="/homework", tags=["学生端-作业管理"])


@router.get("/latest")
async def get_latest(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """最新作业"""
    service = StudentHomeworkService(db)
    return await service.get_latest(current_user.id, page, pageSize)


@router.get("/history")
async def get_history(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    book: str | None = Query(default=None),
    name: str | None = Query(default=None),
    time: str | None = Query(default=None),
    sortField: str | None = Query(default=None),
    sortOrder: str | None = Query(default=None),
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """历史作业"""
    service = StudentHomeworkService(db)
    return await service.get_history(
        current_user.id, page, pageSize,
        book=book, name=name, time=time,
        sort_field=sortField, sort_order=sortOrder,
    )


@router.get("/errors")
async def get_errors(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    name: str | None = Query(default=None),
    book: str | None = Query(default=None),
    startTime: str | None = Query(default=None),
    endTime: str | None = Query(default=None),
    sortField: str | None = Query(default=None),
    sortOrder: str | None = Query(default=None),
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """错题集"""
    service = StudentHomeworkService(db)
    return await service.get_errors(
        current_user.id, page, pageSize,
        name=name, book=book,
        start_time=startTime, end_time=endTime,
        sort_field=sortField, sort_order=sortOrder,
    )


@router.post("/{homework_id}/submit")
async def submit_homework(
    homework_id: uuid.UUID,
    req: SubmitHomeworkRequest,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """提交作业"""
    service = StudentHomeworkService(db)
    return await service.submit(current_user.id, homework_id, req.content)


@router.get("/{homework_id}/correction")
async def get_correction(
    homework_id: uuid.UUID,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """批改结果"""
    service = StudentHomeworkService(db)
    return await service.get_correction(current_user.id, homework_id)


@router.get("/{homework_id}/report")
async def get_report(
    homework_id: uuid.UUID,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """作业报告"""
    service = StudentHomeworkService(db)
    return await service.get_report(current_user.id, homework_id)
