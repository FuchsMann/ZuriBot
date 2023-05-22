import json


class WatchedChannel:
    def __init__(self, channel_id: int, channel_name: str):
        self.channel_id = channel_id
        self.channel_name = channel_name

    def toDict(self) -> dict:
        return {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name
        }


class WatchedChannelList(list[WatchedChannel]):
    def __init__(self):
        super().__init__()

    def contains(self, channel_id) -> bool:
        for channel in self:
            if channel.channel_id == channel_id:
                return True
        return False

    def removeByID(self, channel_id) -> None:
        for channel in self:
            if channel.channel_id == channel_id:
                self.remove(channel)

    def toDict(self) -> dict:
        return {
            'channels': [channel.toDict() for channel in self]
        }

    def toJSON(self, path) -> None:
        with path.open('w') as file:
            json.dump(self.toDict(), file, indent=4)

    def fromJSON(self, path) -> None:
        with path.open('r') as file:
            data = json.load(file)
            for channel in data['channels']:
                self.append(WatchedChannel(
                    channel['channel_id'], channel['channel_name']))
