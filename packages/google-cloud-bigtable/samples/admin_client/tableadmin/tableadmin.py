#!/usr/bin/env python

# Copyright 2024, Google LLC
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

"""Demonstrates how to connect to Cloud Bigtable and run table admin operations using BigtableTableAdminClient.

Prerequisites:
- Create a Cloud Bigtable instance.
- Set your Google Application Default Credentials.
"""

import argparse
import datetime

from google.cloud import bigtable_admin_v2
from google.protobuf import duration_pb2

from ..utils import create_table_cm


def run_table_operations(project_id, instance_id, table_id):
    client = bigtable_admin_v2.BigtableTableAdminClient()
    instance_path = client.instance_path(project_id, instance_id)
    table_path = client.table_path(project_id, instance_id, table_id)

    with create_table_cm(project_id, instance_id, table_id, verbose=False):
        # [START bigtable_list_tables]
        tables = client.list_tables(parent=instance_path)
        print("Listing tables in current project...")
        if tables.tables:
            for tbl in tables.tables:
                print(tbl.name.split("/")[-1])
        else:
            print("No table exists in current project...")
        # [END bigtable_list_tables]

        # [START bigtable_create_family_gc_max_age]
        print("Creating column family cf1 with MaxAge GC Rule...")
        max_age_rule = bigtable_admin_v2.GcRule(
            max_age=duration_pb2.Duration(seconds=5 * 86400)
        )
        cf1 = bigtable_admin_v2.ColumnFamily(gc_rule=max_age_rule)
        mod1 = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf1", create=cf1
        )
        client.modify_column_families(name=table_path, modifications=[mod1])
        print("Created column family cf1 with MaxAge GC Rule.")
        # [END bigtable_create_family_gc_max_age]

        # [START bigtable_create_family_gc_max_versions]
        print("Creating column family cf2 with max versions GC rule...")
        max_versions_rule = bigtable_admin_v2.GcRule(max_num_versions=2)
        cf2 = bigtable_admin_v2.ColumnFamily(gc_rule=max_versions_rule)
        mod2 = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf2", create=cf2
        )
        client.modify_column_families(name=table_path, modifications=[mod2])
        print("Created column family cf2 with Max Versions GC Rule.")
        # [END bigtable_create_family_gc_max_versions]

        # [START bigtable_create_family_gc_union]
        print("Creating column family cf3 with union GC rule...")
        union_rule = bigtable_admin_v2.GcRule(
            union=bigtable_admin_v2.GcRule.Union(
                rules=[
                    bigtable_admin_v2.GcRule(
                        max_age=duration_pb2.Duration(seconds=5 * 86400)
                    ),
                    bigtable_admin_v2.GcRule(max_num_versions=2),
                ]
            )
        )
        cf3 = bigtable_admin_v2.ColumnFamily(gc_rule=union_rule)
        mod3 = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf3", create=cf3
        )
        client.modify_column_families(name=table_path, modifications=[mod3])
        print("Created column family cf3 with Union GC rule")
        # [END bigtable_create_family_gc_union]

        # [START bigtable_create_family_gc_intersection]
        print("Creating column family cf4 with Intersection GC rule...")
        intersection_rule = bigtable_admin_v2.GcRule(
            intersection=bigtable_admin_v2.GcRule.Intersection(
                rules=[
                    bigtable_admin_v2.GcRule(
                        max_age=duration_pb2.Duration(seconds=5 * 86400)
                    ),
                    bigtable_admin_v2.GcRule(max_num_versions=2),
                ]
            )
        )
        cf4 = bigtable_admin_v2.ColumnFamily(gc_rule=intersection_rule)
        mod4 = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf4", create=cf4
        )
        client.modify_column_families(name=table_path, modifications=[mod4])
        print("Created column family cf4 with Intersection GC rule.")
        # [END bigtable_create_family_gc_intersection]

        # [START bigtable_create_family_gc_nested]
        print("Creating column family cf5 with a Nested GC rule...")
        rule1 = bigtable_admin_v2.GcRule(max_num_versions=10)
        rule2 = bigtable_admin_v2.GcRule(
            intersection=bigtable_admin_v2.GcRule.Intersection(
                rules=[
                    bigtable_admin_v2.GcRule(
                        max_age=duration_pb2.Duration(seconds=30 * 86400)
                    ),
                    bigtable_admin_v2.GcRule(max_num_versions=2),
                ]
            )
        )
        nested_rule = bigtable_admin_v2.GcRule(
            union=bigtable_admin_v2.GcRule.Union(rules=[rule1, rule2])
        )
        cf5 = bigtable_admin_v2.ColumnFamily(gc_rule=nested_rule)
        mod5 = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf5", create=cf5
        )
        client.modify_column_families(name=table_path, modifications=[mod5])
        print("Created column family cf5 with a Nested GC rule.")
        # [END bigtable_create_family_gc_nested]

        # [START bigtable_list_column_families]
        print("Printing Column Family and GC Rule for all column families...")
        table_obj = client.get_table(name=table_path)
        for column_family_name, cf_obj in sorted(table_obj.column_families.items()):
            print("Column Family:", column_family_name)
            print("GC Rule:")
            print(cf_obj.gc_rule)
        # [END bigtable_list_column_families]

        # [START bigtable_update_gc_rule]
        print("Updating column family cf1 GC rule...")
        updated_cf1 = bigtable_admin_v2.ColumnFamily(
            gc_rule=bigtable_admin_v2.GcRule(max_num_versions=1)
        )
        mod_update = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf1", update=updated_cf1
        )
        client.modify_column_families(name=table_path, modifications=[mod_update])
        print("Updated column family cf1 GC rule\n")
        # [END bigtable_update_gc_rule]

        # [START bigtable_delete_family]
        print("Delete a column family cf2...")
        mod_delete = bigtable_admin_v2.ModifyColumnFamiliesRequest.Modification(
            id="cf2", drop=True
        )
        client.modify_column_families(name=table_path, modifications=[mod_delete])
        print("Column family cf2 deleted successfully.")
        # [END bigtable_delete_family]


def delete_table(project_id, instance_id, table_id):
    client = bigtable_admin_v2.BigtableTableAdminClient()
    table_path = client.table_path(project_id, instance_id, table_id)

    # [START bigtable_delete_table]
    print("Deleting {} table.".format(table_id))
    client.delete_table(name=table_path)
    print("Deleted {} table.".format(table_id))
    # [END bigtable_delete_table]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("command", help="run or delete.")
    parser.add_argument(
        "--table", help="Cloud Bigtable Table name.", default="Hello-Bigtable"
    )
    parser.add_argument("project_id", help="Your Cloud Platform project ID.")
    parser.add_argument(
        "instance_id", help="ID of the Cloud Bigtable instance to connect to."
    )

    args = parser.parse_args()

    if args.command.lower() == "run":
        run_table_operations(args.project_id, args.instance_id, args.table)
    elif args.command.lower() == "delete":
        delete_table(args.project_id, args.instance_id, args.table)
