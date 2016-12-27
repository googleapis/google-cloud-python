# Copyright 2014 Google Inc.
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

import unittest


class TestKey(unittest.TestCase):

    _DEFAULT_PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.key import Key
        return Key

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor_empty(self):
        self.assertRaises(ValueError, self._make_one)

    def test_ctor_no_project(self):
        klass = self._get_target_class()
        self.assertRaises(ValueError, klass, 'KIND')

    def test_ctor_w_explicit_project_empty_path(self):
        _PROJECT = 'PROJECT'
        self.assertRaises(ValueError, self._make_one, project=_PROJECT)

    def test_ctor_parent(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PROJECT = 'PROJECT-ALT'
        _PARENT_NAMESPACE = 'NAMESPACE'
        _CHILD_KIND = 'KIND2'
        _CHILD_ID = 2345
        _PATH = [
            {'kind': _PARENT_KIND, 'id': _PARENT_ID},
            {'kind': _CHILD_KIND, 'id': _CHILD_ID},
        ]
        parent_key = self._make_one(_PARENT_KIND, _PARENT_ID,
                                    project=_PARENT_PROJECT,
                                    namespace=_PARENT_NAMESPACE)
        key = self._make_one(_CHILD_KIND, _CHILD_ID, parent=parent_key)
        self.assertEqual(key.project, parent_key.project)
        self.assertEqual(key.namespace, parent_key.namespace)
        self.assertEqual(key.kind, _CHILD_KIND)
        self.assertEqual(key.path, _PATH)
        self.assertIs(key.parent, parent_key)

    def test_ctor_partial_parent(self):
        parent_key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        with self.assertRaises(ValueError):
            self._make_one('KIND2', 1234, parent=parent_key)

    def test_ctor_parent_bad_type(self):
        with self.assertRaises(AttributeError):
            self._make_one('KIND2', 1234, parent=('KIND1', 1234),
                           project=self._DEFAULT_PROJECT)

    def test_ctor_parent_bad_namespace(self):
        parent_key = self._make_one('KIND', 1234, namespace='FOO',
                                    project=self._DEFAULT_PROJECT)
        with self.assertRaises(ValueError):
            self._make_one('KIND2', 1234, namespace='BAR', parent=parent_key,
                           PROJECT=self._DEFAULT_PROJECT)

    def test_ctor_parent_bad_project(self):
        parent_key = self._make_one('KIND', 1234, project='FOO')
        with self.assertRaises(ValueError):
            self._make_one('KIND2', 1234, parent=parent_key,
                           project='BAR')

    def test_ctor_parent_empty_path(self):
        parent_key = self._make_one('KIND', 1234,
                                    project=self._DEFAULT_PROJECT)
        with self.assertRaises(ValueError):
            self._make_one(parent=parent_key)

    def test_ctor_explicit(self):
        _PROJECT = 'PROJECT-ALT'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._make_one(_KIND, _ID, namespace=_NAMESPACE,
                             project=_PROJECT)
        self.assertEqual(key.project, _PROJECT)
        self.assertEqual(key.namespace, _NAMESPACE)
        self.assertEqual(key.kind, _KIND)
        self.assertEqual(key.path, _PATH)

    def test_ctor_bad_kind(self):
        self.assertRaises(ValueError, self._make_one, object(),
                          project=self._DEFAULT_PROJECT)

    def test_ctor_bad_id_or_name(self):
        self.assertRaises(ValueError, self._make_one, 'KIND', object(),
                          project=self._DEFAULT_PROJECT)
        self.assertRaises(ValueError, self._make_one, 'KIND', None,
                          project=self._DEFAULT_PROJECT)
        self.assertRaises(ValueError, self._make_one, 'KIND', 10, 'KIND2',
                          None, project=self._DEFAULT_PROJECT)

    def test__clone(self):
        _PROJECT = 'PROJECT-ALT'
        _NAMESPACE = 'NAMESPACE'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = self._make_one(_KIND, _ID, namespace=_NAMESPACE,
                             project=_PROJECT)
        clone = key._clone()
        self.assertEqual(clone.project, _PROJECT)
        self.assertEqual(clone.namespace, _NAMESPACE)
        self.assertEqual(clone.kind, _KIND)
        self.assertEqual(clone.path, _PATH)

    def test__clone_with_parent(self):
        _PROJECT = 'PROJECT-ALT'
        _NAMESPACE = 'NAMESPACE'
        _KIND1 = 'PARENT'
        _KIND2 = 'KIND'
        _ID1 = 1234
        _ID2 = 2345
        _PATH = [{'kind': _KIND1, 'id': _ID1}, {'kind': _KIND2, 'id': _ID2}]

        parent = self._make_one(_KIND1, _ID1, namespace=_NAMESPACE,
                                project=_PROJECT)
        key = self._make_one(_KIND2, _ID2, parent=parent)
        self.assertIs(key.parent, parent)
        clone = key._clone()
        self.assertIs(clone.parent, key.parent)
        self.assertEqual(clone.project, _PROJECT)
        self.assertEqual(clone.namespace, _NAMESPACE)
        self.assertEqual(clone.path, _PATH)

    def test___eq_____ne___w_non_key(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _NAME = 'one'
        key = self._make_one(_KIND, _NAME, project=_PROJECT)
        self.assertFalse(key == object())
        self.assertTrue(key != object())

    def test___eq_____ne___two_incomplete_keys_same_kind(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        key1 = self._make_one(_KIND, project=_PROJECT)
        key2 = self._make_one(_KIND, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___incomplete_key_w_complete_key_same_kind(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._make_one(_KIND, project=_PROJECT)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___complete_key_w_incomplete_key_same_kind(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT)
        key2 = self._make_one(_KIND, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_different_ids(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID1 = 1234
        _ID2 = 2345
        key1 = self._make_one(_KIND, _ID1, project=_PROJECT)
        key2 = self._make_one(_KIND, _ID2, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_project(self):
        _PROJECT1 = 'PROJECT1'
        _PROJECT2 = 'PROJECT2'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT1)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_namespace(self):
        _PROJECT = 'PROJECT'
        _NAMESPACE1 = 'NAMESPACE1'
        _NAMESPACE2 = 'NAMESPACE2'
        _KIND = 'KIND'
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT,
                              namespace=_NAMESPACE1)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT,
                              namespace=_NAMESPACE2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_different_names(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _NAME1 = 'one'
        _NAME2 = 'two'
        key1 = self._make_one(_KIND, _NAME1, project=_PROJECT)
        key2 = self._make_one(_KIND, _NAME2, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._make_one(_KIND, _NAME, project=_PROJECT)
        key2 = self._make_one(_KIND, _NAME, project=_PROJECT)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_project(self):
        _PROJECT1 = 'PROJECT1'
        _PROJECT2 = 'PROJECT2'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._make_one(_KIND, _NAME, project=_PROJECT1)
        key2 = self._make_one(_KIND, _NAME, project=_PROJECT2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_namespace(self):
        _PROJECT = 'PROJECT'
        _NAMESPACE1 = 'NAMESPACE1'
        _NAMESPACE2 = 'NAMESPACE2'
        _KIND = 'KIND'
        _NAME = 'one'
        key1 = self._make_one(_KIND, _NAME, project=_PROJECT,
                              namespace=_NAMESPACE1)
        key2 = self._make_one(_KIND, _NAME, project=_PROJECT,
                              namespace=_NAMESPACE2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___hash___incomplete(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        key = self._make_one(_KIND, project=_PROJECT)
        self.assertNotEqual(hash(key),
                            hash(_KIND) + hash(_PROJECT) + hash(None))

    def test___hash___completed_w_id(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 1234
        key = self._make_one(_KIND, _ID, project=_PROJECT)
        self.assertNotEqual(hash(key),
                            hash(_KIND) + hash(_ID) +
                            hash(_PROJECT) + hash(None))

    def test___hash___completed_w_name(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _NAME = 'NAME'
        key = self._make_one(_KIND, _NAME, project=_PROJECT)
        self.assertNotEqual(hash(key),
                            hash(_KIND) + hash(_NAME) +
                            hash(_PROJECT) + hash(None))

    def test_completed_key_on_partial_w_id(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        _ID = 1234
        new_key = key.completed_key(_ID)
        self.assertIsNot(key, new_key)
        self.assertEqual(new_key.id, _ID)
        self.assertIsNone(new_key.name)

    def test_completed_key_on_partial_w_name(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        _NAME = 'NAME'
        new_key = key.completed_key(_NAME)
        self.assertIsNot(key, new_key)
        self.assertIsNone(new_key.id)
        self.assertEqual(new_key.name, _NAME)

    def test_completed_key_on_partial_w_invalid(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        self.assertRaises(ValueError, key.completed_key, object())

    def test_completed_key_on_complete(self):
        key = self._make_one('KIND', 1234, project=self._DEFAULT_PROJECT)
        self.assertRaises(ValueError, key.completed_key, 5678)

    def test_to_protobuf_defaults(self):
        from google.cloud.grpc.datastore.v1 import entity_pb2

        _KIND = 'KIND'
        key = self._make_one(_KIND, project=self._DEFAULT_PROJECT)
        pb = key.to_protobuf()
        self.assertIsInstance(pb, entity_pb2.Key)

        # Check partition ID.
        self.assertEqual(pb.partition_id.project_id, self._DEFAULT_PROJECT)
        # Unset values are False-y.
        self.assertEqual(pb.partition_id.namespace_id, '')

        # Check the element PB matches the partial key and kind.
        elem, = list(pb.path)
        self.assertEqual(elem.kind, _KIND)
        # Unset values are False-y.
        self.assertEqual(elem.name, '')
        # Unset values are False-y.
        self.assertEqual(elem.id, 0)

    def test_to_protobuf_w_explicit_project(self):
        _PROJECT = 'PROJECT-ALT'
        key = self._make_one('KIND', project=_PROJECT)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.project_id, _PROJECT)

    def test_to_protobuf_w_explicit_namespace(self):
        _NAMESPACE = 'NAMESPACE'
        key = self._make_one('KIND', namespace=_NAMESPACE,
                             project=self._DEFAULT_PROJECT)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.namespace_id, _NAMESPACE)

    def test_to_protobuf_w_explicit_path(self):
        _PARENT = 'PARENT'
        _CHILD = 'CHILD'
        _ID = 1234
        _NAME = 'NAME'
        key = self._make_one(_PARENT, _NAME, _CHILD, _ID,
                             project=self._DEFAULT_PROJECT)
        pb = key.to_protobuf()
        elems = list(pb.path)
        self.assertEqual(len(elems), 2)
        self.assertEqual(elems[0].kind, _PARENT)
        self.assertEqual(elems[0].name, _NAME)
        self.assertEqual(elems[1].kind, _CHILD)
        self.assertEqual(elems[1].id, _ID)

    def test_to_protobuf_w_no_kind(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        # Force the 'kind' to be unset. Maybe `to_protobuf` should fail
        # on this? The backend certainly will.
        key._path[-1].pop('kind')
        pb = key.to_protobuf()
        # Unset values are False-y.
        self.assertEqual(pb.path[0].kind, '')

    def test_is_partial_no_name_or_id(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        self.assertTrue(key.is_partial)

    def test_is_partial_w_id(self):
        _ID = 1234
        key = self._make_one('KIND', _ID, project=self._DEFAULT_PROJECT)
        self.assertFalse(key.is_partial)

    def test_is_partial_w_name(self):
        _NAME = 'NAME'
        key = self._make_one('KIND', _NAME, project=self._DEFAULT_PROJECT)
        self.assertFalse(key.is_partial)

    def test_id_or_name_no_name_or_id(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.id_or_name)

    def test_id_or_name_no_name_or_id_child(self):
        key = self._make_one('KIND1', 1234, 'KIND2',
                             project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.id_or_name)

    def test_id_or_name_w_id_only(self):
        _ID = 1234
        key = self._make_one('KIND', _ID, project=self._DEFAULT_PROJECT)
        self.assertEqual(key.id_or_name, _ID)

    def test_id_or_name_w_name_only(self):
        _NAME = 'NAME'
        key = self._make_one('KIND', _NAME, project=self._DEFAULT_PROJECT)
        self.assertEqual(key.id_or_name, _NAME)

    def test_parent_default(self):
        key = self._make_one('KIND', project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.parent)

    def test_parent_explicit_top_level(self):
        key = self._make_one('KIND', 1234, project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.parent)

    def test_parent_explicit_nested(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PATH = [{'kind': _PARENT_KIND, 'id': _PARENT_ID}]
        key = self._make_one(_PARENT_KIND, _PARENT_ID, 'KIND2',
                             project=self._DEFAULT_PROJECT)
        self.assertEqual(key.parent.path, _PARENT_PATH)

    def test_parent_multiple_calls(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PATH = [{'kind': _PARENT_KIND, 'id': _PARENT_ID}]
        key = self._make_one(_PARENT_KIND, _PARENT_ID, 'KIND2',
                             project=self._DEFAULT_PROJECT)
        parent = key.parent
        self.assertEqual(parent.path, _PARENT_PATH)
        new_parent = key.parent
        self.assertIs(parent, new_parent)
