import unittest2



class TestDataset(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.dataset import Dataset
        return Dataset

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_missing_dataset_id(self):
        self.assertRaises(TypeError, self._makeOne)

    def test_ctor_defaults(self):
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertEqual(dataset.connection(), None)

    def test_ctor_explicit(self):
        DATASET_ID = 'DATASET'
        CONNECTION = object()
        dataset = self._makeOne(DATASET_ID, CONNECTION)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertTrue(dataset.connection() is CONNECTION)

    def test_query_factory(self):
        from gcloud.datastore.query import Query
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        query = dataset.query()
        self.assertIsInstance(query, Query)
        self.assertTrue(query.dataset() is dataset)

    def test_entity_factory(self):
        from gcloud.datastore.entity import Entity
        DATASET_ID = 'DATASET'
        KIND = 'KIND'
        dataset = self._makeOne(DATASET_ID)
        entity = dataset.entity(KIND)
        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.kind(), KIND)

    def test_transaction_factory(self):
        from gcloud.datastore.transaction import Transaction
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        transaction = dataset.transaction()
        self.assertIsInstance(transaction, Transaction)
        self.assertTrue(transaction.dataset() is dataset)
