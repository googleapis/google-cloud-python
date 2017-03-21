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

from google.cloud.datastore.client import _HAVE_GRPC


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class Test__catch_remap_gax_error(unittest.TestCase):

    def _call_fut(self):
        from google.cloud.datastore._gax import _catch_remap_gax_error

        return _catch_remap_gax_error()

    @staticmethod
    def _fake_method(exc, result=None):
        if exc is None:
            return result
        else:
            raise exc

    @staticmethod
    def _make_rendezvous(status_code, details):
        from grpc._channel import _RPCState
        from google.cloud.exceptions import GrpcRendezvous

        exc_state = _RPCState((), None, None, status_code, details)
        return GrpcRendezvous(exc_state, None, None, None)

    def test_success(self):
        expected = object()
        with self._call_fut():
            result = self._fake_method(None, expected)
        self.assertIs(result, expected)

    def test_non_grpc_err(self):
        exc = RuntimeError('Not a gRPC error')
        with self.assertRaises(RuntimeError):
            with self._call_fut():
                self._fake_method(exc)

    def test_gax_error(self):
        from google.gax.errors import GaxError
        from grpc import StatusCode
        from google.cloud.exceptions import Forbidden

        # First, create low-level GrpcRendezvous exception.
        details = 'Some error details.'
        cause = self._make_rendezvous(StatusCode.PERMISSION_DENIED, details)
        # Then put it into a high-level GaxError.
        msg = 'GAX Error content.'
        exc = GaxError(msg, cause=cause)

        with self.assertRaises(Forbidden):
            with self._call_fut():
                self._fake_method(exc)

    def test_gax_error_not_mapped(self):
        from google.gax.errors import GaxError
        from grpc import StatusCode

        cause = self._make_rendezvous(StatusCode.CANCELLED, None)
        exc = GaxError(None, cause=cause)

        with self.assertRaises(GaxError):
            with self._call_fut():
                self._fake_method(exc)


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class TestGAPICDatastoreAPI(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._gax import GAPICDatastoreAPI

        return GAPICDatastoreAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_lookup(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(datastore_client.DatastoreClient, 'lookup')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._catch_remap_gax_error')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_lookup:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.lookup(None, True, bb='cc')
                    mock_lookup.assert_called_once_with(None, True, bb='cc')
                    mock_catch_rendezvous.assert_called_once_with()

    def test_run_query(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(
            datastore_client.DatastoreClient, 'run_query')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._catch_remap_gax_error')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_run_query:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.run_query('47a', none=None)
                    mock_run_query.assert_called_once_with('47a', none=None)
                    mock_catch_rendezvous.assert_called_once_with()

    def test_begin_transaction(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(
            datastore_client.DatastoreClient, 'begin_transaction')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._catch_remap_gax_error')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_begin_transaction:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.begin_transaction('a', 'b', [], key='kei')
                    mock_begin_transaction.assert_called_once_with(
                        'a', 'b', [], key='kei')
                    mock_catch_rendezvous.assert_called_once_with()

    def test_commit(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(datastore_client.DatastoreClient, 'commit')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._catch_remap_gax_error')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_commit:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.commit(1, 2, a=3)
                    mock_commit.assert_called_once_with(1, 2, a=3)
                    mock_catch_rendezvous.assert_called_once_with()

    def test_rollback(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(
            datastore_client.DatastoreClient, 'rollback')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._catch_remap_gax_error')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_rollback:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.rollback(11, 12, arp='marp')
                    mock_rollback.assert_called_once_with(11, 12, arp='marp')
                    mock_catch_rendezvous.assert_called_once_with()

    def test_allocate_ids(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(
            datastore_client.DatastoreClient, 'allocate_ids')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._catch_remap_gax_error')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_allocate_ids:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.allocate_ids(
                        'hey', 'bai', bye=(47, 4), shy={'a': 4})
                    mock_allocate_ids.assert_called_once_with(
                        'hey', 'bai', bye=(47, 4), shy={'a': 4})
                    mock_catch_rendezvous.assert_called_once_with()


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class Test_make_datastore_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.datastore._gax import make_datastore_api

        return make_datastore_api(client)

    @mock.patch(
        'google.cloud.datastore._gax.GAPICDatastoreAPI',
        return_value=mock.sentinel.ds_client)
    @mock.patch('google.cloud.datastore._gax.make_secure_channel',
                return_value=mock.sentinel.channel)
    def test_live_api(self, make_chan, mock_klass):
        from google.cloud.gapic.datastore.v1 import datastore_client
        from google.cloud._http import DEFAULT_USER_AGENT
        from google.cloud.datastore import __version__

        host = datastore_client.DatastoreClient.SERVICE_ADDRESS
        base_url = 'https://' + host
        client = mock.Mock(
            _base_url=base_url,
            _credentials=mock.sentinel.credentials,
            spec=['_base_url', '_credentials'])
        ds_api = self._call_fut(client)
        self.assertIs(ds_api, mock.sentinel.ds_client)

        make_chan.assert_called_once_with(
            mock.sentinel.credentials, DEFAULT_USER_AGENT, host)
        mock_klass.assert_called_once_with(
            channel=mock.sentinel.channel, lib_name='gccl',
            lib_version=__version__)

    @mock.patch(
        'google.cloud.datastore._gax.GAPICDatastoreAPI',
        return_value=mock.sentinel.ds_client)
    @mock.patch('google.cloud.datastore._gax.insecure_channel',
                return_value=mock.sentinel.channel)
    def test_emulator(self, make_chan, mock_klass):
        from google.cloud.datastore import __version__

        host = 'localhost:8901'
        base_url = 'http://' + host
        client = mock.Mock(
            _base_url=base_url,
            _credentials=mock.sentinel.credentials,
            spec=['_base_url', '_credentials'])
        ds_api = self._call_fut(client)
        self.assertIs(ds_api, mock.sentinel.ds_client)

        make_chan.assert_called_once_with(host)
        mock_klass.assert_called_once_with(
            channel=mock.sentinel.channel, lib_name='gccl',
            lib_version=__version__)
