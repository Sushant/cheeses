from big_cheese import BigCheese
from collections import defaultdict
from .exceptions import GCounterException

class GCounter(BigCheese):
    def __init__(self):
        self.e = defaultdict(int)

    @classmethod
    def from_dict(cls, counter_dict):
        obj = cls()
        if 'e' in counter_dict:
            obj.e = counter_dict['e']
        return obj

    def increment(self, delta=1, node=None):
        if delta < 0:
            raise GCounterException('Attempted to decrement g-counter value.')
        if not node:
            node = BigCheese.node()
        self.e[node] += int(delta)

    def value(self):
        return sum(self.e.itervalues())

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise GCounterException('Attempted to merge with different type.')
        
        all_keys = self.e.viewkeys() | other.e
        for k in all_keys:
            if k in other.e: # else defaultdict adds k to other.e
                self.e[k] = max(self.e[k], other.e[k])

    def to_dict(self):
        return {
            'type': self.crdt_type(),
            'e': dict(self.e)
        }

    def crdt_type(self):
        return 'g-counter'
