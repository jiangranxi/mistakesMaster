from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置，支持 .env 文件和环境变量"""

    APP_NAME: str = "MistakesMaster"
    DEBUG: bool = False

    # 数据库（默认 MySQL，可选 SQLite / PostgreSQL）
    DATABASE_URL: str = "mysql+asyncmy://root:115900@localhost:3306/mistakes"

    # JWT
    JWT_SECRET_KEY: str = "change-me-to-a-random-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 小时

    # Redis（可选）
    REDIS_URL: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
