import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.homework import Homework, StudentHomework, ErrorItem
from app.repositories.base import BaseRepository

TZ = timezone(timedelta(hours=8))


class HomeworkRepository(BaseRepository[Homework]):
    model = Homework

    async def get_by_teacher(self, teacher_id: uuid.UUID, page: int = 1, page_size: int = 15) -> tuple[list[Homework], int]:
        offset = (page - 1) * page_size
        stmt = select(Homework).where(Homework.teacher_id == teacher_id).offset(offset).limit(page_size).order_by(desc(Homework.created_at))
        count_stmt = select(func.count()).select_from(Homework).where(Homework.teacher_id == teacher_id)
        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0

    async def get_cloud_homework(self, page: int = 1, page_size: int = 15) -> tuple[list[Homework], int]:
        offset = (page - 1) * page_size
        stmt = select(Homework).where(Homework.source == "cloud").offset(offset).limit(page_size).order_by(desc(Homework.created_at))
        count_stmt = select(func.count()).select_from(Homework).where(Homework.source == "cloud")
        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0

    async def create_homework(self, teacher_id: uuid.UUID, name: str, class_id: uuid.UUID,
                              source: str | None = None, subject: str | None = None,
                              book_id: uuid.UUID | None = None, deadline_str: str | None = None,
                              total_score: int = 100) -> Homework:
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.fromisoformat(deadline_str)
            except (ValueError, TypeError):
                pass

        hw = Homework(
            id=uuid.uuid4(),
            name=name,
            source=source,
            subject=subject,
            class_id=class_id,
            teacher_id=teacher_id,
            book_id=book_id,
            deadline=deadline,
            total_score=total_score,
        )
        self.db.add(hw)
        await self.db.flush()
        await self.db.refresh(hw)
        return hw

    async def get_by_class(self, class_id: uuid.UUID, page: int = 1, page_size: int = 15) -> tuple[list[Homework], int]:
        offset = (page - 1) * page_size
        stmt = select(Homework).where(Homework.class_id == class_id).offset(offset).limit(page_size).order_by(desc(Homework.created_at))
        count_stmt = select(func.count()).select_from(Homework).where(Homework.class_id == class_id)
        result = await self.db.execute(stmt)
        count_result = await self.db.execute(count_stmt)
        return list(result.scalars().all()), count_result.scalar() or 0


