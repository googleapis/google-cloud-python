import unittest2

from gcloud.datastore.dataset import Dataset
from gcloud.datastore.entity import Entity
from gcloud.datastore.query import Query


class TestDataset(unittest2.TestCase):

  def test_init_id_required(self):
    with self.assertRaises(Exception):
      dataset = Dataset()

    dataset = Dataset('dataset-id-here')
    self.assertEqual('dataset-id-here', dataset.id())
    self.assertEqual(None, dataset.connection())

  def test_query_factory(self):
    dataset = Dataset('test')
    query = dataset.query()
    self.assertIsInstance(query, Query)
    self.assertEqual(dataset, query.dataset())

  def test_entity_factory(self):
    dataset = Dataset('test')
    entity = dataset.entity('TestKind')
    self.assertIsInstance(entity, Entity)
    self.assertEqual('TestKind', entity.kind())
