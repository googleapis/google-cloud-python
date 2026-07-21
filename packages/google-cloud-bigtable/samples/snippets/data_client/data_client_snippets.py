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


# ==============================================================================
# Writes & Mutate Operations
# ==============================================================================


def write_simple(table):
    # [START bigtable_write_simple]
    from google.cloud.bigtable.data import BigtableDataClient, SetCell

    def write_simple(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                family_id = "stats_summary"
                row_key = b"phone#4c410523#20190501"

                cell_mutation = SetCell(family_id, "connected_cell", 1)
                wifi_mutation = SetCell(family_id, "connected_wifi", 1)
                os_mutation = SetCell(family_id, "os_build", "PQ2A.190405.003")

                table.mutate_row(row_key, cell_mutation)
                table.mutate_row(row_key, wifi_mutation)
                table.mutate_row(row_key, os_mutation)

    # [END bigtable_write_simple]
    write_simple(table.client.project, table.instance_id, table.table_id)


def write_batch(table):
    # [START bigtable_writes_batch]
    from google.cloud.bigtable.data import BigtableDataClient
    from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup
    from google.cloud.bigtable.data.mutations import RowMutationEntry, SetCell

    def write_batch(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                family_id = "stats_summary"
                try:
                    with table.mutations_batcher() as batcher:
                        mutation_list = [
                            SetCell(family_id, "connected_cell", 1),
                            SetCell(family_id, "connected_wifi", 1),
                            SetCell(family_id, "os_build", "12155.0.0-rc1"),
                        ]
                        batcher.append(
                            RowMutationEntry("tablet#a0b81f74#20190501", mutation_list)
                        )
                        batcher.append(
                            RowMutationEntry("tablet#a0b81f74#20190502", mutation_list)
                        )
                except MutationsExceptionGroup as e:
                    for sub_exception in e.exceptions:
                        failed_entry: RowMutationEntry = sub_exception.entry
                        cause: Exception = sub_exception.__cause__
                        print(
                            f"Failed mutation: {failed_entry.row_key} with error: {cause!r}"
                        )

    # [END bigtable_writes_batch]
    write_batch(table.client.project, table.instance_id, table.table_id)


def write_increment(table):
    # [START bigtable_write_increment]
    from google.cloud.bigtable.data import BigtableDataClient
    from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

    def write_increment(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                family_id = "stats_summary"
                row_key = "phone#4c410523#20190501"

                # Decrement the connected_wifi value by 1.
                increment_rule = IncrementRule(
                    family_id, "connected_wifi", increment_amount=-1
                )
                result_row = table.read_modify_write_row(row_key, increment_rule)

                # check result
                cell = result_row[0]
                print(f"{cell.row_key} value: {int(cell)}")

    # [END bigtable_write_increment]
    write_increment(table.client.project, table.instance_id, table.table_id)


def write_conditional(table):
    # [START bigtable_writes_conditional]
    from google.cloud.bigtable.data import BigtableDataClient, SetCell, row_filters

    def write_conditional(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                family_id = "stats_summary"
                row_key = "phone#4c410523#20190501"

                row_filter = row_filters.RowFilterChain(
                    filters=[
                        row_filters.FamilyNameRegexFilter(family_id),
                        row_filters.ColumnQualifierRegexFilter("os_build"),
                        row_filters.ValueRegexFilter("PQ2A\\..*"),
                    ]
                )

                if_true = SetCell(family_id, "os_name", "android")
                result = table.check_and_mutate_row(
                    row_key,
                    row_filter,
                    true_case_mutations=if_true,
                    false_case_mutations=None,
                )
                if result is True:
                    print("The row os_name was set to android")

    # [END bigtable_writes_conditional]
    write_conditional(table.client.project, table.instance_id, table.table_id)


def write_aggregate(table):
    # [START bigtable_write_aggregate]
    import time

    from google.cloud.bigtable.data import BigtableDataClient
    from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup
    from google.cloud.bigtable.data.mutations import AddToCell, RowMutationEntry

    def write_aggregate(project_id, instance_id, table_id):
        """Increments a value in a Bigtable table using AddToCell mutation."""
        with BigtableDataClient(project=project_id) as client:
            table = client.get_table(instance_id, table_id)
            row_key = "unique_device_ids_1"
            try:
                with table.mutations_batcher() as batcher:
                    reading = AddToCell(
                        family="counters",
                        qualifier="odometer",
                        value=32304,
                        timestamp_micros=time.time_ns() // 1000,
                    )
                    batcher.append(
                        RowMutationEntry(row_key.encode("utf-8"), [reading])
                    )
            except MutationsExceptionGroup as e:
                for sub_exception in e.exceptions:
                    failed_entry: RowMutationEntry = sub_exception.entry
                    cause: Exception = sub_exception.__cause__
                    print(
                        f"Failed mutation for row {failed_entry.row_key!r} with error: {cause!r}"
                    )

    # [END bigtable_write_aggregate]
    write_aggregate(table.client.project, table.instance_id, table.table_id)


# ==============================================================================
# Deletes
# ==============================================================================


def delete_from_column(table):
    # [START bigtable_delete_from_column]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        DeleteRangeFromColumn,
    )

    def delete_from_column(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                table.mutate_row(
                    "phone#4c410523#20190501",
                    DeleteRangeFromColumn(
                        family="stats_summary", qualifier=b"connected_wifi"
                    ),
                )

    # [END bigtable_delete_from_column]
    delete_from_column(table.client.project, table.instance_id, table.table_id)


def delete_from_column_family(table):
    # [START bigtable_delete_from_column_family]
    from google.cloud.bigtable.data import BigtableDataClient, DeleteAllFromFamily

    def delete_from_column_family(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                table.mutate_row(
                    "phone#4c410523#20190501", DeleteAllFromFamily("stats_summary")
                )

    # [END bigtable_delete_from_column_family]
    delete_from_column_family(table.client.project, table.instance_id, table.table_id)


def delete_from_row(table):
    # [START bigtable_delete_from_row]
    from google.cloud.bigtable.data import BigtableDataClient, DeleteAllFromRow

    def delete_from_row(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                table.mutate_row("phone#4c410523#20190501", DeleteAllFromRow())

    # [END bigtable_delete_from_row]
    delete_from_row(table.client.project, table.instance_id, table.table_id)


def streaming_and_batching(table):
    # [START bigtable_streaming_and_batching]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        DeleteRangeFromColumn,
        ReadRowsQuery,
        RowMutationEntry,
    )

    def streaming_and_batching(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                with table.mutations_batcher() as batcher:
                    for row in table.read_rows_stream(ReadRowsQuery(limit=10)):
                        batcher.append(
                            RowMutationEntry(
                                row.row_key,
                                DeleteRangeFromColumn(
                                    family="stats_summary", qualifier=b"connected_cell"
                                ),
                            )
                        )

    # [END bigtable_streaming_and_batching]
    streaming_and_batching(table.client.project, table.instance_id, table.table_id)


def check_and_mutate(table):
    # [START bigtable_check_and_mutate]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        DeleteRangeFromColumn,
    )
    from google.cloud.bigtable.data.row_filters import LiteralValueFilter

    def check_and_mutate(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                table.check_and_mutate_row(
                    "phone#4c410523#20190501",
                    predicate=LiteralValueFilter("PQ2A.190405.003"),
                    true_case_mutations=DeleteRangeFromColumn(
                        family="stats_summary", qualifier=b"connected_cell"
                    ),
                )

    # [END bigtable_check_and_mutate]
    check_and_mutate(table.client.project, table.instance_id, table.table_id)


# ==============================================================================
# Reads & Queries
# ==============================================================================


def read_row(table):
    # [START bigtable_reads_row]
    from google.cloud.bigtable.data import BigtableDataClient

    def read_row(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                row_key = "phone#4c410523#20190501"
                row = table.read_row(row_key)
                print(row)

    # [END bigtable_reads_row]
    read_row(table.client.project, table.instance_id, table.table_id)


def read_row_partial(table):
    # [START bigtable_reads_row_partial]
    from google.cloud.bigtable.data import BigtableDataClient, row_filters

    def read_row_partial(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                row_key = "phone#4c410523#20190501"
                col_filter = row_filters.ColumnQualifierRegexFilter(b"os_build")

                row = table.read_row(row_key, row_filter=col_filter)
                print(row)

    # [END bigtable_reads_row_partial]
    read_row_partial(table.client.project, table.instance_id, table.table_id)


def read_rows_multiple(table):
    # [START bigtable_reads_rows]
    from google.cloud.bigtable.data import BigtableDataClient, ReadRowsQuery

    def read_rows(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                query = ReadRowsQuery(
                    row_keys=[b"phone#4c410523#20190501", b"phone#4c410523#20190502"]
                )
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_reads_rows]
    read_rows(table.client.project, table.instance_id, table.table_id)


def read_row_range(table):
    # [START bigtable_reads_row_range]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        RowRange,
    )

    def read_row_range(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                row_range = RowRange(
                    start_key=b"phone#4c410523#20190501",
                    end_key=b"phone#4c410523#201906201",
                )
                query = ReadRowsQuery(row_ranges=[row_range])

                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_reads_row_range]
    read_row_range(table.client.project, table.instance_id, table.table_id)


def read_row_ranges(table):
    # [START bigtable_reads_row_ranges]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        RowRange,
    )

    def read_row_ranges(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                range_1 = RowRange(
                    start_key=b"phone#4c410523#20190501",
                    end_key=b"phone#4c410523#201906201",
                )
                range_2 = RowRange(
                    start_key=b"phone#5c10102#20190501",
                    end_key=b"phone#5c10102#201906201",
                )
                query = ReadRowsQuery(row_ranges=[range_1, range_2])

                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_reads_row_ranges]
    read_row_ranges(table.client.project, table.instance_id, table.table_id)


def read_with_prefix(table):
    # [START bigtable_reads_prefix]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        RowRange,
    )

    def read_prefix(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                prefix = "phone#"
                end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)
                prefix_range = RowRange(start_key=prefix, end_key=end_key)
                query = ReadRowsQuery(row_ranges=[prefix_range])

                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_reads_prefix]
    read_prefix(table.client.project, table.instance_id, table.table_id)


def read_with_filter(table):
    # [START bigtable_reads_filter]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def read_with_filter(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                row_filter = row_filters.ValueRegexFilter(b"PQ2A.*$")
                query = ReadRowsQuery(row_filter=row_filter)

                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_reads_filter]
    read_with_filter(table.client.project, table.instance_id, table.table_id)


def execute_query(table):
    # [START bigtable_execute_query]
    from google.cloud.bigtable.data import BigtableDataClient

    def execute_query(project_id, instance_id, table_id):
        with BigtableDataClient(project=project_id) as client:
            query = (
                "SELECT _key, stats_summary['os_build'], "
                "stats_summary['connected_cell'], "
                "stats_summary['connected_wifi'] "
                f"from `{table_id}` WHERE _key=@row_key"
            )
            result = client.execute_query(
                query,
                instance_id,
                parameters={"row_key": b"phone#4c410523#20190501"},
            )
            results = [r for r in result]
            print(results)

    # [END bigtable_execute_query]
    execute_query(table.client.project, table.instance_id, table.table_id)


# ==============================================================================
# Filters
# ==============================================================================


def filter_limit_row_sample(table):
    # [START bigtable_filters_limit_row_sample]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_row_sample(project_id, instance_id, table_id):
        query = ReadRowsQuery(row_filter=row_filters.RowSampleFilter(0.75))

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_row_sample]
    filter_limit_row_sample(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_row_regex(table):
    # [START bigtable_filters_limit_row_regex]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_row_regex(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.RowKeyRegexFilter(".*#20190501$".encode("utf-8"))
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_row_regex]
    filter_limit_row_regex(table.client.project, table.instance_id, table.table_id)


def filter_limit_cells_per_col(table):
    # [START bigtable_filters_limit_cells_per_col]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_cells_per_col(project_id, instance_id, table_id):
        query = ReadRowsQuery(row_filter=row_filters.CellsColumnLimitFilter(2))

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_cells_per_col]
    filter_limit_cells_per_col(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_cells_per_row(table):
    # [START bigtable_filters_limit_cells_per_row]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_cells_per_row(project_id, instance_id, table_id):
        query = ReadRowsQuery(row_filter=row_filters.CellsRowLimitFilter(2))

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_cells_per_row]
    filter_limit_cells_per_row(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_cells_per_row_offset(table):
    # [START bigtable_filters_limit_cells_per_row_offset]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_cells_per_row_offset(project_id, instance_id, table_id):
        query = ReadRowsQuery(row_filter=row_filters.CellsRowOffsetFilter(2))

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_cells_per_row_offset]
    filter_limit_cells_per_row_offset(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_col_family_regex(table):
    # [START bigtable_filters_limit_col_family_regex]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_col_family_regex(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.FamilyNameRegexFilter("stats_.*$".encode("utf-8"))
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_col_family_regex]
    filter_limit_col_family_regex(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_col_qualifier_regex(table):
    # [START bigtable_filters_limit_col_qualifier_regex]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_col_qualifier_regex(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.ColumnQualifierRegexFilter(
                "connected_.*$".encode("utf-8")
            )
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_col_qualifier_regex]
    filter_limit_col_qualifier_regex(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_col_range(table):
    # [START bigtable_filters_limit_col_range]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_col_range(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.ColumnRangeFilter(
                "stats_summary", b"connected_cell", b"connected_wifi", inclusive_end=True
            )
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_col_range]
    filter_limit_col_range(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_value_range(table):
    # [START bigtable_filters_limit_value_range]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_value_range(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.ValueRangeFilter(b"PQ2A.190405", b"PQ2A.190406")
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_value_range]
    filter_limit_value_range(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_value_regex(table):
    # [START bigtable_filters_limit_value_regex]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_value_regex(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.ValueRegexFilter("PQ2A.*$".encode("utf-8"))
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_value_regex]
    filter_limit_value_regex(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_timestamp_range(table):
    # [START bigtable_filters_limit_timestamp_range]
    import datetime

    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_timestamp_range(project_id, instance_id, table_id):
        end = datetime.datetime(2019, 5, 1)
        query = ReadRowsQuery(
            row_filter=row_filters.TimestampRangeFilter(
                row_filters.TimestampRange(end=end)
            )
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_timestamp_range]
    filter_limit_timestamp_range(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_block_all(table):
    # [START bigtable_filters_limit_block_all]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_block_all(project_id, instance_id, table_id):
        query = ReadRowsQuery(row_filter=row_filters.BlockAllFilter(True))

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_block_all]
    filter_limit_block_all(
        table.client.project, table.instance_id, table.table_id
    )


def filter_limit_pass_all(table):
    # [START bigtable_filters_limit_pass_all]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_limit_pass_all(project_id, instance_id, table_id):
        query = ReadRowsQuery(row_filter=row_filters.PassAllFilter(True))

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_limit_pass_all]
    filter_limit_pass_all(
        table.client.project, table.instance_id, table.table_id
    )


