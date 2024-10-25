#!/usr/bin/env python

# Copyright 2022, Google LLC
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


# [START bigtable_delete_from_column]
def delete_from_column(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    row = table.row("phone#4c410523#20190501")
    row.delete_cell(column_family_id="cell_plan", column="data_plan_01gb")
    row.commit()


# [END bigtable_delete_from_column]

# [START bigtable_delete_from_column_family]
def delete_from_column_family(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    row = table.row("phone#4c410523#20190501")
    row.delete_cells(column_family_id="cell_plan", columns=row.ALL_COLUMNS)
    row.commit()


# [END bigtable_delete_from_column_family]


# [START bigtable_delete_from_row]
def delete_from_row(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    row = table.row("phone#4c410523#20190501")
    row.delete()
    row.commit()


# [END bigtable_delete_from_row]

# [START bigtable_streaming_and_batching]
def streaming_and_batching(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    batcher = table.mutations_batcher(flush_count=2)
    rows = table.read_rows()
    for row in rows:
        row = table.row(row.row_key)
        row.delete_cell(column_family_id="cell_plan", column="data_plan_01gb")

    batcher.mutate_rows(rows)


# [END bigtable_streaming_and_batching]

# [START bigtable_check_and_mutate]
def check_and_mutate(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    row = table.row("phone#4c410523#20190501")
    row.delete_cell(column_family_id="cell_plan", column="data_plan_01gb")
    row.delete_cell(column_family_id="cell_plan", column="data_plan_05gb")
    row.commit()


# [END bigtable_check_and_mutate]


# [START bigtable_drop_row_range]
def drop_row_range(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    row_key_prefix = "phone#4c410523"
    table.drop_by_prefix(row_key_prefix, timeout=200)


# [END bigtable_drop_row_range]

# [START bigtable_delete_column_family]
def delete_column_family(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    column_family_id = "stats_summary"
    column_family_obj = table.column_family(column_family_id)
    column_family_obj.delete()


# [END bigtable_delete_column_family]

# [START bigtable_delete_table]
def delete_table(project_id, instance_id, table_id):
    from google.cloud.bigtable import Client

    client = Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    table.delete()


# [END bigtable_delete_table]
