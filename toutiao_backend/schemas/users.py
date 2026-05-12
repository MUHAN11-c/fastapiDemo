"""
=== 用户模块 - 数据模型（Pydantic Schema）===

定义了用户模块的所有请求/响应数据模型喵~

关键概念：
- 请求体模型（如 UserRequest）—— 定义前端 POST/PUT 时发送的数据格式喵~
- 响应体模型（如 UserInfoResponse）—— 定义后端返回给前端的数据格式喵~
- from_attributes=True —— 允许直接从 ORM 对象创建 Pydantic 模型喵~
- alias —— 字段别名，实现 Python 下划线命名 ↔ JSON 驼峰命名互转喵~
"""

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# === 注册/登录请求体 ===
# 用户注册和登录都用这个模型（只需要用户名和密码）喵~
class UserRequest(BaseModel):
    username: str
    password: str


# === 用户信息基础模型（可复用的字段）===
# 定义用户的可选信息字段，被下面的 Response 类继承喵~
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


# === 用户信息响应模型 ===
class UserInfoResponse(UserInfoBase):
    """返回给前端时，需要加上 id 和 username 喵~"""
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True  # 可以从 ORM User 对象直接转换喵~
    )


# === 认证响应模型（注册/登录成功后返回的数据）===
class UserAuthResponse(BaseModel):
    """注册或登录成功后，返回 Token 和用户信息喵~"""
    token: str                                                  # 用于后续请求的身份认证喵~
    user_info: UserInfoResponse = Field(..., alias="userInfo")  # alias → JSON中为 userInfo 喵~

    model_config = ConfigDict(
        populate_by_name=True,  # 兼容两种命名方式喵~
        from_attributes=True
    )


# === 更新用户信息请求体 ===
class UserUpdateRequest(BaseModel):
    """所有字段都是可选的 —— 只传需要修改的字段即可喵~"""
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


# === 修改密码请求体 ===
class UserChangePasswordRequest(BaseModel):
    """修改密码需要提供旧密码（验证身份）和新密码喵~"""
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")
