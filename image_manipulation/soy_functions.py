from PIL import Image
from discord import File
from io import BytesIO
from pathlib import Path
import requests


class SoyFunctions:
    def soy(imageUrl: str) -> File:
        inImage = Image.open(BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        overImage = Image.open(Path('image_manipulation', 'images', 'soyjaks.png'))
        overImage = overImage.resize(inImage.size, Image.ANTIALIAS)
        inImage.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        byteArr = BytesIO()
        inImage = inImage.convert('RGB')
        inImage.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='Soy.jpg')

    def soyphone(imageUrl: str) -> File:
        inImage = Image.open(BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        if inImage.size[0] / inImage.size[1] >= 1:
            overImage = Image.open(
                Path('image_manipulation', 'images', 'soyphoneH.png')
            )
            rootImage = Image.new('RGBA', overImage.size, (255, 255, 255))
            inImage = inImage.rotate(-0.92, expand=1)
            inImage = inImage.resize((372, 216), Image.ANTIALIAS)
            rootImage.paste(inImage, (71, 225, 443, 441), inImage)
        else:
            overImage = Image.open(
                Path('image_manipulation', 'images', 'soyphoneV.png')
            )
            rootImage = Image.new('RGBA', overImage.size, (255, 255, 255))
            inImage = inImage.rotate(4.78, expand=1)
            inImage = inImage.resize((276, 447), Image.ANTIALIAS)
            rootImage.paste(inImage, (24, 65, 300, 512), inImage)
        rootImage.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        rootImage = rootImage.convert('RGB')
        byteArr = BytesIO()
        rootImage.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='Soyphone.jpg')
