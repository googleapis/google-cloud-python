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
import bigframes.core.expression as ex
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_capitalize(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.capitalize_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_endswith(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "single": ops.EndsWithOp(pat=("ab",)).as_expr(col_name),
        "double": ops.EndsWithOp(pat=("ab", "cd")).as_expr(col_name),
        "empty": ops.EndsWithOp(pat=()).as_expr(col_name),
    }
    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_isalnum(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.isalnum_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isalpha(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.isalpha_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isdecimal(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.isdecimal_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_isdigit(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.isdigit_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_islower(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.islower_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isnumeric(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.isnumeric_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_isspace(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.isspace_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_isupper(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.isupper_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_len(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.len_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_len_w_array(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "int_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.len_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_lower(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.lower_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_lstrip(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrLstripOp(" ").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_replace_str(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.ReplaceStrOp("e", "a").as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_regex_replace_str(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.RegexReplaceStrOp(r"e", "a").as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_reverse(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.reverse_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_rstrip(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrRstripOp(" ").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_startswith(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "single": ops.StartsWithOp(pat=("ab",)).as_expr(col_name),
        "double": ops.StartsWithOp(pat=("ab", "cd")).as_expr(col_name),
        "empty": ops.StartsWithOp(pat=()).as_expr(col_name),
    }
    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_str_get(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrGetOp(1).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_pad(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "left": ops.StrPadOp(length=10, fillchar="-", side="left").as_expr(col_name),
        "right": ops.StrPadOp(length=10, fillchar="-", side="right").as_expr(col_name),
        "both": ops.StrPadOp(length=10, fillchar="-", side="both").as_expr(col_name),
    }
    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_str_slice(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrSliceOp(1, 3).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_strip(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrStripOp(" ").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_contains(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrContainsOp("e").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_contains_regex(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrContainsRegexOp("e").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_str_extract(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    ops_map = {
        "zero": ops.StrExtractOp(r"([a-z]*)", 0).as_expr(col_name),
        "one": ops.StrExtractOp(r"([a-z]*)", 1).as_expr(col_name),
    }
    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))

    snapshot.assert_match(sql, "out.sql")


def test_str_repeat(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StrRepeatOp(2).as_expr(col_name)], [col_name]
    )
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
    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))

    snapshot.assert_match(sql, "out.sql")


def test_string_split(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.StringSplitOp(pat=",").as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_upper(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.upper_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_zfill(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.ZfillOp(width=10).as_expr(col_name)], [col_name]
    )
    snapshot.assert_match(sql, "out.sql")


def test_add_string(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = utils._apply_binary_op(bf_df, ops.add_op, "string_col", ex.const("a"))

    snapshot.assert_match(sql, "out.sql")


def test_strconcat(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = utils._apply_binary_op(bf_df, ops.strconcat_op, "string_col", ex.const("a"))

    snapshot.assert_match(sql, "out.sql")
