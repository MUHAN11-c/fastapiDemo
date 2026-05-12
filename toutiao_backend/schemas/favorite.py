"""
=== 收藏模块 - 数据模型（Pydantic Schema）===

定义了收藏功能的所有请求/响应数据模型喵~

收藏功能的需求：
- 添加收藏：前端传 newsId → 后端记录收藏喵~
- 取消收藏：前端传 newsId → 后端删除收藏记录喵~
- 检查是否已收藏：前端传 newsId → 后端返回 true/false 喵~
- 收藏列表：返回用户收藏的新闻列表（带分页）喵~
"""

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


# === 检查收藏状态响应 ===
class FavoriteCheckResponse(BaseModel):
    """返回某条新闻是否已被当前用户收藏喵~"""
    is_favorite: bool = Field(..., alias="isFavorite")


# === 添加/取消收藏请求体 ===
class FavoriteAddRequest(BaseModel):
    """添加或取消收藏都只需要一个 newsId 喵~"""
    news_id: int = Field(..., alias="newsId")


# === 收藏列表中的新闻项响应 ===
class FavoriteNewsItemResponse(NewsItemBase):
    """
    继承 NewsItemBase（新闻的基础字段），再加上收藏相关的字段喵~
    这样一条数据就同时包含了"新闻信息"和"收藏信息"喵~
    """
    favorite_id: int = Field(alias="favoriteId")     # 收藏记录的 ID 喵~
    favorite_time: datetime = Field(alias="favoriteTime")  # 收藏时间喵~

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# === 收藏列表整体响应 ===
class FavoriteListResponse(BaseModel):
    """收藏列表的分页响应格式喵~"""
    list: list[FavoriteNewsItemResponse]  # 收藏列表数据喵~
    total: int                            # 总收藏数喵~
    has_more: bool = Field(alias="hasMore")  # 是否还有更多数据喵~

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
