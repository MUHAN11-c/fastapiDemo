"""
=== 第7课：自定义响应数据格式（response_model）===

response_model 过滤响应字段，只返回指定的数据喵~
例如数据库有10个字段，但只返回 id、title、content 这3个喵~

response_model 的作用：
- 过滤不需要返回的字段（安全性）喵~
- 自动校验响应数据格式喵~
- 自动生成 API 文档中的响应示例喵~
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 定义响应数据模型 —— 描述"返回给客户端"的数据结构喵~
class News(BaseModel):
    id: int
    title: str
    content: str


# response_model=News —— 只返回 News 中定义的3个字段喵~
@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是第{id}本书",
        "content": "这是一本好书"
    }


# === 为什么用 response_model？===
# 1. 安全 —— 避免意外暴露敏感字段（如密码hash）喵~
# 2. 规范 —— 统一响应数据格式喵~
# 3. 文档 —— Swagger 自动展示响应结构喵~
