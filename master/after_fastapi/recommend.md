# 错题通后端项目文件说明

## 项目根目录

| 文件 | 用途 |
|------|------|
| `requirements.txt` | Python 依赖清单，包含 FastAPI、SQLAlchemy、bcrypt、JWT 等核心库及其版本号 |
| `pyproject.toml` | 项目元数据配置，定义项目名称、版本号、Python 版本要求及 pytest 配置 |
| `.env` | 环境变量配置文件（不提交 Git），存储数据库连接串、JWT 密钥等敏感信息 |
| `.env.example` | 环境变量模板文件，列出所有可配置项及默认值，供新开发者参考复制 |
| `README.md` | 项目说明文档，包含快速启动指南、技术栈介绍、目录结构说明 |

---

## `app/` — 应用核心

| 文件 | 用途 |
|------|------|
| `app/__init__.py` | Python 包标识文件 |
| `app/main.py` | **FastAPI 应用入口**。创建 app 实例、注册 CORS 中间件、挂载所有路由模块、配置全局异常处理器（AppException → 400+，Exception → 500）、启动时自动建表 |
| `app/config.py` | **配置管理**。使用 pydantic-settings 从 `.env` 文件加载所有配置项（数据库 URL、JWT 密钥/过期时间、调试模式），提供类型安全的全局 `settings` 单例 |
| `app/database.py` | **数据库连接**。创建 SQLAlchemy 异步引擎和会话工厂，SQLite 自动添加 `check_same_thread=False` 参数 |
| `app/dependencies.py` | **FastAPI 依赖注入**。提供三个核心依赖：`get_db`（每个请求获取一个数据库会话并自动提交/回滚）、`get_current_user`（从 Bearer Token 解析当前用户）、`require_role`（角色权限校验工厂函数） |

---

## `app/core/` — 核心基础设施

| 文件 | 用途 |
|------|------|
| `app/core/__init__.py` | Python 包标识文件 |
| `app/core/security.py` | **安全模块**。提供 `hash_password`（bcrypt 哈希）、`verify_password`（bcrypt 校验）、`create_access_token`（签发 JWT）、`decode_access_token`（解析 JWT）四个函数 |
| `app/core/exceptions.py` | **自定义异常类**。定义 `AppException` 基类及 `BadRequest(400)`、`Unauthorized(401)`、`Forbidden(403)`、`NotFound(404)`、`Conflict(409)` 子类，前端通过 `e.response.data.message` 读取错误信息 |
| `app/core/pagination.py` | **分页工具**。`PaginationParams`（page/pageSize 参数模型）、`SortParams`（sortField/sortOrder 排序参数）、`paginate` 函数（构建统一 `{list, total, page, pageSize}` 响应） |

---

## `app/models/` — ORM 数据模型（SQLAlchemy）

| 文件 | 用途 |
|------|------|
| `app/models/__init__.py` | 统一导出所有模型类，方便外部 `from app.models import User, Class, ...` |
| `app/models/base.py` | **ORM 基类**。定义 `Base`（声明式基类）、`UUIDMixin`（UUID 主键）、`TimestampMixin`（created_at/updated_at 时间戳）三个混入类 |
| `app/models/user.py` | **用户表** `users`。phone（手机号，唯一）、password_hash、real_name、role（teacher/student）、job（仅教师）、subject（仅教师）、is_active；关联 profile、created_classes、orders、messages |
| `app/models/profile.py` | **个人资料表** `profiles`。与 users 1:1 关联（user_id 为主键+外键），存储 birthday、gender、email、省市区 |
| `app/models/class_.py` | **班级表** `classes` + **班级学生关联表** `class_students`。班级含 name、code（随机8位班级码）、teacher_id；关联表含 (class_id, student_id) 唯一约束 |
| `app/models/homework.py` | **作业三表**：`homeworks`（教师布置的作业，含 name/class_id/deadline/total_score）、`student_homeworks`（学生作答记录，含 submit_content(JSON)/my_score/rank）、`error_items`（错题，含 error_seq） |
| `app/models/book.py` | **习题集表** `books` + **章节表** `book_chapters`。习题集含 name/cover/price/subject/publisher；章节支持树形结构（parent_id 自引用） |
| `app/models/lesson_plan.py` | **教案表** `lesson_plans`。含 name/size/file_url/teacher_id，is_cloud 字段区分自有教案和云端共享教案 |
| `app/models/review_report.py` | **讲评报告表** `review_reports`。含 seq/date/report/book 及 max/min/avg/median/mode 统计字段，type 区分 error_book/homework |
| `app/models/message.py` | **消息表** `messages`。含 from_user/role/content/is_read/user_id |
| `app/models/order.py` | **订单表** `orders`。含 order_no（唯一）/name/resource_type/price/trade_status/user_id |
| `app/models/sms_code.py` | **短信验证码表** `sms_codes`。含 phone/code/type（register/forgot）/used/verified/expires_at，verified 字段专用于忘记密码流程中间态 |

