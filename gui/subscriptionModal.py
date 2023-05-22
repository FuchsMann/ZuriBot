from discord.ui import Modal, UserSelect
from discord import Interaction

class SubscriptionModal(Modal, title='Subscriptions'):
    userSelect = UserSelect(placeholder='Select a user', min_values=0, max_values=25)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
