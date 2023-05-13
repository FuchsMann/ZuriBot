from pathlib import Path
from data_classes.custom_messages import CustomMessage, CustomMessageList
from data_classes.watched_channels import WatchedChannel, WatchedChannelList

BASEPATH = Path('data')
MESSAGES_BASENAME = "_messages.json"
WATCHLIST_BASENAME = "_watchlist.json"


class DataManager:

    # Custom Messages
    def loadGuildCustomMessages(guild_id: int) -> CustomMessageList:
        DataManager.ensureGuildCustomMessagesFileExists(guild_id)
        path = Path(BASEPATH, str(guild_id) + MESSAGES_BASENAME)
        messages = CustomMessageList()
        messages.fromJSON(path)
        return messages

    def saveGuildCustomMessages(guild_id: int, messages: CustomMessageList) -> None:
        path = Path(BASEPATH, str(guild_id) + MESSAGES_BASENAME)
        messages.toJSON(path)

    def addGuildCustomMessage(guild_id: int, user_id: int, message: str) -> None:
        messages = DataManager.loadGuildCustomMessages(guild_id)
        messages.append(CustomMessage(user_id, message))
        DataManager.saveGuildCustomMessages(guild_id, messages)

    def ensureGuildCustomMessagesFileExists(guild_id: int) -> None:
        path = Path(BASEPATH, str(guild_id) + MESSAGES_BASENAME)
        if not path.exists():
            DataManager.saveGuildCustomMessages(guild_id, CustomMessageList())

    # Watched Channels
    def loadWatchedChannels(guild_id: int) -> WatchedChannelList:
        DataManager.ensureWatchedChannelsFileExists(guild_id)
        path = Path(BASEPATH, str(guild_id) + WATCHLIST_BASENAME)
        channels = WatchedChannelList()
        channels.fromJSON(path)
        return channels

    def saveWatchedChannels(guild_id: int, channels: WatchedChannelList) -> None:
        path = Path(BASEPATH, str(guild_id) + WATCHLIST_BASENAME)
        channels.toJSON(path)

    def toggleWatchedChannel(guild_id: int, channel_id: int, channel_name: str) -> str:
        channels = DataManager.loadWatchedChannels(guild_id)
        if channels.contains(channel_id):
            channels.removeByID(channel_id)
            DataManager.saveWatchedChannels(guild_id, channels)
            return 'removed'
        else:
            channels.append(WatchedChannel(channel_id, channel_name))
            DataManager.saveWatchedChannels(guild_id, channels)
            return 'added'

    def ensureWatchedChannelsFileExists(guild_id: int) -> None:
        path = Path(BASEPATH, str(guild_id) + WATCHLIST_BASENAME)
        if not path.exists():
            DataManager.saveWatchedChannels(guild_id, WatchedChannelList())
