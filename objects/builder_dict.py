import json


class BuilderDict:
    def __init__(self):
        self._dict = dict()

    def add(self, key, val):
        self._dict[key] = val
        return self

    def to_string(self):
        return json.dumps(self._dict)

    @staticmethod
    def create_update_lease():
        response = BuilderDict()
        response.add('status', 'not valid token')
        return response.to_string()
