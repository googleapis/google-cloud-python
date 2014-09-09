import unittest2


_MARKER = object()
_DATASET_ID = 'DATASET'
_KIND = 'KIND'
_ID = 1234


class TestEntity(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.entity import Entity
        return Entity

    def _makeOne(self, dataset=_MARKER, kind=_KIND):
        from gcloud.datastore.dataset import Dataset
        klass = self._getTargetClass()
        if dataset is _MARKER:
            dataset = Dataset(_DATASET_ID)
        if kind is _MARKER:
            kind = _KIND
        return klass(dataset, kind)

    def test_ctor_defaults(self):
        klass = self._getTargetClass()
        entity = klass()
        self.assertEqual(entity.key(), None)
        self.assertEqual(entity.dataset(), None)
        self.assertEqual(entity.kind(), None)

    def test_ctor_explicit(self):
        from gcloud.datastore.dataset import Dataset
        dataset = Dataset(_DATASET_ID)
        entity = self._makeOne(dataset, _KIND)
        self.assertTrue(entity.dataset() is dataset)

    def test_key_getter(self):
        from gcloud.datastore.key import Key
        entity = self._makeOne()
        key = entity.key()
        self.assertIsInstance(key, Key)
        self.assertEqual(key.dataset().id(), _DATASET_ID)
        self.assertEqual(key.kind(), _KIND)

    def test_key_setter(self):
        entity = self._makeOne()
        key = object()
        entity.key(key)
        self.assertTrue(entity.key() is key)

    def test_from_key(self):
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        klass = self._getTargetClass()
        dataset = Dataset(_DATASET_ID)
        key = Key(dataset=dataset).kind(_KIND).id(_ID)
        entity = klass.from_key(key)
        self.assertTrue(entity.dataset() is dataset)
        self.assertEqual(entity.kind(), _KIND)
        key = entity.key()
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.id(), _ID)

    def test_from_protobuf(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.dataset import Dataset
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        entity_pb.key.path_element.add(kind=_KIND, id=_ID)
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        dataset = Dataset(_DATASET_ID)
        klass = self._getTargetClass()
        entity = klass.from_protobuf(entity_pb, dataset)
        self.assertTrue(entity.dataset() is dataset)
        self.assertEqual(entity.kind(), _KIND)
        self.assertEqual(entity['foo'], 'Foo')
        key = entity.key()
        self.assertTrue(key.dataset() is dataset)
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.id(), _ID)
