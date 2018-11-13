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
READY = enums.Cluster.State.READY
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


def test_bigtable_create_instance():
    # [START bigtable_create_prod_instance]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import enums

    my_instance_id = "inst-my-" + unique_resource_id('-')
    my_cluster_id = "clus-my-" + unique_resource_id('-')
    location_id = 'us-central1-f'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD
    production = enums.Instance.Type.PRODUCTION
    labels = {'prod-label': 'prod-label'}

    client = Client(admin=True)
    instance = client.instance(my_instance_id, instance_type=production,
                               labels=labels)
    cluster = instance.cluster(my_cluster_id, location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    operation = instance.create(clusters=[cluster])
    # We want to make sure the operation completes.
    operation.result(timeout=100)
    # [END bigtable_create_prod_instance]
    assert instance.exists()
    instance.delete()


def test_bigtable_create_additional_cluster():
    # [START bigtable_create_cluster]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import enums

    # Assuming that there is an existing instance with `INSTANCE_ID`
    # on the server already.
    # to create an instance see
    # 'https://cloud.google.com/bigtable/docs/creating-instance'

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    cluster_id = "clus-my-" + unique_resource_id('-')
    location_id = 'us-central1-a'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD

    cluster = instance.cluster(cluster_id, location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    operation = cluster.create()
    # We want to make sure the operation completes.
    operation.result(timeout=100)
    # [END bigtable_create_cluster]
    assert cluster.exists()

    cluster.delete()


def test_bigtable_create_app_profile():
    # [START bigtable_create_app_profile]
    from google.cloud.bigtable import Client
    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    app_profile_id = "app-prof-" + unique_resource_id('-')
    description = 'routing policy-multy'
    routing_policy_type = enums.RoutingPolicyType.ANY

    app_profile = instance.app_profile(
        app_profile_id=app_profile_id,
        routing_policy_type=routing_policy_type,
        description=description,
        cluster_id=CLUSTER_ID)

    app_profile = app_profile.create(ignore_warnings=True)
    # [END bigtable_create_app_profile]
    assert app_profile.exists()

    app_profile.delete(ignore_warnings=True)


def test_bigtable_create_table():
    # [START bigtable_create_table]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import column_family

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    # Create table with Column families.
    table1 = instance.table("table_id1_create")
    # Define the GC policy to retain only the most recent 2 versions.
    max_versions_rule = column_family.MaxVersionsGCRule(2)
    table1.create(column_families={'cf1': max_versions_rule})

    # Create table without Column families.
    table2 = instance.table("table_id2_create")
    table2.create()
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
    table.create()

    data = table.sample_row_keys()
    for element in data:
        offset_bytes = str(element).split(":")[1].strip()
    # [END bigtable_sample_row_keys]
    assert offset_bytes == '805306368'
    table.delete()


def test_bigtable_create_column_family():
    # [START bigtable_create_column_family]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import column_family

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    table = instance.table(TABLE_ID)
    column_family_id = 'column-family-id1'

    gc_rule = column_family.MaxVersionsGCRule(1)
    column_family = table.column_family(column_family_id, gc_rule=gc_rule)
    column_family.create()
    # [END bigtable_create_column_family]

    col_fams = table.list_column_families()
    assert column_family_id in col_fams


def test_bigtable_mutations_batcher_read_rows():
    # [START bigtable_mutate_rows]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    row_keys = [b'row_key_1', b'row_key_2', b'row_key_3', b'row_key_4']
    col_name = b'col-name1'
    cell_val = b'cell-val-abc'
    # [END bigtable_mutate_rows]

    expected_rows_data = []
    for row in row_keys:
        expected_rows_data.append(row.decode('utf-8'))
        expected_rows_data.append(cell_val.decode('utf-8'))

    # [START bigtable_mutate_rows]
    rows = []
    for row_key in row_keys:
        row = table.row(row_key)
        row.set_cell(COLUMN_FAMILY_ID, col_name, cell_val)
        rows.append(row)

    batcher = table.mutations_batcher(flush_count=3)

    # In batcher mutate will flush current batch if it
    # reaches the max flush_count
    batcher.mutate_rows(rows)
    batcher.flush()
    # [END bigtable_mutate_rows]

    # [START bigtable_read_rows]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    rows_data = table.read_rows()
    # [END bigtable_read_rows]

    actual_rows_data = []
    for row in rows_data:
        actual_rows_data.append(row.row_key.decode('utf-8'))
        actual_rows_data.append(
            row.cells[COLUMN_FAMILY_ID][col_name][0].value.decode('utf-8')
            )

    assert actual_rows_data == expected_rows_data

    table.truncate(timeout=200)


def test_bigtable_drop_by_prefix():
    # [START bigtable_drop_by_prefix]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    # [END bigtable_drop_by_prefix]

    row_keys = [b'row_key_1', b'row_key_2', b'r_key_3', b'r_key_4']
    rows = []
    for row_key in row_keys:
        row = table.row(row_key)
        row.set_cell(COLUMN_FAMILY_ID, b'col-name1', b'cell-val-abc')
        rows.append(row)
    batcher = table.mutations_batcher()
    batcher.mutate_rows(rows)
    batcher.flush()

    # [START bigtable_drop_by_prefix]
    row_key_prefix = b'r_key'
    table.drop_by_prefix(row_key_prefix, timeout=300)
    # [END bigtable_drop_by_prefix]

    rows_data = table.read_rows()
    actual_rows_keys = []
    for row in rows_data:
        actual_rows_keys.append(row.row_key)

    assert actual_rows_keys == [b'row_key_1', b'row_key_2']

    table.truncate(timeout=300)


def test_bigtable_mutate_rows_read_row():
    # [START bigtable_mutations_batcher]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    row_key = b'row-key'
    row_key_alt = b'row-key-alt'
    col_name1 = b'col-name1'
    cell_val1 = b'cell-val'
    cell_val2 = b'cell-val-newer'
    cell_val3 = b'altcol-cell-val'
    cell_val4 = b'foo'
    row1 = table.row(row_key)
    row1.set_cell(COLUMN_FAMILY_ID, col_name1, cell_val1)
    row1.commit()
    row2 = table.row(row_key_alt)
    row2.set_cell(COLUMN_FAMILY_ID, col_name1, cell_val2)
    row2.commit()

    # Change the contents
    row1.set_cell(COLUMN_FAMILY_ID, col_name1, cell_val3)
    row2.set_cell(COLUMN_FAMILY_ID, col_name1, cell_val4)
    rows = [row1, row2]
    statuses = table.mutate_rows(rows)
    # [END bigtable_mutations_batcher]

    result = [status.code for status in statuses]
    expected_result = [0, 0]
    assert result == expected_result

    # [START bigtable_read_row]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    row_key = b'row-key'
    row = table.read_row(row_key)
    # [END bigtable_read_row]

    assert row.row_key == row_key
    assert row.cells[COLUMN_FAMILY_ID][col_name1][0].value == cell_val3

    table.truncate(timeout=300)


def test_bigtable_list_instances():
    # [START bigtable_list_instances]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    (instances_list, failed_locations_list) = client.list_instances()
    # [END bigtable_list_instances]
    assert len(instances_list) is not 0


def test_bigtable_list_clusters_on_instance():
    # [START bigtable_list_clusters_on_instance]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    (clusters_list, failed_locations_list) = instance.list_clusters()
    # [END bigtable_list_clusters_on_instance]
    assert len(clusters_list) is not 0


def test_bigtable_list_clusters_in_project():
    # [START bigtable_list_clusters_in_project]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    (clusters_list, failed_locations_list) = client.list_clusters()
    # [END bigtable_list_clusters_in_project]
    assert len(clusters_list) is not 0


def test_bigtable_list_app_profiles():
    # [START bigtable_list_app_profiles]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    # [END bigtable_list_app_profiles]

    app_profile = instance.app_profile(
        app_profile_id="app-prof-" + unique_resource_id('-'),
        routing_policy_type=enums.RoutingPolicyType.ANY)
    app_profile = app_profile.create(ignore_warnings=True)

    # [START bigtable_list_app_profiles]
    app_profiles_list = instance.list_app_profiles()
    # [END bigtable_list_app_profiles]
    assert len(app_profiles_list) is not 0


def test_bigtable_list_tables():
    # [START bigtable_list_tables]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    tables_list = instance.list_tables()
    # [END bigtable_list_tables]
    assert len(tables_list) is not 0


def test_bigtable_table_name():
    import os
    import json
    # [START bigtable_table_name]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    table = instance.table(TABLE_ID)
    table_name = table.name
    # [END bigtable_table_name]

    cred = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'project_id')
    with open(cred, "r") as read_file:
        data = json.load(read_file)
        project_id = data["project_id"]

    expected_table_name = 'projects/' + project_id + \
        '/instances/' + INSTANCE_ID + \
        '/tables/' + TABLE_ID
    assert table_name == expected_table_name


def test_bigtable_list_column_families():
    # [START bigtable_list_column_families]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    column_family_list = table.list_column_families()
    # [END bigtable_list_column_families]

    assert len(column_family_list) is not 0


def test_bigtable_get_cluster_states():
    # [START bigtable_get_cluster_states]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    get_cluster_states = table.get_cluster_states()
    # [END bigtable_get_cluster_states]

    assert CLUSTER_ID in get_cluster_states


def test_bigtable_instance_exists():
    # [START bigtable_check_instance_exists]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    instance_exists = instance.exists()
    # [END bigtable_check_instance_exists]
    assert instance_exists


def test_bigtable_cluster_exists():
    # [START bigtable_check_cluster_exists]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID)
    cluster_exists = cluster.exists()
    # [END bigtable_check_cluster_exists]
    assert cluster_exists


def test_bigtable_table_exists():
    # [START bigtable_check_table_exists]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)
    table_exists = table.exists()
    # [END bigtable_check_table_exists]
    assert table_exists


def test_bigtable_reload_instance():
    # [START bigtable_reload_instance]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    instance.reload()
    # [END bigtable_reload_instance]
    assert instance.type_ is PRODUCTION.value


def test_bigtable_reload_cluster():
    # [START bigtable_reload_cluster]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID)
    cluster.reload()
    # [END bigtable_reload_cluster]
    assert cluster.serve_nodes is SERVER_NODES


def test_bigtable_update_instance():
    # [START bigtable_update_instance]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    display_name = "My new instance"
    instance.display_name = display_name
    instance.update()
    # [END bigtable_update_instance]
    assert instance.display_name is display_name


def test_bigtable_update_cluster():
    # [START bigtable_update_cluster]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID)
    cluster.serve_nodes = 8
    cluster.update()
    # [END bigtable_update_cluster]
    assert cluster.serve_nodes is 8


def test_bigtable_delete_cluster():
    # [START bigtable_delete_cluster]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster_id = "clus-my-" + unique_resource_id('-')
    # [END bigtable_delete_cluster]

    cluster = instance.cluster(cluster_id, location_id=ALT_LOCATION_ID,
                               serve_nodes=SERVER_NODES,
                               default_storage_type=STORAGE_TYPE)
    operation = cluster.create()
    # We want to make sure the operation completes.
    operation.result(timeout=1000)

    # [START bigtable_delete_cluster]
    cluster_to_delete = instance.cluster(cluster_id)
    cluster_to_delete.delete()
    # [END bigtable_delete_cluster]
    assert not cluster_to_delete.exists()


def test_bigtable_delete_instance():
    # [START bigtable_delete_instance]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance_id_to_delete = "inst-my-" + unique_resource_id('-')
    # [END bigtable_delete_instance]

    cluster_id = "clus-my-" + unique_resource_id('-')

    instance = client.instance(instance_id_to_delete,
                               instance_type=PRODUCTION,
                               labels=LABELS)
    cluster = instance.cluster(cluster_id,
                               location_id=ALT_LOCATION_ID,
                               serve_nodes=SERVER_NODES,
                               default_storage_type=STORAGE_TYPE)
    operation = instance.create(clusters=[cluster])
    # We want to make sure the operation completes.
    operation.result(timeout=100)

    # [START bigtable_delete_instance]
    instance_to_delete = client.instance(instance_id_to_delete)
    instance_to_delete.delete()
    # [END bigtable_delete_instance]

    assert not instance_to_delete.exists()


def test_bigtable_delete_table():
    # [START bigtable_delete_table]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table("table_id_del")
    # [END bigtable_delete_table]

    table.create()

    # [START bigtable_delete_table]
    table.delete()
    # [END bigtable_delete_table]
    assert not table.exists()


def test_bigtable_table_row_truncate_table():
    # [START bigtable_truncate_table]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    # [END bigtable_truncate_table]
    # [START bigtable_table_row]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    table = instance.table(TABLE_ID)

    row_keys = [b'row_key_1', b'row_key_2']
    row1 = table.row(row_keys[0])
    row1.set_cell(COLUMN_FAMILY_ID, COL_NAME1, CELL_VAL1)
    row1.commit()
    row2 = table.row(row_keys[1])
    row2.set_cell(COLUMN_FAMILY_ID, COL_NAME1, CELL_VAL1)
    row2.commit()
    # [END bigtable_table_row]

    rows_data_before_truncate = []
    for row in table.read_rows():
        rows_data_before_truncate.append(row.row_key)

    assert rows_data_before_truncate == row_keys

    # [START bigtable_truncate_table]
    table.truncate(timeout=300)
    # [END bigtable_truncate_table]

    rows_data_after_truncate = []
    for row in table.read_rows():
        rows_data_after_truncate.append(row.row_key)

    assert rows_data_after_truncate == []


def s___test_bigtable_test_iam_permissions():
    # [START bigtable_test_iam_permissions]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    instance.reload()
    permissions = ["bigtable.clusters.create", "bigtable.tables.create"]
    permissions_allowed = instance.test_iam_permissions(permissions)
    # [END bigtable_test_iam_permissions]

    assert permissions_allowed == permissions


def s___test_bigtable_set_iam_policy_then_get_iam_policy():
    # [START bigtable_set_iam_policy]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable.policy import Policy
    from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

    # [END bigtable_set_iam_policy]

    service_account_email = Config.CLIENT._credentials.service_account_email

    # [START bigtable_set_iam_policy]
    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    instance.reload()
    new_policy = Policy()
    new_policy[BIGTABLE_ADMIN_ROLE] = [
        Policy.service_account(service_account_email),
    ]

    policy_latest = instance.set_iam_policy(new_policy)
    # [END bigtable_set_iam_policy]

    assert len(policy_latest.bigtable_admins) is not 0

    # [START bigtable_get_iam_policy]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    policy = instance.get_iam_policy()
    # [END bigtable_get_iam_policy]

    assert len(policy.bigtable_admins) is not 0


if __name__ == '__main__':
    pytest.main()
