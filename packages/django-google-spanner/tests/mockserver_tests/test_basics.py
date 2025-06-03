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

from google.cloud.spanner_v1 import (
    BatchCreateSessionsRequest,
    ExecuteSqlRequest,
)
from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_select1_result,
    add_singer_query_result,
)
from django.db import connection

from tests.mockserver_tests.models import Singer


class TestBasics(MockServerTestBase):
    def verify_select1(self, results):
        result_list = []
        for row in results:
            result_list.append(row)
            self.assertEqual(row[0], 1)
        self.assertEqual(len(result_list), 1)
        requests = self.spanner_service.requests
        self.assertEqual(len(requests), 2)
        self.assertIsInstance(requests[0], BatchCreateSessionsRequest)
        self.assertIsInstance(requests[1], ExecuteSqlRequest)

    def test_select1(self):
        add_select1_result()
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            self.verify_select1(results)

    def test_django_select1(self):
        add_select1_result()
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            self.verify_select1(cursor.fetchall())

    def test_django_select_singer(self):
        add_singer_query_result(
            "SELECT tests_singer.id, tests_singer.first_name, tests_singer.last_name FROM tests_singer"
        )
        singers = Singer.objects.all()
        self.assertEqual(len(singers), 2)
        requests = self.spanner_service.requests
        self.assertEqual(len(requests), 2)
        self.assertIsInstance(requests[0], BatchCreateSessionsRequest)
        self.assertIsInstance(requests[1], ExecuteSqlRequest)
