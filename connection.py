import requests
from datetime import datetime
from time import time


class Connection:
    def __init__(self, lamp_spec) -> None:
        self.ID = lamp_spec["ID"]

        self.BASE_URL = 'http://10.20.2.138:1484'
        self.API_AUTH = {
            'update': '/makentu/update_detection', 
            'fetch': '/makentu/fetch_object', 
        }

        self.session = requests.Session()
    
    def update_detection(self, objects):
        _data = {
            "ID": self.ID, 
            "objects": objects, 
        }

        req = self.session.post(
            self.BASE_URL + self.API_AUTH['update'], json=_data,
            allow_redirects=True
        )

        return req.json()
    
    def fetch_object(self):
        _data = {
            "ID": self.ID, 
        }

        req = self.session.post(
            self.BASE_URL + self.API_AUTH['fetch'], json=_data,
            allow_redirects=True
        )
        
        return req.json()


# BASE_URL = 'http://10.20.2.138:1484'
# API_AUTH = '/makentu/update_detection'

# session = requests.Session()

# _data = {
#     "ID": "0", 
#     "objects": [
#         { "type": "car", "position": [1, 3] }, 
#         { "type": "car", "position": [3, 2] }, 
#         ], 
# }

# req = session.post(
#     BASE_URL + API_AUTH, json=_data,
#     allow_redirects=True
# )

# print(req.json())

