import ditto as di
from .alerting.discord import DiscordClient
from app.config import AppConfig

discord_client = DiscordClient(AppConfig.discord_webhook_url)
di.register(discord_client)
