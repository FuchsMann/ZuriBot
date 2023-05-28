class TableDefs:
    # Table definitions for sqlite3 tables

    @staticmethod
    def getCustomMessageTableDef():
        # check if table CustomMessage exists, if not create one with the following columns: message_id, user_id, guild_id, message with auto increment on message_id
        return """CREATE TABLE IF NOT EXISTS CustomMessage (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL,
            message TEXT NOT NULL
        )"""

    @staticmethod
    def getWatchedChannelTableDef():
        # check if table WatchedChannel exists, if not create one with the following columns: watch_id as PK, guild_id, channel_id, channel_name
        return """CREATE TABLE IF NOT EXISTS WatchedChannel (
            watch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            channel_name TEXT NOT NULL
        )"""
