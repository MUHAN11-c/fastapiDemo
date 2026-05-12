"""
=== 浏览历史 CRUD ===

浏览历史功能的数据库操作喵~

和收藏的不同：
- 浏览历史允许重复记录（同一条新闻可以多次浏览）喵~
- 如果用户之前浏览过，再次浏览时只更新 view_time（浏览时间）喵~
- 没有 UniqueConstraint，因为允许重复喵~
"""

from datetime import datetime

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


# === 添加/更新浏览历史 ===
async def add_history(db: AsyncSession, user_id: int, news_id: int):
    """
    记录浏览历史喵~

    特殊逻辑：如果用户之前浏览过这条新闻 → 只更新浏览时间喵~
    如果第一次浏览 → 创建新记录喵~

    这样避免了同一个用户对同一条新闻产生大量重复记录，
    既节省了存储空间，又不影响用户体验喵~
    """
    # 先查一下：用户是否已经有这条新闻的浏览记录了喵~
    query = select(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(query)
    existing_history = result.scalar_one_or_none()

    if existing_history:
        # 已经浏览过 → 只更新浏览时间为"现在"喵~
        existing_history.view_time = datetime.now()
        await db.commit()
        await db.refresh(existing_history)
        return existing_history
    else:
        # 第一次浏览 → 创建新的浏览记录喵~
        history = History(user_id=user_id, news_id=news_id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history


# === 获取浏览历史列表（联表查询 + 分页）===
async def get_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """
    获取用户的浏览历史列表，按时间倒序喵~

    联表查询：History join News 喵~
    同一个新闻可能多次浏览，每次都显示（按最新浏览时间排序）喵~
    """
    offset = (page - 1) * page_size

    # 查询总数喵~
    count_query = select(func.count(History.id)).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 联表查询历史列表喵~
    # select(News, History.view_time, History.id) —— 查询新闻信息 + 浏览时间 + 历史ID 喵~
    query = (
        select(
            News,
            History.view_time.label("view_time"),
            History.id.label("history_id")
        )
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())  # 最新浏览的排在最前面喵~
        .offset(offset).limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# === 删除单条浏览历史 ===
async def delete_history(db: AsyncSession, user_id: int, news_id: int):
    """
    删除某条浏览历史记录喵~
    返回 True（删除成功）或 False（没找到记录）喵~
    """
    query = delete(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


# === 清空所有浏览历史 ===
async def clear_history(db: AsyncSession, user_id: int):
    """
    清空某个用户的所有浏览历史喵~
    返回删除的数量喵~
    """
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0
