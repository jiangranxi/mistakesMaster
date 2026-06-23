import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequest, NotFound
from app.repositories.class_repo import ClassRepository


class ClassService:
    """班级管理业务逻辑"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_repo = ClassRepository(db)

    async def get_created_classes(self, teacher_id: uuid.UUID) -> list[dict]:
        classes = await self.class_repo.get_created_by_teacher(teacher_id)
        result = []
        for c in classes:
            count = await self.class_repo.get_student_count(c.id)
            result.append({
                "id": str(c.id),
                "name": c.name,
                "code": c.code,
                "studentCount": count,
                "description": c.description,
                "createdAt": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
            })
        return result

    async def get_joined_classes(self, teacher_id: uuid.UUID) -> list[dict]:
        classes = await self.class_repo.get_joined_by_teacher(teacher_id)
        result = []
        for c in classes:
            count = await self.class_repo.get_student_count(c.id)
            result.append({
                "id": str(c.id),
                "name": c.name,
                "teacherName": c.teacher.real_name if c.teacher else "",
                "studentCount": count,
            })
        return result

    async def create_class(self, teacher_id: uuid.UUID, name: str, description: str | None) -> dict:
        cls = await self.class_repo.create_class(teacher_id, name, description)
        return {"id": str(cls.id), "code": cls.code}

    async def join_class(self, user_id: uuid.UUID, code: str, message: str | None) -> dict:
        cls = await self.class_repo.get_by_code(code)
        if not cls:
            raise NotFound("班级不存在或班级码错误")

        already = await self.class_repo.is_student_in_class(cls.id, user_id)
        if already:
            raise BadRequest("你已加入该班级")

        await self.class_repo.add_student(cls.id, user_id)
        return {"message": "加入成功"}

    async def get_class_detail(self, class_id: uuid.UUID) -> dict:
        cls = await self.class_repo.get_with_teacher(class_id)
        if not cls:
            raise NotFound("班级不存在")
        count = await self.class_repo.get_student_count(class_id)
        return {
            "id": str(cls.id),
            "name": cls.name,
            "description": cls.description,
            "code": cls.code,
            "teacherName": cls.teacher.real_name if cls.teacher else "",
            "studentCount": count,
            "createdAt": cls.created_at.strftime("%Y-%m-%d %H:%M:%S") if cls.created_at else None,
        }

    async def get_class_students(self, class_id: uuid.UUID) -> list[dict]:
        cls = await self.class_repo.get_by_id(class_id)
        if not cls:
            raise NotFound("班级不存在")
        return await self.class_repo.get_students(class_id)
