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

import json

from packaging import version
import pytest
import sqlglot

from bigframes import dataframe
from bigframes import operations as ops
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")

CONNECTION_ID = "bigframes-dev.us.bigframes-default-connection"


def test_ai_generate(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerate(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_model_param(scalar_types_df: dataframe.DataFrame, snapshot):
    if version.Version(sqlglot.__version__) < version.Version("25.18.0"):
        pytest.skip(
            "Skip test because SQLGLot cannot compile model params to JSON at this version."
        )

    col_name = "string_col"

    op = ops.AIGenerate(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerateBool(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    if version.Version(sqlglot.__version__) < version.Version("25.18.0"):
        pytest.skip(
            "Skip test because SQLGLot cannot compile model params to JSON at this version."
        )

    col_name = "string_col"

    op = ops.AIGenerateBool(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerateInt(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    if version.Version(sqlglot.__version__) < version.Version("25.18.0"):
        pytest.skip(
            "Skip test because SQLGLot cannot compile model params to JSON at this version."
        )

    col_name = "string_col"

    op = ops.AIGenerateInt(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerateDouble(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    if version.Version(sqlglot.__version__) < version.Version("25.18.0"):
        pytest.skip(
            "Skip test because SQLGLot cannot compile model params to JSON at this version."
        )

    col_name = "string_col"

    op = ops.AIGenerateDouble(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_if(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIIf(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_classify(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIClassify(
        prompt_context=(None,),
        categories=("greeting", "rejection"),
        connection_id=CONNECTION_ID,
    )

    sql = utils._apply_unary_ops(scalar_types_df, [op.as_expr(col_name)], ["result"])

    snapshot.assert_match(sql, "out.sql")


def test_ai_score(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIScore(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
    )

    sql = utils._apply_unary_ops(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")
