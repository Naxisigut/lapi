from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException
import os
from app.config.logging_config import setup_logging

# 获取数据库专用日志记录器
loggers = setup_logging()
if not loggers:
    raise RuntimeError("Failed to initialize loggers")
logger = loggers.get('database')
if not logger:
    raise RuntimeError("Database logger not found")

# 记录环境变量加载情况
logger.info("正在初始化数据库连接...")
logger.info(f"环境变量: DB_HOST={os.getenv('DB_HOST', 'Not set')}")
logger.info(f"环境变量: DB_PORT={os.getenv('DB_PORT', 'Not set')}")
logger.info(f"环境变量: DB_NAME={os.getenv('DB_NAME', 'Not set')}")

# 构建数据库 URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # 测试数据库连接
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("数据库连接成功")
except OperationalError as e:
    error_msg = f"数据库连接失败: {str(e)}"
    logger.error(error_msg)
    # 这里我们仍然创建 engine，但不立即连接
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # 尝试验证数据库连接
        db.execute(text("SELECT 1"))
        logger.debug("数据库会话创建成功")
        yield db
    except OperationalError as e:
        error_msg = f"数据库会话创建失败: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=503,
            detail="数据库服务不可用，请稍后重试"
        )
    finally:
        logger.debug("关闭数据库会话")
        db.close() 