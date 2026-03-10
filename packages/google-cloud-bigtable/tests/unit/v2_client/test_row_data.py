# Copyright 2016 Google LLC
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


import pytest

from google.cloud.bigtable.data.row import Row, Cell

TIMESTAMP_MICROS = 18738724000  # Make sure millis granularity
ROW_KEY = b"row-key"
FAMILY_NAME = "family"
QUALIFIER = b"qualifier"
VALUE = b"value"
TABLE_NAME = "table_name"
ROWS = [
    Row(
        key=ROW_KEY,
        cells=[
            Cell(
                value=VALUE,
                row_key=ROW_KEY,
                family=FAMILY_NAME,
                qualifier=QUALIFIER,
                timestamp_micros=TIMESTAMP_MICROS,
            )
        ],
    ),
    Row(
        key=ROW_KEY + b"2",
        cells=[
            Cell(
                value=VALUE,
                row_key=ROW_KEY + b"2",
                family=FAMILY_NAME,
                qualifier=QUALIFIER,
                timestamp_micros=TIMESTAMP_MICROS,
            )
        ],
    ),
    Row(
        key=ROW_KEY + b"3",
        cells=[
            Cell(
                value=VALUE,
                row_key=ROW_KEY + b"3",
                family=FAMILY_NAME,
                qualifier=QUALIFIER,
                timestamp_micros=TIMESTAMP_MICROS,
            )
        ],
    ),
]


def _make_cell(*args, **kwargs):
    from google.cloud.bigtable.row_data import Cell

    return Cell(*args, **kwargs)


def _cell_from_pb_test_helper(labels=None):
    import datetime

    from google.cloud._helpers import _EPOCH

    from google.cloud.bigtable.row_data import Cell
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    timestamp = _EPOCH + datetime.timedelta(microseconds=TIMESTAMP_MICROS)
    value = b"value-bytes"

    if labels is None:
        cell_pb = data_v2_pb2.Cell(value=value, timestamp_micros=TIMESTAMP_MICROS)
        cell_expected = _make_cell(value, TIMESTAMP_MICROS)
    else:
        cell_pb = data_v2_pb2.Cell(
            value=value, timestamp_micros=TIMESTAMP_MICROS, labels=labels
        )
        cell_expected = _make_cell(value, TIMESTAMP_MICROS, labels=labels)

    result = Cell.from_pb(cell_pb)

    assert result == cell_expected
    assert result.timestamp == timestamp


def test_cell_from_pb():
    _cell_from_pb_test_helper()


def test_cell_from_pb_with_labels():
    labels = ["label1", "label2"]
    _cell_from_pb_test_helper(labels)


def test_cell__from_data_client_cell():
    from google.cloud.bigtable.data.row import Cell as DataCell
    from google.cloud.bigtable.row_data import Cell

    data_cell = DataCell(
        value=VALUE,
        row_key=ROW_KEY,
        family=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
    )

    cell = Cell._from_data_client_cell(data_cell)

    assert cell.value == VALUE
    assert cell.timestamp_micros == TIMESTAMP_MICROS
    assert cell.labels == []


def test_cell__from_data_client_cell_with_labels():
    from google.cloud.bigtable.data.row import Cell as DataCell
    from google.cloud.bigtable.row_data import Cell

    data_cell = DataCell(
        value=VALUE,
        row_key=ROW_KEY,
        family=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        labels=["label1", "label2"],
    )

    cell = Cell._from_data_client_cell(data_cell)

    assert cell.value == VALUE
    assert cell.timestamp_micros == TIMESTAMP_MICROS
    assert cell.labels == ["label1", "label2"]


def test_cell_constructor():
    value = object()
    cell = _make_cell(value, TIMESTAMP_MICROS)
    assert cell.value == value


def test_cell___eq__():
    value = object()
    cell1 = _make_cell(value, TIMESTAMP_MICROS)
    cell2 = _make_cell(value, TIMESTAMP_MICROS)
    assert cell1 == cell2


def test_cell___eq__type_differ():
    cell1 = _make_cell(None, None)
    cell2 = object()
    assert not (cell1 == cell2)


