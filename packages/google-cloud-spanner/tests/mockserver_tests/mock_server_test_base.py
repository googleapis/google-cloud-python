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
import inspect
import logging
import os
import unittest
from contextvars import ContextVar

import grpc
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.protobuf.duration_pb2 import Duration
from google.rpc import code_pb2, status_pb2
from google.rpc.error_details_pb2 import RetryInfo
from grpc_status._common import code_to_grpc_status_code
from grpc_status.rpc_status import _Status

import google.cloud.spanner_v1.types.result_set as result_set
import google.cloud.spanner_v1.types.type as spanner_type
from google.cloud.spanner_dbapi.parsed_statement import AutocommitDmlMode
from google.cloud.spanner_v1 import (
    Client,
    FixedSizePool,
    PartialResultSet,
    ResultSetMetadata,
    StructType,
    Type,
    TypeCode,
)
from google.cloud.spanner_v1._helpers import _make_value_pb
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance
from google.cloud.spanner_v1.testing.mock_database_admin import DatabaseAdminServicer
from google.cloud.spanner_v1.testing.mock_spanner import (
    MockSpanner,
    PartialResultSetConfig,
    SpannerServicer,
    start_mock_server,
)
from tests._helpers import is_multiplexed_enabled

current_service = ContextVar("current_service", default=None)


def _make_status(code: int, message: str, with_retry_info: bool = False) -> _Status:
    """Create a gRPC status with optional minimal RetryInfo."""
    error = status_pb2.Status(code=code, message=message)
    trailing_metadata = [("grpc-status-details-bin", error.SerializeToString())]
    if with_retry_info:
        retry_info = RetryInfo(retry_delay=Duration(seconds=0, nanos=1))
        trailing_metadata.append(
            ("google.rpc.retryinfo-bin", retry_info.SerializeToString())
        )
    return _Status(
        code=code_to_grpc_status_code(error.code),
        details=error.message,
        trailing_metadata=tuple(trailing_metadata),
    )


# Creates an aborted status with the smallest possible retry delay.
def aborted_status() -> _Status:
    return _make_status(
        code_pb2.ABORTED, "Transaction was aborted.", with_retry_info=True
    )


def invalid_argument_status() -> _Status:
    return _make_status(code_pb2.INVALID_ARGUMENT, "Invalid argument.")


def deadline_exceeded_status() -> _Status:
    return _make_status(code_pb2.DEADLINE_EXCEEDED, "Deadline exceeded.")


def internal_server_error_status(
    message: str = "Internal server error.",
) -> _Status:
    return _make_status(code_pb2.INTERNAL, message)


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
        partial_result_set.chunked_value = result.get("chunked_value") or False
        resume_token = result.get("resume_token")
        if resume_token is not None:
            partial_result_set.resume_token = resume_token
        partial_result_sets.append(partial_result_set)
    return partial_result_sets


# Creates an UNAVAILABLE status with the smallest possible retry delay.
def unavailable_status() -> _Status:
    return _make_status(
        code_pb2.UNAVAILABLE, "Service unavailable.", with_retry_info=True
    )


def get_spanner_service():
    service = current_service.get()
    if service:
        return service
    if AsyncMockServerTestBase.spanner_service:
        return AsyncMockServerTestBase.spanner_service
    return MockServerTestBase.spanner_service


def add_error(method: str, error: status_pb2.Status):
    get_spanner_service().mock_spanner.add_error(method, error)


def add_header(method: str, header: str, value: str):
    get_spanner_service().mock_spanner.add_header(method, header, value)


def add_result(
    sql: str,
    result: result_set.ResultSet,
    chunk_config: PartialResultSetConfig | None = None,
):
    get_spanner_service().mock_spanner.add_result(
        sql, result, chunk_config=chunk_config
    )


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
    get_spanner_service().mock_spanner.add_execute_streaming_sql_results(
        sql, partial_result_sets
    )


