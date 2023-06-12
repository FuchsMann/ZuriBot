import sys
from pathlib import Path

# Add sibling folders to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import atexit
import signal
from database.tabledefs import TableDefs
import sqlite3
from data_classes.invite_timer import InviteTimer
from data_classes.watched_channels import WatchedChannel
from data_classes.custom_messages import CustomMessage
from data_classes.watched_mcserver import WatchedMCServer
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(Path('database', 'db', 'zuri.db'))
        self.cur = self.conn.cursor()
        self.initTables()
        atexit.register(self.closeDB)
        signal.signal(signal.SIGTERM, self.closeDB)
        signal.signal(signal.SIGINT, self.closeDB)

    def closeDB(self, *args):
        try:
            self.cur.close()
            sys.exit(0)
        except:
            exit(0)

    def initTables(self):
        self.cur.execute(TableDefs.getCustomMessageTableDef())
        self.cur.execute(TableDefs.getWatchedChannelTableDef())
        self.cur.execute(TableDefs.getInviteTimerTableDef())
        self.cur.execute(TableDefs.getWatchedMCServerTableDef())
        self.conn.commit()

    # Custom Messages
    def insertIntoCustomMessage(self, user_id: int, guild_id: int, message: str):
        # check if entry with user_id and guild_id exists, if yes update message, if not insert new entry
        self.cur.execute(
            "SELECT * FROM CustomMessage WHERE user_id=? AND guild_id=?", (user_id, guild_id))
        if self.cur.fetchone() is None:
            self.cur.execute(
                "INSERT INTO CustomMessage (user_id, guild_id, message) VALUES (?, ?, ?)", (user_id, guild_id, message))
        else:
            self.cur.execute(
                "UPDATE CustomMessage SET message=? WHERE user_id=? AND guild_id=?", (message, user_id, guild_id))
        self.conn.commit()

    def fetchCustomMessagesForGuild(self, guild_id: int) -> list[CustomMessage] | None:
        self.cur.execute(
            "SELECT user_id, message FROM CustomMessage WHERE guild_id=?", (guild_id,))
        result = self.cur.fetchall()
        if result is None:
            return None
        else:
            return [CustomMessage(guild_id=guild_id, user_id=user_id, message=message) for user_id, message in result]

    def fetchCustomMessage(self, user_id: int, guild_id: int) -> CustomMessage | None:
        self.cur.execute(
            "SELECT message FROM CustomMessage WHERE user_id=? AND guild_id=?", (user_id, guild_id))
        result = self.cur.fetchone()
        if result is None:
            return None
        else:
            return CustomMessage(guild_id=guild_id, user_id=user_id, message=result[0])

    def removeCustomMessage(self, user_id: int, guild_id: int):
        self.cur.execute(
            "DELETE FROM CustomMessage WHERE user_id=? AND guild_id=?", (user_id, guild_id))
        self.conn.commit()

    # Watched Channels
    def fetchWatchedChannel(self, channel_id: int, guild_id: int) -> WatchedChannel | None:
        self.cur.execute(
            "SELECT channel_name FROM WatchedChannel WHERE channel_id=? AND guild_id=?", (channel_id, guild_id))
        result = self.cur.fetchone()
        if result is None:
            return None
        else:
            return WatchedChannel(guild_id=guild_id, channel_id=channel_id, channel_name=result[0])

    def fetchWatchedChannelsForGuild(self, guild_id: int) -> list[WatchedChannel] | None:
        self.cur.execute(
            "SELECT channel_id, channel_name FROM WatchedChannel WHERE guild_id=?", (guild_id,))
        result = self.cur.fetchall()
        if result is None:
            return None
        else:
            return [WatchedChannel(guild_id=guild_id, channel_id=channel_id, channel_name=channel_name) for channel_id, channel_name in result]

    def insertIntoWatchedChannels(self, guild_id: int, channel_id: int, channel_name: str):
        # check if entry with channel_id and guild_id exists, if yes update channel_name, if not insert new entry
        if Database.fetchWatchedChannel(self, channel_id, guild_id) is None:
            self.cur.execute(
                "INSERT INTO WatchedChannel (channel_id, guild_id, channel_name) VALUES (?, ?, ?)", (channel_id, guild_id, channel_name))

    def toggleWatchedChannel(self, guild_id: int, channel_id: int, channel_name: str) -> str:
        if Database.fetchWatchedChannel(self, channel_id, guild_id) is None:
            self.cur.execute(
                "INSERT INTO WatchedChannel (channel_id, guild_id, channel_name) VALUES (?, ?, ?)", (channel_id, guild_id, channel_name))
            self.conn.commit()
            return "added"
        else:
            self.cur.execute(
                "DELETE FROM WatchedChannel WHERE channel_id=? AND guild_id=?", (channel_id, guild_id))
            self.conn.commit()
            return "removed"

    def removeWatchedChannel(self, channel_id: int, guild_id: int):
        self.cur.execute(
            "DELETE FROM WatchedChannel WHERE channel_id=? AND guild_id=?", (channel_id, guild_id))
        self.conn.commit()

    # Invite Timer
    def fetchInviteTimer(self, user_id: int) -> InviteTimer | None:
        self.cur.execute(
            "SELECT last_invite_date FROM InviteTimer WHERE user_id=? ORDER BY timer_ID DESC LIMIT 1", (user_id,))
        result = self.cur.fetchone()
        if result is None:
            return None
        else:
            return InviteTimer(user_id=user_id, last_invite_date=result[0])

    def insertIntoInviteTimer(self, user_id: int, last_invite_date: datetime):
        last_invite_date_str = last_invite_date.isoformat()
        self.cur.execute(
            "INSERT INTO InviteTimer (user_id, last_invite_date) VALUES (?, ?)", (user_id, last_invite_date_str))
        self.conn.commit()

    def clearInviteTimer(self, user_id: int):
        self.cur.execute("DELETE FROM InviteTimer WHERE user_id=?", (user_id,))
        self.conn.commit()


if not 'db' in globals():
    db = Database()