def test_cell___ne__same_value():
    value = object()
    cell1 = _make_cell(value, TIMESTAMP_MICROS)
    cell2 = _make_cell(value, TIMESTAMP_MICROS)
    assert not (cell1 != cell2)


def test_cell___ne__():
    value1 = "value1"
    value2 = "value2"
    cell1 = _make_cell(value1, TIMESTAMP_MICROS)
    cell2 = _make_cell(value2, TIMESTAMP_MICROS)
    assert cell1 != cell2


def _make_partial_row_data(*args, **kwargs):
    from google.cloud.bigtable.row_data import PartialRowData

    return PartialRowData(*args, **kwargs)


def test_partial_row_data_constructor():
    row_key = object()
    partial_row_data = _make_partial_row_data(row_key)
    assert partial_row_data._row_key is row_key
    assert partial_row_data._cells == {}


def test_partial_row_data__from_data_client_row():
    from google.cloud.bigtable.data.row import Row as DataRow
    from google.cloud.bigtable.data.row import Cell as DataCell
    from google.cloud.bigtable.row_data import PartialRowData

    cells = [
        DataCell(
            value=b"1",
            row_key=ROW_KEY,
            family="family1",
            qualifier=b"qual1",
            timestamp_micros=1,
        ),
        DataCell(
            value=b"2",
            row_key=ROW_KEY,
            family="family1",
            qualifier=b"qual1",
            timestamp_micros=2,
        ),
        DataCell(
            value=b"3",
            row_key=ROW_KEY,
            family="family1",
            qualifier=b"qual2",
            timestamp_micros=3,
        ),
        DataCell(
            value=b"4",
            row_key=ROW_KEY,
            family="family2",
            qualifier=b"qual1",
            timestamp_micros=4,
        ),
        DataCell(
            value=b"5",
            row_key=ROW_KEY,
            family="family2",
            qualifier=b"qual2",
            timestamp_micros=5,
        ),
    ]

    row = DataRow(ROW_KEY, cells)
    partial_row_data = PartialRowData._from_data_client_row(row)

    expected_cells = {
        "family1": {
            b"qual1": [
                _make_cell(b"1", 1),
                _make_cell(b"2", 2),
            ],
            b"qual2": [
                _make_cell(b"3", 3),
            ],
        },
        "family2": {
            b"qual1": [
                _make_cell(b"4", 4),
            ],
            b"qual2": [
                _make_cell(b"5", 5),
            ],
        },
    }

    assert partial_row_data._row_key == ROW_KEY
    assert partial_row_data._cells == expected_cells


def test_partial_row_data___eq__():
    row_key = object()
    partial_row_data1 = _make_partial_row_data(row_key)
    partial_row_data2 = _make_partial_row_data(row_key)
    assert partial_row_data1 == partial_row_data2


def test_partial_row_data___eq__type_differ():
    partial_row_data1 = _make_partial_row_data(None)
    partial_row_data2 = object()
    assert not (partial_row_data1 == partial_row_data2)


def test_partial_row_data___ne__same_value():
    row_key = object()
    partial_row_data1 = _make_partial_row_data(row_key)
    partial_row_data2 = _make_partial_row_data(row_key)
    assert not (partial_row_data1 != partial_row_data2)


def test_partial_row_data___ne__():
    row_key1 = object()
    partial_row_data1 = _make_partial_row_data(row_key1)
    row_key2 = object()
    partial_row_data2 = _make_partial_row_data(row_key2)
    assert partial_row_data1 != partial_row_data2


def test_partial_row_data___ne__cells():
    row_key = object()
    partial_row_data1 = _make_partial_row_data(row_key)
    partial_row_data1._cells = object()
    partial_row_data2 = _make_partial_row_data(row_key)
    assert partial_row_data1 != partial_row_data2


def test_partial_row_data_to_dict():
    cell1 = object()
    cell2 = object()
    cell3 = object()

    family_name1 = "name1"
    family_name2 = "name2"
    qual1 = b"col1"
    qual2 = b"col2"
    qual3 = b"col3"

    partial_row_data = _make_partial_row_data(None)
    partial_row_data._cells = {
        family_name1: {qual1: cell1, qual2: cell2},
        family_name2: {qual3: cell3},
    }

    result = partial_row_data.to_dict()
    expected_result = {
        b"name1:col1": cell1,
        b"name1:col2": cell2,
        b"name2:col3": cell3,
    }
    assert result == expected_result


