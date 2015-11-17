# Copyright 2015 Google Inc. All rights reserved.
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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.client import Client
        return Client

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _constructor_test_helper(self, expected_scopes, creds,
                                 read_only=False, admin=False,
                                 user_agent=None, timeout_seconds=None,
                                 expected_creds=None):
        from gcloud.bigtable import client as MUT

        user_agent = user_agent or MUT.DEFAULT_USER_AGENT
        timeout_seconds = timeout_seconds or MUT.DEFAULT_TIMEOUT_SECONDS
        PROJECT = 'PROJECT'
        client = self._makeOne(project=PROJECT, credentials=creds,
                               read_only=read_only, admin=admin,
                               user_agent=user_agent,
                               timeout_seconds=timeout_seconds)

        expected_creds = expected_creds or creds
        self.assertTrue(client._credentials is expected_creds)
        self.assertEqual(client._credentials._scopes, expected_scopes)

        self.assertEqual(client.project, PROJECT)
        self.assertEqual(client.timeout_seconds, timeout_seconds)
        self.assertEqual(client.user_agent, user_agent)
        # Check stubs are set (but null)
        self.assertEqual(client._data_stub, None)
        self.assertEqual(client._cluster_stub, None)
        self.assertEqual(client._operations_stub, None)
        self.assertEqual(client._table_stub, None)

    def test_constructor_default_scopes(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent_and_timeout(self):
        from gcloud.bigtable import client as MUT

        timeout_seconds = 1337
        user_agent = 'custom-application'
        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=user_agent,
                                      timeout_seconds=timeout_seconds)

    def test_constructor_with_admin(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE, MUT.ADMIN_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds, admin=True)

    def test_constructor_with_read_only(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.READ_ONLY_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds, read_only=True)

    def test_constructor_both_admin_and_read_only(self):
        creds = _Credentials()
        with self.assertRaises(ValueError):
            self._constructor_test_helper([], creds, admin=True,
                                          read_only=True)

    def test_constructor_implict_credentials(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT

        creds = _Credentials()
        expected_scopes = [MUT.DATA_SCOPE]

        def mock_get_credentials():
            return creds

        with _Monkey(MUT, get_credentials=mock_get_credentials):
            self._constructor_test_helper(expected_scopes, None,
                                          expected_creds=creds)

    def test_credentials_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        self.assertTrue(client.credentials is credentials)

    def test_project_name_property(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        project_name = 'projects/' + project
        self.assertEqual(client.project_name, project_name)

    def test_data_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        client._data_stub = object()
        self.assertTrue(client.data_stub is client._data_stub)

    def test_data_stub_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        with self.assertRaises(ValueError):
            getattr(client, 'data_stub')

    def test_cluster_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._cluster_stub = object()
        self.assertTrue(client.cluster_stub is client._cluster_stub)

    def test_cluster_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, 'cluster_stub')

    def test_cluster_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, 'cluster_stub')

    def test_operations_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._operations_stub = object()
        self.assertTrue(client.operations_stub is client._operations_stub)

    def test_operations_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, 'operations_stub')

    def test_operations_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, 'operations_stub')

    def test_table_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._table_stub = object()
        self.assertTrue(client.table_stub is client._table_stub)

    def test_table_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, 'table_stub')

    def test_table_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, 'table_stub')

    def test__make_data_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import DATA_API_HOST
        from gcloud.bigtable.client import DATA_API_PORT
        from gcloud.bigtable.client import DATA_STUB_FACTORY

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_stub=mock_make_stub):
            result = client._make_data_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                DATA_STUB_FACTORY,
                DATA_API_HOST,
                DATA_API_PORT,
            ),
        ])

    def test__make_cluster_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import CLUSTER_ADMIN_HOST
        from gcloud.bigtable.client import CLUSTER_ADMIN_PORT
        from gcloud.bigtable.client import CLUSTER_STUB_FACTORY

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_stub=mock_make_stub):
            result = client._make_cluster_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                CLUSTER_STUB_FACTORY,
                CLUSTER_ADMIN_HOST,
                CLUSTER_ADMIN_PORT,
            ),
        ])

    def test__make_operations_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import CLUSTER_ADMIN_HOST
        from gcloud.bigtable.client import CLUSTER_ADMIN_PORT
        from gcloud.bigtable.client import OPERATIONS_STUB_FACTORY

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_stub=mock_make_stub):
            result = client._make_operations_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                OPERATIONS_STUB_FACTORY,
                CLUSTER_ADMIN_HOST,
                CLUSTER_ADMIN_PORT,
            ),
        ])

    def test__make_table_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import TABLE_ADMIN_HOST
        from gcloud.bigtable.client import TABLE_ADMIN_PORT
        from gcloud.bigtable.client import TABLE_STUB_FACTORY

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_stub=mock_make_stub):
            result = client._make_table_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                TABLE_STUB_FACTORY,
                TABLE_ADMIN_HOST,
                TABLE_ADMIN_PORT,
            ),
        ])

    def test_is_started(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        self.assertFalse(client.is_started())
        client._data_stub = object()
        self.assertTrue(client.is_started())
        client._data_stub = None
        self.assertFalse(client.is_started())

    def _start_method_helper(self, admin):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=admin)

        stub = _FakeStub()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return stub

        with _Monkey(MUT, make_stub=mock_make_stub):
            client.start()

        self.assertTrue(client._data_stub is stub)
        if admin:
            self.assertTrue(client._cluster_stub is stub)
            self.assertTrue(client._operations_stub is stub)
            self.assertTrue(client._table_stub is stub)
            self.assertEqual(stub._entered, 4)
            self.assertEqual(len(make_stub_args), 4)
        else:
            self.assertTrue(client._cluster_stub is None)
            self.assertTrue(client._operations_stub is None)
            self.assertTrue(client._table_stub is None)
            self.assertEqual(stub._entered, 1)
            self.assertEqual(len(make_stub_args), 1)
        self.assertEqual(stub._exited, [])

    def test_start_non_admin(self):
        self._start_method_helper(admin=False)

    def test_start_with_admin(self):
        self._start_method_helper(admin=True)

    def test_start_while_started(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        client._data_stub = data_stub = object()
        self.assertTrue(client.is_started())
        client.start()

        # Make sure the stub did not change.
        self.assertEqual(client._data_stub, data_stub)

    def _stop_method_helper(self, admin):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=admin)

        stub1 = _FakeStub()
        stub2 = _FakeStub()
        client._data_stub = stub1
        client._cluster_stub = stub2
        client._operations_stub = stub2
        client._table_stub = stub2
        client.stop()
        self.assertTrue(client._data_stub is None)
        self.assertTrue(client._cluster_stub is None)
        self.assertTrue(client._operations_stub is None)
        self.assertTrue(client._table_stub is None)
        self.assertEqual(stub1._entered, 0)
        self.assertEqual(stub2._entered, 0)
        exc_none_triple = (None, None, None)
        self.assertEqual(stub1._exited, [exc_none_triple])
        if admin:
            self.assertEqual(stub2._exited, [exc_none_triple] * 3)
        else:
            self.assertEqual(stub2._exited, [])

    def test_stop_non_admin(self):
        self._stop_method_helper(admin=False)

    def test_stop_with_admin(self):
        self._stop_method_helper(admin=True)

    def test_stop_while_stopped(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        self.assertFalse(client.is_started())

        # This is a bit hacky. We set the cluster stub protected value
        # since it isn't used in is_started() and make sure that stop
        # doesn't reset this value to None.
        client._cluster_stub = cluster_stub = object()
        client.stop()
        # Make sure the cluster stub did not change.
        self.assertEqual(client._cluster_stub, cluster_stub)


class _Credentials(object):

    _scopes = None

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _FakeStub(object):

    def __init__(self):
        self._entered = 0
        self._exited = []

    def __enter__(self):
        self._entered += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exited.append((exc_type, exc_val, exc_tb))
        return True
