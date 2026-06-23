from typing import Generic, TypeVar

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """通用 CRUD 仓储基类"""

    model: type[T]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id) -> T | None:
        return await self.db.get(self.model, id)

    async def get_all(self, *filters, offset: int = 0, limit: int = 15) -> list[T]:
        stmt = (
            select(self.model)
            .where(*filters)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(self, *filters) -> int:
        stmt = select(func.count()).select_from(self.model).where(*filters)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def create(self, obj: T) -> T:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: T, **values) -> T:
        for k, v in values.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.db.delete(obj)
        await self.db.flush()

    async def delete_by_id(self, id) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount > 0
