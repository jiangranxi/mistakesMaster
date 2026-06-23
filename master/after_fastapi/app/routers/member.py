from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.member import UpdateProfileRequest, ChangePasswordRequest
from app.services.member_service import MemberService

router = APIRouter(prefix="/member", tags=["会员中心"])


@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取个人资料"""
    service = MemberService(db)
    return await service.get_profile(current_user)


@router.put("/profile")
async def update_profile(
    req: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """修改个人资料"""
    service = MemberService(db)
    return await service.update_profile(current_user, req.model_dump(exclude_none=True))


@router.put("/password")
async def change_password(
    req: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """修改密码"""
    service = MemberService(db)
    await service.change_password(current_user, req.oldPassword, req.newPassword)
    return {"message": "密码修改成功"}


@router.get("/orders")
async def get_orders(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=15, ge=1, le=100),
    status: str = Query(default="all"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """订单列表"""
    service = MemberService(db)
    return await service.get_orders(current_user.id, page, pageSize, status)