def test_partial_row_data_cell_value():
    family_name = "name1"
    qualifier = b"col1"
    cell = _make_cell_pb(b"value-bytes")

    partial_row_data = _make_partial_row_data(None)
    partial_row_data._cells = {family_name: {qualifier: [cell]}}

    result = partial_row_data.cell_value(family_name, qualifier)
    assert result == cell.value


def test_partial_row_data_cell_value_invalid_index():
    family_name = "name1"
    qualifier = b"col1"
    cell = _make_cell_pb(b"")

    partial_row_data = _make_partial_row_data(None)
    partial_row_data._cells = {family_name: {qualifier: [cell]}}

    with pytest.raises(IndexError):
        partial_row_data.cell_value(family_name, qualifier, index=None)


def test_partial_row_data_cell_value_invalid_column_family_key():
    family_name = "name1"
    qualifier = b"col1"

    partial_row_data = _make_partial_row_data(None)

    with pytest.raises(KeyError):
        partial_row_data.cell_value(family_name, qualifier)


def test_partial_row_data_cell_value_invalid_column_key():
    family_name = "name1"
    qualifier = b"col1"

    partial_row_data = _make_partial_row_data(None)
    partial_row_data._cells = {family_name: {}}

    with pytest.raises(KeyError):
        partial_row_data.cell_value(family_name, qualifier)


def test_partial_row_data_cell_values():
    family_name = "name1"
    qualifier = b"col1"
    cell = _make_cell_pb(b"value-bytes")

    partial_row_data = _make_partial_row_data(None)
    partial_row_data._cells = {family_name: {qualifier: [cell]}}

    values = []
    for value, timestamp_micros in partial_row_data.cell_values(family_name, qualifier):
        values.append(value)

    assert values[0] == cell.value


def test_partial_row_data_cell_values_with_max_count():
    family_name = "name1"
    qualifier = b"col1"
    cell_1 = _make_cell_pb(b"value-bytes-1")
    cell_2 = _make_cell_pb(b"value-bytes-2")

    partial_row_data = _make_partial_row_data(None)
    partial_row_data._cells = {family_name: {qualifier: [cell_1, cell_2]}}

    values = []
    for value, timestamp_micros in partial_row_data.cell_values(
        family_name, qualifier, max_count=1
    ):
        values.append(value)

    assert 1 == len(values)
    assert values[0] == cell_1.value


def test_partial_row_data_cells_property():
    partial_row_data = _make_partial_row_data(None)
    cells = {1: 2}
    partial_row_data._cells = cells
    assert partial_row_data.cells == cells


def test_partial_row_data_row_key_getter():
    row_key = object()
    partial_row_data = _make_partial_row_data(row_key)
    assert partial_row_data.row_key is row_key


def _make_grpc_call_error(exception):
    from grpc import Call, RpcError

    class TestingException(Call, RpcError):
        def __init__(self, exception):
            self.exception = exception

        def code(self):
            return self.exception.grpc_status_code

        def details(self):
            return "Testing"

        def trailing_metadata(self):
            return None

    return TestingException(exception)


