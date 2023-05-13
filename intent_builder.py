from discord import Intents

class IntentBuilder:
    def getIntents() -> Intents:
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.guilds = True
        intents.guild_messages = True
        return intents