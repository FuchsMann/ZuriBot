from discord.ui import View, UserSelect, ChannelSelect, Button, button
from discord import Interaction, ButtonStyle, ChannelType
import sys
sys.path.append("..")
from data_manager import DataManager

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
        if len(self.userSelectHandle.values) != 0:
            subvals = (self.channelSelectHandle.values[0].id,
                [user.id for user in self.userSelectHandle.values] if len(self.userSelectHandle.values) != 0 else [])
            us = DataManager.loadUserSettings(interaction.user.id)
            us.addOrRemoveSubscriptionForChannel(subvals[0], subvals[1])
            DataManager.saveUserSettings(interaction.user.id, us)
            await interaction.response.send_message(f'Sub added.', ephemeral=True)
            self.value = True
            self.clear_items()
            self.stop()
        else:
            await interaction.response.send_message(f'You must select a channel.', ephemeral=True)
        
    @button(label='Cancel', style=ButtonStyle.red, row=2)
    async def cancel(self, interaction: Interaction, button: Button):
        await interaction.response.send_message('Aborted.', ephemeral=True)
        self.value = True
        self.clear_items()
        self.stop()
