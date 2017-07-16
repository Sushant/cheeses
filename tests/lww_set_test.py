from context import crdt

import unittest

class LWWSetTest(unittest.TestCase):
    def setUp(self):
        self.lww = crdt.LWWSet()

    def test_initialization(self):
        self.assertEqual([], self.lww.to_list())

    def test_add(self):
        self.lww.add('foo')
        self.assertEqual(['foo'], self.lww.to_list())
 
    def test_adding_already_existing_element(self):
        self.lww.add('foo')
        self.lww.add('foo')
        self.assertEqual(['foo'], self.lww.to_list())

    def test_remove(self):
        self.lww.add('foo')
        self.lww.remove('foo')
        self.assertEqual([], self.lww.to_list())

    def test_removing_a_non_existing_element(self):
        self.lww.remove('foo')
        self.assertEqual([], self.lww.to_list())

    def test_removing_a_removed_element(self):
        self.lww.add('foo')
        self.lww.remove('foo')
        self.lww.remove('foo')
        self.assertEqual([], self.lww.to_list())

    def test_adding_a_removed_element(self):
        self.lww.add('foo')
        self.lww.remove('foo')
        self.lww.add('foo')
        self.assertEqual(['foo'], self.lww.to_list())

    def test_lookup(self):
        self.lww.add('foo')
        self.assertTrue(self.lww.lookup('foo'))

        self.lww.remove('foo')
        self.assertFalse(self.lww.lookup('foo'))

        self.lww.add('foo')
        self.assertTrue(self.lww.lookup('foo'))

        self.lww.remove('foo')
        self.lww.add('foo')
        self.assertTrue(self.lww.lookup('foo'))

    def test_lookup_non_existing_element(self):
        self.assertFalse(self.lww.lookup('foo'))

    def test_clone_returns_new_set(self):
        self.lww.add('foo')
        clone = self.lww.clone()
        self.assertEqual(['foo'], clone.to_list())

        clone.add('bar')
        self.assertEqual(['foo', 'bar'], clone.to_list())
        self.assertEqual(['foo'], self.lww.to_list())

    def test_merge_with_different_class(self):
        with self.assertRaises(crdt.LWWSetException):
            self.lww.merge('foo')

    def test_merge_with_other_lww_set(self):
        other = crdt.LWWSet()
        other.add('foo')
        self.lww.add('foo')
        other.add('bar')
        self.lww.add('baz')
        other.remove('foo')
        self.lww.merge(other)
        self.assertItemsEqual(['bar', 'baz'], self.lww.to_list())

        self.lww.add('foo')
        self.assertItemsEqual(['foo', 'bar', 'baz'], self.lww.to_list())
        self.assertEqual(['bar'], other.to_list())

if __name__ == '__main__':
    unittest.main()