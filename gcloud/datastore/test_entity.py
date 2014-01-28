import unittest2

from gcloud.datastore.dataset import Dataset
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key


class TestEntity(unittest2.TestCase):

  def test_init_sets_proper_values(self):
    dataset = Dataset(id='test-dataset')
    entity = Entity(dataset, 'TestKind')
    self.assertEqual('test-dataset', entity.dataset().id())
    self.assertEqual('TestKind', entity.kind())

  def test_key(self):
    dataset = Dataset(id='test-dataset')
    entity = Entity(dataset, 'TestKind')
    self.assertIsInstance(entity.key(), Key)

  def test_from_key(self):
    key = Key(dataset=Dataset('test-dataset')).kind('TestKind').id(1234)
    entity = Entity.from_key(key)
    self.assertEqual('test-dataset', entity.dataset().id())
    self.assertEqual('TestKind', entity.key().kind())
    self.assertEqual(entity.key().kind(), entity.kind())
    self.assertEqual(1234, entity.key().id())
