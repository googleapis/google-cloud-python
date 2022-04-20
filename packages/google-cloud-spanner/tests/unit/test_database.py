# Copyright 2016 Google LLC All rights reserved.
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
from google.api_core import gapic_v1
from google.cloud.spanner_v1.param_types import INT64
from google.api_core.retry import Retry

from google.cloud.spanner_v1 import RequestOptions

DML_WO_PARAM = """
DELETE FROM citizens
"""

DML_W_PARAM = """
INSERT INTO citizens(first_name, last_name, age)
VALUES ("Phred", "Phlyntstone", @age)
"""
PARAMS = {"age": 30}
PARAM_TYPES = {"age": INT64}
MODE = 2  # PROFILE


def _make_credentials():  # pragma: NO COVER
    import google.auth.credentials

    class _CredentialsWithScopes(
        google.auth.credentials.Credentials, google.auth.credentials.Scoped
    ):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class _BaseTest(unittest.TestCase):

    PROJECT_ID = "project-id"
    PARENT = "projects/" + PROJECT_ID
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = PARENT + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database_id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    SESSION_ID = "session_id"
    SESSION_NAME = DATABASE_NAME + "/sessions/" + SESSION_ID
    TRANSACTION_ID = b"transaction_id"
    RETRY_TRANSACTION_ID = b"transaction_id_retry"
    BACKUP_ID = "backup_id"
    BACKUP_NAME = INSTANCE_NAME + "/backups/" + BACKUP_ID
    TRANSACTION_TAG = "transaction-tag"

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _make_timestamp():
        import datetime
        from google.cloud._helpers import UTC

        return datetime.datetime.utcnow().replace(tzinfo=UTC)

    @staticmethod
    def _make_duration(seconds=1, microseconds=0):
        import datetime

        return datetime.timedelta(seconds=seconds, microseconds=microseconds)


