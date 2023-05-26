from datetime import datetime, timedelta
import pytz
from time import sleep
from typing import Optional
from discord import app_commands, Client, Interaction, User, File, VoiceChannel, Message, Member
import json
from io import BytesIO
from data_manager import DataManager
from image_manipulation.image_functions import ImageFunctions


class CommandManager:
    def __init__(self, client: Client):
        self.tree = app_commands.CommandTree(client)
        self.registerCommands()

    def registerCommands(self):

        # SLASH COMMANDS

        @self.tree.command(name="print_messages", description="Shows all current custom messages for this guild")
        async def print_messages(interaction: Interaction):
            outBytes = BytesIO()
            outBytes.write(json.dumps(DataManager.loadGuildCustomMessages(
                interaction.guild_id).toDict(), indent=2).encode('UTF-8'))  # type: ignore
            outBytes.seek(0)
            file = File(fp=outBytes, filename="messages.json")
            await interaction.response.send_message(file=file, ephemeral=True)

        @self.tree.command(name="join_message", description="A custom message for Zuri to say for a certain member")
        async def join_message(interaction: Interaction, user_mention: User, custom_message: str):
            if '@' in custom_message:
                await interaction.response.send_message(f'Custom message cannot contain mentions')
                return
            DataManager.addGuildCustomMessage(
                interaction.guild_id, user_mention.id, custom_message)  # type: ignore
            await interaction.response.send_message(f'Message "{custom_message}" was added for {user_mention.name}', ephemeral=True)

        @self.tree.command(name="remove_message", description="Remove a users custom message from Zuri's memory")
        async def remove_message(interaction: Interaction, user_mention: User):
            DataManager.removeGuildCustomMessage(
                interaction.guild_id, user_mention.id)  # type: ignore
            await interaction.response.send_message(f'Message for {user_mention.name} was removed', ephemeral=True)

        @self.tree.command(name="watch_channel", description="Adds/removes a channel from Zuri's watchlist")
        async def watch_channel(interaction: Interaction, voice_channel: VoiceChannel):
            action: str = DataManager.toggleWatchedChannel(
                interaction.guild_id, voice_channel.id, voice_channel.name)  # type: ignore
            await interaction.response.send_message(f'Channel {voice_channel.name} was {action} to the watchlist', ephemeral=True)

        @self.tree.command(name="print_channels", description="Show Zuri's channel watchlist")
        async def print_channels(interaction: Interaction):
            outBytes = BytesIO()
            outBytes.write(json.dumps(DataManager.loadWatchedChannels(
                interaction.guild_id).toDict(), indent=2).encode('UTF-8'))  # type: ignore
            outBytes.seek(0)
            file = File(fp=outBytes, filename="channels.json")
            await interaction.response.send_message(file=file, ephemeral=True)

        @self.tree.command(name="subscribe", description="Adds/removes a channel from your notifications, optional argument for specific artists")
        async def subscribe(interaction: Interaction, voice_channel: VoiceChannel, artist: Optional[Member] = None):
            await interaction.response.send_message(f'Stubbed command; arg feedback: {voice_channel}, {artist}')

        @self.tree.command(name="print_subscribed_channels", description="Shows all subscribed channels for your account.")
        async def print_subs(interaction: Interaction):
            await interaction.response.send_message('Stubbed command')

        @self.tree.command(name="list_inactives", description="Admin command")
        async def list_inactives(interaction: Interaction) -> None:
            if interaction.guild is None or interaction.channel is None:
                await interaction.response.send_message('This command can only be used in a server')
                return

            if not interaction.user is None:
                member = await interaction.guild.fetch_member(interaction.user.id)
                if member.id in [1059937387574206514, 328142516362805249] or interaction.channel.permissions_for(member).administrator:
                    messages: list[Message] = []
                    afterDate: datetime = datetime.now() - timedelta(days=60)
                    for channel in interaction.guild.text_channels:
                        try:
                            async for message in channel.history(limit=None, after=afterDate):
                                messages.append(message)
                        except:
                            pass

                    referenceDate: datetime = datetime.now(
                        pytz.timezone('Europe/Berlin'))
                    lastMessages: dict[Member, Message] = {}
                    for member in interaction.guild.members:
                        lastMessages[member] = None
                    for message in messages:
                        if not message.author in lastMessages.keys():
                            continue
                        if lastMessages[message.author] is None or message.created_at > lastMessages[message.author].created_at:
                            lastMessages[message.author] = message

                    outString: str = 'User - Days since last message\n'
                    sortedMessages = sorted(lastMessages.items(), key=lambda x: (
                        referenceDate - x[1].created_at).days)
                    sortedMessages.reverse()
                    lastMessages = dict(sortedMessages)

                    for member in lastMessages:
                        if lastMessages[member] is None:
                            outString += f'{member.name} - 60+\n'
                        else:
                            outString += f'{member.name} - {(referenceDate - lastMessages[member].created_at).days}\n'
                    await interaction.response.send_message(outString)
                    return

                else:
                    await interaction.response.send_message('You do not have permission to use this command')
                    return

        # CONTEXT MENU STUFF

        @self.tree.context_menu(name="Soy")
        async def soy(interaction: Interaction, message: Message):
            if len(message.attachments) != 0:
                for attachment in message.attachments:
                    if 'image' in attachment.content_type:  # type: ignore
                        outfile = ImageFunctions.soy(attachment.url)
                        if outfile is not None:
                            await interaction.response.send_message(file=outfile)
                return
            await interaction.response.send_message('No images detected')

        @self.tree.context_menu(name="Soyphone")
        async def soyphone(interaction: Interaction, message: Message):
            if len(message.attachments) != 0:
                for attachment in message.attachments:
                    if 'image' in attachment.content_type:  # type: ignore
                        outfile = ImageFunctions.soyphone(attachment.url)
                        if outfile is not None:
                            await interaction.response.send_message(file=outfile)
                return
            await interaction.response.send_message('No images detected')

        @self.tree.context_menu(name="PepperDream")
        async def pepperdream(interaction: Interaction, message: Message):
            if len(message.attachments) != 0:
                for attachment in message.attachments:
                    if 'image' in attachment.content_type:  # type: ignore
                        outfile = ImageFunctions.pepperdream(attachment.url)
                        if outfile is not None:
                            await interaction.response.send_message(file=outfile)
                return
            await interaction.response.send_message('No images detected')

        @self.tree.context_menu(name="TV")
        async def tv(interaction: Interaction, message: Message):
            if len(message.attachments) != 0:
                for attachment in message.attachments:
                    if 'image' in attachment.content_type:  # type: ignore
                        outfile = ImageFunctions.tv(attachment.url)
                        if outfile is not None:
                            await interaction.response.send_message(file=outfile)
                return
            await interaction.response.send_message('No images detected')