def filter_modify_strip_value(table):
    # [START bigtable_filters_modify_strip_value]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_modify_strip_value(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.StripValueTransformerFilter(True)
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_modify_strip_value]
    filter_modify_strip_value(
        table.client.project, table.instance_id, table.table_id
    )


def filter_modify_apply_label(table):
    # [START bigtable_filters_modify_apply_label]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_modify_apply_label(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.ApplyLabelFilter(label="labelled")
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_modify_apply_label]
    filter_modify_apply_label(
        table.client.project, table.instance_id, table.table_id
    )


def filter_composing_chain(table):
    # [START bigtable_filters_composing_chain]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_composing_chain(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.RowFilterChain(
                filters=[
                    row_filters.CellsColumnLimitFilter(1),
                    row_filters.FamilyNameRegexFilter("stats_summary"),
                ]
            )
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_composing_chain]
    filter_composing_chain(
        table.client.project, table.instance_id, table.table_id
    )


def filter_composing_interleave(table):
    # [START bigtable_filters_composing_interleave]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_composing_interleave(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.RowFilterUnion(
                filters=[
                    row_filters.ValueRegexFilter("1"),
                    row_filters.ColumnQualifierRegexFilter("os_build"),
                ]
            )
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_composing_interleave]
    filter_composing_interleave(
        table.client.project, table.instance_id, table.table_id
    )


def filter_composing_condition(table):
    # [START bigtable_filters_composing_condition]
    from google.cloud.bigtable.data import (
        BigtableDataClient,
        ReadRowsQuery,
        row_filters,
    )

    def filter_composing_condition(project_id, instance_id, table_id):
        query = ReadRowsQuery(
            row_filter=row_filters.ConditionalRowFilter(
                base_filter=row_filters.RowFilterChain(
                    filters=[
                        row_filters.ColumnQualifierRegexFilter("connected_wifi"),
                        row_filters.ValueRegexFilter("1"),
                    ]
                ),
                true_filter=row_filters.ApplyLabelFilter(label="passed-filter"),
                false_filter=row_filters.ApplyLabelFilter(label="filtered-out"),
            )
        )

        with BigtableDataClient(project=project_id) as client:
            with client.get_table(instance_id, table_id) as table:
                for row in table.read_rows_stream(query):
                    print(row)

    # [END bigtable_filters_composing_condition]
    filter_composing_condition(
        table.client.project, table.instance_id, table.table_id
    )
