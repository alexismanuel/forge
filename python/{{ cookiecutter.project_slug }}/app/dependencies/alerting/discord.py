import logging

from discordwebhook import Discord
from result import Err, Ok, Result

from .client import AlertingClient

logger = logging.getLogger()


class DiscordClient(AlertingClient):
    def __init__(self, url: str) -> None:
        super().__init__()
        self._client = Discord(url=url)

    def post(self, msg: str) -> Result[str, str]:
        try:
            self._client.post(content=msg)
        except Exception as err:
            err_msg = str(err)
            logger.exception(err_msg)
            return Err(err_msg)
        return Ok('post success')

