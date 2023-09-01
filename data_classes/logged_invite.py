import json


class LoggedInvite:
    def __init__(self, invite_id: int, guild_id: int, inviter_id: int, invite_url: str):
        self.invite_id = invite_id
        self.guild_id = guild_id
        self.inviter_id = inviter_id
        self.invite_url = invite_url

    def toDict(self) -> dict:
        return {
            "invite_id": self.invite_id,
            "guild_id": self.guild_id,
            "inviter_id": self.inviter_id,
            "invite_url": self.invite_url,
        }

    def toJSON(self) -> str:
        return json.dumps(self.toDict())