---

## `app/schemas/` — Pydantic 请求/响应模型

| 文件 | 用途 |
|------|------|
| `app/schemas/__init__.py` | Python 包标识文件 |
| `app/schemas/common.py` | **通用模型**。`PaginationParams`（分页参数 page/pageSize）、`SortParams`（排序参数 sortField/sortOrder），各接口通过 Depends 注入复用 |
| `app/schemas/auth.py` | **认证模型**。请求：LoginRequest、SendCodeRequest、RegisterTeacherRequest、RegisterStudentRequest、ForgotVerifyRequest、ForgotResetRequest；响应：UserInfo、LoginResponse |
| `app/schemas/class_.py` | **班级模型**。请求：CreateClassRequest、JoinClassRequest；响应：ClassInfo、StudentInfo |
| `app/schemas/homework.py` | **作业模型**。请求：AssignHomeworkRequest、StudentHomeworkFilter、SubmitHomeworkRequest；响应：HomeworkInfo、HomeworkHistoryItem、ErrorItem |
| `app/schemas/member.py` | **会员模型**。请求：UpdateProfileRequest、ChangePasswordRequest、OrderFilter |

---

## `app/routers/` — API 路由层

| 文件 | 用途 |
|------|------|
| `app/routers/__init__.py` | Python 包标识文件 |
| `app/routers/auth.py` | **认证路由** `/auth/*`。7 个端点：login（登录）、send-code（发送验证码）、register/teacher（教师注册）、register/student（学生注册）、forgot/verify（验证身份）、forgot/reset（重置密码）、userinfo（获取当前用户信息） |
| `app/routers/books.py` | **习题集路由** `/books`。2 个端点：GET /books（分页列表）、GET /books/:id（含章节的详情） |
| `app/routers/member.py` | **会员路由** `/member/*`。4 个端点：GET /profile（获取资料）、PUT /profile（修改资料）、PUT /password（修改密码）、GET /orders（订单列表，支持 status 筛选） |
| `app/routers/messages.py` | **消息路由** `/messages/*`。3 个端点：GET /messages（分页列表）、PUT /messages/:id/read（标记已读）、DELETE /messages/:id（删除） |
| `app/routers/teacher/__init__.py` | Python 包标识文件 |
| `app/routers/teacher/classes.py` | **班级管理路由** `/teacher/classes/*`。6 个端点：created（我创建的）、joined（我加入的）、POST /（创建）、POST /join（加入）、GET /:id（详情）、GET /:id/students（学生列表） |
| `app/routers/teacher/homework.py` | **教师作业路由** `/teacher/homework/*`。5 个端点：own（我的作业）、cloud（云端题库）、papers（我的组卷）、:id/chapters（章节）、assign（布置作业） |
| `app/routers/teacher/lesson_plans.py` | **教案路由** `/teacher/lesson-plans/*`。2 个端点：own（我的教案）、cloud（云端教案），均支持分页和排序 |
| `app/routers/teacher/review.py` | **讲评路由** `/teacher/review/*`。2 个端点：error-book（错题本讲评）、homework（作业讲评），支持多条件筛选（report/book/time/subject/class）和排序 |
| `app/routers/student/__init__.py` | Python 包标识文件 |
| `app/routers/student/homework.py` | **学生作业路由** `/student/homework/*`。6 个端点：latest（最新作业）、history（历史作业，支持筛选排序）、errors（错题集，支持筛选排序）、:id/submit（提交）、:id/correction（批改结果）、:id/report（作业报告含错题） |

---

## `app/services/` — 业务逻辑层

