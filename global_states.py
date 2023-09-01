from discord import Invite


class InviteInternal:
    def __init__(self, id: str, guild_id: int, uses: int) -> None:
        self.id: str = id
        self.guild_id: int = guild_id
        self.uses: int = uses

    @staticmethod
    def fromInvite(invite: Invite) -> "InviteInternal":
        return InviteInternal(
            id=invite.id,
            guild_id=invite.guild.id,
            uses=invite.uses if invite.uses is not None else 0,
        )


class InvitesStore:
    def __init__(self, invites: list[InviteInternal] = []) -> None:
        self.invites: list[InviteInternal] = invites

    def getById(self, id: str, guild_id: int) -> InviteInternal | None:
        for invite in self.invites:
            if invite.id == id and invite.guild_id == guild_id:
                return invite
        return None

    def debugPrintAll(self) -> None:
        for invite in self.invites:
            print(invite.id, invite.guild_id, invite.uses)


if not "invitesStore" in globals():
    invitesStore = InvitesStore()
