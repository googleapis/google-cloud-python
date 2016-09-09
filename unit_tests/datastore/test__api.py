# Copyright 2016 Google Inc. All rights reserved.
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

from google.cloud.datastore._api import HAVE_GRPC


class TestDatastoreAPIBase(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore._api import DatastoreAPIBase
        return DatastoreAPIBase

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__lookup_virtual(self):
        api_base = self._makeOne()
        with self.assertRaises(NotImplementedError):
            api_base._lookup(None, None)

    def test__run_query_virtual(self):
        api_base = self._makeOne()
        with self.assertRaises(NotImplementedError):
            api_base._run_query(None, None)

    def test__begin_transaction_virtual(self):
        api_base = self._makeOne()
        with self.assertRaises(NotImplementedError):
            api_base._begin_transaction(None, None)

    def test__commit_virtual(self):
        api_base = self._makeOne()
        with self.assertRaises(NotImplementedError):
            api_base._commit(None, None)

    def test__rollback_virtual(self):
        api_base = self._makeOne()
        with self.assertRaises(NotImplementedError):
            api_base._rollback(None, None)

    def test__allocate_ids_virtual(self):
        api_base = self._makeOne()
        with self.assertRaises(NotImplementedError):
            api_base._allocate_ids(None, None)


class Test_DatastoreAPIOverHttp(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore._api import _DatastoreAPIOverHttp
        return _DatastoreAPIOverHttp

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__rpc(self):
        from google.cloud.datastore._api import build_api_url

        class ReqPB(object):

            def SerializeToString(self):
                return REQPB

        class RspPB(object):

            def __init__(self, pb):
                self._pb = pb

            @classmethod
            def FromString(cls, pb):
                return cls(pb)

        REQPB = b'REQPB'
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        BASE_URI = 'http://api-url'
        conn = _Connection(BASE_URI)
        URI = build_api_url(PROJECT, METHOD, BASE_URI)
        datastore_api = self._makeOne(conn)
        http = conn.http = Http({'status': '200'}, 'CONTENT')
        response = datastore_api._rpc(PROJECT, METHOD, ReqPB(), RspPB)
        self.assertTrue(isinstance(response, RspPB))
        self.assertEqual(response._pb, 'CONTENT')
        called_with = http._called_with
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)
        self.assertEqual(called_with['body'], REQPB)

    def test__request_w_200(self):
        from google.cloud.datastore._api import build_api_url

        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        DATA = b'DATA'
        URI = 'http://api-url'
        BASE_URI = 'http://api-url'
        conn = _Connection(BASE_URI)
        URI = build_api_url(PROJECT, METHOD, BASE_URI)
        datastore_api = self._makeOne(conn)
        http = conn.http = Http({'status': '200'}, 'CONTENT')
        self.assertEqual(datastore_api._request(PROJECT, METHOD, DATA),
                         'CONTENT')
        called_with = http._called_with
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)
        self.assertEqual(called_with['body'], DATA)

    def test__request_not_200(self):
        from google.cloud.datastore._api import build_api_url
        from google.cloud.exceptions import BadRequest
        from google.rpc import status_pb2

        error = status_pb2.Status()
        error.message = 'Entity value is indexed.'
        error.code = 9  # FAILED_PRECONDITION

        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        DATA = 'DATA'
        BASE_URI = 'http://api-url'
        conn = _Connection(BASE_URI)
        URI = build_api_url(PROJECT, METHOD, BASE_URI)
        datastore_api = self._makeOne(conn)
        conn.http = Http({'status': '400'}, error.SerializeToString())
        with self.assertRaises(BadRequest) as exc:
            datastore_api._request(PROJECT, METHOD, DATA)
        expected_message = '400 Entity value is indexed.'
        self.assertEqual(str(exc.exception), expected_message)
        # Verify the API call.
        called_with = conn.http._called_with
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)
        self.assertEqual(called_with['body'], DATA)


