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

import mock


class Test__request(unittest.TestCase):

    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.datastore._http import _request

        return _request(*args, **kwargs)

    def test_success(self):
        from google.cloud import _http as connection_module
        from google.cloud.datastore._http import _CLIENT_INFO

        project = 'PROJECT'
        method = 'METHOD'
        data = b'DATA'
        uri = 'http://api-url'

        # Make mock HTTP object with canned response.
        response_data = 'CONTENT'
        http = Http({'status': '200'}, response_data)

        # Call actual function under test.
        response = self._call_fut(http, project, method, data, uri)
        self.assertEqual(response, response_data)

        # Check that the mocks were called as expected.
        called_with = http._called_with
        self.assertEqual(len(called_with), 4)
        self.assertTrue(called_with['uri'].startswith(uri))
        self.assertEqual(called_with['method'], 'POST')
        expected_headers = {
            'Content-Type': 'application/x-protobuf',
            'User-Agent': connection_module.DEFAULT_USER_AGENT,
            'Content-Length': '4',
            connection_module.CLIENT_INFO_HEADER: _CLIENT_INFO,
        }
        self.assertEqual(called_with['headers'], expected_headers)
        self.assertEqual(called_with['body'], data)

    def test_failure(self):
        from google.cloud.exceptions import BadRequest
        from google.rpc import code_pb2
        from google.rpc import status_pb2

        project = 'PROJECT'
        method = 'METHOD'
        data = 'DATA'
        uri = 'http://api-url'

        # Make mock HTTP object with canned response.
        error = status_pb2.Status()
        error.message = 'Entity value is indexed.'
        error.code = code_pb2.FAILED_PRECONDITION
        http = Http({'status': '400'}, error.SerializeToString())

        # Call actual function under test.
        with self.assertRaises(BadRequest) as exc:
            self._call_fut(http, project, method, data, uri)

        # Check that the mocks were called as expected.
        expected_message = '400 Entity value is indexed.'
        self.assertEqual(str(exc.exception), expected_message)


