#!/usr/bin/python

from client import Client
from helper import try_getenv

TOKEN: str = try_getenv("TOKEN", str)
PREFIX: str = try_getenv("PREFIX", str)
CACHE_LIFETIME: int = try_getenv("CACHE_LIFETIME", int)
DB_NAME: str = try_getenv("DB_NAME", str)

client: Client = Client(command_prefix=PREFIX, cache_lifetime=CACHE_LIFETIME, db_name=DB_NAME)
client.load_extension("modules.status")
client.run(TOKEN)