from discord.ui import View, UserSelect, ChannelSelect, Button, button
from discord import Interaction, ButtonStyle

class SubscriptionView(View):
    
    channelSelect = ChannelSelect(placeholder='Select a channel', min_values=1, max_values=1, row=0)
    
    userSelect = UserSelect(placeholder='Select a user', min_values=0, max_values=25, row=1)
    
    @button(label='Confirm', style=ButtonStyle.green, row=2)
    async def confirm(self, interaction: Interaction, button: Button):
        await interaction.response.send_message('Confirmed.', ephemeral=True)
        self.value = True
        self.stop()
        
    @button(label='Cancel', style=ButtonStyle.red, row=2)
    async def confirm(self, interaction: Interaction, button: Button):
        await interaction.response.send_message('Aborted.', ephemeral=True)
        self.value = True
        self.stop()
