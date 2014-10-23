import unittest2


class TestKey(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.key import Key
        return Key

    def _makeOne(self, path=None, namespace=None, dataset_id=None):
        return self._getTargetClass()(path, namespace, dataset_id)

    def test_ctor_defaults(self):
        key = self._makeOne()
        self.assertEqual(key._dataset_id, None)
        self.assertEqual(key.namespace(), None)
        self.assertEqual(key.kind(), '')
        self.assertEqual(key.path(), [{'kind': ''}])

    def test_ctor_explicit(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._makeOne(_PATH, _NAMESPACE, _DATASET)
        self.assertEqual(key._dataset_id, _DATASET)
        self.assertEqual(key.namespace(), _NAMESPACE)
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.path(), _PATH)

    def test__clone(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._makeOne(_PATH, _NAMESPACE, _DATASET)
        clone = key._clone()
        self.assertEqual(clone._dataset_id, _DATASET)
        self.assertEqual(clone.namespace(), _NAMESPACE)
        self.assertEqual(clone.kind(), _KIND)
        self.assertEqual(clone.path(), _PATH)

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
        _DATASET = 'DATASET'
        key = self._makeOne(dataset_id=_DATASET)
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
        _PATH = [
            {'kind': _PARENT, 'name': _NAME},
            {'kind': _CHILD, 'id': _ID},
            {},
        ]
        key = self._makeOne(path=_PATH)
        pb = key.to_protobuf()
        elems = list(pb.path_element)
        self.assertEqual(len(elems), len(_PATH))
        self.assertEqual(elems[0].kind, _PARENT)
        self.assertEqual(elems[0].name, _NAME)
        self.assertEqual(elems[1].kind, _CHILD)
        self.assertEqual(elems[1].id, _ID)
        self.assertEqual(elems[2].kind, '')
        self.assertEqual(elems[2].name, '')
        self.assertEqual(elems[2].id, 0)

    def test_from_path_empty(self):
        key = self._getTargetClass().from_path()
        self.assertEqual(key._dataset_id, None)
        self.assertEqual(key.namespace(), None)
        self.assertEqual(key.kind(), '')
        self.assertEqual(key.path(), [{'kind': ''}])

    def test_from_path_single_element(self):
        self.assertRaises(ValueError, self._getTargetClass().from_path, 'abc')

    def test_from_path_three_elements(self):
        self.assertRaises(ValueError, self._getTargetClass().from_path,
                          'abc', 'def', 'ghi')

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
        expected_path = [
            {'kind': 'abc', 'name': 'def'},
            {'kind': 'ghi', 'id': 123},
        ]
        self.assertEqual(key.path(), expected_path)

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

    def test_namespace_setter(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        key = self._makeOne(path=_PATH, dataset_id=_DATASET)
        after = key.namespace(_NAMESPACE)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertEqual(after._dataset_id, _DATASET)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), _PATH)

    def test_path_setter(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND, 'name': _NAME}]
        key = self._makeOne(namespace=_NAMESPACE, dataset_id=_DATASET)
        after = key.path(_PATH)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertEqual(after._dataset_id, _DATASET)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), _PATH)

    def test_kind_getter_empty_path(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        key = self._makeOne(namespace=_NAMESPACE, dataset_id=_DATASET)
        key._path = ()  # edge case
        self.assertEqual(key.kind(), None)

    def test_kind_setter(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND_BEFORE = 'KIND_BEFORE'
        _KIND_AFTER = 'KIND_AFTER'
        _NAME = 'NAME'
        _PATH = [{'kind': _KIND_BEFORE, 'name': _NAME}]
        key = self._makeOne(_PATH, _NAMESPACE, _DATASET)
        after = key.kind(_KIND_AFTER)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertEqual(after._dataset_id, _DATASET)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), [{'kind': _KIND_AFTER, 'name': _NAME}])

    def test_id_getter_empty_path(self):
        key = self._makeOne()
        key._path = ()  # edge case
        self.assertEqual(key.id(), None)

    def test_id_setter(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID_BEFORE = 1234
        _ID_AFTER = 5678
        _PATH = [{'kind': _KIND, 'id': _ID_BEFORE}]
        key = self._makeOne(_PATH, _NAMESPACE, _DATASET)
        after = key.id(_ID_AFTER)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertEqual(after._dataset_id, _DATASET)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), [{'kind': _KIND, 'id': _ID_AFTER}])

    def test_name_getter_empty_path(self):
        key = self._makeOne()
        key._path = ()  # edge case
        self.assertEqual(key.name(), None)

    def test_name_setter(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _NAME_BEFORE = 'NAME_BEFORE'
        _NAME_AFTER = 'NAME_AFTER'
        _PATH = [{'kind': _KIND, 'name': _NAME_BEFORE}]
        key = self._makeOne(_PATH, _NAMESPACE, _DATASET)
        after = key.name(_NAME_AFTER)
        self.assertFalse(after is key)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertEqual(after._dataset_id, _DATASET)
        self.assertEqual(after.namespace(), _NAMESPACE)
        self.assertEqual(after.path(), [{'kind': _KIND, 'name': _NAME_AFTER}])

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

    def test_parent_default(self):
        key = self._makeOne()
        self.assertEqual(key.parent(), None)

    def test_parent_explicit_top_level(self):
        key = self._getTargetClass().from_path('abc', 'def')
        self.assertEqual(key.parent(), None)

    def test_parent_explicit_nested(self):
        key = self._getTargetClass().from_path('abc', 'def', 'ghi', 123)
        self.assertEqual(key.parent().path(), [{'kind': 'abc', 'name': 'def'}])
