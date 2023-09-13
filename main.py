import discord
from discord import VoiceState, Member, Invite, Embed
from auth import Auth
from intent_builder import IntentBuilder
from commands import CommandManager
from database.database import db
from reports import Reports
from global_states import invitesStore, InviteInternal
from data_classes.logged_invite import LoggedInvite


class ZuriBot(discord.Client):
    def __init__(self):
        self.authData = Auth()
        super().__init__(intents=IntentBuilder.getIntents())
        self.commandManager = CommandManager(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="You. Meow~"
        )

    def run(self) -> None:
        super().run(self.authData.token)

    async def readInviteStore(self) -> None:
        invitesStore.invites = []
        for guild in self.guilds:
            invites = await guild.invites()
            for invite in invites:
                invitesStore.invites.append(InviteInternal.fromInvite(invite))

    async def on_ready(self) -> None:
        await self.commandManager.tree.sync()
        print(f"Logged on as {self.user}!")

        await self.readInviteStore()

    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ) -> None:
        watchedChannels = db.fetchWatchedChannelsForGuild(member.guild.id)
        if watchedChannels is None:
            return

        memberName = member.nick if member.nick is not None else member.name

        def channelIsWatched(channelID: int) -> bool:
            # type: ignore
            return channelID in [channel.channel_id for channel in watchedChannels]

        if before.channel is None and after.channel is not None:
            if channelIsWatched(after.channel.id):
                customMessage = db.fetchCustomMessage(
                    member.id, member.guild.id)
                if customMessage is not None:
                    await after.channel.send(
                        customMessage.message + f"\n({memberName} joined)"
                    )
                else:
                    await after.channel.send(
                        f"Hello **{memberName}**! Welcome to {after.channel.name}!"
                    )

        elif before.channel is not None and after.channel is None:
            if channelIsWatched(before.channel.id):
                await before.channel.send(
                    f"Goodbye **{memberName}**! I hope you had a good time!"
                )

        elif after.channel is not None and not before.self_stream and after.self_stream:
            if channelIsWatched(after.channel.id):
                await after.channel.send(f"**{memberName}** started streaming. Meow~")

    # invite creation event
    async def on_invite_create(self, invite: Invite):
        if invite.inviter.id == self.user.id:
            return
        db.insertIntoLoggedInvite(
            invite.id, invite.guild.id, invite.inviter.id, invite.url
        )
        inviterName: str = invite.inviter.name
        if invite.guild.get_member(invite.inviter.id) is not None:
            inviterName = invite.guild.get_member(
                invite.inviter.id).display_name
        await Reports.reportInvite(
            invite.guild,
            invite.guild.id,
            invite.channel.id,
            inviterName,
            invite.url,
        )
        await self.readInviteStore()

    # invite deletion event
    async def on_invite_delete(self, invite: Invite):
        await self.readInviteStore()

    # user join event
    async def on_member_join(self, member: Member):
        embed = Embed(
            title="Member Joined",
            description=f"Member **{member.name}** joined the server.",
            color=0x00FF00,
        )
        embed.set_footer(text="ZuriBot")

        invites = await member.guild.invites()
        foundInvite: Invite | None = None
        fallbackFoundInvite: LoggedInvite | None = None

        for invite in invites:
            inviteInternal = invitesStore.getById(invite.id, invite.guild.id)
            if inviteInternal is None:
                continue
            if inviteInternal.uses < invite.uses:
                foundInvite = invite
                break

        inviterFinal: Member | None = foundInvite.inviter if foundInvite is not None else None

        loggedInvites = db.fetchAllLoggedInvitesForGuild(member.guild.id)
        if loggedInvites is not None:
            for loggedInvite in loggedInvites:
                if (
                    invitesStore.getById(
                        loggedInvite.invite_id, loggedInvite.guild_id
                    )
                    is None
                ):
                    fallbackFoundInvite = loggedInvite
                    break

        if fallbackFoundInvite is not None:
            inviter = member.guild.get_member(fallbackFoundInvite.inviter_id)
            if inviter is not None:
                inviterFinal = inviter

        if inviterFinal is not None:
            embed.add_field(
                name="Inviter",
                value=f"**{inviterFinal.display_name}**'s invite was used."
            )

        await self.readInviteStore()

        reportChannels = Reports.getReportChannels()
        if member.guild.id not in reportChannels.keys():
            return
        await member.guild.get_channel(reportChannels[member.guild.id]).send(
            embed=embed
        )


client = ZuriBot()
client.run()
