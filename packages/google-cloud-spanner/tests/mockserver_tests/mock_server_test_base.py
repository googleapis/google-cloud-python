# Copyright 2024 Google LLC All rights reserved.
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

import unittest

import grpc
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud.spanner_v1 import Type

from google.cloud.spanner_v1 import StructType
from google.cloud.spanner_v1._helpers import _make_value_pb

from google.cloud.spanner_v1 import PartialResultSet
from google.protobuf.duration_pb2 import Duration
from google.rpc import code_pb2, status_pb2

from google.rpc.error_details_pb2 import RetryInfo
from grpc_status._common import code_to_grpc_status_code
from grpc_status.rpc_status import _Status

import google.cloud.spanner_v1.types.result_set as result_set
import google.cloud.spanner_v1.types.type as spanner_type
from google.cloud.spanner_dbapi.parsed_statement import AutocommitDmlMode
from google.cloud.spanner_v1 import Client, FixedSizePool, ResultSetMetadata, TypeCode
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance
from google.cloud.spanner_v1.testing.mock_database_admin import DatabaseAdminServicer
from google.cloud.spanner_v1.testing.mock_spanner import (
    SpannerServicer,
    start_mock_server,
)


# Creates an aborted status with the smallest possible retry delay.
def aborted_status() -> _Status:
    error = status_pb2.Status(
        code=code_pb2.ABORTED,
        message="Transaction was aborted.",
    )
    retry_info = RetryInfo(retry_delay=Duration(seconds=0, nanos=1))
    status = _Status(
        code=code_to_grpc_status_code(error.code),
        details=error.message,
        trailing_metadata=(
            ("grpc-status-details-bin", error.SerializeToString()),
            (
                "google.rpc.retryinfo-bin",
                retry_info.SerializeToString(),
            ),
        ),
    )
    return status


def _make_partial_result_sets(
    fields: list[tuple[str, TypeCode]], results: list[dict]
) -> list[result_set.PartialResultSet]:
    partial_result_sets = []
    for result in results:
        partial_result_set = PartialResultSet()
        if len(partial_result_sets) == 0:
            # setting the metadata
            metadata = ResultSetMetadata(row_type=StructType(fields=[]))
            for field in fields:
                metadata.row_type.fields.append(
                    StructType.Field(name=field[0], type_=Type(code=field[1]))
                )
            partial_result_set.metadata = metadata
        for value in result["values"]:
            partial_result_set.values.append(_make_value_pb(value))
        partial_result_set.last = result.get("last") or False
        partial_result_sets.append(partial_result_set)
    return partial_result_sets


# Creates an UNAVAILABLE status with the smallest possible retry delay.
def unavailable_status() -> _Status:
    error = status_pb2.Status(
        code=code_pb2.UNAVAILABLE,
        message="Service unavailable.",
    )
    retry_info = RetryInfo(retry_delay=Duration(seconds=0, nanos=1))
    status = _Status(
        code=code_to_grpc_status_code(error.code),
        details=error.message,
        trailing_metadata=(
            ("grpc-status-details-bin", error.SerializeToString()),
            (
                "google.rpc.retryinfo-bin",
                retry_info.SerializeToString(),
            ),
        ),
    )
    return status


def add_error(method: str, error: status_pb2.Status):
    MockServerTestBase.spanner_service.mock_spanner.add_error(method, error)


def add_result(sql: str, result: result_set.ResultSet):
    MockServerTestBase.spanner_service.mock_spanner.add_result(sql, result)


def add_update_count(
    sql: str, count: int, dml_mode: AutocommitDmlMode = AutocommitDmlMode.TRANSACTIONAL
):
    if dml_mode == AutocommitDmlMode.PARTITIONED_NON_ATOMIC:
        stats = dict(row_count_lower_bound=count)
    else:
        stats = dict(row_count_exact=count)
    result = result_set.ResultSet(dict(stats=result_set.ResultSetStats(stats)))
    add_result(sql, result)


def add_select1_result():
    add_single_result("select 1", "c", TypeCode.INT64, [("1",)])


def add_execute_streaming_sql_results(
    sql: str, partial_result_sets: list[result_set.PartialResultSet]
):
    MockServerTestBase.spanner_service.mock_spanner.add_execute_streaming_sql_results(
        sql, partial_result_sets
    )


def add_single_result(
    sql: str, column_name: str, type_code: spanner_type.TypeCode, row
):
    result = result_set.ResultSet(
        dict(
            metadata=result_set.ResultSetMetadata(
                dict(
                    row_type=spanner_type.StructType(
                        dict(
                            fields=[
                                spanner_type.StructType.Field(
                                    dict(
                                        name=column_name,
                                        type=spanner_type.Type(dict(code=type_code)),
                                    )
                                )
                            ]
                        )
                    )
                )
            ),
        )
    )
    result.rows.extend(row)
    MockServerTestBase.spanner_service.mock_spanner.add_result(sql, result)


class MockServerTestBase(unittest.TestCase):
    server: grpc.Server = None
    spanner_service: SpannerServicer = None
    database_admin_service: DatabaseAdminServicer = None
    port: int = None

    def __init__(self, *args, **kwargs):
        super(MockServerTestBase, self).__init__(*args, **kwargs)
        self._client = None
        self._instance = None
        self._database = None

    @classmethod
    def setup_class(cls):
        (
            MockServerTestBase.server,
            MockServerTestBase.spanner_service,
            MockServerTestBase.database_admin_service,
            MockServerTestBase.port,
        ) = start_mock_server()

    @classmethod
    def teardown_class(cls):
        if MockServerTestBase.server is not None:
            MockServerTestBase.server.stop(grace=None)
            Client.NTH_CLIENT.reset()
            MockServerTestBase.server = None

    def setup_method(self, *args, **kwargs):
        self._client = None
        self._instance = None
        self._database = None

    def teardown_method(self, *args, **kwargs):
        MockServerTestBase.spanner_service.clear_requests()
        MockServerTestBase.database_admin_service.clear_requests()

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(
                project="p",
                credentials=AnonymousCredentials(),
                client_options=ClientOptions(
                    api_endpoint="localhost:" + str(MockServerTestBase.port),
                ),
            )
        return self._client

    @property
    def instance(self) -> Instance:
        if self._instance is None:
            self._instance = self.client.instance("test-instance")
        return self._instance

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = self.instance.database(
                "test-database",
                pool=FixedSizePool(size=10),
                enable_interceptors_in_tests=True,
            )
        return self._database
