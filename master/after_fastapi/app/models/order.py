import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

TZ = timezone(timedelta(hours=8))


class Order(Base, UUIDMixin):
    """订单"""
    __tablename__ = "orders"

    order_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    trade_status: Mapped[str] = mapped_column(String(32), nullable=False)  # pending/paid/cancelled
    time: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(TZ), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    user = relationship("User", back_populates="orders")
