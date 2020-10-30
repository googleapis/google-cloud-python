# Copyright 2014 Google LLC
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

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_entity_pb(project, kind, integer_id, name=None, str_val=None):
    from google.cloud.datastore_v1.types import entity as entity_pb2
    from google.cloud.datastore.helpers import _new_value_pb

    entity_pb = entity_pb2.Entity()
    entity_pb.key.partition_id.project_id = project
    path_element = entity_pb._pb.key.path.add()
    path_element.kind = kind
    path_element.id = integer_id
    if name is not None and str_val is not None:
        value_pb = _new_value_pb(entity_pb, name)
        value_pb.string_value = str_val

    return entity_pb


class Test__get_gcd_project(unittest.TestCase):
    def _call_fut(self):
        from google.cloud.datastore.client import _get_gcd_project

        return _get_gcd_project()

    def test_no_value(self):
        environ = {}
        with mock.patch("os.getenv", new=environ.get):
            project = self._call_fut()
            self.assertIsNone(project)

    def test_value_set(self):
        from google.cloud.datastore.client import DATASTORE_DATASET

        MOCK_PROJECT = object()
        environ = {DATASTORE_DATASET: MOCK_PROJECT}
        with mock.patch("os.getenv", new=environ.get):
            project = self._call_fut()
            self.assertEqual(project, MOCK_PROJECT)


