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


import os

import mock
import pytest

from ._testing import _make_credentials

TIMESTAMP_MICROS = 18738724000  # Make sure millis granularity
ROW_KEY = b"row-key"
FAMILY_NAME = "family"
QUALIFIER = b"qualifier"
TIMESTAMP_MICROS = 100
VALUE = b"value"
TABLE_NAME = "table_name"


def _make_cell(*args, **kwargs):
    from google.cloud.bigtable.row_data import Cell

    return Cell(*args, **kwargs)


def _cell_from_pb_test_helper(labels=None):
    import datetime
    from google.cloud._helpers import _EPOCH
    from google.cloud.bigtable_v2.types import data as data_v2_pb2
    from google.cloud.bigtable.row_data import Cell

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
    from grpc import Call
    from grpc import RpcError

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


def _make_partial_rows_data(*args, **kwargs):
    from google.cloud.bigtable.row_data import PartialRowsData

    return PartialRowsData(*args, **kwargs)


def _partial_rows_data_consume_all(yrd):
    return [row.row_key for row in yrd]


def _make_client(*args, **kwargs):
    from google.cloud.bigtable.client import Client

    return Client(*args, **kwargs)


def test_partial_rows_data_constructor():
    from google.cloud.bigtable.row_data import DEFAULT_RETRY_READ_ROWS

    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    partial_rows_data = _make_partial_rows_data(client._data_stub.ReadRows, request)
    assert partial_rows_data.request is request
    assert partial_rows_data.rows == {}
    assert partial_rows_data.retry == DEFAULT_RETRY_READ_ROWS


def test_partial_rows_data_constructor_with_retry():
    from google.cloud.bigtable.row_data import DEFAULT_RETRY_READ_ROWS

    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    retry = DEFAULT_RETRY_READ_ROWS
    partial_rows_data = _make_partial_rows_data(
        client._data_stub.ReadRows, request, retry
    )
    partial_rows_data.read_method.assert_called_once_with(
        request, timeout=DEFAULT_RETRY_READ_ROWS.deadline + 1
    )
    assert partial_rows_data.request is request
    assert partial_rows_data.rows == {}
    assert partial_rows_data.retry == retry


def test_partial_rows_data___eq__():
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    partial_rows_data1 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    partial_rows_data2 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    assert partial_rows_data1.rows == partial_rows_data2.rows


def test_partial_rows_data___eq__type_differ():
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    partial_rows_data1 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    partial_rows_data2 = object()
    assert not (partial_rows_data1 == partial_rows_data2)


def test_partial_rows_data___ne__same_value():
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    partial_rows_data1 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    partial_rows_data2 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    assert partial_rows_data1 != partial_rows_data2


def test_partial_rows_data___ne__():
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    partial_rows_data1 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    partial_rows_data2 = _make_partial_rows_data(client._data_stub.ReadRows, request)
    assert partial_rows_data1 != partial_rows_data2


def test_partial_rows_data_rows_getter():
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    partial_rows_data = _make_partial_rows_data(client._data_stub.ReadRows, request)
    partial_rows_data.rows = value = object()
    assert partial_rows_data.rows is value


def test_partial_rows_data_state_start():
    client = _Client()
    iterator = _MockCancellableIterator()
    client._data_stub = mock.MagicMock()
    client._data_stub.ReadRows.side_effect = [iterator]
    request = object()
    yrd = _make_partial_rows_data(client._data_stub.ReadRows, request)
    assert yrd.state == yrd.NEW_ROW


def test_partial_rows_data_state_new_row_w_row():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    chunk = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunks = [chunk]

    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)

    data_api = mock.create_autospec(BigtableClient)

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    client._table_data_client = data_api
    request = object()

    yrd = _make_partial_rows_data(client._table_data_client.read_rows, request)
    assert yrd.retry._deadline == 60.0

    yrd.response_iterator = iterator
    rows = [row for row in yrd]

    result = rows[0]
    assert result.row_key == ROW_KEY
    assert yrd._counter == 1
    assert yrd.state == yrd.NEW_ROW


