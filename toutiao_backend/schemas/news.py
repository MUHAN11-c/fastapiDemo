"""
=== 新闻模块 - 数据模型（Pydantic Schema）===

定义了新闻模块的请求体和响应数据结构喵~

- RelatedNewsResponse: 相关新闻的简化信息喵~
- NewsDetailResponse: 新闻详情（继承自 NewsItemBase，添加了 content 和 related_news）喵~
"""

from typing import Optional

from pydantic import Field, ConfigDict, BaseModel

from schemas.base import NewsItemBase


# === 相关新闻响应（简化版）===
class RelatedNewsResponse(BaseModel):
    """
    相关推荐新闻的响应模型 —— 只需要几个关键字段喵~
    不需要返回完整的新闻内容（content），那样响应数据太大了喵~
    """
    id: int
    title: str
    image: Optional[str] = None
    views: int

    model_config = ConfigDict(
        from_attributes=True,
    )


# === 新闻详情响应 ===
class NewsDetailResponse(NewsItemBase):
    """
    新闻详情响应 —— 继承自 NewsItemBase，添加更多字段喵~

    继承的好处：不需要把 id、title、author 等基础字段再写一遍喵~
    只需要定义"新增的字段"即可喵~
    """
    content: str  # 新闻的完整内容（Text 类型）喵~
    # Field(default_factory=list) —— 默认值为空列表喵~
    # alias="relatedNews" —— JSON 中使用驼峰命名 relatedNews 喵~
    related_news: list[RelatedNewsResponse] = Field(default_factory=list, alias="relatedNews")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
