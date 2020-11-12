# Copyright 2020 Google LLC All rights reserved.
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


import datetime
import mock
import unittest

from ._testing import _make_credentials
from google.cloud._helpers import UTC


class TestBackup(unittest.TestCase):
    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    CLUSTER_ID = "cluster-id"
    CLUSTER_NAME = INSTANCE_NAME + "/clusters/" + CLUSTER_ID
    TABLE_ID = "table-id"
    TABLE_NAME = INSTANCE_NAME + "/tables/" + TABLE_ID
    BACKUP_ID = "backup-id"
    BACKUP_NAME = CLUSTER_NAME + "/backups/" + BACKUP_ID

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.backup import Backup

        return Backup

    @staticmethod
    def _make_table_admin_client():
        from google.cloud.bigtable_admin_v2 import BigtableTableAdminClient

        return mock.create_autospec(BigtableTableAdminClient, instance=True)

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _make_timestamp(self):
        return datetime.datetime.utcnow().replace(tzinfo=UTC)

    def test_constructor_defaults(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)

        self.assertEqual(backup.backup_id, self.BACKUP_ID)
        self.assertIs(backup._instance, instance)
        self.assertIsNone(backup._cluster)
        self.assertIsNone(backup.table_id)
        self.assertIsNone(backup._expire_time)

        self.assertIsNone(backup._parent)
        self.assertIsNone(backup._source_table)
        self.assertIsNone(backup._start_time)
        self.assertIsNone(backup._end_time)
        self.assertIsNone(backup._size_bytes)
        self.assertIsNone(backup._state)

    def test_constructor_non_defaults(self):
        instance = _Instance(self.INSTANCE_NAME)
        expire_time = self._make_timestamp()

        backup = self._make_one(
            self.BACKUP_ID,
            instance,
            cluster_id=self.CLUSTER_ID,
            table_id=self.TABLE_ID,
            expire_time=expire_time,
        )

        self.assertEqual(backup.backup_id, self.BACKUP_ID)
        self.assertIs(backup._instance, instance)
        self.assertIs(backup._cluster, self.CLUSTER_ID)
        self.assertEqual(backup.table_id, self.TABLE_ID)
        self.assertEqual(backup._expire_time, expire_time)

        self.assertIsNone(backup._parent)
        self.assertIsNone(backup._source_table)
        self.assertIsNone(backup._start_time)
        self.assertIsNone(backup._end_time)
        self.assertIsNone(backup._size_bytes)
        self.assertIsNone(backup._state)

    def test_from_pb_project_mismatch(self):
        from google.cloud.bigtable_admin_v2.proto import table_pb2

        alt_project_id = "alt-project-id"
        client = _Client(project=alt_project_id)
        instance = _Instance(self.INSTANCE_NAME, client)
        backup_pb = table_pb2.Backup(name=self.BACKUP_NAME)
        klasse = self._get_target_class()

        with self.assertRaises(ValueError):
            klasse.from_pb(backup_pb, instance)

    def test_from_pb_instance_mismatch(self):
        from google.cloud.bigtable_admin_v2.proto import table_pb2

        alt_instance = "/projects/%s/instances/alt-instance" % self.PROJECT_ID
        client = _Client()
        instance = _Instance(alt_instance, client)
        backup_pb = table_pb2.Backup(name=self.BACKUP_NAME)
        klasse = self._get_target_class()

        with self.assertRaises(ValueError):
            klasse.from_pb(backup_pb, instance)

    def test_from_pb_bad_name(self):
        from google.cloud.bigtable_admin_v2.proto import table_pb2

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        backup_pb = table_pb2.Backup(name="invalid_name")
        klasse = self._get_target_class()

        with self.assertRaises(ValueError):
            klasse.from_pb(backup_pb, instance)

    def test_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.gapic import enums
        from google.cloud.bigtable_admin_v2.proto import table_pb2
        from google.cloud._helpers import _datetime_to_pb_timestamp

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        timestamp = _datetime_to_pb_timestamp(self._make_timestamp())
        size_bytes = 1234
        state = enums.Backup.State.READY
        backup_pb = table_pb2.Backup(
            name=self.BACKUP_NAME,
            source_table=self.TABLE_NAME,
            expire_time=timestamp,
            start_time=timestamp,
            end_time=timestamp,
            size_bytes=size_bytes,
            state=state,
        )
        klasse = self._get_target_class()

        backup = klasse.from_pb(backup_pb, instance)

        self.assertTrue(isinstance(backup, klasse))
        self.assertEqual(backup._instance, instance)
        self.assertEqual(backup.backup_id, self.BACKUP_ID)
        self.assertEqual(backup.cluster, self.CLUSTER_ID)
        self.assertEqual(backup.table_id, self.TABLE_ID)
        self.assertEqual(backup._expire_time, timestamp)
        self.assertEqual(backup._start_time, timestamp)
        self.assertEqual(backup._end_time, timestamp)
        self.assertEqual(backup._size_bytes, size_bytes)
        self.assertEqual(backup._state, state)

    def test_property_name(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)
        client._table_admin_client = api
        instance = _Instance(self.INSTANCE_NAME, client)

        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)
        self.assertEqual(backup.name, self.BACKUP_NAME)

    def test_property_cluster(self):
        backup = self._make_one(
            self.BACKUP_ID, _Instance(self.INSTANCE_NAME), cluster_id=self.CLUSTER_ID
        )
        self.assertEqual(backup.cluster, self.CLUSTER_ID)

    def test_property_cluster_setter(self):
        backup = self._make_one(self.BACKUP_ID, _Instance(self.INSTANCE_NAME))
        backup.cluster = self.CLUSTER_ID
        self.assertEqual(backup.cluster, self.CLUSTER_ID)

    def test_property_parent_none(self):
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME),
        )
        self.assertIsNone(backup.parent)

    def test_property_parent_w_cluster(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)
        client._table_admin_client = api
        instance = _Instance(self.INSTANCE_NAME, client)

        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)
        self.assertEqual(backup._cluster, self.CLUSTER_ID)
        self.assertEqual(backup.parent, self.CLUSTER_NAME)

    def test_property_source_table_none(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)
        client._table_admin_client = api
        instance = _Instance(self.INSTANCE_NAME, client)

        backup = self._make_one(self.BACKUP_ID, instance)
        self.assertIsNone(backup.source_table)

    def test_property_source_table_valid(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)
        client._table_admin_client = api
        instance = _Instance(self.INSTANCE_NAME, client)

        backup = self._make_one(self.BACKUP_ID, instance, table_id=self.TABLE_ID)
        self.assertEqual(backup.source_table, self.TABLE_NAME)

    def test_property_expire_time(self):
        instance = _Instance(self.INSTANCE_NAME)
        expire_time = self._make_timestamp()
        backup = self._make_one(self.BACKUP_ID, instance, expire_time=expire_time)
        self.assertEqual(backup.expire_time, expire_time)

    def test_property_expire_time_setter(self):
        instance = _Instance(self.INSTANCE_NAME)
        expire_time = self._make_timestamp()
        backup = self._make_one(self.BACKUP_ID, instance)
        backup.expire_time = expire_time
        self.assertEqual(backup.expire_time, expire_time)

    def test_property_start_time(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._start_time = self._make_timestamp()
        self.assertEqual(backup.start_time, expected)

    def test_property_end_time(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._end_time = self._make_timestamp()
        self.assertEqual(backup.end_time, expected)

    def test_property_size(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._size_bytes = 10
        self.assertEqual(backup.size_bytes, expected)

    def test_property_state(self):
        from google.cloud.bigtable_admin_v2.gapic import enums

        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._state = enums.Backup.State.READY
        self.assertEqual(backup.state, expected)

    def test___eq__(self):
        instance = object()
        backup1 = self._make_one(self.BACKUP_ID, instance)
        backup2 = self._make_one(self.BACKUP_ID, instance)
        self.assertTrue(backup1 == backup2)

    def test___eq__different_types(self):
        instance = object()
        backup1 = self._make_one(self.BACKUP_ID, instance)
        backup2 = object()
        self.assertFalse(backup1 == backup2)

    def test___ne__same_value(self):
        instance = object()
        backup1 = self._make_one(self.BACKUP_ID, instance)
        backup2 = self._make_one(self.BACKUP_ID, instance)
        self.assertFalse(backup1 != backup2)

    def test___ne__(self):
        backup1 = self._make_one("backup_1", "instance1")
        backup2 = self._make_one("backup_2", "instance2")
        self.assertTrue(backup1 != backup2)

    def test_create_grpc_error(self):
        from google.api_core.exceptions import GoogleAPICallError
        from google.api_core.exceptions import Unknown
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.types import table_pb2

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.create_backup.side_effect = Unknown("testing")

        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            table_id=self.TABLE_ID,
            expire_time=timestamp,
        )

        backup_pb = table_pb2.Backup(
            source_table=self.TABLE_NAME,
            expire_time=_datetime_to_pb_timestamp(timestamp),
        )

        with self.assertRaises(GoogleAPICallError):
            backup.create(self.CLUSTER_ID)

        api.create_backup.assert_called_once_with(
            parent=self.CLUSTER_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
        )

    def test_create_already_exists(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.types import table_pb2
        from google.cloud.exceptions import Conflict

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.create_backup.side_effect = Conflict("testing")

        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            table_id=self.TABLE_ID,
            expire_time=timestamp,
        )

        backup_pb = table_pb2.Backup(
            source_table=self.TABLE_NAME,
            expire_time=_datetime_to_pb_timestamp(timestamp),
        )

        with self.assertRaises(Conflict):
            backup.create(self.CLUSTER_ID)

        api.create_backup.assert_called_once_with(
            parent=self.CLUSTER_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
        )

    def test_create_instance_not_found(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.types import table_pb2
        from google.cloud.exceptions import NotFound

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.create_backup.side_effect = NotFound("testing")

        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            table_id=self.TABLE_ID,
            expire_time=timestamp,
        )

        backup_pb = table_pb2.Backup(
            source_table=self.TABLE_NAME,
            expire_time=_datetime_to_pb_timestamp(timestamp),
        )

        with self.assertRaises(NotFound):
            backup.create(self.CLUSTER_ID)

        api.create_backup.assert_called_once_with(
            parent=self.CLUSTER_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
        )

    def test_create_cluster_not_set(self):
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME),
            table_id=self.TABLE_ID,
            expire_time=self._make_timestamp(),
        )

        with self.assertRaises(ValueError):
            backup.create()

    def test_create_table_not_set(self):
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME),
            expire_time=self._make_timestamp(),
        )

        with self.assertRaises(ValueError):
            backup.create(self.CLUSTER_ID)

    def test_create_expire_time_not_set(self):
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME),
            table_id=self.TABLE_ID,
        )

        with self.assertRaises(ValueError):
            backup.create(self.CLUSTER_ID)

    def test_create_success(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.types import table_pb2

        op_future = object()
        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.create_backup.return_value = op_future

        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            table_id=self.TABLE_ID,
            expire_time=timestamp,
        )

        backup_pb = table_pb2.Backup(
            source_table=self.TABLE_NAME,
            expire_time=_datetime_to_pb_timestamp(timestamp),
        )

        future = backup.create(self.CLUSTER_ID)
        self.assertEqual(backup._cluster, self.CLUSTER_ID)
        self.assertIs(future, op_future)

        api.create_backup.assert_called_once_with(
            parent=self.CLUSTER_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
        )

    def test_exists_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.get_backup.side_effect = Unknown("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        with self.assertRaises(Unknown):
            backup.exists()

        api.get_backup.assert_called_once_with(self.BACKUP_NAME)

    def test_exists_not_found(self):
        from google.api_core.exceptions import NotFound

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.get_backup.side_effect = NotFound("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        self.assertFalse(backup.exists())

        api.get_backup.assert_called_once_with(self.BACKUP_NAME)

    def test_get(self):
        from google.cloud.bigtable_admin_v2.gapic import enums
        from google.cloud.bigtable_admin_v2.proto import table_pb2
        from google.cloud._helpers import _datetime_to_pb_timestamp

        timestamp = _datetime_to_pb_timestamp(self._make_timestamp())
        state = enums.Backup.State.READY

        client = _Client()
        backup_pb = table_pb2.Backup(
            name=self.BACKUP_NAME,
            source_table=self.TABLE_NAME,
            expire_time=timestamp,
            start_time=timestamp,
            end_time=timestamp,
            size_bytes=0,
            state=state,
        )
        api = client.table_admin_client = self._make_table_admin_client()
        api.get_backup.return_value = backup_pb

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        self.assertEqual(backup.get(), backup_pb)

    def test_reload(self):
        from google.cloud.bigtable_admin_v2.gapic import enums
        from google.cloud.bigtable_admin_v2.proto import table_pb2
        from google.cloud._helpers import _datetime_to_pb_timestamp

        timestamp = _datetime_to_pb_timestamp(self._make_timestamp())
        state = enums.Backup.State.READY

        client = _Client()
        backup_pb = table_pb2.Backup(
            name=self.BACKUP_NAME,
            source_table=self.TABLE_NAME,
            expire_time=timestamp,
            start_time=timestamp,
            end_time=timestamp,
            size_bytes=0,
            state=state,
        )
        api = client.table_admin_client = self._make_table_admin_client()
        api.get_backup.return_value = backup_pb

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        backup.reload()
        self.assertEqual(backup._source_table, self.TABLE_NAME)
        self.assertEqual(backup._expire_time, timestamp)
        self.assertEqual(backup._start_time, timestamp)
        self.assertEqual(backup._end_time, timestamp)
        self.assertEqual(backup._size_bytes, 0)
        self.assertEqual(backup._state, state)

    def test_exists_success(self):
        from google.cloud.bigtable_admin_v2.proto import table_pb2

        client = _Client()
        backup_pb = table_pb2.Backup(name=self.BACKUP_NAME)
        api = client.table_admin_client = self._make_table_admin_client()
        api.get_backup.return_value = backup_pb

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        self.assertTrue(backup.exists())

        api.get_backup.assert_called_once_with(self.BACKUP_NAME)

    def test_delete_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.delete_backup.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        with self.assertRaises(Unknown):
            backup.delete()

        api.delete_backup.assert_called_once_with(self.BACKUP_NAME)

    def test_delete_not_found(self):
        from google.api_core.exceptions import NotFound

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.delete_backup.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        with self.assertRaises(NotFound):
            backup.delete()

        api.delete_backup.assert_called_once_with(self.BACKUP_NAME)

    def test_delete_success(self):
        from google.protobuf.empty_pb2 import Empty

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.delete_backup.return_value = Empty()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        backup.delete()

        api.delete_backup.assert_called_once_with(self.BACKUP_NAME)

    def test_update_expire_time_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.types import table_pb2
        from google.protobuf import field_mask_pb2

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.update_backup.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)
        expire_time = self._make_timestamp()

        with self.assertRaises(Unknown):
            backup.update_expire_time(expire_time)

        backup_update = table_pb2.Backup(
            name=self.BACKUP_NAME,
            expire_time=_datetime_to_pb_timestamp(expire_time),
        )
        update_mask = field_mask_pb2.FieldMask(paths=["expire_time"])
        api.update_backup.assert_called_once_with(
            backup_update,
            update_mask,
        )

    def test_update_expire_time_not_found(self):
        from google.api_core.exceptions import NotFound
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.types import table_pb2
        from google.protobuf import field_mask_pb2

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.update_backup.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)
        expire_time = self._make_timestamp()

        with self.assertRaises(NotFound):
            backup.update_expire_time(expire_time)

        backup_update = table_pb2.Backup(
            name=self.BACKUP_NAME,
            expire_time=_datetime_to_pb_timestamp(expire_time),
        )
        update_mask = field_mask_pb2.FieldMask(paths=["expire_time"])
        api.update_backup.assert_called_once_with(
            backup_update,
            update_mask,
        )

    def test_update_expire_time_success(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.proto import table_pb2
        from google.protobuf import field_mask_pb2

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.update_backup.return_type = table_pb2.Backup(name=self.BACKUP_NAME)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)
        expire_time = self._make_timestamp()

        backup.update_expire_time(expire_time)

        backup_update = table_pb2.Backup(
            name=self.BACKUP_NAME,
            expire_time=_datetime_to_pb_timestamp(expire_time),
        )
        update_mask = field_mask_pb2.FieldMask(paths=["expire_time"])
        api.update_backup.assert_called_once_with(
            backup_update,
            update_mask,
        )

    def test_restore_grpc_error(self):
        from google.api_core.exceptions import GoogleAPICallError
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.restore_table.side_effect = Unknown("testing")

        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            cluster_id=self.CLUSTER_ID,
            table_id=self.TABLE_NAME,
            expire_time=timestamp,
        )

        with self.assertRaises(GoogleAPICallError):
            backup.restore(self.TABLE_ID)

        api.restore_table.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            table_id=self.TABLE_ID,
            backup=self.BACKUP_NAME,
        )

    def test_restore_cluster_not_set(self):
        client = _Client()
        client.table_admin_client = self._make_table_admin_client()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            table_id=self.TABLE_ID,
            expire_time=self._make_timestamp(),
        )

        with self.assertRaises(ValueError):
            backup.restore(self.TABLE_ID)

    def test_restore_success(self):
        op_future = object()
        client = _Client()
        api = client.table_admin_client = self._make_table_admin_client()
        api.restore_table.return_value = op_future

        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID,
            _Instance(self.INSTANCE_NAME, client=client),
            cluster_id=self.CLUSTER_ID,
            table_id=self.TABLE_NAME,
            expire_time=timestamp,
        )

        future = backup.restore(self.TABLE_ID)
        self.assertEqual(backup._cluster, self.CLUSTER_ID)
        self.assertIs(future, op_future)

        api.restore_table.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            table_id=self.TABLE_ID,
            backup=self.BACKUP_NAME,
        )

    def test_get_iam_policy(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)

        instance = client.instance(instance_id=self.INSTANCE_ID)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        version = 1
        etag = b"etag_v1"
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        bindings = [{"role": BIGTABLE_ADMIN_ROLE, "members": members}]
        iam_policy = policy_pb2.Policy(version=version, etag=etag, bindings=bindings)

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        client._table_admin_client = table_api
        table_api.get_iam_policy.return_value = iam_policy

        result = backup.get_iam_policy()

        table_api.get_iam_policy.assert_called_once_with(resource=backup.name)
        self.assertEqual(result.version, version)
        self.assertEqual(result.etag, etag)

        admins = result.bigtable_admins
        self.assertEqual(len(admins), len(members))
        for found, expected in zip(sorted(admins), sorted(members)):
            self.assertEqual(found, expected)

    def test_set_iam_policy(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import Policy
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)

        instance = client.instance(instance_id=self.INSTANCE_ID)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        version = 1
        etag = b"etag_v1"
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        bindings = [{"role": BIGTABLE_ADMIN_ROLE, "members": sorted(members)}]
        iam_policy_pb = policy_pb2.Policy(version=version, etag=etag, bindings=bindings)

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        client._table_admin_client = table_api
        table_api.set_iam_policy.return_value = iam_policy_pb

        iam_policy = Policy(etag=etag, version=version)
        iam_policy[BIGTABLE_ADMIN_ROLE] = [
            Policy.user("user1@test.com"),
            Policy.service_account("service_acc1@test.com"),
        ]

        result = backup.set_iam_policy(iam_policy)

        table_api.set_iam_policy.assert_called_once_with(
            resource=backup.name, policy=iam_policy_pb
        )
        self.assertEqual(result.version, version)
        self.assertEqual(result.etag, etag)

        admins = result.bigtable_admins
        self.assertEqual(len(admins), len(members))
        for found, expected in zip(sorted(admins), sorted(members)):
            self.assertEqual(found, expected)

    def test_test_iam_permissions(self):
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.iam.v1 import iam_policy_pb2

        credentials = _make_credentials()
        client = Client(project=self.PROJECT_ID, credentials=credentials, admin=True)

        instance = client.instance(instance_id=self.INSTANCE_ID)
        backup = self._make_one(self.BACKUP_ID, instance, cluster_id=self.CLUSTER_ID)

        permissions = ["bigtable.backups.create", "bigtable.backups.list"]

        response = iam_policy_pb2.TestIamPermissionsResponse(permissions=permissions)

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        table_api.test_iam_permissions.return_value = response
        client._table_admin_client = table_api

        result = backup.test_iam_permissions(permissions)

        self.assertEqual(result, permissions)
        table_api.test_iam_permissions.assert_called_once_with(
            resource=backup.name, permissions=permissions
        )


class _Client(object):
    def __init__(self, project=TestBackup.PROJECT_ID):
        self.project = project
        self.project_name = "projects/" + self.project


class _Instance(object):
    def __init__(self, name, client=None):
        self.name = name
        self.instance_id = name.rsplit("/", 1)[1]
        self._client = client
