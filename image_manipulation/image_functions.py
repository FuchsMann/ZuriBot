from PIL import Image
from discord import File
from io import BytesIO
from pathlib import Path
import requests


class ImageFunctions:
    @staticmethod
    def soy(imageUrl: str) -> File:
        inImage = Image.open(
            BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        overImage = Image.open(
            Path('image_manipulation', 'images', 'soyjaks.png'))
        overImage = overImage.resize(
            inImage.size, Image.LANCZOS)  # type: ignore
        inImage.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        byteArr = BytesIO()
        inImage = inImage.convert('RGB')
        inImage.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='Soy.jpg')

    @staticmethod
    def soyphone(imageUrl: str) -> File:
        inImage = Image.open(
            BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        if inImage.size[0] / inImage.size[1] >= 1:
            overImage = Image.open(
                Path('image_manipulation', 'images', 'soyphoneH.png')
            )
            rootImage = Image.new('RGBA', overImage.size, (255, 255, 255))
            inImage = inImage.rotate(-0.92, expand=True)
            inImage = inImage.resize((372, 216), Image.LANCZOS) # type: ignore
            rootImage.paste(inImage, (71, 225, 443, 441), inImage)
        else:
            overImage = Image.open(
                Path('image_manipulation', 'images', 'soyphoneV.png')
            )
            rootImage = Image.new('RGBA', overImage.size, (255, 255, 255))
            inImage = inImage.rotate(4.78, expand=True)
            inImage = inImage.resize((276, 447), Image.LANCZOS) # type: ignore
            rootImage.paste(inImage, (24, 65, 300, 512), inImage)
        rootImage.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        rootImage = rootImage.convert('RGB')
        byteArr = BytesIO()
        rootImage.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='Soyphone.jpg')

    @staticmethod
    def javaKick(imageUrl: str) -> File:
        inImage = Image.open(
            BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        overImage = Image.open(
            Path('image_manipulation', 'images', 'javakick.png'))
        canvas = Image.new(
            'RGBA', overImage.size, (0, 0, 0, 0))
        inImage = inImage.resize((236, 282), Image.LANCZOS)  # type: ignore
        canvas.paste(
            inImage, (132, 666, 132 + 236, 666 + 282)
        )
        canvas.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        byteArr = BytesIO()
        canvas = canvas.convert('RGB')
        canvas.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='JavaKick.jpg')

    @staticmethod
    def pepperdream(imageUrl: str) -> File:
        inImage = Image.open(
            BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        overImage = Image.open(
            Path('image_manipulation', 'images', 'pepperdream.png'))
        canvas = Image.new(
            'RGBA', overImage.size, (0, 0, 0, 0))
        inImage = inImage.resize((1331, 1008), Image.LANCZOS)  # type: ignore
        canvas.paste(
            inImage, (61, 116, 61 + 1331, 116 + 1008)
        )
        canvas.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        byteArr = BytesIO()
        canvas = canvas.convert('RGB')
        canvas.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='PepperDream.jpg')

    @staticmethod
    def tv(imageUrl: str) -> File:
        inImage = Image.open(
            BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        overImage = Image.open(
            Path('image_manipulation', 'images', 'tv.png'))
        canvas = Image.new(
            'RGBA', overImage.size, (0, 0, 0, 0))
        inImage = inImage.resize(
            (281, 195), Image.LANCZOS).rotate(7.3, expand=False)  # type: ignore
        canvas.paste(
            inImage, (579, 254, 579 + 281, 254 + 195)
        )
        canvas.paste(
            overImage, (0, 0, overImage.size[0], overImage.size[1]), overImage
        )
        byteArr = BytesIO()
        canvas = canvas.convert('RGB')
        canvas.save(byteArr, 'JPEG')
        byteArr.seek(0)
        return File(byteArr, filename='TV.jpg')

    @staticmethod
    def rotateHue(imageUrl: str, hueOffsetDeg: int = 70) -> File:
        inImage = Image.open(
            BytesIO(requests.get(imageUrl).content)).convert('RGBA')
        alpha = inImage.getchannel('A')
        inImage = inImage.convert('HSV')
        hue, saturation, value = inImage.split()
        hue = hue.point(lambda i: (i + hueOffsetDeg) % 256)
        inImage = Image.merge('HSV', (hue, saturation, value))
        inImage = inImage.convert('RGBA')
        inImage.putalpha(alpha)
        byteArr = BytesIO()
        inImage.save(byteArr, 'PNG')
        byteArr.seek(0)
        return File(byteArr, filename='Rotated.png')

    # @staticmethod
    # def animatedColorRotation(imageUrl: str) -> File:
    #     inImage = Image.open(
    #         BytesIO(requests.get(imageUrl).content)).convert('RGBA')
    #     inImage.thumbnail((512, 512), Image.LANCZOS)

    #     alpha = inImage.getchannel('A')
    #     inImage = inImage.convert('HSV')
    #     hue, saturation, value = inImage.split()

    #     images = []
    #     for i in range(36):
    #         hueOffsetDeg = i * 10
    #         hueOffset = hueOffsetDeg / 360 * 256
    #         hue = hue.point(lambda i: (i + hueOffset) % 256)
    #         images.append(Image.merge('HSV', (hue, saturation, value)))

    #     for ima in images:
    #         ima = ima.convert('RGBA')
    #         ima.putalpha(alpha)

    #     byteArr = BytesIO()
    #     images[0].save(byteArr, format='GIF', save_all=True,
    #                    append_images=images[1:], duration=4, loop=0)
    #     byteArr.seek(0)
    #     return File(byteArr, filename='Rotated.gif')
