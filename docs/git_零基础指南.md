# Git 零基础入门指南

## 什么是 Git？

Git 是一个**版本控制工具**喵~ 它可以记录项目代码的每一次修改，方便回退、协作和备份喵~

把 Git 想象成游戏里的"存档"功能：
- 写完一个功能 → 存档（commit）喵~
- 改坏了代码 → 读档（checkout/reset）回退喵~
- 多个人协作 → 每个人在自己分支上修改，最后合并喵~

GitHub 是"远程存档仓库"，把你的代码备份到云端喵~

## 核心概念

| 概念 | 解释 |
|------|------|
| 仓库（Repository） | 一个项目就是一个仓库，包含所有代码和历史记录喵~ |
| 工作区（Working Directory） | 你电脑上的项目文件夹，正在编辑的文件喵~ |
| 暂存区（Staging Area） | `git add` 后的区域，准备提交的文件"购物车"喵~ |
| 提交（Commit） | 一次"存档"，记录当前所有暂存文件的状态喵~ |
| 远程（Remote） | 云端仓库，如 GitHub 上的仓库喵~ |
| 推送（Push） | 把本地提交上传到远程仓库喵~ |
| 拉取（Pull） | 从远程仓库下载最新代码喵~ |

工作流程：**修改文件 → git add（加入购物车）→ git commit（存档）→ git push（上传云端）** 喵~

---

## 本次项目的完整 Git 操作过程

### 第1步：初始化本地仓库

```bash
git init
```

这会在项目目录下创建一个隐藏的 `.git` 文件夹，用于存储所有版本信息喵~
执行后这个目录就变成了一个 Git 仓库喵~

### 第2步：配置用户信息

```bash
git config user.email "mu@example.com"
git config user.name "mu"
```

每个提交都会记录"谁提交的"，所以要先配置用户名和邮箱喵~
这些信息会出现在 GitHub 的提交记录中喵~

### 第3步：重命名默认分支

```bash
git branch -m main
```

新版本 Git 默认分支名叫 `master`，GitHub 推荐使用 `main` 喵~
`-m` 参数表示"重命名当前分支"喵~

### 第4步：创建 .gitignore 文件

`.gitignore` 文件告诉 Git **哪些文件不需要版本控制**喵~
比如：缓存文件、虚拟环境、IDE 配置、环境变量等喵~

```gitignore
# Python 缓存和编译文件
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
dist/
build/
.eggs/

# 虚拟环境（几百MB，用 requirements.txt 代替）
venv/
.venv/
env/

# IDE 配置文件
.idea/
.vscode/
*.swp
*.swo

# 环境变量（可能包含数据库密码等敏感信息）
.env
.env.local

# 操作系统文件
.DS_Store
Thumbs.db

# Claude Code 配置
.claude/
```

为什么要忽略这些？
- `__pycache__/` 是 Python 自动生成的缓存，不需要上传喵~
- `venv/` 太大（几百MB），用 `requirements.txt` 记录依赖即可喵~
- `.env` 可能包含数据库密码等敏感信息喵~
- `.claude/` 是 Claude Code 的本地配置，不需要分享喵~

### 第5步：暂存文件（git add）

```bash
git add .gitignore README.md CLAUDE.md examples/ toutiao_backend/
```

`git add` 把文件加入"暂存区"（相当于"加入购物车"）喵~
暂存区里的文件会在下次 commit 时被保存喵~

常用方式：
- `git add 文件名` —— 添加指定文件喵~
- `git add 目录名/` —— 添加整个目录喵~
- `git add .` —— 添加当前目录所有文件（谨慎使用）喵~

查看状态：
```bash
git status
```
会显示哪些文件已暂存（绿色）、哪些未暂存（红色）喵~

### 第6步：提交（git commit）

```bash
git commit -m "提交说明"
```

`git commit` 把暂存区的内容永久保存到 Git 历史中，就像游戏存档喵~
`-m` 后面跟的是"提交信息"，要写清楚这次做了什么喵~

提交信息规范：简短描述做了什么（中文英文都可以）喵~
```
初始化FastAPI学习项目：零基础示例+AI掘金头条实战
```

### 第7步：生成 SSH 密钥

GitHub 推送代码需要身份认证，SSH 密钥是最安全的方式喵~

```bash
ssh-keygen -t ed25519 -C "muhan-github" -f ~/.ssh/id_ed25519 -N ""
```

参数说明：
- `-t ed25519` —— 使用 Ed25519 加密算法（比 RSA 更安全更快）喵~
- `-C "注释"` —— 备注信息，方便在 GitHub 上识别喵~
- `-f ~/.ssh/id_ed25519` —— 密钥文件保存路径喵~
- `-N ""` —— 不设置密码（空密码）喵~

