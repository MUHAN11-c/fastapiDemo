"""
=== 数据库配置模块 ===

这个模块负责：
1. 创建数据库异步引擎（Engine）—— 管理数据库连接池喵~
2. 创建异步会话工厂（SessionMaker）—— 生产数据库会话喵~
3. 提供 get_db 依赖项 —— 供路由注入使用喵~

数据库连接 URL 格式：
  数据库类型+驱动://用户名:密码@主机地址:端口/数据库名?参数

关键技术点：
- 异步引擎（AsyncEngine）：使用 aiomysql 驱动，支持异步 IO 喵~
- 连接池：pool_size 指定"常驻连接数"，max_overflow 指定"最大额外连接数"喵~
- 事务管理：正常提交 commit，异常回滚 rollback，最终关闭 close 喵~
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# === 1. 数据库连接 URL ===
# root:123456 —— 用户名和密码（学习用，生产环境应从环境变量读取）喵~
# localhost:3306 —— MySQL 默认端口 3306 喵~
# news_app —— 数据库名（需要先在 MySQL 中创建）喵~
# charset=utf8mb4 —— 支持 emoji 的 UTF-8 编码喵~
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"

# === 2. 创建异步引擎 ===
# 引擎是 SQLAlchemy 的核心，负责和数据库通信喵~
# echo=True —— 在控制台输出所有 SQL 语句（开发调试用，生产环境应设为 False）喵~
# pool_size=10 —— 连接池保持 10 个"常驻连接"，不用每次都新建连接喵~
# max_overflow=20 —— 当 10 个连接不够用时，允许额外创建最多 20 个连接喵~
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,       # 输出 SQL 日志喵~
    pool_size=10,    # 连接池常驻连接数喵~
    max_overflow=20  # 允许额外创建的连接数喵~
)

# === 3. 创建异步会话工厂 ===
# async_sessionmaker 是一个"工厂函数"，每次调用都会创建一个新的数据库会话喵~
# 会话（Session）是操作数据库的"工作单元"：查询、新增、修改、删除都在会话中进行喵~
# expire_on_commit=False —— 提交后会话不会过期（缓存 ORM 对象，不用重新查询）喵~
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,     # 绑定到上面创建的引擎喵~
    class_=AsyncSession,   # 使用异步会话类喵~
    expire_on_commit=False # 提交后不过期喵~
)


# === 4. 数据库会话依赖项（供 FastAPI Depends 使用）===
# 这是一个"生成器函数"（用 yield 而不是 return）喵~
# yield 之前：创建资源（打开会话）喵~
# yield 之后：清理资源（提交/回滚 + 关闭会话）喵~
# FastAPI 的 Depends 会自动管理这个生命周期喵~
async def get_db():
    # 创建会话（async with 确保会话最后一定被关闭）喵~
    async with AsyncSessionLocal() as session:
        try:
            # 把会话"交给"路由函数使用喵~
            yield session
            # 路由函数正常执行完 → 提交事务（保存所有数据库修改）喵~
            await session.commit()
        except Exception:
            # 路由函数抛出异常 → 回滚事务（撤销所有数据库修改）喵~
            await session.rollback()
            raise  # 重新抛出异常，让异常处理器处理喵~
        finally:
            # 无论如何都要关闭会话（归还连接给连接池）喵~
            await session.close()
