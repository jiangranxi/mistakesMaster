from pydantic import BaseModel, Field
from app.schemas.common import PaginationParams


# ── 请求模型 ──

class TeacherHomeworkListParams(PaginationParams):
    pass


class AssignHomeworkRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=256)
    source: str | None = None
    subject: str | None = None
    classId: str = Field(...)
    bookId: str | None = None
    deadline: str | None = None
    totalScore: int = Field(default=100)


class StudentHomeworkFilter(PaginationParams):
    book: str | None = Field(default=None, alias="book")
    name: str | None = Field(default=None)
    time: str | None = Field(default=None)
    startTime: str | None = Field(default=None)
    endTime: str | None = Field(default=None)
    sortField: str | None = Field(default=None)
    sortOrder: str | None = Field(default=None)

    model_config = {"populate_by_name": True}


class SubmitHomeworkRequest(BaseModel):
    content: dict | None = None  # 作答内容 JSON


# ── 响应模型 ──

class HomeworkInfo(BaseModel):
    id: str
    className: str | None = None
    name: str
    source: str | None = None
    subject: str | None = None
    createTime: str | None = None
    deadline: str | None = None

    model_config = {"from_attributes": True}


class HomeworkHistoryItem(BaseModel):
    id: str
    name: str
    source: str | None = None
    subject: str | None = None
    submitTime: str | None = None
    totalScore: int = 0
    myScore: int = 0
    rank: int | None = None

    model_config = {"from_attributes": True}


class ErrorItem(BaseModel):
    id: str
    name: str
    source: str | None = None
    subject: str | None = None
    submitTime: str | None = None
    errorSeq: int | None = None

    model_config = {"from_attributes": True}
