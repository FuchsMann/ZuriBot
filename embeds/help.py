from discord import Embed

class HelpEmbeds:

    @staticmethod
    def basicHelp() -> Embed:
        embed = Embed(title="Help", description="Here are the commands you can use with me!", color=0xfabf34)
        embed.add_field(name="Image functions", value="Right clicking on a message with an image will list my Image commands under Apps.", inline=False)
        return embed