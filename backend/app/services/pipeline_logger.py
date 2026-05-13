import logging
import sys
import time
from pythonjsonlogger import jsonlogger

def setup_pipeline_logger(name="pipeline_engine"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logHandler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(levelname)s %(name)s %(stage)s %(message)s %(duration)s %(status)s',
            timestamp=True
        )
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
    
    return logger

pipeline_logger = setup_pipeline_logger()

class PipelineTimer:
    def __init__(self, stage_name):
        self.stage_name = stage_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        pipeline_logger.info(f"Starting stage: {self.stage_name}", extra={"stage": self.stage_name, "status": "START"})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        status = "SUCCESS" if exc_type is None else "FAILURE"
        pipeline_logger.info(f"Finished stage: {self.stage_name}", extra={
            "stage": self.stage_name, 
            "duration": f"{duration:.2f}s",
            "status": status
        })
