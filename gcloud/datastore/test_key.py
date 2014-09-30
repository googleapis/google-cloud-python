import unittest2


class TestKey(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.key import Key
        return Key

    def _makeOne(self, dataset=None, namespace=None, path=None):
        return self._getTargetClass()(dataset, namespace, path)

    def _makePB(self, dataset_id=None, namespace=None, path=()):
        from gcloud.datastore.datastore_v1_pb2 import Key
        pb = Key()
        if dataset_id is not None:
            pb.partition_id.dataset_id = dataset_id
        if namespace is not None:
            pb.partition_id.namespace = namespace
        for elem in path:
            added = pb.path_element.add()
            if 'kind' in elem:
                added.kind = elem['kind']
            if 'id' in elem:
                added.id = elem['id']
            if 'name' in elem:
                added.name = elem['name']
        return pb

    def test_ctor_defaults(self):
        key = self._makeOne()
        self.assertEqual(key.dataset(), None)
        self.assertEqual(key.namespace(), None)
        self.assertEqual(key.kind(), '')
        self.assertEqual(key.path(), [{'kind': ''}])

    def test_ctor_explicit(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, _NAMESPACE, _PATH)
        self.assertTrue(key.dataset() is dataset)
        self.assertEqual(key.namespace(), _NAMESPACE)
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.path(), _PATH)

    def test__clone(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, _NAMESPACE, _PATH)
        clone = key._clone()
        self.assertTrue(clone.dataset() is dataset)
        self.assertEqual(clone.namespace(), _NAMESPACE)
        self.assertEqual(clone.kind(), _KIND)
        self.assertEqual(clone.path(), _PATH)

    def test_from_protobuf_empty_path_explicit_dataset(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        dataset = Dataset(_DATASET)
        pb = self._makePB()
        key = self._getTargetClass().from_protobuf(pb, dataset)
        self.assertTrue(key.dataset() is dataset)
        self.assertEqual(key.namespace(), None)
        self.assertEqual(key.kind(), '')
        self.assertEqual(key.path(), [{'kind': ''}])

    def test_from_protobuf_w_dataset_in_pb(self):
        _DATASET = 'DATASET'
        pb = self._makePB(_DATASET)
        key = self._getTargetClass().from_protobuf(pb)
        self.assertEqual(key.dataset().id(), _DATASET)

    def test_from_protobuf_w_namespace_in_pb_wo_dataset_passed(self):
        _NAMESPACE = 'NAMESPACE'
        pb = self._makePB(namespace=_NAMESPACE)
        key = self._getTargetClass().from_protobuf(pb)
        self.assertEqual(key.namespace(), _NAMESPACE)

    def test_from_protobuf_w_namespace_in_pb_w_dataset_passed(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        dataset = Dataset(_DATASET)
        pb = self._makePB(namespace=_NAMESPACE)
        key = self._getTargetClass().from_protobuf(pb, dataset)
        self.assertEqual(key.namespace(), None)

    def test_from_protobuf_w_path_in_pb(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        pb = self._makePB(_DATASET, _NAMESPACE)
        _PARENT = 'PARENT'
        _CHILD = 'CHILD'
        _ID = 1234
        _NAME = 'NAME'
        _PATH = [{'kind': _PARENT, 'name': _NAME}, {'kind': _CHILD, 'id': _ID}]
        pb = self._makePB(path=_PATH)
        key = self._getTargetClass().from_protobuf(pb)
        self.assertEqual(key.path(), _PATH)

    def test_to_protobuf_defaults(self):
        from gcloud.datastore.datastore_v1_pb2 import Key as KeyPB
        key = self._makeOne()
        pb = key.to_protobuf()
        self.assertTrue(isinstance(pb, KeyPB))
        self.assertEqual(pb.partition_id.dataset_id, '')
        self.assertEqual(pb.partition_id.namespace, '')
        elem, = list(pb.path_element)
        self.assertEqual(elem.kind, '')
        self.assertEqual(elem.name, '')
        self.assertEqual(elem.id, 0)

    def test_to_protobuf_w_explicit_dataset_no_prefix(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.dataset_id, 's~%s' % _DATASET)

    def test_to_protobuf_w_explicit_dataset_w_s_prefix(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 's~DATASET'
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.dataset_id, _DATASET)

    def test_to_protobuf_w_explicit_dataset_w_e_prefix(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'e~DATASET'
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.dataset_id, _DATASET)

    def test_to_protobuf_w_explicit_namespace(self):
        _NAMESPACE = 'NAMESPACE'
        key = self._makeOne(namespace=_NAMESPACE)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.namespace, _NAMESPACE)

    def test_to_protobuf_w_explicit_path(self):
        _PARENT = 'PARENT'
        _CHILD = 'CHILD'
        _ID = 1234
        _NAME = 'NAME'
        _PATH = [{'kind': _PARENT, 'name': _NAME}, {'kind': _CHILD, 'id': _ID}]
        key = self._makeOne(path=_PATH)
        pb = key.to_protobuf()
        elems = list(pb.path_element)
        self.assertEqual(elems[0].kind, _PARENT)
        self.assertEqual(elems[0].name, _NAME)
        self.assertEqual(elems[1].kind, _CHILD)
        self.assertEqual(elems[1].id, _ID)

    def test_from_path_empty(self):
        key = self._getTargetClass().from_path()
        self.assertEqual(key.dataset(), None)
        self.assertEqual(key.namespace(), None)
        self.assertEqual(key.kind(), '')
        self.assertEqual(key.path(), [{'kind': ''}])

    def test_from_path_single_element(self):
        # See https://github.com/GoogleCloudPlatform/gcloud-python/issues/134
        key = self._getTargetClass().from_path('abc')
        self.assertEqual(key.dataset(), None)
        self.assertEqual(key.namespace(), None)
        self.assertEqual(key.kind(), '') # XXX s.b. 'abc'?
        self.assertEqual(key.path(), [{'kind': ''}]) # XXX s.b. 'abc'?

    def test_from_path_two_elements_second_string(self):
        key = self._getTargetClass().from_path('abc', 'def')
        self.assertEqual(key.kind(), 'abc')
        self.assertEqual(key.path(), [{'kind': 'abc', 'name': 'def'}])

    def test_from_path_two_elements_second_int(self):
        key = self._getTargetClass().from_path('abc', 123)
        self.assertEqual(key.kind(), 'abc')
        self.assertEqual(key.path(), [{'kind': 'abc', 'id': 123}])

    def test_from_path_nested(self):
        key = self._getTargetClass().from_path('abc', 'def', 'ghi', 123)
        self.assertEqual(key.kind(), 'ghi')
        self.assertEqual(key.path(), [{'kind': 'abc', 'name': 'def'},
                                      {'kind': 'ghi', 'id': 123},
                                     ])

    def test_is_partial_no_name_or_id(self):
        key = self._makeOne()
        self.assertTrue(key.is_partial())

    def test_is_partial_w_id(self):
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._makeOne(path=_PATH)
        self.assertFalse(key.is_partial())

    def test_is_partial_w_name(self):
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        key = self._makeOne(path=_PATH)
        self.assertFalse(key.is_partial())

    def test_dataset_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(namespace=_NAMESPACE, path=_PATH)
        after = key.dataset(dataset)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), _PATH)

    def test_namespace_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, path=_PATH)
        after = key.namespace(_NAMESPACE)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), _PATH)

    def test_path_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, _NAMESPACE)
        after = key.path(_PATH)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), _PATH)

    def test_kind_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND_BEFORE = 'KIND_BEFORE'
        _KIND_AFTER = 'KIND_AFTER'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND_BEFORE, 'name': _NAME}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, _NAMESPACE, _PATH)
        after = key.kind(_KIND_AFTER)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), [{'kind': _KIND_AFTER, 'name': _NAME}])

    def test_name_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME_BEFORE = 'NAME_BEFORE'
        _NAME_AFTER = 'NAME_AFTER'
        _PATH = [{'kind': _KIND, 'name': _NAME_BEFORE}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, _NAMESPACE, _PATH)
        after = key.name(_NAME_AFTER)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), [{'kind': _KIND, 'name': _NAME_AFTER}])

    def test_id_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID_BEFORE = 1234
        _ID_AFTER = 5678
        _PATH = [{'kind': _KIND, 'id': _ID_BEFORE}]
        dataset = Dataset(_DATASET)
        key = self._makeOne(dataset, _NAMESPACE, _PATH)
        after = key.id(_ID_AFTER)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), [{'kind': _KIND, 'id': _ID_AFTER}])

    def test_id_or_name_no_name_or_id(self):
        key = self._makeOne()
        self.assertEqual(key.id_or_name(), None)

    def test_id_or_name_no_name_or_id_child(self):
        _KIND = 'KIND'
        _NAME = 'NAME'
        _ID = 5678
        _PATH = [{'kind': _KIND, 'id': _ID, 'name': _NAME}, {'kind': ''}]
        key = self._makeOne(path=_PATH)
        self.assertEqual(key.id_or_name(), None)

    def test_id_or_name_w_id_only(self):
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._makeOne(path=_PATH)
        self.assertEqual(key.id_or_name(), _ID)

    def test_id_or_name_w_id_and_name(self):
        _KIND = 'KIND'
        _ID = 1234
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'id': _ID, 'name': _NAME}]
        key = self._makeOne(path=_PATH)
        self.assertEqual(key.id_or_name(), _ID)

    def test_id_or_name_w_name_only(self):
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        key = self._makeOne(path=_PATH)
        self.assertEqual(key.id_or_name(), _NAME)

    def _ugh(self):
        protokey = key.to_protobuf()
        self.assertEqual(protokey.partition_id.dataset_id, _DATASET)
