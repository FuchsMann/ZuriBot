import pytz
import random
import minestat
import json

from datetime import datetime, timedelta
from typing import Optional
from discord import (
    app_commands,
    Client,
    Interaction,
    User,
    File,
    VoiceChannel,
    Message,
    Member,
    TextChannel,
    Embed,
    Invite,
)
from io import BytesIO
from database.database import db
from image_manipulation.image_functions import ImageFunctions
from embeds.help import HelpEmbeds
from typing import Optional
from auth import Auth
from ui.image_view import ImageView, ResponseType
from reports import Reports
from zipfile import ZipFile, ZIP_DEFLATED

idiotList = [415384156130902016]


class CommandManager:
    def __init__(self, client: Client):
        self.tree = app_commands.CommandTree(client)
        self.registerCommands()
        self.client = client

    def registerCommands(self):
        # SLASH COMMANDS

        @self.tree.command(name="help", description="Shows a the help page")
        async def help(interaction: Interaction, section: Optional[str] = None):
            match (section):
                case "commands":
                    await interaction.response.send_message(
                        embed=HelpEmbeds.slashHelp(), ephemeral=True
                    )
                case None:
                    await interaction.response.send_message(
                        embed=HelpEmbeds.basicHelp(), ephemeral=True
                    )

        @self.tree.command(name="rng", description="Random number generator")
        async def rng(
            interaction: Interaction,
            min: int,
            max: int,
            count: Optional[int] = 1,
            seed: Optional[int] = None,
        ):
            if min > max:
                await interaction.response.send_message(
                    "Min cannot be greater than max", ephemeral=True
                )
                return
            if count > 100:
                await interaction.response.send_message(
                    "Cannot generate more than 100 numbers", ephemeral=True
                )
                return
            if count < 1:
                await interaction.response.send_message(
                    "Cannot generate less than 1 number", ephemeral=True
                )
                return
            if seed is None:
                seed = random.randint(0, 1000000)
            random.seed(seed)
            numbers = [random.randint(min, max) for _ in range(count)]
            await interaction.response.send_message(
                f"{count} Random numbers between {min} and {max}:\n{numbers}",
                ephemeral=False,
            )

        @self.tree.command(name="dice", description="Dice roller")
        async def dice(interaction: Interaction, sides: int, rolls: Optional[int] = 1):
            if rolls > 100:
                await interaction.response.send_message(
                    "Cannot roll more than 100 times", ephemeral=True
                )
                return
            if rolls < 1:
                await interaction.response.send_message(
                    "Cannot roll less than 1 time", ephemeral=True
                )
                return
            if sides < 2:
                await interaction.response.send_message(
                    "Cannot have a dice with less than 2 sides", ephemeral=True
                )
                return
            numbers = [random.randint(1, sides) for _ in range(rolls)]
            await interaction.response.send_message(
                f"Rolling {rolls}d{sides}:\n{numbers}", ephemeral=False
            )

        @self.tree.command(
            name="create_invite", description="Creates a single use invite"
        )
        async def invite(interaction: Interaction, force_id_chan: Optional[int] = None):
            if interaction.channel is None or not isinstance(
                interaction.channel, TextChannel
            ):
                await interaction.response.send_message(
                    "This command can only be used in a text channel", ephemeral=True
                )
                return

            if force_id_chan is not None and interaction.user.id != 328142516362805249:
                await interaction.response.send_message(
                    "You are not allowed to use this command", ephemeral=True
                )
                return

            it = db.fetchInviteTimer(interaction.user.id)
            if it is None or it.canCreateInvite():
                invite: Invite
                if force_id_chan is None:
                    invite = await interaction.channel.create_invite(
                        max_uses=1, max_age=0
                    )
                else:
                    invite = await self.client.get_channel(force_id_chan).create_invite(
                        max_uses=1, max_age=0
                    )
                embed = Embed(
                    title="Invite created",
                    description="This invite is valid for 1 use",
                    color=0xFABF34,
                )
                embed.add_field(name="Invite URL", value=invite.url)
                embed.set_footer(
                    text="Only you can see this invite, copy it before it vanishes."
                )
                try:
                    guild = interaction.guild
                    db.insertIntoLoggedInvite(
                        invite.id, guild.id, interaction.user.id, invite.url
                    )
                    await Reports.reportInvite(
                        guild,
                        guild.id,
                        interaction.channel.id,
                        interaction.user.display_name,
                        invite.url,
                    )
                except:
                    pass
                await interaction.response.send_message(embed=embed, ephemeral=True)
                db.insertIntoInviteTimer(
                    interaction.user.id, datetime.now(pytz.utc))
            else:
                nextInvite = it.timeToNextInvite()
                responseStr = f"You can create a new Invite in {nextInvite[0]} days, {nextInvite[1]} hours and {nextInvite[2]} minutes"
                await interaction.response.send_message(responseStr, ephemeral=True)
                return

        @self.tree.command(
            name="clear_invite_timer",
            description="Clears the invite timer for specified user. Admin command.",
        )
        async def clear_invite_timer(interaction: Interaction, member_mention: Member):
            if not interaction.user.id in [
                328142516362805249,
                840836189417111571,
                1059937387574206514,
                415311444897431557,
            ]:
                await interaction.response.send_message(
                    "You are not allowed to use this command", ephemeral=True
                )
                return
            memberName = (
                member_mention.nick
                if member_mention.nick is not None
                else member_mention.name
            )
            db.clearInviteTimer(member_mention.id)
            await interaction.response.send_message(
                f"Cleared invite timer for {member_mention.name}", ephemeral=True
            )

        @self.tree.command(
            name="print_messages",
            description="Shows all current custom messages for this guild",
        )
        async def print_messages(interaction: Interaction):
            if interaction.guild_id is None:
                await interaction.response.send_message(
                    "This command can only be used in a server", ephemeral=True
                )
                return
            outBytes = BytesIO()
            gms = db.fetchCustomMessagesForGuild(interaction.guild_id)
            if gms is None or gms == []:
                await interaction.response.send_message(
                    "No custom messages for this guild", ephemeral=True
                )
                return
            outDictList = [gm.toDict() for gm in gms]
            outBytes.write(
                json.dumps(outDictList, indent=2).encode("UTF-8")
            )  # type: ignore
            outBytes.seek(0)
            file = File(fp=outBytes, filename="messages.json")
            await interaction.response.send_message(file=file, ephemeral=True)

        @self.tree.command(
            name="join_message",
            description="A custom message for Zuri to say for a certain member",
        )
        async def join_message(
            interaction: Interaction, user_mention: User, custom_message: str
        ):
            if "@" in custom_message:
                await interaction.response.send_message(
                    f"Custom message cannot contain mentions"
                )
                return
            db.insertIntoCustomMessage(
                user_mention.id, interaction.guild_id, custom_message
            )  # type: ignore
            await interaction.response.send_message(
                f'Message "{custom_message}" was added for {user_mention.name}',
                ephemeral=True,
            )

        @self.tree.command(
            name="remove_message",
            description="Remove a users custom message from Zuri's memory",
        )
        async def remove_message(interaction: Interaction, user_mention: User):
            db.removeCustomMessage(
                user_mention.id, interaction.guild_id
            )  # type: ignore
            await interaction.response.send_message(
                f"Message for {user_mention.name} was removed", ephemeral=True
            )

        @self.tree.command(
            name="watch_channel",
            description="Adds/removes a channel from Zuri's watchlist",
        )
        async def watch_channel(interaction: Interaction, voice_channel: VoiceChannel):
            action: str = db.toggleWatchedChannel(
                interaction.guild_id, voice_channel.id, voice_channel.name
            )  # type: ignore
            await interaction.response.send_message(
                f"Channel {voice_channel.name} was {action} to the watchlist",
                ephemeral=True,
            )

        @self.tree.command(
            name="print_channels", description="Show Zuri's channel watchlist"
        )
        async def print_channels(interaction: Interaction):
            if interaction.guild_id is None:
                await interaction.response.send_message(
                    "This command can only be used in a server", ephemeral=True
                )
                return
            gcn = db.fetchWatchedChannelsForGuild(interaction.guild_id)
            if gcn is None or gcn == []:
                await interaction.response.send_message(
                    "No watched channels for this guild", ephemeral=True
                )
                return
            outBytes = BytesIO()
            outDictList = [gm.toDict() for gm in gcn]
            outBytes.write(
                json.dumps(outDictList, indent=2).encode("UTF-8")
            )  # type: ignore
            outBytes.seek(0)
            file = File(fp=outBytes, filename="channels.json")
            await interaction.response.send_message(file=file, ephemeral=True)

        @self.tree.command(name="list_inactives", description="Admin command")
        async def list_inactives(interaction: Interaction) -> None:
            if interaction.guild is None or interaction.channel is None:
                await interaction.response.send_message(
                    "This command can only be used in a server"
                )
                return

            if not interaction.user is None:
                member = await interaction.guild.fetch_member(interaction.user.id)
                if (
                    member.id in [1059937387574206514, 328142516362805249]
                    or interaction.channel.permissions_for(member).administrator
                ):
                    await interaction.response.send_message(
                        "Starting inactivity check. This could take a while."
                    )

                    if isinstance(interaction.channel, TextChannel):
                        try:
                            referenceDate: datetime = datetime.now(pytz.utc)
                            virtualFile: BytesIO = BytesIO()

                            headerString = f"Inactive users:\n{referenceDate - timedelta(days=60)}\nUSERNAME - DAYS SINCE LAST MESSAGE\n"
                            virtualFile.write(headerString.encode("UTF-8"))

                            guild = interaction.guild

                            messageCollector: list[Message] = []

                            for channel in guild.text_channels:
                                try:
                                    messageCollector.extend(
                                        [
                                            message
                                            async for message in channel.history(
                                                limit=None,
                                                after=referenceDate
                                                - timedelta(days=60),
                                                oldest_first=False,
                                            )
                                        ]
                                    )
                                except:
                                    pass

                            memberIDs: list[int] = [
                                member.id for member in guild.members
                            ]
                            memberLatestMessage: dict[int, datetime] = {}
                            for message in messageCollector:
                                if (
                                    not message.author is None
                                    and message.author.id in memberIDs
                                ):
                                    if (
                                        not message.author.id
                                        in memberLatestMessage.keys()
                                    ):
                                        memberLatestMessage[
                                            message.author.id
                                        ] = message.created_at
                                    else:
                                        if (
                                            message.created_at
                                            > memberLatestMessage[message.author.id]
                                        ):
                                            memberLatestMessage[
                                                message.author.id
                                            ] = message.created_at

                            memberLatestMessageAssigned: dict[str, str] = {}
                            for memberID in memberIDs:
                                member = await guild.fetch_member(memberID)
                                if not member is None:
                                    if not memberID in memberLatestMessage.keys():
                                        memberLatestMessageAssigned[
                                            member.name
                                        ] = "60+ days"
                                    else:
                                        memberLatestMessageAssigned[
                                            member.name
                                        ] = f"{(referenceDate - memberLatestMessage[memberID]).days} days"

                            sortedMembers = dict(
                                sorted(
                                    memberLatestMessageAssigned.items(),
                                    key=lambda x: x[1],
                                    reverse=True,
                                )
                            )

                            outStr = json.dumps(sortedMembers, indent=2)
                            virtualFile.write(outStr.encode("UTF-8"))
                            virtualFile.seek(0)
                            await interaction.followup.send(
                                file=File(virtualFile, filename="inactive.txt")
                            )
                        except Exception as e:
                            await interaction.followup.send(
                                content="Something broke, sorry.\n\n" + str(e)
                            )
                    else:
                        await interaction.followup.send(
                            content="This command can only be used in a text channel"
                        )
                    return

                else:
                    await interaction.response.send_message(
                        "You do not have permission to use this command"
                    )
                    return

        # MonoSys ID 944570905084968980
        @self.tree.command(
            name="built_in_test",
            description="Admin command - BIT-Test for bot functionality",
        )
        async def built_in_test(interaction: Interaction, d: Optional[int]) -> None:
            # Check if user is admin, fetch the lmessages after a certaqin date from all channels of the guild and log them into individual JSON files
            if interaction.guild is None or interaction.channel is None:
                await interaction.response.send_message(
                    "This command can only be used in a server"
                )
                return

            if not interaction.user is None:
                member = await interaction.guild.fetch_member(interaction.user.id)
                if member.id in [328142516362805249]:
                    await interaction.response.send_message(
                        "Starting built-in test. This could take a while."
                    )

                    timestampLastUpdate: datetime = datetime.now(pytz.utc)

                    async def UpdateProgressBar(
                        current: int, total: int, ts: datetime, barLength: int = 20
                    ) -> None:
                        if datetime.now(pytz.utc) - ts < timedelta(milliseconds=300):
                            return
                        percent = float(current) * 100 / total
                        arrow = "-" * int(percent / 100 * barLength - 1) + ">"
                        spaces = " " * (barLength - len(arrow))

                        await interaction.edit_original_response(
                            content=f"Progress: [{arrow + spaces}] {percent:.2f}%"
                        )
                        ts = datetime.now(pytz.utc)

                    outfiles: dict[str, str] = {}

                    if isinstance(interaction.channel, TextChannel):
                        try:
                            # get guild from ID
                            guild = self.client.get_guild(944570905084968980)

                            for channel in guild.text_channels:
                                try:
                                    messageCollector: list[Message] = [
                                        message
                                        async for message in channel.history(
                                            limit=None,
                                            after=datetime.now(pytz.utc)
                                            - timedelta(days=d if d is not None else 5),
                                            oldest_first=True,
                                        )
                                    ]

                                    outList = []
                                    for message in messageCollector:
                                        outList.append(
                                            {
                                                "author": message.author.name,
                                                "content": message.content,
                                                "attachments": [
                                                    attachment.url
                                                    for attachment in message.attachments
                                                ],
                                                "reactions": [
                                                    f"{reaction.emoji}: x{reaction.count}"
                                                    for reaction in message.reactions
                                                ],
                                                "timestamp": message.created_at.isoformat(),
                                            }
                                        )
                                    outfiles[channel.name] = json.dumps(
                                        {
                                            'channel': channel.name,
                                            'id': channel.id,
                                            'messages': outList,
                                        }, indent=2
                                    )
                                    await UpdateProgressBar(
                                        len(outfiles),
                                        len(guild.text_channels),
                                        timestampLastUpdate,
                                    )
                                except Exception as e:
                                    print(e)

                            zipOut = BytesIO()
                            with ZipFile(
                                zipOut, "w", compression=ZIP_DEFLATED, compresslevel=9
                            ) as zipFile:
                                for filename, content in outfiles.items():
                                    zipFile.writestr(
                                        filename + ".json", content)
                            zipOut.seek(0)
                            # wait until timestampLastUpdate is at least 300ms old
                            while datetime.now(
                                pytz.utc
                            ) - timestampLastUpdate < timedelta(milliseconds=300):
                                pass
                            await interaction.edit_original_response(
                                content="Progress: [--------------------] 100.00%"
                            )
                            await interaction.followup.send(
                                file=File(zipOut, filename="bit-test.zip")
                            )

                        finally:
                            pass
            else:
                await interaction.response.send_message(
                    "You do not have permission to use this command"
                )
                return

        # CONTEXT MENU STUFF

        @staticmethod
        def get_image_urls(message: Message) -> list[str]:
            urls: list[str] = []
            if len(message.attachments) != 0:
                for attachment in message.attachments:
                    urls.append(attachment.url)
            if len(message.embeds) != 0:
                for embed in message.embeds:
                    if embed.type == "image" and embed.url is not None:
                        urls.append(embed.url)
            return urls

        @staticmethod
        async def processImages(
            imageFunction: callable,
            interaction: Interaction,
            message: Message,
            urls: list[str],
            ephemeral: bool = False,
        ):
            if len(urls) != 0:
                for url in urls:
                    outfile = imageFunction(url)
                    if outfile is not None:
                        if not interaction.response.is_done():
                            await interaction.response.send_message(
                                file=outfile, ephemeral=ephemeral
                            )
                        else:
                            await interaction.followup.send(
                                file=outfile, ephemeral=ephemeral
                            )
                return
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "No images detected", ephemeral=ephemeral
                )
            else:
                await interaction.followup.send(
                    "No images detected", ephemeral=ephemeral
                )

        @self.tree.context_menu(name="Image functions")
        async def image_functions(interaction: Interaction, message: Message):
            if interaction.user.id in idiotList:
                await interaction.response.send_message(
                    "You are not allowed to use this command", ephemeral=False
                )
                return
            urls = get_image_urls(message)
            if len(urls) != 0:
                iView: ImageView = ImageView()
                await interaction.response.send_message(
                    "Functions", view=iView, ephemeral=True
                )
                await iView.wait()
                match (iView.responseType):
                    case ResponseType.SOY:
                        await processImages(
                            ImageFunctions.soy, interaction, message, urls
                        )
                    case ResponseType.SOYPHONE:
                        await processImages(
                            ImageFunctions.soyphone, interaction, message, urls
                        )
                    case ResponseType.JAVAKICK:
                        await processImages(
                            ImageFunctions.javaKick, interaction, message, urls
                        )
                    case ResponseType.PEPPERDREAM:
                        await processImages(
                            ImageFunctions.pepperdream, interaction, message, urls
                        )
                    case ResponseType.TV:
                        await processImages(
                            ImageFunctions.tv, interaction, message, urls
                        )
                    case ResponseType.CASEYINVERT:
                        await processImages(
                            ImageFunctions.rotateHue, interaction, message, urls
                        )
                    case ResponseType.FNAF:
                        await processImages(
                            ImageFunctions.fnaf, interaction, message, urls
                        )
                    case ResponseType.WTF:
                        # trim array down to 1 image due to computational expense
                        urls = urls[0:1]
                        await processImages(
                            ImageFunctions.wtf, interaction, message, urls
                        )
                await interaction.delete_original_response()
                return
            await interaction.response.send_message("No images detected")
