import copy
import json
import time
from collections import defaultdict
from .exceptions import LWWSetException

class LWWSet(object):
    def __init__(self, bias='a'):
        self.e = defaultdict(lambda : defaultdict(float))
        self.bias = bias

    @classmethod
    def biases(cls):
        return ['a', 'r']

    def add(self, element):
        self.e[element]['a'] = time.time()

    def remove(self, element):
        self.e[element]['r'] = time.time()

    def to_list(self):
        if self.bias == 'r':
            return [x for x in self.e.keys() if self.e[x]['a'] > self.e[x]['r']]
        return [x for x in self.e.keys() if self.e[x]['a'] >= self.e[x]['r']]

    def lookup(self, element):
        if not self.e[element]['a']:
            return False

        if self.bias == 'r':
            return self.e[element]['a'] > self.e[element]['r']
        return self.e[element]['a'] >= self.e[element]['r']

    def clone(self):
        return copy.deepcopy(self)

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise LWWSetException('Attempted to merge with different type.')

        all_keys = self.e.viewkeys() | other.e
        for k in all_keys:
            if k in other.e: # else defaultdict adds k to other.e
                self.e[k]['a'] = max(self.e[k]['a'], other.e[k]['a'])
                self.e[k]['r'] = max(self.e[k]['r'], other.e[k]['r'])

    def __repr__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps({
            'type': 'lww-set',
            'bias': self.bias,
            'e': [[k, v['a'], v['r']] for k, v in self.e.iteritems()]
        })