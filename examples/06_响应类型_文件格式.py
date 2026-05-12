"""
=== 第6课：响应类型 —— 文件格式 ===

返回文件（图片、PDF等）给用户下载或展示喵~
使用 FileResponse 类来处理文件响应喵~
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 返回文件 —— FileResponse(文件路径) 喵~
@app.get("/file")
async def get_file():
    path = "./files/1.jpeg"
    return FileResponse(path)


# === 测试 ===
# 访问 /file 浏览器会显示图片喵~
