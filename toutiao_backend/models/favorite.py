"""
=== 收藏模块 - 数据库模型（ORM）===

收藏表（Favorite）记录了"哪个用户收藏了哪条新闻"喵~

重要的设计点：
- UniqueConstraint('user_id', 'news_id') —— 唯一约束喵~
  同一个用户对同一条新闻只能收藏一次，不能重复收藏喵~
- ForeignKey(User.id) 和 ForeignKey(News.id) —— 外键约束喵~
  确保 user_id 和 news_id 都是有效的（指向存在的用户和新闻）喵~
"""

from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 导入关联的模型类（用于定义外键）喵~
from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


# === 收藏表（Favorite）===
class Favorite(Base):
    __tablename__ = 'favorite'

    __table_args__ = (
        # 联合唯一约束：同一个用户不能重复收藏同一条新闻喵~
        # 如果用户尝试重复收藏，数据库会抛出 IntegrityError 异常喵~
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),  # 按用户查收藏列表 → 建索引喵~
        Index('fk_favorite_news_idx', 'news_id'),  # 按新闻查被谁收藏 → 建索引喵~
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    # ForeignKey(User.id) —— user_id 必须是 user 表中存在的合法用户 ID 喵~
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    # ForeignKey(News.id) —— news_id 必须是 news 表中存在的合法新闻 ID 喵~
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    # datetime.utcnow —— 使用 UTC 时间（标准时间），避免时区混乱喵~
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="收藏时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, created_at={self.created_at})>"