<<<<<<< HEAD
def test__retry_read_rows_exception_miss():
    from google.api_core.exceptions import Conflict

    from google.cloud.bigtable.row_data import _retry_read_rows_exception

    exception = Conflict("testing")
    assert not _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_service_unavailable():
    from google.api_core.exceptions import ServiceUnavailable

    from google.cloud.bigtable.row_data import _retry_read_rows_exception

    exception = ServiceUnavailable("testing")
    assert _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_deadline_exceeded():
    from google.api_core.exceptions import DeadlineExceeded

    from google.cloud.bigtable.row_data import _retry_read_rows_exception

    exception = DeadlineExceeded("testing")
    assert _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_internal_server_not_retriable():
    from google.api_core.exceptions import InternalServerError

    from google.cloud.bigtable.row_data import (
        RETRYABLE_INTERNAL_ERROR_MESSAGES,
        _retry_read_rows_exception,
    )

    err_message = "500 Error"
    exception = InternalServerError(err_message)
    assert err_message not in RETRYABLE_INTERNAL_ERROR_MESSAGES
    assert not _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_internal_server_retriable():
    from google.api_core.exceptions import InternalServerError

    from google.cloud.bigtable.row_data import (
        RETRYABLE_INTERNAL_ERROR_MESSAGES,
        _retry_read_rows_exception,
    )

    for err_message in RETRYABLE_INTERNAL_ERROR_MESSAGES:
        exception = InternalServerError(err_message)
        assert _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_miss_wrapped_in_grpc():
    from google.api_core.exceptions import Conflict

    from google.cloud.bigtable.row_data import _retry_read_rows_exception

    wrapped = Conflict("testing")
    exception = _make_grpc_call_error(wrapped)
    assert not _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_service_unavailable_wrapped_in_grpc():
    from google.api_core.exceptions import ServiceUnavailable

    from google.cloud.bigtable.row_data import _retry_read_rows_exception

    wrapped = ServiceUnavailable("testing")
    exception = _make_grpc_call_error(wrapped)
    assert _retry_read_rows_exception(exception)


def test__retry_read_rows_exception_deadline_exceeded_wrapped_in_grpc():
    from google.api_core.exceptions import DeadlineExceeded

    from google.cloud.bigtable.row_data import _retry_read_rows_exception

    wrapped = DeadlineExceeded("testing")
    exception = _make_grpc_call_error(wrapped)
    assert _retry_read_rows_exception(exception)


