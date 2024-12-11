from fastapi import FastAPI
from app.api.endpoints import items
from app.config.database import engine, Base
import logging

app = FastAPI(
    title="LAPI",
    description="这是一个FastAPI项目示例",
    version="1.0.0"
)

# 尝试创建数据库表，但不阻止应用启动
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logging.error(f"数据库表创建失败: {str(e)}")
    logging.warning("应用将在没有数据库连接的情况下启动")

# 包含路由
app.include_router(items.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "欢迎使用LAPI!"} 