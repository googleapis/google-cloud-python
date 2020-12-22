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

import hashlib
import os
import pickle
import time
import unittest

from google.api_core import exceptions

from google.cloud.spanner_v1 import BurstyPool
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.instance import Backup
from google.cloud.spanner_v1.instance import Instance

from google.cloud.spanner_dbapi.connection import Connection

from test_utils.retry import RetryErrors

from .test_system import (
    CREATE_INSTANCE,
    EXISTING_INSTANCES,
    INSTANCE_ID,
    USE_EMULATOR,
    _list_instances,
    Config,
)


def setUpModule():
    if USE_EMULATOR:
        from google.auth.credentials import AnonymousCredentials

        emulator_project = os.getenv("GCLOUD_PROJECT", "emulator-test-project")
        Config.CLIENT = Client(
            project=emulator_project, credentials=AnonymousCredentials()
        )
    else:
        Config.CLIENT = Client()
    retry = RetryErrors(exceptions.ServiceUnavailable)

    configs = list(retry(Config.CLIENT.list_instance_configs)())

    instances = retry(_list_instances)()
    EXISTING_INSTANCES[:] = instances

    # Delete test instances that are older than an hour.
    cutoff = int(time.time()) - 1 * 60 * 60
    for instance_pb in Config.CLIENT.list_instances(
        "labels.python-spanner-dbapi-systests:true"
    ):
        instance = Instance.from_pb(instance_pb, Config.CLIENT)
        if "created" not in instance.labels:
            continue
        create_time = int(instance.labels["created"])
        if create_time > cutoff:
            continue
        # Instance cannot be deleted while backups exist.
        for backup_pb in instance.list_backups():
            backup = Backup.from_pb(backup_pb, instance)
            backup.delete()
        instance.delete()

    if CREATE_INSTANCE:
        if not USE_EMULATOR:
            # Defend against back-end returning configs for regions we aren't
            # actually allowed to use.
            configs = [config for config in configs if "-us-" in config.name]

        if not configs:
            raise ValueError("List instance configs failed in module set up.")

        Config.INSTANCE_CONFIG = configs[0]
        config_name = configs[0].name
        create_time = str(int(time.time()))
        labels = {"python-spanner-dbapi-systests": "true", "created": create_time}

        Config.INSTANCE = Config.CLIENT.instance(
            INSTANCE_ID, config_name, labels=labels
        )
        created_op = Config.INSTANCE.create()
        created_op.result(30)  # block until completion

    else:
        Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID)
        Config.INSTANCE.reload()


def tearDownModule():
    if CREATE_INSTANCE:
        Config.INSTANCE.delete()


