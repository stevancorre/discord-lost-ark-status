from typing import List

from nextcord.ext.commands import Bot, Cog, Context, command

from scrapper import ScrapperResult, get_servers_statuses

from modules.status.view import RegionsDropdownView
from modules.status.embeds import ServerStatusEmbed


class Status(Cog, name="Status"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="status")
    async def executeAsync(self, context: Context):
        data: ScrapperResult = get_servers_statuses()
        view = RegionsDropdownView(data)

        await context.reply(embed=ServerStatusEmbed(data.regions[0], data.last_updated), view=view)


def setup(bot: Bot):
    bot.add_cog(Status(bot))
