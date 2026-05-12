"""
=== 第8课：中间件（Middleware）===

中间件是一个"拦截器"，在每个请求前后都会执行喵~
就像"安检门"，请求进来和出去都要经过它喵~

中间件执行顺序（洋葱模型）：
请求 → 中间件2开始 → 中间件1开始 → 路由函数 → 中间件1结束 → 中间件2结束 → 响应喵~

常见用途：记录日志、跨域处理、权限验证、统一添加响应头喵~
"""

from fastapi import FastAPI

app = FastAPI()


@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response


@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}
