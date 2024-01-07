from discord import Embed


class HelpEmbeds:

    @staticmethod
    def basicHelp() -> Embed:
        embed = Embed(
            title="Help", description="Here are the commands you can use with me!", color=0xfabf34)
        embed.add_field(
            name="Invites", value="Invites can be created every 7 days for each user. Use /create_invite.", inline=False)
        embed.add_field(name="Image functions",
                        value="Right clicking on a message with an image will list my Image commands under Apps.", inline=False)
        embed.add_field(name="Other functions",
                        value="Use /help commands", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/359108644337483776/1193604223456256010/image.png?ex=65ad518e&is=659adc8e&hm=57ee549aaa0458f584d78bfbaac8ce1459e31731edcf179939ea0ef7390999bd&")

        return embed

    @staticmethod
    def slashHelp() -> Embed:
        embed = Embed(title="Slash commands",
                      description="Commands you can ask me about with '/help command:commandname'", color=0xfabf34)
        embed.set_image(url="https://cdn.discordapp.com/attachments/359108644337483776/1193604761036001280/image.png?ex=65ad520f&is=659add0f&hm=1793907eae72ed28779820ad354ef5af1777123a82838d9d4af143ef8716a42d&")
        return embed
