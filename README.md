# FastAPI MySQL 项目

## 安装说明

1. Python版本管理
   - 推荐使用pyenv管理Python版本
   - 项目开发时使用Python 3.12.7
   - 使用pyenv安装并切换Python版本：
     ```bash
     pyenv install 3.12.7
     pyenv global 3.12.7
     ```

2. 安装pipenv
   ```bash
   python -m pip install pipenv
   ```

3. 安装项目依赖
   ```bash
   pipenv install
   ```

4. 配置数据库
   - 复制 `.env.example` 为 `.env`
   - 更新 `.env` 中的数据库配置信息

5. 运行项目
   ```bash
   pipenv run uvicorn main:app --reload
   ```

## 项目结构

```
lapi/
├── config/              # 配置文件目录
│   ├── database.py     # 数据库配置
│   └── logging_config.py# 日志配置
├── database/           # 数据库相关代码
│   └── connection.py   # 数据库连接管理
├── models/             # SQLAlchemy 模型
│   └── user.py        # 用户模型定义
├── routers/            # API 路由
│   └── users.py       # 用户相关接口
├── schemas/            # Pydantic 模型
│   └── user.py        # 用户数据验证模型
├── logs/              # 日志文件目录（自动创建）
│   └── app_*.log      # 日志文件
├── main.py            # 应用入口
├── Pipfile            # 项目依赖管理
├── .env               # 环境变量配置
├── .env.example       # 环境变量示例
└── .gitignore         # Git忽略配置
```

### 主要组件说明

1. `config/`
   - 存放配置相关文件
   - `database.py` 管理数据库连接配置
   - `logging_config.py` 配置日志系统

2. `database/`
   - 数据库连接和会话管理
   - `connection.py` 提供数据库连接和会话

3. `models/`
   - SQLAlchemy ORM 模型定义
   - `user.py` 定义用户表结构

4. `routers/`
   - API 路由和处理函数
   - `users.py` 实现用户相关的 CRUD 接口

5. `schemas/`
   - Pydantic 数据验证模型
   - `user.py` 定义请求和响应的数据结构

6. `logs/`
   - 存放应用日志文件
   - 自动创建每日日志文件
   - 自动轮转（最多保留5个文件）

## API 接口

- API 文档：http://localhost:8000/docs
- 可用接口：
  - `GET /api/users/` - 获取用户列表
  - `POST /api/users/` - 创建新用户
  - `GET /api/users/{user_id}` - 获取指定用户

## 环境变量

在 `.env` 文件中配置以下环境变量：
- `DB_HOST`: 数据库主机地址
- `DB_PORT`: 数据库端口
- `DB_USER`: 数据库用户名
- `DB_PASSWORD`: 数据库密码
- `DB_NAME`: 数据库名称

## 日志系统

- 日志位置：`logs/app_YYYYMMDD.log`
- 日志级别：INFO 及以上
- 日志格式：时间 - 模块 - 级别 - 消息
- 日志分类：
  - 数据库日志
  - API日志
  - 系统日志
