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


import warnings

import mock
import pytest
from grpc import StatusCode

from google.api_core.exceptions import DeadlineExceeded
from ._testing import _make_credentials

PROJECT_ID = "project-id"
INSTANCE_ID = "instance-id"
INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
CLUSTER_ID = "cluster-id"
CLUSTER_NAME = INSTANCE_NAME + "/clusters/" + CLUSTER_ID
TABLE_ID = "table-id"
TABLE_NAME = INSTANCE_NAME + "/tables/" + TABLE_ID
BACKUP_ID = "backup-id"
BACKUP_NAME = CLUSTER_NAME + "/backups/" + BACKUP_ID
ROW_KEY = b"row-key"
ROW_KEY_1 = b"row-key-1"
ROW_KEY_2 = b"row-key-2"
ROW_KEY_3 = b"row-key-3"
FAMILY_NAME = "family"
QUALIFIER = b"qualifier"
TIMESTAMP_MICROS = 100
VALUE = b"value"

# RPC Status Codes
SUCCESS = StatusCode.OK.value[0]
RETRYABLE_1 = StatusCode.DEADLINE_EXCEEDED.value[0]
RETRYABLE_2 = StatusCode.ABORTED.value[0]
RETRYABLE_3 = StatusCode.UNAVAILABLE.value[0]
RETRYABLES = (RETRYABLE_1, RETRYABLE_2, RETRYABLE_3)
NON_RETRYABLE = StatusCode.CANCELLED.value[0]


@mock.patch("google.cloud.bigtable.table._MAX_BULK_MUTATIONS", new=3)
def test__compile_mutation_entries_w_too_many_mutations():
    from google.cloud.bigtable.row import DirectRow
    from google.cloud.bigtable.table import TooManyMutationsError
    from google.cloud.bigtable.table import _compile_mutation_entries

    table = mock.Mock(name="table", spec=["name"])
    table.name = "table"
    rows = [
        DirectRow(row_key=b"row_key", table=table),
        DirectRow(row_key=b"row_key_2", table=table),
    ]
    rows[0].set_cell("cf1", b"c1", 1)
    rows[0].set_cell("cf1", b"c1", 2)
    rows[1].set_cell("cf1", b"c1", 3)
    rows[1].set_cell("cf1", b"c1", 4)

    with pytest.raises(TooManyMutationsError):
        _compile_mutation_entries("table", rows)


def test__compile_mutation_entries_normal():
    from google.cloud.bigtable.row import DirectRow
    from google.cloud.bigtable.table import _compile_mutation_entries
    from google.cloud.bigtable_v2.types import MutateRowsRequest
    from google.cloud.bigtable_v2.types import data

    table = mock.Mock(spec=["name"])
    table.name = "table"
    rows = [
        DirectRow(row_key=b"row_key", table=table),
        DirectRow(row_key=b"row_key_2"),
    ]
    rows[0].set_cell("cf1", b"c1", b"1")
    rows[1].set_cell("cf1", b"c1", b"2")

    result = _compile_mutation_entries("table", rows)

    entry_1 = MutateRowsRequest.Entry()
    entry_1.row_key = b"row_key"
    mutations_1 = data.Mutation()
    mutations_1.set_cell.family_name = "cf1"
    mutations_1.set_cell.column_qualifier = b"c1"
    mutations_1.set_cell.timestamp_micros = -1
    mutations_1.set_cell.value = b"1"
    entry_1.mutations.append(mutations_1)

    entry_2 = MutateRowsRequest.Entry()
    entry_2.row_key = b"row_key_2"
    mutations_2 = data.Mutation()
    mutations_2.set_cell.family_name = "cf1"
    mutations_2.set_cell.column_qualifier = b"c1"
    mutations_2.set_cell.timestamp_micros = -1
    mutations_2.set_cell.value = b"2"
    entry_2.mutations.append(mutations_2)
    assert result == [entry_1, entry_2]


def test__check_row_table_name_w_wrong_table_name():
    from google.cloud.bigtable.table import _check_row_table_name
    from google.cloud.bigtable.table import TableMismatchError
    from google.cloud.bigtable.row import DirectRow

    table = mock.Mock(name="table", spec=["name"])
    table.name = "table"
    row = DirectRow(row_key=b"row_key", table=table)

    with pytest.raises(TableMismatchError):
        _check_row_table_name("other_table", row)


def test__check_row_table_name_w_right_table_name():
    from google.cloud.bigtable.row import DirectRow
    from google.cloud.bigtable.table import _check_row_table_name

    table = mock.Mock(name="table", spec=["name"])
    table.name = "table"
    row = DirectRow(row_key=b"row_key", table=table)

    assert not _check_row_table_name("table", row)


def test__check_row_type_w_wrong_row_type():
    from google.cloud.bigtable.row import ConditionalRow
    from google.cloud.bigtable.table import _check_row_type

    row = ConditionalRow(row_key=b"row_key", table="table", filter_=None)
    with pytest.raises(TypeError):
        _check_row_type(row)


def test__check_row_type_w_right_row_type():
    from google.cloud.bigtable.row import DirectRow
    from google.cloud.bigtable.table import _check_row_type

    row = DirectRow(row_key=b"row_key", table="table")
    assert not _check_row_type(row)


def _make_client(*args, **kwargs):
    from google.cloud.bigtable.client import Client

    return Client(*args, **kwargs)


def _make_table(*args, **kwargs):
    from google.cloud.bigtable.table import Table

    return Table(*args, **kwargs)


def test_table_constructor_defaults():
    instance = mock.Mock(spec=[])

    table = _make_table(TABLE_ID, instance)

    assert table.table_id == TABLE_ID
    assert table._instance is instance
    assert table.mutation_timeout is None
    assert table._app_profile_id is None


def test_table_constructor_explicit():
    instance = mock.Mock(spec=[])
    mutation_timeout = 123
    app_profile_id = "profile-123"

    table = _make_table(
        TABLE_ID,
        instance,
        mutation_timeout=mutation_timeout,
        app_profile_id=app_profile_id,
    )

    assert table.table_id == TABLE_ID
    assert table._instance is instance
    assert table.mutation_timeout == mutation_timeout
    assert table._app_profile_id == app_profile_id


def test_table_name():
    table_data_client = mock.Mock(spec=["table_path"])
    client = mock.Mock(
        project=PROJECT_ID,
        table_data_client=table_data_client,
        spec=["project", "table_data_client"],
    )
    instance = mock.Mock(
        _client=client,
        instance_id=INSTANCE_ID,
        spec=["_client", "instance_id"],
    )

    table = _make_table(TABLE_ID, instance)

    assert table.name == table_data_client.table_path.return_value


def _table_row_methods_helper():
    client = _make_client(
        project="project-id", credentials=_make_credentials(), admin=True
    )
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    row_key = b"row_key"
    return table, row_key


def test_table_row_factory_direct():
    from google.cloud.bigtable.row import DirectRow

    table, row_key = _table_row_methods_helper()
    with warnings.catch_warnings(record=True) as warned:
        row = table.row(row_key)

    assert isinstance(row, DirectRow)
    assert row._row_key == row_key
    assert row._table == table

    assert len(warned) == 1
    assert warned[0].category is PendingDeprecationWarning


def test_table_row_factory_conditional():
    from google.cloud.bigtable.row import ConditionalRow

    table, row_key = _table_row_methods_helper()
    filter_ = object()

    with warnings.catch_warnings(record=True) as warned:
        row = table.row(row_key, filter_=filter_)

    assert isinstance(row, ConditionalRow)
    assert row._row_key == row_key
    assert row._table == table

    assert len(warned) == 1
    assert warned[0].category is PendingDeprecationWarning


