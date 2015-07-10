# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2


class TestKey(unittest2.TestCase):

    _DEFAULT_DATASET = 'DATASET'

    def _getTargetClass(self):
        from gcloud.datastore.key import Key
        return Key

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_empty(self):
        self.assertRaises(ValueError, self._makeOne)

    def test_ctor_no_dataset_id(self):
        klass = self._getTargetClass()
        self.assertRaises(ValueError, klass, 'KIND')

    def test_ctor_w_explicit_dataset_id_empty_path(self):
        _DATASET = 'DATASET'
        self.assertRaises(ValueError, self._makeOne, dataset_id=_DATASET)

    def test_ctor_parent(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_DATASET = 'DATASET-ALT'
        _PARENT_NAMESPACE = 'NAMESPACE'
        _CHILD_KIND = 'KIND2'
        _CHILD_ID = 2345
        _PATH = [
            {'kind': _PARENT_KIND, 'id': _PARENT_ID},
            {'kind': _CHILD_KIND, 'id': _CHILD_ID},
        ]
        parent_key = self._makeOne(_PARENT_KIND, _PARENT_ID,
                                   dataset_id=_PARENT_DATASET,
                                   namespace=_PARENT_NAMESPACE)
        key = self._makeOne(_CHILD_KIND, _CHILD_ID, parent=parent_key)
        self.assertEqual(key.dataset_id, parent_key.dataset_id)
        self.assertEqual(key.namespace, parent_key.namespace)
        self.assertEqual(key.kind, _CHILD_KIND)
        self.assertEqual(key.path, _PATH)
        self.assertTrue(key.parent is parent_key)

    def test_ctor_partial_parent(self):
        parent_key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        with self.assertRaises(ValueError):
            self._makeOne('KIND2', 1234, parent=parent_key)

    def test_ctor_parent_bad_type(self):
        with self.assertRaises(AttributeError):
            self._makeOne('KIND2', 1234, parent=('KIND1', 1234),
                          dataset_id=self._DEFAULT_DATASET)

    def test_ctor_parent_bad_namespace(self):
        parent_key = self._makeOne('KIND', 1234, namespace='FOO',
                                   dataset_id=self._DEFAULT_DATASET)
        with self.assertRaises(ValueError):
            self._makeOne('KIND2', 1234, namespace='BAR', parent=parent_key,
                          dataset_id=self._DEFAULT_DATASET)

    def test_ctor_parent_bad_dataset_id(self):
        parent_key = self._makeOne('KIND', 1234, dataset_id='FOO')
        with self.assertRaises(ValueError):
            self._makeOne('KIND2', 1234, parent=parent_key,
                          dataset_id='BAR')

    def test_ctor_parent_empty_path(self):
        parent_key = self._makeOne('KIND', 1234,
                                   dataset_id=self._DEFAULT_DATASET)
        with self.assertRaises(ValueError):
            self._makeOne(parent=parent_key)

    def test_ctor_explicit(self):
        _DATASET = 'DATASET-ALT'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._makeOne(_KIND, _ID, namespace=_NAMESPACE,
                            dataset_id=_DATASET)
        self.assertEqual(key.dataset_id, _DATASET)
        self.assertEqual(key.namespace, _NAMESPACE)
        self.assertEqual(key.kind, _KIND)
        self.assertEqual(key.path, _PATH)

    def test_ctor_bad_kind(self):
        self.assertRaises(ValueError, self._makeOne, object(),
                          dataset_id=self._DEFAULT_DATASET)

    def test_ctor_bad_id_or_name(self):
        self.assertRaises(ValueError, self._makeOne, 'KIND', object(),
                          dataset_id=self._DEFAULT_DATASET)
        self.assertRaises(ValueError, self._makeOne, 'KIND', None,
                          dataset_id=self._DEFAULT_DATASET)
        self.assertRaises(ValueError, self._makeOne, 'KIND', 10, 'KIND2', None,
                          dataset_id=self._DEFAULT_DATASET)

    def test__clone(self):
        _DATASET = 'DATASET-ALT'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._makeOne(_KIND, _ID, namespace=_NAMESPACE,
                            dataset_id=_DATASET)
        clone = key._clone()
        self.assertEqual(clone.dataset_id, _DATASET)
        self.assertEqual(clone.namespace, _NAMESPACE)
        self.assertEqual(clone.kind, _KIND)
        self.assertEqual(clone.path, _PATH)

    def test__clone_with_parent(self):
        _DATASET = 'DATASET-ALT'
        _NAMESPACE = 'NAMESPACE'
        _KIND1 = 'PARENT'
        _KIND2 = 'KIND'
        _ID1 = 1234
        _ID2 = 2345
        _PATH = [{'kind': _KIND1, 'id': _ID1}, {'kind': _KIND2, 'id': _ID2}]

        parent = self._makeOne(_KIND1, _ID1, namespace=_NAMESPACE,
                               dataset_id=_DATASET)
        key = self._makeOne(_KIND2, _ID2, parent=parent)
        self.assertTrue(key.parent is parent)
        clone = key._clone()
        self.assertTrue(clone.parent is key.parent)
        self.assertEqual(clone.dataset_id, _DATASET)
        self.assertEqual(clone.namespace, _NAMESPACE)
        self.assertEqual(clone.path, _PATH)

    def test___eq_____ne___w_non_key(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _NAME = 'one'
        key = self._makeOne(_KIND, _NAME, dataset_id=_DATASET)
        self.assertFalse(key == object())
        self.assertTrue(key != object())

    def test___eq_____ne___two_incomplete_keys_same_kind(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        key1 = self._makeOne(_KIND, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, dataset_id=_DATASET)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___incomplete_key_w_complete_key_same_kind(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._makeOne(_KIND, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _ID, dataset_id=_DATASET)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___complete_key_w_incomplete_key_same_kind(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._makeOne(_KIND, _ID, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, dataset_id=_DATASET)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_different_ids(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID1 = 1234
        _ID2 = 2345
        key1 = self._makeOne(_KIND, _ID1, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _ID2, dataset_id=_DATASET)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._makeOne(_KIND, _ID, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _ID, dataset_id=_DATASET)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_dataset(self):
        _DATASET1 = 'DATASET1'
        _DATASET2 = 'DATASET2'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._makeOne(_KIND, _ID, dataset_id=_DATASET1)
        key2 = self._makeOne(_KIND, _ID, dataset_id=_DATASET2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_namespace(self):
        _DATASET = 'DATASET'
        _NAMESPACE1 = 'NAMESPACE1'
        _NAMESPACE2 = 'NAMESPACE2'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._makeOne(_KIND, _ID, dataset_id=_DATASET,
                             namespace=_NAMESPACE1)
        key2 = self._makeOne(_KIND, _ID, dataset_id=_DATASET,
                             namespace=_NAMESPACE2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_dataset_pfx(self):
        _DATASET = 'DATASET'
        _DATASET_W_PFX = 's~DATASET'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._makeOne(_KIND, _ID, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _ID, dataset_id=_DATASET_W_PFX)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_different_names(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _NAME1 = 'one'
        _NAME2 = 'two'
        key1 = self._makeOne(_KIND, _NAME1, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _NAME2, dataset_id=_DATASET)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_dataset(self):
        _DATASET1 = 'DATASET1'
        _DATASET2 = 'DATASET2'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET1)
        key2 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_namespace(self):
        _DATASET = 'DATASET'
        _NAMESPACE1 = 'NAMESPACE1'
        _NAMESPACE2 = 'NAMESPACE2'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET,
                             namespace=_NAMESPACE1)
        key2 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET,
                             namespace=_NAMESPACE2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_dataset_pfx(self):
        _DATASET = 'DATASET'
        _DATASET_W_PFX = 's~DATASET'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET)
        key2 = self._makeOne(_KIND, _NAME, dataset_id=_DATASET_W_PFX)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___hash___incomplete(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        key = self._makeOne(_KIND, dataset_id=_DATASET)
        self.assertNotEqual(hash(key),
                            hash(_KIND) + hash(_DATASET) + hash(None))

    def test___hash___completed_w_id(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        key = self._makeOne(_KIND, _ID, dataset_id=_DATASET)
        self.assertNotEqual(hash(key),
                            hash(_KIND) + hash(_ID) +
                            hash(_DATASET) + hash(None))

    def test___hash___completed_w_name(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _NAME = 'NAME'
        key = self._makeOne(_KIND, _NAME, dataset_id=_DATASET)
        self.assertNotEqual(hash(key),
                            hash(_KIND) + hash(_NAME) +
                            hash(_DATASET) + hash(None))

    def test_completed_key_on_partial_w_id(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        _ID = 1234
        new_key = key.completed_key(_ID)
        self.assertFalse(key is new_key)
        self.assertEqual(new_key.id, _ID)
        self.assertEqual(new_key.name, None)

    def test_completed_key_on_partial_w_name(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        _NAME = 'NAME'
        new_key = key.completed_key(_NAME)
        self.assertFalse(key is new_key)
        self.assertEqual(new_key.id, None)
        self.assertEqual(new_key.name, _NAME)

    def test_completed_key_on_partial_w_invalid(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        self.assertRaises(ValueError, key.completed_key, object())

    def test_completed_key_on_complete(self):
        key = self._makeOne('KIND', 1234, dataset_id=self._DEFAULT_DATASET)
        self.assertRaises(ValueError, key.completed_key, 5678)

    def test_to_protobuf_defaults(self):
        from gcloud.datastore._datastore_v1_pb2 import Key as KeyPB
        _KIND = 'KIND'
        key = self._makeOne(_KIND, dataset_id=self._DEFAULT_DATASET)
        pb = key.to_protobuf()
        self.assertTrue(isinstance(pb, KeyPB))

        # Check partition ID.
        self.assertEqual(pb.partition_id.dataset_id, self._DEFAULT_DATASET)
        self.assertEqual(pb.partition_id.namespace, '')
        self.assertFalse(pb.partition_id.HasField('namespace'))

        # Check the element PB matches the partial key and kind.
        elem, = list(pb.path_element)
        self.assertEqual(elem.kind, _KIND)
        self.assertEqual(elem.name, '')
        self.assertFalse(elem.HasField('name'))
        self.assertEqual(elem.id, 0)
        self.assertFalse(elem.HasField('id'))

    def test_to_protobuf_w_explicit_dataset_id(self):
        _DATASET = 'DATASET-ALT'
        key = self._makeOne('KIND', dataset_id=_DATASET)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.dataset_id, _DATASET)

    def test_to_protobuf_w_explicit_namespace(self):
        _NAMESPACE = 'NAMESPACE'
        key = self._makeOne('KIND', namespace=_NAMESPACE,
                            dataset_id=self._DEFAULT_DATASET)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.namespace, _NAMESPACE)

    def test_to_protobuf_w_explicit_path(self):
        _PARENT = 'PARENT'
        _CHILD = 'CHILD'
        _ID = 1234
        _NAME = 'NAME'
        key = self._makeOne(_PARENT, _NAME, _CHILD, _ID,
                            dataset_id=self._DEFAULT_DATASET)
        pb = key.to_protobuf()
        elems = list(pb.path_element)
        self.assertEqual(len(elems), 2)
        self.assertEqual(elems[0].kind, _PARENT)
        self.assertEqual(elems[0].name, _NAME)
        self.assertEqual(elems[1].kind, _CHILD)
        self.assertEqual(elems[1].id, _ID)

    def test_to_protobuf_w_no_kind(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        # Force the 'kind' to be unset. Maybe `to_protobuf` should fail
        # on this? The backend certainly will.
        key._path[-1].pop('kind')
        pb = key.to_protobuf()
        self.assertFalse(pb.path_element[0].HasField('kind'))

    def test_is_partial_no_name_or_id(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        self.assertTrue(key.is_partial)

    def test_is_partial_w_id(self):
        _ID = 1234
        key = self._makeOne('KIND', _ID, dataset_id=self._DEFAULT_DATASET)
        self.assertFalse(key.is_partial)

    def test_is_partial_w_name(self):
        _NAME = 'NAME'
        key = self._makeOne('KIND', _NAME, dataset_id=self._DEFAULT_DATASET)
        self.assertFalse(key.is_partial)

    def test_id_or_name_no_name_or_id(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.id_or_name, None)

    def test_id_or_name_no_name_or_id_child(self):
        key = self._makeOne('KIND1', 1234, 'KIND2',
                            dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.id_or_name, None)

    def test_id_or_name_w_id_only(self):
        _ID = 1234
        key = self._makeOne('KIND', _ID, dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.id_or_name, _ID)

    def test_id_or_name_w_name_only(self):
        _NAME = 'NAME'
        key = self._makeOne('KIND', _NAME, dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.id_or_name, _NAME)

    def test_parent_default(self):
        key = self._makeOne('KIND', dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.parent, None)

    def test_parent_explicit_top_level(self):
        key = self._makeOne('KIND', 1234, dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.parent, None)

    def test_parent_explicit_nested(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PATH = [{'kind': _PARENT_KIND, 'id': _PARENT_ID}]
        key = self._makeOne(_PARENT_KIND, _PARENT_ID, 'KIND2',
                            dataset_id=self._DEFAULT_DATASET)
        self.assertEqual(key.parent.path, _PARENT_PATH)

    def test_parent_multiple_calls(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PATH = [{'kind': _PARENT_KIND, 'id': _PARENT_ID}]
        key = self._makeOne(_PARENT_KIND, _PARENT_ID, 'KIND2',
                            dataset_id=self._DEFAULT_DATASET)
        parent = key.parent
        self.assertEqual(parent.path, _PARENT_PATH)
        new_parent = key.parent
        self.assertTrue(parent is new_parent)


class Test__dataset_ids_equal(unittest2.TestCase):

    def _callFUT(self, dataset_id1, dataset_id2):
        from gcloud.datastore.key import _dataset_ids_equal
        return _dataset_ids_equal(dataset_id1, dataset_id2)

    def test_identical_prefixed(self):
        self.assertTrue(self._callFUT('s~foo', 's~foo'))
        self.assertTrue(self._callFUT('e~bar', 'e~bar'))

    def test_different_prefixed(self):
        self.assertFalse(self._callFUT('s~foo', 's~bar'))
        self.assertFalse(self._callFUT('s~foo', 'e~foo'))

    def test_all_unprefixed(self):
        self.assertTrue(self._callFUT('foo', 'foo'))
        self.assertFalse(self._callFUT('foo', 'bar'))

    def test_unprefixed_with_prefixed(self):
        self.assertTrue(self._callFUT('foo', 's~foo'))
        self.assertTrue(self._callFUT('foo', 'e~foo'))
        self.assertFalse(self._callFUT('foo', 's~bar'))
