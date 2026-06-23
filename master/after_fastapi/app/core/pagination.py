from typing import Any

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """统一分页参数"""
    page: int = Field(default=1, ge=1, description="页码，从 1 开始")
    pageSize: int = Field(default=15, ge=1, le=100, description="每页条数")


class SortParams(BaseModel):
    """统一排序参数"""
    sortField: str | None = Field(default=None, description="排序字段")
    sortOrder: str | None = Field(default=None, description="排序方向: asc 或 desc")


def paginate(
    items: list[Any],
    total: int,
    page: int,
    page_size: int,
) -> dict:
    """构建统一的分页响应 { list, total, page, pageSize }"""
    return {
        "list": items,
        "total": total,
        "page": page,
        "pageSize": page_size,
    }
