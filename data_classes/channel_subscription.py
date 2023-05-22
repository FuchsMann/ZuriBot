
class ChannelSubscription:
  def __init__(self, channelID: int = 0, userIDs: list[int] = []) -> None:
    self.channelID = channelID
    self.userIDs = userIDs
    
  def toDict(self) -> dict:
    return {
      'channelID': self.channelID,
      'userIDs': self.userIDs
    }