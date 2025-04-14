# Copyright 2025 Google LLC All rights reserved.
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

from google.api_core.exceptions import Unknown
from google.cloud.spanner_dbapi import Connection
from google.cloud.spanner_v1 import (
    BeginTransactionRequest,
    TransactionOptions,
)
from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_update_count,
)


class TestDbapiIsolationLevel(MockServerTestBase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        add_update_count("insert into singers (id, name) values (1, 'Some Singer')", 1)

    def test_isolation_level_default(self):
        connection = Connection(self.instance, self.database)
        with connection.cursor() as cursor:
            cursor.execute("insert into singers (id, name) values (1, 'Some Singer')")
            self.assertEqual(1, cursor.rowcount)
        connection.commit()
        begin_requests = list(
            filter(
                lambda msg: isinstance(msg, BeginTransactionRequest),
                self.spanner_service.requests,
            )
        )
        self.assertEqual(1, len(begin_requests))
        self.assertEqual(
            begin_requests[0].options.isolation_level,
            TransactionOptions.IsolationLevel.ISOLATION_LEVEL_UNSPECIFIED,
        )

    def test_custom_isolation_level(self):
        connection = Connection(self.instance, self.database)
        for level in [
            TransactionOptions.IsolationLevel.ISOLATION_LEVEL_UNSPECIFIED,
            TransactionOptions.IsolationLevel.REPEATABLE_READ,
            TransactionOptions.IsolationLevel.SERIALIZABLE,
        ]:
            connection.isolation_level = level
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into singers (id, name) values (1, 'Some Singer')"
                )
                self.assertEqual(1, cursor.rowcount)
            connection.commit()
            begin_requests = list(
                filter(
                    lambda msg: isinstance(msg, BeginTransactionRequest),
                    self.spanner_service.requests,
                )
            )
            self.assertEqual(1, len(begin_requests))
            self.assertEqual(begin_requests[0].options.isolation_level, level)
            MockServerTestBase.spanner_service.clear_requests()

    def test_isolation_level_in_connection_kwargs(self):
        for level in [
            TransactionOptions.IsolationLevel.ISOLATION_LEVEL_UNSPECIFIED,
            TransactionOptions.IsolationLevel.REPEATABLE_READ,
            TransactionOptions.IsolationLevel.SERIALIZABLE,
        ]:
            connection = Connection(self.instance, self.database, isolation_level=level)
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into singers (id, name) values (1, 'Some Singer')"
                )
                self.assertEqual(1, cursor.rowcount)
            connection.commit()
            begin_requests = list(
                filter(
                    lambda msg: isinstance(msg, BeginTransactionRequest),
                    self.spanner_service.requests,
                )
            )
            self.assertEqual(1, len(begin_requests))
            self.assertEqual(begin_requests[0].options.isolation_level, level)
            MockServerTestBase.spanner_service.clear_requests()

    def test_transaction_isolation_level(self):
        connection = Connection(self.instance, self.database)
        for level in [
            TransactionOptions.IsolationLevel.ISOLATION_LEVEL_UNSPECIFIED,
            TransactionOptions.IsolationLevel.REPEATABLE_READ,
            TransactionOptions.IsolationLevel.SERIALIZABLE,
        ]:
            connection.begin(isolation_level=level)
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into singers (id, name) values (1, 'Some Singer')"
                )
                self.assertEqual(1, cursor.rowcount)
            connection.commit()
            begin_requests = list(
                filter(
                    lambda msg: isinstance(msg, BeginTransactionRequest),
                    self.spanner_service.requests,
                )
            )
            self.assertEqual(1, len(begin_requests))
            self.assertEqual(begin_requests[0].options.isolation_level, level)
            MockServerTestBase.spanner_service.clear_requests()

    def test_begin_isolation_level(self):
        connection = Connection(self.instance, self.database)
        for level in [
            TransactionOptions.IsolationLevel.REPEATABLE_READ,
            TransactionOptions.IsolationLevel.SERIALIZABLE,
        ]:
            isolation_level_name = level.name.replace("_", " ")
            with connection.cursor() as cursor:
                cursor.execute(f"begin isolation level {isolation_level_name}")
                cursor.execute(
                    "insert into singers (id, name) values (1, 'Some Singer')"
                )
                self.assertEqual(1, cursor.rowcount)
            connection.commit()
            begin_requests = list(
                filter(
                    lambda msg: isinstance(msg, BeginTransactionRequest),
                    self.spanner_service.requests,
                )
            )
            self.assertEqual(1, len(begin_requests))
            self.assertEqual(begin_requests[0].options.isolation_level, level)
            MockServerTestBase.spanner_service.clear_requests()

    def test_begin_invalid_isolation_level(self):
        connection = Connection(self.instance, self.database)
        with connection.cursor() as cursor:
            with self.assertRaises(Unknown):
                cursor.execute("begin isolation level does_not_exist")
