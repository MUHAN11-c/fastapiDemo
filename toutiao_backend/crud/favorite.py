"""
=== 收藏 CRUD ===

收藏功能的数据库操作喵~

核心功能：
- is_news_favorite() —— 检查某新闻是否已被收藏喵~
- add_news_favorite() —— 添加收藏喵~
- remove_news_favorite() —— 取消收藏喵~
- get_favorite_list() —— 获取收藏列表（联表查询 + 分页）喵~
- remove_all_favorites() —— 清空所有收藏喵~

联表查询（JOIN）：
收藏表只存了 user_id 和 news_id，但列表页需要显示新闻的标题、图片等喵~
所以需要 JOIN news 表一起查询，一次拿到所有需要的数据喵~
"""

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


# === 检查是否已收藏 ===
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    """
    检查某个用户是否已经收藏了某条新闻喵~
    返回 True（已收藏）或 False（未收藏）喵~
    """
    query = select(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.news_id == news_id
    )
    result = await db.execute(query)
    # 如果能查到记录，说明已收藏喵~
    return result.scalar_one_or_none() is not None


# === 添加收藏 ===
async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    """
    添加收藏喵~
    如果用户重复收藏同一新闻，数据库的 UniqueConstraint 会阻止喵~
    """
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)  # 回读数据库生成的数据（如 id、created_at）喵~
    return favorite


# === 取消收藏 ===
async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    """
    取消收藏喵~
    使用 delete() 语句而不是 db.delete() 方法，更高效（不需要先查询）喵~
    返回 True（删除成功）或 False（没找到记录）喵~
    """
    stmt = delete(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0  # rowcount 表示受影响的行数喵~


# === 获取收藏列表（联表查询 + 分页）===
async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """
    获取用户的收藏列表喵~

    联表查询：Favorite join News 喵~
    为什么需要 join？
    - Favorite 表中只有 user_id 和 news_id 喵~
    - 但前端需要显示新闻的标题、图片、作者等信息喵~
    - 所以需要 JOIN news 表来获取新闻的完整信息喵~

    返回值：
    - rows: 包含 (新闻对象, 收藏时间, 收藏ID) 的元组列表喵~
    - total: 总收藏数（用于分页计算）喵~
    """
    # 第1步：查询总数（用于分页）喵~
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 第2步：联表查询收藏列表喵~
    offset = (page - 1) * page_size

    # 解释这个查询：
    # select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
    #   查询新闻对象 + 收藏时间（别名 favorite_time）+ 收藏ID（别名 favorite_id）喵~
    # .join(Favorite, Favorite.news_id == News.id)
    #   JOIN 条件：收藏表的 news_id 等于新闻表的 id 喵~
    # .label("别名") 给字段起别名，方便后面使用喵~
    query = (
        select(
            News,
            Favorite.created_at.label("favorite_time"),
            Favorite.id.label("favorite_id")
        )
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())  # 最新收藏的排在前面喵~
        .offset(offset).limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# === 清空所有收藏 ===
async def remove_all_favorites(db: AsyncSession, user_id: int):
    """
    删除某个用户的所有收藏记录喵~
    返回删除的数量喵~
    """
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
