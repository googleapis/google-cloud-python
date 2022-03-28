# Copyright 2015 Google LLC
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


import mock
import pytest

from ._testing import _make_credentials


def _make_client(*args, **kwargs):
    from google.cloud.bigtable.client import Client

    return Client(*args, **kwargs)


def _make_row(*args, **kwargs):
    from google.cloud.bigtable.row import Row

    return Row(*args, **kwargs)


def test_row_key_getter():
    row = _make_row(row_key=b"row_key", table="table")
    assert b"row_key" == row.row_key


def test_row_table_getter():
    row = _make_row(row_key=b"row_key", table="table")
    assert "table" == row.table


def _make__set_delete_row(*args, **kwargs):
    from google.cloud.bigtable.row import _SetDeleteRow

    return _SetDeleteRow(*args, **kwargs)


def test__set_detlete_row__get_mutations_virtual():
    row = _make__set_delete_row(b"row-key", None)
    with pytest.raises(NotImplementedError):
        row._get_mutations(None)


def _make_direct_row(*args, **kwargs):
    from google.cloud.bigtable.row import DirectRow

    return DirectRow(*args, **kwargs)


def test_direct_row_constructor():
    row_key = b"row_key"
    table = object()

    row = _make_direct_row(row_key, table)
    assert row._row_key == row_key
    assert row._table is table
    assert row._pb_mutations == []


def test_direct_row_constructor_with_unicode():
    row_key = "row_key"
    row_key_bytes = b"row_key"
    table = object()

    row = _make_direct_row(row_key, table)
    assert row._row_key == row_key_bytes
    assert row._table is table


def test_direct_row_constructor_with_non_bytes():
    row_key = object()
    with pytest.raises(TypeError):
        _make_direct_row(row_key, None)


def test_direct_row__get_mutations():
    row_key = b"row_key"
    row = _make_direct_row(row_key, None)

    row._pb_mutations = mutations = object()
    assert mutations is row._get_mutations(None)


def test_direct_row_get_mutations_size():
    row_key = b"row_key"
    row = _make_direct_row(row_key, None)

    column_family_id1 = "column_family_id1"
    column_family_id2 = "column_family_id2"
    column1 = b"column1"
    column2 = b"column2"
    number_of_bytes = 1 * 1024 * 1024
    value = b"1" * number_of_bytes

    row.set_cell(column_family_id1, column1, value)
    row.set_cell(column_family_id2, column2, value)

    total_mutations_size = 0
    for mutation in row._get_mutations():
        total_mutations_size += mutation._pb.ByteSize()

    assert row.get_mutations_size() == total_mutations_size


def _set_cell_helper(
    column=None,
    column_bytes=None,
    value=b"foobar",
    timestamp=None,
    timestamp_micros=-1,
):
    import struct

    row_key = b"row_key"
    column_family_id = "column_family_id"
    if column is None:
        column = b"column"
    table = object()
    row = _make_direct_row(row_key, table)
    assert row._pb_mutations == []
    row.set_cell(column_family_id, column, value, timestamp=timestamp)

    if isinstance(value, int):
        value = struct.pack(">q", value)
    expected_pb = _MutationPB(
        set_cell=_MutationSetCellPB(
            family_name=column_family_id,
            column_qualifier=column_bytes or column,
            timestamp_micros=timestamp_micros,
            value=value,
        )
    )
    assert row._pb_mutations == [expected_pb]


def test_direct_row_set_cell():
    _set_cell_helper()


def test_direct_row_set_cell_with_string_column():
    column_bytes = b"column"
    column_non_bytes = "column"
    _set_cell_helper(column=column_non_bytes, column_bytes=column_bytes)


def test_direct_row_set_cell_with_integer_value():
    value = 1337
    _set_cell_helper(value=value)


def test_direct_row_set_cell_with_non_bytes_value():
    row_key = b"row_key"
    column = b"column"
    column_family_id = "column_family_id"
    table = object()

    row = _make_direct_row(row_key, table)
    value = object()  # Not bytes
    with pytest.raises(TypeError):
        row.set_cell(column_family_id, column, value)


def test_direct_row_set_cell_with_non_null_timestamp():
    import datetime
    from google.cloud._helpers import _EPOCH

    microseconds = 898294371
    millis_granularity = microseconds - (microseconds % 1000)
    timestamp = _EPOCH + datetime.timedelta(microseconds=microseconds)
    _set_cell_helper(timestamp=timestamp, timestamp_micros=millis_granularity)


