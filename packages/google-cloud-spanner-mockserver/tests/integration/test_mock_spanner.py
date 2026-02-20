# Copyright 2025 Google LLC
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

from google.api_core import exceptions
from google.cloud.spanner_v1 import KeySet, Type, TypeCode
from google.cloud.spanner_v1.types import StructType, result_set
from google.protobuf.struct_pb2 import ListValue, Value
from google.rpc import code_pb2, status_pb2
from grpc_status import rpc_status

from spannermockserver import MockServerTestBase


class TestMockSpanner(MockServerTestBase):
    def test_execute_sql(self):
        sql = "SELECT 1"
        expected_result = result_set.ResultSet(
            metadata=result_set.ResultSetMetadata(
                row_type=StructType(
                    fields=[
                        StructType.Field(
                            name="col1", type=Type(code=TypeCode.INT64)
                        )
                    ]
                )
            ),
            rows=[ListValue(values=[Value(string_value="1")])],
        )
        self.spanner_service.mock_spanner.add_result(sql, expected_result)

        with self.database.snapshot() as snapshot:
            results = list(snapshot.execute_sql(sql))
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], 1)

    def test_execute_sql_error(self):
        sql = "SELECT 1"
        status = status_pb2.Status(
            code=code_pb2.PERMISSION_DENIED, message="Permission denied"
        )
        # Client uses ExecuteStreamingSql for execute_sql
        self.spanner_service.mock_spanner.add_error(
            "ExecuteStreamingSql", rpc_status.to_status(status)
        )

        with self.assertRaises(exceptions.PermissionDenied):
            with self.database.snapshot() as snapshot:
                list(snapshot.execute_sql(sql))

    def test_execute_streaming_sql(self):
        sql = "SELECT * FROM Singers"
        partial_result_1 = result_set.PartialResultSet(
            metadata=result_set.ResultSetMetadata(
                row_type=StructType(
                    fields=[
                        StructType.Field(
                            name="SingerId", type=Type(code=TypeCode.INT64)
                        ),
                        StructType.Field(
                            name="Name", type=Type(code=TypeCode.STRING)
                        ),
                    ]
                )
            ),
        )
        partial_result_1.values.extend(
            [Value(string_value="1"), Value(string_value="Singer1")]
        )

        partial_result_2 = result_set.PartialResultSet(
            stats=result_set.ResultSetStats(row_count_exact=2),
        )
        partial_result_2.values.extend(
            [Value(string_value="2"), Value(string_value="Singer2")]
        )
        self.spanner_service.mock_spanner.add_execute_streaming_sql_results(
            sql, [partial_result_1, partial_result_2]
        )

        with self.database.snapshot() as snapshot:
            results = list(snapshot.execute_sql(sql))
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0][0], 1)
            self.assertEqual(results[0][1], "Singer1")
            self.assertEqual(results[1][0], 2)
            self.assertEqual(results[1][1], "Singer2")

    def test_commit(self):
        sql = "UPDATE Singers SET Name='Test' WHERE SingerId=1"
        self.spanner_service.mock_spanner.add_result(
            sql,
            result_set.ResultSet(
                stats=result_set.ResultSetStats(row_count_exact=1)
            ),
        )

        def unit_of_work(transaction):
            transaction.execute_update(sql)

        self.database.run_in_transaction(unit_of_work)

    def test_commit_error(self):
        sql = "UPDATE Singers SET Name='Test' WHERE SingerId=1"
        self.spanner_service.mock_spanner.add_result(
            sql,
            result_set.ResultSet(
                stats=result_set.ResultSetStats(row_count_exact=1)
            ),
        )
        status = status_pb2.Status(
            code=code_pb2.PERMISSION_DENIED, message="Permission denied"
        )
        self.spanner_service.mock_spanner.add_error(
            "Commit", rpc_status.to_status(status)
        )

        def unit_of_work(transaction):
            transaction.execute_update(sql)

        with self.assertRaises(exceptions.PermissionDenied):
            self.database.run_in_transaction(unit_of_work)

    def test_rollback(self):
        # Rollback is triggered when an exception occurs in the transaction
        sql = "UPDATE Singers SET Name='Test' WHERE SingerId=1"
        self.spanner_service.mock_spanner.add_result(
            sql,
            result_set.ResultSet(
                stats=result_set.ResultSetStats(row_count_exact=1)
            ),
        )

        def unit_of_work(transaction):
            transaction.execute_update(sql)
            raise RuntimeError("Intentional error")

        with self.assertRaises(RuntimeError):
            self.database.run_in_transaction(unit_of_work)

        # Verify Rollback was called
        rollback_requests = [
            req
            for req in self.spanner_service.requests
            if req.__class__.__name__ == "RollbackRequest"
        ]
        self.assertTrue(len(rollback_requests) > 0)

    def test_partition_query(self):
        sql = "SELECT * FROM Singers"
        # Mock implementation returns empty PartitionResponse

        with self.database.batch_snapshot() as snapshot:
            partitions = snapshot.generate_query_batches(sql)
            self.assertEqual(len(list(partitions)), 0)

    def test_partition_read(self):
        table = "Singers"
        columns = ["SingerId", "Name"]
        keyset = KeySet(all_=True)

        with self.database.batch_snapshot() as snapshot:
            partitions = snapshot.generate_read_batches(table, columns, keyset)
            self.assertEqual(len(list(partitions)), 0)
