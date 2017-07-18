from context import crdt

import unittest

class TwoPhaseSetTest(unittest.TestCase):
    def setUp(self):
        self.tp_set = crdt.TwoPhaseSet()

    def test_initialization(self):
        self.assertEqual([], self.tp_set.to_list())

    def test_add(self):
        self.tp_set.add('foo')
        self.assertEqual(['foo'], self.tp_set.to_list())

    def test_adding_already_existing_element(self):
        self.tp_set.add('foo')
        self.tp_set.add('foo')
        self.assertEqual(['foo'], self.tp_set.to_list())

    def test_remove(self):
        self.tp_set.add('foo')
        self.tp_set.remove('foo')
        self.assertEqual([], self.tp_set.to_list())

    def test_removing_a_non_existing_element(self):
        self.tp_set.add('foo')
        with self.assertRaises(crdt.TwoPhaseSetException):
            self.tp_set.remove('bar')

    def test_removing_a_removed_element(self):
        self.tp_set.add('foo')
        self.tp_set.remove('foo')
        self.tp_set.remove('foo')
        self.assertEqual([], self.tp_set.to_list())

    def test_adding_a_removed_element(self):
        self.tp_set.add('foo')
        self.tp_set.remove('foo')
        self.tp_set.add('foo')
        self.assertEqual([], self.tp_set.to_list())

    def test_lookup(self):
        self.tp_set.add('foo')
        self.assertTrue(self.tp_set.lookup('foo'))
        self.tp_set.remove('foo')
        self.assertFalse(self.tp_set.lookup('foo'))

    def test_merge_with_different_class(self):
        with self.assertRaises(crdt.TwoPhaseSetException):
            self.tp_set.merge('foo')

    def test_merge_with_other_2p_set(self):
        other = crdt.TwoPhaseSet()
        other.add('foo')
        self.tp_set.add('foo')
        other.remove('foo')
        self.tp_set.merge(other)
        self.assertEqual([], self.tp_set.to_list())

        self.tp_set.add('bar')
        self.assertEqual(['bar'], self.tp_set.to_list())
        self.assertEqual([], other.to_list())
        
if __name__ == '__main__':
    unittest.main()