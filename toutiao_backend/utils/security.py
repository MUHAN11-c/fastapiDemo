"""
=== 安全工具模块 —— 密码加密与验证 ===

绝不能用明文存储密码！如果数据库被泄露，所有用户的密码就暴露了喵~

bcrypt 是一种密码哈希算法，特点：
- 单向加密（只能加密，不能解密）喵~
- 同样的密码每次加密结果不同（加了随机"盐"值）喵~
- 验证时使用 verify() 方法比对，而不是解密后比对喵~

工作原理：
1. 注册时：用户输入密码"123456" → hash("123456") → 存到数据库 "$2b$12$..." 喵~
2. 登录时：用户输入"123456" → verify("123456", 数据库中的hash值) → True/False 喵~
"""

from passlib.context import CryptContext

# === 创建密码加密上下文 ===
# schemes=["bcrypt"] —— 使用 bcrypt 算法喵~
# deprecated="auto" —— 自动管理算法弃用（如果 bcrypt 过时了会自动警告）喵~
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === 密码加密（注册时使用）===
def get_hash_password(password: str):
    """
    把明文密码加密成 hash 值喵~
    例如：get_hash_password("123456") → "$2b$12$LJ3m..." 喵~
    """
    return pwd_context.hash(password)


# === 密码验证（登录时使用）===
def verify_password(plain_password, hashed_password):
    """
    验证明文密码是否和数据库中的 hash 值匹配喵~
    verify() 不是"解密后比对"，而是"用同样的算法重新加密后比对"喵~
    返回值是布尔型：True（匹配）或 False（不匹配）喵~
    """
    return pwd_context.verify(plain_password, hashed_password)
