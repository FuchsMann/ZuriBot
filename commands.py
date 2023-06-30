from datetime import datetime, timedelta
import pytz
from time import sleep
from typing import Optional
from discord import app_commands, Client, Interaction, User, File, VoiceChannel, Message, Member, TextChannel, Embed
import json
from io import BytesIO
from database.database import db
from image_manipulation.image_functions import ImageFunctions
from embeds.help import HelpEmbeds
from typing import Optional
from auth import Auth
import minestat
import psutil


class CommandManager:
    def __init__(self, client: Client):
        self.tree = app_commands.CommandTree(client)
        self.registerCommands()

    def registerCommands(self):

        # SLASH COMMANDS

        @self.tree.command(name="help", description="Shows a the help page")
        async def help(interaction: Interaction, section: Optional[str] = None):
            match (section):
                case "commands":
                    await interaction.response.send_message(embed=HelpEmbeds.slashHelp(), ephemeral=True)
                case None:
                    await interaction.response.send_message(embed=HelpEmbeds.basicHelp(), ephemeral=True)

        @self.tree.command(name="create_invite", description="Creates a single use invite")
        async def invite(interaction: Interaction):
            if interaction.channel is None or not isinstance(interaction.channel, TextChannel):
                await interaction.response.send_message("This command can only be used in a text channel", ephemeral=True)
                return

            it = db.fetchInviteTimer(interaction.user.id)
            if it is None or it.canCreateInvite():
                invite = await interaction.channel.create_invite(max_uses=1, max_age=0)
                embed = Embed(title="Invite created", description="This invite is valid for 1 use", color=0xfabf34)
                embed.add_field(name="Invite URL", value=invite.url)
                embed.set_footer(text="Only you can see this invite, copy it before it vanishes.")
                try:
                    guild = interaction.guild
                    if guild is not None:
                        for channel in Auth().invite_posting_channels:
                            if channel["guild_id"] == guild.id:
                                notifChan = guild.get_channel(channel["channel_id"])
                                if notifChan is not None and isinstance(notifChan, TextChannel):
                                    notifEmbed = Embed(title="Invite created", description=f"An invite was created by {interaction.user.mention} in {interaction.channel.mention}", color=0xfabf34)
                                    await notifChan.send(embed=notifEmbed)
                except Exception as e:
                    pass
                await interaction.response.send_message(embed=embed, ephemeral=True)
                db.insertIntoInviteTimer(
                    interaction.user.id, datetime.now(pytz.utc))
            else:
                nextInvite = it.timeToNextInvite()
                responseStr = f"You can create a new Invite in {nextInvite[0]} days, {nextInvite[1]} hours and {nextInvite[2]} minutes"
                await interaction.response.send_message(responseStr, ephemeral=True)
                return
            
        @self.tree.command(name="clear_invite_timer", description="Clears the invite timer for specified user. Admin command.")
        async def clear_invite_timer(interaction: Interaction, member_mention: Member):
            if not interaction.user.id in [328142516362805249, 840836189417111571, 1059937387574206514, 415311444897431557]:
                await interaction.response.send_message("You are not allowed to use this command", ephemeral=True)
                return
            memberName = member_mention.nick if member_mention.nick is not None else member_mention.name
            db.clearInviteTimer(member_mention.id)
            await interaction.response.send_message(f"Cleared invite timer for {member_mention.name}", ephemeral=True)

        @self.tree.command(name="print_messages", description="Shows all current custom messages for this guild")
        async def print_messages(interaction: Interaction):
            if interaction.guild_id is None:
                await interaction.response.send_message("This command can only be used in a server", ephemeral=True)
                return
            outBytes = BytesIO()
            gms = db.fetchCustomMessagesForGuild(interaction.guild_id)
            if gms is None or gms == []:
                await interaction.response.send_message("No custom messages for this guild", ephemeral=True)
                return
            outDictList = [gm.toDict() for gm in gms]
            outBytes.write(json.dumps(outDictList, indent=2).encode(
                'UTF-8'))  # type: ignore
            outBytes.seek(0)
            file = File(fp=outBytes, filename="messages.json")
            await interaction.response.send_message(file=file, ephemeral=True)

        @self.tree.command(name="join_message", description="A custom message for Zuri to say for a certain member")
        async def join_message(interaction: Interaction, user_mention: User, custom_message: str):
            if '@' in custom_message:
                await interaction.response.send_message(f'Custom message cannot contain mentions')
                return
            db.insertIntoCustomMessage(
                user_mention.id, interaction.guild_id, custom_message)  # type: ignore
            await interaction.response.send_message(f'Message "{custom_message}" was added for {user_mention.name}', ephemeral=True)

        @self.tree.command(name="remove_message", description="Remove a users custom message from Zuri's memory")
        async def remove_message(interaction: Interaction, user_mention: User):
            db.removeCustomMessage(
                user_mention.id, interaction.guild_id)  # type: ignore
            await interaction.response.send_message(f'Message for {user_mention.name} was removed', ephemeral=True)

        @self.tree.command(name="watch_channel", description="Adds/removes a channel from Zuri's watchlist")
        async def watch_channel(interaction: Interaction, voice_channel: VoiceChannel):
            action: str = db.toggleWatchedChannel(
                interaction.guild_id, voice_channel.id, voice_channel.name)  # type: ignore
            await interaction.response.send_message(f'Channel {voice_channel.name} was {action} to the watchlist', ephemeral=True)

        @self.tree.command(name="print_channels", description="Show Zuri's channel watchlist")
        async def print_channels(interaction: Interaction):
            if interaction.guild_id is None:
                await interaction.response.send_message("This command can only be used in a server", ephemeral=True)
                return
            gcn = db.fetchWatchedChannelsForGuild(interaction.guild_id)
            if gcn is None or gcn == []:
                await interaction.response.send_message("No watched channels for this guild", ephemeral=True)
                return
            outBytes = BytesIO()
            outDictList = [gm.toDict() for gm in gcn]
            outBytes.write(json.dumps(outDictList, indent=2).encode(
                'UTF-8'))  # type: ignore
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

                            messageCollector: list[Message] = []

                            for channel in guild.text_channels:
                                try:
                                    messageCollector.extend([message async for message in channel.history(limit=None, after=referenceDate - timedelta(days=60), oldest_first=False)])
                                except:
                                    pass

                            memberIDs: list[int] = [
                                member.id for member in guild.members]
                            memberLatestMessage: dict[int, datetime] = {}
                            for message in messageCollector:
                                if not message.author is None and message.author.id in memberIDs:
                                    if not message.author.id in memberLatestMessage.keys():
                                        memberLatestMessage[message.author.id] = message.created_at
                                    else:
                                        if message.created_at > memberLatestMessage[message.author.id]:
                                            memberLatestMessage[message.author.id] = message.created_at

                            memberLatestMessageAssigned: dict[str, str] = {}
                            for memberID in memberIDs:
                                member = await guild.fetch_member(memberID)
                                if not member is None:
                                    if not memberID in memberLatestMessage.keys():
                                        memberLatestMessageAssigned[member.name] = '60+ days'
                                    else:
                                        memberLatestMessageAssigned[
                                            member.name] = f'{(referenceDate - memberLatestMessage[memberID]).days} days'

                            sortedMembers = dict(
                                sorted(memberLatestMessageAssigned.items(), key=lambda x: x[1], reverse=True))

                            outStr = json.dumps(
                                sortedMembers, indent=2)
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
                
        @self.tree.command(name="mcstatus", description="shows current status of the MC server")
        async def mcstatus(interaction: Interaction):
            try:
                embed = Embed(title="Minecraft Server Status", description="Data is currently being fetched.", color=0xfabf34)
                await interaction.response.send_message(embed=embed)

                ms = minestat.MineStat(Auth().mcserver_address.split(':')[0], int(Auth().mcserver_address.split(':')[1]))
                embed = Embed(title="Minecraft Server Status", description=f"The server has {len(ms.player_list or [])} player(s) online", color=0xfabf34)
                embed.add_field(name="Version", value=ms.version or "Unknown")
                embed.add_field(name="Latency", value=f"{round(ms.latency or 0)} ms")
                playersList = ms.player_list or []
                if playersList:
                    players = ''
                    for player in playersList:
                        if player == 'paulohare':
                            players += f"Daukus\n"
                        else:
                            players += f"{player}\n"
                    embed.add_field(name="Players", value=players, inline=False)
                message = await interaction.original_response()
                await message.edit(embed=embed)
            except:
                if interaction.response.is_done():
                    message = await interaction.followup.send("Server could not be queried")
                else:
                    await interaction.response.send_message("Server could not be queried")

        @self.tree.command(name="hoststatus", description="shows host server stats")
        async def hoststatus(interaction: Interaction):
            try:
                cpu = psutil.cpu_percent()
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                embed = Embed(title="Host Server Status", color=0xfabf34)
                embed.add_field(name="Node", value=f"Ocelot 2")
                embed.add_field(name="CPU", value=f"cores: {psutil.cpu_count()}\nusage: {cpu}%")
                embed.add_field(name="", value=f"", inline=False)
                embed.add_field(name="Memory", value=f"{mem.percent}%\nused: {round(mem.used / 1024 / 1024 / 1024, 2)}GB\nfree: {round(mem.free / 1024 / 1024 / 1024, 2)}GB\ntotal: {round(mem.total / 1024 / 1024 / 1024, 2)}GB")
                embed.add_field(name="Disk", value=f"{disk.percent}%")
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("Something went wrong")

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
