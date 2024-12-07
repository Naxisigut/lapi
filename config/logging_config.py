import logging
import logging.handlers
import os
from datetime import datetime

# 创建logs目录（如果不存在）
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# 日志文件路径
LOG_FILE = os.path.join(LOGS_DIR, f'app_{datetime.now().strftime("%Y%m%d")}.log')

def setup_logging():
    # 创建日志格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 文件处理器 - 记录所有日志
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 控制台处理器 - 记录INFO及以上级别的日志
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 创建数据库专用日志记录器
    db_logger = logging.getLogger('database')
    db_logger.setLevel(logging.INFO)
    
    # 创建API专用日志记录器
    api_logger = logging.getLogger('api')
    api_logger.setLevel(logging.INFO)

    return {
        'root': root_logger,
        'database': db_logger,
        'api': api_logger
    } 