from big_cheese import BigCheese
from collections import defaultdict
from .exceptions import ORSetException

class ORSet(BigCheese):
    """
    Set where an element may be added and removed any number of times.
    A unique tag is added for every add operation. On remove, all the tags
    in add set are copied to the remove set.
    An element is present iff all tags in add set are not in remove set.
    """

    def __init__(self):
        self.e = defaultdict(lambda : defaultdict(set))

    @classmethod
    def from_dict(cls, set_dict):
        obj = cls()
        if 'e' in set_dict:
            try:
                for item in set_dict['e']:
                    obj.e[item[0]] = {'a': set(item[1]), 'r': set(item[2])}
            except IndexError:
                raise ORSetException('Failed to parse dict.')
        return obj

    def add(self, element):
        self.e[element]['a'].add(BigCheese.tag())

    def remove(self, element):
        if element in self.e:
            self.e[element]['r'].update(self.e[element]['a'])

    def to_list(self):
        return [x for x in self.e.iterkeys() if self.e[x]['a'] - self.e[x]['r']]

    def lookup(self, element):
        if element in self.e:
            return len(self.e[element]['a'] - self.e[element]['r']) > 0
        return False

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise ORSetException('Attempted to merge with different type.')

        all_keys = self.e.viewkeys() | other.e
        for k in all_keys:
            if k in other.e: # else defaultdict adds k to other.e
                self.e[k]['a'].update(other.e[k]['a'])
                self.e[k]['r'].update(other.e[k]['r'])

    def to_dict(self):
        return {
            'type': self.crdt_type(),
            'e': [[k, list(v['a']), list(v['r'])] for k, v in self.e.iteritems()]
        }

    def crdt_type(self):
        return 'or-set'
