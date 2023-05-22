from data_classes.channel_subscription import ChannelSubscription
import json
from pathlib import Path

class UserSettings:
  def __init__(self, userID: int = 0) -> None:
    self.userID = userID
    self.channelSubscriptions: list[ChannelSubscription] = []
    
  def toDict(self) -> dict:
    return {
      'userID': self.userID,
      'channelSubscriptions': [subscription.toDict() for subscription in self.channelSubscriptions]
    }
    
  def getSubscriptionForChannel(self, channelID: int) -> ChannelSubscription:
    for subscription in self.channelSubscriptions:
      if subscription.channelID == channelID:
        return subscription
    return None
  
  def addOrRemoveSubscriptionForChannel(self, guildID: int, channelID: int, userIDs: list[int]) -> None:
    subscription = self.getSubscriptionForChannel(channelID)
    if subscription is not None:
      self.channelSubscriptions.remove(subscription)
    self.channelSubscriptions.append(ChannelSubscription(guildID, channelID, userIDs))
  
  def toJSON(self, path: Path) -> None:
    with path.open('w') as file:
      json.dump(self.toDict(), file, indent=4)
      
  def fromJSON(self, path: Path) -> None:
    with path.open('r') as file:
      data = json.load(file)
      self.userID = data['userID']
      for subscription in data['channelSubscriptions']:
        self.channelSubscriptions.append(ChannelSubscription(subscription['channelID'], subscription['userIDs']))