def test_direct_row_delete():
    row_key = b"row_key"
    row = _make_direct_row(row_key, object())
    assert row._pb_mutations == []
    row.delete()

    expected_pb = _MutationPB(delete_from_row=_MutationDeleteFromRowPB())
    assert row._pb_mutations == [expected_pb]


def test_direct_row_delete_cell():
    from google.cloud.bigtable.row import DirectRow

    class MockRow(DirectRow):
        def __init__(self, *args, **kwargs):
            super(MockRow, self).__init__(*args, **kwargs)
            self._args = []
            self._kwargs = []

        # Replace the called method with one that logs arguments.
        def _delete_cells(self, *args, **kwargs):
            self._args.append(args)
            self._kwargs.append(kwargs)

    row_key = b"row_key"
    column = b"column"
    column_family_id = "column_family_id"
    table = object()

    mock_row = MockRow(row_key, table)
    # Make sure no values are set before calling the method.
    assert mock_row._pb_mutations == []
    assert mock_row._args == []
    assert mock_row._kwargs == []

    # Actually make the request against the mock class.
    time_range = object()
    mock_row.delete_cell(column_family_id, column, time_range=time_range)
    assert mock_row._pb_mutations == []
    assert mock_row._args == [(column_family_id, [column])]
    assert mock_row._kwargs == [{"state": None, "time_range": time_range}]


def test_direct_row_delete_cells_non_iterable():
    row_key = b"row_key"
    column_family_id = "column_family_id"
    table = object()

    row = _make_direct_row(row_key, table)
    columns = object()  # Not iterable
    with pytest.raises(TypeError):
        row.delete_cells(column_family_id, columns)


def test_direct_row_delete_cells_all_columns():
    from google.cloud.bigtable.row import DirectRow

    row_key = b"row_key"
    column_family_id = "column_family_id"
    table = object()

    row = _make_direct_row(row_key, table)
    assert row._pb_mutations == []
    row.delete_cells(column_family_id, DirectRow.ALL_COLUMNS)

    expected_pb = _MutationPB(
        delete_from_family=_MutationDeleteFromFamilyPB(family_name=column_family_id)
    )
    assert row._pb_mutations == [expected_pb]


def test_direct_row_delete_cells_no_columns():
    row_key = b"row_key"
    column_family_id = "column_family_id"
    table = object()

    row = _make_direct_row(row_key, table)
    columns = []
    assert row._pb_mutations == []
    row.delete_cells(column_family_id, columns)
    assert row._pb_mutations == []


def _delete_cells_helper(time_range=None):
    row_key = b"row_key"
    column = b"column"
    column_family_id = "column_family_id"
    table = object()

    row = _make_direct_row(row_key, table)
    columns = [column]
    assert row._pb_mutations == []
    row.delete_cells(column_family_id, columns, time_range=time_range)

    expected_pb = _MutationPB(
        delete_from_column=_MutationDeleteFromColumnPB(
            family_name=column_family_id, column_qualifier=column
        )
    )
    if time_range is not None:
        expected_pb.delete_from_column.time_range._pb.CopyFrom(time_range.to_pb()._pb)
    assert row._pb_mutations == [expected_pb]


def test_direct_row_delete_cells_no_time_range():
    _delete_cells_helper()


def test_direct_row_delete_cells_with_time_range():
    import datetime
    from google.cloud._helpers import _EPOCH
    from google.cloud.bigtable.row_filters import TimestampRange

    microseconds = 30871000  # Makes sure already milliseconds granularity
    start = _EPOCH + datetime.timedelta(microseconds=microseconds)
    time_range = TimestampRange(start=start)
    _delete_cells_helper(time_range=time_range)


def test_direct_row_delete_cells_with_bad_column():
    # This makes sure a failure on one of the columns doesn't leave
    # the row's mutations in a bad state.
    row_key = b"row_key"
    column = b"column"
    column_family_id = "column_family_id"
    table = object()

    row = _make_direct_row(row_key, table)
    columns = [column, object()]
    assert row._pb_mutations == []
    with pytest.raises(TypeError):
        row.delete_cells(column_family_id, columns)
    assert row._pb_mutations == []


def test_direct_row_delete_cells_with_string_columns():
    row_key = b"row_key"
    column_family_id = "column_family_id"
    column1 = "column1"
    column1_bytes = b"column1"
    column2 = "column2"
    column2_bytes = b"column2"
    table = object()

    row = _make_direct_row(row_key, table)
    columns = [column1, column2]
    assert row._pb_mutations == []
    row.delete_cells(column_family_id, columns)

    expected_pb1 = _MutationPB(
        delete_from_column=_MutationDeleteFromColumnPB(
            family_name=column_family_id, column_qualifier=column1_bytes
        )
    )
    expected_pb2 = _MutationPB(
        delete_from_column=_MutationDeleteFromColumnPB(
            family_name=column_family_id, column_qualifier=column2_bytes
        )
    )
    assert row._pb_mutations == [expected_pb1, expected_pb2]


