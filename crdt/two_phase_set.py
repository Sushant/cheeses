import copy
from sets import Set
from .exceptions import TwoPhaseSetException

class TwoPhaseSet(object):
    """
     Set where an element may be added and removed, but never added again thereafter.
     Adding or removing the same element twice has no effect, nor does adding an element
     that has already been removed.
    """

    def __init__(self):
        self.a = Set()
        self.r = Set()

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
        self.a.union_update(other.a)
        self.r.union_update(other.r)

    def clone(self):
        return copy.deepcopy(self)

    def to_list(self):
        return list(self.a - self.r)
