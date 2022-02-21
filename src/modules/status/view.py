from nextcord import Message, Interaction, SelectOption
from nextcord.ui import View, Select
from nextcord.errors import NotFound

from modules.status.embeds import ServerStatusEmbed

from scrapper import ScrapperResult


class RegionsDropdownView(View):
    """Describes a view used to display a dropdown with all regions"""

    def __init__(self, data: ScrapperResult):
        super().__init__(timeout=30)
        self.add_item(RegionsDropdown(data))

    async def on_timeout(self) -> None:
        # (Generic) disable any button or select then edit the message
        for child in self.children:
            child.disabled = True

        try:
            if self.message:
                await self.message.edit(view=self)
        # In case the user deletes the message for some reason
        except NotFound:
            pass


class RegionsDropdown(Select):
    """Describes a dropdown used to select a server region"""

    def __init__(self, data: ScrapperResult):
        self.data = data

        # Create an option with each region, then set the first one as default
        options = [SelectOption(label=region.name, value=str(i))
                   for i, region in enumerate(data.regions)]
        options[0].default = True

        super().__init__(
            min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        # Edit the message with the selected data set
        index: int = int(self.values[0])
        message: Message | None = interaction.message
        if message is None:
            return

        await message.edit(embed=ServerStatusEmbed(self.data.regions[index], self.data.last_updated), view=self.view)