def add_execute_streaming_sql_error(
    sql: str, partial_index: int, error: _Status
) -> None:
    """Queue a mid-stream error for ExecuteStreamingSql on the active mock server."""
    get_spanner_service().mock_spanner.add_execute_streaming_sql_error(
        sql, partial_index, error
    )


def add_streaming_read_error(
    table: str, columns: list[str], partial_index: int, error: _Status
) -> None:
    """Queue a mid-stream error for StreamingRead on the active mock server."""
    sql = MockSpanner.read_request_sql(table, columns)
    add_execute_streaming_sql_error(sql, partial_index, error)


def add_multi_column_result(
    sql: str,
    columns: list[tuple[str, spanner_type.TypeCode]],
    rows: list[tuple],
    chunk_config: PartialResultSetConfig | None = None,
) -> None:
    """Register a multi-column ResultSet with optional PartialResultSet chunking config."""
    fields = [
        spanner_type.StructType.Field(
            dict(name=column_name, type=spanner_type.Type(dict(code=type_code)))
        )
        for column_name, type_code in columns
    ]
    result = result_set.ResultSet(
        dict(
            metadata=result_set.ResultSetMetadata(
                dict(row_type=spanner_type.StructType(dict(fields=fields)))
            )
        )
    )
    result.rows.extend(rows)
    add_result(sql, result, chunk_config=chunk_config)


def add_single_result(
    sql: str,
    column_name: str,
    type_code: spanner_type.TypeCode,
    row,
    chunk_config: PartialResultSetConfig | None = None,
):
    add_multi_column_result(
        sql, [(column_name, type_code)], row, chunk_config=chunk_config
    )


# TODO: Construct test Database/transport directly instead of relying on
# enable_interceptors_in_tests=True.
class MockServerTestBase(unittest.TestCase):
    _interceptors = []
    server: grpc.Server = None
    spanner_service: SpannerServicer = None
    database_admin_service: DatabaseAdminServicer = None
    port: int = None
    logger: logging.Logger = None

    def __init__(self, *args, **kwargs):
        super(MockServerTestBase, self).__init__(*args, **kwargs)
        # Disable built-in metrics for tests to avoid Unauthenticated errors
        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "true"

        self._client = None
        self._instance = None
        self._database = None
        self.logger = logging.getLogger("MockServerTestBase")
        self.logger.setLevel(logging.WARN)

    @classmethod
    def setUpClass(cls):
        (
            MockServerTestBase.server,
            MockServerTestBase.spanner_service,
            MockServerTestBase.database_admin_service,
            MockServerTestBase.port,
        ) = start_mock_server()

    @classmethod
    def tearDownClass(cls):
        if MockServerTestBase.server is not None:
            MockServerTestBase.server.stop(grace=None)
            Client.NTH_CLIENT.reset()
            MockServerTestBase.server = None

    def setUp(self):
        self._client = None
        self._instance = None
        self._database = None
        current_service.set(MockServerTestBase.spanner_service)

    def tearDown(self):
        MockServerTestBase.spanner_service.clear_requests()
        MockServerTestBase.spanner_service.clear_results()
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
                logger=self.logger,
            )
        return self._database

    def assert_requests_sequence(
        self,
        requests,
        expected_types,
        transaction_type,
        allow_multiple_batch_create=True,
    ):
        """Assert that the requests sequence matches expected types."""
        _assert_requests_sequence(
            self,
            requests,
            expected_types,
            transaction_type,
            allow_multiple_batch_create=allow_multiple_batch_create,
        )

    def adjust_request_id_sequence(self, expected_segments, requests, transaction_type):
        """Adjust expected request ID sequence numbers based on actual session creation requests.

        Args:
            expected_segments: List of expected (method, (sequence_numbers)) tuples
            requests: List of actual requests from spanner_service.requests
            transaction_type: TransactionType enum value to check multiplexed session status

        Returns:
            List of adjusted expected segments with corrected sequence numbers
        """
        # Count session creation requests that come before the first non-session request
        session_requests_before = 0
        for req in requests:
            if type(req).__name__ in (
                "BatchCreateSessionsRequest",
                "CreateSessionRequest",
            ):
                session_requests_before += 1
            elif type(req).__name__ in ("ExecuteSqlRequest", "BeginTransactionRequest"):
                break

        # For multiplexed sessions, we expect 2 session requests (BatchCreateSessions + CreateSession)
        # For non-multiplexed, we expect 1 session request (BatchCreateSessions)
        mux_enabled = is_multiplexed_enabled(transaction_type)
        expected_session_requests = 2 if mux_enabled else 1
        extra_session_requests = session_requests_before - expected_session_requests

        # Adjust sequence numbers based on extra session requests
        adjusted_segments = []
        for method, seq_nums in expected_segments:
            # Adjust the sequence number (5th element in the tuple)
            adjusted_seq_nums = list(seq_nums)
            adjusted_seq_nums[4] += extra_session_requests
            adjusted_segments.append((method, tuple(adjusted_seq_nums)))

        return adjusted_segments