=======
>>>>>>> 9ee40327a33 (feat: Rerouted ReadRows to data client (#1299))
def test_partial_cell_data():
    from google.cloud.bigtable.row_data import PartialCellData

    expected_key = b"row-key"
    expected_family_name = b"family-name"
    expected_qualifier = b"qualifier"
    expected_timestamp = 1234
    instance = PartialCellData(
        expected_key, expected_family_name, expected_qualifier, expected_timestamp
    )
    assert instance.row_key == expected_key
    assert instance.family_name == expected_family_name
    assert instance.qualifier == expected_qualifier
    assert instance.timestamp_micros == expected_timestamp
    assert instance.value == b""
    assert instance.labels == ()
    # test updating value
    added_value = b"added-value"
    instance.append_value(added_value)
    assert instance.value == added_value
    instance.append_value(added_value)
    assert instance.value == added_value + added_value


def _make_partial_rows_data(*args, **kwargs):
    from google.cloud.bigtable.row_data import PartialRowsData

    return PartialRowsData(*args, **kwargs)


def _partial_rows_data_consume_all(yrd):
    return [row.row_key for row in yrd]


def _make_generator(rows, error=None):
    for row in rows:
        if error:
            raise error
        else:
            yield row


def _assert_generator_closed(generator):
    with pytest.raises(StopIteration):
        next(generator)


def test_partial_rows_data_consume_all():
    generator = _make_generator(ROWS)
    partial_rows_data = _make_partial_rows_data(generator)
    partial_rows_data.consume_all()

    row1 = _make_partial_row_data(ROW_KEY)
    row1._cells[FAMILY_NAME] = {
        QUALIFIER: [_make_cell(value=VALUE, timestamp_micros=TIMESTAMP_MICROS)]
    }
    row2 = _make_partial_row_data(ROW_KEY + b"2")
    row2._cells[FAMILY_NAME] = {
        QUALIFIER: [_make_cell(value=VALUE, timestamp_micros=TIMESTAMP_MICROS)]
    }
    row3 = _make_partial_row_data(ROW_KEY + b"3")
    row3._cells[FAMILY_NAME] = {
        QUALIFIER: [_make_cell(value=VALUE, timestamp_micros=TIMESTAMP_MICROS)]
    }

    assert partial_rows_data.rows == {
        row1.row_key: row1,
        row2.row_key: row2,
        row3.row_key: row3,
    }

    _assert_generator_closed(generator)


def test_partial_rows_data_cancel():
    generator = _make_generator(ROWS)
    partial_rows_data = _make_partial_rows_data(generator)
    row_data = []

    count = 0
    for row in partial_rows_data:
        row_data.append(row)
        count += 1
        if count == 1:
            partial_rows_data.cancel()

    row1 = _make_partial_row_data(ROW_KEY)
    row1._cells[FAMILY_NAME] = {
        QUALIFIER: [_make_cell(value=VALUE, timestamp_micros=TIMESTAMP_MICROS)]
    }
    assert row_data == [row1]

    # We should have closed the generator, so there should be no more
    # elements left in there even though we haven't iterated through all the rows.
    _assert_generator_closed(generator)


def test_partial_rows_data_deadline_exceeded():
    from google.api_core import exceptions

    generator = _make_generator(
        ROWS, error=exceptions.DeadlineExceeded("Operation timed out.")
    )

    partial_rows_data = _make_partial_rows_data(generator)
    with pytest.raises(exceptions.RetryError):
        list(partial_rows_data)

<<<<<<< HEAD
    assert expected_result == result


def test_RRRM_build_updated_request_full_table():
    from google.cloud.bigtable_v2 import types

    last_scanned_key = b"row_key14"

    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()
    expected_result = _ReadRowsRequestPB(table_name=TABLE_NAME)
    row_range1 = types.RowRange(start_key_open=last_scanned_key)
    expected_result.rows.row_ranges.append(row_range1)
    assert expected_result == result


def test_RRRM_build_updated_request_no_start_key():
    from google.cloud.bigtable.row_filters import RowSampleFilter
    from google.cloud.bigtable_v2 import types

    row_filter = RowSampleFilter(0.33)
    last_scanned_key = b"row_key25"
    request = _ReadRowsRequestPB(
        filter=row_filter._to_pb(), rows_limit=8, table_name=TABLE_NAME
    )
    row_range1 = types.RowRange(end_key_open=b"row_key29")
    request.rows.row_ranges.append(row_range1)

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME, filter=row_filter._to_pb(), rows_limit=6
    )

    row_range2 = types.RowRange(
        start_key_open=last_scanned_key, end_key_open=b"row_key29"
    )
    expected_result.rows.row_ranges.append(row_range2)

    assert expected_result == result


def test_RRRM_build_updated_request_no_end_key():
    from google.cloud.bigtable.row_filters import RowSampleFilter
    from google.cloud.bigtable_v2 import types

    row_filter = RowSampleFilter(0.33)
    last_scanned_key = b"row_key25"
    request = _ReadRowsRequestPB(
        filter=row_filter._to_pb(), rows_limit=8, table_name=TABLE_NAME
    )

    row_range1 = types.RowRange(start_key_closed=b"row_key20")
    request.rows.row_ranges.append(row_range1)

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME, filter=row_filter._to_pb(), rows_limit=6
    )
    row_range2 = types.RowRange(start_key_open=last_scanned_key)
    expected_result.rows.row_ranges.append(row_range2)

    assert expected_result == result


def test_RRRM_build_updated_request_rows():
    from google.cloud.bigtable.row_filters import RowSampleFilter

    row_filter = RowSampleFilter(0.33)
    last_scanned_key = b"row_key4"
    request = _ReadRowsRequestPB(
        filter=row_filter._to_pb(), rows_limit=5, table_name=TABLE_NAME
    )
    request.rows.row_keys.extend(
        [b"row_key1", b"row_key2", b"row_key4", b"row_key5", b"row_key7", b"row_key9"]
    )

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 3)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME, filter=row_filter._to_pb(), rows_limit=2
    )
    expected_result.rows.row_keys.extend([b"row_key5", b"row_key7", b"row_key9"])

    assert expected_result == result


def test_RRRM_build_updated_request_rows_limit():
    from google.cloud.bigtable_v2 import types

    last_scanned_key = b"row_key14"

    request = _ReadRowsRequestPB(table_name=TABLE_NAME, rows_limit=10)
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()
    expected_result = _ReadRowsRequestPB(table_name=TABLE_NAME, rows_limit=8)
    row_range1 = types.RowRange(start_key_open=last_scanned_key)
    expected_result.rows.row_ranges.append(row_range1)
    assert expected_result == result


def test_RRRM__key_already_read():
    last_scanned_key = b"row_key14"
    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    assert request_manager._key_already_read(b"row_key11")
    assert not request_manager._key_already_read(b"row_key16")


