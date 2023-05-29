from discord import Embed

class HelpEmbeds:

    @staticmethod
    def basicHelp() -> Embed:
        embed = Embed(title="Help", description="Here are the commands you can use with me!", color=0xfabf34)
        embed.add_field(name="Invites", value="Invites can be created every 7 days for each user. Use /create_invite.", inline=False)
        embed.add_field(name="Image functions", value="Right clicking on a message with an image will list my Image commands under Apps.", inline=False)
        embed.add_field(name="Other functions", value="Use /help commands", inline=False)
        return embed
    
    @staticmethod
    def slashHelp() -> Embed:
        embed = Embed(title="Slash commands", description="I'll update these when I'm not being lazy", color=0xfabf34)
        return embed