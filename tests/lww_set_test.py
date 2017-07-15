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

if __name__ == '__main__':
    unittest.main()