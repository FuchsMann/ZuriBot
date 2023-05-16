from discord import app_commands, Client, Object, Interaction, User, File, VoiceChannel, Message
import json
from io import BytesIO
from data_manager import DataManager


class CommandManager:
    def __init__(self, client: Client):
        self.tree = app_commands.CommandTree(client)
        self.registerCommands()

    def registerCommands(self):

        @self.tree.command(name="print_messages", description="Shows all current custom messages for this guild")
        async def print_messages(interaction: Interaction):
            outBytes = BytesIO()
            outBytes.write(json.dumps(DataManager.loadGuildCustomMessages(
                interaction.guild_id).toDict(), indent=2).encode('UTF-8'))
            outBytes.seek(0)
            file = File(fp=outBytes, filename="messages.json")
            await interaction.response.send_message(file=file)

        @self.tree.command(name="join_message", description="A custom message for Zuri to say for a certain member")
        async def join_message(interaction: Interaction, user_mention: User, custom_message: str):
            if '@' in custom_message:
                await interaction.response.send_message(f'Custom message cannot contain mentions')
                return
            DataManager.addGuildCustomMessage(
                interaction.guild_id, user_mention.id, custom_message)
            await interaction.response.send_message(f'Message "{custom_message}" was added for {user_mention.name}')

        @self.tree.command(name="remove_message", description="Remove a users custom message from Zuri's memory")
        async def remove_message(interaction: Interaction, user_mention: User):
            DataManager.removeGuildCustomMessage(
                interaction.guild_id, user_mention.id)
            await interaction.response.send_message(f'Message for {user_mention.name} was removed')

        @self.tree.command(name="watch_channel", description="Adds/removes a channel from Zuri's watchlist")
        async def watch_channel(interaction: Interaction, voice_channel: VoiceChannel):
            action: str = DataManager.toggleWatchedChannel(
                interaction.guild_id, voice_channel.id, voice_channel.name)
            await interaction.response.send_message(f'Channel {voice_channel.name} was {action} to the watchlist')

        @self.tree.command(name="print_channels", description="Show Zuri's channel watchlist")
        async def print_channels(interaction: Interaction):
            outBytes = BytesIO()
            outBytes.write(json.dumps(DataManager.loadWatchedChannels(
                interaction.guild_id).toDict(), indent=2).encode('UTF-8'))
            outBytes.seek(0)
            file = File(fp=outBytes, filename="channels.json")
            await interaction.response.send_message(file=file)
            
        @self.tree.context_menu(name="Context m. tst")
        async def ctx_menu_tst(interaction: Interaction, message: Message):
            await interaction.response.send_message(f'ctx. men. test - loopback: {message.content}')
