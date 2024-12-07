from fastapi import FastAPI, HTTPException
from database.connection import engine, Base
from routers import users
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from config.logging_config import setup_logging

# 获取API专用日志记录器
loggers = setup_logging()
logger = loggers['api']

app = FastAPI(
    title="FastAPI MySQL Demo",
    description="使用 FastAPI 和 MySQL 的示例项目",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    try:
        # 测试数据库连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("应用启动：数据库连接正常")
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except OperationalError as e:
        logger.error(f"应用启动失败：数据库连接错误 - {str(e)}")
        # 我们允许应用继续启动，但数据库相关功能可能不可用

# Include routers
app.include_router(users.router, prefix="/api")

@app.get("/")
def read_root():
    logger.info("访问首页")
    return {
        "message": "Welcome to FastAPI with MySQL!",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

@app.get("/health")
async def health_check():
    try:
        # 验证数据库连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status = {"status": "healthy", "database": "connected"}
        logger.info("健康检查：系统正常")
        return status
    except Exception as e:
        error_status = {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
        logger.error(f"健康检查：系统异常 - {str(e)}")
        return error_status 