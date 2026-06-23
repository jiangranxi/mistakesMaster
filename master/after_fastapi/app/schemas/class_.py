from pydantic import BaseModel, Field


# ── 请求模型 ──

class CreateClassRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = Field(default=None)


class JoinClassRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=12)
    message: str | None = Field(default=None)


# ── 响应模型 ──

class ClassInfo(BaseModel):
    id: str
    name: str
    description: str | None = None
    code: str | None = None
    teacherName: str | None = None
    studentCount: int = 0
    createdAt: str | None = None

    model_config = {"from_attributes": True}


class StudentInfo(BaseModel):
    id: str
    name: str
    phone: str
    joinedAt: str | None = None

    model_config = {"from_attributes": True}
