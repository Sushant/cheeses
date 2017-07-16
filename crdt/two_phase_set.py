from base_set import BaseSet
from .exceptions import TwoPhaseSetException

class TwoPhaseSet(BaseSet):
    """
     Set where an element may be added and removed, but never added again thereafter.
     Adding or removing the same element twice has no effect, nor does adding an element
     that has already been removed.
    """

    def __init__(self):
        self.a = set()
        self.r = set()

    @classmethod
    def from_dict(cls, set_dict):
        obj = cls()
        if set_dict:
            if 'a' in set_dict:
                obj.a = set(set_dict['a'])
            if 'r' in set_dict:
                obj.r = set(set_dict['r'])
        return obj

    def add(self, element):
        self.a.add(element)

    def remove(self, element):
        if element in self.a:
            self.r.add(element)
        else:
            raise TwoPhaseSetException('Attempted to delete non-existing element.')

    def lookup(self, element):
        return element in (self.a - self.r)

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise TwoPhaseSetException('Attempted to merge with different type.')
        self.a.update(other.a)
        self.r.update(other.r)

    def to_list(self):
        return list(self.a - self.r)

    def to_dict(self):
        return {
            'type': '2p-set',
            'a': list(self.a),
            'r': list(self.r)
        }
