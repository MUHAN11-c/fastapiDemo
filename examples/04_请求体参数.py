"""
=== 第4课：请求体参数（Request Body）===

请求体是 POST/PUT 请求时附带的数据体喵~ 比如注册时提交的用户名和密码喵~

学习要点：
- Pydantic BaseModel —— 定义数据模型，自动校验数据喵~
- Field() —— 给字段添加校验规则和描述喵~
- POST 方法 —— @app.post 处理数据提交喵~
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 定义请求体数据模型 —— 描述"注册"需要的数据结构喵~
class User(BaseModel):
    # default="张三" —— 默认值（API文档中会显示）喵~
    username: str = Field(default="张三", min_length=2, max_length=10, description="用户名，长度要求2-10个字")
    # 没有 default，所以 password 是必填字段喵~
    password: str = Field(min_length=3, max_length=20)


# POST 路由 —— 数据在请求体中，不在 URL 中喵~
@app.post("/register")
async def register(user: User):
    # FastAPI 自动校验请求体，转成 User 对象喵~
    return user


# === 测试方法 ===
# 访问 /docs → POST /register → Try it out → 输入JSON → Execute 喵~
# 示例请求体：{"username": "小明", "password": "abc123"}
