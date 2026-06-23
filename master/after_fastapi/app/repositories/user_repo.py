import uuid

from sqlalchemy import select # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_phone(self, phone: str) -> User | None:
        stmt = select(User).where(User.phone == phone)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        phone: str,
        password_hash: str,
        real_name: str,
        role: str,
        job: str | None = None,
        subject: str | None = None,
    ) -> User:
        user = User(
            id=uuid.uuid4(),
            phone=phone,
            password_hash=password_hash,
            real_name=real_name,
            role=role,
            job=job,
            subject=subject,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
