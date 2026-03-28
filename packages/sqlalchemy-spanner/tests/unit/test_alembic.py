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

from alembic.ddl import base as ddl_base
from google.cloud.sqlalchemy_spanner import sqlalchemy_spanner
from sqlalchemy import String, TextClause
from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures


class TestAlembicTest(fixtures.TestBase):
    def test_visit_column_nullable_with_not_null_column(self):
        ddl = sqlalchemy_spanner.visit_column_nullable(
            ddl_base.ColumnNullable(
                name="tbl", column_name="col", nullable=False, existing_type=String(256)
            ),
            sqlalchemy_spanner.SpannerDDLCompiler(
                sqlalchemy_spanner.SpannerDialect(), None
            ),
        )
        eq_(ddl, "ALTER TABLE tbl ALTER COLUMN col STRING(256) NOT NULL")

    def test_visit_column_nullable_with_nullable_column(self):
        ddl = sqlalchemy_spanner.visit_column_nullable(
            ddl_base.ColumnNullable(
                name="tbl", column_name="col", nullable=True, existing_type=String(256)
            ),
            sqlalchemy_spanner.SpannerDDLCompiler(
                sqlalchemy_spanner.SpannerDialect(), None
            ),
        )
        eq_(ddl, "ALTER TABLE tbl ALTER COLUMN col STRING(256)")

    def test_visit_column_nullable_with_default(self):
        ddl = sqlalchemy_spanner.visit_column_nullable(
            ddl_base.ColumnNullable(
                name="tbl",
                column_name="col",
                nullable=False,
                existing_type=String(256),
                existing_server_default=TextClause("GENERATE_UUID()"),
            ),
            sqlalchemy_spanner.SpannerDDLCompiler(
                sqlalchemy_spanner.SpannerDialect(), None
            ),
        )
        eq_(
            ddl,
            "ALTER TABLE tbl "
            "ALTER COLUMN col "
            "STRING(256) NOT NULL DEFAULT (GENERATE_UUID())",
        )

    def test_visit_column_type(self):
        ddl = sqlalchemy_spanner.visit_column_type(
            ddl_base.ColumnType(
                name="tbl",
                column_name="col",
                type_=String(256),
                existing_nullable=True,
            ),
            sqlalchemy_spanner.SpannerDDLCompiler(
                sqlalchemy_spanner.SpannerDialect(), None
            ),
        )
        eq_(ddl, "ALTER TABLE tbl ALTER COLUMN col STRING(256)")

    def test_visit_column_type_with_default(self):
        ddl = sqlalchemy_spanner.visit_column_type(
            ddl_base.ColumnType(
                name="tbl",
                column_name="col",
                type_=String(256),
                existing_nullable=False,
                existing_server_default=TextClause("GENERATE_UUID()"),
            ),
            sqlalchemy_spanner.SpannerDDLCompiler(
                sqlalchemy_spanner.SpannerDialect(), None
            ),
        )
        eq_(
            ddl,
            "ALTER TABLE tbl "
            "ALTER COLUMN col "
            "STRING(256) NOT NULL DEFAULT (GENERATE_UUID())",
        )
