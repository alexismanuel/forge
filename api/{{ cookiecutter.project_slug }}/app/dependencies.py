from app.utils.logger import get_logger
from app.config import AppConfig

logger = get_logger(
    '{{ cookiecutter.project_slug }}',
    json_format=AppConfig.log_json_format,
    log_format=AppConfig.log_format,
)

