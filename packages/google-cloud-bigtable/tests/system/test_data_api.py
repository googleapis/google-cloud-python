# Copyright 2011 Google LLC
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

import datetime
import operator

import pytest

COLUMN_FAMILY_ID1 = "col-fam-id1"
COLUMN_FAMILY_ID2 = "col-fam-id2"
COL_NAME1 = b"col-name1"
COL_NAME2 = b"col-name2"
COL_NAME3 = b"col-name3-but-other-fam"
CELL_VAL1 = b"cell-val"
CELL_VAL2 = b"cell-val-newer"
CELL_VAL3 = b"altcol-cell-val"
CELL_VAL4 = b"foo"
ROW_KEY = b"row-key"
ROW_KEY_ALT = b"row-key-alt"


@pytest.fixture(scope="module")
def data_table_id():
    return "test-data-api"


@pytest.fixture(scope="module")
def data_table(data_instance_populated, data_table_id):
    table = data_instance_populated.table(data_table_id)
    table.create()
    table.column_family(COLUMN_FAMILY_ID1).create()
    table.column_family(COLUMN_FAMILY_ID2).create()

    yield table

    table.delete()


@pytest.fixture(scope="function")
def rows_to_delete():
    rows_to_delete = []

    yield rows_to_delete

    for row in rows_to_delete:
        row.clear()
        row.delete()
        row.commit()


def test_table_read_rows_filter_millis(data_table):
    from google.cloud.bigtable import row_filters

    end = datetime.datetime.now()
    start = end - datetime.timedelta(minutes=60)
    timestamp_range = row_filters.TimestampRange(start=start, end=end)
    timefilter = row_filters.TimestampRangeFilter(timestamp_range)
    row_data = data_table.read_rows(filter_=timefilter)
    row_data.consume_all()


def test_table_mutate_rows(data_table, rows_to_delete):
    row1 = data_table.direct_row(ROW_KEY)
    row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1)
    row1.commit()
    rows_to_delete.append(row1)

    row2 = data_table.direct_row(ROW_KEY_ALT)
    row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL2)
    row2.commit()
    rows_to_delete.append(row2)

    # Change the contents
    row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL3)
    row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL4)
    rows = [row1, row2]

    statuses = data_table.mutate_rows(rows)
    assert len(statuses) == len(rows)
    for status in statuses:
        assert status.code == 0

    # Check the contents
    row1_data = data_table.read_row(ROW_KEY)
    assert row1_data.cells[COLUMN_FAMILY_ID1][COL_NAME1][0].value == CELL_VAL3

    row2_data = data_table.read_row(ROW_KEY_ALT)
    assert row2_data.cells[COLUMN_FAMILY_ID1][COL_NAME1][0].value == CELL_VAL4


def _populate_table(data_table, rows_to_delete, row_keys):
    for row_key in row_keys:
        row = data_table.direct_row(row_key)
        row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1)
        row.commit()
        rows_to_delete.append(row)


def test_table_truncate(data_table, rows_to_delete):
    row_keys = [
        b"row_key_1",
        b"row_key_2",
        b"row_key_3",
        b"row_key_4",
        b"row_key_5",
        b"row_key_pr_1",
        b"row_key_pr_2",
        b"row_key_pr_3",
        b"row_key_pr_4",
        b"row_key_pr_5",
    ]
    _populate_table(data_table, rows_to_delete, row_keys)

    data_table.truncate(timeout=200)

    assert list(data_table.read_rows()) == []


def test_table_drop_by_prefix(data_table, rows_to_delete):
    row_keys = [
        b"row_key_1",
        b"row_key_2",
        b"row_key_3",
        b"row_key_4",
        b"row_key_5",
        b"row_key_pr_1",
        b"row_key_pr_2",
        b"row_key_pr_3",
        b"row_key_pr_4",
        b"row_key_pr_5",
    ]
    _populate_table(data_table, rows_to_delete, row_keys)

    data_table.drop_by_prefix(row_key_prefix="row_key_pr", timeout=200)

    remaining_row_keys = [
        row_key for row_key in row_keys if not row_key.startswith(b"row_key_pr")
    ]
    expected_rows_count = len(remaining_row_keys)
    found_rows_count = 0

    for row in data_table.read_rows():
        if row.row_key in row_keys:
            found_rows_count += 1

    assert expected_rows_count == found_rows_count


