"""
=== 异常处理器注册模块 ===

这个模块负责把所有异常处理器"注册"到 FastAPI 应用上喵~

注册顺序很重要！
FastAPI 会按顺序匹配异常类，所以：
- 子类在前面（如 IntegrityError 是 SQLAlchemyError 的子类）喵~
- 具体异常在前面，抽象异常在最后喵~
- Exception 永远在最后（作为"兜底"的万能处理器）喵~

如果顺序反过来，子类异常永远不会被匹配到！喵~
"""

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import (
    http_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
    general_exception_handler
)


def register_exception_handlers(app):
    """
    注册全局异常处理器到 FastAPI 应用喵~

    异常处理的"链"：
    HTTPException → IntegrityError → SQLAlchemyError → Exception 喵~
    当前面的处理器能处理时，后面的就不会被调用喵~
    """
    app.add_exception_handler(HTTPException, http_exception_handler)     # 1. 业务异常（优先）喵~
    app.add_exception_handler(IntegrityError, integrity_error_handler)    # 2. 数据完整性冲突喵~
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # 3. 数据库错误喵~
    app.add_exception_handler(Exception, general_exception_handler)       # 4. 兜底（最后）喵~
