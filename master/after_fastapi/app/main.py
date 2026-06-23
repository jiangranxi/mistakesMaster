from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.core.exceptions import AppException
from app.database import engine
from app.models import Base
from app.routers import auth, books, member, messages
from app.routers.teacher import classes, homework as t_homework, lesson_plans, review
from app.routers.student import classes as s_classes, homework as s_homework


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期 - 启动时自动建表"""
    # 开发阶段自动建表，生产环境应使用 Alembic 迁移
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)

# 教师端
app.include_router(classes.router, prefix="/teacher")
app.include_router(t_homework.router, prefix="/teacher")
app.include_router(lesson_plans.router, prefix="/teacher")
app.include_router(review.router, prefix="/teacher")

# 学生端
app.include_router(s_classes.router, prefix="/student")
app.include_router(s_homework.router, prefix="/student")

# 通用模块
app.include_router(books.router)
app.include_router(member.router)
app.include_router(messages.router)


# 全局异常处理
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误"},
    )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
