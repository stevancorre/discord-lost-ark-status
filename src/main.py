#!/usr/bin/python

from dotenv import load_dotenv
import discord

from datetime import datetime  # lol
import os

load_dotenv()
client: discord.Client = discord.Client()


@client.event
async def on_ready() -> None:
    log(f"Connected as {client.user}")


def log(message: object) -> None:
    time: str = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {message}")


client.run(os.getenv("TOKEN"))
