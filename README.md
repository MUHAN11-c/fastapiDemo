# FastAPI 从入门到实战 —— 学习项目

## 项目简介

本项目是基于《Python Web 开发：FastAPI 从入门到实战》课程整理的学习项目喵~ 所有代码都添加了详细的中文注释，适合零基础学习者从零开始学习 FastAPI 喵~

## 项目结构

```
fastapi_demo/
├── examples/                    # 零基础学习示例（按顺序学习）
│   ├── 01_路由.py               # 路由：把 URL 绑定到函数
│   ├── 02_路径参数.py           # 路径参数：/book/{id}
│   ├── 03_查询参数.py           # 查询参数：?skip=0&limit=10
│   ├── 04_请求体参数.py         # POST 请求体 + Pydantic 模型
│   ├── 05_响应类型_HTML格式.py   # 返回 HTML 页面
│   ├── 06_响应类型_文件格式.py   # 返回文件（图片等）
│   ├── 07_自定义响应数据格式.py  # response_model 过滤字段
│   ├── 08_中间件.py             # 中间件（请求拦截器）
│   ├── 09_依赖注入.py           # 依赖注入（代码复用）
│   ├── 10_ORM_建表.py           # ORM 建表 + 引擎 + 会话
│   ├── 11_ORM_路由中使用ORM.py   # 在路由中使用数据库
│   ├── 12_ORM_查询数据.py       # 查询：all/first/get
│   ├── 13_ORM_查询条件.py       # where 条件查询
│   ├── 14_ORM_模糊查询.py       # like/&/|/in_ 查询
│   ├── 15_ORM_聚合查询.py       # count/max/avg 统计
│   ├── 16_ORM_分页查询.py       # offset/limit 分页
│   ├── 17_ORM_新增数据.py       # add + commit 新增
│   ├── 18_ORM_更新数据.py       # 查询 → 修改 → 提交
│   ├── 19_ORM_删除数据.py       # delete + commit 删除
│   └── files/                   # 静态资源
│
└── toutiao_backend/             # 实战项目：AI掘金头条
    ├── main.py                   # 应用入口，组装所有模块
    ├── requirements.txt          # Python 依赖列表
    ├── config/                   # 配置模块
    │   ├── db_conf.py            # 数据库配置（MySQL + SQLAlchemy）
    │   └── cache_conf.py         # 缓存配置（Redis）
    ├── models/                   # 数据库 ORM 模型
    │   ├── news.py               # 新闻表 + 分类表
    │   ├── users.py              # 用户表 + Token 表
    │   ├── favorite.py           # 收藏表
    │   └── history.py            # 浏览历史表
    ├── schemas/                  # Pydantic 数据校验模型
    │   ├── base.py               # 基础模型（可复用）
    │   ├── news.py               # 新闻请求/响应模型
    │   ├── users.py              # 用户请求/响应模型
    │   ├── favorite.py           # 收藏请求/响应模型
    │   └── history.py            # 历史请求/响应模型
    ├── crud/                     # 数据库操作层
    │   ├── news_cache.py         # 新闻 CRUD（缓存版）
    │   ├── news.py               # 新闻 CRUD（基础版）
    │   ├── users.py              # 用户 CRUD
    │   ├── favorite.py           # 收藏 CRUD
    │   └── history.py            # 历史 CRUD
    ├── routers/                  # API 路由层
    │   ├── news.py               # /api/news/*
    │   ├── users.py              # /api/user/*
    │   ├── favorite.py           # /api/favorite/*
    │   └── history.py            # /api/history/*
    ├── cache/                    # 缓存模块
    │   └── news_cache.py         # 新闻缓存管理
    └── utils/                    # 工具模块
        ├── security.py           # 密码加密（bcrypt）
        ├── auth.py               # 认证依赖项（Token 校验）
        ├── response.py           # 通用响应格式
        ├── exception.py          # 异常处理器
        └── exception_handlers.py # 异常处理器注册
```

## 学习路线

按编号顺序学习 `examples/` 目录下的文件喵~

### 第一部分：FastAPI 基础（01~07）

1. `01_路由.py` —— 理解什么是路由，如何创建 API 接口喵~
2. `02_路径参数.py` —— 学习如何从 URL 路径中提取参数喵~
3. `03_查询参数.py` —— 学习如何从 URL 查询字符串获取参数喵~
4. `04_请求体参数.py` —— 学习如何接收 POST 请求的 JSON 数据喵~
5. `05~07` —— 学习不同的响应格式（HTML、文件、自定义）喵~

### 第二部分：FastAPI 进阶（08~19）

1. `08_中间件.py` —— 理解请求拦截机制喵~
2. `09_依赖注入.py` —— 学会代码复用喵~
3. `10~19` —— 掌握 SQLAlchemy ORM 的完整 CRUD 操作喵~

### 第三部分：实战项目（toutiao_backend/）

研究 `toutiao_backend/` 目录，理解一个完整的 FastAPI 项目是如何组织的：
- models → schemas → crud → routers → main.py 的分层架构
- 异步数据库操作
- Token 认证机制
- Redis 缓存策略
- 全局异常处理

## 环境准备

### 1. 安装 Python 3.10+

### 2. 安装 MySQL 并创建数据库

```sql
CREATE DATABASE news_app CHARACTER SET utf8mb4;
```

### 3. 安装 Redis（用于缓存）

### 4. 安装依赖

```bash
cd toutiao_backend
pip install -r requirements.txt
```

### 5. 启动服务

```bash
cd toutiao_backend
uvicorn main:app --reload --port 8000
```

### 6. 访问 API 文档

打开浏览器访问 http://localhost:8000/docs 查看自动生成的 Swagger API 文档喵~

## 技术栈

- **Web 框架**：FastAPI 0.125
- **ORM**：SQLAlchemy 2.0（异步）
- **数据库**：MySQL + aiomysql
- **缓存**：Redis
- **密码加密**：bcrypt + passlib
- **数据校验**：Pydantic v2
- **服务器**：Uvicorn

## 项目架构说明

项目采用**分层架构**，从上到下依次是：

```
routers/  (路由层 - 接收 HTTP 请求)
    ↓
schemas/  (数据校验层 - Pydantic 模型)
    ↓
crud/     (业务逻辑层 - 数据库操作)
    ↓
models/   (数据模型层 - ORM 表映射)
    ↓
config/   (配置层 - 数据库/缓存配置)
```

核心设计原则：
- **分层解耦**：每层只做自己的事情，不越界
- **依赖注入**：通过 FastAPI 的 Depends 管理数据库会话和认证
- **缓存优先**：先查 Redis，没有再查 MySQL，减少数据库压力
- **统一响应**：所有成功响应使用统一的 JSON 格式 {code, message, data}
- **全局异常处理**：一处注册，全局生效，不用每个路由写 try/except
