import random
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sms_code import SmsCode
from app.repositories.sms_code_repo import SmsCodeRepository

logger = logging.getLogger(__name__)


class SmsService:
    """短信验证码服务（开发期 mock，生产环境对接短信 SDK）"""

    def __init__(self, db: AsyncSession):
        self.sms_repo = SmsCodeRepository(db)

    async def send_code(self, phone: str, code_type: str) -> str:
        """
        生成并"发送"验证码。
        开发阶段：生成 6 位随机码，日志输出，存入数据库。
        """
        code = str(random.randint(100000, 999999))
        await self.sms_repo.create_code(phone, code, code_type)
        logger.info(f"[SMS Mock] 验证码已发送到 {phone}: {code} (类型: {code_type})")
        return code

    async def verify_code(self, phone: str, code: str, code_type: str) -> SmsCode | None:
        """校验验证码，返回 SmsCode 对象或 None"""
        sms = await self.sms_repo.get_valid_code(phone, code, code_type)
        if sms is None:
            return None
        return sms

    async def verify_code_for_forgot(self, phone: str, code: str) -> SmsCode | None:
        """校验忘记密码验证码"""
        return await self.sms_repo.get_valid_code(phone, code, "forgot")

    async def mark_used(self, sms: SmsCode) -> None:
        """标记验证码已使用"""
        await self.sms_repo.mark_used(sms)

    async def mark_verified(self, sms: SmsCode) -> None:
        """标记验证码已验证（忘记密码中间态）"""
        await self.sms_repo.mark_verified(sms)

    async def get_recent_verified(self) -> SmsCode | None:
        """获取最近验证通过的忘记密码记录"""
        return await self.sms_repo.get_recent_verified()
