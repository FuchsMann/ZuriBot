import json


class WatchedChannel:
    def __init__(self, guild_id: int, channel_id: int, channel_name: str):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.channel_name = channel_name

    def toDict(self) -> dict:
        return {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name
        }
