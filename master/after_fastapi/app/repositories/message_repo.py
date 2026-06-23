import uuid

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    model = Message

    async def get_by_user(self, user_id: uuid.UUID, page: int = 1, page_size: int = 15) -> tuple[list[Message], int]:
        offset = (page - 1) * page_size
        stmt = select(Message).where(Message.user_id == user_id).order_by(desc(Message.created_at)).offset(offset).limit(page_size)
        count_stmt = select(func.count()).select_from(Message).where(Message.user_id == user_id)
        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0

    async def mark_read(self, message_id: uuid.UUID, user_id: uuid.UUID) -> Message | None:
        stmt = select(Message).where(Message.id == message_id, Message.user_id == user_id)
        result = await self.db.execute(stmt)
        msg = result.scalar_one_or_none()
        if msg:
            msg.is_read = True
            await self.db.flush()
        return msg
