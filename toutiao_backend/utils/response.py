"""
=== 通用响应工具模块 ===

统一 API 的响应格式，所有成功响应都使用这个格式喵~

标准响应格式：
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}

为什么需要统一格式？
- 前端可以统一处理（判断 code 就知道成功还是失败）喵~
- 避免每个路由都手写相同的响应结构喵~
- jsonable_encoder 确保 ORM 对象、Pydantic 对象都能正确转成 JSON 喵~
"""

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success", data=None):
    """
    生成统一格式的成功响应喵~

    参数：
    - message: 提示信息（如 "登录成功"、"获取新闻列表成功"）喵~
    - data: 响应数据（可以是 ORM 对象、Pydantic 模型、字典、列表等）喵~

    jsonable_encoder 的作用：
    它能把 Python 对象（ORM、Pydantic、datetime 等）递归转换成 JSON 兼容的格式喵~
    比如 datetime 对象 → "2024-01-01T00:00:00" 字符串喵~
    """
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))
