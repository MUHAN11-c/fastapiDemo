# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI 从入门到实战学习项目喵~ 包含零基础学习示例和一个完整的"AI掘金头条"新闻应用后端喵~

项目分为三个部分：
- `examples/` —— 零基础学习示例（19个文件，按编号顺序学习）喵~
- `toutiao_backend/` —— 实战项目，完整的分层架构 FastAPI 应用喵~
- `docs/` —— 学习文档（Git 零基础指南等）喵~

## Development Commands

```bash
# 运行实战项目
cd toutiao_backend && uvicorn main:app --reload --port 8000

# 运行学习示例
cd examples && uvicorn 01_路由:app --reload

# 安装依赖
cd toutiao_backend && pip install -r requirements.txt
```

## Architecture

### 分层架构（toutiao_backend）

```
routers/   → 路由层，接收 HTTP 请求，调用 crud 喵~
schemas/   → Pydantic 数据校验模型（请求体/响应体格式定义）喵~
crud/      → 业务逻辑层，封装数据库操作喵~
models/    → SQLAlchemy ORM 模型，映射数据库表喵~
config/    → 配置层（MySQL 数据库连接、Redis 缓存）喵~
cache/     → Redis 缓存管理喵~
utils/     → 工具层（密码加密 bcrypt、Token 认证、异常处理、通用响应）喵~
```

### 数据流

HTTP 请求 → routers → schemas（校验）→ crud（查缓存/查数据库）→ models（ORM）→ 数据库 → 响应喵~

### 关键设计模式

- 依赖注入（Depends）管理数据库会话 get_db 和认证 get_current_user 喵~
- 缓存优先策略：先查 Redis，没有再查 MySQL，查询结果写入 Redis 喵~
- 统一响应格式：`{code, message, data}`，通过 utils/response.py 的 success_response 封装喵~
- 全局异常处理：HTTPException → IntegrityError → SQLAlchemyError → Exception 逐一捕获喵~
- Token 认证：UUID Token 存 user_token 表，7 天过期喵~

## Database

- MySQL + aiomysql 异步驱动喵~
- 表：news_category、news、user、user_token、favorite、history 喵~
- 数据库名：news_app，charset=utf8mb4 喵~

## 重要注意事项

1. **所有回复必须使用中文，且每句末尾都要加上"喵~"**，无论回答、解释还是留给用户的任何文字输出，一律遵守此规则喵~
2. 代码注释使用中文喵~
