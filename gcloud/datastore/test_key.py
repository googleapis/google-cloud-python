import unittest2

from dataset import Dataset
from key import Key


class TestKey(unittest2.TestCase):

  def test_init_no_arguments(self):
    key = Key()
    self.assertEqual([{'kind': ''}], key.path())
    self.assertEqual('', key.kind())
    self.assertEqual(None, key.dataset())
    self.assertEqual(None, key.namespace())

  def test_dataset_prefix(self):
    key = Key(dataset=Dataset('dset'))
    protokey = key.to_protobuf()
    self.assertEqual('s~dset', protokey.partition_id.dataset_id)

    key = Key(dataset=Dataset('s~dset'))
    protokey = key.to_protobuf()
    self.assertEqual('s~dset', protokey.partition_id.dataset_id)

    key = Key(dataset=Dataset('e~dset'))
    protokey = key.to_protobuf()
    self.assertEqual('e~dset', protokey.partition_id.dataset_id)