def test_direct_row_commit():
    project_id = "project-id"
    row_key = b"row_key"
    table_name = "projects/more-stuff"
    column_family_id = "column_family_id"
    column = b"column"

    credentials = _make_credentials()
    client = _make_client(project=project_id, credentials=credentials, admin=True)
    table = _Table(table_name, client=client)
    row = _make_direct_row(row_key, table)
    value = b"bytes-value"

    # Perform the method and check the result.
    row.set_cell(column_family_id, column, value)
    row.commit()
    assert table.mutated_rows == [row]


def test_direct_row_commit_with_exception():
    from google.rpc import status_pb2

    project_id = "project-id"
    row_key = b"row_key"
    table_name = "projects/more-stuff"
    column_family_id = "column_family_id"
    column = b"column"

    credentials = _make_credentials()
    client = _make_client(project=project_id, credentials=credentials, admin=True)
    table = _Table(table_name, client=client)
    row = _make_direct_row(row_key, table)
    value = b"bytes-value"

    # Perform the method and check the result.
    row.set_cell(column_family_id, column, value)
    result = row.commit()
    expected = status_pb2.Status(code=0)
    assert result == expected


def _make_conditional_row(*args, **kwargs):
    from google.cloud.bigtable.row import ConditionalRow

    return ConditionalRow(*args, **kwargs)


def test_conditional_row_constructor():
    row_key = b"row_key"
    table = object()
    filter_ = object()

    row = _make_conditional_row(row_key, table, filter_=filter_)
    assert row._row_key == row_key
    assert row._table is table
    assert row._filter is filter_
    assert row._true_pb_mutations == []
    assert row._false_pb_mutations == []


def test_conditional_row__get_mutations():
    row_key = b"row_key"
    filter_ = object()
    row = _make_conditional_row(row_key, None, filter_=filter_)

    row._true_pb_mutations = true_mutations = object()
    row._false_pb_mutations = false_mutations = object()
    assert true_mutations is row._get_mutations(True)
    assert false_mutations is row._get_mutations(False)
    assert false_mutations is row._get_mutations(None)


def test_conditional_row_commit():
    from google.cloud.bigtable.row_filters import RowSampleFilter
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    project_id = "project-id"
    row_key = b"row_key"
    table_name = "projects/more-stuff"
    app_profile_id = "app_profile_id"
    column_family_id1 = "column_family_id1"
    column_family_id2 = "column_family_id2"
    column_family_id3 = "column_family_id3"
    column1 = b"column1"
    column2 = b"column2"

    api = mock.create_autospec(BigtableClient)
    credentials = _make_credentials()
    client = _make_client(project=project_id, credentials=credentials, admin=True)
    table = _Table(table_name, client=client, app_profile_id=app_profile_id)
    row_filter = RowSampleFilter(0.33)
    row = _make_conditional_row(row_key, table, filter_=row_filter)

    # Create request_pb
    value1 = b"bytes-value"

    # Create response_pb
    predicate_matched = True
    response_pb = _CheckAndMutateRowResponsePB(predicate_matched=predicate_matched)

    # Patch the stub used by the API method.
    api.check_and_mutate_row.side_effect = [response_pb]
    client._table_data_client = api

    # Create expected_result.
    expected_result = predicate_matched

    # Perform the method and check the result.
    row.set_cell(column_family_id1, column1, value1, state=True)
    row.delete(state=False)
    row.delete_cell(column_family_id2, column2, state=True)
    row.delete_cells(column_family_id3, row.ALL_COLUMNS, state=True)
    result = row.commit()
    call_args = api.check_and_mutate_row.call_args
    assert app_profile_id == call_args.app_profile_id[0]
    assert result == expected_result
    assert row._true_pb_mutations == []
    assert row._false_pb_mutations == []


def test_conditional_row_commit_too_many_mutations():
    from google.cloud._testing import _Monkey
    from google.cloud.bigtable import row as MUT

    row_key = b"row_key"
    table = object()
    filter_ = object()
    row = _make_conditional_row(row_key, table, filter_=filter_)
    row._true_pb_mutations = [1, 2, 3]
    num_mutations = len(row._true_pb_mutations)
    with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
        with pytest.raises(ValueError):
            row.commit()


