import json
from pathlib import Path


class CustomMessage:
    def __init__(self, guild_id=0, user_id=0, message='') -> None:
        self.user_id: int = user_id
        self.message: str = message
        self.guild_id: int = guild_id

    def toDict(self) -> dict:
        return {
            'guild_id': self.guild_id,
            'user_id': self.user_id,
            'message': self.message
        }