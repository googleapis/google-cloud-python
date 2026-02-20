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
Base class for tests using the mock Spanner server.
"""
import logging
import unittest

from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud.spanner_admin_database_v1.types import DatabaseDialect
from google.cloud.spanner_v1 import (
    Client,
    FixedSizePool,
    ResultSet,
    Type,
    TypeCode,
)
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance
from google.cloud.spanner_v1.types import StructType
import google.cloud.spanner_v1.types.result_set as result_set
import google.cloud.spanner_v1.types.type as spanner_type
import grpc

from spannermockserver.mock_database_admin import DatabaseAdminServicer
from spannermockserver.mock_spanner import SpannerServicer, start_mock_server


class MockServerTestBase(unittest.TestCase):
    """
    Base class for tests using the mock Spanner server.
    """

    server: grpc.Server = None
    spanner_service: SpannerServicer = None
    database_admin_service: DatabaseAdminServicer = None
    port: int = None
    logger: logging.Logger = None

    def __init__(self, *args, **kwargs):
        super(MockServerTestBase, self).__init__(*args, **kwargs)
        self._client = None
        self._instance = None
        self._database = None
        self.logger = logging.getLogger("MockServerTestBase")
        self.logger.setLevel(logging.WARN)

    @classmethod
    def setUpClass(cls):
        """Sets up the mock server before any tests run."""
        (
            MockServerTestBase.server,
            MockServerTestBase.spanner_service,
            MockServerTestBase.database_admin_service,
            MockServerTestBase.port,
        ) = start_mock_server()

    @classmethod
    def tearDownClass(cls):
        """Tears down the mock server after all tests have run."""
        if MockServerTestBase.server is not None:
            MockServerTestBase.server.stop(grace=None)
            Client.NTH_CLIENT.reset()
            MockServerTestBase.server = None

    def setUp(self, *args, **kwargs):
        """Sets up the test method."""
        self._client = None
        self._instance = None
        self._database = None

    def tearDown(self, *args, **kwargs):
        """Tears down the test method."""
        MockServerTestBase.spanner_service.clear_requests()
        MockServerTestBase.database_admin_service.clear_requests()
        mock_spanner = MockServerTestBase.spanner_service.mock_spanner
        mock_spanner.results = {}
        mock_spanner.execute_streaming_sql_results = {}
        mock_spanner.errors = {}

    @property
    def client(self) -> Client:
        """Returns a Spanner client connected to the mock server."""
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
        """Returns a Spanner instance."""
        if self._instance is None:
            self._instance = self.client.instance("test-instance")
        return self._instance

    @property
    def database(self) -> Database:
        """Returns a Spanner database."""
        if self._database is None:
            self._database = self.instance.database(
                "test-database",
                pool=FixedSizePool(size=10),
                enable_interceptors_in_tests=True,
                logger=self.logger,
            )
        return self._database


def add_result(sql: str, result: result_set.ResultSet):
    MockServerTestBase.spanner_service.mock_spanner.add_result(sql, result)


def set_database_dialect(
    dialect: DatabaseDialect = DatabaseDialect.GOOGLE_STANDARD_SQL,
):

    sql = (
        "select option_value from information_schema.database_options"
        " where option_name='database_dialect'"
    )
    result = ResultSet()
    result.metadata.row_type.fields.append(
        StructType.Field(name="option_value", type=Type(code=TypeCode.STRING))
    )
    result.rows.append([dialect.name])
    add_result(sql, result)


def add_result_select_1():
    add_single_result("select 1", "c", TypeCode.INT64, [("1",)])


def add_single_result(
    sql: str, column_name: str, type_code: spanner_type.TypeCode, row
):
    metadata = result_set.ResultSetMetadata(
        row_type=spanner_type.StructType(
            fields=[
                spanner_type.StructType.Field(
                    name=column_name,
                    type=spanner_type.Type(code=type_code),
                )
            ]
        )
    )
    result = result_set.ResultSet(metadata=metadata)
    result.rows.extend(row)
    MockServerTestBase.spanner_service.mock_spanner.add_result(sql, result)
