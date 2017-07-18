from context import crdt

import unittest

class GCounterTest(unittest.TestCase):
    def setUp(self):
        self.gc = crdt.GCounter()

    def test_initialization(self):
        self.assertEqual(0, self.gc.value())

    def test_increment(self):
        self.gc.increment(delta=3)
        self.assertEqual(3, self.gc.value())

    def test_increment_with_non_positive_delta(self):
        with self.assertRaises(crdt.GCounterException):
            self.gc.increment(delta=-5)

    def test_increment_with_multiple_nodes(self):
        self.gc.increment(node=1, delta=3)
        self.gc.increment(node=2, delta=3)
        self.gc.increment(node=3, delta=4)
        self.assertEqual(10, self.gc.value())

    def test_merge_with_different_class(self):
        with self.assertRaises(crdt.GCounterException):
            self.gc.merge('foo')

    def test_merge_with_other_g_counter(self):
        other = crdt.GCounter()
        other.increment(delta=1, node=1)
        self.gc.increment(delta=2, node=1)
        other.increment(delta=1, node=3)
        self.gc.increment(delta=2, node=2)
        other.increment(delta=1, node=3)
        self.gc.merge(other)
        self.assertEqual(6, self.gc.value())

        self.gc.increment(delta=1, node=1)
        self.assertEqual(7, self.gc.value())
        self.assertEqual(3, other.value())

if __name__ == '__main__':
    unittest.main()