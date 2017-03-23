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

import operator
import os
import unittest

from google.cloud.proto.spanner.v1.type_pb2 import STRING
from google.cloud.proto.spanner.v1.type_pb2 import Type
from google.cloud.spanner.client import Client
from google.cloud.spanner.pool import BurstyPool
from google.cloud.spanner._fixtures import DDL_STATEMENTS

from test_utils.retry import RetryErrors
from test_utils.retry import RetryInstanceState
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id

IS_CIRCLE = os.getenv('CIRCLECI') == 'true'
CREATE_INSTANCE = IS_CIRCLE or os.getenv(
    'GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE') is not None

if CREATE_INSTANCE:
    INSTANCE_ID = 'google-cloud' + unique_resource_id('-')
else:
    INSTANCE_ID = os.environ.get('GOOGLE_CLOUD_TESTS_SPANNER_INSTANCE',
                                 'google-cloud-python-systest')
DATABASE_ID = 'test_database'
EXISTING_INSTANCES = []


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    INSTANCE_CONFIG = None
    INSTANCE = None


def _retry_on_unavailable(exc):
    """Retry only errors whose status code is 'UNAVAILABLE'."""
    from grpc import StatusCode
    return exc.code() == StatusCode.UNAVAILABLE


def _has_all_ddl(database):
    return len(database.ddl_statements) == len(DDL_STATEMENTS)


def setUpModule():
    from grpc._channel import _Rendezvous
    Config.CLIENT = Client()
    retry = RetryErrors(_Rendezvous, error_predicate=_retry_on_unavailable)

    configs = list(retry(Config.CLIENT.list_instance_configs)())

    if len(configs) < 1:
        raise ValueError('List instance configs failed in module set up.')

    Config.INSTANCE_CONFIG = configs[0]
    config_name = configs[0].name

    def _list_instances():
        return list(Config.CLIENT.list_instances())

    instances = retry(_list_instances)()
    EXISTING_INSTANCES[:] = instances

    if CREATE_INSTANCE:
        Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID, config_name)
        created_op = Config.INSTANCE.create()
        created_op.result(30)  # block until completion

    else:
        Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID)
        Config.INSTANCE.reload()


def tearDownModule():
    if CREATE_INSTANCE:
        Config.INSTANCE.delete()


class TestInstanceAdminAPI(unittest.TestCase):

    def setUp(self):
        self.instances_to_delete = []

    def tearDown(self):
        for instance in self.instances_to_delete:
            instance.delete()

    def test_list_instances(self):
        instances = list(Config.CLIENT.list_instances())
        # We have added one new instance in `setUpModule`.
        if CREATE_INSTANCE:
            self.assertEqual(len(instances), len(EXISTING_INSTANCES) + 1)
        for instance in instances:
            instance_existence = (instance in EXISTING_INSTANCES or
                                  instance == Config.INSTANCE)
            self.assertTrue(instance_existence)

    def test_reload_instance(self):
        # Use same arguments as Config.INSTANCE (created in `setUpModule`)
        # so we can use reload() on a fresh instance.
        instance = Config.CLIENT.instance(
            INSTANCE_ID, Config.INSTANCE_CONFIG.name)
        # Make sure metadata unset before reloading.
        instance.display_name = None

        instance.reload()
        self.assertEqual(instance.display_name, Config.INSTANCE.display_name)

    @unittest.skipUnless(CREATE_INSTANCE, 'Skipping instance creation')
    def test_create_instance(self):
        ALT_INSTANCE_ID = 'new' + unique_resource_id('-')
        instance = Config.CLIENT.instance(
            ALT_INSTANCE_ID, Config.INSTANCE_CONFIG.name)
        operation = instance.create()
        # Make sure this instance gets deleted after the test case.
        self.instances_to_delete.append(instance)

        # We want to make sure the operation completes.
        operation.result(30)  # raises on failure / timeout.

        # Create a new instance instance and make sure it is the same.
        instance_alt = Config.CLIENT.instance(
            ALT_INSTANCE_ID, Config.INSTANCE_CONFIG.name)
        instance_alt.reload()

        self.assertEqual(instance, instance_alt)
        self.assertEqual(instance.display_name, instance_alt.display_name)

    def test_update_instance(self):
        OLD_DISPLAY_NAME = Config.INSTANCE.display_name
        NEW_DISPLAY_NAME = 'Foo Bar Baz'
        Config.INSTANCE.display_name = NEW_DISPLAY_NAME
        operation = Config.INSTANCE.update()

        # We want to make sure the operation completes.
        operation.result(30)  # raises on failure / timeout.

        # Create a new instance instance and reload it.
        instance_alt = Config.CLIENT.instance(INSTANCE_ID, None)
        self.assertNotEqual(instance_alt.display_name, NEW_DISPLAY_NAME)
        instance_alt.reload()
        self.assertEqual(instance_alt.display_name, NEW_DISPLAY_NAME)

        # Make sure to put the instance back the way it was for the
        # other test cases.
        Config.INSTANCE.display_name = OLD_DISPLAY_NAME
        Config.INSTANCE.update()


class TestDatabaseAdminAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pool = BurstyPool()
        cls._db = Config.INSTANCE.database(DATABASE_ID, pool=pool)
        cls._db.create()

    @classmethod
    def tearDownClass(cls):
        cls._db.drop()

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.drop()

    def test_list_databases(self):
        # Since `Config.INSTANCE` is newly created in `setUpModule`, the
        # database created in `setUpClass` here will be the only one.
        databases = list(Config.INSTANCE.list_databases())
        self.assertEqual(databases, [self._db])

    def test_create_database(self):
        pool = BurstyPool()
        temp_db_id = 'temp-db'  # test w/ hyphen
        temp_db = Config.INSTANCE.database(temp_db_id, pool=pool)
        operation = temp_db.create()
        self.to_delete.append(temp_db)

        # We want to make sure the operation completes.
        operation.result(30)  # raises on failure / timeout.

        name_attr = operator.attrgetter('name')
        expected = sorted([temp_db, self._db], key=name_attr)

        databases = list(Config.INSTANCE.list_databases())
        found = sorted(databases, key=name_attr)
        self.assertEqual(found, expected)

    def test_update_database_ddl(self):
        pool = BurstyPool()
        temp_db_id = 'temp_db'
        temp_db = Config.INSTANCE.database(temp_db_id, pool=pool)
        create_op = temp_db.create()
        self.to_delete.append(temp_db)

        # We want to make sure the operation completes.
        create_op.result(90)  # raises on failure / timeout.

        operation = temp_db.update_ddl(DDL_STATEMENTS)

        # We want to make sure the operation completes.
        operation.result(90)  # raises on failure / timeout.

        temp_db.reload()

        self.assertEqual(len(temp_db.ddl_statements), len(DDL_STATEMENTS))


