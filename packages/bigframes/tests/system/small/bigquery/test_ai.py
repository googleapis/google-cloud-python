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

from unittest import mock

from packaging import version
import pandas as pd
import pyarrow as pa
import pytest
import sqlglot

from bigframes import dataframe, dtypes, series
import bigframes.bigquery as bbq
import bigframes.pandas as bpd
from bigframes.testing import utils as test_utils


def test_ai_function_pandas_input(session):
    s1 = pd.Series(["apple", "bear"])
    s2 = bpd.Series(["fruit", "tree"], session=session)
    prompt = (s1, " is a ", s2)

    result = bbq.ai.generate_bool(prompt, endpoint="gemini-2.5-flash")

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.bool_()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_function_string_input(session):
    with mock.patch(
        "bigframes.core.global_session.get_global_session"
    ) as mock_get_session:
        mock_get_session.return_value = session
        prompt = "Is apple a fruit?"

        result = bbq.ai.generate_bool(prompt, endpoint="gemini-2.5-flash")

        assert _contains_no_nulls(result)
        assert result.dtype == pd.ArrowDtype(
            pa.struct(
                (
                    pa.field("result", pa.bool_()),
                    pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                    pa.field("status", pa.string()),
                )
            )
        )


def test_ai_function_compile_model_params(session):
    if version.Version(sqlglot.__version__) < version.Version("25.18.0"):
        pytest.skip(
            "Skip test because SQLGLot cannot compile model params to JSON at this version."
        )

    s1 = bpd.Series(["apple", "bear"], session=session)
    s2 = bpd.Series(["fruit", "tree"], session=session)
    prompt = (s1, " is a ", s2)
    model_params = {"generation_config": {"thinking_config": {"thinking_budget": 0}}}

    result = bbq.ai.generate_bool(
        prompt, endpoint="gemini-2.5-flash", model_params=model_params
    )

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.bool_()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate(session):
    country = bpd.Series(["Japan", "Canada"], session=session)
    prompt = ("What's the capital city of ", country, "? one word only")

    result = bbq.ai.generate(prompt, endpoint="gemini-2.5-flash")

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.string()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_with_output_schema(session):
    country = bpd.Series(["Japan", "Canada"], session=session)
    prompt = ("Describe ", country)

    result = bbq.ai.generate(
        prompt,
        endpoint="gemini-2.5-flash",
        output_schema={"population": "INT64", "is_in_north_america": "bool"},
    )

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("is_in_north_america", pa.bool_()),
                pa.field("population", pa.int64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_with_invalid_output_schema_raise_error(session):
    country = bpd.Series(["Japan", "Canada"], session=session)
    prompt = ("Describe ", country)

    with pytest.raises(ValueError):
        bbq.ai.generate(
            prompt,
            endpoint="gemini-2.5-flash",
            output_schema={"population": "INT64", "is_in_north_america": "JSON"},
        )


def test_ai_generate_bool(session):
    s1 = bpd.Series(["apple", "bear"], session=session)
    s2 = bpd.Series(["fruit", "tree"], session=session)
    prompt = (s1, " is a ", s2)

    result = bbq.ai.generate_bool(prompt, endpoint="gemini-2.5-flash")

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.bool_()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_bool_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )

    result = bbq.ai.generate_bool((df["image"], " contains an animal"))

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.bool_()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_int(session):
    s = bpd.Series(["Cat"], session=session)
    prompt = ("How many legs does a ", s, " have?")

    result = bbq.ai.generate_int(prompt, endpoint="gemini-2.5-flash")

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.int64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_int_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )

    result = bbq.ai.generate_int(
        ("How many animals are there in the picture ", df["image"])
    )

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.int64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_double(session):
    s = bpd.Series(["Cat"], session=session)
    prompt = ("How many legs does a ", s, " have?")

    result = bbq.ai.generate_double(prompt, endpoint="gemini-2.5-flash")

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.float64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_generate_double_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )

    result = bbq.ai.generate_double(
        ("How many animals are there in the picture ", df["image"])
    )

    assert _contains_no_nulls(result)
    assert result.dtype == pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.float64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )


def test_ai_if(session):
    s1 = bpd.Series(["apple", "bear"], session=session)
    s2 = bpd.Series(["fruit", "tree"], session=session)
    prompt = (s1, " is a ", s2)

    result = bbq.ai.if_(prompt)

    assert _contains_no_nulls(result)
    assert result.dtype == dtypes.BOOL_DTYPE


@pytest.mark.skip(reason="b/457416070")
def test_ai_if_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )

    result = bbq.ai.if_((df["image"], " contains an animal"))

    assert _contains_no_nulls(result)
    assert result.dtype == dtypes.BOOL_DTYPE


def test_ai_classify(session):
    s = bpd.Series(["cat", "orchid"], session=session)

    result = bbq.ai.classify(s, ["animal", "plant"])

    assert _contains_no_nulls(result)
    assert result.dtype == dtypes.STRING_DTYPE


@pytest.mark.skip(reason="b/457416070")
def test_ai_classify_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )

    result = bbq.ai.classify(df["image"], ["photo", "cartoon"])

    assert _contains_no_nulls(result)
    assert result.dtype == dtypes.STRING_DTYPE


def test_ai_score(session):
    s = bpd.Series(["Tiger", "Rabbit"], session=session)
    prompt = ("Rank the relative weights of ", s, " on the scale from 1 to 3")

    result = bbq.ai.score(prompt)

    assert _contains_no_nulls(result)
    assert result.dtype == dtypes.FLOAT_DTYPE


def test_ai_score_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )
    prompt = ("Rank the liveliness of ", df["image"], "on the scale from 1 to 3")

    result = bbq.ai.score(prompt)

    assert _contains_no_nulls(result)
    assert result.dtype == dtypes.FLOAT_DTYPE


def test_forecast_default_params(time_series_df_default_index: dataframe.DataFrame):
    df = time_series_df_default_index[time_series_df_default_index["id"] == "1"]

    result = bbq.ai.forecast(df, timestamp_col="parsed_date", data_col="total_visits")

    expected_columns = [
        "forecast_timestamp",
        "forecast_value",
        "confidence_level",
        "prediction_interval_lower_bound",
        "prediction_interval_upper_bound",
        "ai_forecast_status",
    ]
    test_utils.check_pandas_df_schema_and_index(
        result,
        columns=expected_columns,
        index=10,
    )


def test_forecast_w_params(time_series_df_default_index: dataframe.DataFrame):
    result = bbq.ai.forecast(
        time_series_df_default_index,
        timestamp_col="parsed_date",
        data_col="total_visits",
        id_cols=["id"],
        horizon=20,
        confidence_level=0.98,
        context_window=64,
    )

    expected_columns = [
        "id",
        "forecast_timestamp",
        "forecast_value",
        "confidence_level",
        "prediction_interval_lower_bound",
        "prediction_interval_upper_bound",
        "ai_forecast_status",
    ]
    test_utils.check_pandas_df_schema_and_index(
        result,
        columns=expected_columns,
        index=20 * 2,  # 20 for each id
    )


def _contains_no_nulls(s: series.Series) -> bool:
    return len(s) == s.count()