def test_table_row_factory_append():
    from google.cloud.bigtable.row import AppendRow

    table, row_key = _table_row_methods_helper()

    with warnings.catch_warnings(record=True) as warned:
        row = table.row(row_key, append=True)

    assert isinstance(row, AppendRow)
    assert row._row_key == row_key
    assert row._table == table

    assert len(warned) == 1
    assert warned[0].category is PendingDeprecationWarning


def test_table_row_factory_failure():
    table, row_key = _table_row_methods_helper()

    with pytest.raises(ValueError):
        with warnings.catch_warnings(record=True) as warned:
            table.row(row_key, filter_=object(), append=True)

    assert len(warned) == 1
    assert warned[0].category is PendingDeprecationWarning


def test_table_direct_row():
    from google.cloud.bigtable.row import DirectRow

    table, row_key = _table_row_methods_helper()
    row = table.direct_row(row_key)

    assert isinstance(row, DirectRow)
    assert row._row_key == row_key
    assert row._table == table


def test_table_conditional_row():
    from google.cloud.bigtable.row import ConditionalRow

    table, row_key = _table_row_methods_helper()
    filter_ = object()
    row = table.conditional_row(row_key, filter_=filter_)

    assert isinstance(row, ConditionalRow)
    assert row._row_key == row_key
    assert row._table == table


def test_table_append_row():
    from google.cloud.bigtable.row import AppendRow

    table, row_key = _table_row_methods_helper()
    row = table.append_row(row_key)

    assert isinstance(row, AppendRow)
    assert row._row_key == row_key
    assert row._table == table


def test_table___eq__():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table1 = _make_table(TABLE_ID, instance)
    table2 = _make_table(TABLE_ID, instance)
    assert table1 == table2


def test_table___eq__type_differ():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table1 = _make_table(TABLE_ID, instance)
    table2 = object()
    assert not (table1 == table2)


def test_table___ne__same_value():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table1 = _make_table(TABLE_ID, instance)
    table2 = _make_table(TABLE_ID, instance)
    assert not (table1 != table2)


def test_table___ne__():
    table1 = _make_table("table_id1", None)
    table2 = _make_table("table_id2", None)
    assert table1 != table2


def _make_table_api():
    from google.cloud.bigtable_admin_v2.services.bigtable_table_admin import (
        client as bigtable_table_admin,
    )

    return mock.create_autospec(bigtable_table_admin.BigtableTableAdminClient)


def _create_table_helper(split_keys=[], column_families={}):
    from google.cloud.bigtable_admin_v2.types import table as table_pb2
    from google.cloud.bigtable_admin_v2.types import (
        bigtable_table_admin as table_admin_messages_v2_pb2,
    )
    from google.cloud.bigtable.column_family import ColumnFamily

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    table_api = client._table_admin_client = _make_table_api()

    table.create(column_families=column_families, initial_split_keys=split_keys)

    families = {
        id: ColumnFamily(id, table, rule).to_pb()
        for (id, rule) in column_families.items()
    }

    split = table_admin_messages_v2_pb2.CreateTableRequest.Split
    splits = [split(key=split_key) for split_key in split_keys]

    table_api.create_table.assert_called_once_with(
        request={
            "parent": INSTANCE_NAME,
            "table": table_pb2.Table(column_families=families),
            "table_id": TABLE_ID,
            "initial_splits": splits,
        }
    )


def test_table_create():
    _create_table_helper()


def test_table_create_with_families():
    from google.cloud.bigtable.column_family import MaxVersionsGCRule

    families = {"family": MaxVersionsGCRule(5)}
    _create_table_helper(column_families=families)


def test_table_create_with_split_keys():
    _create_table_helper(split_keys=[b"split1", b"split2", b"split3"])


def test_table_exists_hit():
    from google.cloud.bigtable_admin_v2.types import ListTablesResponse
    from google.cloud.bigtable_admin_v2.types import Table
    from google.cloud.bigtable import enums

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = instance.table(TABLE_ID)

    response_pb = ListTablesResponse(tables=[Table(name=TABLE_NAME)])
    table_api = client._table_admin_client = _make_table_api()
    table_api.get_table.return_value = response_pb

    assert table.exists()

    expected_request = {
        "name": table.name,
        "view": enums.Table.View.NAME_ONLY,
    }
    table_api.get_table.assert_called_once_with(request=expected_request)


def test_table_exists_miss():
    from google.api_core.exceptions import NotFound
    from google.cloud.bigtable import enums

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = instance.table("nonesuch-table-id2")

    table_api = client._table_admin_client = _make_table_api()
    table_api.get_table.side_effect = NotFound("testing")

    assert not table.exists()

    expected_request = {
        "name": table.name,
        "view": enums.Table.View.NAME_ONLY,
    }
    table_api.get_table.assert_called_once_with(request=expected_request)


def test_table_exists_error():
    from google.api_core.exceptions import BadRequest
    from google.cloud.bigtable import enums

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)

    table_api = client._table_admin_client = _make_table_api()
    table_api.get_table.side_effect = BadRequest("testing")

    table = instance.table(TABLE_ID)

    with pytest.raises(BadRequest):
        table.exists()

    expected_request = {
        "name": table.name,
        "view": enums.Table.View.NAME_ONLY,
    }
    table_api.get_table.assert_called_once_with(request=expected_request)


def test_table_delete():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    table_api = client._table_admin_client = _make_table_api()

    assert table.delete() is None

    table_api.delete_table.assert_called_once_with(request={"name": table.name})


def _table_list_column_families_helper():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    # Create response_pb
    COLUMN_FAMILY_ID = "foo"
    column_family = _ColumnFamilyPB()
    response_pb = _TablePB(column_families={COLUMN_FAMILY_ID: column_family})

    # Patch the stub used by the API method.
    table_api = client._table_admin_client = _make_table_api()
    table_api.get_table.return_value = response_pb

    # Create expected_result.
    expected_result = {COLUMN_FAMILY_ID: table.column_family(COLUMN_FAMILY_ID)}

    # Perform the method and check the result.
    result = table.list_column_families()

    assert result == expected_result

    table_api.get_table.assert_called_once_with(request={"name": table.name})


def test_table_list_column_families():
    _table_list_column_families_helper()


def test_table_get_cluster_states():
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.table import ClusterState

    INITIALIZING = enum_table.ReplicationState.INITIALIZING
    PLANNED_MAINTENANCE = enum_table.ReplicationState.PLANNED_MAINTENANCE
    READY = enum_table.ReplicationState.READY

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    response_pb = _TablePB(
        cluster_states={
            "cluster-id1": _ClusterStatePB(INITIALIZING),
            "cluster-id2": _ClusterStatePB(PLANNED_MAINTENANCE),
            "cluster-id3": _ClusterStatePB(READY),
        }
    )

    # Patch the stub used by the API method.
    table_api = client._table_admin_client = _make_table_api()
    table_api.get_table.return_value = response_pb

    # build expected result
    expected_result = {
        "cluster-id1": ClusterState(INITIALIZING),
        "cluster-id2": ClusterState(PLANNED_MAINTENANCE),
        "cluster-id3": ClusterState(READY),
    }

    # Perform the method and check the result.
    result = table.get_cluster_states()

    assert result == expected_result

    expected_request = {
        "name": table.name,
        "view": enum_table.View.REPLICATION_VIEW,
    }
    table_api.get_table.assert_called_once_with(request=expected_request)


