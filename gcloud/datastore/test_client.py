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


def _make_entity_pb(project, kind, integer_id, name=None, str_val=None):
    from gcloud.datastore._generated import entity_pb2
    from gcloud.datastore.helpers import _new_value_pb

    entity_pb = entity_pb2.Entity()
    entity_pb.key.partition_id.project_id = project
    path_element = entity_pb.key.path.add()
    path_element.kind = kind
    path_element.id = integer_id
    if name is not None and str_val is not None:
        value_pb = _new_value_pb(entity_pb, name)
        value_pb.string_value = str_val

    return entity_pb


class Test__get_gcd_project(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.datastore.client import _get_gcd_project
        return _get_gcd_project()

    def test_no_value(self):
        import os
        from gcloud._testing import _Monkey

        environ = {}
        with _Monkey(os, getenv=environ.get):
            project = self._callFUT()
            self.assertEqual(project, None)

    def test_value_set(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.datastore.client import GCD_DATASET

        MOCK_PROJECT = object()
        environ = {GCD_DATASET: MOCK_PROJECT}
        with _Monkey(os, getenv=environ.get):
            project = self._callFUT()
            self.assertEqual(project, MOCK_PROJECT)


class Test__determine_default_project(unittest2.TestCase):

    def _callFUT(self, project=None):
        from gcloud.datastore.client import (
            _determine_default_project)
        return _determine_default_project(project=project)

    def _determine_default_helper(self, gcd=None, fallback=None,
                                  project_called=None):
        from gcloud._testing import _Monkey
        from gcloud.datastore import client

        _callers = []

        def gcd_mock():
            _callers.append('gcd_mock')
            return gcd

        def fallback_mock(project=None):
            _callers.append(('fallback_mock', project))
            return fallback

        patched_methods = {
            '_get_gcd_project': gcd_mock,
            '_base_default_project': fallback_mock,
        }

        with _Monkey(client, **patched_methods):
            returned_project = self._callFUT(project_called)

        return returned_project, _callers

    def test_no_value(self):
        project, callers = self._determine_default_helper()
        self.assertEqual(project, None)
        self.assertEqual(callers, ['gcd_mock', ('fallback_mock', None)])

    def test_explicit(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(
            project_called=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, [])

    def test_gcd(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(gcd=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['gcd_mock'])

    def test_fallback(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(fallback=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['gcd_mock', ('fallback_mock', None)])


class TestClient(unittest2.TestCase):

    PROJECT = 'PROJECT'

    def setUp(self):
        KLASS = self._getTargetClass()
        self.original_cnxn_class = KLASS._connection_class
        KLASS._connection_class = _MockConnection

    def tearDown(self):
        KLASS = self._getTargetClass()
        KLASS._connection_class = self.original_cnxn_class

    def _getTargetClass(self):
        from gcloud.datastore.client import Client
        return Client

    def _makeOne(self, project=PROJECT, namespace=None,
                 credentials=None, http=None):
        return self._getTargetClass()(project=project,
                                      namespace=namespace,
                                      credentials=credentials,
                                      http=http)

    def test_ctor_w_project_no_environ(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import client as _MUT

        # Some environments (e.g. AppVeyor CI) run in GCE, so
        # this test would fail artificially.
        with _Monkey(_MUT, _base_default_project=lambda project: None):
            self.assertRaises(EnvironmentError, self._makeOne, None)

    def test_ctor_w_implicit_inputs(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import client as _MUT
        from gcloud import client as _base_client

        OTHER = 'other'
        creds = object()
        default_called = []

        def fallback_mock(project):
            default_called.append(project)
            return project or OTHER

        klass = self._getTargetClass()
        with _Monkey(_MUT,
                     _determine_default_project=fallback_mock):
            with _Monkey(_base_client,
                         get_credentials=lambda: creds):
                client = klass()
        self.assertEqual(client.project, OTHER)
        self.assertEqual(client.namespace, None)
        self.assertTrue(isinstance(client.connection, _MockConnection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is None)
        self.assertTrue(client.current_batch is None)
        self.assertTrue(client.current_transaction is None)
        self.assertEqual(default_called, [None])

    def test_ctor_w_explicit_inputs(self):
        OTHER = 'other'
        NAMESPACE = 'namespace'
        creds = object()
        http = object()
        client = self._makeOne(project=OTHER,
                               namespace=NAMESPACE,
                               credentials=creds,
                               http=http)
        self.assertEqual(client.project, OTHER)
        self.assertEqual(client.namespace, NAMESPACE)
        self.assertTrue(isinstance(client.connection, _MockConnection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)
        self.assertTrue(client.current_batch is None)
        self.assertEqual(list(client._batch_stack), [])

    def test__push_batch_and__pop_batch(self):
        creds = object()
        client = self._makeOne(credentials=creds)
        batch = client.batch()
        xact = client.transaction()
        client._push_batch(batch)
        self.assertEqual(list(client._batch_stack), [batch])
        self.assertTrue(client.current_batch is batch)
        self.assertTrue(client.current_transaction is None)
        client._push_batch(xact)
        self.assertTrue(client.current_batch is xact)
        self.assertTrue(client.current_transaction is xact)
        # list(_LocalStack) returns in reverse order.
        self.assertEqual(list(client._batch_stack), [xact, batch])
        self.assertTrue(client._pop_batch() is xact)
        self.assertEqual(list(client._batch_stack), [batch])
        self.assertTrue(client._pop_batch() is batch)
        self.assertEqual(list(client._batch_stack), [])

    def test_get_miss(self):
        _called_with = []

        def _get_multi(*args, **kw):
            _called_with.append((args, kw))
            return []

        creds = object()
        client = self._makeOne(credentials=creds)
        client.get_multi = _get_multi

        key = object()

        self.assertTrue(client.get(key) is None)

        self.assertEqual(_called_with[0][0], ())
        self.assertEqual(_called_with[0][1]['keys'], [key])
        self.assertTrue(_called_with[0][1]['missing'] is None)
        self.assertTrue(_called_with[0][1]['deferred'] is None)
        self.assertTrue(_called_with[0][1]['transaction'] is None)

    def test_get_hit(self):
        TXN_ID = '123'
        _called_with = []
        _entity = object()

        def _get_multi(*args, **kw):
            _called_with.append((args, kw))
            return [_entity]

        creds = object()
        client = self._makeOne(credentials=creds)
        client.get_multi = _get_multi

        key, missing, deferred = object(), [], []

        self.assertTrue(client.get(key, missing, deferred, TXN_ID) is _entity)

        self.assertEqual(_called_with[0][0], ())
        self.assertEqual(_called_with[0][1]['keys'], [key])
        self.assertTrue(_called_with[0][1]['missing'] is missing)
        self.assertTrue(_called_with[0][1]['deferred'] is deferred)
        self.assertEqual(_called_with[0][1]['transaction'], TXN_ID)

    def test_get_multi_no_keys(self):
        creds = object()
        client = self._makeOne(credentials=creds)
        results = client.get_multi([])
        self.assertEqual(results, [])

    def test_get_multi_miss(self):
        from gcloud.datastore.key import Key

        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._add_lookup_result()
        key = Key('Kind', 1234, project=self.PROJECT)
        results = client.get_multi([key])
        self.assertEqual(results, [])

    def test_get_multi_miss_w_missing(self):
        from gcloud.datastore._generated import entity_pb2
        from gcloud.datastore.key import Key

        KIND = 'Kind'
        ID = 1234

        # Make a missing entity pb to be returned from mock backend.
        missed = entity_pb2.Entity()
        missed.key.partition_id.project_id = self.PROJECT
        path_element = missed.key.path.add()
        path_element.kind = KIND
        path_element.id = ID

        creds = object()
        client = self._makeOne(credentials=creds)
        # Set missing entity on mock connection.
        client.connection._add_lookup_result(missing=[missed])

        key = Key(KIND, ID, project=self.PROJECT)
        missing = []
        entities = client.get_multi([key], missing=missing)
        self.assertEqual(entities, [])
        self.assertEqual([missed.key.to_protobuf() for missed in missing],
                         [key.to_protobuf()])

    def test_get_multi_w_missing_non_empty(self):
        from gcloud.datastore.key import Key

        creds = object()
        client = self._makeOne(credentials=creds)
        key = Key('Kind', 1234, project=self.PROJECT)

        missing = ['this', 'list', 'is', 'not', 'empty']
        self.assertRaises(ValueError, client.get_multi,
                          [key], missing=missing)

    def test_get_multi_w_deferred_non_empty(self):
        from gcloud.datastore.key import Key

        creds = object()
        client = self._makeOne(credentials=creds)
        key = Key('Kind', 1234, project=self.PROJECT)

        deferred = ['this', 'list', 'is', 'not', 'empty']
        self.assertRaises(ValueError, client.get_multi,
                          [key], deferred=deferred)

    def test_get_multi_miss_w_deferred(self):
        from gcloud.datastore.key import Key

        key = Key('Kind', 1234, project=self.PROJECT)

        # Set deferred entity on mock connection.
        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._add_lookup_result(deferred=[key.to_protobuf()])

        deferred = []
        entities = client.get_multi([key], deferred=deferred)
        self.assertEqual(entities, [])
        self.assertEqual([def_key.to_protobuf() for def_key in deferred],
                         [key.to_protobuf()])

    def test_get_multi_w_deferred_from_backend_but_not_passed(self):
        from gcloud.datastore._generated import entity_pb2
        from gcloud.datastore.entity import Entity
        from gcloud.datastore.key import Key

        key1 = Key('Kind', project=self.PROJECT)
        key1_pb = key1.to_protobuf()
        key2 = Key('Kind', 2345, project=self.PROJECT)
        key2_pb = key2.to_protobuf()

        entity1_pb = entity_pb2.Entity()
        entity1_pb.key.CopyFrom(key1_pb)
        entity2_pb = entity_pb2.Entity()
        entity2_pb.key.CopyFrom(key2_pb)

        creds = object()
        client = self._makeOne(credentials=creds)
        # mock up two separate requests
        client.connection._add_lookup_result([entity1_pb], deferred=[key2_pb])
        client.connection._add_lookup_result([entity2_pb])

        missing = []
        found = client.get_multi([key1, key2], missing=missing)
        self.assertEqual(len(found), 2)
        self.assertEqual(len(missing), 0)

        # Check the actual contents on the response.
        self.assertTrue(isinstance(found[0], Entity))
        self.assertEqual(found[0].key.path, key1.path)
        self.assertEqual(found[0].key.project, key1.project)

        self.assertTrue(isinstance(found[1], Entity))
        self.assertEqual(found[1].key.path, key2.path)
        self.assertEqual(found[1].key.project, key2.project)

        cw = client.connection._lookup_cw
        self.assertEqual(len(cw), 2)

        ds_id, k_pbs, eventual, tid = cw[0]
        self.assertEqual(ds_id, self.PROJECT)
        self.assertEqual(len(k_pbs), 2)
        self.assertEqual(key1_pb, k_pbs[0])
        self.assertEqual(key2_pb, k_pbs[1])
        self.assertFalse(eventual)
        self.assertTrue(tid is None)

        ds_id, k_pbs, eventual, tid = cw[1]
        self.assertEqual(ds_id, self.PROJECT)
        self.assertEqual(len(k_pbs), 1)
        self.assertEqual(key2_pb, k_pbs[0])
        self.assertFalse(eventual)
        self.assertTrue(tid is None)

    def test_get_multi_hit(self):
        from gcloud.datastore.key import Key

        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]

        # Make a found entity pb to be returned from mock backend.
        entity_pb = _make_entity_pb(self.PROJECT, KIND, ID, 'foo', 'Foo')

        # Make a connection to return the entity pb.
        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._add_lookup_result([entity_pb])

        key = Key(KIND, ID, project=self.PROJECT)
        result, = client.get_multi([key])
        new_key = result.key

        # Check the returned value is as expected.
        self.assertFalse(new_key is key)
        self.assertEqual(new_key.project, self.PROJECT)
        self.assertEqual(new_key.path, PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

    def test_get_multi_hit_w_transaction(self):
        from gcloud.datastore.key import Key

        TXN_ID = '123'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]

        # Make a found entity pb to be returned from mock backend.
        entity_pb = _make_entity_pb(self.PROJECT, KIND, ID, 'foo', 'Foo')

        # Make a connection to return the entity pb.
        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._add_lookup_result([entity_pb])

        key = Key(KIND, ID, project=self.PROJECT)
        txn = client.transaction()
        txn._id = TXN_ID
        result, = client.get_multi([key], transaction=txn)
        new_key = result.key

        # Check the returned value is as expected.
        self.assertFalse(new_key is key)
        self.assertEqual(new_key.project, self.PROJECT)
        self.assertEqual(new_key.path, PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

        cw = client.connection._lookup_cw
        self.assertEqual(len(cw), 1)
        _, _, _, transaction_id = cw[0]
        self.assertEqual(transaction_id, TXN_ID)

    def test_get_multi_hit_multiple_keys_same_project(self):
        from gcloud.datastore.key import Key

        KIND = 'Kind'
        ID1 = 1234
        ID2 = 2345

        # Make a found entity pb to be returned from mock backend.
        entity_pb1 = _make_entity_pb(self.PROJECT, KIND, ID1)
        entity_pb2 = _make_entity_pb(self.PROJECT, KIND, ID2)

        # Make a connection to return the entity pbs.
        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._add_lookup_result([entity_pb1, entity_pb2])

        key1 = Key(KIND, ID1, project=self.PROJECT)
        key2 = Key(KIND, ID2, project=self.PROJECT)
        retrieved1, retrieved2 = client.get_multi([key1, key2])

        # Check values match.
        self.assertEqual(retrieved1.key.path, key1.path)
        self.assertEqual(dict(retrieved1), {})
        self.assertEqual(retrieved2.key.path, key2.path)
        self.assertEqual(dict(retrieved2), {})

    def test_get_multi_hit_multiple_keys_different_project(self):
        from gcloud.datastore.key import Key

        PROJECT1 = 'PROJECT'
        PROJECT2 = 'PROJECT-ALT'

        # Make sure our IDs are actually different.
        self.assertNotEqual(PROJECT1, PROJECT2)

        key1 = Key('KIND', 1234, project=PROJECT1)
        key2 = Key('KIND', 1234, project=PROJECT2)

        creds = object()
        client = self._makeOne(credentials=creds)

        with self.assertRaises(ValueError):
            client.get_multi([key1, key2])

    def test_get_multi_max_loops(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import client as _MUT
        from gcloud.datastore.key import Key

        KIND = 'Kind'
        ID = 1234

        # Make a found entity pb to be returned from mock backend.
        entity_pb = _make_entity_pb(self.PROJECT, KIND, ID, 'foo', 'Foo')

        # Make a connection to return the entity pb.
        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._add_lookup_result([entity_pb])

        key = Key(KIND, ID, project=self.PROJECT)
        deferred = []
        missing = []
        with _Monkey(_MUT, _MAX_LOOPS=-1):
            result = client.get_multi([key], missing=missing,
                                      deferred=deferred)

        # Make sure we have no results, even though the connection has been
        # set up as in `test_hit` to return a single result.
        self.assertEqual(result, [])
        self.assertEqual(missing, [])
        self.assertEqual(deferred, [])

    def test_put(self):
        _called_with = []

        def _put_multi(*args, **kw):
            _called_with.append((args, kw))

        creds = object()
        client = self._makeOne(credentials=creds)
        client.put_multi = _put_multi
        entity = object()

        client.put(entity)

        self.assertEqual(_called_with[0][0], ())
        self.assertEqual(_called_with[0][1]['entities'], [entity])

    def test_put_multi_no_entities(self):
        creds = object()
        client = self._makeOne(credentials=creds)
        self.assertEqual(client.put_multi([]), None)

    def test_put_multi_w_single_empty_entity(self):
        # https://github.com/GoogleCloudPlatform/gcloud-python/issues/649
        from gcloud.datastore.entity import Entity

        creds = object()
        client = self._makeOne(credentials=creds)
        self.assertRaises(ValueError, client.put_multi, Entity())

    def test_put_multi_no_batch_w_partial_key(self):
        from gcloud.datastore.helpers import _property_tuples
        from gcloud.datastore.test_batch import _Entity
        from gcloud.datastore.test_batch import _Key
        from gcloud.datastore.test_batch import _KeyPB
        from gcloud.datastore.test_batch import _mutated_pb

        entity = _Entity(foo=u'bar')
        key = entity.key = _Key(self.PROJECT)
        key._id = None

        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._commit.append([_KeyPB(key)])

        result = client.put_multi([entity])
        self.assertTrue(result is None)

        self.assertEqual(len(client.connection._commit_cw), 1)
        (project,
         commit_req, transaction_id) = client.connection._commit_cw[0]
        self.assertEqual(project, self.PROJECT)

        mutated_entity = _mutated_pb(self, commit_req.mutations, 'insert')
        self.assertEqual(mutated_entity.key, key.to_protobuf())

        prop_list = list(_property_tuples(mutated_entity))
        self.assertTrue(len(prop_list), 1)
        name, value_pb = prop_list[0]
        self.assertEqual(name, 'foo')
        self.assertEqual(value_pb.string_value, u'bar')

        self.assertTrue(transaction_id is None)

    def test_put_multi_existing_batch_w_completed_key(self):
        from gcloud.datastore.helpers import _property_tuples
        from gcloud.datastore.test_batch import _Entity
        from gcloud.datastore.test_batch import _Key
        from gcloud.datastore.test_batch import _mutated_pb

        creds = object()
        client = self._makeOne(credentials=creds)
        entity = _Entity(foo=u'bar')
        key = entity.key = _Key(self.PROJECT)

        with _NoCommitBatch(client) as CURR_BATCH:
            result = client.put_multi([entity])

        self.assertEqual(result, None)
        mutated_entity = _mutated_pb(self, CURR_BATCH.mutations, 'upsert')
        self.assertEqual(mutated_entity.key, key.to_protobuf())

        prop_list = list(_property_tuples(mutated_entity))
        self.assertTrue(len(prop_list), 1)
        name, value_pb = prop_list[0]
        self.assertEqual(name, 'foo')
        self.assertEqual(value_pb.string_value, u'bar')

    def test_delete(self):
        _called_with = []

        def _delete_multi(*args, **kw):
            _called_with.append((args, kw))

        creds = object()
        client = self._makeOne(credentials=creds)
        client.delete_multi = _delete_multi
        key = object()

        client.delete(key)

        self.assertEqual(_called_with[0][0], ())
        self.assertEqual(_called_with[0][1]['keys'], [key])

    def test_delete_multi_no_keys(self):
        creds = object()
        client = self._makeOne(credentials=creds)
        result = client.delete_multi([])
        self.assertEqual(result, None)
        self.assertEqual(len(client.connection._commit_cw), 0)

    def test_delete_multi_no_batch(self):
        from gcloud.datastore.test_batch import _Key
        from gcloud.datastore.test_batch import _mutated_pb

        key = _Key(self.PROJECT)

        creds = object()
        client = self._makeOne(credentials=creds)
        client.connection._commit.append([])

        result = client.delete_multi([key])
        self.assertEqual(result, None)
        self.assertEqual(len(client.connection._commit_cw), 1)
        (project,
         commit_req, transaction_id) = client.connection._commit_cw[0]
        self.assertEqual(project, self.PROJECT)

        mutated_key = _mutated_pb(self, commit_req.mutations, 'delete')
        self.assertEqual(mutated_key, key.to_protobuf())
        self.assertTrue(transaction_id is None)

    def test_delete_multi_w_existing_batch(self):
        from gcloud.datastore.test_batch import _Key
        from gcloud.datastore.test_batch import _mutated_pb

        creds = object()
        client = self._makeOne(credentials=creds)
        key = _Key(self.PROJECT)

        with _NoCommitBatch(client) as CURR_BATCH:
            result = client.delete_multi([key])

        self.assertEqual(result, None)
        mutated_key = _mutated_pb(self, CURR_BATCH.mutations, 'delete')
        self.assertEqual(mutated_key, key._key)
        self.assertEqual(len(client.connection._commit_cw), 0)

    def test_delete_multi_w_existing_transaction(self):
        from gcloud.datastore.test_batch import _Key
        from gcloud.datastore.test_batch import _mutated_pb

        creds = object()
        client = self._makeOne(credentials=creds)
        key = _Key(self.PROJECT)

        with _NoCommitTransaction(client) as CURR_XACT:
            result = client.delete_multi([key])

        self.assertEqual(result, None)
        mutated_key = _mutated_pb(self, CURR_XACT.mutations, 'delete')
        self.assertEqual(mutated_key, key._key)
        self.assertEqual(len(client.connection._commit_cw), 0)

    def test_allocate_ids_w_partial_key(self):
        from gcloud.datastore.test_batch import _Key

        NUM_IDS = 2

        INCOMPLETE_KEY = _Key(self.PROJECT)
        INCOMPLETE_KEY._id = None

        creds = object()
        client = self._makeOne(credentials=creds)

        result = client.allocate_ids(INCOMPLETE_KEY, NUM_IDS)

        # Check the IDs returned.
        self.assertEqual([key._id for key in result], list(range(NUM_IDS)))

    def test_allocate_ids_with_completed_key(self):
        from gcloud.datastore.test_batch import _Key

        creds = object()
        client = self._makeOne(credentials=creds)

        COMPLETE_KEY = _Key(self.PROJECT)
        self.assertRaises(ValueError, client.allocate_ids, COMPLETE_KEY, 2)

    def test_key_w_project(self):
        KIND = 'KIND'
        ID = 1234

        creds = object()
        client = self._makeOne(credentials=creds)

        self.assertRaises(TypeError,
                          client.key, KIND, ID, project=self.PROJECT)

    def test_key_wo_project(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        ID = 1234

        creds = object()
        client = self._makeOne(credentials=creds)

        with _Monkey(MUT, Key=_Dummy):
            key = client.key(KIND, ID)

        self.assertTrue(isinstance(key, _Dummy))
        self.assertEqual(key.args, (KIND, ID))
        expected_kwargs = {
            'project': self.PROJECT,
            'namespace': None,
        }
        self.assertEqual(key.kwargs, expected_kwargs)

    def test_key_w_namespace(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        ID = 1234
        NAMESPACE = object()

        creds = object()
        client = self._makeOne(namespace=NAMESPACE, credentials=creds)

        with _Monkey(MUT, Key=_Dummy):
            key = client.key(KIND, ID)

        self.assertTrue(isinstance(key, _Dummy))
        expected_kwargs = {
            'project': self.PROJECT,
            'namespace': NAMESPACE,
        }
        self.assertEqual(key.kwargs, expected_kwargs)

    def test_key_w_namespace_collision(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        ID = 1234
        NAMESPACE1 = object()
        NAMESPACE2 = object()

        creds = object()
        client = self._makeOne(namespace=NAMESPACE1, credentials=creds)

        with _Monkey(MUT, Key=_Dummy):
            key = client.key(KIND, ID, namespace=NAMESPACE2)

        self.assertTrue(isinstance(key, _Dummy))
        expected_kwargs = {
            'project': self.PROJECT,
            'namespace': NAMESPACE2,
        }
        self.assertEqual(key.kwargs, expected_kwargs)

    def test_batch(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        creds = object()
        client = self._makeOne(credentials=creds)

        with _Monkey(MUT, Batch=_Dummy):
            batch = client.batch()

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, (client,))
        self.assertEqual(batch.kwargs, {})

    def test_transaction_defaults(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        creds = object()
        client = self._makeOne(credentials=creds)

        with _Monkey(MUT, Transaction=_Dummy):
            xact = client.transaction()

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, (client,))
        self.assertEqual(xact.kwargs, {})

    def test_query_w_client(self):
        KIND = 'KIND'

        creds = object()
        client = self._makeOne(credentials=creds)
        other = self._makeOne(credentials=object())

        self.assertRaises(TypeError, client.query, kind=KIND, client=other)

    def test_query_w_project(self):
        KIND = 'KIND'

        creds = object()
        client = self._makeOne(credentials=creds)

        self.assertRaises(TypeError,
                          client.query, kind=KIND, project=self.PROJECT)

    def test_query_w_defaults(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        creds = object()
        client = self._makeOne(credentials=creds)

        with _Monkey(MUT, Query=_Dummy):
            query = client.query()

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, (client,))
        expected_kwargs = {
            'project': self.PROJECT,
            'namespace': None,
        }
        self.assertEqual(query.kwargs, expected_kwargs)

    def test_query_explicit(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        NAMESPACE = 'NAMESPACE'
        ANCESTOR = object()
        FILTERS = [('PROPERTY', '==', 'VALUE')]
        PROJECTION = ['__key__']
        ORDER = ['PROPERTY']
        DISTINCT_ON = ['DISTINCT_ON']

        creds = object()
        client = self._makeOne(credentials=creds)

        with _Monkey(MUT, Query=_Dummy):
            query = client.query(
                kind=KIND,
                namespace=NAMESPACE,
                ancestor=ANCESTOR,
                filters=FILTERS,
                projection=PROJECTION,
                order=ORDER,
                distinct_on=DISTINCT_ON,
                )

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, (client,))
        kwargs = {
            'project': self.PROJECT,
            'kind': KIND,
            'namespace': NAMESPACE,
            'ancestor': ANCESTOR,
            'filters': FILTERS,
            'projection': PROJECTION,
            'order': ORDER,
            'distinct_on': DISTINCT_ON,
        }
        self.assertEqual(query.kwargs, kwargs)

    def test_query_w_namespace(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        NAMESPACE = object()

        creds = object()
        client = self._makeOne(namespace=NAMESPACE, credentials=creds)

        with _Monkey(MUT, Query=_Dummy):
            query = client.query(kind=KIND)

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, (client,))
        expected_kwargs = {
            'project': self.PROJECT,
            'namespace': NAMESPACE,
            'kind': KIND,
        }
        self.assertEqual(query.kwargs, expected_kwargs)

    def test_query_w_namespace_collision(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        NAMESPACE1 = object()
        NAMESPACE2 = object()

        creds = object()
        client = self._makeOne(namespace=NAMESPACE1, credentials=creds)

        with _Monkey(MUT, Query=_Dummy):
            query = client.query(kind=KIND, namespace=NAMESPACE2)

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, (client,))
        expected_kwargs = {
            'project': self.PROJECT,
            'namespace': NAMESPACE2,
            'kind': KIND,
        }
        self.assertEqual(query.kwargs, expected_kwargs)


class _Dummy(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class _MockConnection(object):

    def __init__(self, credentials=None, http=None):
        self.credentials = credentials
        self.http = http
        self._lookup_cw = []
        self._lookup = []
        self._commit_cw = []
        self._commit = []
        self._alloc_cw = []
        self._alloc = []
        self._index_updates = 0

    def _add_lookup_result(self, results=(), missing=(), deferred=()):
        self._lookup.append((list(results), list(missing), list(deferred)))

    def lookup(self, project, key_pbs, eventual=False, transaction_id=None):
        self._lookup_cw.append((project, key_pbs, eventual, transaction_id))
        triple, self._lookup = self._lookup[0], self._lookup[1:]
        results, missing, deferred = triple
        return results, missing, deferred

    def commit(self, project, commit_request, transaction_id):
        self._commit_cw.append((project, commit_request, transaction_id))
        response, self._commit = self._commit[0], self._commit[1:]
        return self._index_updates, response

    def allocate_ids(self, project, key_pbs):
        from gcloud.datastore.test_connection import _KeyProto
        self._alloc_cw.append((project, key_pbs))
        num_pbs = len(key_pbs)
        return [_KeyProto(i) for i in list(range(num_pbs))]


class _NoCommitBatch(object):

    def __init__(self, client):
        from gcloud.datastore.batch import Batch
        self._client = client
        self._batch = Batch(client)

    def __enter__(self):
        self._client._push_batch(self._batch)
        return self._batch

    def __exit__(self, *args):
        self._client._pop_batch()


class _NoCommitTransaction(object):

    def __init__(self, client, transaction_id='TRANSACTION'):
        from gcloud.datastore.transaction import Transaction
        self._client = client
        xact = self._transaction = Transaction(client)
        xact._id = transaction_id

    def __enter__(self):
        self._client._push_batch(self._transaction)
        return self._transaction

    def __exit__(self, *args):
        self._client._pop_batch()
