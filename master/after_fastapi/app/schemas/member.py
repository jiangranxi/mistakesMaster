from pydantic import BaseModel, Field


class UpdateProfileRequest(BaseModel):
    realName: str | None = None
    birthday: str | None = None
    gender: str | None = None
    email: str | None = None
    province: str | None = None
    city: str | None = None
    district: str | None = None
    subject: str | None = None  # 仅教师


class ChangePasswordRequest(BaseModel):
    oldPassword: str = Field(..., min_length=6, max_length=20)
    newPassword: str = Field(..., min_length=6, max_length=20)


class OrderFilter(BaseModel):
    page: int = Field(default=1, ge=1)
    pageSize: int = Field(default=15, ge=1, le=100)
    status: str = Field(default="all")
