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

pytest.importorskip("pytest_snapshot")


def _apply_unary_op(obj: bpd.DataFrame, op: ops.UnaryOp, arg: str) -> str:
    array_value = obj._block.expr
    op_expr = op.as_expr(arg)
    result, col_ids = array_value.compute_values([op_expr])

    # Rename columns for deterministic golden SQL results.
    assert len(col_ids) == 1
    result = result.rename_columns({col_ids[0]: arg}).select_columns([arg])

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_arccosh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arccosh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arccos(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arccos_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arcsin(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arcsin_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arcsinh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arcsinh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arctan(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arctan_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arctanh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arctanh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_abs(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.abs_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_capitalize(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.capitalize_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_ceil(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.ceil_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_date(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.date_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_day(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.day_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_dayofweek(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.dayofweek_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_dayofyear(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.dayofyear_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_exp(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.exp_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_expm1(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.expm1_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_floor_dt(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.FloorDtOp("DAY"), "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_floor(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.floor_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_area(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_area_op, "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_astext(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_st_astext_op, "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_boundary(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_st_boundary_op, "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_geogfromtext(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_st_geogfromtext_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_isclosed(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_st_isclosed_op, "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_length(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.GeoStLengthOp(True), "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_x(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_x_op, "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_geo_y(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["geography_col"]]
    sql = _apply_unary_op(bf_df, ops.geo_y_op, "geography_col")

    snapshot.assert_match(sql, "out.sql")


def test_array_to_string(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, ops.ArrayToStringOp(delimiter="."), "string_list_col")

    snapshot.assert_match(sql, "out.sql")


def test_array_index(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, convert_index(1), "string_list_col")

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_only_start(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, convert_slice(slice(1, None)), "string_list_col")

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_start_and_stop(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, convert_slice(slice(1, 5)), "string_list_col")

    snapshot.assert_match(sql, "out.sql")


def test_cos(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.cos_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_cosh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.cosh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_hash(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.hash_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_hour(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.hour_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_invert(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.invert_op, "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_is_in(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.IsInOp(values=(1, 2, 3)), "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_isalnum(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isalnum_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isalpha(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isalpha_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isdecimal(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isdecimal_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isdigit(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isdigit_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_islower(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.islower_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isnumeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isnumeric_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isspace(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isspace_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isupper(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isupper_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_len(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.len_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_ln(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.ln_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_log10(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.log10_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_log1p(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.log1p_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_lower(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.lower_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_lstrip(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrLstripOp(" "), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_minute(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.minute_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_month(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.month_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_neg(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.neg_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_normalize(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.normalize_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_pos(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.pos_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_quarter(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.quarter_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_reverse(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.reverse_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_second(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.second_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_rstrip(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrRstripOp(" "), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_sqrt(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.sqrt_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_str_get(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrGetOp(1), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_str_slice(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrSliceOp(1, 3), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_strftime(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.StrftimeOp("%Y-%m-%d"), "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_struct_field(nested_structs_types_df: bpd.DataFrame, snapshot):
    bf_df = nested_structs_types_df[["people"]]

    # When a name string is provided.
    sql = _apply_unary_op(bf_df, ops.StructFieldOp("name"), "people")
    snapshot.assert_match(sql, "out.sql")

    # When an index integer is provided.
    sql = _apply_unary_op(bf_df, ops.StructFieldOp(0), "people")
    snapshot.assert_match(sql, "out.sql")


def test_str_contains(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrContainsOp("e"), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_str_contains_regex(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrContainsRegexOp("e"), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_strip(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.StrStripOp(" "), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_iso_day(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.iso_day_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_iso_week(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.iso_week_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_iso_year(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.iso_year_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_isnull(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.isnull_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_notnull(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.notnull_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_sin(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.sin_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_sinh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.sinh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_tan(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.tan_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_tanh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.tanh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_time(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.time_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_to_datetime(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.ToDatetimeOp(), "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_to_timestamp(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.ToTimestampOp(), "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_to_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.ToTimedeltaOp("s"), "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_unix_micros(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.UnixMicros(), "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_unix_millis(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.UnixMillis(), "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_unix_seconds(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.UnixSeconds(), "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_timedelta_floor(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.timedelta_floor_op, "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_json_extract(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONExtract(json_path="$"), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_json_extract_array(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONExtractArray(json_path="$"), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_json_extract_string_array(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONExtractStringArray(json_path="$"), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_json_query(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONQuery(json_path="$"), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_json_query_array(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONQueryArray(json_path="$"), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_json_value(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONValue(json_path="$"), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_parse_json(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.ParseJSON(), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_to_json_string(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.ToJSONString(), "json_col")

    snapshot.assert_match(sql, "out.sql")


def test_upper(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.upper_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_year(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.year_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")
