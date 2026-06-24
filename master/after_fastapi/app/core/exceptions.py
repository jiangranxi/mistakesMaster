from fastapi import HTTPException


class AppException(HTTPException):
    """应用自定义异常基类，前端通过 e.response.data.message 读取错误信息"""

    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)


class BadRequest(AppException):
    """400 - 请求参数错误"""
    def __init__(self, message: str = "参数错误"):
        super().__init__(status_code=400, message=message)


class Unauthorized(AppException):
    """401 - 未登录或 Token 过期"""
    def __init__(self, message: str = "请先登录"):
        super().__init__(status_code=401, message=message)


class Forbidden(AppException):
    """403 - 无权限"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(status_code=403, message=message)


class NotFound(AppException):
    """404 - 资源不存在"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(status_code=404, message=message)


class Conflict(AppException):
    """409 - 资源冲突（如手机号已注册）"""
    def __init__(self, message: str = "资源已存在"):
        super().__init__(status_code=409, message=message)


class TooManyRequests(AppException):
    """429 - 请求过于频繁"""
    def __init__(self, message: str = "请求过于频繁，请稍后再试"):
        super().__init__(status_code=429, message=message)
