from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["习题集"])


@router.get("")
async def get_book_list(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """习题集列表"""
    service = BookService(db)
    return await service.get_list(page, pageSize)


@router.get("/{book_id}")
async def get_book_detail(
    book_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """习题集详情"""
    from uuid import UUID
    service = BookService(db)
    return await service.get_detail(UUID(book_id))
