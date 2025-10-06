import logging
from enum import Enum
# Cross-cutting concern: logging configuration

class LogLevels(Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL

def configure_logging(level: LogLevels = LogLevels.info):
    logging.basicConfig(
        level=level.value,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )