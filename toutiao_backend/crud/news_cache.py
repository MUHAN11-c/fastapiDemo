"""
=== 新闻 CRUD（缓存版）===

这个模块在原有 CRUD 基础上增加了"缓存优先"策略喵~

"缓存优先"的查询流程：
1. 先查 Redis 缓存 → 有则直接返回（快！）喵~
2. 缓存没有 → 查 MySQL 数据库喵~
3. 把 MySQL 查到的结果写入 Redis 缓存（下次就快了）喵~
4. 返回结果喵~

这就是经典的 Cache-Aside 模式喵~

为什么缓存和数据库数据可能会不一致？
- 数据库数据变了，但缓存还是旧的数据喵~
- 解决方案：设置合理的过期时间（数据越稳定越持久）喵~
- 或者在数据修改时主动删除对应的缓存喵~
"""

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import (
    get_cached_categories, set_cache_categories,
    get_cache_news_list, set_cache_news_list,
    get_cached_news_detail, cache_news_detail,
    get_cached_related_news, cache_related_news
)
from models.news import Category, News
from schemas.base import NewsItemBase
from schemas.news import NewsDetailResponse, RelatedNewsResponse


# === 获取新闻分类列表（缓存优先）===
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 第1步：先尝试从 Redis 缓存中获取喵~
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories  # 缓存命中！直接返回，速度极快喵~

    # 第2步：缓存没命中，从 MySQL 数据库查询喵~
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    # 第3步：把查询结果写入缓存（下次就能命中了）喵~
    if categories:
        # jsonable_encoder 把 ORM 对象转成 Python 基础类型（dict/list）喵~
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    return categories


# === 获取新闻列表（缓存优先）===
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 计算页码（skip 是跳过的记录数，limit 是每页数量）喵~
    # 第1页 → skip=0 → page=1；第2页 → skip=10 → page=2 喵~
    page = skip // limit + 1

    # 第1步：查缓存喵~
    cached_list = await get_cache_news_list(category_id, page, limit)
    if cached_list:
        # 缓存中存的是字典，需要转回 ORM 对象喵~
        # News(**item) 把字典解包传给 News 构造函数喵~
        return [News(**item) for item in cached_list]

    # 第2步：查数据库喵~
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 第3步：写入缓存喵~
    if news_list:
        # model_validate() 把 ORM 对象转成 Pydantic 对象喵~
        # model_dump(mode="json") 把 Pydantic 对象转成 JSON 兼容的字典喵~
        # by_alias=False → 使用 Python 命名（category_id），不使用驼峰（categoryId）喵~
        news_data = [
            NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False)
            for item in news_list
        ]
        await set_cache_news_list(category_id, page, limit, news_data)

    return news_list


# === 获取新闻总数（不缓存，因为需要实时准确）===
async def get_news_count(db: AsyncSession, category_id: int):
    """新闻总数需要实时准确，所以不缓存喵~"""
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


# === 获取新闻详情（缓存优先）===
async def get_news_detail(db: AsyncSession, news_id: int):
    # 第1步：查缓存喵~
    cached_news = await get_cached_news_detail(news_id)
    if cached_news:
        # 把字典转回 ORM 对象返回喵~
        return News(**cached_news)

    # 第2步：查数据库喵~
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news = result.scalar_one_or_none()

    # 第3步：写入缓存（排除 related_news 字段）喵~
    if news:
        news_dict = NewsDetailResponse.model_validate(news).model_dump(
            by_alias=False, mode="json", exclude={'related_news'}
        )
        await cache_news_detail(news_id, news_dict)

    return news


# === 增加新闻浏览量 ===
async def increase_news_views(db: AsyncSession, news_id: int):
    """
    浏览量 +1 —— 直接操作数据库，不走缓存喵~
    使用 SQL 级别的 update，避免并发时数据不一致喵~
    views=News.views+1 是在数据库层面做加法，不是 Python 层面喵~
    """
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # rowcount > 0 表示确实更新了数据喵~
    return result.rowcount > 0


# === 获取相关推荐新闻（缓存优先）===
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # 第1步：查缓存喵~
    cached_related = await get_cached_related_news(news_id, category_id)
    if cached_related:
        return cached_related  # 缓存命中，直接返回喵~

    # 第2步：查数据库（同分类、排除当前新闻、按浏览量和时间排序）喵~
    stmt = select(News).where(
        News.category_id == category_id,  # 同分类喵~
        News.id != news_id               # 排除当前新闻喵~
    ).order_by(
        News.views.desc(),               # 浏览量高的排在前面喵~
        News.publish_time.desc()         # 发布时间新的排在前面喵~
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()

    # 第3步：写入缓存喵~
    if related_news:
        related_data = [
            RelatedNewsResponse.model_validate(news).model_dump(by_alias=False, mode="json")
            for news in related_news
        ]
        await cache_related_news(news_id, category_id, related_data)
        return related_data

    return []
