from typing import List

from nextcord import Interaction, SelectOption
from nextcord.ui import View, Select
from modules.status.embeds import ServerStatusEmbed

from scrapper import ScrapperResult


class RegionsDropdownView(View):
    def __init__(self, data: ScrapperResult):
        super().__init__(timeout=60)

        # Adds the dropdown to our view object.
        self.add_item(RegionsDropdown(data))

    async def interaction_check(self, interaction: Interaction) -> bool:
        return await super().interaction_check(interaction)


class RegionsDropdown(Select):
    def __init__(self, data: ScrapperResult):
        self.data = data
        options = [SelectOption(label=region.name, value=i)
                   for i, region in enumerate(data.regions)]
        options[0].default = True

        super().__init__(
            min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        index: int = int(self.values[0])
        await interaction.message.edit(embed=ServerStatusEmbed(self.data.regions[index], self.data.last_updated))