def test_partial_rows_data_multiple_chunks():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    chunk1 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=False,
    )
    chunk2 = _ReadRowsResponseCellChunkPB(
        qualifier=QUALIFIER + b"1",
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunks = [chunk1, chunk2]

    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)
    data_api = mock.create_autospec(BigtableClient)
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    client._table_data_client = data_api
    request = object()

    yrd = _make_partial_rows_data(data_api.read_rows, request)

    yrd.response_iterator = iterator
    rows = [row for row in yrd]
    result = rows[0]
    assert result.row_key == ROW_KEY
    assert yrd._counter == 1
    assert yrd.state == yrd.NEW_ROW


def test_partial_rows_data_cancel():
    client = _Client()
    response_iterator = _MockCancellableIterator()
    client._data_stub = mock.MagicMock()
    client._data_stub.ReadRows.side_effect = [response_iterator]
    request = object()
    yield_rows_data = _make_partial_rows_data(client._data_stub.ReadRows, request)
    assert response_iterator.cancel_calls == 0
    yield_rows_data.cancel()
    assert response_iterator.cancel_calls == 1
    assert list(yield_rows_data) == []


def test_partial_rows_data_cancel_between_chunks():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    chunk1 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunk2 = _ReadRowsResponseCellChunkPB(
        qualifier=QUALIFIER + b"1",
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunks = [chunk1, chunk2]
    response = _ReadRowsResponseV2(chunks)
    response_iterator = _MockCancellableIterator(response)

    client = _Client()
    data_api = mock.create_autospec(BigtableClient)
    client._table_data_client = data_api
    request = object()
    yrd = _make_partial_rows_data(data_api.read_rows, request)
    yrd.response_iterator = response_iterator

    rows = []
    for row in yrd:
        yrd.cancel()
        rows.append(row)

    assert response_iterator.cancel_calls == 1
    assert list(yrd) == []


# 'consume_next' tested via 'TestPartialRowsData_JSON_acceptance_tests'


def test_partial_rows_data__copy_from_previous_unset():
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    yrd = _make_partial_rows_data(client._data_stub.read_rows, request)
    cell = _PartialCellData()
    yrd._copy_from_previous(cell)
    assert cell.row_key == b""
    assert cell.family_name == ""
    assert cell.qualifier is None
    assert cell.timestamp_micros == 0
    assert cell.labels == []


def test_partial_rows_data__copy_from_previous_blank():
    ROW_KEY = "RK"
    FAMILY_NAME = "A"
    QUALIFIER = b"C"
    TIMESTAMP_MICROS = 100
    LABELS = ["L1", "L2"]
    client = _Client()
    client._data_stub = mock.MagicMock()
    request = object()
    yrd = _make_partial_rows_data(client._data_stub.ReadRows, request)
    cell = _PartialCellData(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        labels=LABELS,
    )
    yrd._previous_cell = _PartialCellData()
    yrd._copy_from_previous(cell)
    assert cell.row_key == ROW_KEY
    assert cell.family_name == FAMILY_NAME
    assert cell.qualifier == QUALIFIER
    assert cell.timestamp_micros == TIMESTAMP_MICROS
    assert cell.labels == LABELS


def test_partial_rows_data__copy_from_previous_filled():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    ROW_KEY = "RK"
    FAMILY_NAME = "A"
    QUALIFIER = b"C"
    TIMESTAMP_MICROS = 100
    LABELS = ["L1", "L2"]
    client = _Client()
    data_api = mock.create_autospec(BigtableClient)
    client._data_stub = data_api
    request = object()
    yrd = _make_partial_rows_data(client._data_stub.read_rows, request)
    yrd._previous_cell = _PartialCellData(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        labels=LABELS,
    )
    cell = _PartialCellData()
    yrd._copy_from_previous(cell)
    assert cell.row_key == ROW_KEY
    assert cell.family_name == FAMILY_NAME
    assert cell.qualifier == QUALIFIER
    assert cell.timestamp_micros == 0
    assert cell.labels == []


def test_partial_rows_data_valid_last_scanned_row_key_on_start():
    client = _Client()
    response = _ReadRowsResponseV2(chunks=(), last_scanned_row_key="2.AFTER")
    iterator = _MockCancellableIterator(response)
    client._data_stub = mock.MagicMock()
    client._data_stub.read_rows.side_effect = [iterator]
    request = object()
    yrd = _make_partial_rows_data(client._data_stub.read_rows, request)
    yrd.last_scanned_row_key = "1.BEFORE"
    _partial_rows_data_consume_all(yrd)
    assert yrd.last_scanned_row_key == "2.AFTER"


def test_partial_rows_data_invalid_empty_chunk():
    from google.cloud.bigtable.row_data import InvalidChunk
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    client = _Client()
    chunks = _generate_cell_chunks([""])
    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)
    client._data_stub = mock.create_autospec(BigtableClient)
    client._data_stub.read_rows.side_effect = [iterator]
    request = object()
    yrd = _make_partial_rows_data(client._data_stub.read_rows, request)
    with pytest.raises(InvalidChunk):
        _partial_rows_data_consume_all(yrd)


