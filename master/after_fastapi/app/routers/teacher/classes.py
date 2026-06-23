import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.class_ import CreateClassRequest, JoinClassRequest
from app.services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["班级管理"])


@router.get("/created")
async def get_created_classes(
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """教师创建的班级列表"""
    service = ClassService(db)
    return await service.get_created_classes(current_user.id)


@router.get("/joined")
async def get_joined_classes(
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """教师加入的班级列表"""
    service = ClassService(db)
    return await service.get_joined_classes(current_user.id)


@router.post("")
async def create_class(
    req: CreateClassRequest,
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """创建班级"""
    service = ClassService(db)
    return await service.create_class(current_user.id, req.name, req.description)


@router.post("/join")
async def join_class(
    req: JoinClassRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """通过班级码加入班级"""
    service = ClassService(db)
    return await service.join_class(current_user.id, req.code, req.message)


@router.get("/{class_id}")
async def get_class_detail(
    class_id: uuid.UUID,
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """班级详情"""
    service = ClassService(db)
    return await service.get_class_detail(class_id)


@router.get("/{class_id}/students")
async def get_class_students(
    class_id: uuid.UUID,
    current_user: User = Depends(require_role("teacher")),
    db: AsyncSession = Depends(get_db),
):
    """班级学生列表"""
    service = ClassService(db)
    return await service.get_class_students(class_id)
