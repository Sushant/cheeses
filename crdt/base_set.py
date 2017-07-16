import copy
import json

class BaseSet(object):
    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {}

    def to_json(self):
        return json.dumps(self.to_dict())

    def clone(self):
        return copy.deepcopy(self)