def test_partial_rows_data_state_cell_in_progress():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    LABELS = ["L1", "L2"]

    request = object()
    client = _Client()
    client._data_stub = mock.create_autospec(BigtableClient)
    yrd = _make_partial_rows_data(client._data_stub.read_rows, request)

    chunk = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        labels=LABELS,
    )
    yrd._update_cell(chunk)

    more_cell_data = _ReadRowsResponseCellChunkPB(value=VALUE)
    yrd._update_cell(more_cell_data)

    assert yrd._cell.row_key == ROW_KEY
    assert yrd._cell.family_name == FAMILY_NAME
    assert yrd._cell.qualifier == QUALIFIER
    assert yrd._cell.timestamp_micros == TIMESTAMP_MICROS
    assert yrd._cell.labels == LABELS
    assert yrd._cell.value == VALUE + VALUE


def test_partial_rows_data_yield_rows_data():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    client = _Client()

    chunk = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunks = [chunk]

    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)
    data_api = mock.create_autospec(BigtableClient)
    client._data_stub = data_api
    client._data_stub.read_rows.side_effect = [iterator]

    request = object()

    yrd = _make_partial_rows_data(client._data_stub.read_rows, request)

    result = _partial_rows_data_consume_all(yrd)[0]

    assert result == ROW_KEY


def test_partial_rows_data_yield_retry_rows_data():
    from google.api_core import retry

    client = _Client()

    retry_read_rows = retry.Retry(predicate=_read_rows_retry_exception)

    chunk = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunks = [chunk]

    response = _ReadRowsResponseV2(chunks)
    failure_iterator = _MockFailureIterator_1()
    iterator = _MockCancellableIterator(response)
    client._data_stub = mock.MagicMock()
    client._data_stub.ReadRows.side_effect = [failure_iterator, iterator]

    request = object()

    yrd = _make_partial_rows_data(client._data_stub.ReadRows, request, retry_read_rows)

    result = _partial_rows_data_consume_all(yrd)[0]

    assert result == ROW_KEY


def _make_read_rows_request_manager(*args, **kwargs):
    from google.cloud.bigtable.row_data import _ReadRowsRequestManager

    return _ReadRowsRequestManager(*args, **kwargs)


@pytest.fixture(scope="session")
def rrrm_data():
    from google.cloud.bigtable import row_set

    row_range1 = row_set.RowRange(b"row_key21", b"row_key29")
    row_range2 = row_set.RowRange(b"row_key31", b"row_key39")
    row_range3 = row_set.RowRange(b"row_key41", b"row_key49")

    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request.rows.row_ranges.append(row_range1.get_range_kwargs())
    request.rows.row_ranges.append(row_range2.get_range_kwargs())
    request.rows.row_ranges.append(row_range3.get_range_kwargs())

    yield {
        "row_range1": row_range1,
        "row_range2": row_range2,
        "row_range3": row_range3,
        "request": request,
    }


def test_RRRM_constructor():
    request = mock.Mock()
    last_scanned_key = "last_key"
    rows_read_so_far = 10

    request_manager = _make_read_rows_request_manager(
        request, last_scanned_key, rows_read_so_far
    )
    assert request == request_manager.message
    assert last_scanned_key == request_manager.last_scanned_key
    assert rows_read_so_far == request_manager.rows_read_so_far


