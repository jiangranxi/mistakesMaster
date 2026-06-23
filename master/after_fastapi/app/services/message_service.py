import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFound
from app.repositories.message_repo import MessageRepository


class MessageService:
    """消息服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.message_repo = MessageRepository(db)

    async def get_list(self, user_id: uuid.UUID, page: int, page_size: int) -> dict:
        items, total = await self.message_repo.get_by_user(user_id, page, page_size)
        return {
            "list": [
                {
                    "id": str(m.id),
                    "from": m.from_user,
                    "role": m.role,
                    "content": m.content,
                    "time": m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else None,
                    "read": m.is_read,
                }
                for m in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def mark_read(self, user_id: uuid.UUID, message_id: uuid.UUID) -> None:
        msg = await self.message_repo.mark_read(message_id, user_id)
        if not msg:
            raise NotFound("消息不存在")

    async def delete(self, user_id: uuid.UUID, message_id: uuid.UUID) -> None:
        msg = await self.message_repo.get_by_id(message_id)
        if not msg or msg.user_id != user_id:
            raise NotFound("消息不存在")
        await self.message_repo.delete(msg)
