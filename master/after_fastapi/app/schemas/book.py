from pydantic import BaseModel, Field


class UpdateBookRequest(BaseModel):
    """更新习题集请求"""
    cover: str | None = Field(default=None, max_length=512, description="封面图片 URL")


# ── 响应模型 ──

class ChapterNode(BaseModel):
    """章节树节点（递归结构）"""
    id: str
    name: str
    sortOrder: int = 0
    children: list["ChapterNode"] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class BookInfo(BaseModel):
    """习题集列表项 / 详情（含嵌套章节树）"""
    id: str
    name: str
    cover: str | None = None
    price: float = 0
    subject: str | None = None
    publisher: str | None = None
    version: str | None = None
    gradeTerm: str | None = None
    description: str | None = None
    updateTime: str | None = None
    chapters: list[ChapterNode] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class BookListResponse(BaseModel):
    """习题集列表分页响应"""
    list_: list[BookInfo] = Field(alias="list")
    total: int
    page: int
    pageSize: int

    model_config = {"populate_by_name": True}
