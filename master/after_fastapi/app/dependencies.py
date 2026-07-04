import logging
from typing import AsyncGenerator

from fastapi import Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import Unauthorized, Forbidden
from app.core.security import decode_access_token
from app.database import async_session
from app.models.user import User

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """每个请求获取一个数据库会话"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            logger.exception("数据库会话异常，已回滚")
            raise


async def get_current_user(
    request: Request,
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """从 Bearer Token 解析当前用户"""
    if not authorization.startswith("Bearer "):
        logger.warning("认证格式错误: Authorization header 缺少 Bearer 前缀")
        raise Unauthorized("认证格式错误")

    token = authorization[7:]
    payload = decode_access_token(token)
    if payload is None:
        logger.warning("Token 无效或已过期")
        raise Unauthorized("Token 无效或已过期")

    user_id = payload.get("sub")
    if not user_id:
        logger.warning("Token 缺少 sub 字段")
        raise Unauthorized("Token 无效")

    from uuid import UUID
    user = await db.get(User, UUID(user_id))
    if not user or not user.is_active:
        logger.warning("用户不存在或已禁用: user_id=%s", user_id)
        raise Unauthorized("用户不存在或已禁用")

    # 将 user_id 存入 request.state 供中间件使用
    request.state.user_id = str(user.id)

    return user


def require_role(*roles: str):
    """工厂函数：返回依赖项，限制特定角色访问"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            logger.warning("权限不足: user_id=%s, role=%s, required=%s",
                           current_user.id, current_user.role, roles)
            raise Forbidden("权限不足")
        return current_user
    return role_checker