def test_RRRM__filter_row_key():
    table_name = "table_name"
    request = _ReadRowsRequestPB(table_name=table_name)
    request.rows.row_keys.extend([b"row_key1", b"row_key2", b"row_key3", b"row_key4"])

    last_scanned_key = b"row_key2"
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)
    row_keys = request_manager._filter_rows_keys()

    expected_row_keys = [b"row_key3", b"row_key4"]
    assert expected_row_keys == row_keys


def test_RRRM__filter_row_ranges_all_ranges_added_back(rrrm_data):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    request = rrrm_data["request"]
    last_scanned_key = b"row_key14"
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)
    row_ranges = request_manager._filter_row_ranges()

    exp_row_range1 = data_v2_pb2.RowRange(
        start_key_closed=b"row_key21", end_key_open=b"row_key29"
    )
    exp_row_range2 = data_v2_pb2.RowRange(
        start_key_closed=b"row_key31", end_key_open=b"row_key39"
    )
    exp_row_range3 = data_v2_pb2.RowRange(
        start_key_closed=b"row_key41", end_key_open=b"row_key49"
    )
    exp_row_ranges = [exp_row_range1, exp_row_range2, exp_row_range3]

    assert exp_row_ranges == row_ranges


def test_RRRM__filter_row_ranges_all_ranges_already_read(rrrm_data):
    request = rrrm_data["request"]
    last_scanned_key = b"row_key54"
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)
    row_ranges = request_manager._filter_row_ranges()

    assert row_ranges == []


def test_RRRM__filter_row_ranges_all_ranges_already_read_open_closed():
    from google.cloud.bigtable import row_set

    last_scanned_key = b"row_key54"

    row_range1 = row_set.RowRange(b"row_key21", b"row_key29", False, True)
    row_range2 = row_set.RowRange(b"row_key31", b"row_key39")
    row_range3 = row_set.RowRange(b"row_key41", b"row_key49", False, True)

    request = _ReadRowsRequestPB(table_name=TABLE_NAME)
    request.rows.row_ranges.append(row_range1.get_range_kwargs())
    request.rows.row_ranges.append(row_range2.get_range_kwargs())
    request.rows.row_ranges.append(row_range3.get_range_kwargs())

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)
    request_manager.new_message = _ReadRowsRequestPB(table_name=TABLE_NAME)
    row_ranges = request_manager._filter_row_ranges()

    assert row_ranges == []


def test_RRRM__filter_row_ranges_some_ranges_already_read(rrrm_data):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    request = rrrm_data["request"]
    last_scanned_key = b"row_key22"
    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)
    request_manager.new_message = _ReadRowsRequestPB(table_name=TABLE_NAME)
    row_ranges = request_manager._filter_row_ranges()

    exp_row_range1 = data_v2_pb2.RowRange(
        start_key_open=b"row_key22", end_key_open=b"row_key29"
    )
    exp_row_range2 = data_v2_pb2.RowRange(
        start_key_closed=b"row_key31", end_key_open=b"row_key39"
    )
    exp_row_range3 = data_v2_pb2.RowRange(
        start_key_closed=b"row_key41", end_key_open=b"row_key49"
    )
    exp_row_ranges = [exp_row_range1, exp_row_range2, exp_row_range3]

    assert exp_row_ranges == row_ranges


def test_RRRM_build_updated_request(rrrm_data):
    from google.cloud.bigtable.row_filters import RowSampleFilter
    from google.cloud.bigtable_v2 import types

    row_range1 = rrrm_data["row_range1"]
    row_filter = RowSampleFilter(0.33)
    last_scanned_key = b"row_key25"
    request = _ReadRowsRequestPB(
        filter=row_filter.to_pb(),
        rows_limit=8,
        table_name=TABLE_NAME,
        app_profile_id="app-profile-id-1",
    )
    request.rows.row_ranges.append(row_range1.get_range_kwargs())

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME,
        filter=row_filter.to_pb(),
        rows_limit=6,
        app_profile_id="app-profile-id-1",
    )

    row_range1 = types.RowRange(
        start_key_open=last_scanned_key, end_key_open=row_range1.end_key
    )
    expected_result.rows.row_ranges.append(row_range1)

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
        filter=row_filter.to_pb(), rows_limit=8, table_name=TABLE_NAME
    )
    row_range1 = types.RowRange(end_key_open=b"row_key29")
    request.rows.row_ranges.append(row_range1)

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME, filter=row_filter.to_pb(), rows_limit=6
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
        filter=row_filter.to_pb(), rows_limit=8, table_name=TABLE_NAME
    )

    row_range1 = types.RowRange(start_key_closed=b"row_key20")
    request.rows.row_ranges.append(row_range1)

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 2)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME, filter=row_filter.to_pb(), rows_limit=6
    )
    row_range2 = types.RowRange(start_key_open=last_scanned_key)
    expected_result.rows.row_ranges.append(row_range2)

    assert expected_result == result