def test_table_read_rows_w_row_set(data_table, rows_to_delete):
    from google.cloud.bigtable.row_set import RowSet
    from google.cloud.bigtable.row_set import RowRange

    row_keys = [
        b"row_key_1",
        b"row_key_2",
        b"row_key_3",
        b"row_key_4",
        b"row_key_5",
        b"row_key_6",
        b"row_key_7",
        b"row_key_8",
        b"row_key_9",
    ]
    _populate_table(data_table, rows_to_delete, row_keys)

    row_range = RowRange(start_key=b"row_key_3", end_key=b"row_key_7")
    row_set = RowSet()
    row_set.add_row_range(row_range)
    row_set.add_row_key(b"row_key_1")

    found_rows = data_table.read_rows(row_set=row_set)

    found_row_keys = [row.row_key for row in found_rows]
    expected_row_keys = [
        row_key for row_key in row_keys[:6] if not row_key.endswith(b"_2")
    ]
    assert found_row_keys == expected_row_keys


def test_rowset_add_row_range_w_pfx(data_table, rows_to_delete):
    from google.cloud.bigtable.row_set import RowSet

    row_keys = [
        b"row_key_1",
        b"row_key_2",
        b"row_key_3",
        b"row_key_4",
        b"sample_row_key_1",
        b"sample_row_key_2",
    ]
    _populate_table(data_table, rows_to_delete, row_keys)

    row_set = RowSet()
    row_set.add_row_range_with_prefix("row")

    expected_row_keys = [row_key for row_key in row_keys if row_key.startswith(b"row")]
    found_rows = data_table.read_rows(row_set=row_set)
    found_row_keys = [row.row_key for row in found_rows]
    assert found_row_keys == expected_row_keys


def test_table_read_row_large_cell(data_table, rows_to_delete, skip_on_emulator):
    # Maximum gRPC received message size for emulator is 4194304 bytes.
    row = data_table.direct_row(ROW_KEY)
    rows_to_delete.append(row)

    number_of_bytes = 10 * 1024 * 1024
    data = b"1" * number_of_bytes  # 10MB of 1's.
    row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, data)
    row.commit()

    # Read back the contents of the row.
    row_data = data_table.read_row(ROW_KEY)
    assert row_data.row_key == ROW_KEY

    cell = row_data.cells[COLUMN_FAMILY_ID1]
    column = cell[COL_NAME1]
    assert len(column) == 1
    assert column[0].value == data


def _write_to_row(row1, row2, row3, row4):
    from google.cloud._helpers import _datetime_from_microseconds
    from google.cloud._helpers import _microseconds_from_datetime
    from google.cloud._helpers import UTC
    from google.cloud.bigtable.row_data import Cell

    timestamp1 = datetime.datetime.utcnow().replace(tzinfo=UTC)
    timestamp1_micros = _microseconds_from_datetime(timestamp1)
    # Truncate to millisecond granularity.
    timestamp1_micros -= timestamp1_micros % 1000
    timestamp1 = _datetime_from_microseconds(timestamp1_micros)
    # 1000 microseconds is a millisecond
    timestamp2 = timestamp1 + datetime.timedelta(microseconds=1000)
    timestamp2_micros = _microseconds_from_datetime(timestamp2)
    timestamp3 = timestamp1 + datetime.timedelta(microseconds=2000)
    timestamp3_micros = _microseconds_from_datetime(timestamp3)
    timestamp4 = timestamp1 + datetime.timedelta(microseconds=3000)
    timestamp4_micros = _microseconds_from_datetime(timestamp4)

    if row1 is not None:
        row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1, timestamp=timestamp1)
    if row2 is not None:
        row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL2, timestamp=timestamp2)
    if row3 is not None:
        row3.set_cell(COLUMN_FAMILY_ID1, COL_NAME2, CELL_VAL3, timestamp=timestamp3)
    if row4 is not None:
        row4.set_cell(COLUMN_FAMILY_ID2, COL_NAME3, CELL_VAL4, timestamp=timestamp4)

    # Create the cells we will check.
    cell1 = Cell(CELL_VAL1, timestamp1_micros)
    cell2 = Cell(CELL_VAL2, timestamp2_micros)
    cell3 = Cell(CELL_VAL3, timestamp3_micros)
    cell4 = Cell(CELL_VAL4, timestamp4_micros)

    return cell1, cell2, cell3, cell4


