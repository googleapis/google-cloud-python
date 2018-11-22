#!/usr/bin/env python

# Copyright 2018, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Testable usage examples for Google Cloud Bigtable API wrapper

Each example function takes a ``client`` argument (which must be an instance
of :class:`google.cloud.bigtable.client.Client`) and uses it to perform a task
with the API.

To facilitate running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.

.. note::
    This file is under progress and will be updated with more guidance from
    the team. Unit tests will be added with guidance from the team.

"""

import datetime
import pytest

from test_utils.system import unique_resource_id
from google.cloud._helpers import UTC
from google.cloud.bigtable import Client
from google.cloud.bigtable import enums
from google.cloud.bigtable import column_family


INSTANCE_ID = "snippet-" + unique_resource_id('-')
CLUSTER_ID = "clus-1-" + unique_resource_id('-')
TABLE_ID = "tabl-1-" + unique_resource_id('-')
COLUMN_FAMILY_ID = "col_fam_id-" + unique_resource_id('-')
LOCATION_ID = 'us-central1-f'
ALT_LOCATION_ID = 'us-central1-a'
PRODUCTION = enums.Instance.Type.PRODUCTION
SERVER_NODES = 3
STORAGE_TYPE = enums.StorageType.SSD
LABEL_KEY = u'python-snippet'
LABEL_STAMP = datetime.datetime.utcnow() \
                               .replace(microsecond=0, tzinfo=UTC,) \
                               .strftime("%Y-%m-%dt%H-%M-%S")
LABELS = {LABEL_KEY: str(LABEL_STAMP)}
COL_NAME1 = b'col-name1'
CELL_VAL1 = b'cell-val'


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    INSTANCE = None
    TABLE = None


def setup_module():
    client = Config.CLIENT = Client(admin=True)
    Config.INSTANCE = client.instance(INSTANCE_ID,
                                      instance_type=PRODUCTION,
                                      labels=LABELS)
    cluster = Config.INSTANCE.cluster(CLUSTER_ID,
                                      location_id=LOCATION_ID,
                                      serve_nodes=SERVER_NODES,
                                      default_storage_type=STORAGE_TYPE)
    operation = Config.INSTANCE.create(clusters=[cluster])
    # We want to make sure the operation completes.
    operation.result(timeout=100)
    Config.TABLE = Config.INSTANCE.table(TABLE_ID)
    Config.TABLE.create()
    gc_rule = column_family.MaxVersionsGCRule(2)
    column_family1 = Config.TABLE.column_family(COLUMN_FAMILY_ID,
                                                gc_rule=gc_rule)
    column_family1.create()


def teardown_module():
    Config.INSTANCE.delete()


def test_bigtable_create_table():
    # [START bigtable_create_table]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import column_family

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    # Create table without Column families.
    table1 = instance.table("table_id1")
    table1.create()

    # Create table with Column families.
    table2 = instance.table("table_id2")
    # Define the GC policy to retain only the most recent 2 versions.
    max_versions_rule = column_family.MaxVersionsGCRule(2)
    table2.create(column_families={'cf1': max_versions_rule})

    # [END bigtable_create_table]
    assert table1.exists()
    assert table2.exists()
    table1.delete()
    table2.delete()


def test_bigtable_sample_row_keys():
    # [START bigtable_sample_row_keys]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    table = instance.table("table_id1_samplerow")
    # [END bigtable_sample_row_keys]
    initial_split_keys = [b'split_key_1', b'split_key_10',
                          b'split_key_20']
    table.create(initial_split_keys=initial_split_keys)
    # [START bigtable_sample_row_keys]
    data = table.sample_row_keys()
    actual_keys, offset = zip(*[(rk.row_key, rk.offset_bytes) for rk in data])
    # [END bigtable_sample_row_keys]
    initial_split_keys.append(b'')
    assert list(actual_keys) == initial_split_keys
    table.delete()


def test_bigtable_write_read_drop_truncate():
    # [START bigtable_mutate_rows]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    row_keys = [b'row_key_1', b'row_key_2', b'row_key_3', b'row_key_4',
                b'row_key_20', b'row_key_22', b'row_key_200']
    col_name = b'col-name1'
    rows = []
    for i, row_key in enumerate(row_keys):
        value = 'value_{}'.format(i).encode()
        row = table.row(row_key)
        row.set_cell(COLUMN_FAMILY_ID,
                     col_name,
                     value,
                     timestamp=datetime.datetime.utcnow())
        rows.append(row)
    response = table.mutate_rows(rows)
    # validate that all rows written successfully
    for i, status in enumerate(response):
        if status.code is not 0:
            print('Row number {} failed to write'.format(i))
    # [END bigtable_mutate_rows]
    assert len(response) == len(rows)
    # [START bigtable_read_row]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    row_key = 'row_key_1'
    row = table.read_row(row_key)
    # [END bigtable_read_row]
    assert row.row_key.decode('utf-8') == row_key
    # [START bigtable_read_rows]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    # Read full table
    partial_rows = table.read_rows()
    read_rows = [row for row in partial_rows]
    # [END bigtable_read_rows]
    assert len(read_rows) == len(rows)
    # [START bigtable_drop_by_prefix]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    row_key_prefix = b'row_key_2'
    table.drop_by_prefix(row_key_prefix, timeout=200)
    # [END bigtable_drop_by_prefix]
    dropped_row_keys = [b'row_key_2', b'row_key_20',
                        b'row_key_22', b'row_key_200']
    for row in table.read_rows():
        assert row.row_key.decode('utf-8') not in dropped_row_keys

    # [START bigtable_truncate_table]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    table.truncate(timeout=200)
    # [END bigtable_truncate_table]
    rows_data_after_truncate = []
    for row in table.read_rows():
        rows_data_after_truncate.append(row.row_key)
    assert rows_data_after_truncate == []


def test_bigtable_mutations_batcher():
    # [START bigtable_mutations_batcher]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    batcher = table.mutations_batcher()
    # [END bigtable_mutations_batcher]

    # Below code will be used while creating batcher.py snippets.
    # So not removing this code as of now.
    row_keys = [b'row_key_1', b'row_key_2', b'row_key_3', b'row_key_4',
                b'row_key_20', b'row_key_22', b'row_key_200']
    column_name = 'column_name'.encode()
    # Add a single row
    row_key = row_keys[0]
    row = table.row(row_key)
    row.set_cell(COLUMN_FAMILY_ID,
                 column_name,
                 'value-0',
                 timestamp=datetime.datetime.utcnow())
    batcher.mutate(row)
    # Add a collections of rows
    rows = []
    for i in range(1, len(row_keys)):
        row = table.row(row_keys[i])
        value = 'value_{}'.format(i).encode()
        row.set_cell(COLUMN_FAMILY_ID,
                     column_name,
                     value,
                     timestamp=datetime.datetime.utcnow())
        rows.append(row)
    batcher.mutate_rows(rows)
    # batcher will flush current batch if it
    # reaches the max flush_count

    # Manually send the current batch to Cloud Bigtable
    batcher.flush()
    rows_on_table = []
    for row in table.read_rows():
        rows_on_table.append(row.row_key)
    assert len(rows_on_table) == len(row_keys)
    table.truncate(timeout=200)


def test_bigtable_table_column_family():
    # [START bigtable_table_column_family]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    table = instance.table(TABLE_ID)
    column_family_obj = table.column_family(COLUMN_FAMILY_ID)
    # [END bigtable_table_column_family]

    assert column_family_obj.column_family_id == COLUMN_FAMILY_ID


def test_bigtable_list_tables():
    # [START bigtable_list_tables]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    tables_list = instance.list_tables()
    # [END bigtable_list_tables]
    assert len(tables_list) is not 0


def test_bigtable_table_name():
    import re
    # [START bigtable_table_name]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    table = instance.table(TABLE_ID)
    table_name = table.name
    # [END bigtable_table_name]
    _table_name_re = re.compile(r'^projects/(?P<project>[^/]+)/'
                                r'instances/(?P<instance>[^/]+)/tables/'
                                r'(?P<table_id>[_a-zA-Z0-9][-_.a-zA-Z0-9]*)$')
    assert _table_name_re.match(table_name)


def test_bigtable_list_column_families():
    # [START bigtable_list_column_families]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    column_family_list = table.list_column_families()
    # [END bigtable_list_column_families]

    assert len(column_family_list) > 0


def test_bigtable_get_cluster_states():
    # [START bigtable_get_cluster_states]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    get_cluster_states = table.get_cluster_states()
    # [END bigtable_get_cluster_states]

    assert CLUSTER_ID in get_cluster_states


def test_bigtable_table_exists():
    # [START bigtable_check_table_exists]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    table_exists = table.exists()
    # [END bigtable_check_table_exists]
    assert table_exists


def test_bigtable_delete_table():
    # [START bigtable_delete_table]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table("table_id_del")
    # [END bigtable_delete_table]

    table.create()
    assert table.exists()

    # [START bigtable_delete_table]
    table.delete()
    # [END bigtable_delete_table]
    assert not table.exists()


def test_bigtable_table_row():
    # [START bigtable_table_row]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    row_keys = [b'row_key_1', b'row_key_2']
    row1_obj = table.row(row_keys[0])
    row2_obj = table.row(row_keys[1])
    # [END bigtable_table_row]

    row1_obj.set_cell(COLUMN_FAMILY_ID, COL_NAME1, CELL_VAL1)
    row1_obj.commit()
    row2_obj.set_cell(COLUMN_FAMILY_ID, COL_NAME1, CELL_VAL1)
    row2_obj.commit()

    actual_rows_keys = []
    for row in table.read_rows():
        actual_rows_keys.append(row.row_key)

    assert actual_rows_keys == row_keys

    table.truncate(timeout=300)


if __name__ == '__main__':
    pytest.main()
