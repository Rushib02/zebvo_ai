import logging
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from datetime import datetime

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter to include timestamps and uppercase levels."""
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

def setup_logger(name, log_file, level=logging.INFO):
    """Initializes a logger with JSON formatting and rotating file handler."""
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = CustomJsonFormatter('%(timestamp)s %(levelname)s %(name)s %(message)s')

    # 10MB per file, keep 5 backups
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if logger is already initialized
    if not logger.handlers:
        logger.addHandler(handler)
        
        # Console handler for development
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
        logger.addHandler(console_handler)

    return logger

# Define base logs directory (root of the workspace)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Standardized Loggers
error_logger = setup_logger('error_logger', os.path.join(LOG_DIR, 'errors.log'), logging.ERROR)
request_logger = setup_logger('request_logger', os.path.join(LOG_DIR, 'requests.log'), logging.INFO)
ai_logger = setup_logger('ai_logger', os.path.join(LOG_DIR, 'ai.log'), logging.INFO)

def log_error(message, extra=None):
    error_logger.error(message, extra=extra)

def log_request(message, extra=None):
    request_logger.info(message, extra=extra)

def log_ai_event(message, extra=None):
    ai_logger.info(message, extra=extra)
