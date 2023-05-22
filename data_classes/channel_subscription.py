
class ChannelSubscription:
  def __init__(self, guildID: int = 0, channelID: int = 0, userIDs: list[int] = []) -> None:
    self.guildID = guildID
    self.channelID = channelID
    self.userIDs = userIDs
    
  def toDict(self) -> dict:
    return {
      'guildID': self.guildID,
      'channelID': self.channelID,
      'userIDs': self.userIDs
    }