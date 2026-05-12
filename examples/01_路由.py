"""
=== 第1课：路由（Routing）===

路由就是把一个网址（URL路径）和一个函数绑定起来喵~
当用户访问这个网址时，绑定的函数就会执行，返回结果喵~

学习要点：
- @app.get("/path") 装饰器 —— 把函数注册到指定 URL 路径喵~
- async 异步函数 —— 可以同时处理多个请求不阻塞喵~
- FastAPI 自动把返回的字典转成 JSON 格式喵~
"""

from fastapi import FastAPI

# 创建 FastAPI 应用实例 —— app 就是我们的 Web 应用喵~
app = FastAPI()


# 定义根路由 —— 访问 http://localhost:8000/ 会执行这个函数喵~
@app.get("/")
async def root():
    return {"message": "Hello World888"}


# 定义第二个路由 —— 访问 /hello 返回不同的内容喵~
@app.get("/hello")
async def get_hello():
    return {"msg": "你好 FastAPI"}


# === 运行方法 ===
# 终端输入：uvicorn 01_路由:app --reload
# 然后访问 http://localhost:8000/docs 看自动生成的 API 文档喵~
