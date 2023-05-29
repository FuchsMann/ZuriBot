import discord
from discord import VoiceState, Member
from auth import Auth
from intent_builder import IntentBuilder
from commands import CommandManager
from database.database import db


class ZuriBot(discord.Client):
    def __init__(self):
        self.authData = Auth()
        super().__init__(intents=IntentBuilder.getIntents())
        self.commandManager = CommandManager(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="You. Meow~")

    def run(self) -> None:
        super().run(self.authData.token)

    async def on_ready(self) -> None:
        await self.commandManager.tree.sync()
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        watchedChannels = db.fetchWatchedChannelsForGuild(
            member.guild.id)
        if watchedChannels is None:
            return
        
        memberName = member.nick if member.nick is not None else member.name

        def channelIsWatched(channelID: int) -> bool:
            return channelID in [channel.channel_id for channel in watchedChannels] # type: ignore

        if before.channel is None and after.channel is not None:
            if channelIsWatched(after.channel.id):
                customMessage = db.fetchCustomMessage(member.id, member.guild.id)
                if customMessage is not None:
                    await after.channel.send(customMessage.message + f'\n({memberName} joined)')
                else:
                    await after.channel.send(f'Hello **{memberName}**! Welcome to {after.channel.name}!')

        elif before.channel is not None and after.channel is None:
            if channelIsWatched(before.channel.id):
                await before.channel.send(f'Goodbye **{memberName}**! I hope you had a good time!')

        elif after.channel is not None and not before.self_stream and after.self_stream:
            if channelIsWatched(after.channel.id):
                await after.channel.send(f'**{memberName}** started streaming. Meow~')


client = ZuriBot()
client.run()
