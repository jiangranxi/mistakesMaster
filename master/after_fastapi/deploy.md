# 生产环境部署文档

## 环境信息

| 项目 | 地址 |
|------|------|
| 后端 API | `http://47.93.4.44:8090` |
| 前端静态文件 | Nginx 站点目录（宝塔 `/www/wwwroot/xxx/`） |
| 宝塔面板 | `https://47.93.4.44:8888`（或其他端口） |

## Nginx 配置（宝塔面板操作）

宝塔 → 网站 → 对应站点 → 配置文件，添加以下内容：

### 1. API 代理

```
location /api/ {
    proxy_pass http://47.93.4.44:8090/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 2. 静态文件代理（图片等上传资源）

```
location /static/ {
    proxy_pass http://47.93.4.44:8090/static/;
    proxy_set_header Host $host;
}
```

### 3. SPA 路由回退（解决 404 问题）

```
location / {
    try_files $uri $uri/ /index.html;
}
```

> ⚠️ 已存在的 `location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$` 和 `location ~ .*\.(js|css)?$` 保持不变，不需要修改。

### 完整配置示例

```nginx
server {
    listen 80;
    server_name 47.93.4.44;
    root /www/wwwroot/你的站点目录;

    # API 代理到后端（注意 proxy_pass 末尾的 / 会去掉 /api 前缀）
    location /api/ {
        proxy_pass http://47.93.4.44:8090/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 图片等静态资源代理
    location /static/ {
        proxy_pass http://47.93.4.44:8090/static/;
        proxy_set_header Host $host;
    }

    # SPA 路由回退（放到最后，确保上面的规则优先匹配）
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 已有规则保持不变
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
        expires 30d;
        error_log /dev/null;
        access_log /dev/null;
    }

    location ~ .*\.(js|css)?$ {
        expires 12h;
        error_log /dev/null;
        access_log /dev/null;
    }
}
```

## 请求链路说明

```
浏览器                     Nginx                        FastAPI
  │                          │                            │
  ├─ GET /api/auth/login ──→ │                            │
  │                          ├─ proxy_pass /auth/login ──→ │
  │                          │                            ├─ 处理请求
  │                          │ ←─ 响应 ───────────────────┤
  │ ←─ 响应 ────────────────┤                            │
  │                          │                            │
  ├─ GET /static/covers/xxx.jpg                           │
  │                          ├─ proxy_pass ──────────────→ │
  │                          │ ←─ 返回图片 ───────────────┤
  │ ←─ 图片 ────────────────┤                            │
```

## 部署步骤

1. `npm run build`（在本地 front 目录执行）
2. 将 `dist/` 文件夹内容上传到宝塔网站根目录
3. 在宝塔 Nginx 配置中添加上述代理规则
4. 重载 Nginx：`nginx -s reload` 或在宝塔面板点击「重载配置」
5. 浏览器访问 `http://47.93.4.44` 测试

## 注意事项

- `proxy_pass` 末尾带 `/` 会自动去掉 `/api` 前缀（前端发 `/api/auth/login` → 后端收到 `/auth/login`）
- 后端已配置 `allow_origins=["*"]`，跨域不是问题
- 如果后端地址变更，只需修改 `proxy_pass` 中的 IP:端口，无需重新构建前端