class Test_DatastoreAPIOverGRPC(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore._api import _DatastoreAPIOverGRPC
        return _DatastoreAPIOverGRPC

    def _makeOne(self, stub, connection=None, secure=True, mock_args=None):
        from google.cloud.datastore import _api as MUT
        from unit_tests._testing import _Monkey

        if connection is None:
            connection = _Connection(None)
            connection.credentials = object()
            connection.host = 'CURR_HOST'

        if mock_args is None:
            mock_args = []

        def mock_make_stub(*args):
            mock_args.append(args)
            return stub

        if secure:
            to_monkey = {'make_secure_stub': mock_make_stub}
        else:
            to_monkey = {'make_insecure_stub': mock_make_stub}
        with _Monkey(MUT, **to_monkey):
            return self._getTargetClass()(connection, secure)

    def test_constructor(self):
        from google.cloud.datastore import _api as MUT

        conn = _Connection(None)
        conn.credentials = object()
        conn.host = 'CURR_HOST'

        stub = _GRPCStub()
        mock_args = []
        datastore_api = self._makeOne(stub, connection=conn,
                                      mock_args=mock_args)
        self.assertIs(datastore_api._stub, stub)

        self.assertEqual(mock_args, [(
            conn.credentials,
            conn.USER_AGENT,
            MUT.datastore_grpc_pb2.DatastoreStub,
            conn.host,
        )])

    def test_constructor_insecure(self):
        from google.cloud.datastore import _api as MUT

        conn = _Connection(None)
        conn.credentials = object()
        conn.host = 'CURR_HOST:1234'

        stub = _GRPCStub()
        mock_args = []
        datastore_api = self._makeOne(stub, connection=conn,
                                      secure=False,
                                      mock_args=mock_args)
        self.assertIs(datastore_api._stub, stub)

        self.assertEqual(mock_args, [(
            MUT.datastore_grpc_pb2.DatastoreStub,
            conn.host,
        )])

    def test_internal_lookup(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api._lookup(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Lookup')])

    def test_internal_run_query(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api._run_query(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'RunQuery')])

    def test_internal_begin_transaction(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api._begin_transaction(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(
            stub.method_calls,
            [(request_pb, 'BeginTransaction')])

    def test_internal_commit_success(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api._commit(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Commit')])

    def _internal_commit_failure_helper(self, exc, err_class):
        stub = _GRPCStub(side_effect=exc)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        with self.assertRaises(err_class):
            datastore_api._commit(project, request_pb)

        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Commit')])

    @unittest.skipUnless(HAVE_GRPC, 'No gRPC')
    def test_internal_commit_failure_aborted(self):
        from grpc import StatusCode
        from grpc._channel import _Rendezvous
        from grpc._channel import _RPCState
        from google.cloud.exceptions import Conflict

        details = 'Bad things.'
        exc_state = _RPCState((), None, None, StatusCode.ABORTED, details)
        exc = _Rendezvous(exc_state, None, None, None)
        self._internal_commit_failure_helper(exc, Conflict)

    @unittest.skipUnless(HAVE_GRPC, 'No gRPC')
    def test_internal_commit_failure_cancelled(self):
        from grpc import StatusCode
        from grpc._channel import _Rendezvous
        from grpc._channel import _RPCState

        exc_state = _RPCState((), None, None, StatusCode.CANCELLED, None)
        exc = _Rendezvous(exc_state, None, None, None)
        self._internal_commit_failure_helper(exc, _Rendezvous)

    @unittest.skipUnless(HAVE_GRPC, 'No gRPC')
    def test_internal_commit_failure_non_grpc_err(self):
        exc = RuntimeError('Not a gRPC error')
        self._internal_commit_failure_helper(exc, RuntimeError)

    def test_internal_rollback(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api._rollback(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Rollback')])

    def test_internal_allocate_ids(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api._allocate_ids(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(
            stub.method_calls,
            [(request_pb, 'AllocateIds')])


class Test_build_api_url(unittest.TestCase):

    def _callFUT(self, project, method, base_url):
        from google.cloud.datastore._api import build_api_url
        return build_api_url(project, method, base_url)

    def test_it(self):
        from google.cloud.datastore import _api as MUT

        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        BASE_URL = 'http://example.com'
        URI = '/'.join([
            BASE_URL,
            MUT.API_VERSION,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        result = self._callFUT(PROJECT, METHOD, BASE_URL)
        self.assertEqual(result, URI)


class Test_parse_commit_response(unittest.TestCase):

    def _callFUT(self, commit_response_pb):
        from google.cloud.datastore._api import parse_commit_response
        return parse_commit_response(commit_response_pb)

    def test_it(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import entity_pb2

        index_updates = 1337
        keys = [
            entity_pb2.Key(
                path=[
                    entity_pb2.Key.PathElement(
                        kind='Foo',
                        id=1234,
                    ),
                ],
            ),
            entity_pb2.Key(
                path=[
                    entity_pb2.Key.PathElement(
                        kind='Bar',
                        name='baz',
                    ),
                ],
            ),
        ]
        response = datastore_pb2.CommitResponse(
            mutation_results=[
                datastore_pb2.MutationResult(key=key) for key in keys
            ],
            index_updates=index_updates,
        )
        result = self._callFUT(response)
        self.assertEqual(result, (index_updates, keys))


class _Connection(object):

    host = None
    USER_AGENT = 'you-sir-age-int'

    def __init__(self, api_base_url):
        self.api_base_url = api_base_url


class _GRPCStub(object):

    def __init__(self, return_val=None, side_effect=Exception):
        self.return_val = return_val
        self.side_effect = side_effect
        self.method_calls = []

    def _method(self, request_pb, name):
        self.method_calls.append((request_pb, name))
        return self.return_val

    def Lookup(self, request_pb):
        return self._method(request_pb, 'Lookup')

    def RunQuery(self, request_pb):
        return self._method(request_pb, 'RunQuery')

    def BeginTransaction(self, request_pb):
        return self._method(request_pb, 'BeginTransaction')

    def Commit(self, request_pb):
        result = self._method(request_pb, 'Commit')
        if self.side_effect is Exception:
            return result
        else:
            raise self.side_effect

    def Rollback(self, request_pb):
        return self._method(request_pb, 'Rollback')

    def AllocateIds(self, request_pb):
        return self._method(request_pb, 'AllocateIds')


class _RequestPB(object):
    project_id = None


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