def test_RRRM_build_updated_request_rows():
    from google.cloud.bigtable.row_filters import RowSampleFilter

    row_filter = RowSampleFilter(0.33)
    last_scanned_key = b"row_key4"
    request = _ReadRowsRequestPB(
        filter=row_filter.to_pb(), rows_limit=5, table_name=TABLE_NAME
    )
    request.rows.row_keys.extend(
        [b"row_key1", b"row_key2", b"row_key4", b"row_key5", b"row_key7", b"row_key9"]
    )

    request_manager = _make_read_rows_request_manager(request, last_scanned_key, 3)

    result = request_manager.build_updated_request()

    expected_result = _ReadRowsRequestPB(
        table_name=TABLE_NAME, filter=row_filter.to_pb(), rows_limit=2
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


@pytest.fixture(scope="session")
def json_tests():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "read-rows-acceptance-test.json")
    raw = _parse_readrows_acceptance_tests(filename)
    tests = {}
    for (name, chunks, results) in raw:
        tests[name] = chunks, results

    yield tests


# JSON Error cases:  invalid chunks


def _fail_during_consume(json_tests, testcase_name):
    from google.cloud.bigtable.row_data import InvalidChunk

    client = _Client()
    chunks, results = json_tests[testcase_name]
    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)
    client._data_stub = mock.MagicMock()
    client._data_stub.ReadRows.side_effect = [iterator]
    request = object()
    prd = _make_partial_rows_data(client._data_stub.ReadRows, request)
    with pytest.raises(InvalidChunk):
        prd.consume_all()
    expected_result = _sort_flattend_cells(
        [result for result in results if not result["error"]]
    )
    flattened = _sort_flattend_cells(_flatten_cells(prd))
    assert flattened == expected_result


def test_prd_json_accept_invalid_no_cell_key_before_commit(json_tests):
    _fail_during_consume(json_tests, "invalid - no cell key before commit")


def test_prd_json_accept_invalid_no_cell_key_before_value(json_tests):
    _fail_during_consume(json_tests, "invalid - no cell key before value")


def test_prd_json_accept_invalid_new_col_family_wo_qualifier(json_tests):
    _fail_during_consume(json_tests, "invalid - new col family must specify qualifier")


def test_prd_json_accept_invalid_no_commit_between_rows(json_tests):
    _fail_during_consume(json_tests, "invalid - no commit between rows")


def test_prd_json_accept_invalid_no_commit_after_first_row(json_tests):
    _fail_during_consume(json_tests, "invalid - no commit after first row")


def test_prd_json_accept_invalid_duplicate_row_key(json_tests):
    _fail_during_consume(json_tests, "invalid - duplicate row key")


def test_prd_json_accept_invalid_new_row_missing_row_key(json_tests):
    _fail_during_consume(json_tests, "invalid - new row missing row key")


def test_prd_json_accept_invalid_bare_reset(json_tests):
    _fail_during_consume(json_tests, "invalid - bare reset")


def test_prd_json_accept_invalid_bad_reset_no_commit(json_tests):
    _fail_during_consume(json_tests, "invalid - bad reset, no commit")


def test_prd_json_accept_invalid_missing_key_after_reset(json_tests):
    _fail_during_consume(json_tests, "invalid - missing key after reset")


def test_prd_json_accept_invalid_reset_with_chunk(json_tests):
    _fail_during_consume(json_tests, "invalid - reset with chunk")


def test_prd_json_accept_invalid_commit_with_chunk(json_tests):
    _fail_during_consume(json_tests, "invalid - commit with chunk")


# JSON Error cases:  incomplete final row


