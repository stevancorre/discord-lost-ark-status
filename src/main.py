#!/usr/bin/python

from datetime import datetime
from nextcord.ext.commands.bot import Bot, Context
from nextcord.ext.commands.errors import CommandNotFound
from helper import try_getenv


TOKEN: str = try_getenv("TOKEN", str)
PREFIX: str = try_getenv("PREFIX", str)

client: Bot = Bot(command_prefix=PREFIX)


@client.event
async def on_ready() -> None:
    log(f"Connected as {client.user}")


@client.event
async def on_command_error(_: Context, error):
    if isinstance(error, CommandNotFound):
        return

    raise error


def log(message: object) -> None:
    time: str = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {message}")


def load_extension(extension: str):
    try:
        client.load_extension(extension + ".cog")
        log(f"Successfully loaded `{extension}`")
    except:
        log(f"ERROR: Error loading `{extension}`")


load_extension("modules.status")
client.run(TOKEN)
