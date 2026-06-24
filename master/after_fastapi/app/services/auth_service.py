import logging

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import timedelta

from app.core.exceptions import BadRequest, Conflict, NotFound
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.models.profile import Profile
from app.repositories.user_repo import UserRepository
from app.services.sms_service import SmsService

logger = logging.getLogger(__name__)


class AuthService:
    """认证业务逻辑"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.sms_service = SmsService(db)

    async def login(self, phone: str, password: str) -> dict:
        """登录，返回 { token, userInfo }"""
        user = await self.user_repo.get_by_phone(phone)
        if not user or not verify_password(password, user.password_hash):
            raise BadRequest("手机号或密码错误")
        if not user.is_active:
            raise BadRequest("账号已被禁用")

        token = create_access_token({"sub": str(user.id), "role": user.role})
        return {"token": token, "userInfo": self._to_user_info(user)}

    async def send_sms_code(self, phone: str, code_type: str, device_id: str | None = None) -> str:
        """发送短信验证码"""
        return await self.sms_service.send_code(phone, code_type, device_id)

    async def register_teacher(self, data) -> User:
        """教师注册"""
        await self._verify_sms(data.phone, data.code, "register")
        await self._check_phone_unique(data.phone)

        password_hash = hash_password(data.password)
        user = await self.user_repo.create_user(
            phone=data.phone,
            password_hash=password_hash,
            real_name=data.realName,
            role="teacher",
            job=data.job,
            subject=data.subject,
        )
        # 创建 profile
        profile = Profile(user_id=user.id)
        self.db.add(profile)
        await self.db.flush()
        return user

    async def register_student(self, data) -> User:
        """学生注册"""
        await self._verify_sms(data.phone, data.code, "register")
        await self._check_phone_unique(data.phone)

        password_hash = hash_password(data.password)
        user = await self.user_repo.create_user(
            phone=data.phone,
            password_hash=password_hash,
            real_name=data.realName,
            role="student",
        )
        profile = Profile(user_id=user.id)
        self.db.add(profile)
        await self.db.flush()
        return user

    async def forgot_verify(self, phone: str, code: str) -> dict:
        """忘记密码 - 验证身份"""
        sms = await self.sms_service.verify_code_for_forgot(phone, code)
        if not sms:
            raise BadRequest("验证码错误或已过期")
        await self.sms_service.mark_verified(sms)
        return {"message": "验证通过"}

    async def forgot_reset(self, password: str) -> None:
        """忘记密码 - 重置密码（基于最近验证通过的记录）"""
        sms = await self.sms_service.get_recent_verified()
        if not sms:
            raise BadRequest("请先验证手机号")
        user = await self.user_repo.get_by_phone(sms.phone)
        if not user:
            raise BadRequest("用户不存在")
        user.password_hash = hash_password(password)
        await self.sms_service.mark_used(sms)
        await self.db.flush()

    async def get_user_info(self, user: User) -> dict:
        """获取当前用户信息"""
        return self._to_user_info(user)

    # ── 私有方法 ──

    async def _verify_sms(self, phone: str, code: str, code_type: str) -> None:
        sms = await self.sms_service.verify_code(phone, code, code_type)
        if sms is None:
            raise BadRequest("验证码错误或已过期")
        await self.sms_service.mark_used(sms)

    async def _check_phone_unique(self, phone: str) -> None:
        existing = await self.user_repo.get_by_phone(phone)
        if existing:
            raise Conflict("该手机号已注册")

    @staticmethod
    def _to_user_info(user: User) -> dict:
        return {
            "id": str(user.id),
            "name": user.real_name,
            "realName": user.real_name,
            "role": user.role,
            "phone": user.phone,
            "job": user.job,
            "subject": user.subject,
        }
