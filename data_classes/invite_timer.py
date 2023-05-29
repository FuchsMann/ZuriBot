from datetime import datetime, timedelta
import pytz


class InviteTimer:
    def __init__(self, user_id: int, last_invite_date: datetime | str):
        self.user_id = user_id
        if isinstance(last_invite_date, str):
            # create datetime from isoformat string
            self.last_invite_date: datetime = datetime.fromisoformat(
                last_invite_date)
        else:
            self.last_invite_date: datetime = last_invite_date
        self.last_invite_date = self.last_invite_date.replace(tzinfo=pytz.utc)

    def timeToNextInvite(self) -> tuple[int, int, int]:
        # returns tuple of days, hours, minutes
        # time to next invite is last invite date + 7 days
        next_invite_date = self.last_invite_date + timedelta(days=7)
        time_to_next_invite = next_invite_date - datetime.now(pytz.utc)
        return (time_to_next_invite.days, time_to_next_invite.seconds // 3600, (time_to_next_invite.seconds // 60) % 60)

    def canCreateInvite(self) -> bool:
        # returns true if time to next invite is 0 or days is negative
        return self.timeToNextInvite() == (0, 0, 0) or self.timeToNextInvite()[0] < 0
