import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import BadRequest, NotFound
from app.core.security import verify_password, hash_password
from app.models.user import User
from app.models.profile import Profile
from app.repositories.order_repo import OrderRepository
from datetime import date, datetime

class MemberService:
    """会员中心服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)

    async def get_profile(self, user: User) -> dict:
        stmt = select(Profile).where(Profile.user_id == user.id)
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        # 安全处理 birthday
        birthday = None
        if profile and profile.birthday:
            if isinstance(profile.birthday, (date, datetime)):
                birthday = profile.birthday.isoformat()
            else:
                birthday = profile.birthday  # 已经是字符串，直接使用

        return {
            "id": str(user.id),
            "accountId": str(user.id),
            "realName": user.real_name,
            "phone": user.phone,
            "role": user.role,
            "job": user.job,
            "subject": user.subject,
            "birthday": birthday,
            "gender": profile.gender if profile else "男",
            "email": profile.email if profile else None,
            "province": profile.province if profile else None,
            "city": profile.city if profile else None,
            "district": profile.district if profile else None,
        }

    async def update_profile(self, user: User, data: dict) -> dict:
        stmt = select(Profile).where(Profile.user_id == user.id)
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        if profile:
            # 1. 单独处理 birthday 字段
            birthday_val = data.get("birthday")
            if birthday_val == "":
                profile.birthday = None
            elif birthday_val is not None:
                profile.birthday = birthday_val

            for field in ["gender", "email", "province", "city", "district"]:
                value = data.get(field)
                if value is not None:
                    setattr(profile, field, value)
        else:
            profile = Profile(user_id=user.id)
            for field in ["birthday", "gender", "email", "province", "city", "district"]:
                value = data.get(field)
                if value is not None:
                    setattr(profile, field, value)
            self.db.add(profile)

        # 更新 real_name
        if data.get("realName"):
            user.real_name = data["realName"]
        # 教师可更新 subject
        if data.get("subject") and user.role == "teacher":
            user.subject = data["subject"]

        await self.db.flush()
        return await self.get_profile(user)

    async def change_password(self, user: User, old_password: str, new_password: str) -> None:
        if not verify_password(old_password, user.password_hash):
            raise BadRequest("原密码错误")
        user.password_hash = hash_password(new_password)
        await self.db.flush()

    async def get_orders(self, user_id: uuid.UUID, page: int, page_size: int,
                          status: str, sort_field: str | None = None,
                          sort_order: str | None = None) -> dict:
        items, total = await self.order_repo.get_by_user(
            user_id, page, page_size, status, sort_field, sort_order,
        )
        return {
            "list": [
                {
                    "id": str(o.id),
                    "orderNo": o.order_no,
                    "name": o.name,
                    "resourceType": o.resource_type,
                    "price": float(o.price) if o.price else 0,
                    "tradeStatus": o.trade_status,
                    "time": o.time.strftime("%Y-%m-%d %H:%M:%S") if o.time else None,
                }
                for o in items
            ],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }
