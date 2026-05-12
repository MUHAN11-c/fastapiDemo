"""
=== 基础 Schema（共享数据模型）===

Schema（Pydantic 模型）的作用：
- 定义 API 请求体和响应的数据结构喵~
- 自动校验数据（类型不对、字段缺失都会报错）喵~
- 自动生成 API 文档（Swagger UI）中的请求/响应示例喵~

基础 Schema 放在这里，各个子模块可以继承和复用喵~
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# === 新闻列表项基础模型 ===
# 这个模型被新闻列表、收藏列表、历史列表等多个地方共用喵~
class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    # Field(alias="categoryId") —— 定义别名喵~
    # 前端使用驼峰命名 categoryId，后端 Python 使用下划线命名 category_id 喵~
    # alias 让两者可以自动转换喵~
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")

    # ConfigDict 是 Pydantic v2 的配置方式（替代了 v1 的 class Config）喵~
    model_config = ConfigDict(
        # from_attributes=True —— 允许从 ORM 对象属性中读取值喵~
        # 这样就能直接用 UserInfoResponse.model_validate(orm_object) 转换喵~
        from_attributes=True,
        # populate_by_name=True —— 允许同时使用字段名和别名来赋值喵~
        # 比如可以用 category_id 或 categoryId 来给 category_id 赋值喵~
        populate_by_name=True
    )
