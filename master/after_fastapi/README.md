# 错题通 (MistakesMaster) 后端 API

FastAPI + SQLAlchemy 2.0 异步后端，为错题通教育平台提供 REST API。

## 快速启动

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务（开发环境使用 SQLite，无需额外数据库）
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

## 技术栈

| 组件 | 选型 |
|------|------|
| Web 框架 | FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 (async) |
| 数据库 | SQLite (开发) / MySQL (生产) |
| 认证 | JWT (python-jose) + bcrypt |
| 配置 | pydantic-settings |

## 项目结构

```
app/
├── main.py            # FastAPI 入口
├── config.py          # 配置管理
├── database.py        # 数据库连接
├── dependencies.py    # 依赖注入（认证/权限）
├── core/              # 安全、异常、分页
├── models/            # SQLAlchemy ORM 模型 (14 张表)
├── schemas/           # Pydantic 请求/响应模型
├── routers/           # API 路由层
│   ├── auth.py        # 认证 (7 端点)
│   ├── teacher/       # 教师端 (班级/作业/教案/讲评)
│   ├── student/       # 学生端 (作业)
│   ├── books.py       # 习题集
│   ├── member.py      # 会员中心
│   └── messages.py    # 消息管理
├── services/          # 业务逻辑层
└── repositories/      # 数据访问层
```

## API 模块

- `/auth/*` — 登录/注册/忘记密码
- `/teacher/classes/*` — 班级管理
- `/teacher/homework/*` — 教师端作业
- `/teacher/lesson-plans/*` — 教案管理
- `/teacher/review/*` — 讲评
- `/student/homework/*` — 学生端作业
- `/books/*` — 习题集
- `/member/*` — 会员中心
- `/messages/*` — 消息管理

## 环境变量

复制 `.env.example` 为 `.env` 并按需修改：

- `DATABASE_URL` — 默认 SQLite，生产环境改为 PostgreSQL
- `JWT_SECRET_KEY` — 生产环境务必更换为随机密钥
- `DEBUG` — 开启 SQLAlchemy echo 日志
