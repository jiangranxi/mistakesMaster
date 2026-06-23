import uuid

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    model = Order

    async def get_by_user(self, user_id: uuid.UUID, page: int, page_size: int,
                          status: str | None = None) -> tuple[list[Order], int]:
        offset = (page - 1) * page_size
        stmt = select(Order).where(Order.user_id == user_id)
        count_stmt = select(func.count()).select_from(Order).where(Order.user_id == user_id)

        if status and status != "all":
            stmt = stmt.where(Order.trade_status == status)
            count_stmt = count_stmt.where(Order.trade_status == status)

        stmt = stmt.order_by(desc(Order.time)).offset(offset).limit(page_size)
        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0
