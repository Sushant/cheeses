from context import crdt

import unittest

class PNCounterTest(unittest.TestCase):
    def setUp(self):
        self.pnc = crdt.PNCounter()

    def test_initialization(self):
        self.assertEqual(0, self.pnc.value())

    def test_increment(self):
        self.pnc.increment(delta=3)
        self.assertEqual(3, self.pnc.value())

    def test_increment_with_non_positive_delta(self):
        with self.assertRaises(crdt.PNCounterException):
            self.pnc.increment(delta=-5)

    def test_increment_with_multiple_nodes(self):
        self.pnc.increment(node=1, delta=3)
        self.pnc.increment(node=2, delta=3)
        self.pnc.increment(node=3, delta=4)
        self.assertEqual(10, self.pnc.value())

    def test_decrement(self):
        self.pnc.decrement(delta=3)
        self.assertEqual(-3, self.pnc.value())

    def test_decrement_with_non_positive_delta(self):
        with self.assertRaises(crdt.PNCounterException):
            self.pnc.decrement(delta=-5)

    def test_decrement_with_multiple_nodes(self):
        self.pnc.decrement(node=1, delta=3)
        self.pnc.decrement(node=2, delta=3)
        self.pnc.decrement(node=3, delta=4)
        self.assertEqual(-10, self.pnc.value())

    def test_increment_decrement_with_multiple_nodes(self):
        self.pnc.increment(node=1, delta=3)
        self.pnc.increment(node=2, delta=3)
        self.pnc.decrement(node=2, delta=3)
        self.pnc.increment(node=3, delta=4)
        self.pnc.decrement(node=1, delta=3)
        self.pnc.decrement(node=3, delta=4)
        self.assertEqual(0, self.pnc.value())

    def test_merge_with_different_class(self):
        with self.assertRaises(crdt.PNCounterException):
            self.pnc.merge('foo')

    def test_merge_with_other_pn_counter(self):
        other = crdt.PNCounter()
        other.increment(delta=1, node=1)
        self.pnc.increment(delta=2, node=1)
        other.increment(delta=1, node=3)
        self.pnc.increment(delta=2, node=2)
        other.decrement(delta=1, node=3)
        self.pnc.merge(other)
        self.assertEqual(4, self.pnc.value())

        self.pnc.decrement(delta=1, node=1)
        self.assertEqual(3, self.pnc.value())
        self.assertEqual(1, other.value())

if __name__ == '__main__':
    unittest.main()