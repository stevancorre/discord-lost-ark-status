from nextcord.ext.commands import Cog, command
from nextcord.ext.commands.bot import Bot, Context

from scrapper import ScrapperResult, get_servers_statuses
from helper import get_ttl_hash, try_getenv

from modules.status.view import RegionsDropdownView
from modules.status.embeds import ServerStatusEmbed


class Status(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="status")
    async def executeAsync(self, context: Context):
        ttl: int = get_ttl_hash(try_getenv("CACHE_LIFETIME", float))
        data: ScrapperResult = get_servers_statuses(ttl)
        view = RegionsDropdownView(data)

        await context.reply(embed=ServerStatusEmbed(data.regions[0], data.last_updated), view=view)


def setup(bot: Bot):
    bot.add_cog(Status(bot))
