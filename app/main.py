from fastapi import FastAPI
from app.api.endpoints import items

app = FastAPI(
    title="MyAPI",
    description="这是一个FastAPI项目示例",
    version="1.0.0"
)

# 包含路由
app.include_router(items.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "欢迎使用FastAPI!"} 