# MistakesMaster 数据库文档

## 概述

- **数据库引擎**: SQLite（开发环境），生产环境可切换 PostgreSQL
- **ORM 框架**: SQLAlchemy 2.0（异步）
- **主键策略**: 全部使用 UUID（uuid4）
- **时区**: UTC+8（东八区北京/上海时间）
- **迁移工具**: Alembic（未生成迁移版本，当前为 code-first 建表）

---

## 表结构

### 1. users — 用户表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `phone` | String(11) | NOT NULL, UNIQUE, INDEX | 手机号（11 位） |
| `password_hash` | String(128) | NOT NULL | 密码哈希 |
| `real_name` | String(64) | NOT NULL | 真实姓名 |
| `role` | String(16) | NOT NULL | 角色：`teacher` / `student` |
| `job` | String(32) | NULLABLE | 职务（仅教师） |
| `subject` | String(32) | NULLABLE | 学科（仅教师） |
| `is_active` | Boolean | NOT NULL, DEFAULT True | 是否启用 |
| `created_at` | DateTime(tz=True) | NOT NULL | 创建时间 |
| `updated_at` | DateTime(tz=True) | NULLABLE | 更新时间 |

**关联关系**:
- 一对一 → `profiles`
- 一对多 → `classes`（教师创建的班级）
- 一对多 → `orders`
- 一对多 → `messages`

---

### 2. profiles — 用户个人资料表（1:1 扩展）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `user_id` | UUID | PK, FK → users.id CASCADE | 主键 & 外键 |
| `birthday` | Date | NULLABLE | 生日 |
| `gender` | String(4) | NOT NULL, DEFAULT '男' | 性别 |
| `email` | String(128) | NULLABLE | 邮箱 |
| `province` | String(32) | NULLABLE | 省 |
| `city` | String(32) | NULLABLE | 市 |
| `district` | String(32) | NULLABLE | 区/县 |

**关联关系**:
- 一对一 → `users`（back_populates: user.profile）

---

### 3. classes — 班级表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `name` | String(128) | NOT NULL | 班级名称 |
| `description` | Text | NULLABLE | 班级描述 |
| `code` | String(12) | NOT NULL, UNIQUE | 班级码（用于学生加入） |
| `teacher_id` | UUID | NOT NULL, FK → users.id | 教师 ID |
| `created_at` | DateTime | NOT NULL | 创建时间 |

**关联关系**:
- 多对一 → `users`（教师）
- 一对多 → `class_students`

---

### 4. class_students — 班级-学生关联表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `class_id` | UUID | NOT NULL, FK → classes.id CASCADE | 班级 ID |
| `student_id` | UUID | NOT NULL, FK → users.id CASCADE | 学生 ID |
| `joined_at` | DateTime | NOT NULL | 加入时间 |

**唯一约束**: `(class_id, student_id)`

---

### 5. homeworks — 作业表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `name` | String(256) | NOT NULL | 作业名称 |
| `source` | String(128) | NULLABLE | 来源（教材/习题集等） |
| `subject` | String(32) | NULLABLE | 学科 |
| `class_id` | UUID | NOT NULL, FK → classes.id | 班级 ID |
| `book_id` | UUID | NULLABLE, FK → books.id | 关联习题集 ID |
| `teacher_id` | UUID | NOT NULL, FK → users.id | 布置教师 ID |
| `deadline` | DateTime | NULLABLE | 截止时间 |
| `total_score` | Integer | NOT NULL, DEFAULT 100 | 满分 |
| `created_at` | DateTime | NOT NULL | 创建时间 |

---

### 6. student_homeworks — 学生作业作答记录

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `homework_id` | UUID | NOT NULL, FK → homeworks.id | 作业 ID |
| `student_id` | UUID | NOT NULL, FK → users.id | 学生 ID |
| `submit_time` | DateTime | NULLABLE | 提交时间 |
| `total_score` | Integer | NOT NULL, DEFAULT 0 | 满分 |
| `my_score` | Integer | NOT NULL, DEFAULT 0 | 学生得分 |
| `submit_content` | JSON | NULLABLE | 作答内容（JSON） |
| `rank` | Integer | NULLABLE | 排名 |

**唯一约束**: `(homework_id, student_id)`

---

### 7. error_items — 错题表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `student_id` | UUID | NOT NULL, FK → users.id | 学生 ID |
| `homework_id` | UUID | NOT NULL, FK → homeworks.id | 作业 ID |
| `name` | String(256) | NOT NULL | 题目名称 |
| `source` | String(128) | NULLABLE | 来源 |
| `subject` | String(32) | NULLABLE | 学科 |
| `error_seq` | Integer | NULLABLE | 错题序号 |
| `submit_time` | DateTime | NULLABLE | 提交时间 |

---

### 8. books — 习题集表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `name` | String(256) | NOT NULL | 习题集名称 |
| `cover` | String(512) | NULLABLE | 封面图片 URL |
| `price` | Numeric(10,2) | NOT NULL, DEFAULT 0 | 价格 |
| `subject` | String(32) | NULLABLE | 学科 |
| `publisher` | String(64) | NULLABLE | 出版社 |
| `version` | String(64) | NULLABLE | 版本 |
| `grade_term` | String(64) | NULLABLE | 年级学期 |
| `description` | Text | NULLABLE | 描述 |
| `updated_at` | DateTime | NOT NULL | 更新时间 |

