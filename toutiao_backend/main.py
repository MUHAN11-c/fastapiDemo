"""
=== AI掘金头条 - 应用入口 ===

这是整个 FastAPI 项目的"入口文件"喵~
所有子模块（新闻、用户、收藏、浏览历史）都在这里"组装"起来喵~

项目架构：
- config/  —— 配置模块（数据库连接、Redis 缓存）喵~
- models/  —— 数据库表模型的 ORM 定义喵~
- schemas/ —— Pydantic 数据校验模型（请求体/响应体格式）喵~
- crud/    —— 数据库增删改查的具体实现喵~
- routers/ —— API 路由（接收 HTTP 请求，调用 crud 处理）喵~
- cache/   —— Redis 缓存相关方法喵~
- utils/   —— 工具模块（加密、认证、异常处理、通用响应）喵~
"""

from fastapi import FastAPI
# 1. 导入各个子模块的路由（每个子模块都是独立的 APIRouter）喵~
from routers import news, users, favorite, history
# 2. 导入 CORS 中间件 —— 解决前端跨域请求问题喵~
from fastapi.middleware.cors import CORSMiddleware

# 3. 导入异常处理器注册函数喵~
from utils.exception_handlers import register_exception_handlers

# === 创建 FastAPI 应用实例 —— 一切从这里开始喵~ ===
app = FastAPI()

# === 注册全局异常处理器 ===
# 统一处理各种异常（HTTP异常、数据库约束异常、未知异常等）喵~
# 这样就不用在每个路由里写 try/except 了喵~
register_exception_handlers(app)


# === 配置 CORS（跨域资源共享）中间件 ===
# 前后端分离开发时，前端（例如 localhost:3000）请求后端（localhost:8000）会触发跨域限制喵~
# CORS 中间件告诉浏览器："允许跨域请求，放心访问" 喵~
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许的源：* 表示允许所有来源（生产环境应指定具体域名）喵~
    allow_credentials=True,  # 允许携带 Cookie 喵~
    allow_methods=["*"],     # 允许的 HTTP 方法：* 表示允许 GET/POST/PUT/DELETE 等所有方法喵~
    allow_headers=["*"],     # 允许的请求头：* 表示允许所有请求头喵~
)


# === 根路径 ===
@app.get("/")
async def root():
    return {"message": "Hello World"}


# === 注册（挂载）各模块的路由 ===
# app.include_router() 把子模块的 APIRouter 挂载到主应用上喵~
# 这样就把 /api/news/* /api/user/* /api/favorite/* /api/history/* 都注册好了喵~
# 这就是"模块化路由"的核心：每个模块独立管理自己的路由，在 main.py 统一注册喵~
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)


# === 启动方式 ===
# 在 toutiao_backend 目录下执行：
#   uvicorn main:app --reload --port 8000
# 然后访问 http://localhost:8000/docs 查看自动生成的 API 文档喵~
