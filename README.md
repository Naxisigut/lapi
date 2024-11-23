# 项目名称

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

4. 激活虚拟环境
   ```bash
   pipenv shell
   ```

5. 运行项目
   ```bash
   uvicorn app.main:app --reload
   ```

## 项目结构
```
myproject/
├── app/                    # 主应用目录
│   ├── __init__.py        # 使app成为一个Python包
│   ├── main.py            # 应用的入口点，包含FastAPI实例和根路由
│   │
│   ├── api/               # API相关代码目录
│   │   ├── __init__.py
│   │   └── endpoints/     # API端点目录
│   │       ├── __init__.py
│   │       └── items.py   # items相关的路由和处理函数
│   │
│   ├── core/              # 核心配置目录
│   │   ├── __init__.py
│   │   └── config.py      # 应用配置文件，包含全局设置
│   │
│   └── models/            # 数据模型目录
│       ├── __init__.py
│       └── item.py        # Item模型定义
│
├── Pipfile                # Pipenv依赖管理文件
├── Pipfile.lock          # Pipenv依赖版本锁定文件
└── README.md             # 项目说明文档
```

### 主要组件说明：

1. `app/main.py`
   - FastAPI应用的主入口
   - 创建FastAPI实例
   - 注册路由和中间件
   - 配置基本的API信息（标题、描述等）

2. `app/api/endpoints/`
   - 包含所有API端点的具体实现
   - `items.py` 定义了与items相关的所有路由和处理函数
   - 可以根据功能模块添加更多endpoint文件

3. `app/core/`
   - 存放核心配置和工具
   - `config.py` 使用pydantic_settings管理应用配置

4. `app/models/`
   - 定义数据模型
   - 使用Pydantic模型进行数据验证
   - `item.py` 定义了Item的数据结构