**关联关系**:
- 一对多 → `book_chapters`

---

### 9. book_chapters — 习题集章节表（树形结构）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `book_id` | UUID | NOT NULL, FK → books.id CASCADE | 习题集 ID |
| `name` | String(256) | NOT NULL | 章节名称 |
| `parent_id` | UUID | NULLABLE, FK → book_chapters.id | 父章节 ID（自引用） |
| `sort_order` | Integer | NOT NULL, DEFAULT 0 | 排序序号 |

---

### 10. lesson_plans — 教案表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `name` | String(256) | NOT NULL | 教案名称 |
| `size` | BigInteger | NOT NULL, DEFAULT 0 | 文件大小（字节） |
| `file_url` | String(512) | NULLABLE | 文件 URL |
| `teacher_id` | UUID | NOT NULL, FK → users.id | 教师 ID |
| `is_cloud` | Boolean | NOT NULL, DEFAULT False | 是否云存储 |
| `created_at` | DateTime | NOT NULL | 创建时间 |

---

### 11. review_reports — 讲评报告表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `seq` | Integer | NULLABLE | 序号 |
| `date` | Date | NULLABLE | 日期 |
| `report` | String(256) | NULLABLE | 报告名称 |
| `book` | String(256) | NULLABLE | 关联教材/习题集 |
| `max` | Integer | NULLABLE | 最高分 |
| `min` | Integer | NULLABLE | 最低分 |
| `avg` | Numeric(5,2) | NULLABLE | 平均分 |
| `median` | Integer | NULLABLE | 中位数 |
| `mode` | Integer | NULLABLE | 众数 |
| `subject` | String(32) | NULLABLE | 学科 |
| `class_name` | String(128) | NULLABLE | 班级名称 |
| `type` | String(32) | NOT NULL | 类型：`error_book` / `homework` |
| `teacher_id` | UUID | NOT NULL, FK → users.id | 教师 ID |

---

### 12. messages — 消息表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `from_user` | String(64) | NULLABLE | 发送者名称 |
| `role` | String(16) | NULLABLE | 发送者角色 |
| `content` | Text | NOT NULL | 消息内容 |
| `is_read` | Boolean | NOT NULL, DEFAULT False | 是否已读 |
| `created_at` | DateTime | NOT NULL | 发送时间 |
| `user_id` | UUID | NOT NULL, FK → users.id | 接收用户 ID |

**关联关系**:
- 多对一 → `users`

---

### 13. orders — 订单表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `order_no` | String(32) | NOT NULL, UNIQUE | 订单号 |
| `name` | String(256) | NOT NULL | 商品名称 |
| `resource_type` | String(64) | NULLABLE | 资源类型 |
| `price` | Numeric(10,2) | NOT NULL | 金额 |
| `trade_status` | String(32) | NOT NULL | 状态：`pending` / `paid` / `cancelled` |
| `time` | DateTime | NOT NULL | 交易时间 |
| `user_id` | UUID | NOT NULL, FK → users.id | 用户 ID |

**关联关系**:
- 多对一 → `users`

---

### 14. sms_codes — 短信验证码表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | UUID | PK, 默认 uuid4 | 主键 |
| `phone` | String(11) | NOT NULL, INDEX | 手机号 |
| `code` | String(6) | NOT NULL | 验证码 |
| `type` | String(16) | NOT NULL | 类型：`register` / `forgot` |
| `used` | Boolean | NOT NULL, DEFAULT False | 是否已使用 |
| `verified` | Boolean | NOT NULL, DEFAULT False | 忘记密码中间态验证 |
| `expires_at` | DateTime(tz=True) | NOT NULL | 过期时间 |
| `created_at` | DateTime | NOT NULL | 创建时间 |

---

## ER 关系图

```
users ──1:1── profiles
users ──1:N── classes (teacher_id)
users ──1:N── orders
users ──1:N── messages
users ──1:N── homeworks (teacher_id)

classes ──1:N── class_students ──N:1── users (student)
classes ──1:N── homeworks

homeworks ──1:N── student_homeworks ──N:1── users (student)
homeworks ──1:N── error_items ──N:1── users (student)
homeworks ──N:1── books

books ──1:N── book_chapters (自引用 parent_id)

users ──1:N── lesson_plans
users ──1:N── review_reports

sms_codes (独立，不关联外键)
```

## 索引

| 表 | 索引字段 | 说明 |
|----|----------|------|
| users | phone (UNIQUE) | 手机号唯一索引 |
| classes | code (UNIQUE) | 班级码唯一索引 |
| class_students | (class_id, student_id) (UNIQUE) | 防重复加入 |
| student_homeworks | (homework_id, student_id) (UNIQUE) | 一人一次提交 |
| orders | order_no (UNIQUE) | 订单号唯一 |
| sms_codes | phone (INDEX) | 按手机号查询验证码 |
