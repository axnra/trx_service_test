from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", backtrace=True, diagnose=True)

logger.add("logs/app.log", rotation="1 MB", retention="10 days", level="INFO")

__all__ = ["logger"]