class TestSessionAPI(unittest.TestCase):
    TABLE = 'contacts'
    COLUMNS = ('contact_id', 'first_name', 'last_name', 'email')
    ROW_DATA = (
        (1, u'Phred', u'Phlyntstone', u'phred@example.com'),
        (2, u'Bharney', u'Rhubble', u'bharney@example.com'),
        (3, u'Wylma', u'Phlyntstone', u'wylma@example.com'),
    )
    SQL = 'SELECT * FROM contacts ORDER BY contact_id'

    @classmethod
    def setUpClass(cls):
        pool = BurstyPool()
        cls._db = Config.INSTANCE.database(
            DATABASE_ID, ddl_statements=DDL_STATEMENTS, pool=pool)
        operation = cls._db.create()
        operation.result(30)  # raises on failure / timeout.

    @classmethod
    def tearDownClass(cls):
        cls._db.drop()

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def _check_row_data(self, row_data):
        self.assertEqual(len(row_data), len(self.ROW_DATA))
        for found, expected in zip(row_data, self.ROW_DATA):
            self.assertEqual(len(found), len(expected))
            for f_cell, e_cell in zip(found, expected):
                self.assertEqual(f_cell, e_cell)

    def test_session_crud(self):
        retry_true = RetryResult(operator.truth)
        retry_false = RetryResult(operator.not_)
        session = self._db.session()
        self.assertFalse(session.exists())
        session.create()
        retry_true(session.exists)()
        session.delete()
        retry_false(session.exists)()

    def test_batch_insert_then_read(self):
        from google.cloud.spanner import KeySet
        keyset = KeySet(all_=True)

        retry = RetryInstanceState(_has_all_ddl)
        retry(self._db.reload)()

        session = self._db.session()
        session.create()
        self.to_delete.append(session)

        batch = session.batch()
        batch.delete(self.TABLE, keyset)
        batch.insert(self.TABLE, self.COLUMNS, self.ROW_DATA)
        batch.commit()

        snapshot = session.snapshot(read_timestamp=batch.committed)
        rows = list(snapshot.read(self.TABLE, self.COLUMNS, keyset))
        self._check_row_data(rows)

    def test_batch_insert_or_update_then_query(self):

        retry = RetryInstanceState(_has_all_ddl)
        retry(self._db.reload)()

        session = self._db.session()
        session.create()
        self.to_delete.append(session)

        with session.batch() as batch:
            batch.insert_or_update(self.TABLE, self.COLUMNS, self.ROW_DATA)

        snapshot = session.snapshot(read_timestamp=batch.committed)
        rows = list(snapshot.execute_sql(self.SQL))
        self._check_row_data(rows)

    def test_transaction_read_and_insert_then_rollback(self):
        from google.cloud.spanner import KeySet
        keyset = KeySet(all_=True)

        retry = RetryInstanceState(_has_all_ddl)
        retry(self._db.reload)()

        session = self._db.session()
        session.create()
        self.to_delete.append(session)

        with session.batch() as batch:
            batch.delete(self.TABLE, keyset)

        transaction = session.transaction()
        transaction.begin()
        rows = list(transaction.read(self.TABLE, self.COLUMNS, keyset))
        self.assertEqual(rows, [])

        transaction.insert(self.TABLE, self.COLUMNS, self.ROW_DATA)

        # Inserted rows can't be read until after commit.
        rows = list(transaction.read(self.TABLE, self.COLUMNS, keyset))
        self.assertEqual(rows, [])
        transaction.rollback()

        rows = list(session.read(self.TABLE, self.COLUMNS, keyset))
        self.assertEqual(rows, [])

    def test_transaction_read_and_insert_or_update_then_commit(self):
        from google.cloud.spanner import KeySet
        keyset = KeySet(all_=True)

        retry = RetryInstanceState(_has_all_ddl)
        retry(self._db.reload)()

        session = self._db.session()
        session.create()
        self.to_delete.append(session)

        with session.batch() as batch:
            batch.delete(self.TABLE, keyset)

        with session.transaction() as transaction:
            rows = list(transaction.read(self.TABLE, self.COLUMNS, keyset))
            self.assertEqual(rows, [])

            transaction.insert_or_update(
                self.TABLE, self.COLUMNS, self.ROW_DATA)

            # Inserted rows can't be read until after commit.
            rows = list(transaction.read(self.TABLE, self.COLUMNS, keyset))
            self.assertEqual(rows, [])

        rows = list(session.read(self.TABLE, self.COLUMNS, keyset))
        self._check_row_data(rows)

    def _set_up_table(self, row_count):
        from google.cloud.spanner import KeySet

        def _row_data(max_index):
            for index in range(max_index):
                yield [index, 'First%09d' % (index,), 'Last09%d' % (index),
                       'test-%09d@example.com' % (index,)]

        keyset = KeySet(all_=True)

        retry = RetryInstanceState(_has_all_ddl)
        retry(self._db.reload)()

        session = self._db.session()
        session.create()
        self.to_delete.append(session)

        with session.transaction() as transaction:
            transaction.delete(self.TABLE, keyset)
            transaction.insert(self.TABLE, self.COLUMNS, _row_data(row_count))

        return session, keyset, transaction.committed

    def test_read_w_manual_consume(self):
        ROW_COUNT = 4000
        session, keyset, committed = self._set_up_table(ROW_COUNT)

        snapshot = session.snapshot(read_timestamp=committed)
        streamed = snapshot.read(self.TABLE, self.COLUMNS, keyset)

        retrieved = 0
        while True:
            try:
                streamed.consume_next()
            except StopIteration:
                break
            retrieved += len(streamed.rows)
            streamed.rows[:] = ()

        self.assertEqual(retrieved, ROW_COUNT)
        self.assertEqual(streamed._current_row, [])
        self.assertEqual(streamed._pending_chunk, None)

    def test_execute_sql_w_manual_consume(self):
        ROW_COUNT = 4000
        session, _, committed = self._set_up_table(ROW_COUNT)

        snapshot = session.snapshot(read_timestamp=committed)
        streamed = snapshot.execute_sql(self.SQL)

        retrieved = 0
        while True:
            try:
                streamed.consume_next()
            except StopIteration:
                break
            retrieved += len(streamed.rows)
            streamed.rows[:] = ()

        self.assertEqual(retrieved, ROW_COUNT)
        self.assertEqual(streamed._current_row, [])
        self.assertEqual(streamed._pending_chunk, None)

    def test_execute_sql_w_query_param(self):
        SQL = 'SELECT * FROM contacts WHERE first_name = @first_name'
        ROW_COUNT = 10
        session, _, committed = self._set_up_table(ROW_COUNT)

        snapshot = session.snapshot(read_timestamp=committed)
        rows = list(snapshot.execute_sql(
            SQL,
            params={'first_name': 'First%09d' % (0,)},
            param_types={'first_name': Type(code=STRING)},
        ))

        self.assertEqual(len(rows), 1)
