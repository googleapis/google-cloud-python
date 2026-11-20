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
import base64
import inspect
from collections import deque
from collections.abc import Iterable, Sequence
from concurrent import futures
from dataclasses import dataclass
from threading import Lock

import grpc
from google.protobuf import empty_pb2
from google.protobuf.struct_pb2 import Value
from google.rpc.code_pb2 import OK
from grpc_status.rpc_status import _Status

import google.cloud.spanner_v1.testing.spanner_database_admin_pb2_grpc as database_admin_grpc
import google.cloud.spanner_v1.testing.spanner_pb2_grpc as spanner_grpc
import google.cloud.spanner_v1.types.commit_response as commit
import google.cloud.spanner_v1.types.result_set as result_set
import google.cloud.spanner_v1.types.spanner as spanner
import google.cloud.spanner_v1.types.transaction as transaction
from google.cloud.spanner_v1.testing.mock_database_admin import DatabaseAdminServicer
from google.cloud.spanner_v1.types.result_set import ResultSetMetadata
from google.cloud.spanner_v1.types.transaction import TransactionOptions


@dataclass
class ExecuteStreamingSqlErrorConfig:
    """Configuration for a mid-stream ExecuteStreamingSql/StreamingRead error."""

    partial_index: int
    error: _Status


@dataclass
class PartialResultSetConfig:
    """Options controlling how a ResultSet is split into PartialResultSets."""

    max_values_per_chunk: int | None = None
    max_string_chunk_length: int | None = None
    emit_resume_tokens: bool = True
    set_last_flag: bool = False

    def __post_init__(self) -> None:
        if self.max_values_per_chunk is not None and self.max_values_per_chunk <= 0:
            raise ValueError("max_values_per_chunk must be positive")
        if (
            self.max_string_chunk_length is not None
            and self.max_string_chunk_length <= 0
        ):
            raise ValueError("max_string_chunk_length must be positive")


class _PartialResultSetBuilder:
    """Accumulates Values into PartialResultSet chunks with Spanner token rules."""

    def __init__(
        self,
        metadata: ResultSetMetadata,
        chunk_config: PartialResultSetConfig,
    ) -> None:
        self._chunk_config = chunk_config
        self._partials: list[result_set.PartialResultSet] = []
        self._token_counter = 0
        self._current_partial = result_set.PartialResultSet()
        self._current_partial.metadata = ResultSetMetadata(metadata)
        self._current_partial_pb = type(self._current_partial).pb(self._current_partial)

    def flush(self, ends_at_row_boundary: bool, chunked_value: bool) -> None:
        """Finalize the current chunk and assign a resume_token only on row ends."""
        self._current_partial_pb.chunked_value = chunked_value
        if (
            self._chunk_config.emit_resume_tokens
            and ends_at_row_boundary
            and not chunked_value
        ):
            self._token_counter += 1
            self._current_partial_pb.resume_token = f"{self._token_counter}".encode(
                "utf-8"
            )
        self._partials.append(self._current_partial)
        self._current_partial = result_set.PartialResultSet()
        self._current_partial_pb = type(self._current_partial).pb(self._current_partial)

    @staticmethod
    def _split_string_cell(
        cell: Value, max_string_chunk_length: int | None
    ) -> list[Value]:
        # Only top-level string_value cells are split automatically to cover
        # chunked_value=True flows; callers needing nested list_value chunks
        # can register explicit partials via add_execute_streaming_sql_results.
        if (
            max_string_chunk_length is None
            or cell.WhichOneof("kind") != "string_value"
            or len(cell.string_value) <= max_string_chunk_length
        ):
            return [cell]
        text = cell.string_value
        return [
            Value(string_value=text[offset : offset + max_string_chunk_length])
            for offset in range(0, len(text), max_string_chunk_length)
        ]

    def append_cell(self, cell: Value) -> None:
        """Append one cell, flushing intermediate chunks for oversized strings."""
        pieces = self._split_string_cell(
            cell, self._chunk_config.max_string_chunk_length
        )
        for piece in pieces[:-1]:
            self._current_partial_pb.values.append(piece)
            self.flush(ends_at_row_boundary=False, chunked_value=True)
        self._current_partial_pb.values.append(pieces[-1])

    def append_row(self, row_values: Sequence[Value], is_last_row: bool) -> None:
        """Append one row, flushing on chunk size limits or row boundaries."""
        column_count = len(row_values)
        max_values = self._chunk_config.max_values_per_chunk
        if column_count == 0:
            if is_last_row or max_values is None:
                self.flush(ends_at_row_boundary=True, chunked_value=False)
            return

        for column_index, cell in enumerate(row_values):
            self.append_cell(cell)
            is_last_column = column_index == column_count - 1
            reached_chunk_limit = (
                max_values is not None
                and len(self._current_partial_pb.values) >= max_values
            )
            flush_at_row_end = is_last_column and (is_last_row or max_values is None)
            if reached_chunk_limit or flush_at_row_end:
                self.flush(
                    ends_at_row_boundary=is_last_column,
                    chunked_value=False,
                )

    def build(
        self, stats: result_set.ResultSetStats
    ) -> list[result_set.PartialResultSet]:
        """Return finalized chunks with trailing stats and optional last flag."""
        if not self._partials:
            self._partials.append(self._current_partial)
        self._partials[-1].stats = stats
        if self._chunk_config.set_last_flag:
            self._partials[-1].last = True
        return self._partials


