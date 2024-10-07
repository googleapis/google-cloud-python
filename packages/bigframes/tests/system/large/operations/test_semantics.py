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


def test_filter_single_column_reference(session, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]},
        session=session,
    )

    actual_df = df.semantics.filter(
        "{country} is in Europe", gemini_flash_model
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


def test_filter_invalid_model_raise_error():
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}
    )

    with pytest.raises(ValueError):
        df.semantics.filter("{city} is the capital of {country}", None)


def test_map(session, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
        },
        session=session,
    )

    actual_df = df.semantics.map(
        "What is the food made from {ingredient_1} and {ingredient_2}? One word only.",
        "food",
        gemini_flash_model,
    ).to_pandas()
    # Result sanitation
    actual_df["food"] = actual_df["food"].str.strip().str.lower()

    expected_df = pd.DataFrame(
        {
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
            "food": ["burger", "tofu"],
        }
    )
    pandas.testing.assert_frame_equal(
        actual_df,
        expected_df,
        check_dtype=False,
        check_index_type=False,
        check_column_type=False,
    )


@pytest.mark.parametrize(
    "instruction",
    [
        "No column reference",
        "What is the food made from {ingredient_1} and {non_existing_column}?}",
    ],
)
def test_map_invalid_instruction_raise_error(instruction, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
        }
    )

    with pytest.raises(ValueError):
        df.semantics.map(instruction, "food", gemini_flash_model)


def test_map_invalid_model_raise_error():
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
        },
    )

    with pytest.raises(ValueError):
        df.semantics.map(
            "What is the food made from {ingredient_1} and {ingredient_2}? One word only.",
            "food",
            None,
        )


def test_join(session, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    cities = dataframe.DataFrame(
        data={
            "city": ["Seattle", "Berlin"],
        },
        session=session,
    )
    countries = dataframe.DataFrame(
        data={"country": ["USA", "UK", "Germany"]},
        session=session,
    )

    actual_df = cities.semantics.join(
        countries,
        "{city} belongs to {country}",
        gemini_flash_model,
    ).to_pandas()

    expected_df = pd.DataFrame(
        {
            "city": ["Seattle", "Berlin"],
            "country": ["USA", "Germany"],
        }
    )
    pandas.testing.assert_frame_equal(
        actual_df,
        expected_df,
        check_dtype=False,
        check_index_type=False,
        check_column_type=False,
    )


def test_self_join(session, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    animals = dataframe.DataFrame(
        data={
            "animal": ["spider", "capybara"],
        },
        session=session,
    )

    actual_df = animals.semantics.join(
        animals,
        "{animal_left} is heavier than {animal_right}",
        gemini_flash_model,
    ).to_pandas()

    expected_df = pd.DataFrame(
        {
            "animal_left": ["capybara"],
            "animal_right": ["spider"],
        }
    )
    pandas.testing.assert_frame_equal(
        actual_df,
        expected_df,
        check_dtype=False,
        check_index_type=False,
        check_column_type=False,
    )


def test_join_data_too_large_raise_error(session, gemini_flash_model):
    bigframes.options.experiments.semantic_operators = True
    cities = dataframe.DataFrame(
        data={
            "city": ["Seattle", "Berlin"],
        },
        session=session,
    )
    countries = dataframe.DataFrame(
        data={"country": ["USA", "UK", "Germany"]},
        session=session,
    )

    with pytest.raises(ValueError):
        cities.semantics.join(
            countries, "{city} belongs to {country}", gemini_flash_model, max_rows=1
        )


@pytest.mark.parametrize(
    ("instruction", "error_pattern"),
    [
        ("No column reference", "No column references"),
        pytest.param(
            "{city} is in {continent}", r"Column .+ not found", id="non_existing_column"
        ),
        pytest.param(
            "{city} is in {country}",
            r"Ambiguous column reference: .+",
            id="ambiguous_column",
        ),
        pytest.param(
            "{city_left} is in {country}",
            r"Unnecessary suffix for .+",
            id="suffix_on_left_unique_column",
        ),
        pytest.param(
            "{city} is in {region_right}",
            r"Unnecessary suffix for .+",
            id="suffix_on_right_unique_column",
        ),
        pytest.param(
            "{city_right} is in {country}", r"Column .+ not found", id="wrong_suffix"
        ),
        pytest.param(
            "{city} is in {continent_right}",
            r"Column .+ not found",
            id="suffix_on_non_existing_column",
        ),
    ],
)
def test_join_invalid_instruction_raise_error(
    instruction, error_pattern, gemini_flash_model
):
    bigframes.options.experiments.semantic_operators = True
    df1 = dataframe.DataFrame(
        {"city": ["Seattle", "Berlin"], "country": ["USA", "Germany"]}
    )
    df2 = dataframe.DataFrame(
        {
            "country": ["USA", "UK", "Germany"],
            "region": ["North America", "Europe", "Europe"],
        }
    )

    with pytest.raises(ValueError, match=error_pattern):
        df1.semantics.join(df2, instruction, gemini_flash_model)


def test_join_invalid_model_raise_error():
    bigframes.options.experiments.semantic_operators = True
    cities = dataframe.DataFrame({"city": ["Seattle", "Berlin"]})
    countries = dataframe.DataFrame({"country": ["USA", "UK", "Germany"]})

    with pytest.raises(ValueError):
        cities.semantics.join(countries, "{city} is in {country}", None)


@pytest.mark.parametrize(
    "score_column",
    [
        pytest.param(None, id="no_score_column"),
        pytest.param("distance", id="has_score_column"),
    ],
)
def test_search(session, text_embedding_generator, score_column):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    actual_result = df.semantics.search(
        "creatures",
        "monkey",
        top_k=2,
        model=text_embedding_generator,
        score_column=score_column,
    ).to_pandas()

    expected_result = pd.Series(
        ["baboons", "chimpanzee"], index=[2, 4], name="creatures"
    )
    pandas.testing.assert_series_equal(
        actual_result["creatures"],
        expected_result,
        check_dtype=False,
        check_index_type=False,
    )

    if score_column is None:
        assert len(actual_result.columns) == 1
    else:
        assert score_column in actual_result.columns


def test_search_invalid_column_raises_error(session, text_embedding_generator):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    with pytest.raises(ValueError):
        df.semantics.search(
            "whatever", "monkey", top_k=2, model=text_embedding_generator
        )


def test_search_invalid_model_raises_error(session):
    bigframes.options.experiments.semantic_operators = True
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    with pytest.raises(TypeError):
        df.semantics.search("creatures", "monkey", top_k=2, model=None)
