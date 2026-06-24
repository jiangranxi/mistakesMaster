from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin

TZ = timezone(timedelta(hours=8))


class SmsCode(Base, UUIDMixin):
    """短信验证码"""
    __tablename__ = "sms_codes"

    phone: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    type: Mapped[str] = mapped_column(String(16), nullable=False)  # 'register' | 'forgot'
    device_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # 忘记密码中间态
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(TZ), nullable=False
    )
