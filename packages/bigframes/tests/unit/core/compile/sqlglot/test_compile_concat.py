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

from bigframes.core import ordering
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_compile_concat(scalar_types_df: bpd.DataFrame, snapshot):
    # TODO: concat two same dataframes, which SQL does not get reused.
    df1 = scalar_types_df[["rowindex", "int64_col", "string_col"]]
    concat_df = bpd.concat([df1, df1])
    snapshot.assert_match(concat_df.sql, "out.sql")


def test_compile_concat_filter_sorted(scalar_types_df: bpd.DataFrame, snapshot):
    scalars_array_value = scalar_types_df._block.expr
    input_1 = scalars_array_value.select_columns(["float64_col", "int64_col"]).order_by(
        [ordering.ascending_over("int64_col")]
    )
    input_2 = scalars_array_value.filter_by_id("bool_col").select_columns(
        ["float64_col", "int64_too"]
    )

    result = input_1.concat([input_2, input_1, input_2])

    new_names = ["float64_col", "int64_col"]
    col_ids = {
        old_name: new_name for old_name, new_name in zip(result.column_ids, new_names)
    }
    result = result.rename_columns(col_ids).select_columns(new_names)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    snapshot.assert_match(sql, "out.sql")
