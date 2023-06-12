class WatchedMCServer:
    def __init__(self, guild_id: int, channel_id: int, message_id: int, server_address: str):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.server_address = server_address