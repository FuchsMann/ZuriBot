from typing import BinaryIO
from pytube import YouTube
from discord import Member
from sys import getsizeof


class AudioItem:
    def __init__(self, url: str, requester_id: int) -> None:
        self.url = url
        self.requester = requester_id
        self.youtubeObject = YouTube(url)
        self.audioBytes: BinaryIO
        stream = self.youtubeObject.streams.filter(
            only_audio=True).first()
        if stream is not None:
            stream.stream_to_buffer(self.audioBytes)
            # print size of self.audioBytes
            print(getsizeof(self.audioBytes))

    def writeToFile(self, path: str) -> None:
        with open(path, 'wb') as file:
            file.write(self.audioBytes)

ai = AudioItem('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 1)
