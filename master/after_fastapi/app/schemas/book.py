from pydantic import BaseModel, Field


class UpdateBookRequest(BaseModel):
    """更新习题集请求"""
    cover: str | None = Field(default=None, max_length=512, description="封面图片 URL")