class TestDatabase(_BaseTest):
    def _get_target_class(self):
        from google.cloud.spanner_v1.database import Database

        return Database

    @staticmethod
    def _make_database_admin_api():
        from google.cloud.spanner_v1.client import DatabaseAdminClient

        return mock.create_autospec(DatabaseAdminClient, instance=True)

    @staticmethod
    def _make_spanner_api():
        from google.cloud.spanner_v1 import SpannerClient

        return mock.create_autospec(SpannerClient, instance=True)

    def test_ctor_defaults(self):
        from google.cloud.spanner_v1.pool import BurstyPool

        instance = _Instance(self.INSTANCE_NAME)

        database = self._make_one(self.DATABASE_ID, instance)

        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertIsInstance(database._pool, BurstyPool)
        self.assertFalse(database.log_commit_stats)
        self.assertIsNone(database._logger)
        # BurstyPool does not create sessions during 'bind()'.
        self.assertTrue(database._pool._sessions.empty())

    def test_ctor_w_explicit_pool(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertIs(database._pool, pool)
        self.assertIs(pool._bound, database)

    def test_ctor_w_ddl_statements_non_string(self):

        with self.assertRaises(ValueError):
            self._make_one(
                self.DATABASE_ID, instance=object(), ddl_statements=[object()]
            )

    def test_ctor_w_ddl_statements_w_create_database(self):

        with self.assertRaises(ValueError):
            self._make_one(
                self.DATABASE_ID,
                instance=object(),
                ddl_statements=["CREATE DATABASE foo"],
            )

    def test_ctor_w_ddl_statements_ok(self):
        from tests._fixtures import DDL_STATEMENTS

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(
            self.DATABASE_ID, instance, ddl_statements=DDL_STATEMENTS, pool=pool
        )
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(list(database.ddl_statements), DDL_STATEMENTS)

    def test_ctor_w_explicit_logger(self):
        from logging import Logger

        instance = _Instance(self.INSTANCE_NAME)
        logger = mock.create_autospec(Logger, instance=True)
        database = self._make_one(self.DATABASE_ID, instance, logger=logger)
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertFalse(database.log_commit_stats)
        self.assertEqual(database._logger, logger)

    def test_ctor_w_encryption_config(self):
        from google.cloud.spanner_admin_database_v1 import EncryptionConfig

        instance = _Instance(self.INSTANCE_NAME)
        encryption_config = EncryptionConfig(kms_key_name="kms_key")
        database = self._make_one(
            self.DATABASE_ID, instance, encryption_config=encryption_config
        )
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(database._encryption_config, encryption_config)

    def test_from_pb_bad_database_name(self):
        from google.cloud.spanner_admin_database_v1 import Database

        database_name = "INCORRECT_FORMAT"
        database_pb = Database(name=database_name)
        klass = self._get_target_class()

        with self.assertRaises(ValueError):
            klass.from_pb(database_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.spanner_admin_database_v1 import Database

        ALT_PROJECT = "ALT_PROJECT"
        client = _Client(project=ALT_PROJECT)
        instance = _Instance(self.INSTANCE_NAME, client)
        database_pb = Database(name=self.DATABASE_NAME)
        klass = self._get_target_class()

        with self.assertRaises(ValueError):
            klass.from_pb(database_pb, instance)

    def test_from_pb_instance_mistmatch(self):
        from google.cloud.spanner_admin_database_v1 import Database

        ALT_INSTANCE = "/projects/%s/instances/ALT-INSTANCE" % (self.PROJECT_ID,)
        client = _Client()
        instance = _Instance(ALT_INSTANCE, client)
        database_pb = Database(name=self.DATABASE_NAME)
        klass = self._get_target_class()

        with self.assertRaises(ValueError):
            klass.from_pb(database_pb, instance)

    def test_from_pb_success_w_explicit_pool(self):
        from google.cloud.spanner_admin_database_v1 import Database

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        database_pb = Database(name=self.DATABASE_NAME)
        klass = self._get_target_class()
        pool = _Pool()

        database = klass.from_pb(database_pb, instance, pool=pool)

        self.assertIsInstance(database, klass)
        self.assertEqual(database._instance, instance)
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._pool, pool)

    def test_from_pb_success_w_hyphen_w_default_pool(self):
        from google.cloud.spanner_admin_database_v1 import Database
        from google.cloud.spanner_v1.pool import BurstyPool

        DATABASE_ID_HYPHEN = "database-id"
        DATABASE_NAME_HYPHEN = self.INSTANCE_NAME + "/databases/" + DATABASE_ID_HYPHEN
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        database_pb = Database(name=DATABASE_NAME_HYPHEN)
        klass = self._get_target_class()

        database = klass.from_pb(database_pb, instance)

        self.assertIsInstance(database, klass)
        self.assertEqual(database._instance, instance)
        self.assertEqual(database.database_id, DATABASE_ID_HYPHEN)
        self.assertIsInstance(database._pool, BurstyPool)
        # BurstyPool does not create sessions during 'bind()'.
        self.assertTrue(database._pool._sessions.empty())

    def test_name_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        expected_name = self.DATABASE_NAME
        self.assertEqual(database.name, expected_name)

    def test_create_time_property(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        expected_create_time = database._create_time = self._make_timestamp()
        self.assertEqual(database.create_time, expected_create_time)

    def test_state_property(self):
        from google.cloud.spanner_admin_database_v1 import Database

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        expected_state = database._state = Database.State.READY
        self.assertEqual(database.state, expected_state)

    def test_restore_info(self):
        from google.cloud.spanner_admin_database_v1 import RestoreInfo

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        restore_info = database._restore_info = mock.create_autospec(
            RestoreInfo, instance=True
        )
        self.assertEqual(database.restore_info, restore_info)

    def test_version_retention_period(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        version_retention_period = database._version_retention_period = "1d"
        self.assertEqual(database.version_retention_period, version_retention_period)

    def test_earliest_version_time(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        earliest_version_time = database._earliest_version_time = self._make_timestamp()
        self.assertEqual(database.earliest_version_time, earliest_version_time)

    def test_logger_property_default(self):
        import logging

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        logger = logging.getLogger(database.name)
        self.assertEqual(database.logger, logger)

    def test_logger_property_custom(self):
        import logging

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        logger = database._logger = mock.create_autospec(logging.Logger, instance=True)
        self.assertEqual(database.logger, logger)

    def test_encryption_config(self):
        from google.cloud.spanner_admin_database_v1 import EncryptionConfig

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        encryption_config = database._encryption_config = mock.create_autospec(
            EncryptionConfig, instance=True
        )
        self.assertEqual(database.encryption_config, encryption_config)

    def test_encryption_info(self):
        from google.cloud.spanner_admin_database_v1 import EncryptionInfo

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        encryption_info = database._encryption_info = [
            mock.create_autospec(EncryptionInfo, instance=True)
        ]
        self.assertEqual(database.encryption_info, encryption_info)

    def test_default_leader(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        default_leader = database._default_leader = "us-east4"
        self.assertEqual(database.default_leader, default_leader)

    def test_spanner_api_property_w_scopeless_creds(self):

        client = _Client()
        client_info = client._client_info = mock.Mock()
        client_options = client._client_options = mock.Mock()
        credentials = client.credentials = object()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        patch = mock.patch("google.cloud.spanner_v1.database.SpannerClient")

        with patch as spanner_client:
            api = database.spanner_api

        self.assertIs(api, spanner_client.return_value)

        # API instance is cached
        again = database.spanner_api
        self.assertIs(again, api)

        spanner_client.assert_called_once_with(
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )

    def test_spanner_api_w_scoped_creds(self):
        import google.auth.credentials
        from google.cloud.spanner_v1.database import SPANNER_DATA_SCOPE

        class _CredentialsWithScopes(google.auth.credentials.Scoped):
            def __init__(self, scopes=(), source=None):
                self._scopes = scopes
                self._source = source

            def requires_scopes(self):  # pragma: NO COVER
                return True

            def with_scopes(self, scopes):
                return self.__class__(scopes, self)

        expected_scopes = (SPANNER_DATA_SCOPE,)
        client = _Client()
        client_info = client._client_info = mock.Mock()
        client_options = client._client_options = mock.Mock()
        credentials = client.credentials = _CredentialsWithScopes()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        patch = mock.patch("google.cloud.spanner_v1.database.SpannerClient")

        with patch as spanner_client:
            api = database.spanner_api

        # API instance is cached
        again = database.spanner_api
        self.assertIs(again, api)

        self.assertEqual(len(spanner_client.call_args_list), 1)
        called_args, called_kw = spanner_client.call_args
        self.assertEqual(called_args, ())
        self.assertEqual(called_kw["client_info"], client_info)
        self.assertEqual(called_kw["client_options"], client_options)
        scoped = called_kw["credentials"]
        self.assertEqual(scoped._scopes, expected_scopes)
        self.assertIs(scoped._source, credentials)

    def test_spanner_api_w_emulator_host(self):
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client, emulator_host="host")
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        patch = mock.patch("google.cloud.spanner_v1.database.SpannerClient")
        with patch as spanner_client:
            api = database.spanner_api

        self.assertIs(api, spanner_client.return_value)

        # API instance is cached
        again = database.spanner_api
        self.assertIs(again, api)

        self.assertEqual(len(spanner_client.call_args_list), 1)
        called_args, called_kw = spanner_client.call_args
        self.assertEqual(called_args, ())
        self.assertIsNotNone(called_kw["transport"])

    def test___eq__(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool1, pool2 = _Pool(), _Pool()
        database1 = self._make_one(self.DATABASE_ID, instance, pool=pool1)
        database2 = self._make_one(self.DATABASE_ID, instance, pool=pool2)
        self.assertEqual(database1, database2)

    def test___eq__type_differ(self):
        pool = _Pool()
        database1 = self._make_one(self.DATABASE_ID, None, pool=pool)
        database2 = object()
        self.assertNotEqual(database1, database2)

    def test___ne__same_value(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool1, pool2 = _Pool(), _Pool()
        database1 = self._make_one(self.DATABASE_ID, instance, pool=pool1)
        database2 = self._make_one(self.DATABASE_ID, instance, pool=pool2)
        comparison_val = database1 != database2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        pool1, pool2 = _Pool(), _Pool()
        database1 = self._make_one("database_id1", "instance1", pool=pool1)
        database2 = self._make_one("database_id2", "instance2", pool=pool2)
        self.assertNotEqual(database1, database2)

    def test_create_grpc_error(self):
        from google.api_core.exceptions import GoogleAPICallError
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_admin_database_v1 import CreateDatabaseRequest

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_database.side_effect = Unknown("testing")

        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(GoogleAPICallError):
            database.create()

        expected_request = CreateDatabaseRequest(
            parent=self.INSTANCE_NAME,
            create_statement="CREATE DATABASE {}".format(self.DATABASE_ID),
            extra_statements=[],
            encryption_config=None,
        )

        api.create_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_create_already_exists(self):
        from google.cloud.exceptions import Conflict
        from google.cloud.spanner_admin_database_v1 import CreateDatabaseRequest

        DATABASE_ID_HYPHEN = "database-id"
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_database.side_effect = Conflict("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(DATABASE_ID_HYPHEN, instance, pool=pool)

        with self.assertRaises(Conflict):
            database.create()

        expected_request = CreateDatabaseRequest(
            parent=self.INSTANCE_NAME,
            create_statement="CREATE DATABASE `{}`".format(DATABASE_ID_HYPHEN),
            extra_statements=[],
            encryption_config=None,
        )

        api.create_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_create_instance_not_found(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.spanner_admin_database_v1 import CreateDatabaseRequest

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_database.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.create()

        expected_request = CreateDatabaseRequest(
            parent=self.INSTANCE_NAME,
            create_statement="CREATE DATABASE {}".format(self.DATABASE_ID),
            extra_statements=[],
            encryption_config=None,
        )

        api.create_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_create_success(self):
        from tests._fixtures import DDL_STATEMENTS
        from google.cloud.spanner_admin_database_v1 import CreateDatabaseRequest
        from google.cloud.spanner_admin_database_v1 import EncryptionConfig

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_database.return_value = op_future
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        encryption_config = EncryptionConfig(kms_key_name="kms_key_name")
        database = self._make_one(
            self.DATABASE_ID,
            instance,
            ddl_statements=DDL_STATEMENTS,
            pool=pool,
            encryption_config=encryption_config,
        )

        future = database.create()

        self.assertIs(future, op_future)

        expected_request = CreateDatabaseRequest(
            parent=self.INSTANCE_NAME,
            create_statement="CREATE DATABASE {}".format(self.DATABASE_ID),
            extra_statements=DDL_STATEMENTS,
            encryption_config=encryption_config,
        )

        api.create_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_create_success_w_encryption_config_dict(self):
        from tests._fixtures import DDL_STATEMENTS
        from google.cloud.spanner_admin_database_v1 import CreateDatabaseRequest
        from google.cloud.spanner_admin_database_v1 import EncryptionConfig

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.create_database.return_value = op_future
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        encryption_config = {"kms_key_name": "kms_key_name"}
        database = self._make_one(
            self.DATABASE_ID,
            instance,
            ddl_statements=DDL_STATEMENTS,
            pool=pool,
            encryption_config=encryption_config,
        )

        future = database.create()

        self.assertIs(future, op_future)

        expected_encryption_config = EncryptionConfig(**encryption_config)
        expected_request = CreateDatabaseRequest(
            parent=self.INSTANCE_NAME,
            create_statement="CREATE DATABASE {}".format(self.DATABASE_ID),
            extra_statements=DDL_STATEMENTS,
            encryption_config=expected_encryption_config,
        )

        api.create_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_exists_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_database_ddl.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(Unknown):
            database.exists()

        api.get_database_ddl.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_exists_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_database_ddl.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        self.assertFalse(database.exists())

        api.get_database_ddl.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_exists_success(self):
        from google.cloud.spanner_admin_database_v1 import GetDatabaseDdlResponse
        from tests._fixtures import DDL_STATEMENTS

        client = _Client()
        ddl_pb = GetDatabaseDdlResponse(statements=DDL_STATEMENTS)
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_database_ddl.return_value = ddl_pb
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        self.assertTrue(database.exists())

        api.get_database_ddl.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_reload_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_database_ddl.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(Unknown):
            database.reload()

        api.get_database_ddl.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_reload_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_database_ddl.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.reload()

        api.get_database_ddl.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_reload_success(self):
        from google.cloud.spanner_admin_database_v1 import Database
        from google.cloud.spanner_admin_database_v1 import EncryptionConfig
        from google.cloud.spanner_admin_database_v1 import EncryptionInfo
        from google.cloud.spanner_admin_database_v1 import GetDatabaseDdlResponse
        from google.cloud.spanner_admin_database_v1 import RestoreInfo
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from tests._fixtures import DDL_STATEMENTS

        timestamp = self._make_timestamp()
        restore_info = RestoreInfo()

        client = _Client()
        ddl_pb = GetDatabaseDdlResponse(statements=DDL_STATEMENTS)
        encryption_config = EncryptionConfig(kms_key_name="kms_key")
        encryption_info = [
            EncryptionInfo(
                encryption_type=EncryptionInfo.Type.CUSTOMER_MANAGED_ENCRYPTION,
                kms_key_version="kms_key_version",
            )
        ]
        default_leader = "us-east4"
        api = client.database_admin_api = self._make_database_admin_api()
        api.get_database_ddl.return_value = ddl_pb
        db_pb = Database(
            state=2,
            create_time=_datetime_to_pb_timestamp(timestamp),
            restore_info=restore_info,
            version_retention_period="1d",
            earliest_version_time=_datetime_to_pb_timestamp(timestamp),
            encryption_config=encryption_config,
            encryption_info=encryption_info,
            default_leader=default_leader,
        )
        api.get_database.return_value = db_pb
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        database.reload()
        self.assertEqual(database._state, Database.State.READY)
        self.assertEqual(database._create_time, timestamp)
        self.assertEqual(database._restore_info, restore_info)
        self.assertEqual(database._version_retention_period, "1d")
        self.assertEqual(database._earliest_version_time, timestamp)
        self.assertEqual(database._ddl_statements, tuple(DDL_STATEMENTS))
        self.assertEqual(database._encryption_config, encryption_config)
        self.assertEqual(database._encryption_info, encryption_info)
        self.assertEqual(database._default_leader, default_leader)

        api.get_database_ddl.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        api.get_database.assert_called_once_with(
            name=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_update_ddl_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from tests._fixtures import DDL_STATEMENTS
        from google.cloud.spanner_admin_database_v1 import UpdateDatabaseDdlRequest

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_database_ddl.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(Unknown):
            database.update_ddl(DDL_STATEMENTS)

        expected_request = UpdateDatabaseDdlRequest(
            database=self.DATABASE_NAME,
            statements=DDL_STATEMENTS,
            operation_id="",
        )

        api.update_database_ddl.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_update_ddl_not_found(self):
        from google.cloud.exceptions import NotFound
        from tests._fixtures import DDL_STATEMENTS
        from google.cloud.spanner_admin_database_v1 import UpdateDatabaseDdlRequest

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_database_ddl.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.update_ddl(DDL_STATEMENTS)

        expected_request = UpdateDatabaseDdlRequest(
            database=self.DATABASE_NAME,
            statements=DDL_STATEMENTS,
            operation_id="",
        )

        api.update_database_ddl.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_update_ddl(self):
        from tests._fixtures import DDL_STATEMENTS
        from google.cloud.spanner_admin_database_v1 import UpdateDatabaseDdlRequest

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_database_ddl.return_value = op_future
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        future = database.update_ddl(DDL_STATEMENTS)

        self.assertIs(future, op_future)

        expected_request = UpdateDatabaseDdlRequest(
            database=self.DATABASE_NAME,
            statements=DDL_STATEMENTS,
            operation_id="",
        )

        api.update_database_ddl.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_update_ddl_w_operation_id(self):
        from tests._fixtures import DDL_STATEMENTS
        from google.cloud.spanner_admin_database_v1 import UpdateDatabaseDdlRequest

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.update_database_ddl.return_value = op_future
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        future = database.update_ddl(DDL_STATEMENTS, operation_id="someOperationId")

        self.assertIs(future, op_future)

        expected_request = UpdateDatabaseDdlRequest(
            database=self.DATABASE_NAME,
            statements=DDL_STATEMENTS,
            operation_id="someOperationId",
        )

        api.update_database_ddl.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_drop_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.drop_database.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(Unknown):
            database.drop()

        api.drop_database.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_drop_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.drop_database.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.drop()

        api.drop_database.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_drop_success(self):
        from google.protobuf.empty_pb2 import Empty

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.drop_database.return_value = Empty()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        database.drop()

        api.drop_database.assert_called_once_with(
            database=self.DATABASE_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def _execute_partitioned_dml_helper(
        self,
        dml,
        params=None,
        param_types=None,
        query_options=None,
        request_options=None,
        retried=False,
    ):
        from google.api_core.exceptions import Aborted
        from google.api_core.retry import Retry
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import (
            PartialResultSet,
            ResultSetStats,
        )
        from google.cloud.spanner_v1 import (
            Transaction as TransactionPB,
            TransactionSelector,
            TransactionOptions,
        )
        from google.cloud.spanner_v1._helpers import (
            _make_value_pb,
            _merge_query_options,
        )
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        import collections

        MethodConfig = collections.namedtuple("MethodConfig", ["retry"])

        transaction_pb = TransactionPB(id=self.TRANSACTION_ID)

        stats_pb = ResultSetStats(row_count_lower_bound=2)
        result_sets = [PartialResultSet(stats=stats_pb)]
        iterator = _MockIterator(*result_sets)

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        api = database._spanner_api = self._make_spanner_api()
        api._method_configs = {"ExecuteStreamingSql": MethodConfig(retry=Retry())}
        if retried:
            retry_transaction_pb = TransactionPB(id=self.RETRY_TRANSACTION_ID)
            api.begin_transaction.side_effect = [transaction_pb, retry_transaction_pb]
            api.execute_streaming_sql.side_effect = [Aborted("test"), iterator]
        else:
            api.begin_transaction.return_value = transaction_pb
            api.execute_streaming_sql.return_value = iterator

        row_count = database.execute_partitioned_dml(
            dml, params, param_types, query_options, request_options
        )

        self.assertEqual(row_count, 2)

        txn_options = TransactionOptions(
            partitioned_dml=TransactionOptions.PartitionedDml()
        )

        api.begin_transaction.assert_called_with(
            session=session.name,
            options=txn_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        if retried:
            self.assertEqual(api.begin_transaction.call_count, 2)
        else:
            self.assertEqual(api.begin_transaction.call_count, 1)

        if params:
            expected_params = Struct(
                fields={key: _make_value_pb(value) for (key, value) in params.items()}
            )
        else:
            expected_params = {}

        expected_transaction = TransactionSelector(id=self.TRANSACTION_ID)
        expected_query_options = client._query_options
        if query_options:
            expected_query_options = _merge_query_options(
                expected_query_options, query_options
            )

        if not request_options:
            expected_request_options = RequestOptions()
        else:
            expected_request_options = RequestOptions(request_options)
            expected_request_options.transaction_tag = None
        expected_request = ExecuteSqlRequest(
            session=self.SESSION_NAME,
            sql=dml,
            transaction=expected_transaction,
            params=expected_params,
            param_types=param_types,
            query_options=expected_query_options,
            request_options=expected_request_options,
        )

        api.execute_streaming_sql.assert_any_call(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        if retried:
            expected_retry_transaction = TransactionSelector(
                id=self.RETRY_TRANSACTION_ID
            )
            expected_request = ExecuteSqlRequest(
                session=self.SESSION_NAME,
                sql=dml,
                transaction=expected_retry_transaction,
                params=expected_params,
                param_types=param_types,
                query_options=expected_query_options,
                request_options=expected_request_options,
            )
            api.execute_streaming_sql.assert_called_with(
                request=expected_request,
                metadata=[("google-cloud-resource-prefix", database.name)],
            )
            self.assertEqual(api.execute_streaming_sql.call_count, 2)
        else:
            self.assertEqual(api.execute_streaming_sql.call_count, 1)

    def test_execute_partitioned_dml_wo_params(self):
        self._execute_partitioned_dml_helper(dml=DML_WO_PARAM)

    def test_execute_partitioned_dml_w_params_wo_param_types(self):
        with self.assertRaises(ValueError):
            self._execute_partitioned_dml_helper(dml=DML_W_PARAM, params=PARAMS)

    def test_execute_partitioned_dml_w_params_and_param_types(self):
        self._execute_partitioned_dml_helper(
            dml=DML_W_PARAM, params=PARAMS, param_types=PARAM_TYPES
        )

    def test_execute_partitioned_dml_w_query_options(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        self._execute_partitioned_dml_helper(
            dml=DML_W_PARAM,
            query_options=ExecuteSqlRequest.QueryOptions(optimizer_version="3"),
        )

    def test_execute_partitioned_dml_w_request_options(self):
        self._execute_partitioned_dml_helper(
            dml=DML_W_PARAM,
            request_options=RequestOptions(
                priority=RequestOptions.Priority.PRIORITY_MEDIUM
            ),
        )

    def test_execute_partitioned_dml_w_trx_tag_ignored(self):
        self._execute_partitioned_dml_helper(
            dml=DML_W_PARAM,
            request_options=RequestOptions(transaction_tag="trx-tag"),
        )

    def test_execute_partitioned_dml_w_req_tag_used(self):
        self._execute_partitioned_dml_helper(
            dml=DML_W_PARAM,
            request_options=RequestOptions(request_tag="req-tag"),
        )

    def test_execute_partitioned_dml_wo_params_retry_aborted(self):
        self._execute_partitioned_dml_helper(dml=DML_WO_PARAM, retried=True)

    def test_session_factory_defaults(self):
        from google.cloud.spanner_v1.session import Session

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        session = database.session()

        self.assertIsInstance(session, Session)
        self.assertIs(session.session_id, None)
        self.assertIs(session._database, database)
        self.assertEqual(session.labels, {})

    def test_session_factory_w_labels(self):
        from google.cloud.spanner_v1.session import Session

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        labels = {"foo": "bar"}
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        session = database.session(labels=labels)

        self.assertIsInstance(session, Session)
        self.assertIs(session.session_id, None)
        self.assertIs(session._database, database)
        self.assertEqual(session.labels, labels)

    def test_snapshot_defaults(self):
        from google.cloud.spanner_v1.database import SnapshotCheckout

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot()
        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertIs(checkout._database, database)
        self.assertEqual(checkout._kw, {})

    def test_snapshot_w_read_timestamp_and_multi_use(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.spanner_v1.database import SnapshotCheckout

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot(read_timestamp=now, multi_use=True)

        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertIs(checkout._database, database)
        self.assertEqual(checkout._kw, {"read_timestamp": now, "multi_use": True})

    def test_batch(self):
        from google.cloud.spanner_v1.database import BatchCheckout

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.batch()
        self.assertIsInstance(checkout, BatchCheckout)
        self.assertIs(checkout._database, database)

    def test_batch_snapshot(self):
        from google.cloud.spanner_v1.database import BatchSnapshot

        database = self._make_one(self.DATABASE_ID, instance=object(), pool=_Pool())

        batch_txn = database.batch_snapshot()
        self.assertIsInstance(batch_txn, BatchSnapshot)
        self.assertIs(batch_txn._database, database)
        self.assertIsNone(batch_txn._read_timestamp)
        self.assertIsNone(batch_txn._exact_staleness)

    def test_batch_snapshot_w_read_timestamp(self):
        from google.cloud.spanner_v1.database import BatchSnapshot

        database = self._make_one(self.DATABASE_ID, instance=object(), pool=_Pool())
        timestamp = self._make_timestamp()

        batch_txn = database.batch_snapshot(read_timestamp=timestamp)
        self.assertIsInstance(batch_txn, BatchSnapshot)
        self.assertIs(batch_txn._database, database)
        self.assertEqual(batch_txn._read_timestamp, timestamp)
        self.assertIsNone(batch_txn._exact_staleness)

    def test_batch_snapshot_w_exact_staleness(self):
        from google.cloud.spanner_v1.database import BatchSnapshot

        database = self._make_one(self.DATABASE_ID, instance=object(), pool=_Pool())
        duration = self._make_duration()

        batch_txn = database.batch_snapshot(exact_staleness=duration)
        self.assertIsInstance(batch_txn, BatchSnapshot)
        self.assertIs(batch_txn._database, database)
        self.assertIsNone(batch_txn._read_timestamp)
        self.assertEqual(batch_txn._exact_staleness, duration)

    def test_run_in_transaction_wo_args(self):
        import datetime

        NOW = datetime.datetime.now()
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        session._committed = NOW
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        _unit_of_work = object()

        committed = database.run_in_transaction(_unit_of_work)

        self.assertEqual(committed, NOW)
        self.assertEqual(session._retried, (_unit_of_work, (), {}))

    def test_run_in_transaction_w_args(self):
        import datetime

        SINCE = datetime.datetime(2017, 1, 1)
        UNTIL = datetime.datetime(2018, 1, 1)
        NOW = datetime.datetime.now()
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        session._committed = NOW
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        _unit_of_work = object()

        committed = database.run_in_transaction(_unit_of_work, SINCE, until=UNTIL)

        self.assertEqual(committed, NOW)
        self.assertEqual(session._retried, (_unit_of_work, (SINCE,), {"until": UNTIL}))

    def test_run_in_transaction_nested(self):
        from datetime import datetime

        # Perform the various setup tasks.
        instance = _Instance(self.INSTANCE_NAME, client=_Client())
        pool = _Pool()
        session = _Session(run_transaction_function=True)
        session._committed = datetime.now()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        # Define the inner function.
        inner = mock.Mock(spec=())

        # Define the nested transaction.
        def nested_unit_of_work():
            return database.run_in_transaction(inner)

        # Attempting to run this transaction should raise RuntimeError.
        with self.assertRaises(RuntimeError):
            database.run_in_transaction(nested_unit_of_work)
        self.assertEqual(inner.call_count, 0)

    def test_restore_backup_unspecified(self):
        instance = _Instance(self.INSTANCE_NAME, client=_Client())
        database = self._make_one(self.DATABASE_ID, instance)

        with self.assertRaises(ValueError):
            database.restore(None)

    def test_restore_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_admin_database_v1 import RestoreDatabaseRequest

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.restore_database.side_effect = Unknown("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        backup = _Backup(self.BACKUP_NAME)

        with self.assertRaises(Unknown):
            database.restore(backup)

        expected_request = RestoreDatabaseRequest(
            parent=self.INSTANCE_NAME,
            database_id=self.DATABASE_ID,
            backup=self.BACKUP_NAME,
        )

        api.restore_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_restore_not_found(self):
        from google.api_core.exceptions import NotFound
        from google.cloud.spanner_admin_database_v1 import RestoreDatabaseRequest

        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.restore_database.side_effect = NotFound("testing")
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        backup = _Backup(self.BACKUP_NAME)

        with self.assertRaises(NotFound):
            database.restore(backup)

        expected_request = RestoreDatabaseRequest(
            parent=self.INSTANCE_NAME,
            database_id=self.DATABASE_ID,
            backup=self.BACKUP_NAME,
        )

        api.restore_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_restore_success(self):
        from google.cloud.spanner_admin_database_v1 import (
            RestoreDatabaseEncryptionConfig,
        )
        from google.cloud.spanner_admin_database_v1 import RestoreDatabaseRequest

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.restore_database.return_value = op_future
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        encryption_config = RestoreDatabaseEncryptionConfig(
            encryption_type=RestoreDatabaseEncryptionConfig.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION,
            kms_key_name="kms_key_name",
        )
        database = self._make_one(
            self.DATABASE_ID, instance, pool=pool, encryption_config=encryption_config
        )
        backup = _Backup(self.BACKUP_NAME)

        future = database.restore(backup)

        self.assertIs(future, op_future)

        expected_request = RestoreDatabaseRequest(
            parent=self.INSTANCE_NAME,
            database_id=self.DATABASE_ID,
            backup=self.BACKUP_NAME,
            encryption_config=encryption_config,
        )

        api.restore_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_restore_success_w_encryption_config_dict(self):
        from google.cloud.spanner_admin_database_v1 import (
            RestoreDatabaseEncryptionConfig,
        )
        from google.cloud.spanner_admin_database_v1 import RestoreDatabaseRequest

        op_future = object()
        client = _Client()
        api = client.database_admin_api = self._make_database_admin_api()
        api.restore_database.return_value = op_future
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        encryption_config = {
            "encryption_type": RestoreDatabaseEncryptionConfig.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION,
            "kms_key_name": "kms_key_name",
        }
        database = self._make_one(
            self.DATABASE_ID, instance, pool=pool, encryption_config=encryption_config
        )
        backup = _Backup(self.BACKUP_NAME)

        future = database.restore(backup)

        self.assertIs(future, op_future)

        expected_encryption_config = RestoreDatabaseEncryptionConfig(
            encryption_type=RestoreDatabaseEncryptionConfig.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION,
            kms_key_name="kms_key_name",
        )
        expected_request = RestoreDatabaseRequest(
            parent=self.INSTANCE_NAME,
            database_id=self.DATABASE_ID,
            backup=self.BACKUP_NAME,
            encryption_config=expected_encryption_config,
        )

        api.restore_database.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_restore_w_invalid_encryption_config_dict(self):
        from google.cloud.spanner_admin_database_v1 import (
            RestoreDatabaseEncryptionConfig,
        )

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        encryption_config = {
            "encryption_type": RestoreDatabaseEncryptionConfig.EncryptionType.GOOGLE_DEFAULT_ENCRYPTION,
            "kms_key_name": "kms_key_name",
        }
        database = self._make_one(
            self.DATABASE_ID, instance, pool=pool, encryption_config=encryption_config
        )
        backup = _Backup(self.BACKUP_NAME)

        with self.assertRaises(ValueError):
            database.restore(backup)

    def test_is_ready(self):
        from google.cloud.spanner_admin_database_v1 import Database

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        database._state = Database.State.READY
        self.assertTrue(database.is_ready())
        database._state = Database.State.READY_OPTIMIZING
        self.assertTrue(database.is_ready())
        database._state = Database.State.CREATING
        self.assertFalse(database.is_ready())

    def test_is_optimized(self):
        from google.cloud.spanner_admin_database_v1 import Database

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        database._state = Database.State.READY
        self.assertTrue(database.is_optimized())
        database._state = Database.State.READY_OPTIMIZING
        self.assertFalse(database.is_optimized())
        database._state = Database.State.CREATING
        self.assertFalse(database.is_optimized())

    def test_list_database_operations_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_v1.database import _DATABASE_METADATA_FILTER

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        instance.list_database_operations = mock.MagicMock(
            side_effect=Unknown("testing")
        )
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(Unknown):
            database.list_database_operations()

        instance.list_database_operations.assert_called_once_with(
            filter_=_DATABASE_METADATA_FILTER.format(database.name), page_size=None
        )

    def test_list_database_operations_not_found(self):
        from google.api_core.exceptions import NotFound
        from google.cloud.spanner_v1.database import _DATABASE_METADATA_FILTER

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        instance.list_database_operations = mock.MagicMock(
            side_effect=NotFound("testing")
        )
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.list_database_operations()

        instance.list_database_operations.assert_called_once_with(
            filter_=_DATABASE_METADATA_FILTER.format(database.name), page_size=None
        )

    def test_list_database_operations_defaults(self):
        from google.cloud.spanner_v1.database import _DATABASE_METADATA_FILTER

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        instance.list_database_operations = mock.MagicMock(return_value=[])
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        database.list_database_operations()

        instance.list_database_operations.assert_called_once_with(
            filter_=_DATABASE_METADATA_FILTER.format(database.name), page_size=None
        )

    def test_list_database_operations_explicit_filter(self):
        from google.cloud.spanner_v1.database import _DATABASE_METADATA_FILTER

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        instance.list_database_operations = mock.MagicMock(return_value=[])
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        expected_filter_ = "({0}) AND ({1})".format(
            "metadata.@type:type.googleapis.com/google.spanner.admin.database.v1.RestoreDatabaseMetadata",
            _DATABASE_METADATA_FILTER.format(database.name),
        )
        page_size = 10
        database.list_database_operations(
            filter_="metadata.@type:type.googleapis.com/google.spanner.admin.database.v1.RestoreDatabaseMetadata",
            page_size=page_size,
        )

        instance.list_database_operations.assert_called_once_with(
            filter_=expected_filter_, page_size=page_size
        )

    def test_table_factory_defaults(self):
        from google.cloud.spanner_v1.table import Table

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        my_table = database.table("my_table")
        self.assertIsInstance(my_table, Table)
        self.assertIs(my_table._database, database)
        self.assertEqual(my_table.table_id, "my_table")

    def test_list_tables(self):
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        tables = database.list_tables()
        self.assertIsNotNone(tables)


class TestBatchCheckout(_BaseTest):
    def _get_target_class(self):
        from google.cloud.spanner_v1.database import BatchCheckout

        return BatchCheckout

    @staticmethod
    def _make_spanner_client():
        from google.cloud.spanner_v1 import SpannerClient

        return mock.create_autospec(SpannerClient)

    def test_ctor(self):
        database = _Database(self.DATABASE_NAME)
        checkout = self._make_one(database)
        self.assertIs(checkout._database, database)

    def test_context_mgr_success(self):
        import datetime
        from google.cloud.spanner_v1 import CommitRequest
        from google.cloud.spanner_v1 import CommitResponse
        from google.cloud.spanner_v1 import TransactionOptions
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner_v1.batch import Batch

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database(self.DATABASE_NAME)
        api = database.spanner_api = self._make_spanner_client()
        api.commit.return_value = response
        pool = database._pool = _Pool()
        session = _Session(database)
        pool.put(session)
        checkout = self._make_one(
            database, request_options={"transaction_tag": self.TRANSACTION_TAG}
        )

        with checkout as batch:
            self.assertIsNone(pool._session)
            self.assertIsInstance(batch, Batch)
            self.assertIs(batch._session, session)

        self.assertIs(pool._session, session)
        self.assertEqual(batch.committed, now)
        self.assertEqual(batch.transaction_tag, self.TRANSACTION_TAG)

        expected_txn_options = TransactionOptions(read_write={})

        request = CommitRequest(
            session=self.SESSION_NAME,
            mutations=[],
            single_use_transaction=expected_txn_options,
            request_options=RequestOptions(transaction_tag=self.TRANSACTION_TAG),
        )
        api.commit.assert_called_once_with(
            request=request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_context_mgr_w_commit_stats_success(self):
        import datetime
        from google.cloud.spanner_v1 import CommitRequest
        from google.cloud.spanner_v1 import CommitResponse
        from google.cloud.spanner_v1 import TransactionOptions
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner_v1.batch import Batch

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        commit_stats = CommitResponse.CommitStats(mutation_count=4)
        response = CommitResponse(commit_timestamp=now_pb, commit_stats=commit_stats)
        database = _Database(self.DATABASE_NAME)
        database.log_commit_stats = True
        api = database.spanner_api = self._make_spanner_client()
        api.commit.return_value = response
        pool = database._pool = _Pool()
        session = _Session(database)
        pool.put(session)
        checkout = self._make_one(database)

        with checkout as batch:
            self.assertIsNone(pool._session)
            self.assertIsInstance(batch, Batch)
            self.assertIs(batch._session, session)

        self.assertIs(pool._session, session)
        self.assertEqual(batch.committed, now)

        expected_txn_options = TransactionOptions(read_write={})

        request = CommitRequest(
            session=self.SESSION_NAME,
            mutations=[],
            single_use_transaction=expected_txn_options,
            return_commit_stats=True,
            request_options=RequestOptions(),
        )
        api.commit.assert_called_once_with(
            request=request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        database.logger.info.assert_called_once_with(
            "CommitStats: mutation_count: 4\n", extra={"commit_stats": commit_stats}
        )

    def test_context_mgr_w_commit_stats_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_v1 import CommitRequest
        from google.cloud.spanner_v1 import TransactionOptions
        from google.cloud.spanner_v1.batch import Batch

        database = _Database(self.DATABASE_NAME)
        database.log_commit_stats = True
        api = database.spanner_api = self._make_spanner_client()
        api.commit.side_effect = Unknown("testing")
        pool = database._pool = _Pool()
        session = _Session(database)
        pool.put(session)
        checkout = self._make_one(database)

        with self.assertRaises(Unknown):
            with checkout as batch:
                self.assertIsNone(pool._session)
                self.assertIsInstance(batch, Batch)
                self.assertIs(batch._session, session)

        self.assertIs(pool._session, session)

        expected_txn_options = TransactionOptions(read_write={})

        request = CommitRequest(
            session=self.SESSION_NAME,
            mutations=[],
            single_use_transaction=expected_txn_options,
            return_commit_stats=True,
            request_options=RequestOptions(),
        )
        api.commit.assert_called_once_with(
            request=request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        database.logger.info.assert_not_called()

    def test_context_mgr_failure(self):
        from google.cloud.spanner_v1.batch import Batch

        database = _Database(self.DATABASE_NAME)
        pool = database._pool = _Pool()
        session = _Session(database)
        pool.put(session)
        checkout = self._make_one(database)

        class Testing(Exception):
            pass

        with self.assertRaises(Testing):
            with checkout as batch:
                self.assertIsNone(pool._session)
                self.assertIsInstance(batch, Batch)
                self.assertIs(batch._session, session)
                raise Testing()

        self.assertIs(pool._session, session)
        self.assertIsNone(batch.committed)


class TestSnapshotCheckout(_BaseTest):
    def _get_target_class(self):
        from google.cloud.spanner_v1.database import SnapshotCheckout

        return SnapshotCheckout

    def test_ctor_defaults(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database)
        self.assertIs(checkout._database, database)
        self.assertEqual(checkout._kw, {})

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertTrue(snapshot._strong)
            self.assertFalse(snapshot._multi_use)

        self.assertIs(pool._session, session)

    def test_ctor_w_read_timestamp_and_multi_use(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.spanner_v1.snapshot import Snapshot

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database, read_timestamp=now, multi_use=True)
        self.assertIs(checkout._database, database)
        self.assertEqual(checkout._kw, {"read_timestamp": now, "multi_use": True})

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertEqual(snapshot._read_timestamp, now)
            self.assertTrue(snapshot._multi_use)

        self.assertIs(pool._session, session)

    def test_context_mgr_failure(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        database = _Database(self.DATABASE_NAME)
        pool = database._pool = _Pool()
        session = _Session(database)
        pool.put(session)
        checkout = self._make_one(database)

        class Testing(Exception):
            pass

        with self.assertRaises(Testing):
            with checkout as snapshot:
                self.assertIsNone(pool._session)
                self.assertIsInstance(snapshot, Snapshot)
                self.assertIs(snapshot._session, session)
                raise Testing()

        self.assertIs(pool._session, session)

    def test_context_mgr_session_not_found_error(self):
        from google.cloud.exceptions import NotFound

        database = _Database(self.DATABASE_NAME)
        session = _Session(database, name="session-1")
        session.exists = mock.MagicMock(return_value=False)
        pool = database._pool = _Pool()
        new_session = _Session(database, name="session-2")
        new_session.create = mock.MagicMock(return_value=[])
        pool._new_session = mock.MagicMock(return_value=new_session)

        pool.put(session)
        checkout = self._make_one(database)

        self.assertEqual(pool._session, session)
        with self.assertRaises(NotFound):
            with checkout as _:
                raise NotFound("Session not found")
        # Assert that session-1 was removed from pool and new session was added.
        self.assertEqual(pool._session, new_session)

    def test_context_mgr_table_not_found_error(self):
        from google.cloud.exceptions import NotFound

        database = _Database(self.DATABASE_NAME)
        session = _Session(database, name="session-1")
        session.exists = mock.MagicMock(return_value=True)
        pool = database._pool = _Pool()
        pool._new_session = mock.MagicMock(return_value=[])

        pool.put(session)
        checkout = self._make_one(database)

        self.assertEqual(pool._session, session)
        with self.assertRaises(NotFound):
            with checkout as _:
                raise NotFound("Table not found")
        # Assert that session-1 was not removed from pool.
        self.assertEqual(pool._session, session)
        pool._new_session.assert_not_called()

    def test_context_mgr_unknown_error(self):
        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool._new_session = mock.MagicMock(return_value=[])
        pool.put(session)
        checkout = self._make_one(database)

        class Testing(Exception):
            pass

        self.assertEqual(pool._session, session)
        with self.assertRaises(Testing):
            with checkout as _:
                raise Testing("Unknown error.")
        # Assert that session-1 was not removed from pool.
        self.assertEqual(pool._session, session)
        pool._new_session.assert_not_called()


class TestBatchSnapshot(_BaseTest):
    TABLE = "table_name"
    COLUMNS = ["column_one", "column_two"]
    TOKENS = [b"TOKEN1", b"TOKEN2"]
    INDEX = "index"

    def _get_target_class(self):
        from google.cloud.spanner_v1.database import BatchSnapshot

        return BatchSnapshot

    @staticmethod
    def _make_database(**kwargs):
        from google.cloud.spanner_v1.database import Database

        return mock.create_autospec(Database, instance=True, **kwargs)

    @staticmethod
    def _make_session(**kwargs):
        from google.cloud.spanner_v1.session import Session

        return mock.create_autospec(Session, instance=True, **kwargs)

    @staticmethod
    def _make_snapshot(transaction_id=None, **kwargs):
        from google.cloud.spanner_v1.snapshot import Snapshot

        snapshot = mock.create_autospec(Snapshot, instance=True, **kwargs)
        if transaction_id is not None:
            snapshot._transaction_id = transaction_id

        return snapshot

    @staticmethod
    def _make_keyset():
        from google.cloud.spanner_v1.keyset import KeySet

        return KeySet(all_=True)

    def test_ctor_no_staleness(self):
        database = self._make_database()

        batch_txn = self._make_one(database)

        self.assertIs(batch_txn._database, database)
        self.assertIsNone(batch_txn._session)
        self.assertIsNone(batch_txn._snapshot)
        self.assertIsNone(batch_txn._read_timestamp)
        self.assertIsNone(batch_txn._exact_staleness)

    def test_ctor_w_read_timestamp(self):
        database = self._make_database()
        timestamp = self._make_timestamp()

        batch_txn = self._make_one(database, read_timestamp=timestamp)

        self.assertIs(batch_txn._database, database)
        self.assertIsNone(batch_txn._session)
        self.assertIsNone(batch_txn._snapshot)
        self.assertEqual(batch_txn._read_timestamp, timestamp)
        self.assertIsNone(batch_txn._exact_staleness)

    def test_ctor_w_exact_staleness(self):
        database = self._make_database()
        duration = self._make_duration()

        batch_txn = self._make_one(database, exact_staleness=duration)

        self.assertIs(batch_txn._database, database)
        self.assertIsNone(batch_txn._session)
        self.assertIsNone(batch_txn._snapshot)
        self.assertIsNone(batch_txn._read_timestamp)
        self.assertEqual(batch_txn._exact_staleness, duration)

    def test_from_dict(self):
        klass = self._get_target_class()
        database = self._make_database()
        session = database.session.return_value = self._make_session()
        snapshot = session.snapshot.return_value = self._make_snapshot()
        api_repr = {
            "session_id": self.SESSION_ID,
            "transaction_id": self.TRANSACTION_ID,
        }

        batch_txn = klass.from_dict(database, api_repr)
        self.assertIs(batch_txn._database, database)
        self.assertIs(batch_txn._session, session)
        self.assertEqual(session._session_id, self.SESSION_ID)
        self.assertEqual(snapshot._transaction_id, self.TRANSACTION_ID)
        snapshot.begin.assert_not_called()
        self.assertIs(batch_txn._snapshot, snapshot)

    def test_to_dict(self):
        database = self._make_database()
        batch_txn = self._make_one(database)
        batch_txn._session = self._make_session(_session_id=self.SESSION_ID)
        batch_txn._snapshot = self._make_snapshot(transaction_id=self.TRANSACTION_ID)

        expected = {
            "session_id": self.SESSION_ID,
            "transaction_id": self.TRANSACTION_ID,
        }
        self.assertEqual(batch_txn.to_dict(), expected)

    def test__get_session_already(self):
        database = self._make_database()
        batch_txn = self._make_one(database)
        already = batch_txn._session = object()
        self.assertIs(batch_txn._get_session(), already)

    def test__get_session_new(self):
        database = self._make_database()
        session = database.session.return_value = self._make_session()
        batch_txn = self._make_one(database)
        self.assertIs(batch_txn._get_session(), session)
        session.create.assert_called_once_with()

    def test__get_snapshot_already(self):
        database = self._make_database()
        batch_txn = self._make_one(database)
        already = batch_txn._snapshot = self._make_snapshot()
        self.assertIs(batch_txn._get_snapshot(), already)
        already.begin.assert_not_called()

    def test__get_snapshot_new_wo_staleness(self):
        database = self._make_database()
        batch_txn = self._make_one(database)
        session = batch_txn._session = self._make_session()
        snapshot = session.snapshot.return_value = self._make_snapshot()
        self.assertIs(batch_txn._get_snapshot(), snapshot)
        session.snapshot.assert_called_once_with(
            read_timestamp=None, exact_staleness=None, multi_use=True
        )
        snapshot.begin.assert_called_once_with()

    def test__get_snapshot_w_read_timestamp(self):
        database = self._make_database()
        timestamp = self._make_timestamp()
        batch_txn = self._make_one(database, read_timestamp=timestamp)
        session = batch_txn._session = self._make_session()
        snapshot = session.snapshot.return_value = self._make_snapshot()
        self.assertIs(batch_txn._get_snapshot(), snapshot)
        session.snapshot.assert_called_once_with(
            read_timestamp=timestamp, exact_staleness=None, multi_use=True
        )
        snapshot.begin.assert_called_once_with()

    def test__get_snapshot_w_exact_staleness(self):
        database = self._make_database()
        duration = self._make_duration()
        batch_txn = self._make_one(database, exact_staleness=duration)
        session = batch_txn._session = self._make_session()
        snapshot = session.snapshot.return_value = self._make_snapshot()
        self.assertIs(batch_txn._get_snapshot(), snapshot)
        session.snapshot.assert_called_once_with(
            read_timestamp=None, exact_staleness=duration, multi_use=True
        )
        snapshot.begin.assert_called_once_with()

    def test_read(self):
        keyset = self._make_keyset()
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()

        rows = batch_txn.read(self.TABLE, self.COLUMNS, keyset, self.INDEX)

        self.assertIs(rows, snapshot.read.return_value)
        snapshot.read.assert_called_once_with(
            self.TABLE, self.COLUMNS, keyset, self.INDEX
        )

    def test_execute_sql(self):
        sql = (
            "SELECT first_name, last_name, email FROM citizens " "WHERE age <= @max_age"
        )
        params = {"max_age": 30}
        param_types = {"max_age": "INT64"}
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()

        rows = batch_txn.execute_sql(sql, params, param_types)

        self.assertIs(rows, snapshot.execute_sql.return_value)
        snapshot.execute_sql.assert_called_once_with(sql, params, param_types)

    def test_generate_read_batches_w_max_partitions(self):
        max_partitions = len(self.TOKENS)
        keyset = self._make_keyset()
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        snapshot.partition_read.return_value = self.TOKENS

        batches = list(
            batch_txn.generate_read_batches(
                self.TABLE, self.COLUMNS, keyset, max_partitions=max_partitions
            )
        )

        expected_read = {
            "table": self.TABLE,
            "columns": self.COLUMNS,
            "keyset": {"all": True},
            "index": "",
        }
        self.assertEqual(len(batches), len(self.TOKENS))
        for batch, token in zip(batches, self.TOKENS):
            self.assertEqual(batch["partition"], token)
            self.assertEqual(batch["read"], expected_read)

        snapshot.partition_read.assert_called_once_with(
            table=self.TABLE,
            columns=self.COLUMNS,
            keyset=keyset,
            index="",
            partition_size_bytes=None,
            max_partitions=max_partitions,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_generate_read_batches_w_retry_and_timeout_params(self):
        max_partitions = len(self.TOKENS)
        keyset = self._make_keyset()
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        snapshot.partition_read.return_value = self.TOKENS
        retry = Retry(deadline=60)
        batches = list(
            batch_txn.generate_read_batches(
                self.TABLE,
                self.COLUMNS,
                keyset,
                max_partitions=max_partitions,
                retry=retry,
                timeout=2.0,
            )
        )

        expected_read = {
            "table": self.TABLE,
            "columns": self.COLUMNS,
            "keyset": {"all": True},
            "index": "",
        }
        self.assertEqual(len(batches), len(self.TOKENS))
        for batch, token in zip(batches, self.TOKENS):
            self.assertEqual(batch["partition"], token)
            self.assertEqual(batch["read"], expected_read)

        snapshot.partition_read.assert_called_once_with(
            table=self.TABLE,
            columns=self.COLUMNS,
            keyset=keyset,
            index="",
            partition_size_bytes=None,
            max_partitions=max_partitions,
            retry=retry,
            timeout=2.0,
        )

    def test_generate_read_batches_w_index_w_partition_size_bytes(self):
        size = 1 << 20
        keyset = self._make_keyset()
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        snapshot.partition_read.return_value = self.TOKENS

        batches = list(
            batch_txn.generate_read_batches(
                self.TABLE,
                self.COLUMNS,
                keyset,
                index=self.INDEX,
                partition_size_bytes=size,
            )
        )

        expected_read = {
            "table": self.TABLE,
            "columns": self.COLUMNS,
            "keyset": {"all": True},
            "index": self.INDEX,
        }
        self.assertEqual(len(batches), len(self.TOKENS))
        for batch, token in zip(batches, self.TOKENS):
            self.assertEqual(batch["partition"], token)
            self.assertEqual(batch["read"], expected_read)

        snapshot.partition_read.assert_called_once_with(
            table=self.TABLE,
            columns=self.COLUMNS,
            keyset=keyset,
            index=self.INDEX,
            partition_size_bytes=size,
            max_partitions=None,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_process_read_batch(self):
        keyset = self._make_keyset()
        token = b"TOKEN"
        batch = {
            "partition": token,
            "read": {
                "table": self.TABLE,
                "columns": self.COLUMNS,
                "keyset": {"all": True},
                "index": self.INDEX,
            },
        }
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        expected = snapshot.read.return_value = object()

        found = batch_txn.process_read_batch(batch)

        self.assertIs(found, expected)

        snapshot.read.assert_called_once_with(
            table=self.TABLE,
            columns=self.COLUMNS,
            keyset=keyset,
            index=self.INDEX,
            partition=token,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_process_read_batch_w_retry_timeout(self):
        keyset = self._make_keyset()
        token = b"TOKEN"
        batch = {
            "partition": token,
            "read": {
                "table": self.TABLE,
                "columns": self.COLUMNS,
                "keyset": {"all": True},
                "index": self.INDEX,
            },
        }
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        expected = snapshot.read.return_value = object()
        retry = Retry(deadline=60)
        found = batch_txn.process_read_batch(batch, retry=retry, timeout=2.0)

        self.assertIs(found, expected)

        snapshot.read.assert_called_once_with(
            table=self.TABLE,
            columns=self.COLUMNS,
            keyset=keyset,
            index=self.INDEX,
            partition=token,
            retry=retry,
            timeout=2.0,
        )

    def test_generate_query_batches_w_max_partitions(self):
        sql = "SELECT COUNT(*) FROM table_name"
        max_partitions = len(self.TOKENS)
        client = _Client(self.PROJECT_ID)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        database = _Database(self.DATABASE_NAME, instance=instance)
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        snapshot.partition_query.return_value = self.TOKENS

        batches = list(
            batch_txn.generate_query_batches(sql, max_partitions=max_partitions)
        )

        expected_query = {"sql": sql, "query_options": client._query_options}
        self.assertEqual(len(batches), len(self.TOKENS))
        for batch, token in zip(batches, self.TOKENS):
            self.assertEqual(batch["partition"], token)
            self.assertEqual(batch["query"], expected_query)

        snapshot.partition_query.assert_called_once_with(
            sql=sql,
            params=None,
            param_types=None,
            partition_size_bytes=None,
            max_partitions=max_partitions,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_generate_query_batches_w_params_w_partition_size_bytes(self):
        sql = (
            "SELECT first_name, last_name, email FROM citizens " "WHERE age <= @max_age"
        )
        params = {"max_age": 30}
        param_types = {"max_age": "INT64"}
        size = 1 << 20
        client = _Client(self.PROJECT_ID)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        database = _Database(self.DATABASE_NAME, instance=instance)
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        snapshot.partition_query.return_value = self.TOKENS

        batches = list(
            batch_txn.generate_query_batches(
                sql, params=params, param_types=param_types, partition_size_bytes=size
            )
        )

        expected_query = {
            "sql": sql,
            "params": params,
            "param_types": param_types,
            "query_options": client._query_options,
        }
        self.assertEqual(len(batches), len(self.TOKENS))
        for batch, token in zip(batches, self.TOKENS):
            self.assertEqual(batch["partition"], token)
            self.assertEqual(batch["query"], expected_query)

        snapshot.partition_query.assert_called_once_with(
            sql=sql,
            params=params,
            param_types=param_types,
            partition_size_bytes=size,
            max_partitions=None,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_generate_query_batches_w_retry_and_timeout_params(self):
        sql = (
            "SELECT first_name, last_name, email FROM citizens " "WHERE age <= @max_age"
        )
        params = {"max_age": 30}
        param_types = {"max_age": "INT64"}
        size = 1 << 20
        client = _Client(self.PROJECT_ID)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        database = _Database(self.DATABASE_NAME, instance=instance)
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        snapshot.partition_query.return_value = self.TOKENS
        retry = Retry(deadline=60)
        batches = list(
            batch_txn.generate_query_batches(
                sql,
                params=params,
                param_types=param_types,
                partition_size_bytes=size,
                retry=retry,
                timeout=2.0,
            )
        )

        expected_query = {
            "sql": sql,
            "params": params,
            "param_types": param_types,
            "query_options": client._query_options,
        }
        self.assertEqual(len(batches), len(self.TOKENS))
        for batch, token in zip(batches, self.TOKENS):
            self.assertEqual(batch["partition"], token)
            self.assertEqual(batch["query"], expected_query)

        snapshot.partition_query.assert_called_once_with(
            sql=sql,
            params=params,
            param_types=param_types,
            partition_size_bytes=size,
            max_partitions=None,
            retry=retry,
            timeout=2.0,
        )

    def test_process_query_batch(self):
        sql = (
            "SELECT first_name, last_name, email FROM citizens " "WHERE age <= @max_age"
        )
        params = {"max_age": 30}
        param_types = {"max_age": "INT64"}
        token = b"TOKEN"
        batch = {
            "partition": token,
            "query": {"sql": sql, "params": params, "param_types": param_types},
        }
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        expected = snapshot.execute_sql.return_value = object()

        found = batch_txn.process_query_batch(batch)

        self.assertIs(found, expected)

        snapshot.execute_sql.assert_called_once_with(
            sql=sql,
            params=params,
            param_types=param_types,
            partition=token,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_process_query_batch_w_retry_timeout(self):
        sql = (
            "SELECT first_name, last_name, email FROM citizens " "WHERE age <= @max_age"
        )
        params = {"max_age": 30}
        param_types = {"max_age": "INT64"}
        token = b"TOKEN"
        batch = {
            "partition": token,
            "query": {"sql": sql, "params": params, "param_types": param_types},
        }
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        expected = snapshot.execute_sql.return_value = object()
        retry = Retry(deadline=60)
        found = batch_txn.process_query_batch(batch, retry=retry, timeout=2.0)

        self.assertIs(found, expected)

        snapshot.execute_sql.assert_called_once_with(
            sql=sql,
            params=params,
            param_types=param_types,
            partition=token,
            retry=retry,
            timeout=2.0,
        )

    def test_close_wo_session(self):
        database = self._make_database()
        batch_txn = self._make_one(database)

        batch_txn.close()  # no raise

    def test_close_w_session(self):
        database = self._make_database()
        batch_txn = self._make_one(database)
        session = batch_txn._session = self._make_session()

        batch_txn.close()

        session.delete.assert_called_once_with()

    def test_process_w_invalid_batch(self):
        token = b"TOKEN"
        batch = {"partition": token, "bogus": b"BOGUS"}
        database = self._make_database()
        batch_txn = self._make_one(database)

        with self.assertRaises(ValueError):
            batch_txn.process(batch)

    def test_process_w_read_batch(self):
        keyset = self._make_keyset()
        token = b"TOKEN"
        batch = {
            "partition": token,
            "read": {
                "table": self.TABLE,
                "columns": self.COLUMNS,
                "keyset": {"all": True},
                "index": self.INDEX,
            },
        }
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        expected = snapshot.read.return_value = object()

        found = batch_txn.process(batch)

        self.assertIs(found, expected)

        snapshot.read.assert_called_once_with(
            table=self.TABLE,
            columns=self.COLUMNS,
            keyset=keyset,
            index=self.INDEX,
            partition=token,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )

    def test_process_w_query_batch(self):
        sql = (
            "SELECT first_name, last_name, email FROM citizens " "WHERE age <= @max_age"
        )
        params = {"max_age": 30}
        param_types = {"max_age": "INT64"}
        token = b"TOKEN"
        batch = {
            "partition": token,
            "query": {"sql": sql, "params": params, "param_types": param_types},
        }
        database = self._make_database()
        batch_txn = self._make_one(database)
        snapshot = batch_txn._snapshot = self._make_snapshot()
        expected = snapshot.execute_sql.return_value = object()

        found = batch_txn.process(batch)

        self.assertIs(found, expected)

        snapshot.execute_sql.assert_called_once_with(
            sql=sql,
            params=params,
            param_types=param_types,
            partition=token,
            retry=gapic_v1.method.DEFAULT,
            timeout=gapic_v1.method.DEFAULT,
        )


def _make_instance_api():
    from google.cloud.spanner_admin_instance_v1 import InstanceAdminClient

    return mock.create_autospec(InstanceAdminClient)


class _Client(object):
    def __init__(self, project=TestDatabase.PROJECT_ID):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        self.project = project
        self.project_name = "projects/" + self.project
        self._endpoint_cache = {}
        self.instance_admin_api = _make_instance_api()
        self._client_info = mock.Mock()
        self._client_options = mock.Mock()
        self._query_options = ExecuteSqlRequest.QueryOptions(optimizer_version="1")


class _Instance(object):
    def __init__(self, name, client=None, emulator_host=None):
        self.name = name
        self.instance_id = name.rsplit("/", 1)[1]
        self._client = client
        self.emulator_host = emulator_host


class _Backup(object):
    def __init__(self, name):
        self.name = name


class _Database(object):
    log_commit_stats = False

    def __init__(self, name, instance=None):
        self.name = name
        self.database_id = name.rsplit("/", 1)[1]
        self._instance = instance
        from logging import Logger

        self.logger = mock.create_autospec(Logger, instance=True)


class _Pool(object):
    _bound = None

    def bind(self, database):
        self._bound = database

    def get(self):
        session, self._session = self._session, None
        return session

    def put(self, session):
        self._session = session


class _Session(object):

    _rows = ()
    _created = False
    _transaction = None
    _snapshot = None

    def __init__(
        self, database=None, name=_BaseTest.SESSION_NAME, run_transaction_function=False
    ):
        self._database = database
        self.name = name
        self._run_transaction_function = run_transaction_function

    def run_in_transaction(self, func, *args, **kw):
        if self._run_transaction_function:
            func(*args, **kw)
        self._retried = (func, args, kw)
        return self._committed


class _MockIterator(object):
    def __init__(self, *values, **kw):
        self._iter_values = iter(values)
        self._fail_after = kw.pop("fail_after", False)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._iter_values)
        except StopIteration:
            raise

    next = __next__
