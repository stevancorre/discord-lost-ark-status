from datetime import datetime
from typing import Optional, Dict, Any
from nextcord.ext.commands.bot import Bot, Context
from nextcord.ext.commands.errors import CommandError, CommandNotFound


class Client(Bot):
    """Describes the bot client"""

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=command_prefix)

    async def on_ready(self) -> None:
        self.log(f"Connected as {self.user}")

    # Called if the client has an error with a command
    # Here, we filter CommandNotFounds to avoid spamming the stderr
    async def on_command_error(self, _: Context, exception: CommandError) -> None:
        if isinstance(exception, CommandNotFound):
            return

        raise exception

    def log(self, message: object) -> None:
        """Prints a message to stdout with the current time"""

        time: str = datetime.now().strftime("%H:%M:%S")
        print(f"[{time}] {message}")

    def load_extension(self, name: str, *, package: Optional[str] = None, extras: Optional[Dict[str, Any]] = None) -> None:
        """Loads a module"""

        try:
            super().load_extension(name=name + ".cog", package=package, extras=extras)
            self.log(f"Successfully loaded `{name}`")
        except Exception as exception:
            self.log(f"ERROR: Error loading `{name}`")
            raise exception
