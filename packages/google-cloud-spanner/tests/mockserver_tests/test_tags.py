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

from google.cloud.spanner_dbapi import Connection
from google.cloud.spanner_v1 import (
    BatchCreateSessionsRequest,
    ExecuteSqlRequest,
    BeginTransactionRequest,
    TypeCode,
    CommitRequest,
)
from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_single_result,
)


class TestTags(MockServerTestBase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        add_single_result(
            "select name from singers", "name", TypeCode.STRING, [("Some Singer",)]
        )

    def test_select_autocommit_no_tags(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        request = self._execute_and_verify_select_singers(connection)
        self.assertEqual("", request.request_options.request_tag)
        self.assertEqual("", request.request_options.transaction_tag)

    def test_select_autocommit_with_request_tag(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        request = self._execute_and_verify_select_singers(
            connection, request_tag="my_tag"
        )
        self.assertEqual("my_tag", request.request_options.request_tag)
        self.assertEqual("", request.request_options.transaction_tag)

    def test_select_read_only_transaction_no_tags(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        connection.read_only = True
        request = self._execute_and_verify_select_singers(connection)
        self.assertEqual("", request.request_options.request_tag)
        self.assertEqual("", request.request_options.transaction_tag)

    def test_select_read_only_transaction_with_request_tag(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        connection.read_only = True
        request = self._execute_and_verify_select_singers(
            connection, request_tag="my_tag"
        )
        self.assertEqual("my_tag", request.request_options.request_tag)
        self.assertEqual("", request.request_options.transaction_tag)

    def test_select_read_only_transaction_with_transaction_tag(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        connection.read_only = True
        connection.transaction_tag = "my_transaction_tag"
        self._execute_and_verify_select_singers(connection)
        self._execute_and_verify_select_singers(connection)

        # Read-only transactions do not support tags, so the transaction_tag is
        # also not cleared from the connection when a read-only transaction is
        # executed.
        self.assertEqual("my_transaction_tag", connection.transaction_tag)

        # Read-only transactions do not need to be committed or rolled back on
        # Spanner, but dbapi requires this to end the transaction.
        connection.commit()
        requests = self.spanner_service.requests
        self.assertEqual(4, len(requests))
        self.assertTrue(isinstance(requests[0], BatchCreateSessionsRequest))
        self.assertTrue(isinstance(requests[1], BeginTransactionRequest))
        self.assertTrue(isinstance(requests[2], ExecuteSqlRequest))
        self.assertTrue(isinstance(requests[3], ExecuteSqlRequest))
        # Transaction tags are not supported for read-only transactions.
        self.assertEqual("", requests[2].request_options.transaction_tag)
        self.assertEqual("", requests[3].request_options.transaction_tag)

    def test_select_read_write_transaction_no_tags(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        request = self._execute_and_verify_select_singers(connection)
        self.assertEqual("", request.request_options.request_tag)
        self.assertEqual("", request.request_options.transaction_tag)

    def test_select_read_write_transaction_with_request_tag(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        request = self._execute_and_verify_select_singers(
            connection, request_tag="my_tag"
        )
        self.assertEqual("my_tag", request.request_options.request_tag)
        self.assertEqual("", request.request_options.transaction_tag)

    def test_select_read_write_transaction_with_transaction_tag(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        connection.transaction_tag = "my_transaction_tag"
        # The transaction tag should be included for all statements in the transaction.
        self._execute_and_verify_select_singers(connection)
        self._execute_and_verify_select_singers(connection)

        # The transaction tag was cleared from the connection when the transaction
        # was started.
        self.assertIsNone(connection.transaction_tag)
        # The commit call should also include a transaction tag.
        connection.commit()
        requests = self.spanner_service.requests
        self.assertEqual(5, len(requests))
        self.assertTrue(isinstance(requests[0], BatchCreateSessionsRequest))
        self.assertTrue(isinstance(requests[1], BeginTransactionRequest))
        self.assertTrue(isinstance(requests[2], ExecuteSqlRequest))
        self.assertTrue(isinstance(requests[3], ExecuteSqlRequest))
        self.assertTrue(isinstance(requests[4], CommitRequest))
        self.assertEqual(
            "my_transaction_tag", requests[2].request_options.transaction_tag
        )
        self.assertEqual(
            "my_transaction_tag", requests[3].request_options.transaction_tag
        )
        self.assertEqual(
            "my_transaction_tag", requests[4].request_options.transaction_tag
        )

    def test_select_read_write_transaction_with_transaction_and_request_tag(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        connection.transaction_tag = "my_transaction_tag"
        # The transaction tag should be included for all statements in the transaction.
        self._execute_and_verify_select_singers(connection, request_tag="my_tag1")
        self._execute_and_verify_select_singers(connection, request_tag="my_tag2")

        # The transaction tag was cleared from the connection when the transaction
        # was started.
        self.assertIsNone(connection.transaction_tag)
        # The commit call should also include a transaction tag.
        connection.commit()
        requests = self.spanner_service.requests
        self.assertEqual(5, len(requests))
        self.assertTrue(isinstance(requests[0], BatchCreateSessionsRequest))
        self.assertTrue(isinstance(requests[1], BeginTransactionRequest))
        self.assertTrue(isinstance(requests[2], ExecuteSqlRequest))
        self.assertTrue(isinstance(requests[3], ExecuteSqlRequest))
        self.assertTrue(isinstance(requests[4], CommitRequest))
        self.assertEqual(
            "my_transaction_tag", requests[2].request_options.transaction_tag
        )
        self.assertEqual("my_tag1", requests[2].request_options.request_tag)
        self.assertEqual(
            "my_transaction_tag", requests[3].request_options.transaction_tag
        )
        self.assertEqual("my_tag2", requests[3].request_options.request_tag)
        self.assertEqual(
            "my_transaction_tag", requests[4].request_options.transaction_tag
        )

    def test_request_tag_is_cleared(self):
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.request_tag = "my_tag"
            cursor.execute("select name from singers")
            # This query will not have a request tag.
            cursor.execute("select name from singers")
        requests = self.spanner_service.requests

        # Filter for SQL requests calls
        sql_requests = [
            request for request in requests if isinstance(request, ExecuteSqlRequest)
        ]

        self.assertTrue(isinstance(sql_requests[0], ExecuteSqlRequest))
        self.assertTrue(isinstance(sql_requests[1], ExecuteSqlRequest))
        self.assertEqual("my_tag", sql_requests[0].request_options.request_tag)
        self.assertEqual("", sql_requests[1].request_options.request_tag)

    def _execute_and_verify_select_singers(
        self, connection: Connection, request_tag: str = "", transaction_tag: str = ""
    ) -> ExecuteSqlRequest:
        with connection.cursor() as cursor:
            if request_tag:
                cursor.request_tag = request_tag
            cursor.execute("select name from singers")
            result_list = cursor.fetchall()
            for row in result_list:
                self.assertEqual("Some Singer", row[0])
            self.assertEqual(1, len(result_list))
        requests = self.spanner_service.requests
        return next(
            request
            for request in requests
            if isinstance(request, ExecuteSqlRequest)
            and request.sql == "select name from singers"
        )
