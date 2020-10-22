# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import unittest
import os

from google.api_core import exceptions

from google.cloud.spanner import Client
from google.cloud.spanner import BurstyPool
from google.cloud.spanner_dbapi.connection import Connection

from test_utils.retry import RetryErrors
from test_utils.system import unique_resource_id


CREATE_INSTANCE = (
    os.getenv("GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE") is not None
)
USE_EMULATOR = os.getenv("SPANNER_EMULATOR_HOST") is not None

if CREATE_INSTANCE:
    INSTANCE_ID = "google-cloud" + unique_resource_id("-")
else:
    INSTANCE_ID = os.environ.get(
        "GOOGLE_CLOUD_TESTS_SPANNER_INSTANCE", "google-cloud-python-systest"
    )
EXISTING_INSTANCES = []

DDL_STATEMENTS = (
    """CREATE TABLE contacts (
            contact_id INT64,
            first_name STRING(1024),
            last_name STRING(1024),
            email STRING(1024)
        )
        PRIMARY KEY (contact_id)""",
)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT = None
    INSTANCE_CONFIG = None
    INSTANCE = None


def _list_instances():
    return list(Config.CLIENT.list_instances())


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

    if CREATE_INSTANCE:
        if not USE_EMULATOR:
            # Defend against back-end returning configs for regions we aren't
            # actually allowed to use.
            configs = [config for config in configs if "-us-" in config.name]

        if not configs:
            raise ValueError("List instance configs failed in module set up.")

        Config.INSTANCE_CONFIG = configs[0]
        config_name = configs[0].name

        Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID, config_name)
        created_op = Config.INSTANCE.create()
        created_op.result(30)  # block until completion
    else:
        Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID)
        Config.INSTANCE.reload()


def tearDownModule():
    """Delete the test instance, if it was created."""
    if CREATE_INSTANCE:
        Config.INSTANCE.delete()


class TestTransactionsManagement(unittest.TestCase):
    """Transactions management support tests."""

    DATABASE_NAME = "db-api-transactions-management"

    @classmethod
    def setUpClass(cls):
        """Create a test database."""
        cls._db = Config.INSTANCE.database(
            cls.DATABASE_NAME,
            ddl_statements=DDL_STATEMENTS,
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


def clear_table(transaction):
    """Clear the test table."""
    transaction.execute_update("DELETE FROM contacts WHERE true")
