from typing import Optional, Dict, Any

from nextcord.ext.commands.bot import Bot, Context
from nextcord.ext.commands.errors import CommandError, CommandNotFound

from provider import DataProvider
from helper import log

class Client(Bot):
    """Describes the bot client"""

    def __init__(self, command_prefix: str, cache_lifetime: int, db_name: str):
        super().__init__(command_prefix=command_prefix)

        self.provider = DataProvider(
            db_name=db_name, cache_lifetime=cache_lifetime)

    async def on_ready(self) -> None:
        log(f"Connected as {self.user}")

    # Called if the client has an error with a command
    # Here, we filter CommandNotFounds to avoid spamming the stderr
    async def on_command_error(self, _: Context, exception: CommandError) -> None:
        if isinstance(exception, CommandNotFound):
            return

        raise exception

    def load_extension(self, name: str, *, package: Optional[str] = None, extras: Optional[Dict[str, Any]] = None) -> None:
        """Loads a module"""

        try:
            super().load_extension(name=name + ".cog", package=package, extras=extras)
            log(f"Successfully loaded `{name}`")
        except Exception as exception:
            log(f"ERROR: Error loading `{name}`")
            raise exception