def test_conditional_row_commit_no_mutations():
    from tests.unit._testing import _FakeStub

    project_id = "project-id"
    row_key = b"row_key"

    credentials = _make_credentials()
    client = _make_client(project=project_id, credentials=credentials, admin=True)
    table = _Table(None, client=client)
    filter_ = object()
    row = _make_conditional_row(row_key, table, filter_=filter_)
    assert row._true_pb_mutations == []
    assert row._false_pb_mutations == []

    # Patch the stub used by the API method.
    stub = _FakeStub()

    # Perform the method and check the result.
    result = row.commit()
    assert result is None
    # Make sure no request was sent.
    assert stub.method_calls == []


def _make_append_row(*args, **kwargs):
    from google.cloud.bigtable.row import AppendRow

    return AppendRow(*args, **kwargs)


def test_append_row_constructor():
    row_key = b"row_key"
    table = object()

    row = _make_append_row(row_key, table)
    assert row._row_key == row_key
    assert row._table is table
    assert row._rule_pb_list == []


def test_append_row_clear():
    row_key = b"row_key"
    table = object()
    row = _make_append_row(row_key, table)
    row._rule_pb_list = [1, 2, 3]
    row.clear()
    assert row._rule_pb_list == []


def test_append_row_append_cell_value():
    table = object()
    row_key = b"row_key"
    row = _make_append_row(row_key, table)
    assert row._rule_pb_list == []

    column = b"column"
    column_family_id = "column_family_id"
    value = b"bytes-val"
    row.append_cell_value(column_family_id, column, value)
    expected_pb = _ReadModifyWriteRulePB(
        family_name=column_family_id, column_qualifier=column, append_value=value
    )
    assert row._rule_pb_list == [expected_pb]


def test_append_row_increment_cell_value():
    table = object()
    row_key = b"row_key"
    row = _make_append_row(row_key, table)
    assert row._rule_pb_list == []

    column = b"column"
    column_family_id = "column_family_id"
    int_value = 281330
    row.increment_cell_value(column_family_id, column, int_value)
    expected_pb = _ReadModifyWriteRulePB(
        family_name=column_family_id,
        column_qualifier=column,
        increment_amount=int_value,
    )
    assert row._rule_pb_list == [expected_pb]


def test_append_row_commit():
    from google.cloud._testing import _Monkey
    from google.cloud.bigtable import row as MUT
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    project_id = "project-id"
    row_key = b"row_key"
    table_name = "projects/more-stuff"
    app_profile_id = "app_profile_id"
    column_family_id = "column_family_id"
    column = b"column"

    api = mock.create_autospec(BigtableClient)

    credentials = _make_credentials()
    client = _make_client(project=project_id, credentials=credentials, admin=True)
    table = _Table(table_name, client=client, app_profile_id=app_profile_id)
    row = _make_append_row(row_key, table)

    # Create request_pb
    value = b"bytes-value"

    # Create expected_result.
    row_responses = []
    expected_result = object()

    # Patch API calls
    client._table_data_client = api

    def mock_parse_rmw_row_response(row_response):
        row_responses.append(row_response)
        return expected_result

    # Perform the method and check the result.
    with _Monkey(MUT, _parse_rmw_row_response=mock_parse_rmw_row_response):
        row._table._instance._client._table_data_client = api
        row.append_cell_value(column_family_id, column, value)
        result = row.commit()
    call_args = api.read_modify_write_row.call_args_list[0]
    assert app_profile_id == call_args.app_profile_id[0]
    assert result == expected_result
    assert row._rule_pb_list == []


def test_append_row_commit_no_rules():
    from tests.unit._testing import _FakeStub

    project_id = "project-id"
    row_key = b"row_key"

    credentials = _make_credentials()
    client = _make_client(project=project_id, credentials=credentials, admin=True)
    table = _Table(None, client=client)
    row = _make_append_row(row_key, table)
    assert row._rule_pb_list == []

    # Patch the stub used by the API method.
    stub = _FakeStub()

    # Perform the method and check the result.
    result = row.commit()
    assert result == {}
    # Make sure no request was sent.
    assert stub.method_calls == []


def test_append_row_commit_too_many_mutations():
    from google.cloud._testing import _Monkey
    from google.cloud.bigtable import row as MUT

    row_key = b"row_key"
    table = object()
    row = _make_append_row(row_key, table)
    row._rule_pb_list = [1, 2, 3]
    num_mutations = len(row._rule_pb_list)
    with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
        with pytest.raises(ValueError):
            row.commit()


