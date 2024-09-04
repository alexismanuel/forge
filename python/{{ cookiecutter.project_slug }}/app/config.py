import os

class AppConfig:
    env = os.environ.get('ENV', 'prd')
    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', '')
    db_url = os.environ.get('DB_URL')

