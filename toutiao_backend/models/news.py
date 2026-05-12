"""
=== 新闻模块 - 数据库模型（ORM）===

这里定义了两个数据库表对应的 Python 类喵~

1. Category（新闻分类表）—— 存储新闻的分类信息，如"科技"、"娱乐"等喵~
2. News（新闻表）—— 存储新闻的详细内容喵~

ORM 的核心概念：
- Python 类 = 数据库表
- 类的属性 = 表的列
- 类的实例 = 表中的一行数据

SQLAlchemy 2.0 使用了新的"声明式映射"语法：
- Mapped[类型] —— 声明 Python 中的类型
- mapped_column(...) —— 声明数据库中的列属性

索引（Index）的作用 —— 就像书的目录，帮助快速查找数据喵~
给经常查询的字段加索引，查询速度能提升几十倍喵~
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


# === 基类：所有模型类都继承它喵~ ===
# 定义所有表共有的字段（创建时间、更新时间），避免在每个表里重复定义喵~
class Base(DeclarativeBase):
    # 创建时间：插入数据时自动填入当前时间喵~
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    # 更新时间：每次修改数据时自动更新喵~
    # onupdate=datetime.now —— 每次 UPDATE 操作时自动更新这个字段喵~
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )


# === 新闻分类表（Category）===
class Category(Base):
    __tablename__ = "news_category"  # 数据库中的表名喵~

    # autoincrement=True —— 主键自增，插入新数据时自动生成递增的 ID 喵~
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    # unique=True —— 值必须唯一（不能有两个同名的分类）喵~
    # nullable=False —— 不允许为空喵~
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    # default=0 —— 默认值为 0，数值越小排名越靠前喵~
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    def __repr__(self):
        """对象的字符串表示，方便调试时打印查看喵~"""
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"


# === 新闻表（News）===
class News(Base):
    __tablename__ = "news"

    # __table_args__ 用于定义表级别的约束和索引喵~
    __table_args__ = (
        # Index('索引名', '列名') —— 给 category_id 创建索引（因为经常按分类查新闻）喵~
        Index('fk_news_category_idx', 'category_id'),
        # 给 publish_time 创建索引（因为经常按时间排序）喵~
        Index('idx_publish_time', 'publish_time')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    # Optional[str] —— Python 类型提示：这个字段可以是 str 或 None 喵~
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    # Text 类型 —— 比 String 更大，适合存长文本内容喵~
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    # ForeignKey('news_category.id') —— 外键约束，关联到 news_category 表的 id 字段喵~
    # 确保 category_id 的值一定是 news_category 表中存在的合法分类 ID 喵~
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
