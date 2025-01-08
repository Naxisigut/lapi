# 开发笔记

本文档记录项目开发过程中的问题和解决方案。

## 2024-03-XX

### 问题与解决方案记录

1. 问题：项目中的 `__init__.py` 文件看不到
   
   解释：
   - `__init__.py` 是Python包的标识文件
   - 作用：将一个目录标记为Python包，使其可以被导入
   - 在项目中的位置：
     ```
     app/
     ├── __init__.py
     ├── api/
     │   ├── __init__.py
     │   └── endpoints/
     │       └── __init__.py
     ├── core/
     │   └── __init__.py
     └── models/
         └── __init__.py
     ```
   - 如果看不到这些文件，可能是因为：
     1. 操作系统默认隐藏了以 `__` 开头的文件
     2. 编辑器设置隐藏了这类文件
   
   解决方案：
   1. 创建这些空文件：
      ```bash
      touch app/__init__.py
      touch app/api/__init__.py
      touch app/api/endpoints/__init__.py
      touch app/core/__init__.py
      touch app/models/__init__.py
      ```
   2. 检查编辑器设置，确保显示所有文件

2. 问题：如何查看已安装的依赖包的源代码？

   解决方案：
   1. 查看依赖包安装位置：
      ```bash
      # 在虚拟环境中执行
      pipenv --venv
      ```
      这会显示虚拟环境的路径，依赖包通常安装在 `lib/python3.x/site-packages/` 目录下

   2. 直接在Python中查看包的位置：
      ```python
      # 在Python解释器中执行
      import fastapi
      print(fastapi.__file__)  # 这会显示fastapi包的位置
      ```

   3. 在线查看源代码：
      - FastAPI: https://github.com/tiangolo/fastapi
      - Pydantic: https://github.com/pydantic/pydantic
      - Uvicorn: https://github.com/encode/uvicorn

   4. 使用IDE功能：
      - 在VSCode中，按住Ctrl（Windows）或Cmd（Mac）点击导入的包名
      - 这会直接跳转到包的源代码

   建议：
   - 优先查看官方文档了解API用法
   - 需要深入理解实现时再查看源代码
   - GitHub上的源代码通常有更好的可读性和完整的历史记录

3. 问题：VSCode中提示"无法解析导入fastapi (Pylance reportMissingImports)"

   原因：
   - VSCode无法找到虚拟环境中安装的包
   - Python解释器可能没有正确设置
   
   解决方案：
   1. 确保已激活虚拟环境：
      ```bash
      pipenv shell
      ```

   2. 在VSCode中选择正确的Python解释器：
      - 按 `Ctrl+Shift+P`（Windows）或 `Cmd+Shift+P`（Mac）
      - 输入 "Python: Select Interpreter"
      - 选择以 `(.venv)`或`pipenv` 结尾的解释器路径
      
   3. 如果看不到虚拟环境的解释器，可以手动添加路径：
      ```bash
      # 获取虚拟环境路径
      pipenv --venv
      ```
      然后将输出的路径添加到VSCode的Python解释器列表中

   4. 安装类型提示包：
      ```bash
      pipenv install --dev pylance
      ```

   注意事项：
   - 每次打开新的VSCode窗口可能都需要重新选择解释器
   - 确保项目根目录下有 `.vscode/settings.json` 文件，可以保存解释器设置

### 开发讨论

1. 讨论主题：Python包结构
   - Python使用 `__init__.py` 来组织代码结构
   - 这种结构允许我们使用点号来导入模块，例如：`from app.models.item import Item`
   - 即使 `__init__.py` 是空文件，也需要创建它们以确保包结构正确

2. 讨论主题：IDE配置最佳实践
   - 使用虚拟环境可以避免全局包冲突
   - VSCode的Python插件提供了良好的开发体验
   - 正确配置解释器可以获得代码补全和类型提示



## 2025-01-09
### FastAPI 请求处理

#### 1. 接收请求头（Headers）

```python
@router.get("/hello")
async def hello(
    test: str = Header(),              # 接收必需的请求头
    user_agent: str = Header(),        # 可以接收多个请求头
    custom_header: str = Header(default=None)  # 可选的请求头
):
    return {
        "test_header": test,
        "user_agent": user_agent,
        "custom": custom_header
    }
```

对应的前端请求：
```javascript
fetch('/api/v1/hello', {
    headers: {
        'test': 'get',
        'user-agent': 'Mozilla/5.0',
        'custom-header': 'value'
    }
})
```

#### 2. 接收请求体（Body）

```python
from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str
    age: int | None = None  # 可选字段

@router.post("/users")
async def create_user(user: UserRequest):  # 直接接收请求体
    return {
        "username": user.username,
        "age": user.age
    }
```

对应的前端请求：
```javascript
fetch('/api/v1/users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'john',
        password: '123456',
        age: 25
    })
})
```

#### 3. 同时接收请求头和请求体

```python
@router.post("/hello")
async def hello_post(
    request: HelloRequest,           # 请求体
    token: str = Header(),          # 必需的请求头
    trace_id: str = Header(default=None)  # 可选的请求头
):
    return {
        "body": request.dict(),
        "token": token,
        "trace_id": trace_id
    }
```

对应的前端请求：
```javascript
fetch('/api/v1/hello', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'token': 'xxx',
        'trace-id': '123'
    },
    body: JSON.stringify({
        test: 'post'
    })
})
```

#### 特点说明

1. FastAPI 自动处理：
   - 请求参数验证
   - 数据类型转换
   - API 文档生成
   - 类型提示

2. Pydantic 模型：
   - 用于定义请求体的结构
   - 提供数据验证
   - 类似 TypeScript 的接口定义

3. Header 参数：
   - 可设置默认值
   - 可设置是否必需
   - 自动处理大小写转换

4. 错误处理：
   - 自动生成错误响应
   - 参数验证失败时返回 422 状态码
   - 可自定义错误处理 