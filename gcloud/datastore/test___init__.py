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


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.datastore import get_connection
        return get_connection()

    def test_it(self):
        from gcloud import credentials
        from gcloud.datastore.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        self.assertTrue(client._get_app_default_called)


class Test_set_default_dataset(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_dataset = _implicit_environ.DATASET
        _implicit_environ.DATASET = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.DATASET = self._replaced_dataset

    def _callFUT(self, dataset_id=None):
        from gcloud.datastore import set_default_dataset
        return set_default_dataset(dataset_id=dataset_id)

    def _test_with_environ(self, environ, expected_result, dataset_id=None):
        import os
        from gcloud._testing import _Monkey
        from gcloud import datastore
        from gcloud.datastore import _implicit_environ

        # Check the environment is unset.
        self.assertEqual(_implicit_environ.DATASET, None)

        def custom_getenv(key):
            return environ.get(key)

        def custom_get_dataset(local_dataset_id):
            return local_dataset_id

        with _Monkey(os, getenv=custom_getenv):
            with _Monkey(datastore, get_dataset=custom_get_dataset):
                self._callFUT(dataset_id=dataset_id)

        self.assertEqual(_implicit_environ.DATASET, expected_result)

    def test_set_from_env_var(self):
        from gcloud.datastore import _DATASET_ENV_VAR_NAME

        # Make a custom getenv function to Monkey.
        DATASET = 'dataset'
        VALUES = {
            _DATASET_ENV_VAR_NAME: DATASET,
        }
        self._test_with_environ(VALUES, DATASET)

    def test_no_env_var_set(self):
        self._test_with_environ({}, None)

    def test_set_explicit(self):
        DATASET_ID = 'DATASET'
        self._test_with_environ({}, DATASET_ID, dataset_id=DATASET_ID)


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_connection = _implicit_environ.CONNECTION
        _implicit_environ.CONNECTION = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.CONNECTION = self._replaced_connection

    def _callFUT(self, connection=None):
        from gcloud.datastore import set_default_connection
        return set_default_connection(connection=connection)

    def test_set_explicit(self):
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)

    def test_set_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud import datastore
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)

        fake_cnxn = object()
        with _Monkey(datastore, get_connection=lambda: fake_cnxn):
            self._callFUT()

        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)


class Test_get_dataset(unittest2.TestCase):

    def _callFUT(self, dataset_id):
        from gcloud.datastore import get_dataset
        return get_dataset(dataset_id)

    def test_it(self):
        from gcloud import credentials
        from gcloud.datastore.connection import Connection
        from gcloud.datastore.dataset import Dataset
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        DATASET_ID = 'DATASET'
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT(DATASET_ID)
        self.assertTrue(isinstance(found, Dataset))
        self.assertTrue(isinstance(found.connection(), Connection))
        self.assertEqual(found.id(), DATASET_ID)
        self.assertTrue(client._get_app_default_called)


