import json


class JsonObject:
    def __init__(self, _json):
        self.__dict__ = json.loads(_json)
