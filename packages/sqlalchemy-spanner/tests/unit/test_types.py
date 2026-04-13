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

import warnings

from sqlalchemy import types
from sqlalchemy.testing.plugin.plugin_base import fixtures

from google.cloud.sqlalchemy_spanner import sqlalchemy_spanner


class TestDesignateType(fixtures.TestBase):
    """Unit tests for SpannerDialect._designate_type."""

    def setup_method(self):
        self.dialect = sqlalchemy_spanner.SpannerDialect()

    def test_known_types(self):
        assert isinstance(self.dialect._designate_type("BOOL"), types.Boolean)
        assert isinstance(self.dialect._designate_type("INT64"), types.BIGINT)
        assert isinstance(self.dialect._designate_type("FLOAT64"), types.Float)
        assert isinstance(self.dialect._designate_type("DATE"), types.DATE)
        assert isinstance(self.dialect._designate_type("TIMESTAMP"), types.TIMESTAMP)
        assert isinstance(self.dialect._designate_type("JSON"), types.JSON)

    def test_string_with_length(self):
        result = self.dialect._designate_type("STRING(255)")
        assert isinstance(result, types.String)
        assert result.length == 255

    def test_bytes_with_length(self):
        result = self.dialect._designate_type("BYTES(1024)")
        assert isinstance(result, types.LargeBinary)
        assert result.length == 1024

    def test_tokenlist_returns_tokenlist_type(self):
        result = self.dialect._designate_type("TOKENLIST")
        assert isinstance(result, sqlalchemy_spanner.TOKENLIST)

    def test_unknown_type_returns_nulltype_with_warning(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = self.dialect._designate_type("SOME_FUTURE_TYPE")
        assert isinstance(result, types.NullType)
        assert len(caught) == 1
        assert "SOME_FUTURE_TYPE" in str(caught[0].message)

    def test_array_of_known_type(self):
        result = self.dialect._designate_type("ARRAY<INT64>")
        assert isinstance(result, types.ARRAY)


class TestTokenlistType(fixtures.TestBase):
    """Verify TOKENLIST is a proper first-class type."""

    def test_in_type_map(self):
        assert "TOKENLIST" in sqlalchemy_spanner._type_map
        assert sqlalchemy_spanner._type_map["TOKENLIST"] is sqlalchemy_spanner.TOKENLIST

    def test_in_inverse_type_map(self):
        assert sqlalchemy_spanner.TOKENLIST in sqlalchemy_spanner._type_map_inv
        assert sqlalchemy_spanner._type_map_inv[sqlalchemy_spanner.TOKENLIST] == "TOKENLIST"

    def test_type_compiler_roundtrip(self):
        compiler = sqlalchemy_spanner.SpannerTypeCompiler(
            sqlalchemy_spanner.SpannerDialect()
        )
        assert compiler.process(sqlalchemy_spanner.TOKENLIST()) == "TOKENLIST"

    def test_is_type_engine(self):
        assert issubclass(sqlalchemy_spanner.TOKENLIST, types.TypeEngine)
