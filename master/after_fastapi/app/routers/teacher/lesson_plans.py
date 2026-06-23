from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.services.lesson_plan_service import LessonPlanService

router = APIRouter(prefix="/lesson-plans", tags=["教师端-教案管理"])


@router.get("/own")
async def get_own_plans(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    sortField: str | None = Query(default=None),
    sortOrder: str | None = Query(default=None),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """我的教案"""
    service = LessonPlanService(db)
    return await service.get_own_plans(current_user.id, page, pageSize, sortField, sortOrder)


@router.get("/cloud")
async def get_cloud_plans(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    sortField: str | None = Query(default=None),
    sortOrder: str | None = Query(default=None),
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """云端教案"""
    service = LessonPlanService(db)
    return await service.get_cloud_plans(page, pageSize, sortField, sortOrder)
