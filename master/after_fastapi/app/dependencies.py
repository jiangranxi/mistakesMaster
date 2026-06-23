from typing import AsyncGenerator

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import Unauthorized, Forbidden
from app.core.security import decode_access_token
from app.database import async_session
from app.models.user import User


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """每个请求获取一个数据库会话"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """从 Bearer Token 解析当前用户"""
    if not authorization.startswith("Bearer "):
        raise Unauthorized("认证格式错误")

    token = authorization[7:]
    payload = decode_access_token(token)
    if payload is None:
        raise Unauthorized("Token 无效或已过期")

    user_id = payload.get("sub")
    if not user_id:
        raise Unauthorized("Token 无效")

    from uuid import UUID
    user = await db.get(User, UUID(user_id))
    if not user or not user.is_active:
        raise Unauthorized("用户不存在或已禁用")

    return user


def require_role(*roles: str):
    """工厂函数：返回依赖项，限制特定角色访问"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise Forbidden("权限不足")
        return current_user
    return role_checker