class Test__rpc(unittest.TestCase):

    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.datastore._http import _rpc

        return _rpc(*args, **kwargs)

    def test_it(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        http = object()
        project = 'projectOK'
        method = 'beginTransaction'
        base_url = 'test.invalid'
        request_pb = datastore_pb2.BeginTransactionRequest(
            project_id=project)

        response_pb = datastore_pb2.BeginTransactionResponse(
            transaction=b'7830rmc')
        patch = mock.patch('google.cloud.datastore._http._request',
                           return_value=response_pb.SerializeToString())
        with patch as mock_request:
            result = self._call_fut(
                http, project, method, base_url,
                request_pb, datastore_pb2.BeginTransactionResponse)
            self.assertEqual(result, response_pb)

            mock_request.assert_called_once_with(
                http, project, method, request_pb.SerializeToString(),
                base_url)


class Test_DatastoreAPIOverHttp(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._http import _DatastoreAPIOverHttp

        return _DatastoreAPIOverHttp

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        connection = object()
        ds_api = self._make_one(connection)
        self.assertIs(ds_api.connection, connection)

    def test_lookup(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        connection = mock.Mock(
            api_base_url='test.invalid', spec=['http', 'api_base_url'])
        ds_api = self._make_one(connection)

        project = 'project'
        request_pb = object()

        patch = mock.patch(
            'google.cloud.datastore._http._rpc',
            return_value=mock.sentinel.looked_up)
        with patch as mock_rpc:
            result = ds_api.lookup(project, request_pb)
            self.assertIs(result, mock.sentinel.looked_up)

            mock_rpc.assert_called_once_with(
                connection.http, project, 'lookup',
                connection.api_base_url,
                request_pb, datastore_pb2.LookupResponse)


class TestConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._http import Connection

        return Connection

    def _make_query_pb(self, kind):
        from google.cloud.proto.datastore.v1 import query_pb2

        pb = query_pb2.Query()
        pb.kind.add().name = kind
        return pb

    def _make_one(self, client, use_grpc=False):
        with mock.patch('google.cloud.datastore._http._USE_GRPC',
                        new=use_grpc):
            return self._get_target_class()(client)

    def test_inherited_url(self):
        client = mock.Mock(_base_url='test.invalid', spec=['_base_url'])
        conn = self._make_one(client)
        self.assertEqual(conn.api_base_url, client._base_url)

    def test_constructor(self):
        client = mock.Mock(spec=['_base_url'])
        conn = self._make_one(client)
        self.assertIs(conn._client, client)

    def test_constructor_without_grpc(self):
        connections = []
        client = mock.Mock(spec=['_base_url'])
        return_val = object()

        def mock_api(connection):
            connections.append(connection)
            return return_val

        patch = mock.patch(
            'google.cloud.datastore._http._DatastoreAPIOverHttp',
            new=mock_api)
        with patch:
            conn = self._make_one(client, use_grpc=False)

        self.assertIs(conn._client, client)
        self.assertIs(conn._datastore_api, return_val)
        self.assertEqual(connections, [conn])

    def test_constructor_with_grpc(self):
        client = mock.Mock(spec=['_base_url'])

        patch = mock.patch(
            'google.cloud.datastore._http._DatastoreAPIOverGRPC',
            return_value=mock.sentinel.ds_api)
        with patch as mock_klass:
            conn = self._make_one(client, use_grpc=True)
            mock_klass.assert_called_once_with(conn)

        self.assertIs(conn._client, client)
        self.assertIs(conn._datastore_api, mock.sentinel.ds_api)

    def test_lookup_single_key_empty_response(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])

    def test_lookup_single_key_empty_response_w_eventual(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb], eventual=True)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb2.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_lookup_single_key_empty_response_w_eventual_and_transaction(self):
        PROJECT = 'PROJECT'
        TRANSACTION = b'TRANSACTION'
        key_pb = _make_key_pb(PROJECT)

        client = mock.Mock(spec=['_base_url'])
        conn = self._make_one(client)
        self.assertRaises(ValueError, conn.lookup, PROJECT, key_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_lookup_single_key_empty_response_w_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        transaction = b'TRANSACTION'
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb], transaction_id=transaction)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])
        self.assertEqual(request.read_options.transaction, transaction)

    def test_lookup_single_key_nonempty_response(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.proto.datastore.v1 import entity_pb2

        project = 'PROJECT'
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()
        entity = entity_pb2.Entity()
        entity.key.CopyFrom(key_pb)
        rsp_pb.found.add(entity=entity)

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 1)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)
        found = response.found[0].entity
        self.assertEqual(found.key.path[0].kind, 'Kind')
        self.assertEqual(found.key.path[0].id, 1234)
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])

    def test_lookup_multiple_keys_empty_response(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb1, key_pb2])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_lookup_multiple_keys_w_missing(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        er_1 = rsp_pb.missing.add()
        er_1.entity.key.CopyFrom(key_pb1)
        er_2 = rsp_pb.missing.add()
        er_2.entity.key.CopyFrom(key_pb2)

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb1, key_pb2])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.deferred), 0)
        missing_keys = [result.entity.key for result in response.missing]
        self.assertEqual(missing_keys, [key_pb1, key_pb2])
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_lookup_multiple_keys_w_deferred(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        from google.cloud import _http as connection_module
        from google.cloud.datastore._http import _CLIENT_INFO

        project = 'PROJECT'
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        rsp_pb.deferred.add().CopyFrom(key_pb1)
        rsp_pb.deferred.add().CopyFrom(key_pb2)

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.lookup(project, [key_pb1, key_pb2])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'lookup')
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(list(response.deferred), [key_pb1, key_pb2])
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        self.assertEqual(cw['uri'], uri)
        self.assertEqual(cw['method'], 'POST')
        expected_headers = {
            'Content-Type': 'application/x-protobuf',
            'User-Agent': conn.USER_AGENT,
            'Content-Length': '48',
            connection_module.CLIENT_INFO_HEADER: _CLIENT_INFO,
        }
        self.assertEqual(cw['headers'], expected_headers)
        request = datastore_pb2.LookupRequest()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_run_query_w_eventual_no_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.proto.datastore.v1 import query_pb2

        project = 'PROJECT'
        kind = 'Nonesuch'
        cursor = b'\x00'
        q_pb = self._make_query_pb(kind)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = cursor
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.run_query(project, q_pb, eventual=True)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'runQuery')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.RunQueryRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb2.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_run_query_wo_eventual_w_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.proto.datastore.v1 import query_pb2

        project = 'PROJECT'
        kind = 'Nonesuch'
        cursor = b'\x00'
        transaction = b'TRANSACTION'
        q_pb = self._make_query_pb(kind)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = cursor
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.run_query(
            project, q_pb, transaction_id=transaction)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'runQuery')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.RunQueryRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(
            request.read_options.read_consistency,
            datastore_pb2.ReadOptions.READ_CONSISTENCY_UNSPECIFIED)
        self.assertEqual(request.read_options.transaction, transaction)

    def test_run_query_w_eventual_and_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.proto.datastore.v1 import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = b'TRANSACTION'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL

        client = mock.Mock(spec=['_base_url'])
        conn = self._make_one(client)
        self.assertRaises(ValueError, conn.run_query, PROJECT, q_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_run_query_wo_namespace_empty_result(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.proto.datastore.v1 import query_pb2

        project = 'PROJECT'
        kind = 'Nonesuch'
        cursor = b'\x00'
        q_pb = self._make_query_pb(kind)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = cursor
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.run_query(project, q_pb)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(conn.api_base_url, project, 'runQuery')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.RunQueryRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)

    def test_run_query_w_namespace_nonempty_result(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.proto.datastore.v1 import entity_pb2
        from google.cloud.proto.datastore.v1 import query_pb2

        project = 'PROJECT'
        kind = 'Kind'
        entity = entity_pb2.Entity()
        q_pb = self._make_query_pb(kind)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.entity_results.add(entity=entity)
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        rsp_pb.batch.more_results = query_pb2.QueryResultBatch.NO_MORE_RESULTS

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        namespace = 'NS'
        response = conn.run_query(project, q_pb, namespace=namespace)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        cw = http._called_with
        uri = _build_expected_url(conn.api_base_url, project, 'runQuery')
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.RunQueryRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, namespace)
        self.assertEqual(request.query, q_pb)

    def test_begin_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        transaction = b'TRANSACTION'
        rsp_pb = datastore_pb2.BeginTransactionResponse()
        rsp_pb.transaction = transaction

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        conn = self._make_one(client)
        response = conn.begin_transaction(project)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(
            conn.api_base_url, project, 'beginTransaction')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.BeginTransactionRequest()
        request.ParseFromString(cw['body'])
        # The RPC-over-HTTP request does not set the project in the request.
        self.assertEqual(request.project_id, u'')


class TestHTTPDatastoreAPI(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._http import HTTPDatastoreAPI

        return HTTPDatastoreAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        client = object()
        ds_api = self._make_one(client)
        self.assertIs(ds_api.client, client)

    def test_commit_wo_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        project = 'PROJECT'
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb)
        value_pb = _new_value_pb(insert, 'foo')
        value_pb.string_value = u'Foo'

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        rq_class = datastore_pb2.CommitRequest
        ds_api = self._make_one(client)
        mode = rq_class.NON_TRANSACTIONAL
        result = ds_api.commit(project, mode, [mutation])

        # Check the result and verify the callers.
        self.assertEqual(result, rsp_pb)
        uri = _build_expected_url(client._base_url, project, 'commit')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'')
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_commit_w_transaction(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        project = 'PROJECT'
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb)
        value_pb = _new_value_pb(insert, 'foo')
        value_pb.string_value = u'Foo'

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        rq_class = datastore_pb2.CommitRequest
        ds_api = self._make_one(client)
        mode = rq_class.TRANSACTIONAL
        result = ds_api.commit(project, mode, [mutation], transaction=b'xact')

        # Check the result and verify the callers.
        self.assertEqual(result, rsp_pb)
        uri = _build_expected_url(client._base_url, project, 'commit')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'xact')
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.TRANSACTIONAL)

    def test_rollback_ok(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        transaction = b'xact'
        rsp_pb = datastore_pb2.RollbackResponse()

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.rollback(project, transaction)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(client._base_url, project, 'rollback')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.RollbackRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, transaction)

    def test_allocate_ids_empty(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        rsp_pb = datastore_pb2.AllocateIdsResponse()

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.allocate_ids(project, [])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb)
        self.assertEqual(list(response.keys), [])
        uri = _build_expected_url(client._base_url, project, 'allocateIds')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.AllocateIdsRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(list(request.keys), [])

    def test_allocate_ids_non_empty(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2

        project = 'PROJECT'
        before_key_pbs = [
            _make_key_pb(project, id_=None),
            _make_key_pb(project, id_=None),
        ]
        after_key_pbs = [
            _make_key_pb(project),
            _make_key_pb(project, id_=2345),
        ]
        rsp_pb = datastore_pb2.AllocateIdsResponse()
        rsp_pb.keys.add().CopyFrom(after_key_pbs[0])
        rsp_pb.keys.add().CopyFrom(after_key_pbs[1])

        # Create mock HTTP and client with response.
        http = Http({'status': '200'}, rsp_pb.SerializeToString())
        client = mock.Mock(
            _http=http, _base_url='test.invalid', spec=['_http', '_base_url'])

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.allocate_ids(project, before_key_pbs)

        # Check the result and verify the callers.
        self.assertEqual(list(response.keys), after_key_pbs)
        self.assertEqual(response, rsp_pb)
        uri = _build_expected_url(client._base_url, project, 'allocateIds')
        cw = http._called_with
        _verify_protobuf_call(self, cw, uri)
        request = datastore_pb2.AllocateIdsRequest()
        request.ParseFromString(cw['body'])
        self.assertEqual(len(request.keys), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.keys):
            self.assertEqual(key_before, key_after)


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response

        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content


def _build_expected_url(api_base_url, project, method):
    from google.cloud.datastore._http import API_VERSION

    return '/'.join([
        api_base_url,
        API_VERSION,
        'projects',
        project + ':' + method,
    ])


def _make_key_pb(project, id_=1234):
    from google.cloud.datastore.key import Key

    path_args = ('Kind',)
    if id_ is not None:
        path_args += (id_,)
    return Key(*path_args, project=project).to_protobuf()


def _verify_protobuf_call(testcase, called_with, uri):
    from google.cloud import _http as connection_module
    from google.cloud.datastore._http import _CLIENT_INFO

    testcase.assertEqual(called_with['uri'], uri)
    testcase.assertEqual(called_with['method'], 'POST')
    expected_headers = {
        'Content-Type': 'application/x-protobuf',
        'User-Agent': connection_module.DEFAULT_USER_AGENT,
        'Content-Length': str(len(called_with['body'])),
        connection_module.CLIENT_INFO_HEADER: _CLIENT_INFO,
    }
    testcase.assertEqual(called_with['headers'], expected_headers)
