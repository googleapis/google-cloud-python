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


import time

import unittest2

from gcloud import _helpers
from gcloud.bigtable import client as client_mod
from gcloud.bigtable.happybase.connection import Connection
from gcloud.environment_vars import TESTS_PROJECT


_helpers.PROJECT = TESTS_PROJECT
ZONE = 'us-central1-c'
NOW_MILLIS = int(1000 * time.time())
CLUSTER_ID = 'gcloud-python-%d' % (NOW_MILLIS,)
TABLE_NAME = 'table-name'
ALT_TABLE_NAME = 'other-table'
TTL_FOR_TEST = 3
COL_FAM1 = 'cf1'
COL_FAM2 = 'cf2'
COL_FAM3 = 'cf3'
FAMILIES = {
    COL_FAM1: {'max_versions': 10},
    COL_FAM2: {'max_versions': 1, 'time_to_live': TTL_FOR_TEST},
    COL_FAM3: {},  # use defaults
}


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CONNECTION = None
    TABLE = None


def _operation_wait(operation, max_attempts=5):
    """Wait until an operation has completed.

    :type operation: :class:`gcloud.bigtable.cluster.Operation`
    :param operation: Operation that has not finished.

    :type max_attempts: int
    :param max_attempts: (Optional) The maximum number of times to check if
                         the operation has finished. Defaults to 5.
    """
    total_sleep = 0
    while not operation.finished():
        if total_sleep > max_attempts:
            return False
        time.sleep(1)
        total_sleep += 1

    return True


def set_connection():
    client = client_mod.Client(admin=True)
    cluster = client.cluster(ZONE, CLUSTER_ID)
    client.start()
    operation = cluster.create()
    if not _operation_wait(operation):
        raise RuntimeError('Cluster creation exceed 5 seconds.')
    Config.CONNECTION = Connection(cluster=cluster)


def setUpModule():
    set_connection()
    Config.CONNECTION.create_table(TABLE_NAME, FAMILIES)
    Config.TABLE = Config.CONNECTION.table(TABLE_NAME)


def tearDownModule():
    Config.CONNECTION.delete_table(TABLE_NAME)
    Config.CONNECTION._cluster.delete()
    Config.CONNECTION.close()


class TestConnection(unittest2.TestCase):

    def test_create_and_delete_table(self):
        connection = Config.CONNECTION

        self.assertFalse(ALT_TABLE_NAME in connection.tables())
        connection.create_table(ALT_TABLE_NAME, {COL_FAM1: {}})
        self.assertTrue(ALT_TABLE_NAME in connection.tables())
        connection.delete_table(ALT_TABLE_NAME)
        self.assertFalse(ALT_TABLE_NAME in connection.tables())

    def test_create_table_failure(self):
        connection = Config.CONNECTION

        self.assertFalse(ALT_TABLE_NAME in connection.tables())
        empty_families = {}
        with self.assertRaises(ValueError):
            connection.create_table(ALT_TABLE_NAME, empty_families)
        self.assertFalse(ALT_TABLE_NAME in connection.tables())
