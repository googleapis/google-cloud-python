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

import typing

import pytest

from bigframes import operations as ops
from bigframes.core import expression as expr
from bigframes.operations._op_converters import convert_index, convert_slice
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_unary_ops(
    obj: bpd.DataFrame,
    ops_list: typing.Sequence[expr.Expression],
    new_names: typing.Sequence[str],
) -> str:
    array_value = obj._block.expr
    result, old_names = array_value.compute_values(ops_list)

    # Rename columns for deterministic golden SQL results.
    assert len(old_names) == len(new_names)
    col_ids = {old_name: new_name for old_name, new_name in zip(old_names, new_names)}
    result = result.rename_columns(col_ids).select_columns(new_names)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_arccosh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.arccosh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arccos(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.arccos_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arcsin(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.arcsin_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arcsinh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.arcsinh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arctan(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.arctan_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arctanh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.arctanh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_abs(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.abs_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_capitalize(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.capitalize_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_ceil(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ceil_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_date(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.date_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_day(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.day_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_dayofweek(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.dayofweek_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_dayofyear(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.dayofyear_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_endswith(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "single": ops.EndsWithOp(pat=("ab",)).as_expr(col_name),
        "double": ops.EndsWithOp(pat=("ab", "cd")).as_expr(col_name),
        "empty": ops.EndsWithOp(pat=()).as_expr(col_name),
    }
    sql = _apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_exp(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.exp_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_expm1(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.expm1_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_floor_dt(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.FloorDtOp("D").as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_floor(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.floor_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_geo_area(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.geo_area_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_astext(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.geo_st_astext_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_boundary(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.geo_st_boundary_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_buffer(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.GeoStBufferOp(1.0, 8.0, False).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_centroid(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.geo_st_centroid_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_convexhull(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.geo_st_convexhull_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_geogfromtext(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.geo_st_geogfromtext_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_isclosed(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.geo_st_isclosed_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_length(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.GeoStLengthOp(True).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_x(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.geo_x_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_geo_y(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.geo_y_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_array_to_string(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.ArrayToStringOp(delimiter=".").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_index(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [convert_index(1).as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_only_start(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [convert_slice(slice(1, None)).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_start_and_stop(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [convert_slice(slice(1, 5)).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_cos(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.cos_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_cosh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.cosh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_hash(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.hash_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_hour(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.hour_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_invert(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.invert_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_is_in(scalar_types_df: bpd.DataFrame, snapshot):
    int_col = "int64_col"
    float_col = "float64_col"
    bf_df = scalar_types_df[[int_col, float_col]]
    ops_map = {
        "ints": ops.IsInOp(values=(1, 2, 3)).as_expr(int_col),
        "ints_w_null": ops.IsInOp(values=(None, 123456)).as_expr(int_col),
        "floats": ops.IsInOp(values=(1.0, 2.0, 3.0), match_nulls=False).as_expr(
            int_col
        ),
        "strings": ops.IsInOp(values=("1.0", "2.0")).as_expr(int_col),
        "mixed": ops.IsInOp(values=("1.0", 2.5, 3)).as_expr(int_col),
        "empty": ops.IsInOp(values=()).as_expr(int_col),
        "ints_wo_match_nulls": ops.IsInOp(
            values=(None, 123456), match_nulls=False
        ).as_expr(int_col),
        "float_in_ints": ops.IsInOp(values=(1, 2, 3, None)).as_expr(float_col),
    }

    sql = _apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_isalnum(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isalnum_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isalpha(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isalpha_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isdecimal(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isdecimal_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isdigit(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isdigit_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_islower(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.islower_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isnumeric(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isnumeric_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isspace(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isspace_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isupper(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isupper_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_len(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.len_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_ln(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ln_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_log10(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.log10_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_log1p(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.log1p_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_lower(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.lower_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_map(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df,
        [ops.MapOp(mappings=(("value1", "mapped1"),)).as_expr(col_name)],
        [col_name],
    )

    snapshot.assert_match(sql, "out.sql")


def test_lstrip(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.StrLstripOp(" ").as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_minute(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.minute_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_month(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.month_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_neg(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.neg_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_normalize(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.normalize_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_obj_fetch_metadata(scalar_types_df: bpd.DataFrame, snapshot):
    blob_s = scalar_types_df["string_col"].str.to_blob()
    sql = blob_s.blob.version().to_frame().sql
    snapshot.assert_match(sql, "out.sql")


def test_obj_get_access_url(scalar_types_df: bpd.DataFrame, snapshot):
    blob_s = scalar_types_df["string_col"].str.to_blob()
    sql = blob_s.blob.read_url().to_frame().sql
    snapshot.assert_match(sql, "out.sql")


def test_pos(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.pos_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_quarter(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.quarter_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_replace_str(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.ReplaceStrOp("e", "a").as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_regex_replace_str(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.RegexReplaceStrOp(r"e", "a").as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_reverse(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.reverse_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_second(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.second_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_rstrip(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.StrRstripOp(" ").as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_sqrt(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.sqrt_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_startswith(scalar_types_df: bpd.DataFrame, snapshot):

    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "single": ops.StartsWithOp(pat=("ab",)).as_expr(col_name),
        "double": ops.StartsWithOp(pat=("ab", "cd")).as_expr(col_name),
        "empty": ops.StartsWithOp(pat=()).as_expr(col_name),
    }
    sql = _apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_str_get(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.StrGetOp(1).as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_str_pad(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "left": ops.StrPadOp(length=10, fillchar="-", side="left").as_expr(col_name),
        "right": ops.StrPadOp(length=10, fillchar="-", side="right").as_expr(col_name),
        "both": ops.StrPadOp(length=10, fillchar="-", side="both").as_expr(col_name),
    }
    sql = _apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_str_slice(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.StrSliceOp(1, 3).as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_strftime(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.StrftimeOp("%Y-%m-%d").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_struct_field(nested_structs_types_df: bpd.DataFrame, snapshot):
    col_name = "people"
    bf_df = nested_structs_types_df[[col_name]]

    ops_map = {
        # When a name string is provided.
        "string": ops.StructFieldOp("name").as_expr(col_name),
        # When an index integer is provided.
        "int": ops.StructFieldOp(0).as_expr(col_name),
    }
    sql = _apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))

    snapshot.assert_match(sql, "out.sql")


def test_str_contains(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.StrContainsOp("e").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_contains_regex(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.StrContainsRegexOp("e").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_extract(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.StrExtractOp(r"([a-z]*)", 1).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_repeat(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.StrRepeatOp(2).as_expr(col_name)], [col_name])
    snapshot.assert_match(sql, "out.sql")


def test_str_find(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "none_none": ops.StrFindOp("e", start=None, end=None).as_expr(col_name),
        "start_none": ops.StrFindOp("e", start=2, end=None).as_expr(col_name),
        "none_end": ops.StrFindOp("e", start=None, end=5).as_expr(col_name),
        "start_end": ops.StrFindOp("e", start=2, end=5).as_expr(col_name),
    }
    sql = _apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))

    snapshot.assert_match(sql, "out.sql")


def test_strip(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.StrStripOp(" ").as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_day(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.iso_day_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_week(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.iso_week_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_year(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.iso_year_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isnull(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.isnull_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_notnull(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.notnull_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_sin(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.sin_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_sinh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.sinh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_string_split(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.StringSplitOp(pat=",").as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_tan(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.tan_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_tanh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.tanh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_time(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.time_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_to_datetime(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ToDatetimeOp().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_to_timestamp(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ToTimestampOp().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_to_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    bf_df["duration_us"] = bpd.to_timedelta(bf_df["int64_col"], "us")
    bf_df["duration_s"] = bpd.to_timedelta(bf_df["int64_col"], "s")
    bf_df["duration_w"] = bpd.to_timedelta(bf_df["int64_col"], "W")

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_unix_micros(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.UnixMicros().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_unix_millis(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.UnixMillis().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_unix_seconds(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.UnixSeconds().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_timedelta_floor(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.timedelta_floor_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_extract(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.JSONExtract(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_extract_array(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.JSONExtractArray(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_extract_string_array(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.JSONExtractStringArray(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_query(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.JSONQuery(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_query_array(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.JSONQueryArray(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_value(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(
        bf_df, [ops.JSONValue(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_parse_json(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ParseJSON().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_to_json_string(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ToJSONString().as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_upper(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.upper_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_year(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.year_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_zfill(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = _apply_unary_ops(bf_df, [ops.ZfillOp(width=10).as_expr(col_name)], [col_name])
    snapshot.assert_match(sql, "out.sql")
