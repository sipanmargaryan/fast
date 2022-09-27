import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter_args = "%(timestamp)s %(level)s %(message)s"
formatter = CustomJsonFormatter(formatter_args)

logger = logging.getLogger()


logHandler = logging.StreamHandler()

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(level="INFO")
