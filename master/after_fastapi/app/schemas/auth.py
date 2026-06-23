from pydantic import BaseModel, Field


# ── 请求模型 ──

class LoginRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
    password: str = Field(..., min_length=6, max_length=20)


class SendCodeRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
    type: str = Field(..., pattern=r"^(register|forgot)$")


class RegisterTeacherRequest(BaseModel):
    job: str = Field(..., description="职务")
    realName: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=6, max_length=20)
    subject: str = Field(..., description="学科")
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
    code: str = Field(..., min_length=4, max_length=6)


class RegisterStudentRequest(BaseModel):
    realName: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=6, max_length=20)
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
    code: str = Field(..., min_length=4, max_length=6)


class ForgotVerifyRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
    code: str = Field(..., min_length=4, max_length=6)


class ForgotResetRequest(BaseModel):
    password: str = Field(..., min_length=6, max_length=20)


# ── 响应模型 ──

class UserInfo(BaseModel):
    id: str
    name: str
    role: str
    phone: str
    job: str | None = None
    subject: str | None = None
    realName: str = ""

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    token: str
    userInfo: UserInfo
