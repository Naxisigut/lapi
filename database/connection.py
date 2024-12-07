from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from config.database import db_settings
from config.logging_config import setup_logging
from fastapi import HTTPException

# 获取数据库专用日志记录器
loggers = setup_logging()
logger = loggers['database']

try:
    engine = create_engine(db_settings.DATABASE_URL)
    # 测试数据库连接
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("数据库连接成功")
except OperationalError as e:
    logger.error(f"数据库连接失败: {str(e)}")
    # 这里我们仍然创建 engine，但不立即连接
    engine = create_engine(db_settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # 尝试验证数据库连接
        db.execute(text("SELECT 1"))
        yield db
    except OperationalError as e:
        logger.error(f"数据库会话创建失败: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="数据库服务不可用，请稍后重试"
        )
    finally:
        db.close() 