class Test__determine_default_project(unittest.TestCase):
    def _call_fut(self, project=None):
        from google.cloud.datastore.client import _determine_default_project

        return _determine_default_project(project=project)

    def _determine_default_helper(self, gcd=None, fallback=None, project_called=None):
        _callers = []

        def gcd_mock():
            _callers.append("gcd_mock")
            return gcd

        def fallback_mock(project=None):
            _callers.append(("fallback_mock", project))
            return fallback

        patch = mock.patch.multiple(
            "google.cloud.datastore.client",
            _get_gcd_project=gcd_mock,
            _base_default_project=fallback_mock,
        )
        with patch:
            returned_project = self._call_fut(project_called)

        return returned_project, _callers

    def test_no_value(self):
        project, callers = self._determine_default_helper()
        self.assertIsNone(project)
        self.assertEqual(callers, ["gcd_mock", ("fallback_mock", None)])

    def test_explicit(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(project_called=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, [])

    def test_gcd(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(gcd=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ["gcd_mock"])

    def test_fallback(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(fallback=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ["gcd_mock", ("fallback_mock", None)])


class TestClient(unittest.TestCase):

    PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.client import Client

        return Client

    def _make_one(
        self,
        project=PROJECT,
        namespace=None,
        credentials=None,
        client_info=None,
        client_options=None,
        _http=None,
        _use_grpc=None,
    ):
        return self._get_target_class()(
            project=project,
            namespace=namespace,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
            _http=_http,
            _use_grpc=_use_grpc,
        )

    def test_constructor_w_project_no_environ(self):
        # Some environments (e.g. AppVeyor CI) run in GCE, so
        # this test would fail artificially.
        patch = mock.patch(
            "google.cloud.datastore.client._base_default_project", return_value=None
        )
        with patch:
            self.assertRaises(EnvironmentError, self._make_one, None)

    def test_constructor_w_implicit_inputs(self):
        from google.cloud.datastore.client import _CLIENT_INFO
        from google.cloud.datastore.client import _DATASTORE_BASE_URL

        klass = self._get_target_class()
        other = "other"
        creds = _make_credentials()

        klass = self._get_target_class()
        patch1 = mock.patch(
            "google.cloud.datastore.client._determine_default_project",
            return_value=other,
        )
        patch2 = mock.patch("google.auth.default", return_value=(creds, None))

        with patch1 as _determine_default_project:
            with patch2 as default:
                client = klass()

        self.assertEqual(client.project, other)
        self.assertIsNone(client.namespace)
        self.assertIs(client._credentials, creds)
        self.assertIs(client._client_info, _CLIENT_INFO)
        self.assertIsNone(client._http_internal)
        self.assertIsNone(client._client_options)
        self.assertEqual(client.base_url, _DATASTORE_BASE_URL)

        self.assertIsNone(client.current_batch)
        self.assertIsNone(client.current_transaction)

        default.assert_called_once_with(scopes=klass.SCOPE,)
        _determine_default_project.assert_called_once_with(None)

    def test_constructor_w_explicit_inputs(self):
        from google.api_core.client_options import ClientOptions

        other = "other"
        namespace = "namespace"
        creds = _make_credentials()
        client_info = mock.Mock()
        client_options = ClientOptions("endpoint")
        http = object()
        client = self._make_one(
            project=other,
            namespace=namespace,
            credentials=creds,
            client_info=client_info,
            client_options=client_options,
            _http=http,
        )
        self.assertEqual(client.project, other)
        self.assertEqual(client.namespace, namespace)
        self.assertIs(client._credentials, creds)
        self.assertIs(client._client_info, client_info)
        self.assertIs(client._http_internal, http)
        self.assertIsNone(client.current_batch)
        self.assertIs(client._base_url, "endpoint")
        self.assertEqual(list(client._batch_stack), [])

    def test_constructor_use_grpc_default(self):
        import google.cloud.datastore.client as MUT

        project = "PROJECT"
        creds = _make_credentials()
        http = object()

        with mock.patch.object(MUT, "_USE_GRPC", new=True):
            client1 = self._make_one(project=project, credentials=creds, _http=http)
            self.assertTrue(client1._use_grpc)
            # Explicitly over-ride the environment.
            client2 = self._make_one(
                project=project, credentials=creds, _http=http, _use_grpc=False
            )
            self.assertFalse(client2._use_grpc)

        with mock.patch.object(MUT, "_USE_GRPC", new=False):
            client3 = self._make_one(project=project, credentials=creds, _http=http)
            self.assertFalse(client3._use_grpc)
            # Explicitly over-ride the environment.
            client4 = self._make_one(
                project=project, credentials=creds, _http=http, _use_grpc=True
            )
            self.assertTrue(client4._use_grpc)

    def test_constructor_w_emulator_w_creds(self):
        from google.cloud.datastore.client import DATASTORE_EMULATOR_HOST

        host = "localhost:1234"
        fake_environ = {DATASTORE_EMULATOR_HOST: host}
        project = "PROJECT"
        creds = _make_credentials()
        http = object()

        with mock.patch("os.environ", new=fake_environ):
            with self.assertRaises(ValueError):
                self._make_one(project=project, credentials=creds, _http=http)

    def test_constructor_w_emulator_wo_creds(self):
        from google.auth.credentials import AnonymousCredentials
        from google.cloud.datastore.client import DATASTORE_EMULATOR_HOST

        host = "localhost:1234"
        fake_environ = {DATASTORE_EMULATOR_HOST: host}
        project = "PROJECT"
        http = object()

        with mock.patch("os.environ", new=fake_environ):
            client = self._make_one(project=project, _http=http)

        self.assertEqual(client.base_url, "http://" + host)
        self.assertIsInstance(client._credentials, AnonymousCredentials)

    def test_base_url_property(self):
        from google.cloud.datastore.client import _DATASTORE_BASE_URL
        from google.api_core.client_options import ClientOptions

        alternate_url = "https://alias.example.com/"
        project = "PROJECT"
        creds = _make_credentials()
        http = object()
        client_options = ClientOptions()

        client = self._make_one(
            project=project,
            credentials=creds,
            _http=http,
            client_options=client_options,
        )
        self.assertEqual(client.base_url, _DATASTORE_BASE_URL)
        client.base_url = alternate_url
        self.assertEqual(client.base_url, alternate_url)

    def test_base_url_property_w_client_options(self):
        alternate_url = "https://alias.example.com/"
        project = "PROJECT"
        creds = _make_credentials()
        http = object()
        client_options = {"api_endpoint": "endpoint"}

        client = self._make_one(
            project=project,
            credentials=creds,
            _http=http,
            client_options=client_options,
        )
        self.assertEqual(client.base_url, "endpoint")
        client.base_url = alternate_url
        self.assertEqual(client.base_url, alternate_url)

    def test__datastore_api_property_already_set(self):
        client = self._make_one(
            project="prahj-ekt", credentials=_make_credentials(), _use_grpc=True
        )
        already = client._datastore_api_internal = object()
        self.assertIs(client._datastore_api, already)

    def test__datastore_api_property_gapic(self):
        client_info = mock.Mock()
        client = self._make_one(
            project="prahj-ekt",
            credentials=_make_credentials(),
            client_info=client_info,
            _http=object(),
            _use_grpc=True,
        )

        self.assertIsNone(client._datastore_api_internal)
        patch = mock.patch(
            "google.cloud.datastore.client.make_datastore_api",
            return_value=mock.sentinel.ds_api,
        )
        with patch as make_api:
            ds_api = client._datastore_api

        self.assertIs(ds_api, mock.sentinel.ds_api)
        self.assertIs(client._datastore_api_internal, mock.sentinel.ds_api)
        make_api.assert_called_once_with(client)

    def test__datastore_api_property_http(self):
        client_info = mock.Mock()
        client = self._make_one(
            project="prahj-ekt",
            credentials=_make_credentials(),
            client_info=client_info,
            _http=object(),
            _use_grpc=False,
        )

        self.assertIsNone(client._datastore_api_internal)
        patch = mock.patch(
            "google.cloud.datastore.client.HTTPDatastoreAPI",
            return_value=mock.sentinel.ds_api,
        )
        with patch as make_api:
            ds_api = client._datastore_api

        self.assertIs(ds_api, mock.sentinel.ds_api)
        self.assertIs(client._datastore_api_internal, mock.sentinel.ds_api)
        make_api.assert_called_once_with(client)

    def test__push_batch_and__pop_batch(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        batch = client.batch()
        xact = client.transaction()
        client._push_batch(batch)
        self.assertEqual(list(client._batch_stack), [batch])
        self.assertIs(client.current_batch, batch)
        self.assertIsNone(client.current_transaction)
        client._push_batch(xact)
        self.assertIs(client.current_batch, xact)
        self.assertIs(client.current_transaction, xact)
        # list(_LocalStack) returns in reverse order.
        self.assertEqual(list(client._batch_stack), [xact, batch])
        self.assertIs(client._pop_batch(), xact)
        self.assertEqual(list(client._batch_stack), [batch])
        self.assertIs(client._pop_batch(), batch)
        self.assertEqual(list(client._batch_stack), [])

    def test_get_miss(self):

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        get_multi = client.get_multi = mock.Mock(return_value=[])

        key = object()

        self.assertIsNone(client.get(key))

        get_multi.assert_called_once_with(
            keys=[key],
            missing=None,
            deferred=None,
            transaction=None,
            eventual=False,
            retry=None,
            timeout=None,
        )

    def test_get_hit(self):
        TXN_ID = "123"
        _called_with = []
        _entity = object()

        def _get_multi(*args, **kw):
            _called_with.append((args, kw))
            return [_entity]

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        client.get_multi = _get_multi

        key, missing, deferred = object(), [], []

        self.assertIs(client.get(key, missing, deferred, TXN_ID), _entity)

        self.assertEqual(_called_with[0][0], ())
        self.assertEqual(_called_with[0][1]["keys"], [key])
        self.assertIs(_called_with[0][1]["missing"], missing)
        self.assertIs(_called_with[0][1]["deferred"], deferred)
        self.assertEqual(_called_with[0][1]["transaction"], TXN_ID)

    def test_get_multi_no_keys(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        results = client.get_multi([])
        self.assertEqual(results, [])

    def test_get_multi_miss(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.key import Key

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        ds_api = _make_datastore_api()
        client._datastore_api_internal = ds_api

        key = Key("Kind", 1234, project=self.PROJECT)
        results = client.get_multi([key])
        self.assertEqual(results, [])

        read_options = datastore_pb2.ReadOptions()
        ds_api.lookup.assert_called_once_with(
            request={
                "project_id": self.PROJECT,
                "keys": [key.to_protobuf()],
                "read_options": read_options,
            }
        )

    def test_get_multi_miss_w_missing(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore.key import Key

        KIND = "Kind"
        ID = 1234

        # Make a missing entity pb to be returned from mock backend.
        missed = entity_pb2.Entity()
        missed.key.partition_id.project_id = self.PROJECT
        path_element = missed._pb.key.path.add()
        path_element.kind = KIND
        path_element.id = ID

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        # Set missing entity on mock connection.
        lookup_response = _make_lookup_response(missing=[missed._pb])
        ds_api = _make_datastore_api(lookup_response=lookup_response)
        client._datastore_api_internal = ds_api

        key = Key(KIND, ID, project=self.PROJECT)
        missing = []
        entities = client.get_multi([key], missing=missing)
        self.assertEqual(entities, [])
        key_pb = key.to_protobuf()
        self.assertEqual([missed.key.to_protobuf() for missed in missing], [key_pb._pb])

        read_options = datastore_pb2.ReadOptions()
        ds_api.lookup.assert_called_once_with(
            request={
                "project_id": self.PROJECT,
                "keys": [key_pb],
                "read_options": read_options,
            }
        )

    def test_get_multi_w_missing_non_empty(self):
        from google.cloud.datastore.key import Key

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        key = Key("Kind", 1234, project=self.PROJECT)

        missing = ["this", "list", "is", "not", "empty"]
        self.assertRaises(ValueError, client.get_multi, [key], missing=missing)

    def test_get_multi_w_deferred_non_empty(self):
        from google.cloud.datastore.key import Key

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        key = Key("Kind", 1234, project=self.PROJECT)

        deferred = ["this", "list", "is", "not", "empty"]
        self.assertRaises(ValueError, client.get_multi, [key], deferred=deferred)

    def test_get_multi_miss_w_deferred(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.key import Key

        key = Key("Kind", 1234, project=self.PROJECT)
        key_pb = key.to_protobuf()

        # Set deferred entity on mock connection.
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        lookup_response = _make_lookup_response(deferred=[key_pb])
        ds_api = _make_datastore_api(lookup_response=lookup_response)
        client._datastore_api_internal = ds_api

        deferred = []
        entities = client.get_multi([key], deferred=deferred)
        self.assertEqual(entities, [])
        self.assertEqual([def_key.to_protobuf() for def_key in deferred], [key_pb])

        read_options = datastore_pb2.ReadOptions()
        ds_api.lookup.assert_called_once_with(
            request={
                "project_id": self.PROJECT,
                "keys": [key_pb],
                "read_options": read_options,
            }
        )

    def test_get_multi_w_deferred_from_backend_but_not_passed(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.key import Key

        key1 = Key("Kind", project=self.PROJECT)
        key1_pb = key1.to_protobuf()
        key2 = Key("Kind", 2345, project=self.PROJECT)
        key2_pb = key2.to_protobuf()

        entity1_pb = entity_pb2.Entity()
        entity1_pb._pb.key.CopyFrom(key1_pb._pb)
        entity2_pb = entity_pb2.Entity()
        entity2_pb._pb.key.CopyFrom(key2_pb._pb)

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        # Mock up two separate requests. Using an iterable as side_effect
        # allows multiple return values.
        lookup_response1 = _make_lookup_response(
            results=[entity1_pb], deferred=[key2_pb]
        )
        lookup_response2 = _make_lookup_response(results=[entity2_pb])
        ds_api = _make_datastore_api()
        ds_api.lookup = mock.Mock(
            side_effect=[lookup_response1, lookup_response2], spec=[]
        )
        client._datastore_api_internal = ds_api

        missing = []
        found = client.get_multi([key1, key2], missing=missing)
        self.assertEqual(len(found), 2)
        self.assertEqual(len(missing), 0)

        # Check the actual contents on the response.
        self.assertIsInstance(found[0], Entity)
        self.assertEqual(found[0].key.path, key1.path)
        self.assertEqual(found[0].key.project, key1.project)

        self.assertIsInstance(found[1], Entity)
        self.assertEqual(found[1].key.path, key2.path)
        self.assertEqual(found[1].key.project, key2.project)

        self.assertEqual(ds_api.lookup.call_count, 2)
        read_options = datastore_pb2.ReadOptions()

        ds_api.lookup.assert_any_call(
            request={
                "project_id": self.PROJECT,
                "keys": [key2_pb],
                "read_options": read_options,
            },
        )

        ds_api.lookup.assert_any_call(
            request={
                "project_id": self.PROJECT,
                "keys": [key1_pb, key2_pb],
                "read_options": read_options,
            },
        )

    def test_get_multi_hit_w_retry_w_timeout(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.key import Key

        kind = "Kind"
        id_ = 1234
        path = [{"kind": kind, "id": id_}]
        retry = mock.Mock()
        timeout = 100000

        # Make a found entity pb to be returned from mock backend.
        entity_pb = _make_entity_pb(self.PROJECT, kind, id_, "foo", "Foo")

        # Make a connection to return the entity pb.
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        lookup_response = _make_lookup_response(results=[entity_pb])
        ds_api = _make_datastore_api(lookup_response=lookup_response)
        client._datastore_api_internal = ds_api

        key = Key(kind, id_, project=self.PROJECT)
        (result,) = client.get_multi([key], retry=retry, timeout=timeout)
        new_key = result.key

        # Check the returned value is as expected.
        self.assertIsNot(new_key, key)
        self.assertEqual(new_key.project, self.PROJECT)
        self.assertEqual(new_key.path, path)
        self.assertEqual(list(result), ["foo"])
        self.assertEqual(result["foo"], "Foo")

        read_options = datastore_pb2.ReadOptions()

        ds_api.lookup.assert_called_once_with(
            request={
                "project_id": self.PROJECT,
                "keys": [key.to_protobuf()],
                "read_options": read_options,
            },
            retry=retry,
            timeout=timeout,
        )

    def test_get_multi_hit_w_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.key import Key

        txn_id = b"123"
        kind = "Kind"
        id_ = 1234
        path = [{"kind": kind, "id": id_}]

        # Make a found entity pb to be returned from mock backend.
        entity_pb = _make_entity_pb(self.PROJECT, kind, id_, "foo", "Foo")

        # Make a connection to return the entity pb.
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        lookup_response = _make_lookup_response(results=[entity_pb])
        ds_api = _make_datastore_api(lookup_response=lookup_response)
        client._datastore_api_internal = ds_api

        key = Key(kind, id_, project=self.PROJECT)
        txn = client.transaction()
        txn._id = txn_id
        (result,) = client.get_multi([key], transaction=txn)
        new_key = result.key

        # Check the returned value is as expected.
        self.assertIsNot(new_key, key)
        self.assertEqual(new_key.project, self.PROJECT)
        self.assertEqual(new_key.path, path)
        self.assertEqual(list(result), ["foo"])
        self.assertEqual(result["foo"], "Foo")

        read_options = datastore_pb2.ReadOptions(transaction=txn_id)
        ds_api.lookup.assert_called_once_with(
            request={
                "project_id": self.PROJECT,
                "keys": [key.to_protobuf()],
                "read_options": read_options,
            }
        )

    def test_get_multi_hit_multiple_keys_same_project(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.key import Key

        kind = "Kind"
        id1 = 1234
        id2 = 2345

        # Make a found entity pb to be returned from mock backend.
        entity_pb1 = _make_entity_pb(self.PROJECT, kind, id1)
        entity_pb2 = _make_entity_pb(self.PROJECT, kind, id2)

        # Make a connection to return the entity pbs.
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        lookup_response = _make_lookup_response(results=[entity_pb1, entity_pb2])
        ds_api = _make_datastore_api(lookup_response=lookup_response)
        client._datastore_api_internal = ds_api

        key1 = Key(kind, id1, project=self.PROJECT)
        key2 = Key(kind, id2, project=self.PROJECT)
        retrieved1, retrieved2 = client.get_multi([key1, key2])

        # Check values match.
        self.assertEqual(retrieved1.key.path, key1.path)
        self.assertEqual(dict(retrieved1), {})
        self.assertEqual(retrieved2.key.path, key2.path)
        self.assertEqual(dict(retrieved2), {})

        read_options = datastore_pb2.ReadOptions()
        ds_api.lookup.assert_called_once_with(
            request={
                "project_id": self.PROJECT,
                "keys": [key1.to_protobuf(), key2.to_protobuf()],
                "read_options": read_options,
            }
        )

    def test_get_multi_hit_multiple_keys_different_project(self):
        from google.cloud.datastore.key import Key

        PROJECT1 = "PROJECT"
        PROJECT2 = "PROJECT-ALT"

        # Make sure our IDs are actually different.
        self.assertNotEqual(PROJECT1, PROJECT2)

        key1 = Key("KIND", 1234, project=PROJECT1)
        key2 = Key("KIND", 1234, project=PROJECT2)

        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        with self.assertRaises(ValueError):
            client.get_multi([key1, key2])

    def test_get_multi_max_loops(self):
        from google.cloud.datastore.key import Key

        kind = "Kind"
        id_ = 1234

        # Make a found entity pb to be returned from mock backend.
        entity_pb = _make_entity_pb(self.PROJECT, kind, id_, "foo", "Foo")

        # Make a connection to return the entity pb.
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        lookup_response = _make_lookup_response(results=[entity_pb])
        ds_api = _make_datastore_api(lookup_response=lookup_response)
        client._datastore_api_internal = ds_api

        key = Key(kind, id_, project=self.PROJECT)
        deferred = []
        missing = []

        patch = mock.patch("google.cloud.datastore.client._MAX_LOOPS", new=-1)
        with patch:
            result = client.get_multi([key], missing=missing, deferred=deferred)

        # Make sure we have no results, even though the connection has been
        # set up as in `test_hit` to return a single result.
        self.assertEqual(result, [])
        self.assertEqual(missing, [])
        self.assertEqual(deferred, [])
        ds_api.lookup.assert_not_called()

    def test_put(self):

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        put_multi = client.put_multi = mock.Mock()
        entity = mock.Mock()

        client.put(entity)

        put_multi.assert_called_once_with(entities=[entity], retry=None, timeout=None)

    def test_put_w_retry_w_timeout(self):

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        put_multi = client.put_multi = mock.Mock()
        entity = mock.Mock()
        retry = mock.Mock()
        timeout = 100000

        client.put(entity, retry=retry, timeout=timeout)

        put_multi.assert_called_once_with(
            entities=[entity], retry=retry, timeout=timeout
        )

    def test_put_multi_no_entities(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        self.assertIsNone(client.put_multi([]))

    def test_put_multi_w_single_empty_entity(self):
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/649
        from google.cloud.datastore.entity import Entity

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        self.assertRaises(ValueError, client.put_multi, Entity())

    def test_put_multi_no_batch_w_partial_key_w_retry_w_timeout(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.helpers import _property_tuples

        entity = _Entity(foo=u"bar")
        key = entity.key = _Key(_Key.kind, None)
        retry = mock.Mock()
        timeout = 100000

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        key_pb = _make_key(234)
        ds_api = _make_datastore_api(key_pb)
        client._datastore_api_internal = ds_api

        result = client.put_multi([entity], retry=retry, timeout=timeout)
        self.assertIsNone(result)

        self.assertEqual(ds_api.commit.call_count, 1)
        _, positional, keyword = ds_api.commit.mock_calls[0]

        self.assertEqual(len(positional), 0)

        self.assertEqual(len(keyword), 3)
        self.assertEqual(keyword["retry"], retry)
        self.assertEqual(keyword["timeout"], timeout)

        self.assertEqual(len(keyword["request"]), 4)
        self.assertEqual(keyword["request"]["project_id"], self.PROJECT)
        self.assertEqual(
            keyword["request"]["mode"],
            datastore_pb2.CommitRequest.Mode.NON_TRANSACTIONAL,
        )
        self.assertEqual(keyword["request"]["transaction"], None)
        mutations = keyword["request"]["mutations"]
        mutated_entity = _mutated_pb(self, mutations, "insert")
        self.assertEqual(mutated_entity.key, key.to_protobuf())

        prop_list = list(_property_tuples(mutated_entity))
        self.assertTrue(len(prop_list), 1)
        name, value_pb = prop_list[0]
        self.assertEqual(name, "foo")
        self.assertEqual(value_pb.string_value, u"bar")

    def test_put_multi_existing_batch_w_completed_key(self):
        from google.cloud.datastore.helpers import _property_tuples

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        entity = _Entity(foo=u"bar")
        key = entity.key = _Key()

        with _NoCommitBatch(client) as CURR_BATCH:
            result = client.put_multi([entity])

        self.assertIsNone(result)
        mutated_entity = _mutated_pb(self, CURR_BATCH.mutations, "upsert")
        self.assertEqual(mutated_entity.key, key.to_protobuf())

        prop_list = list(_property_tuples(mutated_entity))
        self.assertTrue(len(prop_list), 1)
        name, value_pb = prop_list[0]
        self.assertEqual(name, "foo")
        self.assertEqual(value_pb.string_value, u"bar")

    def test_delete(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        delete_multi = client.delete_multi = mock.Mock()
        key = mock.Mock()

        client.delete(key)

        delete_multi.assert_called_once_with(keys=[key], retry=None, timeout=None)

    def test_delete_w_retry_w_timeout(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        delete_multi = client.delete_multi = mock.Mock()
        key = mock.Mock()
        retry = mock.Mock()
        timeout = 100000

        client.delete(key, retry=retry, timeout=timeout)

        delete_multi.assert_called_once_with(keys=[key], retry=retry, timeout=timeout)

    def test_delete_multi_no_keys(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        client._datastore_api_internal = _make_datastore_api()

        result = client.delete_multi([])
        self.assertIsNone(result)
        client._datastore_api_internal.commit.assert_not_called()

    def test_delete_multi_no_batch_w_retry_w_timeout(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        key = _Key()
        retry = mock.Mock()
        timeout = 100000

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        ds_api = _make_datastore_api()
        client._datastore_api_internal = ds_api

        result = client.delete_multi([key], retry=retry, timeout=timeout)
        self.assertIsNone(result)

        self.assertEqual(ds_api.commit.call_count, 1)
        _, positional, keyword = ds_api.commit.mock_calls[0]

        self.assertEqual(len(positional), 0)

        self.assertEqual(len(keyword), 3)
        self.assertEqual(keyword["retry"], retry)
        self.assertEqual(keyword["timeout"], timeout)

        self.assertEqual(len(keyword["request"]), 4)
        self.assertEqual(keyword["request"]["project_id"], self.PROJECT)
        self.assertEqual(
            keyword["request"]["mode"],
            datastore_pb2.CommitRequest.Mode.NON_TRANSACTIONAL,
        )
        self.assertEqual(keyword["request"]["transaction"], None)
        mutations = keyword["request"]["mutations"]
        mutated_key = _mutated_pb(self, mutations, "delete")
        self.assertEqual(mutated_key, key.to_protobuf())

    def test_delete_multi_w_existing_batch(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        client._datastore_api_internal = _make_datastore_api()

        key = _Key()

        with _NoCommitBatch(client) as CURR_BATCH:
            result = client.delete_multi([key])

        self.assertIsNone(result)
        mutated_key = _mutated_pb(self, CURR_BATCH.mutations, "delete")
        self.assertEqual(mutated_key, key._key)
        client._datastore_api_internal.commit.assert_not_called()

    def test_delete_multi_w_existing_transaction(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        client._datastore_api_internal = _make_datastore_api()

        key = _Key()

        with _NoCommitTransaction(client) as CURR_XACT:
            result = client.delete_multi([key])

        self.assertIsNone(result)
        mutated_key = _mutated_pb(self, CURR_XACT.mutations, "delete")
        self.assertEqual(mutated_key, key._key)
        client._datastore_api_internal.commit.assert_not_called()

    def test_allocate_ids_w_partial_key(self):
        num_ids = 2

        incomplete_key = _Key(_Key.kind, None)

        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        allocated = mock.Mock(keys=[_KeyPB(i) for i in range(num_ids)], spec=["keys"])
        alloc_ids = mock.Mock(return_value=allocated, spec=[])
        ds_api = mock.Mock(allocate_ids=alloc_ids, spec=["allocate_ids"])
        client._datastore_api_internal = ds_api

        result = client.allocate_ids(incomplete_key, num_ids)

        # Check the IDs returned.
        self.assertEqual([key.id for key in result], list(range(num_ids)))

        expected_keys = [incomplete_key.to_protobuf()] * num_ids
        alloc_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys}
        )

    def test_allocate_ids_w_partial_key_w_retry_w_timeout(self):
        num_ids = 2

        incomplete_key = _Key(_Key.kind, None)
        retry = mock.Mock()
        timeout = 100000

        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        allocated = mock.Mock(keys=[_KeyPB(i) for i in range(num_ids)], spec=["keys"])
        alloc_ids = mock.Mock(return_value=allocated, spec=[])
        ds_api = mock.Mock(allocate_ids=alloc_ids, spec=["allocate_ids"])
        client._datastore_api_internal = ds_api

        result = client.allocate_ids(
            incomplete_key, num_ids, retry=retry, timeout=timeout
        )

        # Check the IDs returned.
        self.assertEqual([key.id for key in result], list(range(num_ids)))

        expected_keys = [incomplete_key.to_protobuf()] * num_ids
        alloc_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys},
            retry=retry,
            timeout=timeout,
        )

    def test_allocate_ids_w_completed_key(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        complete_key = _Key()
        self.assertRaises(ValueError, client.allocate_ids, complete_key, 2)

    def test_reserve_ids_sequential_w_completed_key(self):
        num_ids = 2
        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        complete_key = _Key()
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api
        self.assertTrue(not complete_key.is_partial)

        client.reserve_ids_sequential(complete_key, num_ids)

        reserved_keys = (
            _Key(_Key.kind, id)
            for id in range(complete_key.id, complete_key.id + num_ids)
        )
        expected_keys = [key.to_protobuf() for key in reserved_keys]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys}
        )

    def test_reserve_ids_sequential_w_completed_key_w_retry_w_timeout(self):
        num_ids = 2
        retry = mock.Mock()
        timeout = 100000

        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        complete_key = _Key()
        self.assertTrue(not complete_key.is_partial)
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api

        client.reserve_ids_sequential(
            complete_key, num_ids, retry=retry, timeout=timeout
        )

        reserved_keys = (
            _Key(_Key.kind, id)
            for id in range(complete_key.id, complete_key.id + num_ids)
        )
        expected_keys = [key.to_protobuf() for key in reserved_keys]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys},
            retry=retry,
            timeout=timeout,
        )

    def test_reserve_ids_sequential_w_completed_key_w_ancestor(self):
        num_ids = 2
        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        complete_key = _Key("PARENT", "SINGLETON", _Key.kind, 1234)
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api
        self.assertTrue(not complete_key.is_partial)

        client.reserve_ids_sequential(complete_key, num_ids)

        reserved_keys = (
            _Key("PARENT", "SINGLETON", _Key.kind, id)
            for id in range(complete_key.id, complete_key.id + num_ids)
        )
        expected_keys = [key.to_protobuf() for key in reserved_keys]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys}
        )

    def test_reserve_ids_sequential_w_partial_key(self):
        num_ids = 2
        incomplete_key = _Key(_Key.kind, None)
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids_sequential(incomplete_key, num_ids)

    def test_reserve_ids_sequential_w_wrong_num_ids(self):
        num_ids = "2"
        complete_key = _Key()
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids_sequential(complete_key, num_ids)

    def test_reserve_ids_sequential_w_non_numeric_key_name(self):
        num_ids = 2
        complete_key = _Key(_Key.kind, "batman")
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids_sequential(complete_key, num_ids)

    def test_reserve_ids_w_completed_key(self):
        num_ids = 2
        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        complete_key = _Key()
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api
        self.assertTrue(not complete_key.is_partial)

        client.reserve_ids(complete_key, num_ids)

        reserved_keys = (
            _Key(_Key.kind, id)
            for id in range(complete_key.id, complete_key.id + num_ids)
        )
        expected_keys = [key.to_protobuf() for key in reserved_keys]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys}
        )

    def test_reserve_ids_w_completed_key_w_retry_w_timeout(self):
        num_ids = 2
        retry = mock.Mock()
        timeout = 100000

        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        complete_key = _Key()
        self.assertTrue(not complete_key.is_partial)
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api

        client.reserve_ids(complete_key, num_ids, retry=retry, timeout=timeout)

        reserved_keys = (
            _Key(_Key.kind, id)
            for id in range(complete_key.id, complete_key.id + num_ids)
        )
        expected_keys = [key.to_protobuf() for key in reserved_keys]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys},
            retry=retry,
            timeout=timeout,
        )

    def test_reserve_ids_w_completed_key_w_ancestor(self):
        num_ids = 2
        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        complete_key = _Key("PARENT", "SINGLETON", _Key.kind, 1234)
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api
        self.assertTrue(not complete_key.is_partial)

        client.reserve_ids(complete_key, num_ids)

        reserved_keys = (
            _Key("PARENT", "SINGLETON", _Key.kind, id)
            for id in range(complete_key.id, complete_key.id + num_ids)
        )
        expected_keys = [key.to_protobuf() for key in reserved_keys]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys}
        )

    def test_reserve_ids_w_partial_key(self):
        num_ids = 2
        incomplete_key = _Key(_Key.kind, None)
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids(incomplete_key, num_ids)

    def test_reserve_ids_w_wrong_num_ids(self):
        num_ids = "2"
        complete_key = _Key()
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids(complete_key, num_ids)

    def test_reserve_ids_w_non_numeric_key_name(self):
        num_ids = 2
        complete_key = _Key(_Key.kind, "batman")
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids(complete_key, num_ids)

    def test_reserve_ids_multi(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds, _use_grpc=False)
        key1 = _Key(_Key.kind, "one")
        key2 = _Key(_Key.kind, "two")
        reserve_ids = mock.Mock()
        ds_api = mock.Mock(reserve_ids=reserve_ids, spec=["reserve_ids"])
        client._datastore_api_internal = ds_api

        client.reserve_ids_multi([key1, key2])

        expected_keys = [key1.to_protobuf(), key2.to_protobuf()]
        reserve_ids.assert_called_once_with(
            request={"project_id": self.PROJECT, "keys": expected_keys}
        )

    def test_reserve_ids_multi_w_partial_key(self):
        incomplete_key = _Key(_Key.kind, None)
        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        with self.assertRaises(ValueError):
            client.reserve_ids_multi([incomplete_key])

    def test_key_w_project(self):
        KIND = "KIND"
        ID = 1234

        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        self.assertRaises(TypeError, client.key, KIND, ID, project=self.PROJECT)

    def test_key_wo_project(self):
        kind = "KIND"
        id_ = 1234

        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Key", spec=["__call__"])
        with patch as mock_klass:
            key = client.key(kind, id_)
            self.assertIs(key, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                kind, id_, project=self.PROJECT, namespace=None
            )

    def test_key_w_namespace(self):
        kind = "KIND"
        id_ = 1234
        namespace = object()

        creds = _make_credentials()
        client = self._make_one(namespace=namespace, credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Key", spec=["__call__"])
        with patch as mock_klass:
            key = client.key(kind, id_)
            self.assertIs(key, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                kind, id_, project=self.PROJECT, namespace=namespace
            )

    def test_key_w_namespace_collision(self):
        kind = "KIND"
        id_ = 1234
        namespace1 = object()
        namespace2 = object()

        creds = _make_credentials()
        client = self._make_one(namespace=namespace1, credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Key", spec=["__call__"])
        with patch as mock_klass:
            key = client.key(kind, id_, namespace=namespace2)
            self.assertIs(key, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                kind, id_, project=self.PROJECT, namespace=namespace2
            )

    def test_batch(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Batch", spec=["__call__"])
        with patch as mock_klass:
            batch = client.batch()
            self.assertIs(batch, mock_klass.return_value)
            mock_klass.assert_called_once_with(client)

    def test_transaction_defaults(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        patch = mock.patch(
            "google.cloud.datastore.client.Transaction", spec=["__call__"]
        )
        with patch as mock_klass:
            xact = client.transaction()
            self.assertIs(xact, mock_klass.return_value)
            mock_klass.assert_called_once_with(client)

    def test_read_only_transaction_defaults(self):
        from google.cloud.datastore_v1.types import TransactionOptions

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        xact = client.transaction(read_only=True)
        self.assertEqual(
            xact._options, TransactionOptions(read_only=TransactionOptions.ReadOnly())
        )
        self.assertFalse(xact._options._pb.HasField("read_write"))
        self.assertTrue(xact._options._pb.HasField("read_only"))
        self.assertEqual(xact._options._pb.read_only, TransactionOptions.ReadOnly()._pb)

    def test_query_w_client(self):
        KIND = "KIND"

        creds = _make_credentials()
        client = self._make_one(credentials=creds)
        other = self._make_one(credentials=_make_credentials())

        self.assertRaises(TypeError, client.query, kind=KIND, client=other)

    def test_query_w_project(self):
        KIND = "KIND"

        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        self.assertRaises(TypeError, client.query, kind=KIND, project=self.PROJECT)

    def test_query_w_defaults(self):
        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Query", spec=["__call__"])
        with patch as mock_klass:
            query = client.query()
            self.assertIs(query, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                client, project=self.PROJECT, namespace=None
            )

    def test_query_explicit(self):
        kind = "KIND"
        namespace = "NAMESPACE"
        ancestor = object()
        filters = [("PROPERTY", "==", "VALUE")]
        projection = ["__key__"]
        order = ["PROPERTY"]
        distinct_on = ["DISTINCT_ON"]

        creds = _make_credentials()
        client = self._make_one(credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Query", spec=["__call__"])
        with patch as mock_klass:
            query = client.query(
                kind=kind,
                namespace=namespace,
                ancestor=ancestor,
                filters=filters,
                projection=projection,
                order=order,
                distinct_on=distinct_on,
            )
            self.assertIs(query, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                client,
                project=self.PROJECT,
                kind=kind,
                namespace=namespace,
                ancestor=ancestor,
                filters=filters,
                projection=projection,
                order=order,
                distinct_on=distinct_on,
            )

    def test_query_w_namespace(self):
        kind = "KIND"
        namespace = object()

        creds = _make_credentials()
        client = self._make_one(namespace=namespace, credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Query", spec=["__call__"])
        with patch as mock_klass:
            query = client.query(kind=kind)
            self.assertIs(query, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                client, project=self.PROJECT, namespace=namespace, kind=kind
            )

    def test_query_w_namespace_collision(self):
        kind = "KIND"
        namespace1 = object()
        namespace2 = object()

        creds = _make_credentials()
        client = self._make_one(namespace=namespace1, credentials=creds)

        patch = mock.patch("google.cloud.datastore.client.Query", spec=["__call__"])
        with patch as mock_klass:
            query = client.query(kind=kind, namespace=namespace2)
            self.assertIs(query, mock_klass.return_value)
            mock_klass.assert_called_once_with(
                client, project=self.PROJECT, namespace=namespace2, kind=kind
            )


class _NoCommitBatch(object):
    def __init__(self, client):
        from google.cloud.datastore.batch import Batch

        self._client = client
        self._batch = Batch(client)
        self._batch.begin()

    def __enter__(self):
        self._client._push_batch(self._batch)
        return self._batch

    def __exit__(self, *args):
        self._client._pop_batch()


class _NoCommitTransaction(object):
    def __init__(self, client, transaction_id="TRANSACTION"):
        from google.cloud.datastore.batch import Batch
        from google.cloud.datastore.transaction import Transaction

        self._client = client
        xact = self._transaction = Transaction(client)
        xact._id = transaction_id
        Batch.begin(xact)

    def __enter__(self):
        self._client._push_batch(self._transaction)
        return self._transaction

    def __exit__(self, *args):
        self._client._pop_batch()


class _Entity(dict):
    key = None
    exclude_from_indexes = ()
    _meanings = {}


class _Key(object):
    kind = "KIND"
    id = 1234
    name = None
    _project = project = "PROJECT"
    _namespace = None

    _key = "KEY"
    _path = None
    _stored = None

    def __init__(self, *flat_path, **kwargs):
        if flat_path:
            self._flat_path = flat_path
            self.kind = flat_path[-2]
            id_or_name = flat_path[-1]
            if isinstance(id_or_name, int):
                self.id = id_or_name
            else:
                self.id = None
                self.name = id_or_name

        else:
            self._flat_path = [self.kind, self.id]

        self.__dict__.update(kwargs)
        self._kw_args = kwargs

    @property
    def is_partial(self):
        return self.id is None and self.name is None

    def to_protobuf(self):
        from google.cloud.datastore_v1.types import entity as entity_pb2

        key = self._key = entity_pb2.Key()

        path = self._flat_path
        while path:
            element = key._pb.path.add()
            kind, id_or_name = path[:2]
            element.kind = kind
            if isinstance(id_or_name, int):
                element.id = id_or_name
            elif id_or_name is not None:
                element.name = id_or_name

            path = path[2:]

        return key

    def completed_key(self, new_id):
        assert self.is_partial

        path = list(self._flat_path)
        path[-1] = new_id

        key_class = type(self)
        new_key = key_class(*path, **self._kw_args)
        return new_key


class _PathElementPB(object):
    def __init__(self, id_):
        self.id = id_


class _KeyPB(object):
    def __init__(self, id_):
        self.path = [_PathElementPB(id_)]


def _assert_num_mutations(test_case, mutation_pb_list, num_mutations):
    test_case.assertEqual(len(mutation_pb_list), num_mutations)


def _mutated_pb(test_case, mutation_pb_list, mutation_type):
    # Make sure there is only one mutation.
    _assert_num_mutations(test_case, mutation_pb_list, 1)

    # We grab the only mutation.
    mutated_pb = mutation_pb_list[0]
    # Then check if it is the correct type.
    test_case.assertEqual(mutated_pb._pb.WhichOneof("operation"), mutation_type)

    return getattr(mutated_pb, mutation_type)


def _make_key(id_):
    from google.cloud.datastore_v1.types import entity as entity_pb2

    key = entity_pb2.Key()
    elem = key._pb.path.add()
    elem.id = id_
    return key


def _make_commit_response(*keys):
    from google.cloud.datastore_v1.types import datastore as datastore_pb2

    mutation_results = [datastore_pb2.MutationResult(key=key) for key in keys]
    return datastore_pb2.CommitResponse(mutation_results=mutation_results)


def _make_lookup_response(results=(), missing=(), deferred=()):
    entity_results_found = [
        mock.Mock(entity=result, spec=["entity"]) for result in results
    ]
    entity_results_missing = [
        mock.Mock(entity=missing_entity, spec=["entity"]) for missing_entity in missing
    ]
    return mock.Mock(
        found=entity_results_found,
        missing=entity_results_missing,
        deferred=deferred,
        spec=["found", "missing", "deferred"],
    )


def _make_datastore_api(*keys, **kwargs):
    commit_method = mock.Mock(return_value=_make_commit_response(*keys), spec=[])
    lookup_response = kwargs.pop("lookup_response", _make_lookup_response())
    lookup_method = mock.Mock(return_value=lookup_response, spec=[])
    return mock.Mock(
        commit=commit_method, lookup=lookup_method, spec=["commit", "lookup"]
    )
