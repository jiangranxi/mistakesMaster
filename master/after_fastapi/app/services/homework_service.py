import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequest, NotFound
from app.repositories.homework_repo import HomeworkRepository, StudentHomeworkRepository, ErrorItemRepository


class HomeworkService:
    """教师端作业服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.homework_repo = HomeworkRepository(db)

    async def get_own_homework(self, teacher_id: uuid.UUID, page: int, page_size: int) -> dict:
        items, total = await self.homework_repo.get_by_teacher(teacher_id, page, page_size)
        return {
            "list": [
                {
                    "id": str(h.id),
                    "name": h.name,
                    "source": h.source,
                    "subject": h.subject,
                    "createTime": h.created_at.strftime("%Y-%m-%d %H:%M:%S") if h.created_at else None,
                }
                for h in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def get_cloud_homework(self, page: int, page_size: int) -> dict:
        items, total = await self.homework_repo.get_cloud_homework(page, page_size)
        return {
            "list": [
                {
                    "id": str(h.id),
                    "name": h.name,
                    "source": h.source,
                    "subject": h.subject,
                }
                for h in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def get_my_papers(self, teacher_id: uuid.UUID, page: int, page_size: int) -> dict:
        items, total = await self.homework_repo.get_by_teacher(teacher_id, page, page_size)
        return {
            "list": [
                {
                    "id": str(h.id),
                    "name": h.name,
                    "subject": h.subject,
                    "createdAt": h.created_at.strftime("%Y-%m-%d %H:%M:%S") if h.created_at else None,
                }
                for h in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def get_chapters(self, homework_id: uuid.UUID) -> list:
        """获取作业关联的章节（从习题集获取）"""
        hw = await self.homework_repo.get_by_id(homework_id)
        if not hw:
            raise NotFound("作业不存在")
        # 简化：返回空列表或从关联习题集获取
        return []

    async def assign_homework(self, teacher_id: uuid.UUID, data) -> dict:
        class_id = uuid.UUID(data.classId)
        book_id = uuid.UUID(data.bookId) if data.bookId else None
        hw = await self.homework_repo.create_homework(
            teacher_id=teacher_id,
            name=data.name,
            class_id=class_id,
            source=data.source,
            subject=data.subject,
            book_id=book_id,
            deadline_str=data.deadline,
            total_score=data.totalScore,
        )
        return {"id": str(hw.id), "message": "布置成功"}


class StudentHomeworkService:
    """学生端作业服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.student_hw_repo = StudentHomeworkRepository(db)
        self.error_repo = ErrorItemRepository(db)

    async def get_latest(self, student_id: uuid.UUID, page: int, page_size: int) -> dict:
        items, total = await self.student_hw_repo.get_latest(student_id, page, page_size)
        return {"list": items, "total": total, "page": page, "pageSize": page_size}

    async def get_history(self, student_id: uuid.UUID, page: int, page_size: int,
                          book: str | None = None, name: str | None = None,
                          time: str | None = None, sort_field: str | None = None,
                          sort_order: str | None = None) -> dict:
        items, total = await self.student_hw_repo.get_by_student(
            student_id, page, page_size,
            name=name, book=book,
            sort_field=sort_field, sort_order=sort_order,
            is_history=True,
        )
        return {"list": items, "total": total, "page": page, "pageSize": page_size}

    async def get_errors(self, student_id: uuid.UUID, page: int, page_size: int,
                         name: str | None = None, book: str | None = None,
                         start_time: str | None = None, end_time: str | None = None,
                         sort_field: str | None = None, sort_order: str | None = None) -> dict:
        items, total = await self.error_repo.get_by_student(
            student_id, page, page_size,
            name=name, book=book,
            start_time=start_time, end_time=end_time,
            sort_field=sort_field, sort_order=sort_order,
        )
        return {
            "list": [
                {
                    "id": str(e.id),
                    "name": e.name,
                    "source": e.source,
                    "subject": e.subject,
                    "submitTime": e.submit_time.strftime("%Y-%m-%d %H:%M:%S") if e.submit_time else None,
                    "errorSeq": e.error_seq,
                }
                for e in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }

    async def submit(self, student_id: uuid.UUID, homework_id: uuid.UUID, content: dict | None) -> dict:
        await self.student_hw_repo.submit(homework_id, student_id, content or {})
        return {"message": "提交成功"}

    async def get_correction(self, student_id: uuid.UUID, homework_id: uuid.UUID) -> dict:
        result = await self.student_hw_repo.get_correction(homework_id, student_id)
        if not result:
            raise NotFound("批改结果不存在")
        return result

    async def get_report(self, student_id: uuid.UUID, homework_id: uuid.UUID) -> dict:
        result = await self.student_hw_repo.get_report(homework_id, student_id)
        if not result:
            raise NotFound("报告不存在")
        return result
