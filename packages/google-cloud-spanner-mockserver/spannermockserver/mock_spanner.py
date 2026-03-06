#  Copyright 2025 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Mock Spanner Server for testing.
"""

import base64
from concurrent import futures
import inspect

from google.cloud.spanner_v1 import (
    ExecuteSqlRequest,
    ResultSetMetadata,
    TransactionOptions,
)
import google.cloud.spanner_v1.types.commit_response as commit
import google.cloud.spanner_v1.types.result_set as result_set
import google.cloud.spanner_v1.types.spanner as spanner
import google.cloud.spanner_v1.types.transaction as transaction
from google.protobuf import empty_pb2
import grpc
from grpc_status.rpc_status import _Status

from .generated import spanner_database_admin_pb2_grpc as database_admin_grpc
from .generated import spanner_pb2_grpc as spanner_grpc
from .mock_database_admin import DatabaseAdminServicer


class MockSpanner:
    """
    Mock Spanner class to handle in-memory state and responses.
    """

    def __init__(self):
        """Initializes the MockSpanner."""
        self.results = {}
        self.execute_streaming_sql_results = {}
        self.errors = {}

    def add_result(self, sql: str, result: result_set.ResultSet):
        """Adds a result for a specific SQL query."""
        self.results[sql.lower().strip()] = result

    def add_execute_streaming_sql_results(
        self, sql: str, partial_result_sets: list[result_set.PartialResultSet]
    ):
        """Adds streaming SQL results for a specific SQL query."""
        self.execute_streaming_sql_results[sql.lower().strip()] = (
            partial_result_sets
        )

    def get_result(self, sql: str) -> result_set.ResultSet:
        """Retrieves the result for a specific SQL query."""
        result = self.results.get(sql.lower().strip())
        if result is None:
            raise ValueError(f"No result found for {sql}")
        return result

    def add_error(self, method: str, error: _Status):
        """Adds an error to be raised for a specific method."""
        self.errors[method] = error

    def pop_error(self, context):
        """Pops and aborts with an error if one is set for the calling
        method.
        """
        name = inspect.currentframe().f_back.f_code.co_name
        error: _Status | None = self.errors.pop(name, None)
        if error:
            context.abort_with_status(error)

    def get_execute_streaming_sql_results(
        self, sql: str, started_transaction: transaction.Transaction
    ) -> list[result_set.PartialResultSet]:
        """Retrieves streaming SQL results for a specific SQL query."""
        if self.execute_streaming_sql_results.get(sql.lower().strip()):
            partials = self.execute_streaming_sql_results[sql.lower().strip()]
        else:
            partials = self.get_result_as_partial_result_sets(
                sql, started_transaction
            )
        if started_transaction:
            partials[0].metadata.transaction = started_transaction
        return partials

    def get_result_as_partial_result_sets(
        self, sql: str, started_transaction: transaction.Transaction
    ) -> list[result_set.PartialResultSet]:
        """Converts a ResultSet to a list of PartialResultSets."""
        result: result_set.ResultSet = self.get_result(sql)
        partials = []
        first = True
        if len(result.rows) == 0:
            partial = result_set.PartialResultSet()
            partial.metadata = ResultSetMetadata(result.metadata)
            partials.append(partial)
        else:
            for row in result.rows:
                partial = result_set.PartialResultSet()
                if first:
                    partial.metadata = ResultSetMetadata(result.metadata)
                first = False
                partial.values.extend(row)
                partials.append(partial)
        partials[len(partials) - 1].stats = result.stats
        if started_transaction:
            partials[0].metadata.transaction = started_transaction
        return partials


class SpannerServicer(spanner_grpc.SpannerServicer):
    """
    An in-memory mock Spanner server that can be used for testing.
    """

    def __init__(self):
        """Initializes the SpannerServicer."""
        self._requests = []
        self.session_counter = 0
        self.sessions = {}
        self.transaction_counter = 0
        self.transactions = {}
        self._mock_spanner = MockSpanner()

    @property
    def mock_spanner(self):
        """Returns the MockSpanner instance."""
        return self._mock_spanner

    @property
    def requests(self):
        """Returns the list of requests received by the server."""
        return self._requests

    def clear_requests(self):
        """Clears the list of requests received by the server."""
        self._requests = []

    def CreateSession(self, request, context):
        """Creates a new session."""
        self._requests.append(request)
        return self.__create_session(request.database, request.session)

    def BatchCreateSessions(self, request, context):
        """Creates multiple sessions in a batch."""
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        sessions = []
        for i in range(request.session_count):
            sessions.append(
                self.__create_session(
                    request.database, request.session_template
                )
            )
        return spanner.BatchCreateSessionsResponse(dict(session=sessions))

    def __create_session(
        self, database: str, session_template: spanner.Session
    ):
        """Helper method to create a session."""
        self.session_counter += 1
        session = spanner.Session()
        session.name = database + "/sessions/" + str(self.session_counter)
        session.multiplexed = session_template.multiplexed
        session.labels.MergeFrom(session_template.labels)
        session.creator_role = session_template.creator_role
        self.sessions[session.name] = session
        return session

    def GetSession(self, request, context):
        """Retrieves a session."""
        self._requests.append(request)
        return spanner.Session()

    def ListSessions(self, request, context):
        """Lists sessions."""
        self._requests.append(request)
        return [spanner.Session()]

    def DeleteSession(self, request, context):
        """Deletes a session."""
        self._requests.append(request)
        return empty_pb2.Empty()

    def ExecuteSql(self, request, context):
        """Executes a SQL query."""
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        started_transaction = self.__maybe_create_transaction(request)
        result: result_set.ResultSet = self.mock_spanner.get_result(request.sql)
        if started_transaction:
            result.metadata = ResultSetMetadata(result.metadata)
            result.metadata.transaction = started_transaction
        return result

    def ExecuteStreamingSql(self, request: ExecuteSqlRequest, context):
        """Executes a streaming SQL query."""
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        started_transaction = self.__maybe_create_transaction(request)
        partials = self.mock_spanner.get_execute_streaming_sql_results(
            request.sql, started_transaction
        )
        for result in partials:
            yield result

    def ExecuteBatchDml(self, request, context):
        """Executes a batch of DML statements."""
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        response = spanner.ExecuteBatchDmlResponse()
        started_transaction = self.__maybe_create_transaction(request)
        first = True
        for statement in request.statements:
            result = self.mock_spanner.get_result(statement.sql)
            if first and started_transaction is not None:
                result = result_set.ResultSet(
                    self.mock_spanner.get_result(statement.sql)
                )
                result.metadata = result_set.ResultSetMetadata(result.metadata)
                result.metadata.transaction = started_transaction
            response.result_sets.append(result)
        return response

    def Read(self, request, context):
        """Reads rows from the database."""
        self._requests.append(request)
        return result_set.ResultSet()

    def StreamingRead(self, request, context):
        """Reads rows from the database in a streaming fashion."""
        self._requests.append(request)
        for result in [
            result_set.PartialResultSet(),
            result_set.PartialResultSet(),
        ]:
            yield result

    def BeginTransaction(self, request, context):
        """Begins a new transaction."""
        self._requests.append(request)
        return self.__create_transaction(request.session, request.options)

    def __maybe_create_transaction(self, request):
        """Helper method to create a transaction if requested."""
        started_transaction = None
        if not request.transaction.begin == TransactionOptions():
            started_transaction = self.__create_transaction(
                request.session, request.transaction.begin
            )
        return started_transaction

    def __create_transaction(
        self, session: str, options: transaction.TransactionOptions
    ) -> transaction.Transaction:
        """Helper method to create a transaction."""
        session_obj = self.sessions.get(session)
        if session_obj is None:
            raise ValueError(f"Session not found: {session}")
        session = session_obj
        self.transaction_counter += 1
        id_bytes = bytes(
            f"{session.name}/transactions/{self.transaction_counter}", "UTF-8"
        )
        transaction_id = base64.urlsafe_b64encode(id_bytes)
        self.transactions[transaction_id] = options
        return transaction.Transaction(dict(id=transaction_id))

    def Commit(self, request, context):
        """Commits a transaction."""
        self._requests.append(request)
        self.mock_spanner.pop_error(context)
        if not request.transaction_id == b"":
            tx = self.transactions.get(request.transaction_id)
            if tx is None:
                raise ValueError(
                    f"Transaction not found: {request.transaction_id}"
                )
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
        """Rolls back a transaction."""
        self._requests.append(request)
        return empty_pb2.Empty()

    def PartitionQuery(self, request, context):
        """Creates a set of partition tokens for a query."""
        self._requests.append(request)
        return spanner.PartitionResponse()

    def PartitionRead(self, request, context):
        """Creates a set of partition tokens for a read."""
        self._requests.append(request)
        return spanner.PartitionResponse()

    def BatchWrite(self, request, context):
        """Writes a batch of mutations."""
        self._requests.append(request)
        for result in [
            spanner.BatchWriteResponse(),
            spanner.BatchWriteResponse(),
        ]:
            yield result


def start_mock_server() -> tuple[
    grpc.Server,
    SpannerServicer,
    DatabaseAdminServicer,
    int,
]:
    """Starts the mock server."""
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