class TestTransactionsManagement(unittest.TestCase):
    """Transactions management support tests."""

    DATABASE_NAME = "db-api-transactions-management"

    DDL_STATEMENTS = (
        """CREATE TABLE contacts (
            contact_id INT64,
            first_name STRING(1024),
            last_name STRING(1024),
            email STRING(1024)
        )
        PRIMARY KEY (contact_id)""",
    )

    @classmethod
    def setUpClass(cls):
        """Create a test database."""
        cls._db = Config.INSTANCE.database(
            cls.DATABASE_NAME,
            ddl_statements=cls.DDL_STATEMENTS,
            pool=BurstyPool(labels={"testcase": "database_api"}),
        )
        cls._db.create().result(30)  # raises on failure / timeout.

    @classmethod
    def tearDownClass(cls):
        """Delete the test database."""
        cls._db.drop()

    def tearDown(self):
        """Clear the test table after every test."""
        self._db.run_in_transaction(clear_table)

    def test_commit(self):
        """Test committing a transaction with several statements."""
        want_row = (
            1,
            "updated-first-name",
            "last-name",
            "test.email_updated@domen.ru",
        )
        # connect to the test database
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        # execute several DML statements within one transaction
        cursor.execute(
            """
INSERT INTO contacts (contact_id, first_name, last_name, email)
VALUES (1, 'first-name', 'last-name', 'test.email@domen.ru')
        """
        )
        cursor.execute(
            """
UPDATE contacts
SET first_name = 'updated-first-name'
WHERE first_name = 'first-name'
"""
        )
        cursor.execute(
            """
UPDATE contacts
SET email = 'test.email_updated@domen.ru'
WHERE email = 'test.email@domen.ru'
"""
        )
        conn.commit()

        # read the resulting data from the database
        cursor.execute("SELECT * FROM contacts")
        got_rows = cursor.fetchall()
        conn.commit()

        self.assertEqual(got_rows, [want_row])

        cursor.close()
        conn.close()

    def test_rollback(self):
        """Test rollbacking a transaction with several statements."""
        want_row = (2, "first-name", "last-name", "test.email@domen.ru")
        # connect to the test database
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        cursor.execute(
            """
INSERT INTO contacts (contact_id, first_name, last_name, email)
VALUES (2, 'first-name', 'last-name', 'test.email@domen.ru')
        """
        )
        conn.commit()

        # execute several DMLs with one transaction
        cursor.execute(
            """
UPDATE contacts
SET first_name = 'updated-first-name'
WHERE first_name = 'first-name'
"""
        )
        cursor.execute(
            """
UPDATE contacts
SET email = 'test.email_updated@domen.ru'
WHERE email = 'test.email@domen.ru'
"""
        )
        conn.rollback()

        # read the resulting data from the database
        cursor.execute("SELECT * FROM contacts")
        got_rows = cursor.fetchall()
        conn.commit()

        self.assertEqual(got_rows, [want_row])

        cursor.close()
        conn.close()

    def test_autocommit_mode_change(self):
        """Test auto committing a transaction on `autocommit` mode change."""
        want_row = (
            2,
            "updated-first-name",
            "last-name",
            "test.email@domen.ru",
        )
        # connect to the test database
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        cursor.execute(
            """
INSERT INTO contacts (contact_id, first_name, last_name, email)
VALUES (2, 'first-name', 'last-name', 'test.email@domen.ru')
        """
        )
        cursor.execute(
            """
UPDATE contacts
SET first_name = 'updated-first-name'
WHERE first_name = 'first-name'
"""
        )
        conn.autocommit = True

        # read the resulting data from the database
        cursor.execute("SELECT * FROM contacts")
        got_rows = cursor.fetchall()

        self.assertEqual(got_rows, [want_row])

        cursor.close()
        conn.close()

    def test_rollback_on_connection_closing(self):
        """
        When closing a connection all the pending transactions
        must be rollbacked. Testing if it's working this way.
        """
        want_row = (1, "first-name", "last-name", "test.email@domen.ru")
        # connect to the test database
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        cursor.execute(
            """
INSERT INTO contacts (contact_id, first_name, last_name, email)
VALUES (1, 'first-name', 'last-name', 'test.email@domen.ru')
        """
        )
        conn.commit()

        cursor.execute(
            """
UPDATE contacts
SET first_name = 'updated-first-name'
WHERE first_name = 'first-name'
"""
        )
        conn.close()

        # connect again, as the previous connection is no-op after closing
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        # read the resulting data from the database
        cursor.execute("SELECT * FROM contacts")
        got_rows = cursor.fetchall()
        conn.commit()

        self.assertEqual(got_rows, [want_row])

        cursor.close()
        conn.close()

    def test_results_checksum(self):
        """Test that results checksum is calculated properly."""
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        cursor.execute(
            """
INSERT INTO contacts (contact_id, first_name, last_name, email)
VALUES
    (1, 'first-name', 'last-name', 'test.email@domen.ru'),
    (2, 'first-name2', 'last-name2', 'test.email2@domen.ru')
        """
        )
        self.assertEqual(len(conn._statements), 1)
        conn.commit()

        cursor.execute("SELECT * FROM contacts")
        got_rows = cursor.fetchall()

        self.assertEqual(len(conn._statements), 1)
        conn.commit()

        checksum = hashlib.sha256()
        checksum.update(pickle.dumps(got_rows[0]))
        checksum.update(pickle.dumps(got_rows[1]))

        self.assertEqual(cursor._checksum.checksum.digest(), checksum.digest())

    def test_execute_many(self):
        # connect to the test database
        conn = Connection(Config.INSTANCE, self._db)
        cursor = conn.cursor()

        cursor.execute(
            """
INSERT INTO contacts (contact_id, first_name, last_name, email)
VALUES (1, 'first-name', 'last-name', 'test.email@example.com'),
       (2, 'first-name2', 'last-name2', 'test.email2@example.com')
        """
        )
        conn.commit()

        cursor.executemany(
            """
SELECT * FROM contacts WHERE contact_id = @a1
""",
            ({"a1": 1}, {"a1": 2}),
        )
        res = cursor.fetchall()
        conn.commit()

        self.assertEqual(len(res), 2)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[1][0], 2)

        # checking that execute() and executemany()
        # results are not mixed together
        cursor.execute(
            """
SELECT * FROM contacts WHERE contact_id = 1
""",
        )
        res = cursor.fetchone()
        conn.commit()

        self.assertEqual(res[0], 1)
        conn.close()


def clear_table(transaction):
    """Clear the test table."""
    transaction.execute_update("DELETE FROM contacts WHERE true")
