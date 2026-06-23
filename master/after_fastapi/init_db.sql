-- ============================================================
-- MistakesMaster (错题通) 数据库初始化脚本
-- 目标: MySQL 8.0+
-- 编码: utf8mb4
-- 执行方式: mysql -h localhost -P 3306 -u root -p115900 mistakes < init_db.sql
-- 注意: UUID 主键由应用层 (Python uuid4) 生成, 不在数据库层自动生成
-- ============================================================

CREATE DATABASE IF NOT EXISTS `mistakes`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `mistakes`;

-- -----------------------------------------------------------
-- 1. users — 用户表
-- -----------------------------------------------------------
CREATE TABLE `users` (
  `id`            CHAR(32)     NOT NULL COMMENT '主键, UUID v4 (应用层生成)',
  `phone`         VARCHAR(11)  NOT NULL COMMENT '手机号 (11位)',
  `password_hash` VARCHAR(128) NOT NULL COMMENT '密码哈希 (bcrypt)',
  `real_name`     VARCHAR(64)  NOT NULL COMMENT '真实姓名',
  `role`          VARCHAR(16)  NOT NULL COMMENT '角色: teacher | student',
  `job`           VARCHAR(32)  DEFAULT NULL COMMENT '职务 (仅教师)',
  `subject`       VARCHAR(32)  DEFAULT NULL COMMENT '学科 (仅教师)',
  `is_active`     TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '是否启用: 1-启用 0-禁用',
  `created_at`    DATETIME     NOT NULL COMMENT '创建时间 (UTC+8)',
  `updated_at`    DATETIME     DEFAULT NULL COMMENT '更新时间 (UTC+8)',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ix_users_phone` (`phone`),
  INDEX `ix_users_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- -----------------------------------------------------------
-- 2. profiles — 用户个人资料表 (1:1 扩展)
-- -----------------------------------------------------------
CREATE TABLE `profiles` (
  `user_id`   CHAR(32)     NOT NULL COMMENT '主键 & 外键 → users.id',
  `birthday`  DATE         DEFAULT NULL COMMENT '生日',
  `gender`    VARCHAR(4)   NOT NULL DEFAULT '男' COMMENT '性别: 男 | 女',
  `email`     VARCHAR(128) DEFAULT NULL COMMENT '邮箱',
  `province`  VARCHAR(32)  DEFAULT NULL COMMENT '省',
  `city`      VARCHAR(32)  DEFAULT NULL COMMENT '市',
  `district`  VARCHAR(32)  DEFAULT NULL COMMENT '区/县',
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_profiles_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户个人资料表';

-- -----------------------------------------------------------
-- 3. classes — 班级表
-- -----------------------------------------------------------
CREATE TABLE `classes` (
  `id`          CHAR(32)     NOT NULL COMMENT '主键, UUID v4',
  `name`        VARCHAR(128) NOT NULL COMMENT '班级名称',
  `description` TEXT         DEFAULT NULL COMMENT '班级描述',
  `code`        VARCHAR(12)  NOT NULL COMMENT '班级码 (学生凭此加入)',
  `teacher_id`  CHAR(32)     NOT NULL COMMENT '教师 ID → users.id',
  `created_at`  DATETIME     NOT NULL COMMENT '创建时间 (UTC+8)',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ix_classes_code` (`code`),
  INDEX `ix_classes_teacher_id` (`teacher_id`),
  CONSTRAINT `fk_classes_teacher` FOREIGN KEY (`teacher_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级表';

-- -----------------------------------------------------------
-- 4. class_students — 班级-学生关联表
-- -----------------------------------------------------------
CREATE TABLE `class_students` (
  `id`         CHAR(32) NOT NULL COMMENT '主键, UUID v4',
  `class_id`   CHAR(32) NOT NULL COMMENT '班级 ID → classes.id',
  `student_id` CHAR(32) NOT NULL COMMENT '学生 ID → users.id',
  `joined_at`  DATETIME NOT NULL COMMENT '加入时间 (UTC+8)',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_class_student` (`class_id`, `student_id`),
  INDEX `ix_class_students_student_id` (`student_id`),
  CONSTRAINT `fk_class_students_class` FOREIGN KEY (`class_id`)
    REFERENCES `classes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_class_students_student` FOREIGN KEY (`student_id`)
    REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级-学生关联表';

-- -----------------------------------------------------------
-- 5. books — 习题集表 (必须在 homeworks 之前)
-- -----------------------------------------------------------
CREATE TABLE `books` (
  `id`          CHAR(32)      NOT NULL COMMENT '主键, UUID v4',
  `name`        VARCHAR(256)  NOT NULL COMMENT '习题集名称',
  `cover`       VARCHAR(512)  DEFAULT NULL COMMENT '封面图片 URL',
  `price`       DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '价格',
  `subject`     VARCHAR(32)   DEFAULT NULL COMMENT '学科',
  `publisher`   VARCHAR(64)   DEFAULT NULL COMMENT '出版社',
  `version`     VARCHAR(64)   DEFAULT NULL COMMENT '版本',
  `grade_term`  VARCHAR(64)   DEFAULT NULL COMMENT '年级学期',
  `description` TEXT          DEFAULT NULL COMMENT '描述',
  `updated_at`  DATETIME      NOT NULL COMMENT '更新时间 (UTC+8)',
  PRIMARY KEY (`id`),
  INDEX `ix_books_subject` (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='习题集表';

-- -----------------------------------------------------------
-- 6. homeworks — 作业表
-- -----------------------------------------------------------
CREATE TABLE `homeworks` (
  `id`          CHAR(32)     NOT NULL COMMENT '主键, UUID v4',
  `name`        VARCHAR(256) NOT NULL COMMENT '作业名称',
  `source`      VARCHAR(128) DEFAULT NULL COMMENT '来源 (教材/习题集等)',
  `subject`     VARCHAR(32)  DEFAULT NULL COMMENT '学科',
  `class_id`    CHAR(32)     NOT NULL COMMENT '班级 ID → classes.id',
  `book_id`     CHAR(32)     DEFAULT NULL COMMENT '关联习题集 ID → books.id',
  `teacher_id`  CHAR(32)     NOT NULL COMMENT '布置教师 ID → users.id',
  `deadline`    DATETIME     DEFAULT NULL COMMENT '截止时间 (UTC+8)',
  `total_score` INT          NOT NULL DEFAULT 100 COMMENT '满分',
  `created_at`  DATETIME     NOT NULL COMMENT '创建时间 (UTC+8)',
  PRIMARY KEY (`id`),
  INDEX `ix_homeworks_class_id` (`class_id`),
  INDEX `ix_homeworks_book_id` (`book_id`),
  INDEX `ix_homeworks_teacher_id` (`teacher_id`),
  CONSTRAINT `fk_homeworks_class` FOREIGN KEY (`class_id`)
    REFERENCES `classes` (`id`),
  CONSTRAINT `fk_homeworks_book` FOREIGN KEY (`book_id`)
    REFERENCES `books` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_homeworks_teacher` FOREIGN KEY (`teacher_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='作业表';

-- -----------------------------------------------------------
-- 7. student_homeworks — 学生作业作答记录
-- -----------------------------------------------------------
CREATE TABLE `student_homeworks` (
  `id`             CHAR(32) NOT NULL COMMENT '主键, UUID v4',
  `homework_id`    CHAR(32) NOT NULL COMMENT '作业 ID → homeworks.id',
  `student_id`     CHAR(32) NOT NULL COMMENT '学生 ID → users.id',
  `submit_time`    DATETIME DEFAULT NULL COMMENT '提交时间 (UTC+8)',
  `total_score`    INT      NOT NULL DEFAULT 0 COMMENT '满分',
  `my_score`       INT      NOT NULL DEFAULT 0 COMMENT '学生得分',
  `submit_content` JSON     DEFAULT NULL COMMENT '作答内容 (JSON)',
  `rank`           INT      DEFAULT NULL COMMENT '排名',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_student_homework` (`homework_id`, `student_id`),
  INDEX `ix_student_homeworks_student_id` (`student_id`),
  CONSTRAINT `fk_student_homeworks_homework` FOREIGN KEY (`homework_id`)
    REFERENCES `homeworks` (`id`),
  CONSTRAINT `fk_student_homeworks_student` FOREIGN KEY (`student_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生作业作答记录';

-- -----------------------------------------------------------
-- 8. error_items — 错题表
-- -----------------------------------------------------------
CREATE TABLE `error_items` (
  `id`          CHAR(32)     NOT NULL COMMENT '主键, UUID v4',
  `student_id`  CHAR(32)     NOT NULL COMMENT '学生 ID → users.id',
  `homework_id` CHAR(32)     NOT NULL COMMENT '作业 ID → homeworks.id',
  `name`        VARCHAR(256) NOT NULL COMMENT '题目名称',
  `source`      VARCHAR(128) DEFAULT NULL COMMENT '来源',
  `subject`     VARCHAR(32)  DEFAULT NULL COMMENT '学科',
  `error_seq`   INT          DEFAULT NULL COMMENT '错题序号',
  `submit_time` DATETIME     DEFAULT NULL COMMENT '提交时间 (UTC+8)',
  PRIMARY KEY (`id`),
  INDEX `ix_error_items_student_id` (`student_id`),
  INDEX `ix_error_items_homework_id` (`homework_id`),
  CONSTRAINT `fk_error_items_student` FOREIGN KEY (`student_id`)
    REFERENCES `users` (`id`),
  CONSTRAINT `fk_error_items_homework` FOREIGN KEY (`homework_id`)
    REFERENCES `homeworks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='错题表';

-- -----------------------------------------------------------
-- 9. book_chapters — 习题集章节表 (树形结构)
-- -----------------------------------------------------------
CREATE TABLE `book_chapters` (
  `id`         CHAR(32)     NOT NULL COMMENT '主键, UUID v4',
  `book_id`    CHAR(32)     NOT NULL COMMENT '习题集 ID → books.id',
  `name`       VARCHAR(256) NOT NULL COMMENT '章节名称',
  `parent_id`  CHAR(32)     DEFAULT NULL COMMENT '父章节 ID → book_chapters.id (自引用)',
  `sort_order` INT          NOT NULL DEFAULT 0 COMMENT '排序序号',
  PRIMARY KEY (`id`),
  INDEX `ix_book_chapters_book_id` (`book_id`),
  INDEX `ix_book_chapters_parent_id` (`parent_id`),
  CONSTRAINT `fk_book_chapters_book` FOREIGN KEY (`book_id`)
    REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_book_chapters_parent` FOREIGN KEY (`parent_id`)
    REFERENCES `book_chapters` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='习题集章节表';

-- -----------------------------------------------------------
-- 10. lesson_plans — 教案表
-- -----------------------------------------------------------
CREATE TABLE `lesson_plans` (
  `id`         CHAR(32)     NOT NULL COMMENT '主键, UUID v4',
  `name`       VARCHAR(256) NOT NULL COMMENT '教案名称',
  `size`       BIGINT       NOT NULL DEFAULT 0 COMMENT '文件大小 (字节)',
  `file_url`   VARCHAR(512) DEFAULT NULL COMMENT '文件 URL',
  `teacher_id` CHAR(32)     NOT NULL COMMENT '教师 ID → users.id',
  `is_cloud`   TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '是否云存储: 1-是 0-否',
  `created_at` DATETIME     NOT NULL COMMENT '创建时间 (UTC+8)',
  PRIMARY KEY (`id`),
  INDEX `ix_lesson_plans_teacher_id` (`teacher_id`),
  CONSTRAINT `fk_lesson_plans_teacher` FOREIGN KEY (`teacher_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教案表';

-- -----------------------------------------------------------
-- 11. review_reports — 讲评报告表
-- -----------------------------------------------------------
CREATE TABLE `review_reports` (
  `id`         CHAR(32)      NOT NULL COMMENT '主键, UUID v4',
  `seq`        INT           DEFAULT NULL COMMENT '序号',
  `date`       DATE          DEFAULT NULL COMMENT '日期',
  `report`     VARCHAR(256)  DEFAULT NULL COMMENT '报告名称',
  `book`       VARCHAR(256)  DEFAULT NULL COMMENT '关联教材/习题集',
  `max`        INT           DEFAULT NULL COMMENT '最高分',
  `min`        INT           DEFAULT NULL COMMENT '最低分',
  `avg`        DECIMAL(5,2)  DEFAULT NULL COMMENT '平均分',
  `median`     INT           DEFAULT NULL COMMENT '中位数',
  `mode`       INT           DEFAULT NULL COMMENT '众数',
  `subject`    VARCHAR(32)   DEFAULT NULL COMMENT '学科',
  `class_name` VARCHAR(128)  DEFAULT NULL COMMENT '班级名称',
  `type`       VARCHAR(32)   NOT NULL COMMENT '类型: error_book | homework',
  `teacher_id` CHAR(32)      NOT NULL COMMENT '教师 ID → users.id',
  PRIMARY KEY (`id`),
  INDEX `ix_review_reports_teacher_id` (`teacher_id`),
  INDEX `ix_review_reports_type` (`type`),
  CONSTRAINT `fk_review_reports_teacher` FOREIGN KEY (`teacher_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='讲评报告表';

-- -----------------------------------------------------------
-- 12. messages — 消息表
-- -----------------------------------------------------------
CREATE TABLE `messages` (
  `id`         CHAR(32)    NOT NULL COMMENT '主键, UUID v4',
  `from_user`  VARCHAR(64) DEFAULT NULL COMMENT '发送者名称',
  `role`       VARCHAR(16) DEFAULT NULL COMMENT '发送者角色',
  `content`    TEXT        NOT NULL COMMENT '消息内容',
  `is_read`    TINYINT(1)  NOT NULL DEFAULT 0 COMMENT '是否已读: 1-已读 0-未读',
  `created_at` DATETIME    NOT NULL COMMENT '发送时间 (UTC+8)',
  `user_id`    CHAR(32)    NOT NULL COMMENT '接收用户 ID → users.id',
  PRIMARY KEY (`id`),
  INDEX `ix_messages_user_id` (`user_id`),
  INDEX `ix_messages_is_read` (`is_read`),
  CONSTRAINT `fk_messages_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- -----------------------------------------------------------
-- 13. orders — 订单表
-- -----------------------------------------------------------
CREATE TABLE `orders` (
  `id`            CHAR(32)      NOT NULL COMMENT '主键, UUID v4',
  `order_no`      VARCHAR(32)   NOT NULL COMMENT '订单号',
  `name`          VARCHAR(256)  NOT NULL COMMENT '商品名称',
  `resource_type` VARCHAR(64)   DEFAULT NULL COMMENT '资源类型',
  `price`         DECIMAL(10,2) NOT NULL COMMENT '金额',
  `trade_status`  VARCHAR(32)   NOT NULL COMMENT '状态: pending | paid | cancelled',
  `time`          DATETIME      NOT NULL COMMENT '交易时间 (UTC+8)',
  `user_id`       CHAR(32)      NOT NULL COMMENT '用户 ID → users.id',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ix_orders_order_no` (`order_no`),
  INDEX `ix_orders_user_id` (`user_id`),
  INDEX `ix_orders_trade_status` (`trade_status`),
  CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- -----------------------------------------------------------
-- 14. sms_codes — 短信验证码表
-- -----------------------------------------------------------
CREATE TABLE `sms_codes` (
  `id`         CHAR(32)    NOT NULL COMMENT '主键, UUID v4',
  `phone`      VARCHAR(11) NOT NULL COMMENT '手机号',
  `code`       VARCHAR(6)  NOT NULL COMMENT '验证码 (6位)',
  `type`       VARCHAR(16) NOT NULL COMMENT '类型: register | forgot',
  `used`       TINYINT(1)  NOT NULL DEFAULT 0 COMMENT '是否已使用: 1-已用 0-未用',
  `verified`   TINYINT(1)  NOT NULL DEFAULT 0 COMMENT '忘记密码中间态验证: 1-已验证 0-未验证',
  `expires_at` DATETIME    NOT NULL COMMENT '过期时间 (UTC+8)',
  `created_at` DATETIME    NOT NULL COMMENT '创建时间 (UTC+8)',
  PRIMARY KEY (`id`),
  INDEX `ix_sms_codes_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='短信验证码表';

-- ============================================================
-- 初始化完成
-- 共 14 张表, 表依赖顺序已处理 (先建被引用表, 后建引用表)
-- ============================================================
