import unittest2

from key import Key


class TestKey(unittest2.TestCase):

  def test_init_no_arguments(self):
    key = Key()
    self.assertEqual([{'kind': ''}], key.path())
    self.assertEqual('', key.kind())
    self.assertEqual(None, key.dataset())
    self.assertEqual(None, key.namespace())