class MockSpanner:
    def __init__(self):
        self.results = {}
        self.result_chunk_configs: dict[str, PartialResultSetConfig] = {}
        self.execute_streaming_sql_results = {}
        self.execute_streaming_sql_errors: dict[
            str, deque[ExecuteStreamingSqlErrorConfig]
        ] = {}
        self._execute_streaming_sql_errors_lock = Lock()
        self.partition_results = {}
        self.errors = {}
        self.headers = {}

    def clear_results(self):
        self.results = {}
        self.result_chunk_configs = {}
        self.execute_streaming_sql_results = {}
        with self._execute_streaming_sql_errors_lock:
            self.execute_streaming_sql_errors = {}
        self.partition_results = {}
        self.errors = {}
        if hasattr(self, "_errors_list"):
            self._errors_list = {}
        self.headers = {}

    def add_header(self, method: str, header: str, value: str):
        if method not in self.headers:
            self.headers[method] = []
        self.headers[method].append((header, value))

    def send_initial_metadata(self, method_name: str, context):
        headers = self.headers.get(method_name)
        if headers:
            context.send_initial_metadata(tuple(headers))

    def add_result(
        self,
        sql: str,
        result: result_set.ResultSet,
        chunk_config: PartialResultSetConfig | None = None,
    ) -> None:
        normalized_sql = sql.lower().strip()
        self.results[normalized_sql] = result
        # Ensure re-registering via add_result overrides prior explicit partials.
        self.execute_streaming_sql_results.pop(normalized_sql, None)
        if chunk_config is not None:
            self.result_chunk_configs[normalized_sql] = chunk_config
        else:
            self.result_chunk_configs.pop(normalized_sql, None)

    @staticmethod
    def read_request_sql(table: str, columns: Iterable[str]) -> str:
        """Build the canonical synthetic SELECT query key for a ReadRequest."""
        columns_clause = ", ".join(columns) if columns else "*"
        return f"SELECT {columns_clause} FROM {table}"

    def add_partition_result(self, sql: str, result: spanner.PartitionResponse):
        self.partition_results[sql.lower().strip()] = result

    def add_execute_streaming_sql_results(
        self, sql: str, partial_result_sets: list[result_set.PartialResultSet]
    ):
        self.execute_streaming_sql_results[sql.lower().strip()] = partial_result_sets

    def add_execute_streaming_sql_error(
        self, sql: str, partial_index: int, error: _Status
    ) -> None:
        """Queue an error to abort streaming after yielding partial_index chunks."""
        if partial_index < 0:
            raise ValueError("partial_index must be non-negative")
        normalized_sql = sql.lower().strip()
        config = ExecuteStreamingSqlErrorConfig(
            partial_index=partial_index, error=error
        )
        with self._execute_streaming_sql_errors_lock:
            if normalized_sql not in self.execute_streaming_sql_errors:
                self.execute_streaming_sql_errors[normalized_sql] = deque()
            self.execute_streaming_sql_errors[normalized_sql].append(config)

    def pop_execute_streaming_sql_error(
        self, sql: str
    ) -> ExecuteStreamingSqlErrorConfig | None:
        """Pop the next queued mid-stream error for the given SQL, if any."""
        normalized_sql = sql.lower().strip()
        with self._execute_streaming_sql_errors_lock:
            errors = self.execute_streaming_sql_errors.get(normalized_sql)
            if errors:
                return errors.popleft()
        return None

    def has_execute_streaming_sql_result(self, sql: str) -> bool:
        """Return whether a result or partial stream is registered for the SQL."""
        normalized_sql = sql.lower().strip()
        return (
            normalized_sql in self.execute_streaming_sql_results
            or normalized_sql in self.results
        )

    def get_result(self, sql: str) -> result_set.ResultSet:
        result = self.results.get(sql.lower().strip())
        if result is None:
            raise ValueError(f"No result found for {sql}")
        return result

    def get_partition_result(self, sql: str) -> spanner.PartitionResponse:
        result = self.partition_results.get(sql.lower().strip())
        if result is None:
            return spanner.PartitionResponse()
        return result

    def add_error(self, method: str, error: _Status):
        if not hasattr(self, "_errors_list"):
            self._errors_list = {}
        if method not in self._errors_list:
            self._errors_list[method] = []
        self._errors_list[method].append(error)
        self.errors[method] = error

    def pop_error(self, context, method_name: str | None = None):
        name = method_name or inspect.currentframe().f_back.f_code.co_name
        if hasattr(self, "_errors_list") and name in self._errors_list:
            if self._errors_list[name]:
                error = self._errors_list[name].pop(0)
                context.abort_with_status(error)
                return
            return  # Queue is empty, return normally (no error)

        # Fallback to single error
        error: _Status | None = self.errors.pop(name, None)
        if error:
            context.abort_with_status(error)

    def get_execute_streaming_sql_results(
        self, sql: str, started_transaction: transaction.Transaction
    ) -> list[result_set.PartialResultSet]:
        normalized_sql = sql.lower().strip()
        if normalized_sql in self.execute_streaming_sql_results:
            partials = list(self.execute_streaming_sql_results[normalized_sql])
            if started_transaction and partials:
                first_partial = result_set.PartialResultSet()
                type(first_partial).pb(first_partial).CopyFrom(
                    type(partials[0]).pb(partials[0])
                )
                partials[0] = first_partial
        else:
            partials = self.get_result_as_partial_result_sets(sql)
        if started_transaction and partials:
            partials[0].metadata.transaction = started_transaction
        return partials

    def get_result_as_partial_result_sets(
        self, sql: str
    ) -> list[result_set.PartialResultSet]:
        normalized_sql = sql.lower().strip()
        result: result_set.ResultSet = self.get_result(sql)
        chunk_config = self.result_chunk_configs.get(
            normalized_sql, PartialResultSetConfig()
        )
        return self._split_result_into_partial_result_sets(result, chunk_config)

    @staticmethod
    def _split_result_into_partial_result_sets(
        result: result_set.ResultSet, chunk_config: PartialResultSetConfig
    ) -> list[result_set.PartialResultSet]:
        """Convert a ResultSet into PartialResultSets with row-boundary resume tokens.

        Auto-chunking emits resume_token only when emit_resume_tokens is True at a
        non-chunked row boundary; callers testing mid-row or chunked_value=True
        resume tokens can supply explicit chunks via add_execute_streaming_sql_results.
        """
        result_pb = type(result).pb(result)
        builder = _PartialResultSetBuilder(result.metadata, chunk_config)
        total_rows = len(result_pb.rows)
        for row_index, row in enumerate(result_pb.rows):
            builder.append_row(row.values, is_last_row=(row_index == total_rows - 1))
        return builder.build(result.stats)


