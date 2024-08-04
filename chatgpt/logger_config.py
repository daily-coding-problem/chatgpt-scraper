import logging
import os

# Get the log level from the environment variable, default to "INFO"
log_level_str = os.getenv("LOG_LEVEL", "INFO")

# Map the string to the corresponding logging level constant
log_level = getattr(logging, log_level_str.upper(), logging.INFO)

# Configure logging
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