def _assert_requests_sequence(
    test_case,
    requests,
    expected_types,
    transaction_type,
    allow_multiple_batch_create=True,
):
    """Assert that requests match expected types, accounting for multiplexed sessions and retries."""
    mux_enabled = is_multiplexed_enabled(transaction_type)
    request_index = 0
    # Skip all leading BatchCreateSessionsRequest (for retries)
    if allow_multiple_batch_create:
        while (
            request_index < len(requests)
            and type(requests[request_index]).__name__ == "BatchCreateSessionsRequest"
        ):
            request_index += 1
        # For multiplexed, optionally skip a CreateSessionRequest
        if (
            mux_enabled
            and request_index < len(requests)
            and type(requests[request_index]).__name__ == "CreateSessionRequest"
        ):
            request_index += 1
    else:
        expected_leading = ["BatchCreateSessionsRequest"]
        if mux_enabled:
            expected_leading.append("CreateSessionRequest")
        for expected_name in expected_leading:
            test_case.assertLess(
                request_index,
                len(requests),
                f"Expected {expected_name} at index {request_index}, got {requests}",
            )
            test_case.assertTrue(
                type(requests[request_index]).__name__ == expected_name,
                f"Expected {expected_name} at index {request_index}, got {type(requests[request_index])}",
            )
            request_index += 1
    # Check the rest of the expected request types
    for expected_type in expected_types:
        test_case.assertLess(
            request_index,
            len(requests),
            f"Expected {expected_type} at index {request_index}, got only {len(requests)} requests",
        )
        test_case.assertTrue(
            isinstance(requests[request_index], expected_type)
            or type(requests[request_index]).__name__ == expected_type.__name__,
            f"Expected {expected_type} at index {request_index}, got {type(requests[request_index])}",
        )
        request_index += 1
    test_case.assertEqual(
        request_index,
        len(requests),
        f"Expected {request_index} requests, got {len(requests)}",
    )