生成的密钥对：
- `~/.ssh/id_ed25519` —— 私钥（**绝对不能泄露！**）喵~
- `~/.ssh/id_ed25519.pub` —— 公钥（可以放心给别人）喵~

查看公钥内容：
```bash
cat ~/.ssh/id_ed25519.pub
```

### 第8步：添加公钥到 GitHub

1. 复制公钥内容喵~
2. 打开 https://github.com/settings/ssh/new
3. Title 填入备注名（如 `muhan-github`）喵~
4. Key 填入公钥内容喵~
5. 点击 "Add SSH key" 喵~

### 第9步：设置远程仓库地址

```bash
git remote add origin git@github.com:MUHAN11-c/fastapiDemo.git
```

`git remote add` 给本地仓库关联一个远程地址喵~
- `origin` —— 远程仓库的别名（约定俗成叫 origin）喵~
- `git@github.com:...` —— SSH 格式的 GitHub 仓库地址喵~

查看已关联的远程仓库：
```bash
git remote -v
```

### 第10步：添加 GitHub 主机密钥

第一次连接 GitHub 时，需要把 GitHub 的主机密钥加入信任列表喵~

```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

`ssh-keyscan` 获取 GitHub 的主机公钥，追加到 `~/.ssh/known_hosts` 文件中喵~
这样 SSH 才知道 `github.com` 是可信的服务器喵~

### 第11步：推送代码（git push）

```bash
git push -u origin main
```

`git push` 把本地提交上传到远程仓库喵~
- `-u` —— 设置上游跟踪（以后只需要 `git push` 就行）喵~
- `origin` —— 远程仓库名喵~
- `main` —— 要推送的分支名喵~

### 第12步：处理冲突（git pull --rebase）

当远程仓库已经有内容时（比如 GitHub 自动创建的 README.md），直接 push 会被拒绝喵~

```bash
# 先拉取远程代码并变基
git pull origin main --rebase
```

`git pull` 从远程拉取最新代码喵~
`--rebase` 参数表示"变基"：把本地提交"接"在远程提交之后，保持历史线性喵~

如果出现冲突（同一个文件两边都改了）：
1. Git 会在文件中标记冲突位置：
   ```
   <<<<<<< HEAD         # 远程的版本
   # fastapiDemo
   =======              # 分隔线
   # FastAPI 从入门到实战  # 你的版本
   >>>>>>> ec4efcb
   ```

2. 手动编辑文件，保留想要的内容，删除冲突标记喵~

3. 标记冲突已解决：
   ```bash
   git add README.md
   ```

4. 继续变基：
   ```bash
   GIT_EDITOR=true git rebase --continue
   ```
   `GIT_EDITOR=true` 跳过编辑提交信息的步骤，使用原来的提交信息喵~

5. 推送：
   ```bash
   git push -u origin main
   ```

---

## 常用 Git 命令速查表

| 命令 | 作用 |
|------|------|
| `git init` | 初始化新仓库喵~ |
| `git status` | 查看文件状态（改了哪些、暂存了哪些）喵~ |
| `git add 文件名` | 将文件加入暂存区喵~ |
| `git commit -m "信息"` | 提交暂存区的内容喵~ |
| `git log --oneline` | 查看提交历史喵~ |
| `git diff` | 查看具体改了什么喵~ |
| `git remote -v` | 查看远程仓库地址喵~ |
| `git push` | 推送到远程仓库喵~ |
| `git pull` | 从远程拉取最新代码喵~ |
| `git clone 地址` | 克隆远程仓库到本地喵~ |
| `git branch` | 查看分支列表喵~ |
| `git checkout -b 分支名` | 创建并切换到新分支喵~ |

## 工作流程图

```
工作区（改文件）
    │
    │ git add
    ↓
暂存区（准备提交）
    │
    │ git commit
    ↓
本地仓库（存档完成）
    │
    │ git push
    ↓
远程仓库（GitHub 云端）
    │
    │ git pull
    ↓
回到本地
```

## 注意事项

1. **永远不要把私钥（id_ed25519）发给任何人**喵~
2. **不要提交 .env、密码、API Key 等敏感信息**喵~
3. **每次 commit 前用 git status 检查一下**喵~
4. **提交信息写清楚改了啥**，方便以后回顾喵~
5. **拉取（pull）先于推送（push）**，避免冲突喵~
6. **遇到冲突不要慌**，看清楚两个版本的区别再合并喵~
