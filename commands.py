from datetime import datetime, timedelta
import pytz
from time import sleep
from typing import Optional
from discord import app_commands, Client, Interaction, User, File, VoiceChannel, Message, Member, TextChannel
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
                    await interaction.response.send_message('Starting inactivity check. This could take a while.')

                    if isinstance(interaction.channel, TextChannel):
                        try:
                            referenceDate: datetime = datetime.now(
                                pytz.utc)
                            virtualFile: BytesIO = BytesIO()

                            headerString = f'Inactive users:\n{referenceDate - timedelta(days=60)}\nUSERNAME - DAYS SINCE LAST MESSAGE\n'
                            virtualFile.write(headerString.encode('UTF-8'))

                            guild = interaction.guild

                            meassageCollector: list[Message] = []

                            for channel in guild.text_channels:
                                try:
                                    meassageCollector.extend([message async for message in channel.history(limit=None, after=referenceDate - timedelta(days=60), oldest_first=False)])
                                except:
                                    pass

                            memberIDs: list[int] = [
                                member.id for member in guild.members]
                            memberLatestMessage: dict[int, datetime] = {}
                            for message in meassageCollector:
                                if not message.author is None and message.author.id in memberIDs:
                                    if not message.author.id in memberLatestMessage.keys():
                                        memberLatestMessage[message.author.id] = message.created_at
                                    else:
                                        if message.created_at > memberLatestMessage[message.author.id]:
                                            memberLatestMessage[message.author.id] = message.created_at

                            # sort by date, oldest first

                            memberLatestMessage = dict(sorted(
                                memberLatestMessage.items(), key=lambda item: item[1]))

                            memberLatestMessageAssigned: dict[str, str] = {}
                            for memberID in memberLatestMessage.keys():
                                member = await guild.fetch_member(memberID)
                                if not member is None:
                                    if memberLatestMessage[memberID] is None:
                                        memberLatestMessageAssigned[member.name] = '60+ days'
                                    memberLatestMessageAssigned[
                                        member.name] = f'{(referenceDate - memberLatestMessage[memberID]).days} days'
                                else:
                                    memberLatestMessageAssigned[str(
                                        memberID)] = f'{(referenceDate - memberLatestMessage[memberID]).days} days'

                            outStr = json.dumps(
                                memberLatestMessageAssigned, indent=2)
                            virtualFile.write(outStr.encode('UTF-8'))
                            virtualFile.seek(0)
                            await interaction.followup.send(file=File(virtualFile, filename='inactive.txt'))
                        except Exception as e:
                            await interaction.followup.send(content='Something broke, sorry.\n\n' + str(e))
                    else:
                        await interaction.followup.send(content='This command can only be used in a text channel')
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
