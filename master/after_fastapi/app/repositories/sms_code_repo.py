import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sms_code import SmsCode
from app.repositories.base import BaseRepository

TZ = timezone(timedelta(hours=8))


class SmsCodeRepository(BaseRepository[SmsCode]):
    model = SmsCode

    async def create_code(self, phone: str, code: str, code_type: str, ttl_minutes: int = 5) -> SmsCode:
        sms = SmsCode(
            id=uuid.uuid4(),
            phone=phone,
            code=code,
            type=code_type,
            expires_at=datetime.now(TZ) + timedelta(minutes=ttl_minutes),
        )
        self.db.add(sms)
        await self.db.flush()
        return sms

    async def get_valid_code(self, phone: str, code: str, code_type: str) -> SmsCode | None:
        stmt = (
            select(SmsCode)
            .where(
                SmsCode.phone == phone,
                SmsCode.code == code,
                SmsCode.type == code_type,
                SmsCode.used == False,
                SmsCode.expires_at > datetime.now(TZ),
            )
            .order_by(SmsCode.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_used(self, sms: SmsCode) -> None:
        sms.used = True
        await self.db.flush()

    async def mark_verified(self, sms: SmsCode) -> None:
        """忘记密码流程: 标记验证码已验证（未使用）"""
        sms.verified = True
        await self.db.flush()

    async def get_recent_verified(self) -> SmsCode | None:
        """获取最近验证通过但未重置的忘记密码验证码（10分钟内）"""
        cutoff = datetime.now(TZ) - timedelta(minutes=10)
        stmt = (
            select(SmsCode)
            .where(
                SmsCode.type == "forgot",
                SmsCode.verified == True,
                SmsCode.used == False,
                SmsCode.created_at > cutoff,
            )
            .order_by(SmsCode.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()
