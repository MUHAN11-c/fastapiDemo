"""
=== Redis 缓存配置模块 ===

缓存是什么喵~ 就是把频繁访问的数据临时存储在"高速存储"中喵~
比如新闻分类列表不常变化，每次都查数据库太浪费，就放到 Redis 缓存中喵~

Redis 是一个内存数据库，读写速度极快（微秒级），非常适合做缓存喵~
数据库（MySQL）就像"仓库"——容量大但速度慢喵~
缓存（Redis）就像"桌面"——容量小但取东西超快喵~

这个模块提供了三个底层方法：
- get_cache(key)      —— 读取字符串缓存喵~
- get_json_cache(key)  —— 读取 JSON（列表/字典）缓存喵~
- set_cache(key, value, expire) —— 设置缓存喵~
"""

import json
from typing import Any

# redis.asyncio 是 Redis 的异步客户端，支持 async/await 喵~
import redis.asyncio as redis

# === Redis 连接配置 ===
REDIS_HOST = "localhost"  # Redis 服务器地址（本机）喵~
REDIS_PORT = 6379         # Redis 默认端口号喵~
REDIS_DB = 0              # 使用的数据库编号（Redis 支持 0~15 共 16 个数据库）喵~


# === 创建 Redis 异步客户端 ===
# decode_responses=True —— 自动把 Redis 返回的字节数据解码为字符串喵~
# 这样就不用手动 .decode('utf-8') 了喵~
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)


# === 读取缓存：字符串 ===
async def get_cache(key: str):
    """根据 key 从 Redis 获取字符串类型的缓存值喵~"""
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None


# === 读取缓存：JSON（列表/字典）===
async def get_json_cache(key: str):
    """
    根据 key 从 Redis 获取 JSON 格式的缓存值喵~
    Redis 存储的都是字符串，但 Python 中我们想要列表或字典喵~
    所以需要 json.loads() 把字符串"反序列化"成 Python 对象喵~
    """
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)  # 把 JSON 字符串转成 Python 的 list/dict 喵~
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败：{e}")
        return None


# === 设置缓存 ===
async def set_cache(key: str, value: Any, expire: int = 3600):
    """
    设置缓存（支持字符串、列表和字典）喵~

    参数：
    - key: 缓存的键名（建议有意义的命名，如 "news:categories"）喵~
    - value: 要缓存的值（字符串/列表/字典）喵~
    - expire: 过期时间（秒），默认 3600 秒 = 1 小时喵~

    setex = set + expire，设置值的同时设置过期时间喵~
    设置过期时间很重要！否则缓存会一直存在，占用内存喵~
    ensure_ascii=False —— 让中文正常保存而不是转成 \\uXXXX 格式喵~
    """
    try:
        # 如果是列表或字典，需要先用 json.dumps() 转成 JSON 字符串喵~
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        # setex(key, expire, value) —— 设置 key 的值为 value，expire 秒后自动删除喵~
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False
