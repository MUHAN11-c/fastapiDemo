"""
=== 第2课：路径参数（Path Parameters）===

路径参数就是把参数直接写在 URL 路径里面喵~
比如 /book/5 中的 5 就是一个路径参数，表示第5本书喵~

学习要点：
- {参数名} 在路径中占位，函数参数名必须一致喵~
- Path() 提供校验：gt/lt 数值范围、min_length/max_length 字符串长度喵~
- ... 表示参数是必填的喵~
"""

from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 路径参数示例：/book/5 → id=5，返回第5本书的信息喵~
@app.get("/book/{id}")
async def get_book(
    # Path(...) 必填，gt=0 必须大于0，lt=101 必须小于101 喵~
    id: int = Path(..., gt=0, lt=101, description="书籍id，取值范围1-100")
):
    return {"id": id, "title": f"这是第{id}本书"}


# 字符串类型的路径参数：/author/张三 → name="张三" 喵~
@app.get("/author/{name}")
async def get_name(
    # min_length=2 最少2个字符，max_length=10 最多10个字符喵~
    name: str = Path(..., min_length=2, max_length=10)
):
    return {"msg": f"这是{name}的信息"}


# === 测试 ===
# /book/5 正常；/book/0 报错；/author/张三 正常；/author/a 报错喵~
