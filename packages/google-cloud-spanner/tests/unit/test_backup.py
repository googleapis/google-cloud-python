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


import unittest

import mock


class _BaseTest(unittest.TestCase):
    PROJECT_ID = "project-id"
    PARENT = "projects/" + PROJECT_ID
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = PARENT + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database_id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    BACKUP_ID = "backup_id"
    BACKUP_NAME = INSTANCE_NAME + "/backups/" + BACKUP_ID

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _make_timestamp():
        import datetime
        from google.cloud._helpers import UTC

        return datetime.datetime.utcnow().replace(tzinfo=UTC)


class TestBackup(_BaseTest):
    def _get_target_class(self):
        from google.cloud.spanner_v1.backup import Backup

        return Backup

    @staticmethod
    def _make_database_admin_api():
        from google.cloud.spanner_admin_database_v1 import DatabaseAdminClient

        return mock.create_autospec(DatabaseAdminClient, instance=True)

    def test_ctor_defaults(self):
        instance = _Instance(self.INSTANCE_NAME)

        backup = self._make_one(self.BACKUP_ID, instance)

        self.assertEqual(backup.backup_id, self.BACKUP_ID)
        self.assertIs(backup._instance, instance)
        self.assertEqual(backup._database, "")
        self.assertIsNone(backup._expire_time)

    def test_ctor_non_defaults(self):
        instance = _Instance(self.INSTANCE_NAME)
        timestamp = self._make_timestamp()

        backup = self._make_one(
            self.BACKUP_ID, instance, database=self.DATABASE_NAME, expire_time=timestamp
        )

        self.assertEqual(backup.backup_id, self.BACKUP_ID)
        self.assertIs(backup._instance, instance)
        self.assertEqual(backup._database, self.DATABASE_NAME)
        self.assertIsNotNone(backup._expire_time)
        self.assertIs(backup._expire_time, timestamp)

    def test_from_pb_project_mismatch(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        ALT_PROJECT = "ALT_PROJECT"
        client = _Client(project=ALT_PROJECT)
        instance = _Instance(self.INSTANCE_NAME, client)
        backup_pb = Backup(name=self.BACKUP_NAME)
        backup_class = self._get_target_class()

        with self.assertRaises(ValueError):
            backup_class.from_pb(backup_pb, instance)

    def test_from_pb_instance_mismatch(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        ALT_INSTANCE = "/projects/%s/instances/ALT-INSTANCE" % (self.PROJECT_ID,)
        client = _Client()
        instance = _Instance(ALT_INSTANCE, client)
        backup_pb = Backup(name=self.BACKUP_NAME)
        backup_class = self._get_target_class()

        with self.assertRaises(ValueError):
            backup_class.from_pb(backup_pb, instance)

    def test_from_pb_invalid_name(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        backup_pb = Backup(name="invalid_format")
        backup_class = self._get_target_class()

        with self.assertRaises(ValueError):
            backup_class.from_pb(backup_pb, instance)

    def test_from_pb_success(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        backup_pb = Backup(name=self.BACKUP_NAME)
        backup_class = self._get_target_class()

        backup = backup_class.from_pb(backup_pb, instance)

        self.assertIsInstance(backup, backup_class)
        self.assertEqual(backup._instance, instance)
        self.assertEqual(backup.backup_id, self.BACKUP_ID)
        self.assertEqual(backup._database, "")
        self.assertIsNone(backup._expire_time)

    def test_name_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected_name = self.BACKUP_NAME
        self.assertEqual(backup.name, expected_name)

    def test_database_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._database = self.DATABASE_NAME
        self.assertEqual(backup.database, expected)

    def test_expire_time_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._expire_time = self._make_timestamp()
        self.assertEqual(backup.expire_time, expected)

    def test_create_time_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._create_time = self._make_timestamp()
        self.assertEqual(backup.create_time, expected)

    def test_size_bytes_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._size_bytes = 10
        self.assertEqual(backup.size_bytes, expected)

    def test_state_property(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._state = Backup.State.READY
        self.assertEqual(backup.state, expected)

    def test_referencing_databases_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance)
        expected = backup._referencing_databases = [self.DATABASE_NAME]
        self.assertEqual(backup.referencing_databases, expected)

    def test_create_grpc_error(self):
        from google.api_core.exceptions import GoogleAPICallError
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_backup.side_effect = Unknown("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID, instance, database=self.DATABASE_NAME, expire_time=timestamp
        )

        backup_pb = Backup(database=self.DATABASE_NAME, expire_time=timestamp,)

        with self.assertRaises(GoogleAPICallError):
            backup.create()

        api.create_backup.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_create_already_exists(self):
        from google.cloud.exceptions import Conflict
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_backup.side_effect = Conflict("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID, instance, database=self.DATABASE_NAME, expire_time=timestamp
        )

        backup_pb = Backup(database=self.DATABASE_NAME, expire_time=timestamp,)

        with self.assertRaises(Conflict):
            backup.create()

        api.create_backup.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_create_instance_not_found(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_backup.side_effect = NotFound("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID, instance, database=self.DATABASE_NAME, expire_time=timestamp
        )

        backup_pb = Backup(database=self.DATABASE_NAME, expire_time=timestamp,)

        with self.assertRaises(NotFound):
            backup.create()

        api.create_backup.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_create_expire_time_not_set(self):
        instance = _Instance(self.INSTANCE_NAME)
        backup = self._make_one(self.BACKUP_ID, instance, database=self.DATABASE_NAME)

        with self.assertRaises(ValueError):
            backup.create()

    def test_create_database_not_set(self):
        instance = _Instance(self.INSTANCE_NAME)
        timestamp = self._make_timestamp()
        backup = self._make_one(self.BACKUP_ID, instance, expire_time=timestamp)

        with self.assertRaises(ValueError):
            backup.create()

    def test_create_success(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_backup.return_value = op_future

        instance = _Instance(self.INSTANCE_NAME, client=client)
        timestamp = self._make_timestamp()
        backup = self._make_one(
            self.BACKUP_ID, instance, database=self.DATABASE_NAME, expire_time=timestamp
        )

        backup_pb = Backup(database=self.DATABASE_NAME, expire_time=timestamp,)

        future = backup.create()
        self.assertIs(future, op_future)

        api.create_backup.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            backup_id=self.BACKUP_ID,
            backup=backup_pb,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_exists_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_backup.side_effect = Unknown("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        with self.assertRaises(Unknown):
            backup.exists()

        api.get_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_exists_not_found(self):
        from google.api_core.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_backup.side_effect = NotFound("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        self.assertFalse(backup.exists())

        api.get_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_exists_success(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        backup_pb = Backup(name=self.BACKUP_NAME)
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_backup.return_value = backup_pb

        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        self.assertTrue(backup.exists())

        api.get_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_delete_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.delete_backup.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        with self.assertRaises(Unknown):
            backup.delete()

        api.delete_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_delete_not_found(self):
        from google.api_core.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.delete_backup.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        with self.assertRaises(NotFound):
            backup.delete()

        api.delete_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_delete_success(self):
        from google.protobuf.empty_pb2 import Empty

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.delete_backup.return_value = Empty()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        backup.delete()

        api.delete_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_reload_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_backup.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        with self.assertRaises(Unknown):
            backup.reload()

        api.get_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_reload_not_found(self):
        from google.api_core.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_backup.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        with self.assertRaises(NotFound):
            backup.reload()

        api.get_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_reload_success(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        timestamp = self._make_timestamp()

        client = _Client()
        backup_pb = Backup(
            name=self.BACKUP_NAME,
            database=self.DATABASE_NAME,
            expire_time=timestamp,
            create_time=timestamp,
            size_bytes=10,
            state=1,
            referencing_databases=[],
        )
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_backup.return_value = backup_pb
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)

        backup.reload()
        self.assertEqual(backup.name, self.BACKUP_NAME)
        self.assertEqual(backup.database, self.DATABASE_NAME)
        self.assertEqual(backup.expire_time, timestamp)
        self.assertEqual(backup.create_time, timestamp)
        self.assertEqual(backup.size_bytes, 10)
        self.assertEqual(backup.state, Backup.State.CREATING)
        self.assertEqual(backup.referencing_databases, [])

        api.get_backup.assert_called_once_with(
            name=self.BACKUP_NAME,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_update_expire_time_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_backup.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)
        expire_time = self._make_timestamp()

        with self.assertRaises(Unknown):
            backup.update_expire_time(expire_time)

        backup_update = Backup(name=self.BACKUP_NAME, expire_time=expire_time,)
        update_mask = {"paths": ["expire_time"]}
        api.update_backup.assert_called_once_with(
            backup=backup_update,
            update_mask=update_mask,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_update_expire_time_not_found(self):
        from google.api_core.exceptions import NotFound
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_backup.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)
        expire_time = self._make_timestamp()

        with self.assertRaises(NotFound):
            backup.update_expire_time(expire_time)

        backup_update = Backup(name=self.BACKUP_NAME, expire_time=expire_time,)
        update_mask = {"paths": ["expire_time"]}
        api.update_backup.assert_called_once_with(
            backup=backup_update,
            update_mask=update_mask,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_update_expire_time_success(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_backup.return_type = Backup(name=self.BACKUP_NAME)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)
        expire_time = self._make_timestamp()

        backup.update_expire_time(expire_time)

        backup_update = Backup(name=self.BACKUP_NAME, expire_time=expire_time,)
        update_mask = {"paths": ["expire_time"]}
        api.update_backup.assert_called_once_with(
            backup=backup_update,
            update_mask=update_mask,
            metadata=[("google-cloud-resource-prefix", backup.name)],
        )

    def test_is_ready(self):
        from google.cloud.spanner_admin_database_v1 import Backup

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        backup = self._make_one(self.BACKUP_ID, instance)
        backup._state = Backup.State.READY
        self.assertTrue(backup.is_ready())
        backup._state = Backup.State.CREATING
        self.assertFalse(backup.is_ready())


class _Client(object):
    def __init__(self, project=TestBackup.PROJECT_ID):
        self.project = project
        self.project_name = "projects/" + self.project


class _Instance(object):
    def __init__(self, name, client=None):
        self.name = name
        self.instance_id = name.rsplit("/", 1)[1]
        self._client = client
