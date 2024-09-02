import os

class AppConfig:
    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', '')
