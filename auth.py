import json
from pathlib import Path

class Auth:
    def __init__(self):
        jsonPath = Path('./data/auth.json')
        in_json = json.loads(open(jsonPath).read())
        self.token = in_json['token']
        self.permissions_int = in_json['permissions_int']
        self.invite_posting_channels = in_json['invite_posting_channels']
        self.mcserver_address = in_json['mcserver_address']