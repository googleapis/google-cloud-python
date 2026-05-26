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

import pytest

import bigframes.dataframe as dataframe
from bigframes import dtypes
from bigframes.operations.googlesql import ArgSpec, GoogleSqlScalarOp, apply_op

# Define standard Google SQL operations to test with
GREATEST_OP = GoogleSqlScalarOp(
    sql_name="GREATEST",
    args=(ArgSpec(arg_name="x"), ArgSpec(arg_name="y")),
    signature=lambda x, y: dtypes.INT_DTYPE,
)

CONCAT_OP = GoogleSqlScalarOp(
    sql_name="CONCAT",
    args=(ArgSpec(arg_name="a"), ArgSpec(arg_name="b")),
    signature=lambda a, b: dtypes.STRING_DTYPE,
)


def test_apply_op_positional_series(scalar_types_df: dataframe.DataFrame):
    s1 = scalar_types_df["int64_col"]
    s2 = scalar_types_df["int64_too"]

    result = apply_op(GREATEST_OP, args=(s1, s2))

    # Compile the resulting Series' underlying ArrayValue to SQL
    array_value = result._block.expr
    sql = array_value.session._executor.to_sql(array_value, enable_cache=False)
    
    assert "GREATEST(" in sql
    assert "`int64_col`" in sql
    assert "`int64_too`" in sql


def test_apply_op_keyword_series(scalar_types_df: dataframe.DataFrame):
    s1 = scalar_types_df["int64_col"]
    s2 = scalar_types_df["int64_too"]

    result = apply_op(GREATEST_OP, kwargs={"x": s1, "y": s2})

    array_value = result._block.expr
    sql = array_value.session._executor.to_sql(array_value, enable_cache=False)

    assert "GREATEST(" in sql
    assert "x => `int64_col`" in sql
    assert "y => `int64_too`" in sql


def test_apply_op_mixed_series_and_literal(scalar_types_df: dataframe.DataFrame):
    s1 = scalar_types_df["int64_col"]

    result = apply_op(GREATEST_OP, args=(s1, 15))

    array_value = result._block.expr
    sql = array_value.session._executor.to_sql(array_value, enable_cache=False)

    assert "GREATEST(" in sql
    assert "`int64_col`" in sql
    assert "15" in sql


def test_apply_op_string_concat(scalar_types_df: dataframe.DataFrame):
    s1 = scalar_types_df["string_col"]

    result = apply_op(CONCAT_OP, args=(s1, "world"))

    array_value = result._block.expr
    sql = array_value.session._executor.to_sql(array_value, enable_cache=False)

    assert "CONCAT(" in sql
    assert "`string_col`" in sql
    assert "'world'" in sql
