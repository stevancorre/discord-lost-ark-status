from nextcord import Message, Interaction, SelectOption
from nextcord.ui import View, Select
from nextcord.errors import NotFound

from modules.status.embeds import ServerStatusEmbed

from scrapper import ScrapperResult


class RegionsDropdownView(View):
    def __init__(self, data: ScrapperResult):
        super().__init__(timeout=30)
        self.add_item(RegionsDropdown(data))

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True

        try:
            if self.message:
                await self.message.edit(view=self)
        except NotFound:
            pass 


class RegionsDropdown(Select):
    def __init__(self, data: ScrapperResult):
        self.data = data
        options = [SelectOption(label=region.name, value=str(i))
                   for i, region in enumerate(data.regions)]
        options[0].default = True

        super().__init__(
            min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        index: int = int(self.values[0])
        message: Message | None = interaction.message
        if message is None:
            return

        await message.edit(embed=ServerStatusEmbed(self.data.regions[index], self.data.last_updated))
