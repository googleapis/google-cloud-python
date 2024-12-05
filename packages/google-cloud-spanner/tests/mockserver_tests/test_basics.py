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

from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
from google.cloud.spanner_v1.testing.mock_database_admin import DatabaseAdminServicer
from google.cloud.spanner_v1.testing.mock_spanner import (
    start_mock_server,
    SpannerServicer,
)
import google.cloud.spanner_v1.types.type as spanner_type
import google.cloud.spanner_v1.types.result_set as result_set
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud.spanner_v1 import (
    Client,
    FixedSizePool,
    BatchCreateSessionsRequest,
    ExecuteSqlRequest,
)
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance
import grpc


class TestBasics(unittest.TestCase):
    server: grpc.Server = None
    spanner_service: SpannerServicer = None
    database_admin_service: DatabaseAdminServicer = None
    port: int = None

    def __init__(self, *args, **kwargs):
        super(TestBasics, self).__init__(*args, **kwargs)
        self._client = None
        self._instance = None
        self._database = None

    @classmethod
    def setUpClass(cls):
        (
            TestBasics.server,
            TestBasics.spanner_service,
            TestBasics.database_admin_service,
            TestBasics.port,
        ) = start_mock_server()

    @classmethod
    def tearDownClass(cls):
        if TestBasics.server is not None:
            TestBasics.server.stop(grace=None)
            TestBasics.server = None

    def _add_select1_result(self):
        result = result_set.ResultSet(
            dict(
                metadata=result_set.ResultSetMetadata(
                    dict(
                        row_type=spanner_type.StructType(
                            dict(
                                fields=[
                                    spanner_type.StructType.Field(
                                        dict(
                                            name="c",
                                            type=spanner_type.Type(
                                                dict(code=spanner_type.TypeCode.INT64)
                                            ),
                                        )
                                    )
                                ]
                            )
                        )
                    )
                ),
            )
        )
        result.rows.extend(["1"])
        TestBasics.spanner_service.mock_spanner.add_result("select 1", result)

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(
                project="test-project",
                credentials=AnonymousCredentials(),
                client_options=ClientOptions(
                    api_endpoint="localhost:" + str(TestBasics.port),
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
                "test-database", pool=FixedSizePool(size=10)
            )
        return self._database

    def test_select1(self):
        self._add_select1_result()
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        requests = self.spanner_service.requests
        self.assertEqual(2, len(requests), msg=requests)
        self.assertTrue(isinstance(requests[0], BatchCreateSessionsRequest))
        self.assertTrue(isinstance(requests[1], ExecuteSqlRequest))

    def test_create_table(self):
        database_admin_api = self.client.database_admin_api
        request = spanner_database_admin.UpdateDatabaseDdlRequest(
            dict(
                database=database_admin_api.database_path(
                    "test-project", "test-instance", "test-database"
                ),
                statements=[
                    "CREATE TABLE Test ("
                    "Id INT64, "
                    "Value STRING(MAX)) "
                    "PRIMARY KEY (Id)",
                ],
            )
        )
        operation = database_admin_api.update_database_ddl(request)
        operation.result(1)
