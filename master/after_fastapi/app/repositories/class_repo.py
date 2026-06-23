import uuid
import random
import string

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.class_ import Class, ClassStudent
from app.models.user import User
from app.repositories.base import BaseRepository


class ClassRepository(BaseRepository[Class]):
    model = Class

    async def get_by_code(self, code: str) -> Class | None:
        stmt = select(Class).where(Class.code == code)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_teacher(self, class_id: uuid.UUID) -> Class | None:
        stmt = select(Class).options(selectinload(Class.teacher)).where(Class.id == class_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_created_by_teacher(self, teacher_id: uuid.UUID) -> list[Class]:
        stmt = select(Class).where(Class.teacher_id == teacher_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_joined_by_teacher(self, teacher_id: uuid.UUID) -> list[Class]:
        """教师作为成员加入的班级"""
        stmt = (
            select(Class)
            .options(selectinload(Class.teacher))
            .join(ClassStudent, ClassStudent.class_id == Class.id)
            .where(ClassStudent.student_id == teacher_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_student_count(self, class_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(ClassStudent).where(
            ClassStudent.class_id == class_id
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_students(self, class_id: uuid.UUID) -> list[dict]:
        stmt = (
            select(User, ClassStudent.joined_at)
            .join(ClassStudent, ClassStudent.student_id == User.id)
            .where(ClassStudent.class_id == class_id)
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        return [
            {
                "id": str(row[0].id),
                "name": row[0].real_name,
                "phone": row[0].phone,
                "joinedAt": row[1].strftime("%Y-%m-%d %H:%M:%S") if row[1] else None,
            }
            for row in rows
        ]

    async def create_class(self, teacher_id: uuid.UUID, name: str, description: str | None = None) -> Class:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        cls = Class(
            id=uuid.uuid4(),
            name=name,
            description=description,
            code=code,
            teacher_id=teacher_id,
        )
        self.db.add(cls)
        await self.db.flush()
        await self.db.refresh(cls)
        return cls

    async def add_student(self, class_id: uuid.UUID, student_id: uuid.UUID) -> ClassStudent:
        cs = ClassStudent(
            id=uuid.uuid4(),
            class_id=class_id,
            student_id=student_id,
        )
        self.db.add(cs)
        await self.db.flush()
        return cs

    async def is_student_in_class(self, class_id: uuid.UUID, student_id: uuid.UUID) -> bool:
        stmt = select(ClassStudent).where(
            ClassStudent.class_id == class_id,
            ClassStudent.student_id == student_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None
