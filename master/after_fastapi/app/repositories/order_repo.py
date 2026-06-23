import uuid

from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.repositories.base import BaseRepository

# 允许的排序字段映射（前端字段名 → ORM 列）
_SORT_COLUMN_MAP = {
    "orderNo": Order.order_no,
    "name": Order.name,
    "resourceType": Order.resource_type,
    "price": Order.price,
    "tradeStatus": Order.trade_status,
    "time": Order.time,
}


class OrderRepository(BaseRepository[Order]):
    model = Order

    async def get_by_user(self, user_id: uuid.UUID, page: int, page_size: int,
                          status: str | None = None,
                          sort_field: str | None = None,
                          sort_order: str | None = None) -> tuple[list[Order], int]:
        offset = (page - 1) * page_size
        stmt = select(Order).where(Order.user_id == user_id)
        count_stmt = select(func.count()).select_from(Order).where(Order.user_id == user_id)

        if status and status != "all":
            stmt = stmt.where(Order.trade_status == status)
            count_stmt = count_stmt.where(Order.trade_status == status)

        # 动态排序：合法字段按指定方向排，否则默认按时间倒序
        order_clauses = []
        if sort_field and sort_field in _SORT_COLUMN_MAP:
            col = _SORT_COLUMN_MAP[sort_field]
            if sort_order == "asc":
                order_clauses.append(asc(col))
            else:
                order_clauses.append(desc(col))
        # 次排序始终按时间倒序（分层排序中最低优先级）
        order_clauses.append(desc(Order.time))
        stmt = stmt.order_by(*order_clauses).offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0
