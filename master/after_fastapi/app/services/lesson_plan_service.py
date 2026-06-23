import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_plan_repo import LessonPlanRepository


class LessonPlanService:
    """教案管理服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.plan_repo = LessonPlanRepository(db)

    async def get_own_plans(self, teacher_id: uuid.UUID, page: int, page_size: int,
                            sort_field: str | None = None, sort_order: str | None = None) -> dict:
        items, total = await self.plan_repo.get_by_teacher(
            teacher_id, page, page_size, sort_field, sort_order
        )
        return {
            "list": [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "size": p.size,
                    "createTime": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
                }
                for p in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def get_cloud_plans(self, page: int, page_size: int,
                              sort_field: str | None = None, sort_order: str | None = None) -> dict:
        items, total = await self.plan_repo.get_cloud(
            page, page_size, sort_field, sort_order
        )
        return {
            "list": [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "size": p.size,
                    "createTime": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
                }
                for p in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }
