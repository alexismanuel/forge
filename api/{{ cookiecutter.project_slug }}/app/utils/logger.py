import logging
import sys
from typing import Any, Optional, Mapping
from pythonjsonlogger import jsonlogger

import datetime
import pytz


class LoggerWrongLogLevel(Exception):
    pass


class BaseCustomFormatter:
    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        return datetime.fromisoformat(record.created).replace(tzinfo=pytz.UTC).isoformat()


class CustomFormatter(BaseCustomFormatter, logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.levelname = record.levelname.lower()
        return super().format(record)


class CustomJSONFormatter(BaseCustomFormatter, jsonlogger.JsonFormatter):
    def format(self, record: logging.LogRecord) -> str:
        record.levelname = record.levelname.lower()
        return super().format(record)


class MergingLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        kwargs["extra"] = (self.extra or {}) | kwargs.get("extra", {})
        return msg, kwargs


def get_logger(
        name: str,
        log_level: Optional[str] = None,
        log_format: Optional[str] = None,
        json_format: Optional[bool] = False,
        extra: Mapping[str, Any] = None
    ) -> logging.LoggerAdapter:
    log_format = log_format or '%(asctime)s [%(levelname)s][%(name)s] %(message)s'
    extra = extra or {}
    formatter_class = CustomFormatter if not json_format else CustomJSONFormatter
    formatter = formatter_class(log_format)

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
    logger.setLevel(getattr(logging, log_level.upper()))

    logger_with_extra = MergingLoggerAdapter(logger, extra)

    return logger_with_extra
