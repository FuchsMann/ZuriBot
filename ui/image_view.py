import discord
from discord.ui import View, button
from enum import Enum

class ResponseType(Enum):
    NONE = 0
    SOY = 1
    SOYPHONE = 2
    JAVAKICK = 3
    PEPPERDREAM = 4
    TV = 5
    CASEYINVERT = 6


class ImageView(View):

    def __init__(self):
        super().__init__(timeout=30.0)
        self.responseType: ResponseType = ResponseType.NONE
    
    def closeView(self):
        self.is_finished = True
        self.stop()

    @button(label='Soy', style=discord.ButtonStyle.blurple, row=1)
    async def soy(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.responseType = ResponseType.SOY
        self.closeView()

    @button(label='Soy Phone', style=discord.ButtonStyle.blurple, row=1)
    async def soyPhone(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.responseType = ResponseType.SOYPHONE
        self.closeView()

    @button(label='Java Kick', style=discord.ButtonStyle.blurple, row=2)
    async def javaKick(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.responseType = ResponseType.JAVAKICK
        self.closeView()

    @button(label='Pepper Dream', style=discord.ButtonStyle.blurple, row=2)
    async def pepperDream(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.responseType = ResponseType.PEPPERDREAM
        self.closeView()

    @button(label='TV', style=discord.ButtonStyle.blurple, row=3)
    async def tv(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.responseType = ResponseType.TV
        self.closeView()

    @button(label='Casey Invert', style=discord.ButtonStyle.blurple, row=3)
    async def caseyInvert(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.responseType = ResponseType.CASEYINVERT
        self.closeView()