class StudentHomeworkRepository(BaseRepository[StudentHomework]):
    model = StudentHomework

    async def get_by_student(self, student_id: uuid.UUID, page: int = 1, page_size: int = 15,
                             name: str | None = None, book: str | None = None,
                             start_time: str | None = None, end_time: str | None = None,
                             sort_field: str | None = None, sort_order: str | None = None,
                             is_history: bool = True) -> tuple[list[dict], int]:
        offset = (page - 1) * page_size
        stmt = (
            select(StudentHomework, Homework.name, Homework.source, Homework.subject)
            .join(Homework, StudentHomework.homework_id == Homework.id)
            .where(StudentHomework.student_id == student_id)
        )

        if is_history:
            stmt = stmt.where(StudentHomework.submit_time.isnot(None))
        else:
            stmt = stmt.where(StudentHomework.submit_time.is_(None))

        if name:
            stmt = stmt.where(Homework.name.ilike(f"%{name}%"))
        if book:
            stmt = stmt.where(Homework.source.ilike(f"%{book}%"))
        if start_time:
            stmt = stmt.where(StudentHomework.submit_time >= datetime.fromisoformat(start_time))
        if end_time:
            stmt = stmt.where(StudentHomework.submit_time <= datetime.fromisoformat(end_time))

        count_stmt = select(func.count()).select_from(StudentHomework).join(Homework).where(StudentHomework.student_id == student_id)

        # 排序
        order_col = None
        if sort_field == "submitTime":
            order_col = StudentHomework.submit_time
        elif sort_field == "totalScore":
            order_col = StudentHomework.total_score
        elif sort_field == "myScore":
            order_col = StudentHomework.my_score
        elif sort_field == "name":
            order_col = Homework.name
        elif sort_field == "subject":
            order_col = Homework.subject

        if order_col is not None:
            stmt = stmt.order_by(asc(order_col) if sort_order == "asc" else desc(order_col))
        else:
            stmt = stmt.order_by(desc(StudentHomework.submit_time))

        stmt = stmt.offset(offset).limit(page_size)
        result = await self.db.execute(stmt)
        rows = result.all()
        count_result = await self.db.execute(count_stmt)

        items = [
            {
                "id": str(row[0].id),
                "name": row[1],
                "source": row[2],
                "subject": row[3],
                "submitTime": row[0].submit_time.strftime("%Y-%m-%d %H:%M:%S") if row[0].submit_time else None,
                "totalScore": row[0].total_score,
                "myScore": row[0].my_score,
                "rank": row[0].rank,
            }
            for row in rows
        ]
        return items, count_result.scalar() or 0

    async def get_latest(self, student_id: uuid.UUID, page: int = 1, page_size: int = 15) -> tuple[list[dict], int]:
        """获取最新作业（未提交的）"""
        return await self.get_by_student(student_id, page, page_size, is_history=False)

    async def submit(self, homework_id: uuid.UUID, student_id: uuid.UUID, content: dict) -> StudentHomework:
        stmt = select(StudentHomework).where(
            StudentHomework.homework_id == homework_id,
            StudentHomework.student_id == student_id,
        )
        result = await self.db.execute(stmt)
        sh = result.scalar_one_or_none()

        if not sh:
            sh = StudentHomework(
                id=uuid.uuid4(),
                homework_id=homework_id,
                student_id=student_id,
                submit_content=content,
                submit_time=datetime.now(TZ),
            )
            self.db.add(sh)
        else:
            sh.submit_content = content
            sh.submit_time = datetime.now(TZ)

        await self.db.flush()
        await self.db.refresh(sh)
        return sh

    async def get_correction(self, homework_id: uuid.UUID, student_id: uuid.UUID) -> dict | None:
        stmt = select(StudentHomework).where(
            StudentHomework.homework_id == homework_id,
            StudentHomework.student_id == student_id,
        )
        result = await self.db.execute(stmt)
        sh = result.scalar_one_or_none()
        if not sh:
            return None
        return {
            "id": str(sh.id),
            "totalScore": sh.total_score,
            "myScore": sh.my_score,
            "rank": sh.rank,
            "submitContent": sh.submit_content,
            "submitTime": sh.submit_time.strftime("%Y-%m-%d %H:%M:%S") if sh.submit_time else None,
        }

    async def get_report(self, homework_id: uuid.UUID, student_id: uuid.UUID) -> dict | None:
        """作业报告（含错题）"""
        correction = await self.get_correction(homework_id, student_id)
        if not correction:
            return None

        # 获取错题
        stmt = select(ErrorItem).where(
            ErrorItem.student_id == student_id,
            ErrorItem.homework_id == homework_id,
        )
        result = await self.db.execute(stmt)
        errors = result.scalars().all()

        correction["errors"] = [
            {
                "id": str(e.id),
                "name": e.name,
                "errorSeq": e.error_seq,
            }
            for e in errors
        ]
        return correction


class ErrorItemRepository(BaseRepository[ErrorItem]):
    model = ErrorItem

    async def get_by_student(self, student_id: uuid.UUID, page: int = 1, page_size: int = 15,
                             name: str | None = None, book: str | None = None,
                             start_time: str | None = None, end_time: str | None = None,
                             sort_field: str | None = None, sort_order: str | None = None) -> tuple[list[ErrorItem], int]:
        offset = (page - 1) * page_size
        stmt = select(ErrorItem).where(ErrorItem.student_id == student_id)

        if name:
            stmt = stmt.where(ErrorItem.name.ilike(f"%{name}%"))
        if book:
            stmt = stmt.where(ErrorItem.source.ilike(f"%{book}%"))
        if start_time:
            stmt = stmt.where(ErrorItem.submit_time >= datetime.fromisoformat(start_time))
        if end_time:
            stmt = stmt.where(ErrorItem.submit_time <= datetime.fromisoformat(end_time))

        count_stmt = select(func.count()).select_from(ErrorItem).where(ErrorItem.student_id == student_id)

        order_col = None
        if sort_field == "submitTime":
            order_col = ErrorItem.submit_time
        elif sort_field == "name":
            order_col = ErrorItem.name
        elif sort_field == "errorSeq":
            order_col = ErrorItem.error_seq

        if order_col is not None:
            stmt = stmt.order_by(asc(order_col) if sort_order == "asc" else desc(order_col))
        else:
            stmt = stmt.order_by(desc(ErrorItem.submit_time))

        stmt = stmt.offset(offset).limit(page_size)
        result = await self.db.execute(stmt)
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_stmt)
        return items, count_result.scalar() or 0
