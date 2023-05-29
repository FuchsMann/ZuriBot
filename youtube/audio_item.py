from pytube import YouTube
from discord import Member

class AudioItem:
    def __init__(self, url: str, requester: Member) -> None:
        self.url = url
        self.requester = requester
        self.youtubeObject = YouTube(url)