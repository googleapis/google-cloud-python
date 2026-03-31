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
# Tests that use real LLM models are under system/large/test_semantcs.py

import pandas as pd
import pandas.testing
import pytest

import bigframes
from bigframes import dataframe, dtypes
from bigframes.ml import llm

SEM_OP_EXP_OPTION = "experiments.semantic_operators"
THRESHOLD_OPTION = "compute.semantic_ops_confirmation_threshold"


class FakeGeminiTextGenerator(llm.GeminiTextGenerator):
    def __init__(self, prediction):
        self.prediction = prediction

    def predict(self, *args, **kwargs):
        return self.prediction


def test_semantics_experiment_off_raise_error(session):
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}, session=session
    )

    with bigframes.option_context(SEM_OP_EXP_OPTION, False), pytest.raises(
        NotImplementedError
    ):
        df.semantics


def test_filter(session):
    df = dataframe.DataFrame({"col": ["A", "B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {"ml_generate_text_llm_result": ["true", "false"]}, session=session
        ),
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = df.semantics.filter(
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
            {"ml_generate_text_llm_result": ["true", "false"]}, session=session
        ),
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = df.semantics.map(
            "map {col}", model=model, output_column="output"
        ).to_pandas()

    pandas.testing.assert_frame_equal(
        result,
        pd.DataFrame(
            {"col": ["A", "B"], "output": ["true", "false"]}, dtype=dtypes.STRING_DTYPE
        ),
        check_index_type=False,
    )


def test_join(session):
    left_df = dataframe.DataFrame({"col_A": ["A"]}, session=session)
    right_df = dataframe.DataFrame({"col_B": ["B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame({"ml_generate_text_llm_result": ["true"]}, session=session),
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = left_df.semantics.join(
            right_df, "join {col_A} and {col_B}", model
        ).to_pandas()

    pandas.testing.assert_frame_equal(
        result,
        pd.DataFrame({"col_A": ["A"], "col_B": ["B"]}, dtype=dtypes.STRING_DTYPE),
        check_index_type=False,
    )


def test_top_k(session):
    df = dataframe.DataFrame({"col": ["A", "B"]}, session=session)
    model = FakeGeminiTextGenerator(
        dataframe.DataFrame(
            {"ml_generate_text_llm_result": ["Document 1"]}, session=session
        ),
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        result = df.semantics.top_k("top k of {col}", model, k=1).to_pandas()

    assert len(result) == 1
