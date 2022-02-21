from nextcord.ext.commands import Cog, command
from client import Client

from scrapper import ScrapperResult, scrap_servers_statuses
from helper import get_ttl_hash, try_getenv
from nextcord.ext.commands.bot import Bot, Context

from modules.status.view import RegionsDropdownView
from modules.status.embeds import ServerStatusEmbed


class Status(Cog):
    """Contains status commands"""

    def __init__(self, client: Client):
        self.client = client

    @command(name="status")
    async def executeAsync(self, context: Context) -> None:
        data: ScrapperResult = self.client.provider.get_servers_statuses()
        view = RegionsDropdownView(data)
        view.message = await context.reply(embed=ServerStatusEmbed(data.regions[0], data.last_updated), view=view)


def setup(client: Client):
    client.add_cog(Status(client))
