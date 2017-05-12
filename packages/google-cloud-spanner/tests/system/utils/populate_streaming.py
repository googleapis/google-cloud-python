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

"""Populate spanner databases with data for streaming system tests."""

from google.cloud.spanner import Client
from google.cloud.spanner.keyset import KeySet
from google.cloud.spanner.pool import BurstyPool

# Import relative to the script's directory
from streaming_utils import DATABASE_NAME
from streaming_utils import INSTANCE_NAME
from streaming_utils import print_func

DDL = """\
CREATE TABLE four_kay (
    pkey INT64,
    chunk_me STRING(4096) )
    PRIMARY KEY (pkey);
CREATE TABLE forty_kay (
    pkey INT64,
    chunk_me STRING(40960) )
    PRIMARY KEY (pkey);
CREATE TABLE four_hundred_kay (
    pkey INT64,
    chunk_me STRING(409600) )
    PRIMARY KEY (pkey);
CREATE TABLE four_meg (
    pkey INT64,
    chunk_me STRING(2097152),
    chunk_me_2 STRING(2097152) )
    PRIMARY KEY (pkey);
"""

DDL_STATEMENTS = [stmt.strip() for stmt in DDL.split(';') if stmt.strip()]


def ensure_database(client):
    instance = client.instance(INSTANCE_NAME)

    if not instance.exists():
        configs = list(client.list_instance_configs())
        config_name = configs[0].name
        print_func("Creating instance: {}".format(INSTANCE_NAME))
        instance = client.instance(INSTANCE_NAME, config_name)
        operation = instance.create()
        operation.result(30)
    else:
        print_func("Instance exists: {}".format(INSTANCE_NAME))
        instance.reload()

    pool = BurstyPool()
    database = instance.database(
        DATABASE_NAME, ddl_statements=DDL_STATEMENTS, pool=pool)

    if not database.exists():
        print_func("Creating database: {}".format(DATABASE_NAME))
        operation = database.create()
        operation.result(30)
    else:
        print_func("Database exists: {}".format(DATABASE_NAME))
        database.reload()

    return database


def populate_table(database, table_name, row_count, val_size):
    all_ = KeySet(all_=True)
    columns = ('pkey', 'chunk_me')
    rows = list(database.execute_sql(
        'SELECT COUNT(*) FROM {}'.format(table_name)))
    assert len(rows) == 1
    count = rows[0][0]
    if count != row_count:
        print_func("Repopulating table: {}".format(table_name))
        chunk_me = 'X' * val_size
        row_data = [(index, chunk_me) for index in range(row_count)]
        with database.batch() as batch:
            batch.delete(table_name, all_)
            batch.insert(table_name, columns, row_data)
    else:
        print_func("Leaving table: {}".format(table_name))


def populate_table_2_columns(database, table_name, row_count, val_size):
    all_ = KeySet(all_=True)
    columns = ('pkey', 'chunk_me', 'chunk_me_2')
    rows = list(database.execute_sql(
        'SELECT COUNT(*) FROM {}'.format(table_name)))
    assert len(rows) == 1
    count = rows[0][0]
    if count != row_count:
        print_func("Repopulating table: {}".format(table_name))
        chunk_me = 'X' * val_size
        row_data = [(index, chunk_me, chunk_me) for index in range(row_count)]
        with database.batch() as batch:
            batch.delete(table_name, all_)
            batch.insert(table_name, columns, row_data)
    else:
        print_func("Leaving table: {}".format(table_name))


def populate_streaming(client):
    database = ensure_database(client)
    populate_table(database, 'four_kay', 1000, 4096)
    populate_table(database, 'forty_kay', 100, 4096 * 10)
    populate_table(database, 'four_hundred_kay', 25, 4096 * 100)
    # Max STRING column size is just larger than 2 Mb, so use two columns
    populate_table_2_columns(database, 'four_meg', 10, 2048 * 1024)


if __name__ == '__main__':
    client = Client()
    populate_streaming(client)
