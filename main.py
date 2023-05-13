import discord
from discord import VoiceState, Member
from auth import Auth
from intent_builder import IntentBuilder
from commands import CommandManager
from data_manager import DataManager


class ZuriBot(discord.Client):
    def __init__(self):
        self.authData = Auth()
        super().__init__(intents=IntentBuilder.getIntents())
        self.commandManager = CommandManager(self)

    def run(self) -> None:
        super().run(self.authData.token)

    async def on_ready(self) -> None:
        await self.commandManager.tree.sync()
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        watchedChannels = DataManager.loadWatchedChannels(
            member.guild.id)
        customMessages = DataManager.loadGuildCustomMessages(
            member.guild.id)
        if before.channel is None and after.channel is not None:
            if watchedChannels.contains(after.channel.id):
                if customMessages.contains(member.id):
                    await after.channel.send(customMessages.getByID(member.id).message)
                else:
                    await after.channel.send(f'Hello **{member.name}**! Welcome to {after.channel.name}!')
        elif before.channel is not None and after.channel is None:
            if watchedChannels.contains(before.channel.id):
                await before.channel.send(f'Goodbye **{member.name}**! I hope you had a good time!')


client = ZuriBot()
client.run()
