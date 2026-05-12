"""
=== 认证工具模块 —— 获取当前登录用户 ===

这个模块提供了一个 FastAPI 依赖项：get_current_user 喵~

工作流程：
1. 从请求头（Header）中获取 Authorization 字段的值喵~
2. 提取 Token 值（去掉 "Bearer " 前缀）喵~
3. 用 Token 在 user_token 表中查找对应的用户喵~
4. 检查 Token 是否过期喵~
5. 返回用户对象（如果无效则抛出 401 错误）喵~

使用方式：
  @router.get("/info")
  async def get_user_info(user: User = Depends(get_current_user)):
      # user 就是当前登录的用户对象喵~
      return success_response(data=user)
"""

from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users


# === 获取当前登录用户的依赖项 ===
async def get_current_user(
    # Header(..., alias="Authorization") —— 从 HTTP 请求头获取 Authorization 字段喵~
    # ... 表示这个请求头是"必填"的，没有则 FastAPI 自动返回 422 错误喵~
    authorization: str = Header(..., alias="Authorization"),
    # 同时还需要数据库会话（Depends 自动注入）喵~
    db: AsyncSession = Depends(get_db)
):
    # === 提取 Token 值 ===
    # 请求头的格式：Authorization: Bearer xxxxx-xxxx-xxxx
    # "Bearer " 后面才是真正的 Token 值喵~
    # 方法1：用 split 分割
    # token = authorization.split(" ")[1]  # 按空格分割，取第二部分喵~
    # 方法2：直接替换掉前缀（更健壮，即使前缀大小写不一致也没关系）喵~
    token = authorization.replace("Bearer ", "")

    # === 根据 Token 查找用户 ===
    # 调用 crud/users.py 中的 get_user_by_token 方法喵~
    user = await users.get_user_by_token(db, token)

    # === 检查 Token 是否有效 ===
    # 如果 Token 不存在 或 已经过期，返回 401 未授权错误喵~
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # 401 = 未授权喵~
            detail="无效的令牌或已经过期的令牌"
        )

    # Token 有效，返回用户对象给路由函数使用喵~
    return user
