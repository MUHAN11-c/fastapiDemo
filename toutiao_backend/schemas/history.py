"""
=== 浏览历史模块 - 数据模型（Pydantic Schema）===

定义了浏览历史功能的所有请求/响应数据模型喵~

浏览历史功能需求：
- 记录浏览：用户查看新闻详情时，自动记录浏览历史喵~
- 历史列表：按时间倒序显示用户的浏览历史（带分页）喵~
"""

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


# === 添加历史记录请求体 ===
class HistoryAddRequest(BaseModel):
    """前端只需要传一个 newsId 就能记录浏览历史喵~"""
    news_id: int = Field(..., alias="newsId")


# === 浏览历史列表中的新闻项响应 ===
class HistoryNewsItemResponse(NewsItemBase):
    """
    继承 NewsItemBase（新闻基础字段），加上浏览历史相关的字段喵~
    """
    history_id: int = Field(alias="historyId")     # 历史记录的 ID 喵~
    view_time: datetime = Field(alias="viewTime")   # 浏览时间喵~

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# === 浏览历史列表整体响应 ===
class HistoryListResponse(BaseModel):
    """浏览历史列表的分页响应格式喵~"""
    list: list[HistoryNewsItemResponse]  # 历史列表数据喵~
    total: int                           # 总记录数喵~
    has_more: bool = Field(alias="hasMore")  # 是否还有更多数据喵~

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
