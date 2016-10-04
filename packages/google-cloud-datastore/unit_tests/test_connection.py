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

from google.cloud.datastore.connection import _HAVE_GRPC


class Test_DatastoreAPIOverHttp(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore.connection import _DatastoreAPIOverHttp
        return _DatastoreAPIOverHttp

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__rpc(self):
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
        URI = 'http://api-url'
        conn = _Connection(URI)
        datastore_api = self._makeOne(conn)
        http = conn.http = Http({'status': '200'}, 'CONTENT')
        response = datastore_api._rpc(PROJECT, METHOD, ReqPB(), RspPB)
        self.assertIsInstance(response, RspPB)
        self.assertEqual(response._pb, 'CONTENT')
        called_with = http._called_with
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)
        self.assertEqual(called_with['body'], REQPB)
        self.assertEqual(conn.build_kwargs,
                         [{'method': METHOD, 'project': PROJECT}])

    def test__request_w_200(self):
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        DATA = b'DATA'
        URI = 'http://api-url'
        conn = _Connection(URI)
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
        self.assertEqual(conn.build_kwargs,
                         [{'method': METHOD, 'project': PROJECT}])

    def test__request_not_200(self):
        from google.cloud.exceptions import BadRequest
        from google.rpc import status_pb2

        error = status_pb2.Status()
        error.message = 'Entity value is indexed.'
        error.code = 9  # FAILED_PRECONDITION

        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        DATA = 'DATA'
        URI = 'http://api-url'
        conn = _Connection(URI)
        datastore_api = self._makeOne(conn)
        conn.http = Http({'status': '400'}, error.SerializeToString())
        with self.assertRaises(BadRequest) as exc:
            datastore_api._request(PROJECT, METHOD, DATA)
        expected_message = '400 Entity value is indexed.'
        self.assertEqual(str(exc.exception), expected_message)
        self.assertEqual(conn.build_kwargs,
                         [{'method': METHOD, 'project': PROJECT}])


