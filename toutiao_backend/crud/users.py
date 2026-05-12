"""
=== 用户 CRUD ===

这个模块封装了所有用户相关的数据库操作喵~

核心功能：
- get_user_by_username() —— 根据用户名找用户（注册时检查重名、登录时查询）喵~
- create_user() —— 创建新用户（密码加密后存储）喵~
- create_token() —— 生成登录令牌（UUID Token）喵~
- authenticate_user() —— 验证用户名密码喵~
- get_user_by_token() —— 根据 Token 查找用户（认证用）喵~
- update_user() —— 更新用户信息喵~
- change_password() —— 修改密码喵~
"""

import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security


# === 根据用户名查询用户 ===
async def get_user_by_username(db: AsyncSession, username: str):
    """
    根据用户名查找用户喵~
    注册时用来检查"用户名是否已经被占用"喵~
    登录时用来找到对应的用户记录喵~
    """
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# === 创建用户（注册）===
async def create_user(db: AsyncSession, user_data: UserRequest):
    """
    创建新用户喵~
    第1步：把明文密码加密成 hash 值（绝对不能存明文！）喵~
    第2步：创建 User ORM 对象喵~
    第3步：add → commit → refresh（写库 + 回读最新数据）喵~
    """
    # 密码加密：用户输入的 "123456" → "$2b$12$..." 喵~
    hashed_password = security.get_hash_password(user_data.password)
    # 创建 User 对象（注意：密码存的是 hash 值，不是明文）喵~
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)         # 加入会话（标记为待保存）喵~
    await db.commit()    # 提交事务（真正写入数据库）喵~
    await db.refresh(user)  # 从数据库读回最新数据（包括自动生成的 id 等）喵~
    return user


# === 生成登录令牌（Token）===
async def create_token(db: AsyncSession, user_id: int):
    """
    为用户生成或更新 Token 喵~

    策略：每个用户只保留一个 Token 喵~
    - 如果用户已经有 Token → 更新 Token 值和过期时间喵~
    - 如果用户还没有 Token → 创建新的 Token 记录喵~

    uuid.uuid4() 生成一个全球唯一的随机字符串，比如：
    "a1b2c3d4-e5f6-7890-abcd-ef1234567890" 喵~
    """
    token = str(uuid.uuid4())  # 生成随机唯一 Token 喵~
    # Token 有效期：7天喵~
    expires_at = datetime.now() + timedelta(days=7)

    # 先查用户是否已有 Token 记录喵~
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 已有 Token → 更新喵~
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 没有 Token → 新建喵~
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token


# === 用户认证（登录验证）===
async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    验证用户名和密码是否正确喵~

    第1步：根据用户名查用户喵~
    第2步：用 bcrypt 验证明文密码和数据库中的 hash 是否匹配喵~
    返回：验证成功返回 User 对象，失败返回 None 喵~
    """
    user = await get_user_by_username(db, username)
    if not user:
        return None  # 用户名不存在喵~

    if not security.verify_password(password, user.password):
        return None  # 密码不正确喵~

    return user  # 认证成功！喵~


# === 根据 Token 查找用户 ===
async def get_user_by_token(db: AsyncSession, token: str):
    """
    根据 Token 值查找对应的用户喵~

    第1步：在 user_token 表中查找 Token 记录喵~
    第2步：检查 Token 是否过期喵~
    第3步：根据 user_id 查找用户信息喵~
    """
    # 查找 Token 记录喵~
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    # Token 不存在 或 已过期 → 返回 None 喵~
    if not db_token or db_token.expires_at < datetime.now():
        return None

    # Token 有效 → 查找对应的用户喵~
    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# === 更新用户信息 ===
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    """
    更新用户信息（昵称、头像、性别等）喵~

    关键技巧：
    - model_dump(exclude_unset=True) —— 只导出"用户明确设置了的"字段喵~
    - model_dump(exclude_none=True) —— 排除值为 None 的字段喵~
    这样就能实现"只更新用户传了的字段，没传的不动"喵~
    """
    # 构建 update 语句喵~
    # ** 解包运算符：把字典的键值对展开为关键字参数喵~
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,  # 排除"用户没有设置的"字段喵~
        exclude_none=True    # 排除"值为 None 的"字段喵~
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查是否真的更新了数据喵~
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 查询更新后的用户信息并返回喵~
    updated_user = await get_user_by_username(db, username)
    return updated_user


# === 修改密码 ===
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    """
    修改密码喵~

    第1步：验证旧密码是否正确（防止别人盗用）喵~
    第2步：加密新密码喵~
    第3步：更新密码保存到数据库喵~
    """
    # 验证旧密码喵~
    if not security.verify_password(old_password, user.password):
        return False

    # 加密新密码并更新喵~
    hashed_new_pwd = security.get_hash_password(new_password)
    user.password = hashed_new_pwd

    # db.add(user) 让 SQLAlchemy 重新"接管"这个对象喵~
    # 这是因为 user 可能来自不同的数据库会话，需要重新关联喵~
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
