"""
=== 收藏模块 - API 路由 ===

所有收藏相关的 API 接口（都需要登录）喵~

API 接口：
- GET    /api/favorite/check  —— 检查某新闻是否已收藏喵~
- POST   /api/favorite/add    —— 添加收藏喵~
- DELETE /api/favorite/remove —— 取消收藏喵~
- GET    /api/favorite/list   —— 获取收藏列表（分页）喵~
- DELETE /api/favorite/clear  —— 清空所有收藏喵~

所有接口都需要 Depends(get_current_user) 来校验登录状态喵~
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from models.users import User
from schemas.favorite import (
    FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
)
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# === 检查是否已收藏 ===
@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),        # 查询参数：新闻ID 喵~
    user: User = Depends(get_current_user),            # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """
    检查当前用户是否已经收藏了某条新闻喵~
    前端在展示新闻详情时调用，决定"收藏按钮"的状态喵~
    """
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckResponse(isFavorite=is_favorited)
    )


# === 添加收藏 ===
@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,                          # 请求体：{newsId: 123} 喵~
    user: User = Depends(get_current_user),            # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """添加收藏喵~"""
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)


# === 取消收藏 ===
@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),         # 查询参数：新闻ID 喵~
    user: User = Depends(get_current_user),            # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """取消收藏喵~"""
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏记录不存在"
        )
    return success_response(message="删除收藏成功")


# === 获取收藏列表 ===
@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),                        # 页码，最小为1喵~
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),            # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的收藏列表（带分页）喵~

    联表查询结果 rows 中每条数据是：(新闻对象, 收藏时间, 收藏ID) 喵~
    需要解包后重组成前端需要的格式喵~
    """
    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)

    # 解包联表查询结果，合并新闻信息和收藏信息喵~
    # **news.__dict__ 把新闻对象的所有属性展开，再添加 favorite_time 和 favorite_id 喵~
    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news, favorite_time, favorite_id in rows]

    # 判断是否还有更多喵~
    has_more = total > page * page_size

    data = FavoriteListResponse(list=favorite_list, total=total, hasMore=has_more)
    return success_response(message="获取收藏列表成功", data=data)


# === 清空所有收藏 ===
@router.delete("/clear")
async def clear_favorite(
    user: User = Depends(get_current_user),            # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """删除当前用户的所有收藏记录喵~"""
    count = await favorite.remove_all_favorites(db, user.id)
    return success_response(message=f"清空了{count}条记录")
