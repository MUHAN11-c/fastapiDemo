"""
=== 用户模块 - API 路由 ===

所有用户相关的 API 接口喵~

API 接口：
- POST /api/user/register —— 注册喵~
- POST /api/user/login    —— 登录喵~
- GET  /api/user/info     —— 获取当前用户信息（需要登录）喵~
- PUT  /api/user/update   —— 修改用户信息（需要登录）喵~
- PUT  /api/user/password —— 修改密码（需要登录）喵~

需要登录的接口通过 Depends(get_current_user) 来校验 Token 喵~
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.users import User
from schemas.users import (
    UserRequest, UserAuthResponse, UserInfoResponse,
    UserUpdateRequest, UserChangePasswordRequest
)

from config.db_conf import get_db
from crud import users
from utils.response import success_response
from utils.auth import get_current_user  # Token 认证依赖项喵~

# === 创建路由实例 ===
# prefix="/api/user" —— 所有用户接口都在 /api/user/ 路径下喵~
router = APIRouter(prefix="/api/user", tags=["users"])


# === 用户注册 ===
@router.post("/register")
async def register(
    user_data: UserRequest,  # 请求体：用户名 + 密码喵~
    db: AsyncSession = Depends(get_db)
):
    """
    注册流程：
    1. 检查用户名是否已存在 → 存在则返回 400 错误喵~
    2. 创建用户（密码加密存储）喵~
    3. 生成登录 Token（注册即登录）喵~
    4. 返回 Token 和用户信息喵~
    """
    # 第1步：检查用户名是否已被占用喵~
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已存在"
        )
    # 第2步：创建用户喵~
    user = await users.create_user(db, user_data)
    # 第3步：生成 Token（注册成功后自动登录）喵~
    token = await users.create_token(db, user.id)
    # 第4步：构造响应数据喵~
    # model_validate() 把 ORM 对象转成 Pydantic 响应模型喵~
    response_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user)
    )
    return success_response(message="注册成功", data=response_data)


# === 用户登录 ===
@router.post("/login")
async def login(
    user_data: UserRequest,  # 请求体：用户名 + 密码喵~
    db: AsyncSession = Depends(get_db)
):
    """
    登录流程：
    1. 验证用户名和密码喵~
    2. 生成/更新 Token 喵~
    3. 返回 Token 和用户信息喵~
    """
    # 第1步：认证用户（内部会查用户 + 验证密码）喵~
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # 401 = 未授权喵~
            detail="用户名或密码错误"
        )
    # 第2步：生成 Token 喵~
    token = await users.create_token(db, user.id)
    # 第3步：构造响应数据喵~
    response_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user)
    )
    return success_response(message="登录成功啦", data=response_data)


# === 获取当前用户信息 ===
@router.get("/info")
async def get_user_info(
    # Depends(get_current_user) 自动从请求头提取 Token，验证并返回用户对象喵~
    # 如果没有 Token 或 Token 无效/过期，自动返回 401 错误喵~
    user: User = Depends(get_current_user)
):
    """获取当前登录用户的信息（需要登录）喵~"""
    return success_response(
        message="获取用户信息成功",
        data=UserInfoResponse.model_validate(user)
    )


# === 修改用户信息 ===
@router.put("/update")
async def update_user_info(
    user_data: UserUpdateRequest,  # 请求体：要修改的字段喵~
    user: User = Depends(get_current_user),  # 验证 Token 喵~
    db: AsyncSession = Depends(get_db)
):
    """
    修改当前用户的信息（昵称、头像、性别等）喵~
    只更新用户明确传了的字段，没传的保持不变喵~
    """
    # 调用 update_user，只更新用户传了的字段喵~
    user = await users.update_user(db, user.username, user_data)
    return success_response(
        message="更新用户信息成功",
        data=UserInfoResponse.model_validate(user)
    )


# === 修改密码 ===
@router.put("/password")
async def update_password(
    password_data: UserChangePasswordRequest,  # 请求体：旧密码 + 新密码喵~
    user: User = Depends(get_current_user),     # 验证 Token 喵~
    db: AsyncSession = Depends(get_db)
):
    """修改密码：需要提供旧密码验证身份喵~"""
    res_change_pwd = await users.change_password(
        db, user,
        password_data.old_password,  # Pydantic 会自动按 alias 转换喵~
        password_data.new_password
    )
    if not res_change_pwd:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="修改密码失败，请稍后再试"
        )
    return success_response(message="修改密码成功")
