"""
=== 第9课：依赖注入（Dependency Injection）===

把重复的代码抽出来，让多个路由共享喵~
比如分页参数，新闻列表和用户列表都需要，抽成一个"依赖项"即可喵~

Depends() 是 FastAPI 依赖注入的核心喵~
"""

from fastapi import FastAPI, Query, Depends  # Depends 是依赖注入的关键喵~

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 分页参数逻辑共用： 新闻列表和用户列表
# 1. 依赖项
async def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=60)
):
    return {"skip": skip, "limit": limit}


# 3. 声明依赖项 → 依赖注入
@app.get("/news/news_list")
async def get_news_list(commons=Depends(common_parameters)):
    return commons


@app.get("/user/user_list")
async def get_user_list(commons=Depends(common_parameters)):
    return commons
