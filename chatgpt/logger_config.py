import logging
import os

log_level = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
