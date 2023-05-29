from audio_item import AudioItem

class AudioManager:
    def __init__(self) -> None:
        self.audioItemQueue: list[AudioItem] = []
        self.currentAudioItem: AudioItem | None = None

    def next(self) -> None:
        if len(self.audioItemQueue) > 0:
            self.currentAudioItem = self.audioItemQueue.pop(0)
        else:
            self.currentAudioItem = None

    def clear(self) -> None:
        self.audioItemQueue.clear()
        self.currentAudioItem = None