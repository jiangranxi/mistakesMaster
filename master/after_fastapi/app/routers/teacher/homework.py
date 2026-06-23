import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.homework import AssignHomeworkRequest
from app.services.homework_service import HomeworkService

router = APIRouter(prefix="/homework", tags=["教师端-作业管理"])


@router.get("/own")
async def get_own_homework(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """教师自己的作业/试卷列表"""
    service = HomeworkService(db)
    return await service.get_own_homework(current_user.id, page, pageSize)


@router.get("/cloud")
async def get_cloud_homework(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """云端题库"""
    service = HomeworkService(db)
    return await service.get_cloud_homework(page, pageSize)


@router.get("/papers")
async def get_my_papers(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """我的组卷"""
    service = HomeworkService(db)
    return await service.get_my_papers(current_user.id, page, pageSize)


@router.get("/{homework_id}/chapters")
async def get_chapters(
    homework_id: uuid.UUID,
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """作业关联章节"""
    service = HomeworkService(db)
    return await service.get_chapters(homework_id)


@router.post("/assign")
async def assign_homework(
    req: AssignHomeworkRequest,
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """布置作业"""
    service = HomeworkService(db)
    return await service.assign_homework(current_user.id, req)
