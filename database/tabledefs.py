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

    @staticmethod
    def getInviteTimerTableDef():
        # check if table InviteTimer exists, if not create one with the following columns: timer_id as PK, user_id, last_invite_date
        return """CREATE TABLE IF NOT EXISTS InviteTimer (
            timer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            last_invite_date TEXT NOT NULL
        )"""

    @staticmethod
    def getWatchedMCServerTableDef():
        # check if table WatchedMCServer exists, if not create one with the following columns: server_id as PK, guild_id, channel_id, message_id, server_address
        return """CREATE TABLE IF NOT EXISTS WatchedMCServer (
            server_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            server_address TEXT NOT NULL
        )"""

    @staticmethod
    def getLoggedInviteTableDef():
        # check if table LoggedInvite exists, if not create one with the following columns: invite_id as PK, guild_id, inviter_id, invite_url
        return """CREATE TABLE IF NOT EXISTS LoggedInvite (
            invite_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invite_id TEXT NOT NULL,
            guild_id INTEGER NOT NULL,
            inviter_id INTEGER NOT NULL,
            invite_url TEXT NOT NULL
        )"""