@dataclass
class BatchDmlResponseConfig:
    status: _Status
    include_transaction_id: bool = True


# An in-memory mock Spanner server that can be used for testing.
class SpannerServicer(spanner_grpc.SpannerServicer):
    def __init__(self):
        self._requests = []
        self.session_counter = 0
        self.sessions = {}
        self.transaction_counter = 0
        self.transactions = {}
        self._mock_spanner = MockSpanner()
        self._batch_dml_response_configs = []

    @property
    def mock_spanner(self):
        return self._mock_spanner

    @property
    def requests(self):
        return self._requests

    def clear_requests(self):
        self._requests = []

    def add_batch_dml_response_status(self, status, include_transaction_id=True):
        if not hasattr(self, "_batch_dml_response_configs"):
            self._batch_dml_response_configs = []
        self._batch_dml_response_configs.append(
            BatchDmlResponseConfig(
                status=status, include_transaction_id=include_transaction_id
            )
        )

    def clear_results(self):
        self.mock_spanner.clear_results()
        self._batch_dml_response_configs = []

    def CreateSession(self, request, context):
        self._requests.append(request)
        return self.__create_session(request.database, request.session)

    def BatchCreateSessions(self, request, context):
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        sessions = []
        for i in range(request.session_count):
            sessions.append(
                self.__create_session(request.database, request.session_template)
            )
        return spanner.BatchCreateSessionsResponse(dict(session=sessions))

    def __create_session(self, database: str, session_template: spanner.Session):
        self.session_counter += 1
        session = spanner.Session()
        session.name = database + "/sessions/" + str(self.session_counter)
        session.multiplexed = session_template.multiplexed
        session.labels.MergeFrom(session_template.labels)
        session.creator_role = session_template.creator_role
        self.sessions[session.name] = session
        return session

    def GetSession(self, request, context):
        self._requests.append(request)
        return spanner.Session()

    def ListSessions(self, request, context):
        self._requests.append(request)
        return [spanner.Session()]

    def DeleteSession(self, request, context):
        self._requests.append(request)
        return empty_pb2.Empty()

    def ExecuteSql(self, request, context):
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        self.mock_spanner.send_initial_metadata("ExecuteSql", context)
        started_transaction = self.__maybe_create_transaction(request)
        result: result_set.ResultSet = self.mock_spanner.get_result(request.sql)
        if started_transaction:
            result.metadata = ResultSetMetadata(result.metadata)
            result.metadata.transaction = started_transaction
        return result

    @staticmethod
    def _advance_past_resume_token(
        partials: Iterable[result_set.PartialResultSet], resume_token: bytes
    ) -> Iterable[result_set.PartialResultSet] | None:
        """Advance past the chunk matching resume_token, returning remaining chunks or None."""
        iterator = iter(partials)
        for partial in iterator:
            if partial.resume_token == resume_token:
                return iterator
        return None

    @staticmethod
    def _read_request_to_sql(request: spanner.ReadRequest) -> str:
        """Convert a ReadRequest to a SELECT query key for MockSpanner lookup.

        Read results share MockSpanner's SQL-keyed registry, matched by table and
        columns only (key_set, index, limit, and partition_token are ignored).
        """
        return MockSpanner.read_request_sql(request.table, request.columns)

    def _execute_streaming(
        self,
        method_name: str,
        sql: str,
        request,
        context,
        allow_missing_result: bool = False,
    ):
        """Stream PartialResultSets for ExecuteStreamingSql or StreamingRead.

        Results and queued errors are keyed by normalized SQL (ignoring
        partition_token), and precommit_token fields are emitted only when
        present on explicitly registered PartialResultSets.
        """
        self._requests.append(request)
        self.mock_spanner.pop_error(context, method_name=method_name)
        self.mock_spanner.send_initial_metadata(method_name, context)
        if request.resume_token and type(request.transaction).pb(
            request.transaction
        ).HasField("begin"):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Cannot combine begin transaction with resume_token.",
            )
            return
        stream_error = self.mock_spanner.pop_execute_streaming_sql_error(sql)
        if stream_error is not None and stream_error.partial_index == 0:
            context.abort_with_status(stream_error.error)
            return
        started_transaction = self.__maybe_create_transaction(request)
        if (
            allow_missing_result
            and not self.mock_spanner.has_execute_streaming_sql_result(sql)
        ):
            partials: Iterable[result_set.PartialResultSet] = [
                result_set.PartialResultSet(),
                result_set.PartialResultSet(),
            ]
            if started_transaction:
                partials[0].metadata.transaction = started_transaction
        else:
            partials = self.mock_spanner.get_execute_streaming_sql_results(
                sql, started_transaction
            )
        if request.resume_token:
            resumed_partials = self._advance_past_resume_token(
                partials, request.resume_token
            )
            if resumed_partials is None:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Invalid resume_token.",
                )
                return
            partials = resumed_partials
        for index, result in enumerate(partials):
            if stream_error is not None and index == stream_error.partial_index:
                context.abort_with_status(stream_error.error)
                return
            yield result
        # Errors with partial_index >= len(partials) abort after the final chunk
        # (even when last=True), allowing tests to exercise trailing stream errors.
        if stream_error is not None:
            context.abort_with_status(stream_error.error)

    def ExecuteStreamingSql(self, request, context):
        yield from self._execute_streaming(
            "ExecuteStreamingSql",
            request.sql,
            request,
            context,
            allow_missing_result=False,
        )

    def ExecuteBatchDml(self, request, context):
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        self.mock_spanner.send_initial_metadata("ExecuteBatchDml", context)
        response = spanner.ExecuteBatchDmlResponse()
        started_transaction = self.__maybe_create_transaction(request)

        config = None
        if (
            hasattr(self, "_batch_dml_response_configs")
            and self._batch_dml_response_configs
        ):
            config = self._batch_dml_response_configs.pop(0)

        first = True
        for statement in request.statements:
            result = self.mock_spanner.get_result(statement.sql)
            if first and started_transaction is not None:
                result = result_set.ResultSet(
                    self.mock_spanner.get_result(statement.sql)
                )
                result.metadata = result_set.ResultSetMetadata(result.metadata)
                if config is None or config.include_transaction_id:
                    result.metadata.transaction = started_transaction
                first = False
            response.result_sets.append(result)

        if config is not None:
            response.status.CopyFrom(config.status)
        else:
            response.status.code = OK

        return response

    def Read(self, request, context):
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        self.mock_spanner.send_initial_metadata("Read", context)
        return result_set.ResultSet()

    def StreamingRead(self, request, context):
        sql = self._read_request_to_sql(request)
        yield from self._execute_streaming(
            "StreamingRead",
            sql,
            request,
            context,
            allow_missing_result=True,
        )

    def BeginTransaction(self, request, context):
        self._requests.append(request)
        return self.__create_transaction(request.session, request.options)

    def __maybe_create_transaction(self, request):
        started_transaction = None
        if not request.transaction.begin == TransactionOptions():
            started_transaction = self.__create_transaction(
                request.session, request.transaction.begin
            )
        return started_transaction

    def __create_transaction(
        self, session: str, options: transaction.TransactionOptions
    ) -> transaction.Transaction:
        session = self.sessions[session]
        if session is None:
            raise ValueError(f"Session not found: {session}")
        self.transaction_counter += 1
        id_bytes = bytes(
            f"{session.name}/transactions/{self.transaction_counter}", "UTF-8"
        )
        transaction_id = base64.urlsafe_b64encode(id_bytes)
        self.transactions[transaction_id] = options
        return transaction.Transaction(dict(id=transaction_id))

    def Commit(self, request, context):
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        if not request.transaction_id == b"":
            tx = self.transactions[request.transaction_id]
            if tx is None:
                raise ValueError(f"Transaction not found: {request.transaction_id}")
            tx_id = request.transaction_id
        elif not request.single_use_transaction == TransactionOptions():
            tx = self.__create_transaction(
                request.session, request.single_use_transaction
            )
            tx_id = tx.id
        else:
            raise ValueError("Unsupported transaction type")
        del self.transactions[tx_id]
        return commit.CommitResponse()

    def Rollback(self, request, context):
        self._requests.append(request)
        return empty_pb2.Empty()

    def PartitionQuery(self, request, context):
        self._requests.append(request)
        return self.mock_spanner.get_partition_result(request.sql)

    def PartitionRead(self, request, context):
        self._requests.append(request)
        # For reads, look up by target table name
        return self.mock_spanner.get_partition_result(request.table)

    def BatchWrite(self, request, context):
        self._requests.append(request)
        for result in [spanner.BatchWriteResponse(), spanner.BatchWriteResponse()]:
            yield result


def start_mock_server() -> (grpc.Server, SpannerServicer, DatabaseAdminServicer, int):
    # Create a gRPC server.
    spanner_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add the Spanner services to the gRPC server.
    spanner_servicer = SpannerServicer()
    spanner_grpc.add_SpannerServicer_to_server(spanner_servicer, spanner_server)
    database_admin_servicer = DatabaseAdminServicer()
    database_admin_grpc.add_DatabaseAdminServicer_to_server(
        database_admin_servicer, spanner_server
    )

    # Start the server on a random port.
    port = spanner_server.add_insecure_port("[::]:0")
    spanner_server.start()
    return spanner_server, spanner_servicer, database_admin_servicer, port
