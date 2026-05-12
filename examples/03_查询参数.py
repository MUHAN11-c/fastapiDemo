"""
=== 第3课：查询参数（Query Parameters）===

查询参数就是 URL 中 ? 后面的部分，用 & 分隔喵~
比如 /news?skip=0&limit=10 中的 skip 和 limit 喵~

查询参数的特点：可选的（不传用默认值），适合做分页、筛选喵~
"""

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 查询参数示例：?skip=5&limit=3 跳过5条返回3条喵~
@app.get("/news/news_list")
async def get_news_list(
    # Query(0) —— 默认值为0，不传就用默认值（可选参数）喵~
    skip: int = Query(0, description="跳过的记录数", lt=100),
    limit: int = Query(10, description="返回的记录数")
):
    return {"skip": skip, "limit": limit}


# === 路径参数 vs 查询参数 ===
# 路径参数：/book/{id} —— 写在路径中，用于标识"资源"喵~
# 查询参数：?skip=0&limit=10 —— 写在?后面，用于"筛选/分页"喵~