def _sort_flattend_cells(flattened):
    import operator

    key_func = operator.itemgetter("rk", "fm", "qual")
    return sorted(flattened, key=key_func)


def _incomplete_final_row(json_tests, testcase_name):
    client = _Client()
    chunks, results = json_tests[testcase_name]
    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)
    client._data_stub = mock.MagicMock()
    client._data_stub.ReadRows.side_effect = [iterator]
    request = object()
    prd = _make_partial_rows_data(client._data_stub.ReadRows, request)
    with pytest.raises(ValueError):
        prd.consume_all()
    assert prd.state == prd.ROW_IN_PROGRESS
    expected_result = _sort_flattend_cells(
        [result for result in results if not result["error"]]
    )
    flattened = _sort_flattend_cells(_flatten_cells(prd))
    assert flattened == expected_result


def test_prd_json_accept_invalid_no_commit(json_tests):
    _incomplete_final_row(json_tests, "invalid - no commit")


def test_prd_json_accept_invalid_last_row_missing_commit(json_tests):
    _incomplete_final_row(json_tests, "invalid - last row missing commit")


# Non-error cases

_marker = object()


def _match_results(json_tests, testcase_name, expected_result=_marker):
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    client = _Client()
    chunks, results = json_tests[testcase_name]
    response = _ReadRowsResponseV2(chunks)
    iterator = _MockCancellableIterator(response)
    data_api = mock.create_autospec(BigtableClient)
    client._table_data_client = data_api
    client._table_data_client.read_rows.side_effect = [iterator]
    request = object()
    prd = _make_partial_rows_data(client._table_data_client.read_rows, request)
    prd.consume_all()
    flattened = _sort_flattend_cells(_flatten_cells(prd))
    if expected_result is _marker:
        expected_result = _sort_flattend_cells(results)
    assert flattened == expected_result


def test_prd_json_accept_bare_commit_implies_ts_zero(json_tests):
    _match_results(json_tests, "bare commit implies ts=0")


def test_prd_json_accept_simple_row_with_timestamp(json_tests):
    _match_results(json_tests, "simple row with timestamp")


def test_prd_json_accept_missing_timestamp_implies_ts_zero(json_tests):
    _match_results(json_tests, "missing timestamp, implied ts=0")


def test_prd_json_accept_empty_cell_value(json_tests):
    _match_results(json_tests, "empty cell value")


def test_prd_json_accept_two_unsplit_cells(json_tests):
    _match_results(json_tests, "two unsplit cells")


def test_prd_json_accept_two_qualifiers(json_tests):
    _match_results(json_tests, "two qualifiers")


def test_prd_json_accept_two_families(json_tests):
    _match_results(json_tests, "two families")


def test_prd_json_accept_with_labels(json_tests):
    _match_results(json_tests, "with labels")


def test_prd_json_accept_split_cell_bare_commit(json_tests):
    _match_results(json_tests, "split cell, bare commit")


def test_prd_json_accept_split_cell(json_tests):
    _match_results(json_tests, "split cell")


def test_prd_json_accept_split_four_ways(json_tests):
    _match_results(json_tests, "split four ways")


def test_prd_json_accept_two_split_cells(json_tests):
    _match_results(json_tests, "two split cells")


def test_prd_json_accept_multi_qualifier_splits(json_tests):
    _match_results(json_tests, "multi-qualifier splits")


def test_prd_json_accept_multi_qualifier_multi_split(json_tests):
    _match_results(json_tests, "multi-qualifier multi-split")


def test_prd_json_accept_multi_family_split(json_tests):
    _match_results(json_tests, "multi-family split")


def test_prd_json_accept_two_rows(json_tests):
    _match_results(json_tests, "two rows")


def test_prd_json_accept_two_rows_implicit_timestamp(json_tests):
    _match_results(json_tests, "two rows implicit timestamp")


def test_prd_json_accept_two_rows_empty_value(json_tests):
    _match_results(json_tests, "two rows empty value")


def test_prd_json_accept_two_rows_one_with_multiple_cells(json_tests):
    _match_results(json_tests, "two rows, one with multiple cells")


def test_prd_json_accept_two_rows_multiple_cells_multiple_families(json_tests):
    _match_results(json_tests, "two rows, multiple cells, multiple families")