def test_RRRM__rows_limit_reached():
    from google.cloud.bigtable.row_data import InvalidRetryRequest

    last_scanned_key = b"row_key14"
    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request.rows_limit = 2
    request_manager = _make_read_rows_request_manager(
        request, last_scanned_key=last_scanned_key, rows_read_so_far=2
    )
    with pytest.raises(InvalidRetryRequest):
        request_manager.build_updated_request()


def test_RRRM_build_updated_request_last_row_read_raises_invalid_retry_request():
    from google.cloud.bigtable.row_data import InvalidRetryRequest

    last_scanned_key = b"row_key4"
    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request.rows.row_keys.extend([b"row_key1", b"row_key2", b"row_key4"])

    request_manager = _make_read_rows_request_manager(
        request, last_scanned_key, rows_read_so_far=3
    )
    with pytest.raises(InvalidRetryRequest):
        request_manager.build_updated_request()


def test_RRRM_build_updated_request_row_ranges_read_raises_invalid_retry_request():
    from google.cloud.bigtable import row_set
    from google.cloud.bigtable.row_data import InvalidRetryRequest

    row_range1 = row_set.RowRange(b"row_key21", b"row_key29")

    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request.rows.row_ranges.append(row_range1.get_range_kwargs())

    last_scanned_key = b"row_key4"
    request = _ReadRowsRequestPB(
        table_name=TABLE_NAME,
    )
    request.rows.row_ranges.append(row_range1.get_range_kwargs())

    request_manager = _make_read_rows_request_manager(
        request, last_scanned_key, rows_read_so_far=2
    )
    with pytest.raises(InvalidRetryRequest):
        request_manager.build_updated_request()


def test_RRRM_build_updated_request_row_ranges_valid():
    from google.cloud.bigtable import row_set

    row_range1 = row_set.RowRange(b"row_key21", b"row_key29")

    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request.rows.row_ranges.append(row_range1.get_range_kwargs())

    last_scanned_key = b"row_key21"
    request = _ReadRowsRequestPB(
        table_name=TABLE_NAME,
    )
    request.rows.row_ranges.append(row_range1.get_range_kwargs())

    request_manager = _make_read_rows_request_manager(
        request, last_scanned_key, rows_read_so_far=1
    )
    updated_request = request_manager.build_updated_request()
    assert len(updated_request.rows.row_ranges) > 0


class _MockCancellableIterator(object):
    cancel_calls = 0

    def __init__(self, *values):
        self.iter_values = iter(values)
        self.last_scanned_row_key = ""

    def cancel(self):
        self.cancel_calls += 1

    def next(self):
        return next(self.iter_values)

    __next__ = next


class _MockFailureIterator_1(object):
    def next(self):
        from google.api_core.exceptions import DeadlineExceeded

        raise DeadlineExceeded("Failed to read from server")

    __next__ = next


def _ReadRowsResponseV2(chunks, last_scanned_row_key=b""):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.ReadRowsResponse(
        chunks=chunks, last_scanned_row_key=last_scanned_row_key
    )


def _generate_cell_chunks(chunk_text_pbs):
    from google.protobuf.text_format import Merge

    from google.cloud.bigtable_v2.types.bigtable import ReadRowsResponse

    chunks = []

    for chunk_text_pb in chunk_text_pbs:
        chunk = ReadRowsResponse.CellChunk()
        chunk._pb = Merge(chunk_text_pb, chunk._pb)
        chunks.append(chunk)

    return chunks


def _ReadRowsResponseCellChunkPB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    family_name = kw.pop("family_name", None)
    qualifier = kw.pop("qualifier", None)
    message = messages_v2_pb2.ReadRowsResponse.CellChunk(*args, **kw)

    if family_name:
        message.family_name = family_name
    if qualifier:
        message.qualifier = qualifier

    return message
=======
    # An exception should close the generator.
    _assert_generator_closed(generator)
>>>>>>> 9ee40327a33 (feat: Rerouted ReadRows to data client (#1299))


def _make_cell_pb(value):
    from google.cloud.bigtable import row_data

    return row_data.Cell(value, TIMESTAMP_MICROS)