def test__parse_rmw_row_response():
    from google.cloud._helpers import _datetime_from_microseconds
    from google.cloud.bigtable.row import _parse_rmw_row_response

    col_fam1 = "col-fam-id"
    col_fam2 = "col-fam-id2"
    col_name1 = b"col-name1"
    col_name2 = b"col-name2"
    col_name3 = b"col-name3-but-other-fam"
    cell_val1 = b"cell-val"
    cell_val2 = b"cell-val-newer"
    cell_val3 = b"altcol-cell-val"
    cell_val4 = b"foo"

    microseconds = 1000871
    timestamp = _datetime_from_microseconds(microseconds)
    expected_output = {
        col_fam1: {
            col_name1: [(cell_val1, timestamp), (cell_val2, timestamp)],
            col_name2: [(cell_val3, timestamp)],
        },
        col_fam2: {col_name3: [(cell_val4, timestamp)]},
    }
    response_row = _RowPB(
        families=[
            _FamilyPB(
                name=col_fam1,
                columns=[
                    _ColumnPB(
                        qualifier=col_name1,
                        cells=[
                            _CellPB(value=cell_val1, timestamp_micros=microseconds),
                            _CellPB(value=cell_val2, timestamp_micros=microseconds),
                        ],
                    ),
                    _ColumnPB(
                        qualifier=col_name2,
                        cells=[_CellPB(value=cell_val3, timestamp_micros=microseconds)],
                    ),
                ],
            ),
            _FamilyPB(
                name=col_fam2,
                columns=[
                    _ColumnPB(
                        qualifier=col_name3,
                        cells=[_CellPB(value=cell_val4, timestamp_micros=microseconds)],
                    )
                ],
            ),
        ]
    )
    sample_input = _ReadModifyWriteRowResponsePB(row=response_row)
    assert expected_output == _parse_rmw_row_response(sample_input)


def test__parse_family_pb():
    from google.cloud._helpers import _datetime_from_microseconds
    from google.cloud.bigtable.row import _parse_family_pb

    col_fam1 = "col-fam-id"
    col_name1 = b"col-name1"
    col_name2 = b"col-name2"
    cell_val1 = b"cell-val"
    cell_val2 = b"cell-val-newer"
    cell_val3 = b"altcol-cell-val"

    microseconds = 5554441037
    timestamp = _datetime_from_microseconds(microseconds)
    expected_dict = {
        col_name1: [(cell_val1, timestamp), (cell_val2, timestamp)],
        col_name2: [(cell_val3, timestamp)],
    }
    expected_output = (col_fam1, expected_dict)
    sample_input = _FamilyPB(
        name=col_fam1,
        columns=[
            _ColumnPB(
                qualifier=col_name1,
                cells=[
                    _CellPB(value=cell_val1, timestamp_micros=microseconds),
                    _CellPB(value=cell_val2, timestamp_micros=microseconds),
                ],
            ),
            _ColumnPB(
                qualifier=col_name2,
                cells=[_CellPB(value=cell_val3, timestamp_micros=microseconds)],
            ),
        ],
    )
    assert expected_output == _parse_family_pb(sample_input)


def _CheckAndMutateRowResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.CheckAndMutateRowResponse(*args, **kw)


def _ReadModifyWriteRowResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.ReadModifyWriteRowResponse(*args, **kw)


def _CellPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Cell(*args, **kw)


def _ColumnPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Column(*args, **kw)


def _FamilyPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Family(*args, **kw)


def _MutationPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Mutation(*args, **kw)


def _MutationSetCellPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Mutation.SetCell(*args, **kw)


def _MutationDeleteFromColumnPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Mutation.DeleteFromColumn(*args, **kw)


def _MutationDeleteFromFamilyPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Mutation.DeleteFromFamily(*args, **kw)


def _MutationDeleteFromRowPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Mutation.DeleteFromRow(*args, **kw)


def _RowPB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.Row(*args, **kw)


def _ReadModifyWriteRulePB(*args, **kw):
    from google.cloud.bigtable_v2.types import data as data_v2_pb2

    return data_v2_pb2.ReadModifyWriteRule(*args, **kw)


class _Instance(object):
    def __init__(self, client=None):
        self._client = client


class _Table(object):
    def __init__(self, name, client=None, app_profile_id=None):
        self.name = name
        self._instance = _Instance(client)
        self._app_profile_id = app_profile_id
        self.client = client
        self.mutated_rows = []

    def mutate_rows(self, rows):
        from google.rpc import status_pb2

        self.mutated_rows.extend(rows)
        return [status_pb2.Status(code=0)]
