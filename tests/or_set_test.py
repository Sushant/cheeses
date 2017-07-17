from context import crdt

import unittest

class ORSetTest(unittest.TestCase):
    def setUp(self):
        self.ors = crdt.ORSet()

    def test_initialization(self):
        self.assertEqual([], self.ors.to_list())

    def test_add(self):
        self.ors.add('foo')
        self.assertEqual(['foo'], self.ors.to_list())

    def test_adding_already_existing_element(self):
        self.ors.add('foo')
        self.ors.add('foo')
        self.assertEqual(['foo'], self.ors.to_list())

    def test_remove(self):
        self.ors.add('foo')
        self.ors.remove('foo')
        self.assertEqual([], self.ors.to_list())

    def test_removing_a_non_existing_element(self):
        self.ors.remove('foo')
        self.assertEqual([], self.ors.to_list())

    def test_removing_a_removed_element(self):
        self.ors.add('foo')
        self.ors.remove('foo')
        self.ors.remove('foo')
        self.assertEqual([], self.ors.to_list())

    def test_adding_a_removed_element(self):
        self.ors.add('foo')
        self.ors.remove('foo')
        self.ors.add('foo')
        self.assertEqual(['foo'], self.ors.to_list())

    def test_lookup(self):
        self.ors.add('foo')
        self.assertTrue(self.ors.lookup('foo'))

        self.ors.remove('foo')
        self.assertFalse(self.ors.lookup('foo'))

        self.ors.add('foo')
        self.assertTrue(self.ors.lookup('foo'))

        self.ors.remove('foo')
        self.ors.add('foo')
        self.assertTrue(self.ors.lookup('foo'))

    def test_lookup_non_existing_element(self):
        self.assertFalse(self.ors.lookup('foo'))

    def test_clone_returns_new_set(self):
        self.ors.add('foo')
        clone = self.ors.clone()
        self.assertEqual(['foo'], clone.to_list())

        clone.add('bar')
        self.assertEqual(['foo', 'bar'], clone.to_list())
        self.assertEqual(['foo'], self.ors.to_list())

    def test_merge_with_different_class(self):
        with self.assertRaises(crdt.ORSetException):
            self.ors.merge('foo')

    def test_merge_with_other_or_set(self):
        other = crdt.ORSet()
        other.add('foo')
        self.ors.add('foo')
        other.add('bar')
        self.ors.add('baz')
        other.remove('foo')
        self.ors.merge(other)
        self.assertItemsEqual(['foo', 'bar', 'baz'], self.ors.to_list())

        self.ors.add('foo')
        self.assertItemsEqual(['foo', 'bar', 'baz'], self.ors.to_list())
        self.assertEqual(['bar'], other.to_list())

if __name__ == '__main__':
    unittest.main()