def test_table_get_encryption_info():
    from google.rpc.code_pb2 import Code
    from google.cloud.bigtable.encryption_info import EncryptionInfo
    from google.cloud.bigtable.enums import EncryptionInfo as enum_crypto
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.error import Status

    ENCRYPTION_TYPE_UNSPECIFIED = enum_crypto.EncryptionType.ENCRYPTION_TYPE_UNSPECIFIED
    GOOGLE_DEFAULT_ENCRYPTION = enum_crypto.EncryptionType.GOOGLE_DEFAULT_ENCRYPTION
    CUSTOMER_MANAGED_ENCRYPTION = enum_crypto.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    response_pb = _TablePB(
        cluster_states={
            "cluster-id1": _ClusterStateEncryptionInfoPB(
                encryption_type=ENCRYPTION_TYPE_UNSPECIFIED,
                encryption_status=_StatusPB(Code.OK, "Status OK"),
            ),
            "cluster-id2": _ClusterStateEncryptionInfoPB(
                encryption_type=GOOGLE_DEFAULT_ENCRYPTION,
            ),
            "cluster-id3": _ClusterStateEncryptionInfoPB(
                encryption_type=CUSTOMER_MANAGED_ENCRYPTION,
                encryption_status=_StatusPB(
                    Code.UNKNOWN, "Key version is not yet known."
                ),
                kms_key_version="UNKNOWN",
            ),
        }
    )

    # Patch the stub used by the API method.
    table_api = client._table_admin_client = _make_table_api()
    table_api.get_table.return_value = response_pb

    # build expected result
    expected_result = {
        "cluster-id1": (
            EncryptionInfo(
                encryption_type=ENCRYPTION_TYPE_UNSPECIFIED,
                encryption_status=Status(_StatusPB(Code.OK, "Status OK")),
                kms_key_version="",
            ),
        ),
        "cluster-id2": (
            EncryptionInfo(
                encryption_type=GOOGLE_DEFAULT_ENCRYPTION,
                encryption_status=Status(_StatusPB(0, "")),
                kms_key_version="",
            ),
        ),
        "cluster-id3": (
            EncryptionInfo(
                encryption_type=CUSTOMER_MANAGED_ENCRYPTION,
                encryption_status=Status(
                    _StatusPB(Code.UNKNOWN, "Key version is not yet known.")
                ),
                kms_key_version="UNKNOWN",
            ),
        ),
    }

    # Perform the method and check the result.
    result = table.get_encryption_info()

    assert result == expected_result
    expected_request = {
        "name": table.name,
        "view": enum_table.View.ENCRYPTION_VIEW,
    }
    table_api.get_table.assert_called_once_with(request=expected_request)


def _make_data_api():
    from google.cloud.bigtable_v2.services.bigtable import BigtableClient

    return mock.create_autospec(BigtableClient)


def _table_read_row_helper(chunks, expected_result, app_profile_id=None):
    from google.cloud._testing import _Monkey
    from google.cloud.bigtable import table as MUT
    from google.cloud.bigtable.row_set import RowSet
    from google.cloud.bigtable.row_filters import RowSampleFilter

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance, app_profile_id=app_profile_id)

    # Create request_pb
    request_pb = object()  # Returned by our mock.
    mock_created = []

    def mock_create_row_request(table_name, **kwargs):
        mock_created.append((table_name, kwargs))
        return request_pb

    # Create response_iterator
    if chunks is None:
        response_iterator = iter(())  # no responses at all
    else:
        response_pb = _ReadRowsResponsePB(chunks=chunks)
        response_iterator = iter([response_pb])

    data_api = client._table_data_client = _make_data_api()
    data_api.read_rows.return_value = response_iterator

    filter_obj = RowSampleFilter(0.33)

    with _Monkey(MUT, _create_row_request=mock_create_row_request):
        result = table.read_row(ROW_KEY, filter_=filter_obj)

    row_set = RowSet()
    row_set.add_row_key(ROW_KEY)
    expected_request = [
        (
            table.name,
            {
                "end_inclusive": False,
                "row_set": row_set,
                "app_profile_id": app_profile_id,
                "end_key": None,
                "limit": None,
                "start_key": None,
                "filter_": filter_obj,
            },
        )
    ]
    assert result == expected_result
    assert mock_created == expected_request

    data_api.read_rows.assert_called_once_with(request_pb, timeout=61.0)


def test_table_read_row_miss_no__responses():
    _table_read_row_helper(None, None)


def test_table_read_row_miss_no_chunks_in_response():
    chunks = []
    _table_read_row_helper(chunks, None)


def test_table_read_row_complete():
    from google.cloud.bigtable.row_data import Cell
    from google.cloud.bigtable.row_data import PartialRowData

    app_profile_id = "app-profile-id"
    chunk = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )
    chunks = [chunk]
    expected_result = PartialRowData(row_key=ROW_KEY)
    family = expected_result._cells.setdefault(FAMILY_NAME, {})
    column = family.setdefault(QUALIFIER, [])
    column.append(Cell.from_pb(chunk))

    _table_read_row_helper(chunks, expected_result, app_profile_id)


def test_table_read_row_more_than_one_row_returned():
    app_profile_id = "app-profile-id"
    chunk_1 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )._pb
    chunk_2 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_2,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )._pb

    chunks = [chunk_1, chunk_2]

    with pytest.raises(ValueError):
        _table_read_row_helper(chunks, None, app_profile_id)


def test_table_read_row_still_partial():
    chunk = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
    )
    chunks = [chunk]  # No "commit row".

    with pytest.raises(ValueError):
        _table_read_row_helper(chunks, None)


def _table_mutate_rows_helper(
    mutation_timeout=None, app_profile_id=None, retry=None, timeout=None
):
    from google.rpc.status_pb2 import Status
    from google.cloud.bigtable.table import DEFAULT_RETRY

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    ctor_kwargs = {}

    if mutation_timeout is not None:
        ctor_kwargs["mutation_timeout"] = mutation_timeout

    if app_profile_id is not None:
        ctor_kwargs["app_profile_id"] = app_profile_id

    table = _make_table(TABLE_ID, instance, **ctor_kwargs)

    rows = [mock.MagicMock(), mock.MagicMock()]
    response = [Status(code=0), Status(code=1)]
    instance_mock = mock.Mock(return_value=response)
    klass_mock = mock.patch(
        "google.cloud.bigtable.table._RetryableMutateRowsWorker",
        new=mock.MagicMock(return_value=instance_mock),
    )

    call_kwargs = {}

    if retry is not None:
        call_kwargs["retry"] = retry

    if timeout is not None:
        expected_timeout = call_kwargs["timeout"] = timeout
    else:
        expected_timeout = mutation_timeout

    with klass_mock:
        statuses = table.mutate_rows(rows, **call_kwargs)

    result = [status.code for status in statuses]
    expected_result = [0, 1]
    assert result == expected_result

    klass_mock.new.assert_called_once_with(
        client,
        TABLE_NAME,
        rows,
        app_profile_id=app_profile_id,
        timeout=expected_timeout,
    )

    if retry is not None:
        instance_mock.assert_called_once_with(retry=retry)
    else:
        instance_mock.assert_called_once_with(retry=DEFAULT_RETRY)


def test_table_mutate_rows_w_default_mutation_timeout_app_profile_id():
    _table_mutate_rows_helper()


def test_table_mutate_rows_w_mutation_timeout():
    mutation_timeout = 123
    _table_mutate_rows_helper(mutation_timeout=mutation_timeout)


def test_table_mutate_rows_w_app_profile_id():
    app_profile_id = "profile-123"
    _table_mutate_rows_helper(app_profile_id=app_profile_id)


def test_table_mutate_rows_w_retry():
    retry = mock.Mock()
    _table_mutate_rows_helper(retry=retry)


def test_table_mutate_rows_w_timeout_arg():
    timeout = 123
    _table_mutate_rows_helper(timeout=timeout)


def test_table_mutate_rows_w_mutation_timeout_and_timeout_arg():
    mutation_timeout = 123
    timeout = 456
    _table_mutate_rows_helper(mutation_timeout=mutation_timeout, timeout=timeout)


def test_table_read_rows():
    from google.cloud._testing import _Monkey
    from google.cloud.bigtable.row_data import PartialRowsData
    from google.cloud.bigtable import table as MUT
    from google.cloud.bigtable.row_data import DEFAULT_RETRY_READ_ROWS

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    data_api = client._table_data_client = _make_data_api()
    instance = client.instance(instance_id=INSTANCE_ID)
    app_profile_id = "app-profile-id"
    table = _make_table(TABLE_ID, instance, app_profile_id=app_profile_id)

    # Create request_pb
    request_pb = object()  # Returned by our mock.
    retry = DEFAULT_RETRY_READ_ROWS
    mock_created = []

    def mock_create_row_request(table_name, **kwargs):
        mock_created.append((table_name, kwargs))
        return request_pb

    # Create expected_result.
    expected_result = PartialRowsData(
        client._table_data_client.transport.read_rows, request_pb, retry
    )

    # Perform the method and check the result.
    start_key = b"start-key"
    end_key = b"end-key"
    filter_obj = object()
    limit = 22
    with _Monkey(MUT, _create_row_request=mock_create_row_request):
        result = table.read_rows(
            start_key=start_key,
            end_key=end_key,
            filter_=filter_obj,
            limit=limit,
            retry=retry,
        )

    assert result.rows == expected_result.rows
    assert result.retry == expected_result.retry
    created_kwargs = {
        "start_key": start_key,
        "end_key": end_key,
        "filter_": filter_obj,
        "limit": limit,
        "end_inclusive": False,
        "app_profile_id": app_profile_id,
        "row_set": None,
    }
    assert mock_created == [(table.name, created_kwargs)]

    data_api.read_rows.assert_called_once_with(request_pb, timeout=61.0)


def test_table_read_retry_rows():
    from google.api_core import retry
    from google.cloud.bigtable.table import _create_row_request

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    data_api = client._table_data_client = _make_data_api()
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    retry_read_rows = retry.Retry(predicate=_read_rows_retry_exception)

    # Create response_iterator
    chunk_1 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_1,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    chunk_2 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_2,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    response_1 = _ReadRowsResponseV2([chunk_1])
    response_2 = _ReadRowsResponseV2([chunk_2])
    response_failure_iterator_1 = _MockFailureIterator_1()
    response_failure_iterator_2 = _MockFailureIterator_2([response_1])
    response_iterator = _MockReadRowsIterator(response_2)

    data_api.table_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/tables/{TABLE_ID}"
    )

    data_api.read_rows.side_effect = [
        response_failure_iterator_1,
        response_failure_iterator_2,
        response_iterator,
    ]

    rows = [
        row
        for row in table.read_rows(
            start_key=ROW_KEY_1, end_key=ROW_KEY_2, retry=retry_read_rows
        )
    ]

    result = rows[1]
    assert result.row_key == ROW_KEY_2

    expected_request = _create_row_request(
        table.name,
        start_key=ROW_KEY_1,
        end_key=ROW_KEY_2,
    )
    data_api.read_rows.mock_calls = [expected_request] * 3


def test_table_yield_retry_rows():
    from google.cloud.bigtable.table import _create_row_request

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    # Create response_iterator
    chunk_1 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_1,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    chunk_2 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_2,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    response_1 = _ReadRowsResponseV2([chunk_1])
    response_2 = _ReadRowsResponseV2([chunk_2])
    response_failure_iterator_1 = _MockFailureIterator_1()
    response_failure_iterator_2 = _MockFailureIterator_2([response_1])
    response_iterator = _MockReadRowsIterator(response_2)

    data_api = client._table_data_client = _make_data_api()
    data_api.table_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/tables/{TABLE_ID}"
    )
    data_api.read_rows.side_effect = [
        response_failure_iterator_1,
        response_failure_iterator_2,
        response_iterator,
    ]

    rows = []
    with warnings.catch_warnings(record=True) as warned:
        for row in table.yield_rows(start_key=ROW_KEY_1, end_key=ROW_KEY_2):
            rows.append(row)

    assert len(warned) == 1
    assert warned[0].category is DeprecationWarning

    result = rows[1]
    assert result.row_key == ROW_KEY_2

    expected_request = _create_row_request(
        table.name,
        start_key=ROW_KEY_1,
        end_key=ROW_KEY_2,
    )
    data_api.read_rows.mock_calls = [expected_request] * 3


def test_table_yield_rows_with_row_set():
    from google.cloud.bigtable.row_set import RowSet
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.table import _create_row_request

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    # Create response_iterator
    chunk_1 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_1,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    chunk_2 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_2,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    chunk_3 = _ReadRowsResponseCellChunkPB(
        row_key=ROW_KEY_3,
        family_name=FAMILY_NAME,
        qualifier=QUALIFIER,
        timestamp_micros=TIMESTAMP_MICROS,
        value=VALUE,
        commit_row=True,
    )

    response_1 = _ReadRowsResponseV2([chunk_1])
    response_2 = _ReadRowsResponseV2([chunk_2])
    response_3 = _ReadRowsResponseV2([chunk_3])
    response_iterator = _MockReadRowsIterator(response_1, response_2, response_3)

    data_api = client._table_data_client = _make_data_api()
    data_api.table_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/tables/{TABLE_ID}"
    )
    data_api.read_rows.side_effect = [response_iterator]

    rows = []
    row_set = RowSet()
    row_set.add_row_range(RowRange(start_key=ROW_KEY_1, end_key=ROW_KEY_2))
    row_set.add_row_key(ROW_KEY_3)

    with warnings.catch_warnings(record=True) as warned:
        for row in table.yield_rows(row_set=row_set):
            rows.append(row)

    assert len(warned) == 1
    assert warned[0].category is DeprecationWarning

    assert rows[0].row_key == ROW_KEY_1
    assert rows[1].row_key == ROW_KEY_2
    assert rows[2].row_key == ROW_KEY_3

    expected_request = _create_row_request(
        table.name,
        start_key=ROW_KEY_1,
        end_key=ROW_KEY_2,
    )
    expected_request.rows.row_keys.append(ROW_KEY_3)
    data_api.read_rows.assert_called_once_with(expected_request, timeout=61.0)


def test_table_sample_row_keys():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    response_iterator = object()

    data_api = client._table_data_client = _make_data_api()
    data_api.sample_row_keys.return_value = [response_iterator]

    result = table.sample_row_keys()

    assert result[0] == response_iterator


def test_table_truncate():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    table_api = client._table_admin_client = _make_table_api()

    with mock.patch("google.cloud.bigtable.table.Table.name", new=TABLE_NAME):
        result = table.truncate()

    assert result is None

    table_api.drop_row_range.assert_called_once_with(
        request={"name": TABLE_NAME, "delete_all_data_from_table": True}
    )


