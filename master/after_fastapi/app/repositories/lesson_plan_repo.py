import uuid

from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson_plan import LessonPlan
from app.repositories.base import BaseRepository


class LessonPlanRepository(BaseRepository[LessonPlan]):
    model = LessonPlan

    async def get_by_teacher(self, teacher_id: uuid.UUID, page: int, page_size: int,
                             sort_field: str | None = None, sort_order: str | None = None) -> tuple[list[LessonPlan], int]:
        offset = (page - 1) * page_size
        stmt = select(LessonPlan).where(
            LessonPlan.teacher_id == teacher_id,
            LessonPlan.is_cloud == False,
        )

        count_stmt = select(func.count()).select_from(LessonPlan).where(
            LessonPlan.teacher_id == teacher_id,
            LessonPlan.is_cloud == False,
        )

        order_col = LessonPlan.created_at
        if sort_field == "name":
            order_col = LessonPlan.name
        elif sort_field == "size":
            order_col = LessonPlan.size

        stmt = stmt.order_by(asc(order_col) if sort_order == "asc" else desc(order_col))
        stmt = stmt.offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0

    async def get_cloud(self, page: int, page_size: int,
                        sort_field: str | None = None, sort_order: str | None = None) -> tuple[list[LessonPlan], int]:
        offset = (page - 1) * page_size
        stmt = select(LessonPlan).where(LessonPlan.is_cloud == True)
        count_stmt = select(func.count()).select_from(LessonPlan).where(LessonPlan.is_cloud == True)

        order_col = LessonPlan.created_at
        if sort_field == "name":
            order_col = LessonPlan.name
        elif sort_field == "size":
            order_col = LessonPlan.size
        elif sort_field == "createTime":
            order_col = LessonPlan.created_at

        stmt = stmt.order_by(asc(order_col) if sort_order == "asc" else desc(order_col))
        stmt = stmt.offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0
