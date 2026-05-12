"""
=== 用户模块 - 数据库模型（ORM）===

这里定义了两个用户相关的数据库表喵~

1. User（用户信息表）—— 用户名、密码（加密存储）、昵称、头像等喵~
2. UserToken（令牌表）—— 存储用户的登录令牌（Token），用于身份认证喵~

Token 认证流程：
1. 用户登录 → 服务端验证用户名密码 → 生成一个随机 Token（UUID）喵~
2. Token 存储到 user_token 表，同时返回给客户端喵~
3. 客户端后续请求在 Header 中带上 Authorization: Bearer <token> 喵~
4. 服务端根据 Token 查找用户，确认身份喵~
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Index, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """用户模块的基类（空基类，不含公共字段）喵~"""
    pass


# === 用户信息表（User）===
class User(Base):
    __tablename__ = 'user'

    # 创建索引：username 和 phone 经常用于查询，给它们建索引喵~
    __table_args__ = (
        Index('username_UNIQUE', 'username'),  # 用户名索引（登录时根据用户名查找）喵~
        Index('phone_UNIQUE', 'phone'),        # 手机号索引喵~
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    # unique=True —— 用户名必须唯一，两个用户不能重名喵~
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    # 密码存储的是 hash 值（bcrypt 加密后的结果），不是明文！所以长度设为 255 喵~
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（加密存储）")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment="昵称")
    # 头像有默认值：一个可爱的猫咪图片喵~
    avatar: Mapped[Optional[str]] = mapped_column(
        String(255), comment="头像URL",
        default='https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'
    )
    # Enum('male', 'female', 'unknown') —— 性别只能是这三个值之一喵~
    gender: Mapped[Optional[str]] = mapped_column(
        Enum('male', 'female', 'unknown'), comment="性别", default='unknown'
    )
    bio: Mapped[Optional[str]] = mapped_column(
        String(500), comment="个人简介", default='这个人很懒，什么都没留下'
    )
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment="手机号")
    # datetime.now() 带括号 —— 会在模块加载时求值一次喵~
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), comment="更新时间"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', nickname='{self.nickname}')>"


# === 用户令牌表（UserToken）===
class UserToken(Base):
    __tablename__ = 'user_token'

    __table_args__ = (
        Index('token_UNIQUE', 'token'),            # 令牌值索引（根据 Token 查找用户最频繁）喵~
        Index('fk_user_token_user_idx', 'user_id'), # 用户 ID 索引（查某个用户的所有 Token）喵~
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    # ForeignKey(User.id) —— 外键：关联到 user 表，保证数据完整性喵~
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    # Token 值 —— 使用 Python 的 uuid.uuid4() 生成随机唯一标识喵~
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
    # 过期时间 —— Token 不是永久的，过期后需要重新登录喵~
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")

    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token='{self.token}')>"
