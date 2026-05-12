"""
=== 浏览历史模块 - API 路由 ===

所有浏览历史相关的 API 接口（都需要登录）喵~

API 接口：
- POST   /api/history/add         —— 添加浏览记录喵~
- GET    /api/history/list        —— 获取浏览历史列表（分页）喵~
- DELETE /api/history/delete/{id} —— 删除单条浏览记录喵~
- DELETE /api/history/clear       —— 清空所有浏览记录喵~

浏览历史自动记录：
前端在用户查看新闻详情时，调用 POST /api/history/add 自动记录喵~
用户不需要手动操作喵~
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import history
from models.users import User
from schemas.history import (
    HistoryAddRequest, HistoryNewsItemResponse, HistoryListResponse
)
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])


# === 添加浏览历史 ===
@router.post("/add")
async def add_history(
    data: HistoryAddRequest,                    # 请求体：{newsId: 123} 喵~
    user: User = Depends(get_current_user),     # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """
    记录浏览历史喵~
    如果用户之前浏览过 → 更新浏览时间喵~
    如果是第一次浏览 → 创建新记录喵~
    """
    result = await history.add_history(db, user.id, data.news_id)
    return success_response(message="添加成功", data=result)


# === 获取浏览历史列表 ===
@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1),                 # 页码，最小为1喵~
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),     # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的浏览历史列表（带分页）喵~
    按浏览时间倒序排列（最新浏览的在最上面）喵~
    """
    rows, total = await history.get_history_list(db, user.id, page, page_size)

    # 判断是否还有更多数据喵~
    has_more = total > page * page_size

    # 解包联表查询结果喵~
    # 每条 row 是：(新闻ORM对象, 浏览时间, 历史记录ID) 喵~
    history_list = [HistoryNewsItemResponse.model_validate({
        **news.__dict__,
        "view_time": view_time,
        "history_id": history_id
    }) for news, view_time, history_id in rows]

    data = HistoryListResponse(list=history_list, total=total, hasMore=has_more)
    return success_response(data=data)


# === 删除单条浏览历史 ===
@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: int,                            # 路径参数：历史记录ID 喵~
    user: User = Depends(get_current_user),     # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """删除指定 ID 的浏览历史记录喵~"""
    result = await history.delete_history(db, user.id, history_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="历史记录不存在"
        )
    return success_response(message="删除成功")


# === 清空所有浏览历史 ===
@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),     # 验证登录喵~
    db: AsyncSession = Depends(get_db)
):
    """清空当前用户的所有浏览历史记录喵~"""
    result = await history.clear_history(db, user.id)
    return success_response(message="清空成功")
