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


# Note that the tests in this files uses fake models for deterministic results.
# Tests that use real LLM models are under system/large/test_ai.py

import pandas as pd
import pandas.testing
import pytest

import bigframes
from bigframes import dataframe, dtypes
from bigframes.ml import llm
import bigframes.operations.ai
from bigframes.testing import utils

AI_OP_EXP_OPTION = "experiments.ai_operators"
THRESHOLD_OPTION = "compute.ai_ops_confirmation_threshold"
AI_FORECAST_COLUMNS = [
    "forecast_timestamp",
    "forecast_value",
    "confidence_level",
    "prediction_interval_lower_bound",
    "prediction_interval_upper_bound",
    "ai_forecast_status",
]


class FakeGeminiTextGenerator(llm.GeminiTextGenerator):
    def __init__(self, prediction):
        self.prediction = prediction

    def predict(self, *args, **kwargs):
        return self.prediction


@pytest.mark.parametrize(
    ("func", "kwargs"),
    [
        pytest.param(
            bigframes.operations.ai.AIAccessor.filter,
            {"instruction": None, "model": None},
            id="filter",
        ),
        pytest.param(
            bigframes.operations.ai.AIAccessor.map,
            {"instruction": None, "model": None},
            id="map",
        ),
        pytest.param(
            bigframes.operations.ai.AIAccessor.classify,
            {"instruction": None, "model": None, "labels": None},
            id="classify",
        ),
        pytest.param(
            bigframes.operations.ai.AIAccessor.join,
            {"other": None, "instruction": None, "model": None},
            id="join",
        ),
        pytest.param(
            bigframes.operations.ai.AIAccessor.search,
            {"search_column": None, "query": None, "top_k": None, "model": None},
            id="search",
        ),
        pytest.param(
            bigframes.operations.ai.AIAccessor.sim_join,
            {"other": None, "left_on": None, "right_on": None, "model": None},
            id="sim_join",
        ),
    ],
)
def test_experiment_off_raise_error(session, func, kwargs):
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}, session=session
    )

    with bigframes.option_context(AI_OP_EXP_OPTION, False), pytest.raises(
        NotImplementedError
    ):
        func(df.ai, **kwargs)


def test_filter(session):
    df = dataframe.DataFrame({"col": ["A", "B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {
                "answer": [True, False],
                "full_response": _create_dummy_full_response(2),
            },
            session=session,
        ),
    )

    with bigframes.option_context(
        AI_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = df.ai.filter(
            "filter {col}",
            model=model,
        ).to_pandas()

    pandas.testing.assert_frame_equal(
        result,
        pd.DataFrame({"col": ["A"]}, dtype=dtypes.STRING_DTYPE),
        check_index_type=False,
    )


def test_map(session):
    df = dataframe.DataFrame({"col": ["A", "B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {
                "output": ["true", "false"],
                "full_response": _create_dummy_full_response(2),
            },
            session=session,
        ),
    )

    with bigframes.option_context(
        AI_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = df.ai.map(
            "map {col}", model=model, output_schema={"output": "string"}
        ).to_pandas()

    pandas.testing.assert_frame_equal(
        result,
        pd.DataFrame(
            {"col": ["A", "B"], "output": ["true", "false"]}, dtype=dtypes.STRING_DTYPE
        ),
        check_index_type=False,
    )


def test_classify(session):
    df = dataframe.DataFrame({"col": ["A", "B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {
                "result": ["A", "B"],
                "full_response": _create_dummy_full_response(2),
            },
            session=session,
        ),
    )

    with bigframes.option_context(
        AI_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = df.ai.classify(
            "classify {col}", model=model, labels=["A", "B"]
        ).to_pandas()

    pandas.testing.assert_frame_equal(
        result,
        pd.DataFrame(
            {"col": ["A", "B"], "result": ["A", "B"]}, dtype=dtypes.STRING_DTYPE
        ),
        check_index_type=False,
    )


@pytest.mark.parametrize(
    "labels",
    [
        pytest.param([], id="empty-label"),
        pytest.param(["A", "A", "B"], id="duplicate-labels"),
    ],
)
def test_classify_invalid_labels_raise_error(session, labels):
    df = dataframe.DataFrame({"col": ["A", "B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {
                "result": ["A", "B"],
                "full_response": _create_dummy_full_response(2),
            },
            session=session,
        ),
    )

    with bigframes.option_context(
        AI_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ), pytest.raises(ValueError):
        df.ai.classify("classify {col}", model=model, labels=labels)


def test_join(session):
    left_df = dataframe.DataFrame({"col_A": ["A"]}, session=session)
    right_df = dataframe.DataFrame({"col_B": ["B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {
                "answer": [True],
                "full_response": _create_dummy_full_response(1),
            },
            session=session,
        ),
    )

    with bigframes.option_context(
        AI_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = left_df.ai.join(
            right_df, "join {col_A} and {col_B}", model
        ).to_pandas()

    pandas.testing.assert_frame_equal(
        result,
        pd.DataFrame({"col_A": ["A"], "col_B": ["B"]}, dtype=dtypes.STRING_DTYPE),
        check_index_type=False,
    )


def test_forecast_default(time_series_df_default_index: dataframe.DataFrame):
    df = time_series_df_default_index[time_series_df_default_index["id"] == "1"]

    result = df.ai.forecast(timestamp_column="parsed_date", data_column="total_visits")

    utils.check_pandas_df_schema_and_index(
        result,
        columns=AI_FORECAST_COLUMNS,
        index=10,
    )


def test_forecast_w_params(time_series_df_default_index: dataframe.DataFrame):
    result = time_series_df_default_index.ai.forecast(
        timestamp_column="parsed_date",
        data_column="total_visits",
        id_columns=["id"],
        horizon=20,
        confidence_level=0.98,
    )

    utils.check_pandas_df_schema_and_index(
        result,
        columns=["id"] + AI_FORECAST_COLUMNS,
        index=20 * 2,  # 20 for each id
    )


def _create_dummy_full_response(row_count: int) -> pd.Series:
    entry = """{"candidates": [{"avg_logprobs": -0.5}]}"""

    return pd.Series([entry] * row_count)
