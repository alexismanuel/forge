from app.config import AppConfig
import structlog
from structlog.dev import set_exc_info, ConsoleRenderer
from structlog.processors import StackInfoRenderer, TimeStamper, add_log_level


base_processors = [
    add_log_level,
    StackInfoRenderer(),
    set_exc_info,
    TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=True)
]
def dev_log_config() -> None:
    structlog.configure_once(
        processors=[
            *base_processors,
            ConsoleRenderer(),
        ]
    )

def prd_log_config():
    structlog.configure_once(
        processors=[
            *base_processors,
            structlog.processors.JSONRenderer(),
        ]
    )



def config_structlog():
    return dev_log_config if AppConfig.env == 'dev' else prd_log_config()

