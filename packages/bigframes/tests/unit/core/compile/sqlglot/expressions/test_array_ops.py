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

import pytest

from bigframes import operations as ops
from bigframes.operations._op_converters import convert_index, convert_slice
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_array_to_string(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.ArrayToStringOp(delimiter=".").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_index(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [convert_index(1).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_only_start(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [convert_slice(slice(1, None)).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_start_and_stop(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [convert_slice(slice(1, 5)).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")
