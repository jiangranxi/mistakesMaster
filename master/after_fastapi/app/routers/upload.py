import uuid
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import BadRequest
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["文件上传"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """上传图片（封面等），返回静态资源 URL"""
    # 校验扩展名
    ext = Path(file.filename).suffix.lower() if file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise BadRequest("仅支持 JPG / PNG 格式")

    # 校验 MIME
    if file.content_type not in ALLOWED_MIMETYPES:
        raise BadRequest("仅支持 image/jpeg / image/png 格式")

    # 读取并校验大小
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise BadRequest(f"图片大小不能超过 {settings.MAX_UPLOAD_SIZE // (1024 * 1024)}MB")

    # 按月分目录，UUID 命名
    sub_dir = date.today().strftime("%Y%m")
    dest_dir = Path(settings.UPLOAD_DIR) / "covers" / sub_dir
    dest_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = dest_dir / filename
    with open(file_path, "wb") as f:
        f.write(content)

    url = f"/static/covers/{sub_dir}/{filename}"
    return {"url": url}