class Test_implicit_behavior(unittest2.TestCase):

    def test__require_dataset_value_unset(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud._testing import _Monkey

        with _Monkey(_implicit_environ, DATASET=None):
            with self.assertRaises(EnvironmentError):
                gcloud.datastore._require_dataset()

    def test__require_dataset_value_set(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud._testing import _Monkey

        FAKE_DATASET = object()
        with _Monkey(_implicit_environ, DATASET=FAKE_DATASET):
            stored_dataset = gcloud.datastore._require_dataset()
        self.assertTrue(stored_dataset is FAKE_DATASET)

    def test__require_connection_value_unset(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud._testing import _Monkey

        with _Monkey(_implicit_environ, CONNECTION=None):
            with self.assertRaises(EnvironmentError):
                gcloud.datastore._require_connection()

    def test__require_connection_value_set(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud._testing import _Monkey

        FAKE_CONNECTION = object()
        with _Monkey(_implicit_environ, CONNECTION=FAKE_CONNECTION):
            stored_connection = gcloud.datastore._require_connection()
        self.assertTrue(stored_connection is FAKE_CONNECTION)


class Test_get_entities_function(unittest2.TestCase):

    def _callFUT(self, keys, missing=None, deferred=None,
                 connection=None, dataset_id=None):
        from gcloud.datastore import get_entities
        return get_entities(keys, missing=missing, deferred=deferred,
                            connection=connection, dataset_id=dataset_id)

    def test_get_entities_miss(self):
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection

        DATASET_ID = 'DATASET'
        connection = _Connection()
        key = Key('Kind', 1234, dataset_id=DATASET_ID)
        results = self._callFUT([key], connection=connection,
                                dataset_id=DATASET_ID)
        self.assertEqual(results, [])

    def test_get_entities_miss_w_missing(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection

        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234

        # Make a missing entity pb to be returned from mock backend.
        missed = datastore_pb.Entity()
        missed.key.partition_id.dataset_id = DATASET_ID
        path_element = missed.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID

        # Set missing entity on mock connection.
        connection = _Connection()
        connection._missing = [missed]

        key = Key(KIND, ID, dataset_id=DATASET_ID)
        missing = []
        entities = self._callFUT([key], connection=connection,
                                 dataset_id=DATASET_ID, missing=missing)
        self.assertEqual(entities, [])
        self.assertEqual([missed.key().to_protobuf() for missed in missing],
                         [key.to_protobuf()])

    def test_get_entities_miss_w_deferred(self):
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection

        DATASET_ID = 'DATASET'
        key = Key('Kind', 1234, dataset_id=DATASET_ID)

        # Set deferred entity on mock connection.
        connection = _Connection()
        connection._deferred = [key.to_protobuf()]

        deferred = []
        entities = self._callFUT([key], connection=connection,
                                 dataset_id=DATASET_ID, deferred=deferred)
        self.assertEqual(entities, [])
        self.assertEqual([def_key.to_protobuf() for def_key in deferred],
                         [key.to_protobuf()])

    def _make_entity_pb(self, dataset_id, kind, integer_id, name, str_val):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb

        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = dataset_id
        path_element = entity_pb.key.path_element.add()
        path_element.kind = kind
        path_element.id = integer_id
        prop = entity_pb.property.add()
        prop.name = name
        prop.value.string_value = str_val

        return entity_pb

    def test_get_entities_hit(self):
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection

        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]

        # Make a found entity pb to be returned from mock backend.
        entity_pb = self._make_entity_pb(DATASET_ID, KIND, ID,
                                         'foo', 'Foo')

        # Make a connection to return the entity pb.
        connection = _Connection(entity_pb)

        key = Key(KIND, ID, dataset_id=DATASET_ID)
        result, = self._callFUT([key], connection=connection,
                                dataset_id=DATASET_ID)
        new_key = result.key()

        # Check the returned value is as expected.
        self.assertFalse(new_key is key)
        self.assertEqual(new_key.dataset_id, DATASET_ID)
        self.assertEqual(new_key.path, PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

    def test_get_entities_implicit(self):
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection
        from gcloud.datastore.test_entity import _Dataset
        from gcloud._testing import _Monkey

        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]

        # Make a found entity pb to be returned from mock backend.
        entity_pb = self._make_entity_pb(DATASET_ID, KIND, ID,
                                         'foo', 'Foo')

        # Make a connection to return the entity pb.
        CUSTOM_CONNECTION = _Connection(entity_pb)
        CUSTOM_DATASET = _Dataset()

        key = Key(KIND, ID, dataset_id=DATASET_ID)
        with _Monkey(_implicit_environ, DATASET=CUSTOM_DATASET,
                     CONNECTION=CUSTOM_CONNECTION):
            result, = self._callFUT([key])

        expected_called_with = {
            'dataset_id': DATASET_ID,
            'key_pbs': [key.to_protobuf()],
        }
        self.assertEqual(CUSTOM_CONNECTION._called_with, expected_called_with)

        new_key = result.key()
        # Check the returned value is as expected.
        self.assertFalse(new_key is key)
        self.assertEqual(new_key.dataset_id, DATASET_ID)
        self.assertEqual(new_key.path, PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')


class Test_allocate_ids_function(unittest2.TestCase):

    def _callFUT(self, incomplete_key, num_ids,
                 connection=None, dataset_id=None):
        from gcloud.datastore import allocate_ids
        return allocate_ids(incomplete_key, num_ids, connection=connection,
                            dataset_id=dataset_id)

    def test_allocate_ids(self):
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection

        DATASET_ID = 'DATASET'
        INCOMPLETE_KEY = Key('KIND', dataset_id=DATASET_ID)
        CONNECTION = _Connection()
        NUM_IDS = 2
        result = self._callFUT(INCOMPLETE_KEY, NUM_IDS,
                               connection=CONNECTION, dataset_id=DATASET_ID)

        # Check the IDs returned match.
        self.assertEqual([key.id for key in result], range(NUM_IDS))

        # Check connection is called correctly.
        self.assertEqual(CONNECTION._called_dataset_id, DATASET_ID)
        self.assertEqual(len(CONNECTION._called_key_pbs), NUM_IDS)

    def test_allocate_ids_implicit(self):
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection
        from gcloud.datastore.test_entity import _Dataset
        from gcloud._testing import _Monkey

        CUSTOM_DATASET = _Dataset()
        CUSTOM_CONNECTION = _Connection()
        NUM_IDS = 2
        with _Monkey(_implicit_environ, DATASET=CUSTOM_DATASET,
                     CONNECTION=CUSTOM_CONNECTION):
            INCOMPLETE_KEY = Key('KIND')
            result = self._callFUT(INCOMPLETE_KEY, NUM_IDS)

        # Check the IDs returned.
        self.assertEqual([key.id for key in result], range(NUM_IDS))

    def test_allocate_ids_with_complete(self):
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_connection import _Connection
        from gcloud.datastore.test_entity import _Dataset
        from gcloud._testing import _Monkey

        CUSTOM_DATASET = _Dataset()
        CUSTOM_CONNECTION = _Connection()
        with _Monkey(_implicit_environ, DATASET=CUSTOM_DATASET,
                     CONNECTION=CUSTOM_CONNECTION):
            COMPLETE_KEY = Key('KIND', 1234)
            self.assertRaises(ValueError, self._callFUT,
                              COMPLETE_KEY, 2)
