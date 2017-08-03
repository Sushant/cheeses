from big_cheese import BigCheese
from collections import defaultdict
from .exceptions import PNCounterException

class PNCounter(BigCheese):
    def __init__(self):
        self.p = defaultdict(int)
        self.n = defaultdict(int)

    def value(self):
        return sum(self.p.itervalues()) - sum(self.n.itervalues())

    def increment(self, delta=1, node=None):
        if delta < 0:
            raise PNCounterException('Use decrement operation to decrement counter value.')
        if not node:
            node = BigCheese.node()
        self.p[node] += int(delta)

    def decrement(self, delta=1, node=None):
        if delta < 0:
            raise PNCounterException('Use increment operation to increment counter value.')
        if not node:
            node = BigCheese.node()
        self.n[node] += int(delta)

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise PNCounterException('Attempted to merge with different type.')
        
        all_p_keys = self.p.viewkeys() | other.p
        for k in all_p_keys:
            if k in other.p:
                self.p[k] = max(self.p[k], other.p[k])

        all_n_keys = self.n.viewkeys() | other.n
        for k in all_n_keys:
            if k in other.n:
                self.n[k] = max(self.n[k], other.n[k])

    def to_dict(self):
        return {
            'type': self.crdt_type(),
            'p': dict(self.p),
            'n': dict(self.n)
        }
    
    def crdt_type(self):
        return 'pn-counter'