# TODO: Construct test Database/transport directly instead of relying on
# enable_interceptors_in_tests=True.
class AsyncMockServerTestBase(unittest.IsolatedAsyncioTestCase):
    server: grpc.Server = None
    spanner_service: SpannerServicer = None
    database_admin_service: DatabaseAdminServicer = None
    port: int = None
    logger: logging.Logger = None

    def __init__(self, *args, **kwargs):
        super(AsyncMockServerTestBase, self).__init__(*args, **kwargs)
        self._client = None
        self._instance = None
        self._database = None
        self._databases_to_close = []
        self.logger = logging.getLogger("AsyncMockServerTestBase")
        self.logger.setLevel(logging.WARN)

    @classmethod
    def setUpClass(cls):
        (
            AsyncMockServerTestBase.server,
            AsyncMockServerTestBase.spanner_service,
            AsyncMockServerTestBase.database_admin_service,
            AsyncMockServerTestBase.port,
        ) = start_mock_server()

    @classmethod
    def tearDownClass(cls):
        if AsyncMockServerTestBase.server is not None:
            AsyncMockServerTestBase.server.stop(grace=None)
            from google.cloud.spanner_v1._async.client import Client as AsyncClient

            AsyncClient.NTH_CLIENT.reset()
            AsyncMockServerTestBase.server = None

    async def asyncSetUp(self):
        self._client = None
        self._instance = None
        self._database = None
        self._databases_to_close = []
        current_service.set(AsyncMockServerTestBase.spanner_service)

    async def _close_database_and_transport(self, database):
        """Close a database's background session tasks and its gRPC AsyncIO transport."""
        try:
            await database.close()
        finally:
            spanner_api = getattr(database, "_spanner_api", None)
            transport = getattr(spanner_api, "transport", None) if spanner_api else None
            if transport is not None and hasattr(transport, "close"):
                close_result = transport.close()
                if inspect.isawaitable(close_result):
                    await close_result

    async def asyncTearDown(self):
        first_error = None
        try:
            for database in reversed(self._databases_to_close):
                try:
                    await self._close_database_and_transport(database)
                except Exception as error:
                    if first_error is None:
                        first_error = error
            self._databases_to_close.clear()
        finally:
            AsyncMockServerTestBase.spanner_service.clear_requests()
            AsyncMockServerTestBase.spanner_service.clear_results()
            AsyncMockServerTestBase.database_admin_service.clear_requests()
        if first_error is not None:
            raise first_error

    def create_client(
        self,
        *,
        disable_builtin_metrics: bool = True,
        observability_options: dict | None = None,
        client_options: ClientOptions | None = None,
        **kwargs,
    ):
        """Create an AsyncClient configured against the active mock server."""
        from google.cloud.spanner_v1._async.client import Client as AsyncClient

        if client_options is None:
            client_options = ClientOptions(
                api_endpoint=f"localhost:{AsyncMockServerTestBase.port}",
            )
        return AsyncClient(
            project="p",
            credentials=AnonymousCredentials(),
            client_options=client_options,
            disable_builtin_metrics=disable_builtin_metrics,
            observability_options=observability_options,
            **kwargs,
        )

    @property
    def client(self):
        if self._client is None:
            self._client = self.create_client()
        return self._client

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self.client.instance("test-instance")
        return self._instance

    async def create_database(
        self,
        database_id: str = "test-database",
        *,
        client=None,
        instance=None,
        pool=None,
        enable_interceptors_in_tests: bool = False,
        interceptors=None,
        logger: logging.Logger | None = None,
        **kwargs,
    ):
        """Create, bind, and track an async Database for automatic teardown."""
        from google.cloud.spanner_v1._async.pool import FixedSizePool

        if interceptors is not None and not enable_interceptors_in_tests:
            raise ValueError(
                "enable_interceptors_in_tests must be True when interceptors are provided."
            )

        target_instance = instance or (
            client.instance("test-instance") if client is not None else self.instance
        )
        if pool is None:
            pool = FixedSizePool(size=10)

        if interceptors is not None:
            from google.cloud.spanner_v1._async.testing.database_test import (
                TestDatabase,
            )

            database = TestDatabase(
                database_id,
                target_instance,
                pool=pool,
                logger=logger or self.logger,
                **kwargs,
            )
            database._interceptors.extend(interceptors)
            bind_result = database._pool.bind(database)
            if bind_result is not None:
                await bind_result
        else:
            database = await target_instance.database(
                database_id,
                pool=pool,
                enable_interceptors_in_tests=enable_interceptors_in_tests,
                logger=logger or self.logger,
                **kwargs,
            )
        self._databases_to_close.append(database)
        return database

    async def get_database(self):
        """Return a lazily-created default async Database bound to the mock server."""
        if self._database is None:
            self._database = await self.create_database()
        return self._database

    def assert_requests_sequence(
        self,
        requests,
        expected_types,
        transaction_type,
        allow_multiple_batch_create=True,
    ):
        """Assert that the requests sequence matches expected types."""
        _assert_requests_sequence(
            self,
            requests,
            expected_types,
            transaction_type,
            allow_multiple_batch_create=allow_multiple_batch_create,
        )
