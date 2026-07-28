# Copyright 2026 Google LLC
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

from sqlalchemy import Column, MetaData, Table, types
from sqlalchemy.schema import CreateTable
from sqlalchemy.testing import eq_, fixtures
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import (
    SpannerDialect,
    _type_map,
    _type_map_inv,
)


class UuidTest(fixtures.TestBase):
    def test_uuid_type_mapping(self):
        """Test UUID is registered in _type_map and _type_map_inv."""
        assert "UUID" in _type_map
        eq_(_type_map["UUID"], types.UUID)
        assert types.UUID in _type_map_inv
        eq_(_type_map_inv[types.UUID], "UUID")
        assert types.Uuid in _type_map_inv
        eq_(_type_map_inv[types.Uuid], "UUID")

    def test_uuid_designate_type(self):
        """Test reflecting UUID type string returns types.UUID."""
        dialect = SpannerDialect()
        assert dialect.supports_native_uuid is False
        col_type = dialect._designate_type("UUID")
        eq_(col_type, types.UUID)

    def test_uuid_ddl_compilation_default(self):
        """Test DDL compilation: types.Uuid emits STRING(36) by default and
        types.UUID emits UUID by default.
        """
        dialect = SpannerDialect()
        metadata = MetaData()
        table = Table(
            "test_uuid_table",
            metadata,
            Column("legacy_id", types.Uuid, primary_key=True),
            Column("native_id", types.UUID),
        )
        statement = str(CreateTable(table).compile(dialect=dialect)).strip()
        assert "legacy_id STRING(36) NOT NULL" in statement
        assert "native_id UUID" in statement

    def test_uuid_ddl_compilation_native_enabled(self):
        """Test DDL compilation emits UUID type for types.Uuid when supports_native_uuid
        is set to True on dialect.
        """
        dialect = SpannerDialect()
        dialect.supports_native_uuid = True
        metadata = MetaData()
        table = Table(
            "test_uuid_table",
            metadata,
            Column("user_id", types.Uuid, primary_key=True),
        )
        statement = str(CreateTable(table).compile(dialect=dialect)).strip()
        assert "user_id UUID NOT NULL" in statement

    def test_uuid_python_conversion_legacy(self):
        """Test that types.Uuid automatically converts uuid.UUID to/from str
        when native_uuid is False.
        """
        import uuid

        dialect = SpannerDialect()
        dialect.supports_native_uuid = False
        uuid_type = types.Uuid()
        test_uuid = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")

        # Test bind processor converts uuid.UUID -> str
        bind_proc = uuid_type.bind_processor(dialect)
        eq_(bind_proc(test_uuid), "123e4567e89b12d3a456426614174000")

        # Test result processor converts str -> uuid.UUID
        res_proc = uuid_type.result_processor(dialect, "STRING")
        eq_(res_proc("123e4567-e89b-12d3-a456-426614174000"), test_uuid)
