from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    SendCodeRequest,
    RegisterTeacherRequest,
    RegisterStudentRequest,
    ForgotVerifyRequest,
    ForgotResetRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """学生和教师共用登录入口，后端根据手机号判断角色"""
    service = AuthService(db)
    return await service.login(req.phone, req.password)


@router.post("/send-code")
async def send_code(req: SendCodeRequest, db: AsyncSession = Depends(get_db)):
    """发送短信验证码（注册/忘记密码）"""
    service = AuthService(db)
    code = await service.send_sms_code(req.phone, req.type, req.deviceId)
    print(code)
    return {"message": f"验证码已发送: {code}"}


@router.post("/register/teacher")
async def register_teacher(req: RegisterTeacherRequest, db: AsyncSession = Depends(get_db)):
    """教师注册"""
    service = AuthService(db)
    await service.register_teacher(req)
    return {"message": "注册成功"}


@router.post("/register/student")
async def register_student(req: RegisterStudentRequest, db: AsyncSession = Depends(get_db)):
    """学生注册"""
    service = AuthService(db)
    await service.register_student(req)
    return {"message": "注册成功"}


@router.post("/forgot/verify")
async def forgot_verify(req: ForgotVerifyRequest, db: AsyncSession = Depends(get_db)):
    """忘记密码 - 验证手机号和验证码，返回临时令牌"""
    service = AuthService(db)
    result = await service.forgot_verify(req.phone, req.code)
    return result


@router.post("/forgot/reset")
async def forgot_reset(req: ForgotResetRequest, db: AsyncSession = Depends(get_db)):
    """忘记密码 - 重置密码"""
    service = AuthService(db)
    await service.forgot_reset(req.password)
    return {"message": "密码重置成功"}


@router.get("/userinfo")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return AuthService._to_user_info(current_user)