def test_table_truncate_w_timeout():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    table_api = client._table_admin_client = _make_table_api()

    timeout = 120
    result = table.truncate(timeout=timeout)

    assert result is None

    table_api.drop_row_range.assert_called_once_with(
        request={"name": TABLE_NAME, "delete_all_data_from_table": True},
        timeout=120,
    )


def test_table_drop_by_prefix():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    table_api = client._table_admin_client = _make_table_api()

    row_key_prefix = b"row-key-prefix"

    result = table.drop_by_prefix(row_key_prefix=row_key_prefix)

    assert result is None

    table_api.drop_row_range.assert_called_once_with(
        request={"name": TABLE_NAME, "row_key_prefix": row_key_prefix},
    )


def test_table_drop_by_prefix_w_timeout():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    table_api = client._table_admin_client = _make_table_api()

    row_key_prefix = b"row-key-prefix"

    timeout = 120
    result = table.drop_by_prefix(row_key_prefix=row_key_prefix, timeout=timeout)

    assert result is None

    table_api.drop_row_range.assert_called_once_with(
        request={"name": TABLE_NAME, "row_key_prefix": row_key_prefix},
        timeout=120,
    )


def test_table_mutations_batcher_factory():
    flush_count = 100
    max_row_bytes = 1000
    table = _make_table(TABLE_ID, None)
    mutation_batcher = table.mutations_batcher(
        flush_count=flush_count, max_row_bytes=max_row_bytes
    )

    assert mutation_batcher.table.table_id == TABLE_ID
    assert mutation_batcher.flush_count == flush_count
    assert mutation_batcher.max_row_bytes == max_row_bytes


def test_table_get_iam_policy():
    from google.iam.v1 import policy_pb2
    from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    version = 1
    etag = b"etag_v1"
    members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
    bindings = [{"role": BIGTABLE_ADMIN_ROLE, "members": members}]
    iam_policy = policy_pb2.Policy(version=version, etag=etag, bindings=bindings)

    table_api = client._table_admin_client = _make_table_api()
    table_api.get_iam_policy.return_value = iam_policy

    result = table.get_iam_policy()

    assert result.version == version
    assert result.etag == etag
    admins = result.bigtable_admins
    assert len(admins) == len(members)

    for found, expected in zip(sorted(admins), sorted(members)):
        assert found == expected

    table_api.get_iam_policy.assert_called_once_with(request={"resource": table.name})


def test_table_set_iam_policy():
    from google.iam.v1 import policy_pb2
    from google.cloud.bigtable.policy import Policy
    from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    version = 1
    etag = b"etag_v1"
    members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
    bindings = [{"role": BIGTABLE_ADMIN_ROLE, "members": sorted(members)}]
    iam_policy_pb = policy_pb2.Policy(version=version, etag=etag, bindings=bindings)

    table_api = client._table_admin_client = _make_table_api()
    table_api.set_iam_policy.return_value = iam_policy_pb

    iam_policy = Policy(etag=etag, version=version)
    iam_policy[BIGTABLE_ADMIN_ROLE] = [
        Policy.user("user1@test.com"),
        Policy.service_account("service_acc1@test.com"),
    ]

    result = table.set_iam_policy(iam_policy)

    assert result.version == version
    assert result.etag == etag
    admins = result.bigtable_admins
    assert len(admins) == len(members)

    for found, expected in zip(sorted(admins), sorted(members)):
        assert found == expected

    table_api.set_iam_policy.assert_called_once_with(
        request={"resource": table.name, "policy": iam_policy_pb}
    )


def test_table_test_iam_permissions():
    from google.iam.v1 import iam_policy_pb2

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    permissions = ["bigtable.tables.mutateRows", "bigtable.tables.readRows"]

    response = iam_policy_pb2.TestIamPermissionsResponse(permissions=permissions)

    table_api = client._table_admin_client = _make_table_api()
    table_api.test_iam_permissions.return_value = response

    result = table.test_iam_permissions(permissions)

    assert result == permissions

    table_api.test_iam_permissions.assert_called_once_with(
        request={"resource": table.name, "permissions": permissions}
    )


def test_table_backup_factory_defaults():
    from google.cloud.bigtable.backup import Backup

    instance = _make_table(INSTANCE_ID, None)
    table = _make_table(TABLE_ID, instance)
    backup = table.backup(BACKUP_ID)

    assert isinstance(backup, Backup)
    assert backup.backup_id == BACKUP_ID
    assert backup._instance is instance
    assert backup._cluster is None
    assert backup.table_id == TABLE_ID
    assert backup._expire_time is None

    assert backup._parent is None
    assert backup._source_table is None
    assert backup._start_time is None
    assert backup._end_time is None
    assert backup._size_bytes is None
    assert backup._state is None


def test_table_backup_factory_non_defaults():
    import datetime
    from google.cloud._helpers import UTC
    from google.cloud.bigtable.backup import Backup
    from google.cloud.bigtable.instance import Instance

    instance = Instance(INSTANCE_ID, None)
    table = _make_table(TABLE_ID, instance)
    timestamp = datetime.datetime.utcnow().replace(tzinfo=UTC)
    backup = table.backup(
        BACKUP_ID,
        cluster_id=CLUSTER_ID,
        expire_time=timestamp,
    )

    assert isinstance(backup, Backup)
    assert backup.backup_id == BACKUP_ID
    assert backup._instance is instance

    assert backup.backup_id == BACKUP_ID
    assert backup._cluster is CLUSTER_ID
    assert backup.table_id == TABLE_ID
    assert backup._expire_time == timestamp
    assert backup._start_time is None
    assert backup._end_time is None
    assert backup._size_bytes is None
    assert backup._state is None


def _table_list_backups_helper(cluster_id=None, filter_=None, **kwargs):
    from google.cloud.bigtable_admin_v2.types import (
        Backup as backup_pb,
        bigtable_table_admin,
    )
    from google.cloud.bigtable.backup import Backup

    client = _make_client(
        project=PROJECT_ID, credentials=_make_credentials(), admin=True
    )
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    parent = INSTANCE_NAME + "/clusters/cluster"
    backups_pb = bigtable_table_admin.ListBackupsResponse(
        backups=[
            backup_pb(name=parent + "/backups/op1"),
            backup_pb(name=parent + "/backups/op2"),
            backup_pb(name=parent + "/backups/op3"),
        ]
    )

    table_api = client._table_admin_client = _make_table_api()
    table_api.list_backups.return_value = backups_pb

    backups_filter = "source_table:{}".format(TABLE_NAME)
    if filter_:
        backups_filter = "({}) AND ({})".format(backups_filter, filter_)

    backups = table.list_backups(cluster_id=cluster_id, filter_=filter_, **kwargs)

    for backup in backups:
        assert isinstance(backup, Backup)

    if not cluster_id:
        cluster_id = "-"
    parent = "{}/clusters/{}".format(INSTANCE_NAME, cluster_id)

    order_by = None
    page_size = 0
    if "order_by" in kwargs:
        order_by = kwargs["order_by"]

    if "page_size" in kwargs:
        page_size = kwargs["page_size"]

    table_api.list_backups.assert_called_once_with(
        request={
            "parent": parent,
            "filter": backups_filter,
            "order_by": order_by,
            "page_size": page_size,
        }
    )


def test_table_list_backups_defaults():
    _table_list_backups_helper()


def test_table_list_backups_w_options():
    _table_list_backups_helper(
        cluster_id="cluster", filter_="filter", order_by="order_by", page_size=10
    )


