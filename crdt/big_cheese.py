import copy
import json
import uuid

class BigCheese(object):
    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {}

    def to_json(self):
        return json.dumps(self.to_dict())

    def clone(self):
        return copy.deepcopy(self)

    @staticmethod
    def tag():
        return str(uuid.uuid4())

    @staticmethod
    def node():
        return str(uuid.getnode())