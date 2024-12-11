# LAPI

## 项目结构

```
project_root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       └── items.py
│   └── config/
│       ├── __init__.py
│       └── database.py
├── docs/
│   └── deploy/
│       ├── README.md
│       └── build_in_server.md
├── tests/
│   └── __init__.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── Pipfile
├── Pipfile.lock
└── README.md
```

## 目录说明

- `app/`: 应用主目录
  - `main.py`: 应用入口文件
  - `api/`: API 相关代码
    - `endpoints/`: API 端点定义
  - `config/`: 配置文件
- `docs/`: 项目文档
- `tests/`: 测试文件
- `.env`: 环境变量（不提交到git）
- `.env.example`: 环境变量示例
- `Dockerfile`: Docker 配置文件
- `Pipfile` & `Pipfile.lock`: 依赖管理
