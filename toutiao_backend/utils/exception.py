"""
=== 异常处理器模块 ===

这个模块定义了各种异常的处理逻辑喵~

为什么需要全局异常处理？
- 避免后台报错直接 500 返回给前端（不友好）喵~
- 统一异常响应的格式喵~
- 开发模式下返回详细错误信息（方便调试）喵~
- 生产模式下返回简化信息（不暴露代码细节）喵~

异常处理器之间的"优先级"：
FastAPI 会按照注册顺序匹配异常类，找到第一个匹配的处理器喵~
所以：具体异常在前，通用异常在后喵~
- HTTPException → 业务逻辑主动抛出的异常喵~
- IntegrityError → 数据库约束冲突（如重复插入）喵~
- SQLAlchemyError → 数据库操作错误喵~
- Exception → 兜底（捕获所有未处理的异常）喵~
"""

import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# === 调试模式开关 ===
# True = 开发模式：返回详细错误信息（traceback、错误路径）喵~
# False = 生产模式：只返回简短描述喵~
DEBUG_MODE = True  # 教学项目保持开启喵~


# === 1. 处理 HTTPException（业务异常）===
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTPException 通常是路由中主动抛出的喵~
    比如：用户不存在 → raise HTTPException(404, "查无此人") 喵~
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )


# === 2. 处理数据库完整性约束错误 ===
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    IntegrityError 是数据库约束冲突时抛出的喵~
    常见场景：
    - 用户名重复（违反了 unique 约束）喵~
    - 外键关联的数据不存在（违反了 foreign key 约束）喵~
    """
    error_msg = str(exc.orig)  # exc.orig 是数据库原始错误信息喵~

    # 根据错误信息判断具体是什么约束冲突喵~
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    # 开发模式下返回详细信息帮助调试喵~
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )


# === 3. 处理 SQLAlchemy 数据库错误 ===
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    处理数据库操作中的其他错误喵~
    比如：数据库连接失败、SQL 语法错误等喵~
    """
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),  # 完整的调用栈信息喵~
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后重试",
            "data": error_data
        }
    )


# === 4. 兜底异常处理器 ===
async def general_exception_handler(request: Request, exc: Exception):
    """
    捕获所有上面没处理的异常（最后的"安全网"）喵~
    如果走到了这里，说明发生了意料之外的错误喵~
    """
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data
        }
    )