def test_table_read_row(data_table, rows_to_delete):
    row = data_table.direct_row(ROW_KEY)
    rows_to_delete.append(row)
    cell1, cell2, cell3, cell4 = _write_to_row(row, row, row, row)
    row.commit()

    partial_row_data = data_table.read_row(ROW_KEY)

    assert partial_row_data.row_key == ROW_KEY

    # Check the cells match.
    ts_attr = operator.attrgetter("timestamp")
    expected_row_contents = {
        COLUMN_FAMILY_ID1: {
            COL_NAME1: sorted([cell1, cell2], key=ts_attr, reverse=True),
            COL_NAME2: [cell3],
        },
        COLUMN_FAMILY_ID2: {COL_NAME3: [cell4]},
    }
    assert partial_row_data.cells == expected_row_contents


def test_table_read_rows(data_table, rows_to_delete):
    from google.cloud.bigtable.row_data import PartialRowData

    row = data_table.direct_row(ROW_KEY)
    rows_to_delete.append(row)
    row_alt = data_table.direct_row(ROW_KEY_ALT)
    rows_to_delete.append(row_alt)

    cell1, cell2, cell3, cell4 = _write_to_row(row, row_alt, row, row_alt)
    row.commit()
    row_alt.commit()

    rows_data = data_table.read_rows()
    assert rows_data.rows == {}
    rows_data.consume_all()

    # NOTE: We should refrain from editing protected data on instances.
    #       Instead we should make the values public or provide factories
    #       for constructing objects with them.
    row_data = PartialRowData(ROW_KEY)
    row_data._chunks_encountered = True
    row_data._committed = True
    row_data._cells = {COLUMN_FAMILY_ID1: {COL_NAME1: [cell1], COL_NAME2: [cell3]}}

    row_alt_data = PartialRowData(ROW_KEY_ALT)
    row_alt_data._chunks_encountered = True
    row_alt_data._committed = True
    row_alt_data._cells = {
        COLUMN_FAMILY_ID1: {COL_NAME1: [cell2]},
        COLUMN_FAMILY_ID2: {COL_NAME3: [cell4]},
    }

    expected_rows = {ROW_KEY: row_data, ROW_KEY_ALT: row_alt_data}
    assert rows_data.rows == expected_rows


def test_read_with_label_applied(data_table, rows_to_delete, skip_on_emulator):
    from google.cloud.bigtable.row_filters import ApplyLabelFilter
    from google.cloud.bigtable.row_filters import ColumnQualifierRegexFilter
    from google.cloud.bigtable.row_filters import RowFilterChain
    from google.cloud.bigtable.row_filters import RowFilterUnion

    row = data_table.direct_row(ROW_KEY)
    rows_to_delete.append(row)

    cell1, _, cell3, _ = _write_to_row(row, None, row, None)
    row.commit()

    # Combine a label with column 1.
    label1 = "label-red"
    label1_filter = ApplyLabelFilter(label1)
    col1_filter = ColumnQualifierRegexFilter(COL_NAME1)
    chain1 = RowFilterChain(filters=[col1_filter, label1_filter])

    # Combine a label with column 2.
    label2 = "label-blue"
    label2_filter = ApplyLabelFilter(label2)
    col2_filter = ColumnQualifierRegexFilter(COL_NAME2)
    chain2 = RowFilterChain(filters=[col2_filter, label2_filter])

    # Bring our two labeled columns together.
    row_filter = RowFilterUnion(filters=[chain1, chain2])
    partial_row_data = data_table.read_row(ROW_KEY, filter_=row_filter)
    assert partial_row_data.row_key == ROW_KEY

    cells_returned = partial_row_data.cells
    col_fam1 = cells_returned.pop(COLUMN_FAMILY_ID1)
    # Make sure COLUMN_FAMILY_ID1 was the only key.
    assert len(cells_returned) == 0

    (cell1_new,) = col_fam1.pop(COL_NAME1)
    (cell3_new,) = col_fam1.pop(COL_NAME2)
    # Make sure COL_NAME1 and COL_NAME2 were the only keys.
    assert len(col_fam1) == 0

    # Check that cell1 has matching values and gained a label.
    assert cell1_new.value == cell1.value
    assert cell1_new.timestamp == cell1.timestamp
    assert cell1.labels == []
    assert cell1_new.labels == [label1]

    # Check that cell3 has matching values and gained a label.
    assert cell3_new.value == cell3.value
    assert cell3_new.timestamp == cell3.timestamp
    assert cell3.labels == []
    assert cell3_new.labels == [label2]


def test_access_with_non_admin_client(data_client, data_instance_id, data_table_id):
    instance = data_client.instance(data_instance_id)
    table = instance.table(data_table_id)
    assert table.read_row("nonesuch") is None  # no raise
