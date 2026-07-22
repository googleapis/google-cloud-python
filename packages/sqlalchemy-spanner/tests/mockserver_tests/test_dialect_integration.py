# Copyright 2026 Google LLC All rights reserved.
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

from google.cloud.spanner_admin_database_v1 import UpdateDatabaseDdlRequest
from google.cloud.spanner_v1 import ResultSet
from sqlalchemy import Column, Index, MetaData, Table, Uuid, types
from sqlalchemy.testing import eq_, is_instance_of

from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_result,
)


class TestDialectIntegration(MockServerTestBase):
    def test_create_table_with_native_uuid(self):
        """Integration test verifying native UUID and TOKENLIST DDL generation."""
        add_result(
            """SELECT true
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA="" AND TABLE_NAME="products"
LIMIT 1
""",
            ResultSet(),
        )
        engine = self.create_engine()
        metadata = MetaData()
        Table(
            "products",
            metadata,
            Column("product_id", Uuid, primary_key=True),
            Column("token_data", types.String()),
        )
        metadata.create_all(engine)
        requests = self.database_admin_service.requests
        eq_(1, len(requests))
        is_instance_of(requests[0], UpdateDatabaseDdlRequest)
        statement = requests[0].statements[0]
        assert "product_id UUID NOT NULL" in statement

    def test_create_index_with_storing_clause(self):
        """Integration test verifying DDL generation for indexes with STORING clause."""
        add_result(
            """SELECT true
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA="" AND TABLE_NAME="items"
LIMIT 1
""",
            ResultSet(),
        )
        engine = self.create_engine()
        metadata = MetaData()
        items = Table(
            "items",
            metadata,
            Column("id", Uuid, primary_key=True),
            Column("category", types.String(50)),
            Column("name", types.String(100)),
            Column("description", types.String(500)),
        )
        Index(
            "ix_items_category",
            items.c.category,
            spanner_storing=["name", "description"],
        )
        metadata.create_all(engine)
        requests = self.database_admin_service.requests
        eq_(1, len(requests))
        is_instance_of(requests[0], UpdateDatabaseDdlRequest)
        statements = requests[0].statements
        create_index_statement = [s for s in statements if "CREATE INDEX" in s][0]
        assert "STORING (name, description)" in create_index_statement