def _table_restore_helper(backup_name=None):
    from google.cloud.bigtable.instance import Instance

    op_future = object()
    credentials = _make_credentials()
    client = _make_client(project=PROJECT_ID, credentials=credentials, admin=True)

    instance = Instance(INSTANCE_ID, client=client)
    table = _make_table(TABLE_ID, instance)

    table_api = client._table_admin_client = _make_table_api()
    table_api.restore_table.return_value = op_future

    if backup_name:
        future = table.restore(TABLE_ID, backup_name=BACKUP_NAME)
    else:
        future = table.restore(TABLE_ID, CLUSTER_ID, BACKUP_ID)

    assert future is op_future

    expected_request = {
        "parent": INSTANCE_NAME,
        "table_id": TABLE_ID,
        "backup": BACKUP_NAME,
    }
    table_api.restore_table.assert_called_once_with(request=expected_request)


def test_table_restore_table_w_backup_id():
    _table_restore_helper()


def test_table_restore_table_w_backup_name():
    _table_restore_helper(backup_name=BACKUP_NAME)


def _make_worker(*args, **kwargs):
    from google.cloud.bigtable.table import _RetryableMutateRowsWorker

    return _RetryableMutateRowsWorker(*args, **kwargs)


def _make_responses_statuses(codes):
    from google.rpc.status_pb2 import Status

    response = [Status(code=code) for code in codes]
    return response


def _make_responses(codes):
    from google.cloud.bigtable_v2.types.bigtable import MutateRowsResponse
    from google.rpc.status_pb2 import Status

    entries = [
        MutateRowsResponse.Entry(index=i, status=Status(code=codes[i]))
        for i in range(len(codes))
    ]
    return MutateRowsResponse(entries=entries)


def test_rmrw_callable_empty_rows():
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    data_api = client._table_data_client = _make_data_api()
    data_api.mutate_rows.return_value = []
    data_api.table_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/tables/{TABLE_ID}"
    )

    worker = _make_worker(client, table.name, [])
    statuses = worker()

    assert len(statuses) == 0


def test_rmrw_callable_no_retry_strategy():
    from google.cloud.bigtable.row import DirectRow

    # Setup:
    #   - Mutate 3 rows.
    # Action:
    #   - Attempt to mutate the rows w/o any retry strategy.
    # Expectation:
    #   - Since no retry, should return statuses as they come back.
    #   - Even if there are retryable errors, no retry attempt is made.
    #   - State of responses_statuses should be
    #       [success, retryable, non-retryable]
    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    row_1 = DirectRow(row_key=b"row_key", table=table)
    row_1.set_cell("cf", b"col", b"value1")
    row_2 = DirectRow(row_key=b"row_key_2", table=table)
    row_2.set_cell("cf", b"col", b"value2")
    row_3 = DirectRow(row_key=b"row_key_3", table=table)
    row_3.set_cell("cf", b"col", b"value3")

    response_codes = [SUCCESS, RETRYABLE_1, NON_RETRYABLE]
    response = _make_responses(response_codes)

    data_api = client._table_data_client = _make_data_api()
    data_api.mutate_rows.return_value = [response]
    data_api.table_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/tables/{TABLE_ID}"
    )
    worker = _make_worker(client, table.name, [row_1, row_2, row_3])

    statuses = worker(retry=None)

    result = [status.code for status in statuses]
    assert result == response_codes

    data_api.mutate_rows.assert_called_once()


def test_rmrw_callable_retry():
    from google.cloud.bigtable.row import DirectRow
    from google.cloud.bigtable.table import DEFAULT_RETRY

    # Setup:
    #   - Mutate 3 rows.
    # Action:
    #   - Initial attempt will mutate all 3 rows.
    # Expectation:
    #   - First attempt will result in one retryable error.
    #   - Second attempt will result in success for the retry-ed row.
    #   - Check MutateRows is called twice.
    #   - State of responses_statuses should be
    #       [success, success, non-retryable]

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)
    row_1 = DirectRow(row_key=b"row_key", table=table)
    row_1.set_cell("cf", b"col", b"value1")
    row_2 = DirectRow(row_key=b"row_key_2", table=table)
    row_2.set_cell("cf", b"col", b"value2")
    row_3 = DirectRow(row_key=b"row_key_3", table=table)
    row_3.set_cell("cf", b"col", b"value3")

    response_1 = _make_responses([SUCCESS, RETRYABLE_1, NON_RETRYABLE])
    response_2 = _make_responses([SUCCESS])
    data_api = client._table_data_client = _make_data_api()
    data_api.mutate_rows.side_effect = [[response_1], [response_2]]
    data_api.table_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/tables/{TABLE_ID}"
    )
    worker = _make_worker(client, table.name, [row_1, row_2, row_3])
    retry = DEFAULT_RETRY.with_delay(initial=0.1)

    statuses = worker(retry=retry)

    result = [status.code for status in statuses]

    assert result == [SUCCESS, SUCCESS, NON_RETRYABLE]

    assert client._table_data_client.mutate_rows.call_count == 2


def _do_mutate_retryable_rows_helper(
    row_cells,
    responses,
    prior_statuses=None,
    expected_result=None,
    raising_retry=False,
    retryable_error=False,
    timeout=None,
):
    from google.api_core.exceptions import ServiceUnavailable
    from google.cloud.bigtable.row import DirectRow
    from google.cloud.bigtable.table import _BigtableRetryableError
    from google.cloud.bigtable_v2.types import bigtable as data_messages_v2_pb2

    # Setup:
    #   - Mutate 2 rows.
    # Action:
    #   - Initial attempt will mutate all 2 rows.
    # Expectation:
    #   - Expect [success, non-retryable]

    credentials = _make_credentials()
    client = _make_client(project="project-id", credentials=credentials, admin=True)
    instance = client.instance(instance_id=INSTANCE_ID)
    table = _make_table(TABLE_ID, instance)

    rows = []
    for row_key, cell_data in row_cells:
        row = DirectRow(row_key=row_key, table=table)
        row.set_cell(*cell_data)
        rows.append(row)

    response = _make_responses(responses)

    data_api = client._table_data_client = _make_data_api()
    if retryable_error:
        data_api.mutate_rows.side_effect = ServiceUnavailable("testing")
    else:
        data_api.mutate_rows.return_value = [response]

    worker = _make_worker(client, table.name, rows=rows)

    if prior_statuses is not None:
        assert len(prior_statuses) == len(rows)
        worker.responses_statuses = _make_responses_statuses(prior_statuses)

    expected_entries = []
    for row, prior_status in zip(rows, worker.responses_statuses):

        if prior_status is None or prior_status.code in RETRYABLES:
            mutations = row._get_mutations().copy()  # row clears on success
            entry = data_messages_v2_pb2.MutateRowsRequest.Entry(
                row_key=row.row_key,
                mutations=mutations,
            )
            expected_entries.append(entry)

    expected_kwargs = {}
    if timeout is not None:
        worker.timeout = timeout
        expected_kwargs["timeout"] = mock.ANY

    if retryable_error or raising_retry:
        with pytest.raises(_BigtableRetryableError):
            worker._do_mutate_retryable_rows()
        statuses = worker.responses_statuses
    else:
        statuses = worker._do_mutate_retryable_rows()

    if not retryable_error:
        result = [status.code for status in statuses]

        if expected_result is None:
            expected_result = responses

        assert result == expected_result

    if len(responses) == 0 and not retryable_error:
        data_api.mutate_rows.assert_not_called()
    else:
        data_api.mutate_rows.assert_called_once_with(
            table_name=table.name,
            entries=expected_entries,
            app_profile_id=None,
            retry=None,
            **expected_kwargs,
        )
        if timeout is not None:
            called = data_api.mutate_rows.mock_calls[0]
            assert called.kwargs["timeout"]._deadline == timeout


