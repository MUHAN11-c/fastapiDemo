"""
=== 第5课：响应类型 —— HTML 格式 ===

FastAPI 默认返回 JSON，但也可以返回 HTML 喵~
通过 response_class=HTMLResponse 指定响应为 HTML 格式喵~
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 返回 HTML 内容 —— 必须指定 response_class=HTMLResponse 喵~
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一级标题</h1>"


# === 测试 ===
# 访问 /html 看到渲染后的 HTML 标题（大字加粗）喵~
