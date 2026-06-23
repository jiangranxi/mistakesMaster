import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["消息管理"])


@router.get("")
async def get_messages(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """消息列表"""
    service = MessageService(db)
    return await service.get_list(current_user.id, page, pageSize)


@router.put("/{message_id}/read")
async def mark_read(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """标记已读"""
    service = MessageService(db)
    await service.mark_read(current_user.id, message_id)
    return {"message": "已标记为已读"}


@router.delete("/{message_id}")
async def delete_message(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除消息"""
    service = MessageService(db)
    await service.delete(current_user.id, message_id)
    return {"message": "删除成功"}