def test_rmrw_do_mutate_retryable_rows_empty_rows():
    #
    # Setup:
    #   - No mutated rows.
    # Action:
    #   - No API call made.
    # Expectation:
    #   - No change.
    #
    row_cells = []
    responses = []

    _do_mutate_retryable_rows_helper(row_cells, responses)


def test_rmrw_do_mutate_retryable_rows_w_timeout():
    #
    # Setup:
    #   - Mutate 2 rows.
    # Action:
    #   - Initial attempt will mutate all 2 rows.
    # Expectation:
    #   - No retryable error codes, so don't expect a raise.
    #   - State of responses_statuses should be [success, non-retryable].
    #
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
    ]

    responses = [SUCCESS, NON_RETRYABLE]

    timeout = 5  # seconds

    _do_mutate_retryable_rows_helper(
        row_cells,
        responses,
        timeout=timeout,
    )


def test_rmrw_do_mutate_retryable_rows_w_retryable_error():
    #
    # Setup:
    #   - Mutate 2 rows.
    # Action:
    #   - Initial attempt will mutate all 2 rows.
    # Expectation:
    #   - No retryable error codes, so don't expect a raise.
    #   - State of responses_statuses should be [success, non-retryable].
    #
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
    ]

    responses = ()

    _do_mutate_retryable_rows_helper(
        row_cells,
        responses,
        retryable_error=True,
    )


def test_rmrw_do_mutate_retryable_rows_retry():
    #
    # Setup:
    #   - Mutate 3 rows.
    # Action:
    #   - Initial attempt will mutate all 3 rows.
    # Expectation:
    #   - Second row returns retryable error code, so expect a raise.
    #   - State of responses_statuses should be
    #       [success, retryable, non-retryable]
    #
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
        (b"row_key_3", ("cf", b"col", b"value3")),
    ]

    responses = [SUCCESS, RETRYABLE_1, NON_RETRYABLE]

    _do_mutate_retryable_rows_helper(
        row_cells,
        responses,
        raising_retry=True,
    )


def test_rmrw_do_mutate_retryable_rows_second_retry():
    #
    # Setup:
    #   - Mutate 4 rows.
    #   - First try results:
    #       [success, retryable, non-retryable, retryable]
    # Action:
    #   - Second try should re-attempt the 'retryable' rows.
    # Expectation:
    #   - After second try:
    #       [success, success, non-retryable, retryable]
    #   - One of the rows tried second time returns retryable error code,
    #     so expect a raise.
    #   - Exception contains response whose index should be '3' even though
    #     only two rows were retried.
    #
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
        (b"row_key_3", ("cf", b"col", b"value3")),
        (b"row_key_4", ("cf", b"col", b"value4")),
    ]

    responses = [SUCCESS, RETRYABLE_1]

    prior_statuses = [
        SUCCESS,
        RETRYABLE_1,
        NON_RETRYABLE,
        RETRYABLE_2,
    ]

    expected_result = [
        SUCCESS,
        SUCCESS,
        NON_RETRYABLE,
        RETRYABLE_1,
    ]

    _do_mutate_retryable_rows_helper(
        row_cells,
        responses,
        prior_statuses=prior_statuses,
        expected_result=expected_result,
        raising_retry=True,
    )


def test_rmrw_do_mutate_retryable_rows_second_try():
    #
    # Setup:
    #   - Mutate 4 rows.
    #   - First try results:
    #       [success, retryable, non-retryable, retryable]
    # Action:
    #   - Second try should re-attempt the 'retryable' rows.
    # Expectation:
    #   - After second try:
    #       [success, non-retryable, non-retryable, success]
    #
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
        (b"row_key_3", ("cf", b"col", b"value3")),
        (b"row_key_4", ("cf", b"col", b"value4")),
    ]

    responses = [NON_RETRYABLE, SUCCESS]

    prior_statuses = [
        SUCCESS,
        RETRYABLE_1,
        NON_RETRYABLE,
        RETRYABLE_2,
    ]

    expected_result = [
        SUCCESS,
        NON_RETRYABLE,
        NON_RETRYABLE,
        SUCCESS,
    ]

    _do_mutate_retryable_rows_helper(
        row_cells,
        responses,
        prior_statuses=prior_statuses,
        expected_result=expected_result,
    )


def test_rmrw_do_mutate_retryable_rows_second_try_no_retryable():
    #
    # Setup:
    #   - Mutate 2 rows.
    #   - First try results: [success, non-retryable]
    # Action:
    #   - Second try has no row to retry.
    # Expectation:
    #   - After second try: [success, non-retryable]
    #
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
    ]

    responses = []  # no calls will be made

    prior_statuses = [
        SUCCESS,
        NON_RETRYABLE,
    ]

    expected_result = [
        SUCCESS,
        NON_RETRYABLE,
    ]

    _do_mutate_retryable_rows_helper(
        row_cells,
        responses,
        prior_statuses=prior_statuses,
        expected_result=expected_result,
    )


def test_rmrw_do_mutate_retryable_rows_mismatch_num_responses():
    row_cells = [
        (b"row_key_1", ("cf", b"col", b"value1")),
        (b"row_key_2", ("cf", b"col", b"value2")),
    ]

    responses = [SUCCESS]

    with pytest.raises(RuntimeError):
        _do_mutate_retryable_rows_helper(row_cells, responses)


def test__create_row_request_table_name_only():
    from google.cloud.bigtable.table import _create_row_request

    table_name = "table_name"
    result = _create_row_request(table_name)
    expected_result = _ReadRowsRequestPB(table_name=table_name)
    assert result == expected_result


def test__create_row_request_row_range_row_set_conflict():
    from google.cloud.bigtable.table import _create_row_request

    with pytest.raises(ValueError):
        _create_row_request(None, end_key=object(), row_set=object())


def test__create_row_request_row_range_start_key():
    from google.cloud.bigtable.table import _create_row_request
    from google.cloud.bigtable_v2.types import RowRange

    table_name = "table_name"
    start_key = b"start_key"
    result = _create_row_request(table_name, start_key=start_key)
    expected_result = _ReadRowsRequestPB(table_name=table_name)
    row_range = RowRange(start_key_closed=start_key)
    expected_result.rows.row_ranges.append(row_range)
    assert result == expected_result


def test__create_row_request_row_range_end_key():
    from google.cloud.bigtable.table import _create_row_request
    from google.cloud.bigtable_v2.types import RowRange

    table_name = "table_name"
    end_key = b"end_key"
    result = _create_row_request(table_name, end_key=end_key)
    expected_result = _ReadRowsRequestPB(table_name=table_name)
    row_range = RowRange(end_key_open=end_key)
    expected_result.rows.row_ranges.append(row_range)
    assert result == expected_result


def test__create_row_request_row_range_both_keys():
    from google.cloud.bigtable.table import _create_row_request
    from google.cloud.bigtable_v2.types import RowRange

    table_name = "table_name"
    start_key = b"start_key"
    end_key = b"end_key"
    result = _create_row_request(table_name, start_key=start_key, end_key=end_key)
    row_range = RowRange(start_key_closed=start_key, end_key_open=end_key)
    expected_result = _ReadRowsRequestPB(table_name=table_name)
    expected_result.rows.row_ranges.append(row_range)
    assert result == expected_result


