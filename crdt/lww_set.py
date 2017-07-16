import time
from base_set import BaseSet
from collections import defaultdict
from .exceptions import LWWSetException

class LWWSet(BaseSet):
    def __init__(self, bias='a'):
        self.e = defaultdict(lambda : defaultdict(float))
        self.bias = bias

    @classmethod
    def from_dict(cls, set_dict):
        obj = cls()
        if 'bias' in set_dict:
            obj.bias = set_dict['bias']
        if 'e' in set_dict:
            try:
                for item in set_dict['e']:
                    obj.e[item[0]] = {'a': item[1], 'r': item[2]}
            except IndexError:
                raise LWWSetException('Failed to parse dict.')
        return obj

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

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise LWWSetException('Attempted to merge with different type.')

        all_keys = self.e.viewkeys() | other.e
        for k in all_keys:
            if k in other.e: # else defaultdict adds k to other.e
                self.e[k]['a'] = max(self.e[k]['a'], other.e[k]['a'])
                self.e[k]['r'] = max(self.e[k]['r'], other.e[k]['r'])

    def to_dict(self):
        return {
            'type': 'lww-set',
            'bias': self.bias,
            'e': [[k, v['a'], v['r']] for k, v in self.e.iteritems()]
        }
