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

from google.cloud.spanner import __version__

from google.cloud._testing import _GAXBaseAPI


class _BaseTest(unittest.TestCase):

    PROJECT_ID = 'project-id'
    PARENT = 'projects/' + PROJECT_ID
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = PARENT + '/instances/' + INSTANCE_ID
    DATABASE_ID = 'database_id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session_id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)


class TestDatabase(_BaseTest):

    def _getTargetClass(self):
        from google.cloud.spanner.database import Database

        return Database

    def test_ctor_defaults(self):
        from google.cloud.spanner.pool import BurstyPool

        instance = _Instance(self.INSTANCE_NAME)

        database = self._make_one(self.DATABASE_ID, instance)

        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertTrue(database._instance is instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertIsInstance(database._pool, BurstyPool)
        # BurstyPool does not create sessions during 'bind()'.
        self.assertTrue(database._pool._sessions.empty())

    def test_ctor_w_explicit_pool(self):
        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertTrue(database._instance is instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertIs(database._pool, pool)
        self.assertIs(pool._bound, database)

    def test_ctor_w_ddl_statements_non_string(self):

        with self.assertRaises(ValueError):
            self._make_one(
                self.DATABASE_ID, instance=object(),
                ddl_statements=[object()])

    def test_ctor_w_ddl_statements_w_create_database(self):

        with self.assertRaises(ValueError):
            self._make_one(
                self.DATABASE_ID, instance=object(),
                ddl_statements=['CREATE DATABASE foo'])

    def test_ctor_w_ddl_statements_ok(self):
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        instance = _Instance(self.INSTANCE_NAME)
        pool = _Pool()
        database = self._make_one(
            self.DATABASE_ID, instance, ddl_statements=DDL_STATEMENTS,
            pool=pool)
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertTrue(database._instance is instance)
        self.assertEqual(list(database.ddl_statements), DDL_STATEMENTS)

    def test_from_pb_bad_database_name(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)

        database_name = 'INCORRECT_FORMAT'
        database_pb = admin_v1_pb2.Database(name=database_name)
        klass = self._getTargetClass()

        with self.assertRaises(ValueError):
            klass.from_pb(database_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)

        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(project=ALT_PROJECT)
        instance = _Instance(self.INSTANCE_NAME, client)
        database_pb = admin_v1_pb2.Database(name=self.DATABASE_NAME)
        klass = self._getTargetClass()

        with self.assertRaises(ValueError):
            klass.from_pb(database_pb, instance)

    def test_from_pb_instance_mistmatch(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)

        ALT_INSTANCE = '/projects/%s/instances/ALT-INSTANCE' % (
            self.PROJECT_ID,)
        client = _Client()
        instance = _Instance(ALT_INSTANCE, client)
        database_pb = admin_v1_pb2.Database(name=self.DATABASE_NAME)
        klass = self._getTargetClass()

        with self.assertRaises(ValueError):
            klass.from_pb(database_pb, instance)

    def test_from_pb_success_w_explicit_pool(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        database_pb = admin_v1_pb2.Database(name=self.DATABASE_NAME)
        klass = self._getTargetClass()
        pool = _Pool()

        database = klass.from_pb(database_pb, instance, pool=pool)

        self.assertTrue(isinstance(database, klass))
        self.assertEqual(database._instance, instance)
        self.assertEqual(database.database_id, self.DATABASE_ID)
        self.assertIs(database._pool, pool)

    def test_from_pb_success_w_hyphen_w_default_pool(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)
        from google.cloud.spanner.pool import BurstyPool

        DATABASE_ID_HYPHEN = 'database-id'
        DATABASE_NAME_HYPHEN = (
            self.INSTANCE_NAME + '/databases/' + DATABASE_ID_HYPHEN)
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client)
        database_pb = admin_v1_pb2.Database(name=DATABASE_NAME_HYPHEN)
        klass = self._getTargetClass()

        database = klass.from_pb(database_pb, instance)

        self.assertTrue(isinstance(database, klass))
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

    def test_spanner_api_property(self):
        from google.cloud._testing import _Monkey
        from google.cloud.spanner import database as MUT

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        _client = object()
        _clients = [_client]

        def _mock_spanner_client(*args, **kwargs):
            self.assertIsInstance(args, tuple)
            self.assertEqual(kwargs['lib_name'], 'gccl')
            self.assertEqual(kwargs['lib_version'], __version__)
            return _clients.pop(0)

        with _Monkey(MUT, SpannerClient=_mock_spanner_client):
            api = database.spanner_api
            self.assertTrue(api is _client)
            # API instance is cached
            again = database.spanner_api
            self.assertTrue(again is api)

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
        comparison_val = (database1 != database2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        pool1, pool2 = _Pool(), _Pool()
        database1 = self._make_one('database_id1', 'instance1', pool=pool1)
        database2 = self._make_one('database_id2', 'instance2', pool=pool2)
        self.assertNotEqual(database1, database2)

    def test_create_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _random_gax_error=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(GaxError):
            database.create()

        (parent, create_statement, extra_statements,
         options) = api._created_database
        self.assertEqual(parent, self.INSTANCE_NAME)
        self.assertEqual(create_statement,
                         'CREATE DATABASE %s' % self.DATABASE_ID)
        self.assertEqual(extra_statements, [])
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_create_already_exists(self):
        from google.cloud.exceptions import Conflict

        DATABASE_ID_HYPHEN = 'database-id'
        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _create_database_conflict=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(DATABASE_ID_HYPHEN, instance, pool=pool)

        with self.assertRaises(Conflict):
            database.create()

        (parent, create_statement, extra_statements,
         options) = api._created_database
        self.assertEqual(parent, self.INSTANCE_NAME)
        self.assertEqual(create_statement,
                         'CREATE DATABASE `%s`' % DATABASE_ID_HYPHEN)
        self.assertEqual(extra_statements, [])
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_create_instance_not_found(self):
        from google.cloud.exceptions import NotFound

        DATABASE_ID_HYPHEN = 'database-id'
        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _database_not_found=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(DATABASE_ID_HYPHEN, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.create()

        (parent, create_statement, extra_statements,
         options) = api._created_database
        self.assertEqual(parent, self.INSTANCE_NAME)
        self.assertEqual(create_statement,
                         'CREATE DATABASE `%s`' % DATABASE_ID_HYPHEN)
        self.assertEqual(extra_statements, [])
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_create_success(self):
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        op_future = _FauxOperationFuture()
        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _create_database_response=op_future)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(
            self.DATABASE_ID, instance, ddl_statements=DDL_STATEMENTS,
            pool=pool)

        future = database.create()

        self.assertIs(future, op_future)
        self.assertEqual(future.caller_metadata,
                         {'request_type': 'CreateDatabase'})

        (parent, create_statement, extra_statements,
         options) = api._created_database
        self.assertEqual(parent, self.INSTANCE_NAME)
        self.assertEqual(create_statement,
                         'CREATE DATABASE %s' % self.DATABASE_ID)
        self.assertEqual(extra_statements, DDL_STATEMENTS)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_exists_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _random_gax_error=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(GaxError):
            database.exists()

        name, options = api._got_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_exists_not_found(self):
        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _database_not_found=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        self.assertFalse(database.exists())

        name, options = api._got_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_exists_success(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        client = _Client()
        ddl_pb = admin_v1_pb2.GetDatabaseDdlResponse(
            statements=DDL_STATEMENTS)
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _get_database_ddl_response=ddl_pb)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        self.assertTrue(database.exists())

        name, options = api._got_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_reload_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _random_gax_error=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(GaxError):
            database.reload()

        name, options = api._got_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_reload_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _database_not_found=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.reload()

        name, options = api._got_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_reload_success(self):
        from google.cloud.proto.spanner.admin.database.v1 import (
            spanner_database_admin_pb2 as admin_v1_pb2)
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        client = _Client()
        ddl_pb = admin_v1_pb2.GetDatabaseDdlResponse(
            statements=DDL_STATEMENTS)
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _get_database_ddl_response=ddl_pb)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        database.reload()

        self.assertEqual(database._ddl_statements, tuple(DDL_STATEMENTS))

        name, options = api._got_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_update_ddl_grpc_error(self):
        from google.gax.errors import GaxError
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _random_gax_error=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(GaxError):
            database.update_ddl(DDL_STATEMENTS)

        name, statements, op_id, options = api._updated_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(statements, DDL_STATEMENTS)
        self.assertEqual(op_id, '')
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_update_ddl_not_found(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _database_not_found=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.update_ddl(DDL_STATEMENTS)

        name, statements, op_id, options = api._updated_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(statements, DDL_STATEMENTS)
        self.assertEqual(op_id, '')
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_update_ddl(self):
        from google.cloud.spanner._fixtures import DDL_STATEMENTS

        op_future = _FauxOperationFuture()
        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _update_database_ddl_response=op_future)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        future = database.update_ddl(DDL_STATEMENTS)

        self.assertIs(future, op_future)
        self.assertEqual(future.caller_metadata,
                         {'request_type': 'UpdateDatabaseDdl'})

        name, statements, op_id, options = api._updated_database_ddl
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(statements, DDL_STATEMENTS)
        self.assertEqual(op_id, '')
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_drop_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _random_gax_error=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(GaxError):
            database.drop()

        name, options = api._dropped_database
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_drop_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _database_not_found=True)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        with self.assertRaises(NotFound):
            database.drop()

        name, options = api._dropped_database
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_drop_success(self):
        from google.protobuf.empty_pb2 import Empty

        client = _Client()
        api = client.database_admin_api = _FauxDatabaseAdminAPI(
            _drop_database_response=Empty())
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        database.drop()

        name, options = api._dropped_database
        self.assertEqual(name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_session_factory(self):
        from google.cloud.spanner.session import Session

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        session = database.session()

        self.assertTrue(isinstance(session, Session))
        self.assertTrue(session.session_id is None)
        self.assertTrue(session._database is database)

    def test_execute_sql_defaults(self):
        QUERY = 'SELECT * FROM employees'
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        session._execute_result = []
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        rows = list(database.execute_sql(QUERY))

        self.assertEqual(rows, [])
        self.assertEqual(session._executed, (QUERY, None, None, None, b''))

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

        committed = database.run_in_transaction(
            _unit_of_work, SINCE, until=UNTIL)

        self.assertEqual(committed, NOW)
        self.assertEqual(session._retried,
                         (_unit_of_work, (SINCE,), {'until': UNTIL}))

    def test_read(self):
        from google.cloud.spanner.keyset import KeySet

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        KEYS = ['bharney@example.com', 'phred@example.com']
        KEYSET = KeySet(keys=KEYS)
        INDEX = 'email-address-index'
        LIMIT = 20
        TOKEN = b'DEADBEEF'
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        rows = list(database.read(
            TABLE_NAME, COLUMNS, KEYSET, INDEX, LIMIT, TOKEN))

        self.assertEqual(rows, [])

        (table, columns, key_set, index, limit,
         resume_token) = session._read_with

        self.assertEqual(table, TABLE_NAME)
        self.assertEqual(columns, COLUMNS)
        self.assertEqual(key_set, KEYSET)
        self.assertEqual(index, INDEX)
        self.assertEqual(limit, LIMIT)
        self.assertEqual(resume_token, TOKEN)

    def test_batch(self):
        from google.cloud.spanner.database import BatchCheckout

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.batch()
        self.assertIsInstance(checkout, BatchCheckout)
        self.assertTrue(checkout._database is database)

    def test_snapshot_defaults(self):
        from google.cloud.spanner.database import SnapshotCheckout

        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot()
        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertIsNone(checkout._max_staleness)
        self.assertIsNone(checkout._exact_staleness)

    def test_snapshot_w_read_timestamp(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.spanner.database import SnapshotCheckout

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot(read_timestamp=now)

        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertTrue(checkout._database is database)
        self.assertEqual(checkout._read_timestamp, now)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertIsNone(checkout._max_staleness)
        self.assertIsNone(checkout._exact_staleness)

    def test_snapshot_w_min_read_timestamp(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.spanner.database import SnapshotCheckout

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot(min_read_timestamp=now)

        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertEqual(checkout._min_read_timestamp, now)
        self.assertIsNone(checkout._max_staleness)
        self.assertIsNone(checkout._exact_staleness)

    def test_snapshot_w_max_staleness(self):
        import datetime
        from google.cloud.spanner.database import SnapshotCheckout

        staleness = datetime.timedelta(seconds=1, microseconds=234567)
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot(max_staleness=staleness)

        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertEqual(checkout._max_staleness, staleness)
        self.assertIsNone(checkout._exact_staleness)

    def test_snapshot_w_exact_staleness(self):
        import datetime
        from google.cloud.spanner.database import SnapshotCheckout

        staleness = datetime.timedelta(seconds=1, microseconds=234567)
        client = _Client()
        instance = _Instance(self.INSTANCE_NAME, client=client)
        pool = _Pool()
        session = _Session()
        pool.put(session)
        database = self._make_one(self.DATABASE_ID, instance, pool=pool)

        checkout = database.snapshot(exact_staleness=staleness)

        self.assertIsInstance(checkout, SnapshotCheckout)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertIsNone(checkout._max_staleness)
        self.assertEqual(checkout._exact_staleness, staleness)


class TestBatchCheckout(_BaseTest):

    def _getTargetClass(self):
        from google.cloud.spanner.database import BatchCheckout

        return BatchCheckout

    def test_ctor(self):
        database = _Database(self.DATABASE_NAME)
        checkout = self._make_one(database)
        self.assertTrue(checkout._database is database)

    def test_context_mgr_success(self):
        import datetime
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            TransactionOptions)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner.batch import Batch

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database(self.DATABASE_NAME)
        api = database.spanner_api = _FauxSpannerClient()
        api._commit_response = response
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
        (session_name, mutations, single_use_txn,
         options) = api._committed
        self.assertIs(session_name, self.SESSION_NAME)
        self.assertEqual(mutations, [])
        self.assertIsInstance(single_use_txn, TransactionOptions)
        self.assertTrue(single_use_txn.HasField('read_write'))
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_context_mgr_failure(self):
        from google.cloud.spanner.batch import Batch

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

    def _getTargetClass(self):
        from google.cloud.spanner.database import SnapshotCheckout

        return SnapshotCheckout

    def test_ctor_defaults(self):
        from google.cloud.spanner.snapshot import Snapshot

        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertIsNone(checkout._max_staleness)
        self.assertIsNone(checkout._exact_staleness)

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertTrue(snapshot._strong)

        self.assertIs(pool._session, session)

    def test_ctor_w_read_timestamp(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.spanner.snapshot import Snapshot

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database, read_timestamp=now)
        self.assertTrue(checkout._database is database)
        self.assertEqual(checkout._read_timestamp, now)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertIsNone(checkout._max_staleness)
        self.assertIsNone(checkout._exact_staleness)

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertFalse(snapshot._strong)
            self.assertEqual(snapshot._read_timestamp, now)

        self.assertIs(pool._session, session)

    def test_ctor_w_min_read_timestamp(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.spanner.snapshot import Snapshot

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database, min_read_timestamp=now)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertEqual(checkout._min_read_timestamp, now)
        self.assertIsNone(checkout._max_staleness)
        self.assertIsNone(checkout._exact_staleness)

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertFalse(snapshot._strong)
            self.assertEqual(snapshot._min_read_timestamp, now)

        self.assertIs(pool._session, session)

    def test_ctor_w_max_staleness(self):
        import datetime
        from google.cloud.spanner.snapshot import Snapshot

        staleness = datetime.timedelta(seconds=1, microseconds=234567)
        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database, max_staleness=staleness)
        self.assertTrue(checkout._database is database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertEqual(checkout._max_staleness, staleness)
        self.assertIsNone(checkout._exact_staleness)

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertFalse(snapshot._strong)
            self.assertEqual(snapshot._max_staleness, staleness)

        self.assertIs(pool._session, session)

    def test_ctor_w_exact_staleness(self):
        import datetime
        from google.cloud.spanner.snapshot import Snapshot

        staleness = datetime.timedelta(seconds=1, microseconds=234567)
        database = _Database(self.DATABASE_NAME)
        session = _Session(database)
        pool = database._pool = _Pool()
        pool.put(session)

        checkout = self._make_one(database, exact_staleness=staleness)

        self.assertIs(checkout._database, database)
        self.assertIsNone(checkout._read_timestamp)
        self.assertIsNone(checkout._min_read_timestamp)
        self.assertIsNone(checkout._max_staleness)
        self.assertEqual(checkout._exact_staleness, staleness)

        with checkout as snapshot:
            self.assertIsNone(pool._session)
            self.assertIsInstance(snapshot, Snapshot)
            self.assertIs(snapshot._session, session)
            self.assertFalse(snapshot._strong)
            self.assertEqual(snapshot._exact_staleness, staleness)

        self.assertIs(pool._session, session)

    def test_context_mgr_failure(self):
        from google.cloud.spanner.snapshot import Snapshot

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


class _Client(object):

    def __init__(self, project=TestDatabase.PROJECT_ID):
        self.project = project
        self.project_name = 'projects/' + self.project


class _Instance(object):

    def __init__(self, name, client=None):
        self.name = name
        self.instance_id = name.rsplit('/', 1)[1]
        self._client = client


class _Database(object):

    def __init__(self, name, instance=None):
        self.name = name
        self.database_id = name.rsplit('/', 1)[1]
        self._instance = instance


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

    def __init__(self, database=None, name=_BaseTest.SESSION_NAME):
        self._database = database
        self.name = name

    def execute_sql(self, sql, params, param_types, query_mode, resume_token):
        self._executed = (sql, params, param_types, query_mode, resume_token)
        return iter(self._rows)

    def run_in_transaction(self, func, *args, **kw):
        self._retried = (func, args, kw)
        return self._committed

    def read(self, table, columns, keyset, index, limit, resume_token):
        self._read_with = (table, columns, keyset, index, limit, resume_token)
        return iter(self._rows)


class _SessionPB(object):
    name = TestDatabase.SESSION_NAME


class _FauxOperationFuture(object):
    pass


class _FauxSpannerClient(_GAXBaseAPI):

    _committed = None

    def commit(self, session, mutations,
               transaction_id='', single_use_transaction=None, options=None):
        assert transaction_id == ''
        self._committed = (session, mutations, single_use_transaction, options)
        return self._commit_response


class _FauxDatabaseAdminAPI(_GAXBaseAPI):

    _create_database_conflict = False
    _database_not_found = False

    def _make_grpc_already_exists(self):
        from grpc.beta.interfaces import StatusCode

        return self._make_grpc_error(StatusCode.ALREADY_EXISTS)

    def create_database(self, parent, create_statement, extra_statements=None,
                        options=None):
        from google.gax.errors import GaxError

        self._created_database = (
            parent, create_statement, extra_statements, options)
        if self._random_gax_error:
            raise GaxError('error')
        if self._create_database_conflict:
            raise GaxError('conflict', self._make_grpc_already_exists())
        if self._database_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._create_database_response

    def get_database_ddl(self, database, options=None):
        from google.gax.errors import GaxError

        self._got_database_ddl = database, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._database_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._get_database_ddl_response

    def drop_database(self, database, options=None):
        from google.gax.errors import GaxError

        self._dropped_database = database, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._database_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._drop_database_response

    def update_database_ddl(self, database, statements, operation_id,
                            options=None):
        from google.gax.errors import GaxError

        self._updated_database_ddl = (
            database, statements, operation_id, options)
        if self._random_gax_error:
            raise GaxError('error')
        if self._database_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._update_database_ddl_response
