# Copyright 2017 Google Inc.
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

from google.cloud.datastore._http import _HAVE_GRPC


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class Test__grpc_catch_rendezvous(unittest.TestCase):

    def _call_fut(self):
        from google.cloud.datastore._gax import _grpc_catch_rendezvous

        return _grpc_catch_rendezvous()

    @staticmethod
    def _fake_method(exc, result=None):
        if exc is None:
            return result
        else:
            raise exc

    def test_success(self):
        expected = object()
        with self._call_fut():
            result = self._fake_method(None, expected)
        self.assertIs(result, expected)

    def test_failure_aborted(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import Conflict
        from google.cloud.exceptions import GrpcRendezvous

        details = 'Bad things.'
        exc_state = _RPCState((), None, None, StatusCode.ABORTED, details)
        exc = GrpcRendezvous(exc_state, None, None, None)
        with self.assertRaises(Conflict):
            with self._call_fut():
                self._fake_method(exc)

    def test_failure_invalid_argument(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import BadRequest
        from google.cloud.exceptions import GrpcRendezvous

        details = ('Cannot have inequality filters on multiple '
                   'properties: [created, priority]')
        exc_state = _RPCState((), None, None,
                              StatusCode.INVALID_ARGUMENT, details)
        exc = GrpcRendezvous(exc_state, None, None, None)
        with self.assertRaises(BadRequest):
            with self._call_fut():
                self._fake_method(exc)

    def test_failure_cancelled(self):
        from grpc import StatusCode
        from grpc._channel import _RPCState
        from google.cloud.exceptions import GrpcRendezvous

        exc_state = _RPCState((), None, None, StatusCode.CANCELLED, None)
        exc = GrpcRendezvous(exc_state, None, None, None)
        with self.assertRaises(GrpcRendezvous):
            with self._call_fut():
                self._fake_method(exc)

    def test_commit_failure_non_grpc_err(self):
        exc = RuntimeError('Not a gRPC error')
        with self.assertRaises(RuntimeError):
            with self._call_fut():
                self._fake_method(exc)


class Test_DatastoreAPIOverGRPC(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._gax import _DatastoreAPIOverGRPC

        return _DatastoreAPIOverGRPC

    def _make_one(self, stub, connection=None, secure=True):
        if secure:
            patch = mock.patch(
                'google.cloud.datastore._gax.make_secure_stub',
                return_value=stub)
            base_url = 'https://test.invalid'
        else:
            patch = mock.patch(
                'google.cloud.datastore._gax.make_insecure_stub',
                return_value=stub)
            base_url = 'http://test.invalid'

        if connection is None:
            connection = mock.Mock(
                credentials=object(),
                api_base_url=base_url,
                spec=['credentials', 'api_base_url'],
            )

        with patch as make_stub_mock:
            api_obj = self._get_target_class()(connection)
            return api_obj, make_stub_mock

    def test_constructor(self):
        from google.cloud._http import DEFAULT_USER_AGENT
        import google.cloud.datastore._gax as MUT

        host = 'test.invalid'
        conn = mock.Mock(
            credentials=object(),
            api_base_url='https://' + host,
            spec=['credentials', 'api_base_url'],
        )

        stub = _GRPCStub()
        datastore_api, make_stub_mock = self._make_one(
            stub, connection=conn)

        self.assertIs(datastore_api._stub, stub)
        make_stub_mock.assert_called_once_with(
            conn.credentials,
            DEFAULT_USER_AGENT,
            MUT.datastore_pb2_grpc.DatastoreStub,
            host,
            extra_options=MUT._GRPC_EXTRA_OPTIONS,
        )

    def test_constructor_insecure(self):
        from google.cloud.proto.datastore.v1 import datastore_pb2_grpc

        host = 'test.invalid'
        conn = mock.Mock(
            credentials=object(),
            api_base_url='http://' + host,
            spec=['credentials', 'api_base_url'],
        )

        stub = _GRPCStub()
        datastore_api, make_stub_mock = self._make_one(
            stub, connection=conn, secure=False)

        self.assertIs(datastore_api._stub, stub)
        make_stub_mock.assert_called_once_with(
            datastore_pb2_grpc.DatastoreStub,
            host,
        )

    def test_lookup(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
        project = 'PROJECT'
        result = datastore_api.lookup(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Lookup')])

    def test_run_query(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
        project = 'PROJECT'
        result = datastore_api.run_query(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'RunQuery')])

    def _run_query_failure_helper(self, exc, err_class):
        stub = _GRPCStub(side_effect=exc)
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
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

    def test_begin_transaction(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
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
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
        project = 'PROJECT'
        result = datastore_api.commit(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Commit')])

    def test_rollback(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
        project = 'PROJECT'
        result = datastore_api.rollback(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(stub.method_calls,
                         [(request_pb, 'Rollback')])

    def test_allocate_ids(self):
        return_val = object()
        stub = _GRPCStub(return_val)
        datastore_api, _ = self._make_one(stub=stub)

        request_pb = mock.Mock(project_id=None, spec=['project_id'])
        project = 'PROJECT'
        result = datastore_api.allocate_ids(project, request_pb)
        self.assertIs(result, return_val)
        self.assertEqual(request_pb.project_id, project)
        self.assertEqual(
            stub.method_calls,
            [(request_pb, 'AllocateIds')])


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class Test_make_datastore_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.datastore._gax import make_datastore_api

        return make_datastore_api(client)

    @mock.patch(
        'google.cloud.gapic.datastore.v1.datastore_client.DatastoreClient',
        SERVICE_ADDRESS='datastore.mock.mock',
        return_value=mock.sentinel.ds_client)
    @mock.patch('google.cloud.datastore._gax.make_secure_channel',
                return_value=mock.sentinel.channel)
    def test_it(self, make_chan, mock_klass):
        from google.cloud._http import DEFAULT_USER_AGENT
        from google.cloud.datastore import __version__

        client = mock.Mock(
            _credentials=mock.sentinel.credentials, spec=['_credentials'])
        ds_api = self._call_fut(client)
        self.assertIs(ds_api, mock.sentinel.ds_client)

        make_chan.assert_called_once_with(
            mock.sentinel.credentials, DEFAULT_USER_AGENT,
            mock_klass.SERVICE_ADDRESS)
        mock_klass.assert_called_once_with(
            channel=mock.sentinel.channel, lib_name='gccl',
            lib_version=__version__)


class _GRPCStub(object):

    def __init__(self, return_val=None, side_effect=Exception):
        self.return_val = return_val
        self.side_effect = side_effect
        self.method_calls = []

    def _method(self, request_pb, name):
        self.method_calls.append((request_pb, name))
        if self.side_effect is Exception:
            return self.return_val
        else:
            raise self.side_effect

    def Lookup(self, request_pb):
        return self._method(request_pb, 'Lookup')

    def RunQuery(self, request_pb):
        return self._method(request_pb, 'RunQuery')

    def BeginTransaction(self, request_pb):
        return self._method(request_pb, 'BeginTransaction')

    def Commit(self, request_pb):
        return self._method(request_pb, 'Commit')

    def Rollback(self, request_pb):
        return self._method(request_pb, 'Rollback')

    def AllocateIds(self, request_pb):
        return self._method(request_pb, 'AllocateIds')
