from discord.ui import View, UserSelect, ChannelSelect, Button, button
from discord import Interaction, ButtonStyle, ChannelType

class SubscriptionView(View):
    def __init__(self):
        super().__init__()
        self.value = False
        
        self.channelSelectHandle = ChannelSelect(placeholder='Select a channel', min_values=0, max_values=1, row=0, channel_types=[ChannelType.voice])
        self.userSelectHandle = UserSelect(placeholder='Select a user', min_values=0, max_values=25, row=1)
        
        for item in [self.channelSelectHandle, self.userSelectHandle]:
            item.callback = self.selectDefer
            self.add_item(item)
    
    async def selectDefer(self, interaction: Interaction):
        await interaction.response.defer()
    
    @button(label='Confirm', style=ButtonStyle.green, row=2)
    async def confirm(self, interaction: Interaction, button: Button):
        await interaction.response.send_message(f'{[user.name for user in self.userSelectHandle.values]}; {self.channelSelectHandle.values[0].name}', ephemeral=True)
        self.value = True
        self.stop()
        
    @button(label='Cancel', style=ButtonStyle.red, row=2)
    async def cancel(self, interaction: Interaction, button: Button):
        await interaction.response.send_message('Aborted.', ephemeral=True)
        self.value = True
        self.stop()
