#!/usr/bin/env python

# Copyright 2026 Google LLC
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

"""Demonstrates how to connect to Cloud Bigtable and run some basic operations with the sync data APIs

Prerequisites:

- Create a Cloud Bigtable instance.
  https://cloud.google.com/bigtable/docs/creating-instance
- Set your Google Application Default Credentials.
  https://developers.google.com/identity/protocols/application-default-credentials
"""

import argparse

# [START bigtable_hw_imports_data_client]
from google.cloud import bigtable
from google.cloud.bigtable.data import row_filters

from ..utils import wait_for_table

# [END bigtable_hw_imports_data_client]

# use to ignore warnings
row_filters


def main(project_id, instance_id, table_id):
    # [START bigtable_hw_connect_data_client]
    client = bigtable.data.BigtableDataClient(project=project_id)
    table = client.get_table(instance_id, table_id)
    # [END bigtable_hw_connect_data_client]

    # [START bigtable_hw_create_table_data_client]
    from google.cloud.bigtable import column_family

    # the data client only supports the data API. Table creation is an admin operation
    # use admin client to create the table
    print("Creating the {} table.".format(table_id))
    admin_client = bigtable.Client(project=project_id, admin=True)
    admin_instance = admin_client.instance(instance_id)
    admin_table = admin_instance.table(table_id)

    print("Creating column family cf1 with Max Version GC rule...")
    # Create a column family with GC policy : most recent N versions
    # Define the GC policy to retain only the most recent 2 versions
    max_versions_rule = column_family.MaxVersionsGCRule(2)
    column_family_id = b"cf1"
    column_families = {column_family_id: max_versions_rule}
    if not admin_table.exists():
        admin_table.create(column_families=column_families)
    else:
        print("Table {} already exists.".format(table_id))
    # [END bigtable_hw_create_table_data_client]

    try:
        # let table creation complete
        wait_for_table(admin_table)
        # [START bigtable_hw_write_rows_data_client]
        print("Writing some greetings to the table.")
        greetings = [b"Hello World!", b"Hello Cloud Bigtable!", b"Hello Python!"]
        mutations = []
        column = b"greeting"
        for i, value in enumerate(greetings):
            row_key = f"greeting{i}".encode()
            row_mutation = bigtable.data.RowMutationEntry(
                row_key, bigtable.data.SetCell(column_family_id, column, value)
            )
            mutations.append(row_mutation)
        table.bulk_mutate_rows(mutations)
        # [END bigtable_hw_write_rows_data_client]

        # [START bigtable_hw_create_filter_data_client]
        # Create a filter to only retrieve the most recent version of the cell
        # for each column across entire row.
        row_filter = bigtable.data.row_filters.CellsColumnLimitFilter(1)
        # [END bigtable_hw_create_filter_data_client]

        # [START bigtable_hw_get_with_filter_data_client]
        # [START bigtable_hw_get_by_key_data_client]
        print("Getting a single greeting by row key.")
        key = "greeting0".encode()

        row = table.read_row(key, row_filter=row_filter)
        cell = row.cells[0]
        print(cell.value.decode("utf-8"))
        # [END bigtable_hw_get_by_key_data_client]
        # [END bigtable_hw_get_with_filter_data_client]

        # [START bigtable_hw_scan_with_filter_data_client]
        # [START bigtable_hw_scan_all_data_client]
        print("Scanning for all greetings:")
        query = bigtable.data.ReadRowsQuery(row_filter=row_filter)
        for row in table.read_rows(query):
            cell = row.cells[0]
            print(cell.value.decode("utf-8"))
        # [END bigtable_hw_scan_all_data_client]
        # [END bigtable_hw_scan_with_filter_data_client]
    finally:
        # [START bigtable_hw_delete_table_data_client]
        print("Deleting the {} table.".format(table_id))
        admin_table.delete()
        client.close()
        # [END bigtable_hw_delete_table_data_client]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("project_id", help="Your Cloud Platform project ID.")
    parser.add_argument(
        "instance_id", help="ID of the Cloud Bigtable instance to connect to."
    )
    parser.add_argument(
        "--table", help="Table to create and destroy.", default="Hello-Bigtable"
    )

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table)
