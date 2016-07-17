import json


class Like:
    def __init__(self, _json=None):
        if _json:
            self._dict__ = json.loads(_json)
        else:
            pass
