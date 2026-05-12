"""
=== 浏览历史模块 - 数据库模型（ORM）===

浏览历史表（History）记录了"哪个用户在什么时间浏览了哪条新闻"喵~

和收藏表的区别：
- 收藏：用户主动操作（点击收藏按钮），同一条新闻只能收藏一次喵~
- 浏览历史：每次查看新闻都记录，同一条新闻可以多次浏览喵~
  所以这里没有 UniqueConstraint，允许多次记录喵~
"""

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, DateTime, ForeignKey, Index
from datetime import datetime
from .users import User
from .news import News


class Base(DeclarativeBase):
    pass


# === 浏览历史表（History）===
class History(Base):
    __tablename__ = 'history'

    # 注意：这里没有 UniqueConstraint，因为同一用户可多次浏览同一新闻喵~
    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),  # 按用户查浏览记录喵~
        Index('fk_history_news_idx', 'news_id'),  # 按新闻查浏览记录喵~
        Index('idx_view_time', 'view_time'),      # 按时间排序（最新浏览在最上面）喵~
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="浏览时间")

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
