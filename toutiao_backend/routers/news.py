"""
=== 新闻模块 - API 路由 ===

这个模块定义了所有新闻相关的 API 接口喵~

API 接口：
- GET  /api/news/categories —— 获取新闻分类列表喵~
- GET  /api/news/list —— 获取新闻列表（按分类 + 分页）喵~
- GET  /api/news/detail —— 获取新闻详情（含浏览量+1 和相关推荐）喵~

使用 APIRouter 而不是 app.get() 的好处：
- 每个模块独立管理自己的路由喵~
- 通过 prefix="/api/news" 统一设置前缀喵~
- 通过 tags=["news"] 在 Swagger 文档中分组显示喵~
- 最后在 main.py 中统一注册（app.include_router）喵~
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news
from crud import news_cache  # 缓存版的 CRUD 方法喵~

# === 创建 APIRouter 实例 ===
# prefix="/api/news" —— 所有接口的 URL 前缀喵~
#   比如 @router.get("/categories") 的实际访问路径是 /api/news/categories 喵~
# tags=["news"] —— 在 Swagger 文档中归到"news"分组喵~
router = APIRouter(prefix="/api/news", tags=["news"])

# === 接口开发流程 ===
# 1. 看 API 接口规范文档 → 确定接口的路径、参数、响应格式喵~
# 2. 在 models/ 中定义数据库表模型（ORM）喵~
# 3. 在 crud/ 中封装操作数据库的方法喵~
# 4. 在 routers/ 中编写路由处理函数，调用 crud 方法喵~


# === 获取新闻分类列表 ===
@router.get("/categories")
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    # Depends(get_db) —— 注入数据库会话（FastAPI 自动管理生命周期）喵~
    db: AsyncSession = Depends(get_db)
):
    """返回所有新闻分类（支持分页）喵~"""
    # 调用缓存版 CRUD 方法（先查 Redis，没有则查 MySQL）喵~
    categories = await news_cache.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }


# === 获取新闻列表 ===
@router.get("/list")
async def get_news_list(
    # Query(..., alias="categoryId") —— 查询参数，必填(...)，前端用驼峰 categoryId 喵~
    category_id: int = Query(..., alias="categoryId"),
    page: int = 1,  # 页码，默认第1页喵~
    # le=100 —— 每页最多 100 条，防止一次请求太多数据喵~
    page_size: int = Query(10, alias="pageSize", le=100),
    db: AsyncSession = Depends(get_db)
):
    """获取指定分类下的新闻列表（带分页）喵~"""
    # 计算 offset（跳过的记录数）喵~
    # 第1页 skip=0，第2页 skip=10，第3页 skip=20 ... 喵~
    offset = (page - 1) * page_size

    # 查询新闻列表（带缓存）喵~
    news_list = await news_cache.get_news_list(db, category_id, offset, page_size)
    # 查询该分类的总新闻数（不走缓存，需要实时准确）喵~
    total = await news.get_news_count(db, category_id)

    # 判断"是否还有更多数据"喵~
    # (已跳过的 + 当前返回的) < 总数 → 还有更多喵~
    has_more = (offset + len(news_list)) < total

    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }


# === 获取新闻详情 ===
@router.get("/detail")
async def get_news_detail(
    # Query(..., alias="id") —— 前端用 ?id=xxx 来传递新闻 ID 喵~
    news_id: int = Query(..., alias="id"),
    db: AsyncSession = Depends(get_db)
):
    """获取新闻详情、增加浏览量、返回相关推荐喵~"""
    # 第1步：获取新闻详情（带缓存）喵~
    news_detail = await news_cache.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 第2步：浏览量 +1（直接操作数据库，不走缓存）喵~
    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 第3步：获取相关推荐新闻（带缓存）喵~
    related_news = await news_cache.get_related_news(db, news_detail.id, news_detail.category_id)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,  # 驼峰命名喵~
            "categoryId": news_detail.category_id,    # 驼峰命名喵~
            "views": news_detail.views,
            "relatedNews": related_news               # 驼峰命名喵~
        }
    }
