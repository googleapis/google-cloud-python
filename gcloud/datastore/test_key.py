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

    def setUp(self):

        from gcloud.datastore import _implicit_environ
        self._replaced_dataset_id = _implicit_environ.DATASET_ID
        _implicit_environ.DATASET_ID = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.DATASET_ID = self._replaced_dataset_id

    def _getTargetClass(self):
        from gcloud.datastore.key import Key
        return Key

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _monkeyDatasetID(self, dataset_id=_DEFAULT_DATASET):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ
        return _Monkey(_implicit_environ, DATASET_ID=dataset_id)

    def test_ctor_empty(self):
        self.assertRaises(ValueError, self._makeOne)

    def test_ctor_no_dataset_id(self):
        klass = self._getTargetClass()
        with self._monkeyDatasetID(None):
            self.assertRaises(ValueError, klass, 'KIND')

    def test_ctor_w_implicit_dataset_id(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        with self._monkeyDatasetID(_DATASET):
            key = self._makeOne(_KIND)
        self.assertEqual(key.dataset_id, _DATASET)
        self.assertEqual(key.namespace, None)
        self.assertEqual(key.kind, _KIND)
        self.assertEqual(key.path, [{'kind': _KIND}])

    def test_ctor_w_implicit_dataset_id_empty_path(self):
        _DATASET = 'DATASET'
        with self._monkeyDatasetID(_DATASET):
            self.assertRaises(ValueError, self._makeOne)

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
        with self._monkeyDatasetID():
            key = self._makeOne(_CHILD_KIND, _CHILD_ID, parent=parent_key)
        self.assertEqual(key.dataset_id, parent_key.dataset_id)
        self.assertEqual(key.namespace, parent_key.namespace)
        self.assertEqual(key.kind, _CHILD_KIND)
        self.assertEqual(key.path, _PATH)
        self.assertTrue(key.parent is parent_key)

    def test_ctor_partial_parent(self):
        with self._monkeyDatasetID():
            parent_key = self._makeOne('KIND')
            with self.assertRaises(ValueError):
                self._makeOne('KIND2', 1234, parent=parent_key)

    def test_ctor_parent_bad_type(self):
        with self._monkeyDatasetID():
            with self.assertRaises(AttributeError):
                self._makeOne('KIND2', 1234, parent=('KIND1', 1234))

    def test_ctor_parent_bad_namespace(self):
        with self._monkeyDatasetID():
            parent_key = self._makeOne('KIND', 1234, namespace='FOO')
            with self.assertRaises(ValueError):
                self._makeOne(
                    'KIND2', 1234, namespace='BAR', parent=parent_key)

    def test_ctor_parent_bad_dataset_id(self):
        parent_key = self._makeOne('KIND', 1234, dataset_id='FOO')
        with self._monkeyDatasetID():
            with self.assertRaises(ValueError):
                self._makeOne('KIND2', 1234, dataset_id='BAR',
                              parent=parent_key)

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
        with self._monkeyDatasetID():
            self.assertRaises(ValueError, self._makeOne, object())

    def test_ctor_bad_id_or_name(self):
        with self._monkeyDatasetID():
            self.assertRaises(ValueError, self._makeOne, 'KIND', object())
            self.assertRaises(ValueError, self._makeOne, 'KIND', None)
            self.assertRaises(ValueError,
                              self._makeOne, 'KIND', 10, 'KIND2', None)

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

    def test_completed_key_on_partial_w_id(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        _ID = 1234
        new_key = key.completed_key(_ID)
        self.assertFalse(key is new_key)
        self.assertEqual(new_key.id, _ID)
        self.assertEqual(new_key.name, None)

    def test_completed_key_on_partial_w_name(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        _NAME = 'NAME'
        new_key = key.completed_key(_NAME)
        self.assertFalse(key is new_key)
        self.assertEqual(new_key.id, None)
        self.assertEqual(new_key.name, _NAME)

    def test_completed_key_on_partial_w_invalid(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        self.assertRaises(ValueError, key.completed_key, object())

    def test_completed_key_on_complete(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        self.assertRaises(ValueError, key.completed_key, 5678)

    def test_to_protobuf_defaults(self):
        from gcloud.datastore.datastore_v1_pb2 import Key as KeyPB
        _KIND = 'KIND'
        with self._monkeyDatasetID():
            key = self._makeOne(_KIND)
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
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', dataset_id=_DATASET)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.dataset_id, _DATASET)

    def test_to_protobuf_w_explicit_namespace(self):
        _NAMESPACE = 'NAMESPACE'
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', namespace=_NAMESPACE)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.namespace, _NAMESPACE)

    def test_to_protobuf_w_explicit_path(self):
        _PARENT = 'PARENT'
        _CHILD = 'CHILD'
        _ID = 1234
        _NAME = 'NAME'
        with self._monkeyDatasetID():
            key = self._makeOne(_PARENT, _NAME, _CHILD, _ID)
        pb = key.to_protobuf()
        elems = list(pb.path_element)
        self.assertEqual(len(elems), 2)
        self.assertEqual(elems[0].kind, _PARENT)
        self.assertEqual(elems[0].name, _NAME)
        self.assertEqual(elems[1].kind, _CHILD)
        self.assertEqual(elems[1].id, _ID)

    def test_to_protobuf_w_no_kind(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        # Force the 'kind' to be unset. Maybe `to_protobuf` should fail
        # on this? The backend certainly will.
        key._path[-1].pop('kind')
        pb = key.to_protobuf()
        self.assertFalse(pb.path_element[0].HasField('kind'))

    def test_get_explicit_connection_miss(self):
        from gcloud.datastore.test_connection import _Connection

        cnxn_lookup_result = []
        cnxn = _Connection(*cnxn_lookup_result)
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        entity = key.get(connection=cnxn)
        self.assertEqual(entity, None)

    def test_get_implicit_connection_miss(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.test_connection import _Connection

        cnxn_lookup_result = []
        cnxn = _Connection(*cnxn_lookup_result)
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        with _Monkey(_implicit_environ, CONNECTION=cnxn):
            entity = key.get()
        self.assertEqual(entity, None)

    def test_get_explicit_connection_hit(self):
        from gcloud.datastore import datastore_v1_pb2
        from gcloud.datastore.test_connection import _Connection

        KIND = 'KIND'
        ID = 1234

        # Make a bogus entity PB to be returned from fake Connection.
        entity_pb = datastore_v1_pb2.Entity()
        entity_pb.key.partition_id.dataset_id = self._DEFAULT_DATASET
        path_element = entity_pb.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'

        # Make fake connection.
        cnxn_lookup_result = [entity_pb]
        cnxn = _Connection(*cnxn_lookup_result)

        # Create key and look-up.
        with self._monkeyDatasetID():
            key = self._makeOne(KIND, ID)
        entity = key.get(connection=cnxn)
        self.assertEqual(entity.items(), [('foo', 'Foo')])
        self.assertTrue(entity.key is key)

    def test_get_no_connection(self):
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        with self.assertRaises(EnvironmentError):
            key.get()

    def test_delete_explicit_connection(self):
        from gcloud.datastore.test_connection import _Connection

        cnxn = _Connection()
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        result = key.delete(connection=cnxn)
        self.assertEqual(result, None)
        self.assertEqual(cnxn._called_dataset_id, self._DEFAULT_DATASET)
        self.assertEqual(cnxn._called_key_pbs, [key.to_protobuf()])

    def test_delete_implicit_connection(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.test_connection import _Connection

        cnxn = _Connection()
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        with _Monkey(_implicit_environ, CONNECTION=cnxn):
            result = key.delete()

        self.assertEqual(result, None)
        self.assertEqual(cnxn._called_dataset_id, self._DEFAULT_DATASET)
        self.assertEqual(cnxn._called_key_pbs, [key.to_protobuf()])

    def test_delete_no_connection(self):
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        with self.assertRaises(AttributeError):
            key.delete()

    def test_is_partial_no_name_or_id(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        self.assertTrue(key.is_partial)

    def test_is_partial_w_id(self):
        _ID = 1234
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', _ID)
        self.assertFalse(key.is_partial)

    def test_is_partial_w_name(self):
        _NAME = 'NAME'
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', _NAME)
        self.assertFalse(key.is_partial)

    def test_id_or_name_no_name_or_id(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        self.assertEqual(key.id_or_name, None)

    def test_id_or_name_no_name_or_id_child(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND1', 1234, 'KIND2')
        self.assertEqual(key.id_or_name, None)

    def test_id_or_name_w_id_only(self):
        _ID = 1234
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', _ID)
        self.assertEqual(key.id_or_name, _ID)

    def test_id_or_name_w_name_only(self):
        _NAME = 'NAME'
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', _NAME)
        self.assertEqual(key.id_or_name, _NAME)

    def test_parent_default(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND')
        self.assertEqual(key.parent, None)

    def test_parent_explicit_top_level(self):
        with self._monkeyDatasetID():
            key = self._makeOne('KIND', 1234)
        self.assertEqual(key.parent, None)

    def test_parent_explicit_nested(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PATH = [{'kind': _PARENT_KIND, 'id': _PARENT_ID}]
        with self._monkeyDatasetID():
            key = self._makeOne(_PARENT_KIND, _PARENT_ID, 'KIND2')
        self.assertEqual(key.parent.path, _PARENT_PATH)

    def test_parent_multiple_calls(self):
        _PARENT_KIND = 'KIND1'
        _PARENT_ID = 1234
        _PARENT_PATH = [{'kind': _PARENT_KIND, 'id': _PARENT_ID}]
        with self._monkeyDatasetID():
            key = self._makeOne(_PARENT_KIND, _PARENT_ID, 'KIND2')
        parent = key.parent
        self.assertEqual(parent.path, _PARENT_PATH)
        new_parent = key.parent
        self.assertTrue(parent is new_parent)
