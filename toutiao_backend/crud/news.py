"""
=== 新闻 CRUD（基础版，无缓存）===

CRUD = Create / Read / Update / Delete 喵~

这个模块是原始的新闻数据操作（不包含缓存），作为学习参考喵~
实际项目中使用的是 news_cache.py（缓存版）喵~

每个函数都只做一件事：操作数据库喵~
路由函数（routers/）负责接收 HTTP 请求、调用这里的函数、返回响应喵~
"""

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


# === 获取新闻分类列表 ===
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取所有新闻分类，支持分页喵~"""
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# === 获取指定分类下的新闻列表 ===
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    """获取某个分类下的新闻列表，支持分页喵~"""
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# === 获取指定分类下的新闻总数 ===
async def get_news_count(db: AsyncSession, category_id: int):
    """统计某个分类下有多少条新闻喵~"""
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    # scalar_one() —— 聚合查询确保返回一个值喵~
    return result.scalar_one()


# === 获取单条新闻详情 ===
async def get_news_detail(db: AsyncSession, news_id: int):
    """根据新闻 ID 获取新闻详情，找不到返回 None 喵~"""
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# === 增加新闻浏览量 ===
async def increase_news_views(db: AsyncSession, news_id: int):
    """
    浏览量 +1 喵~
    使用 SQL 级别的 update 语句，避免并发问题喵~
    News.views + 1 是在数据库层面做计算，不是 Python 层面喵~
    如果在 Python 中做 +1（views += 1），多个请求同时读取可能会互相覆盖喵~
    """
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 检查是否真的更新了数据（防止 news_id 不存在）喵~
    return result.rowcount > 0


# === 获取相关推荐新闻 ===
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    """
    获取同分类下的相关新闻推荐喵~
    排序规则：浏览量高的在前，发布时间新的在前喵~
    排除当前新闻自己喵~
    """
    stmt = select(News).where(
        News.category_id == category_id,  # 同分类喵~
        News.id != news_id               # 排除当前新闻喵~
    ).order_by(
        News.views.desc(),               # 浏览量降序（高的在前面）喵~
        News.publish_time.desc()         # 发布时间降序（新的在前面）喵~
    ).limit(limit)

    result = await db.execute(stmt)
    related_news = result.scalars().all()

    # 使用列表推导式，把 ORM 对象转成前端需要的格式喵~
    # 这样做的好处：精确控制返回哪些字段，不暴露数据库内部细节喵~
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,  # 驼峰命名喵~
        "categoryId": news_detail.category_id,    # 驼峰命名喵~
        "views": news_detail.views
    } for news_detail in related_news]
