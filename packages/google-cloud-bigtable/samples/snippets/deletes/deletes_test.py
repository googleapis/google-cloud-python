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

from google.cloud import bigtable
import pytest

import deletes_snippets

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BIGTABLE_INSTANCE = os.environ["BIGTABLE_INSTANCE"]
TABLE_ID_PREFIX = "mobile-time-series-{}"


@pytest.fixture(scope="module", autouse=True)
def table_id():
    from google.cloud.bigtable.row_set import RowSet

    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)

    table_id = TABLE_ID_PREFIX.format(str(uuid.uuid4())[:16])
    table = instance.table(table_id)
    if table.exists():
        table.delete()

    table.create(column_families={"stats_summary": None, "cell_plan": None})

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

    yield table_id


def assert_snapshot_match(capsys, snapshot):
    out, _ = capsys.readouterr()
    snapshot.assert_match(out)


def test_delete_from_column(capsys, snapshot, table_id):
    deletes_snippets.delete_from_column(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_delete_from_column_family(capsys, snapshot, table_id):
    deletes_snippets.delete_from_column_family(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_delete_from_row(capsys, snapshot, table_id):
    deletes_snippets.delete_from_row(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_streaming_and_batching(capsys, snapshot, table_id):
    deletes_snippets.streaming_and_batching(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_check_and_mutate(capsys, snapshot, table_id):
    deletes_snippets.check_and_mutate(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_drop_row_range(capsys, snapshot, table_id):
    deletes_snippets.drop_row_range(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_delete_column_family(capsys, snapshot, table_id):
    deletes_snippets.delete_column_family(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)


def test_delete_table(capsys, snapshot, table_id):
    deletes_snippets.delete_table(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_snapshot_match(capsys, snapshot)
