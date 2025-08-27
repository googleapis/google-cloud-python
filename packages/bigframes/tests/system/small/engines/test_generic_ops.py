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

import re

import pytest

from bigframes.core import array_value, expression
import bigframes.dtypes
import bigframes.operations as ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


def apply_op(
    array: array_value.ArrayValue, op: ops.AsTypeOp, excluded_cols=[]
) -> array_value.ArrayValue:
    exprs = []
    labels = []
    for arg in array.column_ids:
        if arg in excluded_cols:
            continue
        try:
            _ = op.output_type(array.get_column_type(arg))
            expr = op.as_expr(arg)
            exprs.append(expr)
            type_string = re.sub(r"[^a-zA-Z\d]", "_", str(op.to_type))
            labels.append(f"{arg}_as_{type_string}")
        except TypeError:
            continue
    assert len(exprs) > 0
    new_arr, ids = array.compute_values(exprs)
    new_arr = new_arr.rename_columns(
        {new_col: label for new_col, label in zip(ids, labels)}
    )
    return new_arr


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_int(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.INT_DTYPE),
        excluded_cols=["string_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string_int(scalars_array_value: array_value.ArrayValue, engine):
    vals = ["1", "100", "-3"]
    arr, _ = scalars_array_value.compute_values(
        [
            ops.AsTypeOp(to_type=bigframes.dtypes.INT_DTYPE).as_expr(
                expression.const(val)
            )
            for val in vals
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_float(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.FLOAT_DTYPE),
        excluded_cols=["string_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string_float(
    scalars_array_value: array_value.ArrayValue, engine
):
    vals = ["1", "1.1", ".1", "1e3", "1.34235e4", "3.33333e-4"]
    arr, _ = scalars_array_value.compute_values(
        [
            ops.AsTypeOp(to_type=bigframes.dtypes.FLOAT_DTYPE).as_expr(
                expression.const(val)
            )
            for val in vals
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_bool(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value, ops.AsTypeOp(to_type=bigframes.dtypes.BOOL_DTYPE)
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string(scalars_array_value: array_value.ArrayValue, engine):
    # floats work slightly different with trailing zeroes rn
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.STRING_DTYPE),
        excluded_cols=["float64_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_numeric(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.NUMERIC_DTYPE),
        excluded_cols=["string_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string_numeric(
    scalars_array_value: array_value.ArrayValue, engine
):
    vals = ["1", "1.1", ".1", "23428975070235903.209", "-23428975070235903.209"]
    arr, _ = scalars_array_value.compute_values(
        [
            ops.AsTypeOp(to_type=bigframes.dtypes.NUMERIC_DTYPE).as_expr(
                expression.const(val)
            )
            for val in vals
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_date(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.DATE_DTYPE),
        excluded_cols=["string_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string_date(
    scalars_array_value: array_value.ArrayValue, engine
):
    vals = ["2014-08-15", "2215-08-15", "2016-02-29"]
    arr, _ = scalars_array_value.compute_values(
        [
            ops.AsTypeOp(to_type=bigframes.dtypes.DATE_DTYPE).as_expr(
                expression.const(val)
            )
            for val in vals
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_datetime(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.DATETIME_DTYPE),
        excluded_cols=["string_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string_datetime(
    scalars_array_value: array_value.ArrayValue, engine
):
    vals = ["2014-08-15 08:15:12", "2015-08-15 08:15:12.654754", "2016-02-29 00:00:00"]
    arr, _ = scalars_array_value.compute_values(
        [
            ops.AsTypeOp(to_type=bigframes.dtypes.DATETIME_DTYPE).as_expr(
                expression.const(val)
            )
            for val in vals
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_timestamp(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.TIMESTAMP_DTYPE),
        excluded_cols=["string_col"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_string_timestamp(
    scalars_array_value: array_value.ArrayValue, engine
):
    vals = [
        "2014-08-15 08:15:12+00:00",
        "2015-08-15 08:15:12.654754+05:00",
        "2016-02-29 00:00:00+08:00",
    ]
    arr, _ = scalars_array_value.compute_values(
        [
            ops.AsTypeOp(to_type=bigframes.dtypes.TIMESTAMP_DTYPE).as_expr(
                expression.const(val)
            )
            for val in vals
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_time(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.TIME_DTYPE),
        excluded_cols=["string_col", "int64_col", "int64_too"],
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_from_json(scalars_array_value: array_value.ArrayValue, engine):
    exprs = [
        ops.AsTypeOp(to_type=bigframes.dtypes.INT_DTYPE).as_expr(
            expression.const("5", bigframes.dtypes.JSON_DTYPE)
        ),
        ops.AsTypeOp(to_type=bigframes.dtypes.FLOAT_DTYPE).as_expr(
            expression.const("5", bigframes.dtypes.JSON_DTYPE)
        ),
        ops.AsTypeOp(to_type=bigframes.dtypes.BOOL_DTYPE).as_expr(
            expression.const("true", bigframes.dtypes.JSON_DTYPE)
        ),
        ops.AsTypeOp(to_type=bigframes.dtypes.STRING_DTYPE).as_expr(
            expression.const('"hello world"', bigframes.dtypes.JSON_DTYPE)
        ),
    ]
    arr, _ = scalars_array_value.compute_values(exprs)

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_astype_timedelta(scalars_array_value: array_value.ArrayValue, engine):
    arr = apply_op(
        scalars_array_value,
        ops.AsTypeOp(to_type=bigframes.dtypes.TIMEDELTA_DTYPE),
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_where_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.where_op.as_expr(
                expression.deref("int64_col"),
                expression.deref("bool_col"),
                expression.deref("float64_col"),
            )
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_coalesce_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.coalesce_op.as_expr(
                expression.deref("int64_col"),
                expression.deref("float64_col"),
            )
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_fillna_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.fillna_op.as_expr(
                expression.deref("int64_col"),
                expression.deref("float64_col"),
            )
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_casewhen_op_single_case(
    scalars_array_value: array_value.ArrayValue, engine
):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.case_when_op.as_expr(
                expression.deref("bool_col"),
                expression.deref("int64_col"),
            )
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_casewhen_op_double_case(
    scalars_array_value: array_value.ArrayValue, engine
):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.case_when_op.as_expr(
                ops.gt_op.as_expr(expression.deref("int64_col"), expression.const(3)),
                expression.deref("int64_col"),
                ops.lt_op.as_expr(expression.deref("int64_col"), expression.const(-3)),
                expression.deref("int64_too"),
            )
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_isnull_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [ops.isnull_op.as_expr(expression.deref("string_col"))]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_notnull_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [ops.notnull_op.as_expr(expression.deref("string_col"))]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_invert_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.invert_op.as_expr(expression.deref("bytes_col")),
            ops.invert_op.as_expr(expression.deref("bool_col")),
        ]
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_isin_op(scalars_array_value: array_value.ArrayValue, engine):
    arr, col_ids = scalars_array_value.compute_values(
        [
            ops.IsInOp((1, 2, 3)).as_expr(expression.deref("int64_col")),
            ops.IsInOp((None, 123456)).as_expr(expression.deref("int64_col")),
            ops.IsInOp((None, 123456), match_nulls=False).as_expr(
                expression.deref("int64_col")
            ),
            ops.IsInOp((1.0, 2.0, 3.0)).as_expr(expression.deref("int64_col")),
            ops.IsInOp(("1.0", "2.0")).as_expr(expression.deref("int64_col")),
            ops.IsInOp(("1.0", 2.5, 3)).as_expr(expression.deref("int64_col")),
            ops.IsInOp(()).as_expr(expression.deref("int64_col")),
            ops.IsInOp((1, 2, 3, None)).as_expr(expression.deref("float64_col")),
        ]
    )
    new_names = (
        "int in ints",
        "int in ints w null",
        "int in ints w null wo match nulls",
        "int in floats",
        "int in strings",
        "int in mixed",
        "int in empty",
        "float in ints",
    )
    arr = arr.rename_columns(
        {old_name: new_names[i] for i, old_name in enumerate(col_ids)}
    )

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_isin_op_nested_filter(
    scalars_array_value: array_value.ArrayValue, engine
):
    isin_clause = ops.IsInOp((1, 2, 3)).as_expr(expression.deref("int64_col"))
    filter_clause = ops.invert_op.as_expr(
        ops.or_op.as_expr(
            expression.deref("bool_col"), ops.invert_op.as_expr(isin_clause)
        )
    )
    arr = scalars_array_value.filter(filter_clause)

    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)
