import json
from pathlib import Path


class CustomMessage:
    def __init__(self, user_id=0, message='') -> None:
        self.user_id: int = user_id
        self.message: str = message

    def toDict(self) -> dict:
        return {
            'user_id': self.user_id,
            'message': self.message
        }


class CustomMessageList(list[CustomMessage]):

    def __init__(self) -> None:
        super().__init__()
        
    def contains(self, user_id: int) -> bool:
        for message in self:
            if message.user_id == user_id:
                return True
        return False
    
    def removeByID(self, user_id: int) -> None:
        for message in self:
            if message.user_id == user_id:
                self.remove(message)
                return
    
    def getByID(self, user_id: int) -> CustomMessage:
        for message in self:
            if message.user_id == user_id:
                return message
        return None

    def toDict(self) -> dict:
        return {
            'messages': [message.toDict() for message in self]
        }

    def toJSON(self, path: Path) -> None:
        with path.open('w') as file:
            json.dump(self.toDict(), file, indent=4)

    def fromJSON(self, path: Path) -> None:
        with path.open('r') as file:
            data = json.load(file)
            for message in data['messages']:
                self.append(CustomMessage(
                    message['user_id'], message['message']))