def test__create_row_request_row_range_both_keys_inclusive():
    from google.cloud.bigtable.table import _create_row_request
    from google.cloud.bigtable_v2.types import RowRange

    table_name = "table_name"
    start_key = b"start_key"
    end_key = b"end_key"
    result = _create_row_request(
        table_name, start_key=start_key, end_key=end_key, end_inclusive=True
    )
    expected_result = _ReadRowsRequestPB(table_name=table_name)
    row_range = RowRange(start_key_closed=start_key, end_key_closed=end_key)
    expected_result.rows.row_ranges.append(row_range)
    assert result == expected_result


def test__create_row_request_with_filter():
    from google.cloud.bigtable.table import _create_row_request
    from google.cloud.bigtable.row_filters import RowSampleFilter

    table_name = "table_name"
    row_filter = RowSampleFilter(0.33)
    result = _create_row_request(table_name, filter_=row_filter)
    expected_result = _ReadRowsRequestPB(
        table_name=table_name, filter=row_filter.to_pb()
    )
    assert result == expected_result


def test__create_row_request_with_limit():
    from google.cloud.bigtable.table import _create_row_request

    table_name = "table_name"
    limit = 1337
    result = _create_row_request(table_name, limit=limit)
    expected_result = _ReadRowsRequestPB(table_name=table_name, rows_limit=limit)
    assert result == expected_result


def test__create_row_request_with_row_set():
    from google.cloud.bigtable.table import _create_row_request
    from google.cloud.bigtable.row_set import RowSet

    table_name = "table_name"
    row_set = RowSet()
    result = _create_row_request(table_name, row_set=row_set)
    expected_result = _ReadRowsRequestPB(table_name=table_name)
    assert result == expected_result


def test__create_row_request_with_app_profile_id():
    from google.cloud.bigtable.table import _create_row_request

    table_name = "table_name"
    limit = 1337
    app_profile_id = "app-profile-id"
    result = _create_row_request(table_name, limit=limit, app_profile_id=app_profile_id)
    expected_result = _ReadRowsRequestPB(
        table_name=table_name, rows_limit=limit, app_profile_id=app_profile_id
    )
    assert result == expected_result


def _ReadRowsRequestPB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.ReadRowsRequest(*args, **kw)


def test_cluster_state___eq__():
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.table import ClusterState

    READY = enum_table.ReplicationState.READY
    state1 = ClusterState(READY)
    state2 = ClusterState(READY)
    assert state1 == state2


def test_cluster_state___eq__type_differ():
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.table import ClusterState

    READY = enum_table.ReplicationState.READY
    state1 = ClusterState(READY)
    state2 = object()
    assert not (state1 == state2)


def test_cluster_state___ne__same_value():
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.table import ClusterState

    READY = enum_table.ReplicationState.READY
    state1 = ClusterState(READY)
    state2 = ClusterState(READY)
    assert not (state1 != state2)


def test_cluster_state___ne__():
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.table import ClusterState

    READY = enum_table.ReplicationState.READY
    INITIALIZING = enum_table.ReplicationState.INITIALIZING
    state1 = ClusterState(READY)
    state2 = ClusterState(INITIALIZING)
    assert state1 != state2


def test_cluster_state__repr__():
    from google.cloud.bigtable.enums import Table as enum_table
    from google.cloud.bigtable.table import ClusterState

    STATE_NOT_KNOWN = enum_table.ReplicationState.STATE_NOT_KNOWN
    INITIALIZING = enum_table.ReplicationState.INITIALIZING
    PLANNED_MAINTENANCE = enum_table.ReplicationState.PLANNED_MAINTENANCE
    UNPLANNED_MAINTENANCE = enum_table.ReplicationState.UNPLANNED_MAINTENANCE
    READY = enum_table.ReplicationState.READY

    replication_dict = {
        STATE_NOT_KNOWN: "STATE_NOT_KNOWN",
        INITIALIZING: "INITIALIZING",
        PLANNED_MAINTENANCE: "PLANNED_MAINTENANCE",
        UNPLANNED_MAINTENANCE: "UNPLANNED_MAINTENANCE",
        READY: "READY",
    }

    assert str(ClusterState(STATE_NOT_KNOWN)) == replication_dict[STATE_NOT_KNOWN]
    assert str(ClusterState(INITIALIZING)) == replication_dict[INITIALIZING]
    assert (
        str(ClusterState(PLANNED_MAINTENANCE)) == replication_dict[PLANNED_MAINTENANCE]
    )
    assert (
        str(ClusterState(UNPLANNED_MAINTENANCE))
        == replication_dict[UNPLANNED_MAINTENANCE]
    )
    assert str(ClusterState(READY)) == replication_dict[READY]

    assert ClusterState(STATE_NOT_KNOWN).replication_state == STATE_NOT_KNOWN
    assert ClusterState(INITIALIZING).replication_state == INITIALIZING
    assert ClusterState(PLANNED_MAINTENANCE).replication_state == PLANNED_MAINTENANCE
    assert (
        ClusterState(UNPLANNED_MAINTENANCE).replication_state == UNPLANNED_MAINTENANCE
    )
    assert ClusterState(READY).replication_state == READY


def _ReadRowsResponseCellChunkPB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    family_name = kw.pop("family_name")
    qualifier = kw.pop("qualifier")
    message = messages_v2_pb2.ReadRowsResponse.CellChunk(*args, **kw)
    message.family_name = family_name
    message.qualifier = qualifier
    return message


def _ReadRowsResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.ReadRowsResponse(*args, **kw)


class _MockReadRowsIterator(object):
    def __init__(self, *values):
        self.iter_values = iter(values)

    def next(self):
        return next(self.iter_values)

    __next__ = next


class _MockFailureIterator_1(object):
    def next(self):
        raise DeadlineExceeded("Failed to read from server")

    def __init__(self, last_scanned_row_key=""):
        self.last_scanned_row_key = last_scanned_row_key

    __next__ = next


class _MockFailureIterator_2(object):
    def __init__(self, *values):
        self.iter_values = values[0]
        self.calls = 0
        self.last_scanned_row_key = ""

    def next(self):
        self.calls += 1
        if self.calls == 1:
            return self.iter_values[0]
        else:
            raise DeadlineExceeded("Failed to read from server")

    __next__ = next


class _ReadRowsResponseV2(object):
    def __init__(self, chunks, last_scanned_row_key=""):
        self.chunks = chunks
        self.last_scanned_row_key = last_scanned_row_key


def _TablePB(*args, **kw):
    from google.cloud.bigtable_admin_v2.types import table as table_v2_pb2

    return table_v2_pb2.Table(*args, **kw)


def _ColumnFamilyPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.types import table as table_v2_pb2

    return table_v2_pb2.ColumnFamily(*args, **kw)


def _ClusterStatePB(replication_state):
    from google.cloud.bigtable_admin_v2.types import table as table_v2_pb2

    return table_v2_pb2.Table.ClusterState(replication_state=replication_state)


def _ClusterStateEncryptionInfoPB(
    encryption_type, encryption_status=None, kms_key_version=None
):
    from google.cloud.bigtable_admin_v2.types import table as table_v2_pb2

    return table_v2_pb2.Table.ClusterState(
        encryption_info=(
            table_v2_pb2.EncryptionInfo(
                encryption_type=encryption_type,
                encryption_status=encryption_status,
                kms_key_version=kms_key_version,
            ),
        )
    )


def _StatusPB(code, message):
    from google.rpc import status_pb2

    status_pb = status_pb2.Status()
    status_pb.code = code
    status_pb.message = message

    return status_pb


def _read_rows_retry_exception(exc):
    return isinstance(exc, DeadlineExceeded)
