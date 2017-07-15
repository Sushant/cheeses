import time
from collections import defaultdict

class LWWSet(object):
    def __init__(self):
        self.e = defaultdict(lambda : defaultdict(float))

    def add(self, element):
        self.e[element]['a'] = time.time()

    def remove(self, element):
        self.e[element]['r'] = time.time()

    def to_list(self):
        return [x for x in self.e.keys() if self.e[x]['a'] > self.e[x]['r']]

    def lookup(self, element):
        return self.e[element]['a'] > self.e[element]['r']
