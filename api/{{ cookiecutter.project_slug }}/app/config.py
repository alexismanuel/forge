import os


class AppConfig:
    app_port = int(os.getenv('APP_PORT', '8080'))
    log_format = '%(asctime)s [%(levelname)s][%(name)s][%(cart_id)s] %(message)s'
    log_json_format = int(os.getenv('LOG_JSON_FORMAT', '0'))
    log_level = os.getenv('LOG_LEVEL', 'info')
