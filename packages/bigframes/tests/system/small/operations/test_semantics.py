# Copyright 2024 Google LLC
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

import pandas as pd
import pandas.testing
import pytest

import bigframes
import bigframes.dataframe as dataframe


def test_semantics_experiment_off_raise_error():
    bigframes.options.experiments.semantic_operators = False
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}
    )

    with pytest.raises(NotImplementedError):
        df.semantics


def test_filter(session, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]},
        session=session,
    )

    actual_df = df.semantics.filter(
        "{city} is the capital of {country}", gemini_flash_model
    ).to_pandas()

    expected_df = pd.DataFrame({"country": ["Germany"], "city": ["Berlin"]}, index=[1])
    pandas.testing.assert_frame_equal(
        actual_df, expected_df, check_dtype=False, check_index_type=False
    )


@pytest.mark.parametrize(
    "instruction",
    [
        "No column reference",
        "{city} is in the {non_existing_column}",
    ],
)
def test_filter_invalid_instruction_raise_error(instruction, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}
    )

    with pytest.raises(ValueError):
        df.semantics.filter(instruction, gemini_flash_model)
