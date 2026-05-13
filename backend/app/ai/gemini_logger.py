import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_gemini_logger(name="gemini_engine"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:
        logHandler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(levelname)s %(name)s %(message)s %(request_id)s %(model)s',
            timestamp=True
        )
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
    
    return logger

# Global logger instance
gemini_logger = setup_gemini_logger()
