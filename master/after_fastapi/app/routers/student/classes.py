from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.class_ import JoinClassRequest
from app.services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["学生端-班级管理"])


@router.get("/joined")
async def get_joined_classes(
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """我加入的班级列表"""
    service = ClassService(db)
    return await service.get_joined_classes(current_user.id)


@router.post("/join")
async def join_class(
    req: JoinClassRequest,
    current_user: User = Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """通过班级码加入班级"""
    service = ClassService(db)
    return await service.join_class(current_user.id, req.code, req.message)
