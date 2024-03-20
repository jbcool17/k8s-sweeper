import logging
import os
import sys

logging.basicConfig(
    stream=sys.stdout, format="%(asctime)s: %(levelname)s - %(message)s", level=os.getenv("LOG_LEVEL", "INFO")
)