| 文件 | 用途 |
|------|------|
| `app/services/__init__.py` | Python 包标识文件 |
| `app/services/auth_service.py` | **认证服务**。处理登录（验证密码→签发JWT）、注册（验证码校验→密码哈希→创建用户+Profile）、忘记密码（验证码校验→标记验证→重置密码）全流程 |
| `app/services/sms_service.py` | **短信验证码服务**。send_code（生成6位随机码→存入DB→日志输出，生产环境对接短信SDK）、verify_code（校验有效性）、mark_used/mark_verified（状态管理） |
| `app/services/class_service.py` | **班级服务**。创建班级（生成8位随机码）、加入班级（校验班级码→防重复→添加成员）、查看已创建/已加入的班级列表（含学生数统计） |
| `app/services/homework_service.py` | **作业服务**（含两个类）。`HomeworkService`：教师端的作业CRUD、云端题库、组卷、布置；`StudentHomeworkService`：学生端的最新/历史作业、错题集查询、提交作业、批改结果、作业报告 |
| `app/services/lesson_plan_service.py` | **教案服务**。管理教师自有教案和云端共享教案的列表查询（分页+排序） |
| `app/services/review_service.py` | **讲评服务**。处理错题本讲评和作业讲评的列表查询，支持 report/book/time/subject/class 多条件组合筛选和排序 |
| `app/services/book_service.py` | **习题集服务**。习题集列表分页查询、详情查询（含章节树），未找到时抛 NotFound |
| `app/services/member_service.py` | **会员服务**。个人资料的查询与更新（User表+Profile表联动）、密码修改（旧密码校验→新密码哈希）、订单分页列表（支持 status 筛选） |
| `app/services/message_service.py` | **消息服务**。消息分页列表查询、标记已读（归属校验）、删除（归属校验） |

---

## `app/repositories/` — 数据访问层

| 文件 | 用途 |
|------|------|
| `app/repositories/__init__.py` | Python 包标识文件 |
| `app/repositories/base.py` | **通用 CRUD 基类**。提供 `get_by_id`、`get_all`、`count`、`create`、`update`、`delete`、`delete_by_id` 七个通用方法，所有 Repository 继承此类 |
| `app/repositories/user_repo.py` | **用户数据访问**。继承基类，新增 `get_by_phone`（按手机号查用户）、`create_user`（创建用户并返回） |
| `app/repositories/sms_code_repo.py` | **验证码数据访问**。create_code（生成验证码记录）、get_valid_code（查询未使用且未过期的验证码）、mark_used（标记已用）、mark_verified（标记已验证）、get_recent_verified（查找10分钟内验证通过但未重置的记录） |
| `app/repositories/class_repo.py` | **班级数据访问**。get_by_code（按班级码查询）、get_with_teacher（联查教师信息）、get_created_by_teacher/get_joined_by_teacher（教师视角）、get_student_count（统计学生数）、get_students（联查学生信息）、create_class（生成随机8位班级码）、is_student_in_class（查重） |
| `app/repositories/homework_repo.py` | **作业数据访问**（含三个类）。`HomeworkRepository`：教师作业CRUD；`StudentHomeworkRepository`：学生作业历史/最新查询（JOIN homeworks 获取 name/source/subject，支持 name/book/time/sort 多条件筛选）；`ErrorItemRepository`：错题集查询（同样支持多条件筛选和排序） |
| `app/repositories/lesson_plan_repo.py` | **教案数据访问**。get_by_teacher（查询自有教案，分页+排序）、get_cloud（查询云端共享教案，分页+排序） |
| `app/repositories/review_repo.py` | **讲评数据访问**。get_reports（按 type 和 teacher_id 查询，支持 report/book/time/subject/class 多条件筛选，动态排序字段包括 seq/date/max/min/avg/median/mode） |
| `app/repositories/book_repo.py` | **习题集数据访问**。get_list（分页列表）、get_with_chapters（联查章节，使用 selectinload 优化 N+1 查询） |
| `app/repositories/order_repo.py` | **订单数据访问**。get_by_user（按用户+状态筛选分页查询） |
| `app/repositories/message_repo.py` | **消息数据访问**。get_by_user（分页列表）、mark_read（标记已读并校验归属） |

---

## `tests/` — 测试（待补充）

测试文件应使用 pytest + httpx 异步测试客户端，覆盖认证流程和核心业务逻辑。

---

## 架构分层调用链

```
客户端请求
  ↓
router/   (参数校验、提取当前用户、调用 service)
  ↓
service/  (业务逻辑、事务协调、异常抛出)
  ↓
repository/  (SQL 构建、数据库交互)
  ↓
models/   (ORM 映射 → 数据库表)
```

每一层职责单一：
- **Router** 只做参数提取和 HTTP 状态码处理
- **Service** 包含所有业务规则和流程编排
- **Repository** 只负责数据库查询，不包含业务逻辑
- **Model** 纯数据结构，不含行为
