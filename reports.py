from discord import Embed, Guild
from auth import Auth


class Reports:
    # guild ID: report channel ID

    @staticmethod
    def getReportChannels() -> dict[int, int]:
        objDict = Auth().invite_posting_channels
        outDict = {}
        for obj in objDict:
            outDict[obj['guild_id']] = int(obj['channel_id'])
        return outDict


    @staticmethod
    async def reportInvite(
        guild: Guild,
        guild_id: int,
        invite_creation_channel_id: int,
        member_nick: str,
        invite_url: str,
    ) -> None:
        reportChannels = Auth().invite_posting_channels['guild_id']
        if guild_id not in Reports.reportChannels:
            return
        embed = Embed(
            title="Invite Created",
            description=f"Invite created by **{member_nick}**",
            color=0x00FF00,
        )
        embed.add_field(name="Invite URL", value=invite_url, inline=False)
        embed.add_field(
            name="Invite Channel",
            value=f"<#{invite_creation_channel_id}>",
            inline=False,
        )
        embed.set_footer(text="ZuriBot")
        await guild.get_channel(Reports.reportChannels[guild_id]).send(embed=embed)
