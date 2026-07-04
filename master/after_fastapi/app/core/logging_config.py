"""
日志配置模块 — 在 main.py 启动时调用 setup_logging() 完成全局日志初始化。

特性：
- 控制台 + 文件双输出，文件按天轮转
- 分离的应用日志 (app.log) 和错误日志 (error.log)
- 屏蔽 SQLAlchemy / asyncmy 等数据库组件的 INFO/WARNING 日志
- 级别和保留天数通过 config.Settings 控制
"""

import logging
import logging.config
import os

from app.config import settings


def _to_py_level(level: str) -> int:
    """将字符串日志级别转为 Python int 级别，默认 INFO"""
    return getattr(logging, level.upper(), logging.INFO)


LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)-5s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": os.path.join(settings.LOG_DIR, "app.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": settings.LOG_BACKUP_COUNT,
            "encoding": "utf-8",
        },
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": os.path.join(settings.LOG_DIR, "error.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": settings.LOG_ERROR_BACKUP_COUNT,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # ── 屏蔽数据库组件 INFO/WARNING ──
        "sqlalchemy.engine": {
            "level": "ERROR",
            "handlers": [],
            "propagate": True,
        },
        "sqlalchemy.pool": {
            "level": "ERROR",
            "handlers": [],
            "propagate": True,
        },
        "sqlalchemy.orm": {
            "level": "WARNING",
            "handlers": [],
            "propagate": True,
        },
        "sqlalchemy.dialects": {
            "level": "ERROR",
            "handlers": [],
            "propagate": True,
        },
        "asyncmy": {
            "level": "ERROR",
            "handlers": [],
            "propagate": True,
        },
        "aiomysql": {
            "level": "ERROR",
            "handlers": [],
            "propagate": True,
        },
        "aiosqlite": {
            "level": "ERROR",
            "handlers": [],
            "propagate": True,
        },
        # ── 请求日志 ──
        "app.access": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        # ── 慢查询检测 ──
        "sqlalchemy.slow": {
            "level": "WARNING",
            "handlers": ["console", "file", "error_file"],
            "propagate": False,
        },
        # ── Uvicorn ──
        "uvicorn.access": {
            "level": "INFO",
            "handlers": [],
            "propagate": True,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": [],
            "propagate": True,
        },
    },
    "root": {
        "level": _to_py_level(settings.LOG_LEVEL),
        "handlers": ["console", "file", "error_file"],
    },
}


def setup_logging() -> None:
    """初始化日志系统，创建 logs/ 目录并应用配置"""
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)
