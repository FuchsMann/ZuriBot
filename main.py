import discord
from discord import VoiceState, Member
from auth import Auth
from intent_builder import IntentBuilder
from commands import CommandManager


class ZuriBot(discord.Client):
    def __init__(self):
        self.authData = Auth()
        super().__init__(intents=IntentBuilder.getIntents())
        self.commandManager = CommandManager(self)

    def run(self) -> None:
        super().run(self.authData.token)

    async def on_ready(self) -> None:
        await self.commandManager.tree.sync(guild=discord.Object(id=359108643599417344))
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        # print(f'Voice state update from {member}: {before} -> {after}')
        if before.channel is None and after.channel is not None:
            print(f'{member} joined {after.channel}')


client = ZuriBot()
client.run()