def test_prd_json_accept_two_rows_multiple_cells(json_tests):
    _match_results(json_tests, "two rows, multiple cells")


def test_prd_json_accept_two_rows_four_cells_two_labels(json_tests):
    _match_results(json_tests, "two rows, four cells, 2 labels")


def test_prd_json_accept_two_rows_with_splits_same_timestamp(json_tests):
    _match_results(json_tests, "two rows with splits, same timestamp")


def test_prd_json_accept_no_data_after_reset(json_tests):
    # JSON testcase has `"results": null`
    _match_results(json_tests, "no data after reset", expected_result=[])


def test_prd_json_accept_simple_reset(json_tests):
    _match_results(json_tests, "simple reset")


def test_prd_json_accept_reset_to_new_val(json_tests):
    _match_results(json_tests, "reset to new val")


def test_prd_json_accept_reset_to_new_qual(json_tests):
    _match_results(json_tests, "reset to new qual")


def test_prd_json_accept_reset_with_splits(json_tests):
    _match_results(json_tests, "reset with splits")


def test_prd_json_accept_two_resets(json_tests):
    _match_results(json_tests, "two resets")


def test_prd_json_accept_reset_to_new_row(json_tests):
    _match_results(json_tests, "reset to new row")


def test_prd_json_accept_reset_in_between_chunks(json_tests):
    _match_results(json_tests, "reset in between chunks")


def test_prd_json_accept_empty_cell_chunk(json_tests):
    _match_results(json_tests, "empty cell chunk")


def test_prd_json_accept_empty_second_qualifier(json_tests):
    _match_results(json_tests, "empty second qualifier")


def _flatten_cells(prd):
    # Match results format from JSON testcases.
    # Doesn't handle error cases.
    from google.cloud._helpers import _bytes_to_unicode
    from google.cloud._helpers import _microseconds_from_datetime

    for row_key, row in prd.rows.items():
        for family_name, family in row.cells.items():
            for qualifier, column in family.items():
                for cell in column:
                    yield {
                        "rk": _bytes_to_unicode(row_key),
                        "fm": family_name,
                        "qual": _bytes_to_unicode(qualifier),
                        "ts": _microseconds_from_datetime(cell.timestamp),
                        "value": _bytes_to_unicode(cell.value),
                        "label": " ".join(cell.labels),
                        "error": False,
                    }


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


class _PartialCellData(object):

    row_key = b""
    family_name = ""
    qualifier = None
    timestamp_micros = 0
    last_scanned_row_key = ""

    def __init__(self, **kw):
        self.labels = kw.pop("labels", [])
        self.__dict__.update(kw)


class _ReadRowsResponseV2(object):
    def __init__(self, chunks, last_scanned_row_key=""):
        self.chunks = chunks
        self.last_scanned_row_key = last_scanned_row_key


def _generate_cell_chunks(chunk_text_pbs):
    from google.protobuf.text_format import Merge
    from google.cloud.bigtable_v2.types.bigtable import ReadRowsResponse

    chunks = []

    for chunk_text_pb in chunk_text_pbs:
        chunk = ReadRowsResponse.CellChunk()
        chunk._pb = Merge(chunk_text_pb, chunk._pb)
        chunks.append(chunk)

    return chunks


def _parse_readrows_acceptance_tests(filename):
    """Parse acceptance tests from JSON

    See
    https://github.com/googleapis/python-bigtable/blob/main/\
    tests/unit/read-rows-acceptance-test.json
    """
    import json

    with open(filename) as json_file:
        test_json = json.load(json_file)

    for test in test_json["tests"]:
        name = test["name"]
        chunks = _generate_cell_chunks(test["chunks"])
        results = test["results"]
        yield name, chunks, results


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


def _make_cell_pb(value):
    from google.cloud.bigtable import row_data

    return row_data.Cell(value, TIMESTAMP_MICROS)


def _ReadRowsRequestPB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.ReadRowsRequest(*args, **kw)


def _read_rows_retry_exception(exc):
    from google.api_core.exceptions import DeadlineExceeded

    return isinstance(exc, DeadlineExceeded)


class _Client(object):

    data_stub = None
