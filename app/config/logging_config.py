import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    # 确保日志目录存在
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建日志记录器
    loggers = {}
    
    # 数据库日志
    db_logger = logging.getLogger('database')
    db_logger.setLevel(logging.INFO)
    
    # 防止日志重复
    if not db_logger.handlers:
        # 创建文件处理器
        log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        db_logger.addHandler(file_handler)
        db_logger.addHandler(console_handler)

        # 设置不传播到父记录器
        db_logger.propagate = False
    
    loggers['database'] = db_logger
    
    return loggers 