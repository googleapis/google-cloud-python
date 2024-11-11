# Copyright 2020, Google LLC

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


import datetime
import os
import time
import uuid

import pytest

from . import deletes_snippets
from ...utils import create_table_cm

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BIGTABLE_INSTANCE = os.environ["BIGTABLE_INSTANCE"]
TABLE_ID = f"mobile-time-series-deletes-{str(uuid.uuid4())[:16]}"


@pytest.fixture(scope="module")
def table_id():
    from google.cloud.bigtable.row_set import RowSet

    with create_table_cm(PROJECT, BIGTABLE_INSTANCE, TABLE_ID, {"stats_summary": None, "cell_plan": None}, verbose=False) as table:
        timestamp = datetime.datetime(2019, 5, 1)
        timestamp_minus_hr = datetime.datetime(2019, 5, 1) - datetime.timedelta(hours=1)

        row_keys = [
            "phone#4c410523#20190501",
            "phone#4c410523#20190502",
            "phone#4c410523#20190505",
            "phone#5c10102#20190501",
            "phone#5c10102#20190502",
        ]

        rows = [table.direct_row(row_key) for row_key in row_keys]

        rows[0].set_cell("stats_summary", "connected_cell", 1, timestamp)
        rows[0].set_cell("stats_summary", "connected_wifi", 1, timestamp)
        rows[0].set_cell("stats_summary", "os_build", "PQ2A.190405.003", timestamp)
        rows[0].set_cell("cell_plan", "data_plan_01gb", "true", timestamp_minus_hr)
        rows[0].set_cell("cell_plan", "data_plan_01gb", "false", timestamp)
        rows[0].set_cell("cell_plan", "data_plan_05gb", "true", timestamp)
        rows[1].set_cell("stats_summary", "connected_cell", 1, timestamp)
        rows[1].set_cell("stats_summary", "connected_wifi", 1, timestamp)
        rows[1].set_cell("stats_summary", "os_build", "PQ2A.190405.004", timestamp)
        rows[1].set_cell("cell_plan", "data_plan_05gb", "true", timestamp)
        rows[2].set_cell("stats_summary", "connected_cell", 0, timestamp)
        rows[2].set_cell("stats_summary", "connected_wifi", 1, timestamp)
        rows[2].set_cell("stats_summary", "os_build", "PQ2A.190406.000", timestamp)
        rows[2].set_cell("cell_plan", "data_plan_05gb", "true", timestamp)
        rows[3].set_cell("stats_summary", "connected_cell", 1, timestamp)
        rows[3].set_cell("stats_summary", "connected_wifi", 1, timestamp)
        rows[3].set_cell("stats_summary", "os_build", "PQ2A.190401.002", timestamp)
        rows[3].set_cell("cell_plan", "data_plan_10gb", "true", timestamp)
        rows[4].set_cell("stats_summary", "connected_cell", 1, timestamp)
        rows[4].set_cell("stats_summary", "connected_wifi", 0, timestamp)
        rows[4].set_cell("stats_summary", "os_build", "PQ2A.190406.000", timestamp)
        rows[4].set_cell("cell_plan", "data_plan_10gb", "true", timestamp)

        table.mutate_rows(rows)

        # Ensure mutations have propagated.
        row_set = RowSet()

        for row_key in row_keys:
            row_set.add_row_key(row_key)

        fetched = list(table.read_rows(row_set=row_set))

        while len(fetched) < len(rows):
            time.sleep(5)
            fetched = list(table.read_rows(row_set=row_set))

        yield TABLE_ID


def assert_output_match(capsys, expected):
    out, _ = capsys.readouterr()
    assert out == expected


def test_delete_from_column(capsys, table_id):
    deletes_snippets.delete_from_column(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_delete_from_column_family(capsys, table_id):
    deletes_snippets.delete_from_column_family(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_delete_from_row(capsys, table_id):
    deletes_snippets.delete_from_row(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_streaming_and_batching(capsys, table_id):
    deletes_snippets.streaming_and_batching(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_check_and_mutate(capsys, table_id):
    deletes_snippets.check_and_mutate(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_drop_row_range(capsys, table_id):
    deletes_snippets.drop_row_range(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_delete_column_family(capsys, table_id):
    deletes_snippets.delete_column_family(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


def test_delete_table(capsys):
    delete_table_id = f"to-delete-table-{str(uuid.uuid4())[:16]}"
    with create_table_cm(PROJECT, BIGTABLE_INSTANCE, delete_table_id, verbose=False):
        deletes_snippets.delete_table(PROJECT, BIGTABLE_INSTANCE, delete_table_id)
        assert_output_match(capsys, "")