class Test_DatastoreAPIOverGRPC(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore.connection import _DatastoreAPIOverGRPC
        return _DatastoreAPIOverGRPC

    def _makeOne(self, stub, connection=None, secure=True, mock_args=None):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore import connection as MUT

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
        from google.cloud.datastore import connection as MUT

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
        from google.cloud.datastore import connection as MUT

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

    def test_lookup(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api.lookup(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Lookup')])

    def test_run_query(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api.run_query(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'RunQuery')])

    def _run_query_failure_helper(self, exc, err_class):
        stub = _GRPCStub(side_effect=exc)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        with self.assertRaises(err_class):
            datastore_api.run_query(project, request_pb)

        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'RunQuery')])

    @unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
    def test_run_query_invalid_argument(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import BadRequest
        from google.cloud.exceptions import GrpcRendezvous

        details = ('Cannot have inequality filters on multiple '
                   'properties: [created, priority]')
        exc_state = _RPCState((), None, None,
                              StatusCode.INVALID_ARGUMENT, details)
        exc = GrpcRendezvous(exc_state, None, None, None)
        self._run_query_failure_helper(exc, BadRequest)

    @unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
    def test_run_query_cancelled(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import GrpcRendezvous

        exc_state = _RPCState((), None, None, StatusCode.CANCELLED, None)
        exc = GrpcRendezvous(exc_state, None, None, None)
        self._run_query_failure_helper(exc, GrpcRendezvous)

    def test_begin_transaction(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api.begin_transaction(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(
            stub.method_calls,
            [(request_pb, 'BeginTransaction')])

    def test_commit_success(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api.commit(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Commit')])

    def _commit_failure_helper(self, exc, err_class):
        stub = _GRPCStub(side_effect=exc)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        with self.assertRaises(err_class):
            datastore_api.commit(project, request_pb)

        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Commit')])

    @unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
    def test_commit_failure_aborted(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import Conflict
        from google.cloud.exceptions import GrpcRendezvous

        details = 'Bad things.'
        exc_state = _RPCState((), None, None, StatusCode.ABORTED, details)
        exc = GrpcRendezvous(exc_state, None, None, None)
        self._commit_failure_helper(exc, Conflict)

    @unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
    def test_commit_failure_invalid_argument(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import BadRequest
        from google.cloud.exceptions import GrpcRendezvous

        details = 'Too long content.'
        exc_state = _RPCState((), None, None,
                              StatusCode.INVALID_ARGUMENT, details)
        exc = GrpcRendezvous(exc_state, None, None, None)
        self._commit_failure_helper(exc, BadRequest)

    @unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
    def test_commit_failure_cancelled(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import GrpcRendezvous

        exc_state = _RPCState((), None, None, StatusCode.CANCELLED, None)
        exc = GrpcRendezvous(exc_state, None, None, None)
        self._commit_failure_helper(exc, GrpcRendezvous)

    @unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
    def test_commit_failure_non_grpc_err(self):
        exc = RuntimeError('Not a gRPC error')
        self._commit_failure_helper(exc, RuntimeError)

    def test_rollback(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api.rollback(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Rollback')])

    def test_allocate_ids(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api = self._makeOne(stub=stub)

        request_pb = _RequestPB()
        project = 'PROJECT'
        result = datastore_api.allocate_ids(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(
            stub.method_calls,
            [(request_pb, 'AllocateIds')])


class TestConnection(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore.connection import Connection

        return Connection

    def _make_key_pb(self, project, id_=1234):
        from google.cloud.datastore.key import Key
        path_args = ('Kind',)
        if id_ is not None:
            path_args += (id_,)
        return Key(*path_args, project=project).to_protobuf()

    def _make_query_pb(self, kind):
        from google.cloud.datastore._generated import query_pb2
        pb = query_pb2.Query()
        pb.kind.add().name = kind
        return pb

    def _makeOne(self, credentials=None, http=None, use_grpc=False):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore import connection as MUT
        with _Monkey(MUT, _USE_GRPC=use_grpc):
            return self._getTargetClass()(credentials=credentials, http=http)

    def _verifyProtobufCall(self, called_with, URI, conn):
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)

    def test_default_url(self):
        klass = self._getTargetClass()
        conn = self._makeOne()
        self.assertEqual(conn.api_base_url, klass.API_BASE_URL)

    def test_custom_url_from_env(self):
        import os
        from google.cloud._testing import _Monkey
        from google.cloud.connection import API_BASE_URL
        from google.cloud.environment_vars import GCD_HOST

        HOST = 'CURR_HOST'
        fake_environ = {GCD_HOST: HOST}

        with _Monkey(os, environ=fake_environ):
            conn = self._makeOne()

        self.assertNotEqual(conn.api_base_url, API_BASE_URL)
        self.assertEqual(conn.api_base_url, 'http://' + HOST)

    def test_ctor_defaults(self):
        conn = self._makeOne()
        self.assertIsNone(conn.credentials)

    def test_ctor_without_grpc(self):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore import connection as MUT

        connections = []
        return_val = object()

        def mock_api(connection):
            connections.append(connection)
            return return_val

        with _Monkey(MUT, _DatastoreAPIOverHttp=mock_api):
            conn = self._makeOne(use_grpc=False)

        self.assertIsNone(conn.credentials)
        self.assertIs(conn._datastore_api, return_val)
        self.assertEqual(connections, [conn])

    def test_ctor_with_grpc(self):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore import connection as MUT

        api_args = []
        return_val = object()

        def mock_api(connection, secure):
            api_args.append((connection, secure))
            return return_val

        with _Monkey(MUT, _DatastoreAPIOverGRPC=mock_api):
            conn = self._makeOne(use_grpc=True)

        self.assertIsNone(conn.credentials)
        self.assertIs(conn._datastore_api, return_val)
        self.assertEqual(api_args, [(conn, True)])

    def test_ctor_explicit(self):
        class Creds(object):

            def create_scoped_required(self):
                return False

        creds = Creds()
        conn = self._makeOne(creds)
        self.assertIs(conn.credentials, creds)

    def test_http_w_existing(self):
        conn = self._makeOne()
        conn._http = http = object()
        self.assertIs(conn.http, http)

    def test_http_wo_creds(self):
        import httplib2

        conn = self._makeOne()
        self.assertIsInstance(conn.http, httplib2.Http)

    def test_http_w_creds(self):
        import httplib2

        authorized = object()

        class Creds(object):

            def authorize(self, http):
                self._called_with = http
                return authorized

            def create_scoped_required(self):
                return False

        creds = Creds()
        conn = self._makeOne(creds)
        self.assertIs(conn.http, authorized)
        self.assertIsInstance(creds._called_with, httplib2.Http)

    def test_build_api_url_w_default_base_version(self):
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        self.assertEqual(conn.build_api_url(PROJECT, METHOD), URI)

    def test_build_api_url_w_explicit_base_version(self):
        BASE = 'http://example.com/'
        VER = '3.1415926'
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            BASE,
            VER,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        self.assertEqual(conn.build_api_url(PROJECT, METHOD, BASE, VER),
                         URI)

    def test_lookup_single_key_empty_response(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb])
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])

    def test_lookup_single_key_empty_response_w_eventual(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb],
                                               eventual=True)
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
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
        key_pb = self._make_key_pb(PROJECT)
        conn = self._makeOne()
        self.assertRaises(ValueError, conn.lookup, PROJECT, key_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_lookup_single_key_empty_response_w_transaction(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        TRANSACTION = b'TRANSACTION'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb],
                                               transaction_id=TRANSACTION)
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_lookup_single_key_nonempty_response(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import entity_pb2

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        entity = entity_pb2.Entity()
        entity.key.CopyFrom(key_pb)
        rsp_pb.found.add(entity=entity)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        (found,), missing, deferred = conn.lookup(PROJECT, [key_pb])
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        self.assertEqual(found.key.path[0].kind, 'Kind')
        self.assertEqual(found.key.path[0].id, 1234)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])

    def test_lookup_multiple_keys_empty_response(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb1 = self._make_key_pb(PROJECT)
        key_pb2 = self._make_key_pb(PROJECT, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb1, key_pb2])
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_lookup_multiple_keys_w_missing(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb1 = self._make_key_pb(PROJECT)
        key_pb2 = self._make_key_pb(PROJECT, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        er_1 = rsp_pb.missing.add()
        er_1.entity.key.CopyFrom(key_pb1)
        er_2 = rsp_pb.missing.add()
        er_2.entity.key.CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result, missing, deferred = conn.lookup(PROJECT, [key_pb1, key_pb2])
        self.assertEqual(result, [])
        self.assertEqual(len(deferred), 0)
        self.assertEqual([missed.key for missed in missing],
                         [key_pb1, key_pb2])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_lookup_multiple_keys_w_deferred(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb1 = self._make_key_pb(PROJECT)
        key_pb2 = self._make_key_pb(PROJECT, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        rsp_pb.deferred.add().CopyFrom(key_pb1)
        rsp_pb.deferred.add().CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result, missing, deferred = conn.lookup(PROJECT, [key_pb1, key_pb2])
        self.assertEqual(result, [])
        self.assertEqual(len(missing), 0)
        self.assertEqual([def_key for def_key in deferred], [key_pb1, key_pb2])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(cw['headers']['User-Agent'], conn.USER_AGENT)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_run_query_w_eventual_no_transaction(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(PROJECT, q_pb,
                                                 eventual=True)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb2.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_run_query_wo_eventual_w_transaction(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import query_pb2

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
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(
            PROJECT, q_pb, transaction_id=TRANSACTION)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(
            request.read_options.read_consistency,
            datastore_pb2.ReadOptions.READ_CONSISTENCY_UNSPECIFIED)
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_run_query_w_eventual_and_transaction(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import query_pb2

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
        conn = self._makeOne()
        self.assertRaises(ValueError, conn.run_query, PROJECT, q_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_run_query_wo_namespace_empty_result(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(PROJECT, q_pb)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)

    def test_run_query_w_namespace_nonempty_result(self):
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore._generated import entity_pb2

        PROJECT = 'PROJECT'
        KIND = 'Kind'
        entity = entity_pb2.Entity()
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.entity_results.add(entity=entity)
        rsp_pb.batch.entity_result_type = 1  # FULL
        rsp_pb.batch.more_results = 3  # NO_MORE_RESULTS
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs = conn.run_query(PROJECT, q_pb, 'NS')[0]
        self.assertEqual(len(pbs), 1)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, 'NS')
        self.assertEqual(request.query, q_pb)

    def test_begin_transaction(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        TRANSACTION = b'TRANSACTION'
        rsp_pb = datastore_pb2.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':beginTransaction',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.begin_transaction(PROJECT), TRANSACTION)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.BeginTransactionRequest
        request = rq_class()
        request.ParseFromString(cw['body'])

    def test_commit_wo_transaction(self):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore import connection as MUT
        from google.cloud.datastore.helpers import _new_value_pb

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb)
        value_pb = _new_value_pb(insert, 'foo')
        value_pb.string_value = u'Foo'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())

        # Set up mock for parsing the response.
        expected_result = object()
        _parsed = []

        def mock_parse(response):
            _parsed.append(response)
            return expected_result

        with _Monkey(MUT, _parse_commit_response=mock_parse):
            result = conn.commit(PROJECT, req_pb, None)

        self.assertIs(result, expected_result)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'')
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)
        self.assertEqual(_parsed, [rsp_pb])

    def test_commit_w_transaction(self):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore._generated import datastore_pb2
        from google.cloud.datastore import connection as MUT
        from google.cloud.datastore.helpers import _new_value_pb

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb)
        value_pb = _new_value_pb(insert, 'foo')
        value_pb.string_value = u'Foo'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())

        # Set up mock for parsing the response.
        expected_result = object()
        _parsed = []

        def mock_parse(response):
            _parsed.append(response)
            return expected_result

        with _Monkey(MUT, _parse_commit_response=mock_parse):
            result = conn.commit(PROJECT, req_pb, b'xact')

        self.assertIs(result, expected_result)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'xact')
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.TRANSACTIONAL)
        self.assertEqual(_parsed, [rsp_pb])

    def test_rollback_ok(self):
        from google.cloud.datastore._generated import datastore_pb2
        PROJECT = 'PROJECT'
        TRANSACTION = b'xact'

        rsp_pb = datastore_pb2.RollbackResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':rollback',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertIsNone(conn.rollback(PROJECT, TRANSACTION))
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RollbackRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, TRANSACTION)

    def test_allocate_ids_empty(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        rsp_pb = datastore_pb2.AllocateIdsResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':allocateIds',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.allocate_ids(PROJECT, []), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.AllocateIdsRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(list(request.keys), [])

    def test_allocate_ids_non_empty(self):
        from google.cloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        before_key_pbs = [
            self._make_key_pb(PROJECT, id_=None),
            self._make_key_pb(PROJECT, id_=None),
            ]
        after_key_pbs = [
            self._make_key_pb(PROJECT),
            self._make_key_pb(PROJECT, id_=2345),
            ]
        rsp_pb = datastore_pb2.AllocateIdsResponse()
        rsp_pb.keys.add().CopyFrom(after_key_pbs[0])
        rsp_pb.keys.add().CopyFrom(after_key_pbs[1])
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':allocateIds',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.allocate_ids(PROJECT, before_key_pbs),
                         after_key_pbs)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.AllocateIdsRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(len(request.keys), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.keys):
            self.assertEqual(key_before, key_after)


class Test__parse_commit_response(unittest.TestCase):

    def _callFUT(self, commit_response_pb):
        from google.cloud.datastore.connection import _parse_commit_response
        return _parse_commit_response(commit_response_pb)

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


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content


class _Connection(object):

    host = None
    USER_AGENT = 'you-sir-age-int'

    def __init__(self, api_url):
        self.api_url = api_url
        self.build_kwargs = []

    def build_api_url(self, **kwargs):
        self.build_kwargs.append(kwargs)
        return self.api_url


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
        result = self._method(request_pb, 'RunQuery')
        if self.side_effect is Exception:
            return result
        else:
            raise self.side_effect

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
