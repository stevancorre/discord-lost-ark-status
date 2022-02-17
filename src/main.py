#!/usr/bin/python

from client import Client
from helper import try_getenv

TOKEN: str = try_getenv("TOKEN", str)
PREFIX: str = try_getenv("PREFIX", str)

client: Client = Client(command_prefix=PREFIX)
client.load_extension("modules.status")
client.run(TOKEN)
