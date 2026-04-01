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

from contextlib import nullcontext
from unittest.mock import patch

import pandas as pd
import pandas.testing
import pytest

import bigframes
from bigframes import dataframe, dtypes, exceptions, series

pytest.skip(
    "Semantics namespace is deprecated. ",
    allow_module_level=True,
)

SEM_OP_EXP_OPTION = "experiments.semantic_operators"
BLOB_EXP_OPTION = "experiments.blob"
THRESHOLD_OPTION = "compute.semantic_ops_confirmation_threshold"


def test_semantics_experiment_off_raise_error():
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}
    )

    with bigframes.option_context(SEM_OP_EXP_OPTION, False), pytest.raises(
        NotImplementedError
    ):
        df.semantics


@pytest.mark.parametrize(
    ("max_agg_rows", "cluster_column"),
    [
        pytest.param(1, None, id="one", marks=pytest.mark.xfail(raises=ValueError)),
        pytest.param(2, None, id="two"),
        pytest.param(3, None, id="three"),
        pytest.param(4, None, id="four"),
        pytest.param(5, "Years", id="two_w_cluster_column"),
        pytest.param(6, "Years", id="three_w_cluster_column"),
        pytest.param(7, "Years", id="four_w_cluster_column"),
    ],
)
def test_agg(session, gemini_flash_model, max_agg_rows, cluster_column):
    df = dataframe.DataFrame(
        data={
            "Movies": [
                "Titanic",
                "The Wolf of Wall Street",
                "Killers of the Flower Moon",
                "The Revenant",
                "Inception",
                "Shuttle Island",
                "The Great Gatsby",
            ],
            "Years": [1997, 2013, 2023, 2015, 2010, 2010, 2013],
        },
        session=session,
    )
    instruction = "Find the shared first name of actors in {Movies}. One word answer."

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        50,
    ):
        actual_s = df.semantics.agg(
            instruction,
            model=gemini_flash_model,
            max_agg_rows=max_agg_rows,
            cluster_column=cluster_column,
        ).to_pandas()

    expected_s = pd.Series(["Leonardo\n"], dtype=dtypes.STRING_DTYPE)
    expected_s.name = "Movies"
    pandas.testing.assert_series_equal(actual_s, expected_s, check_index_type=False)


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_agg_with_confirmation(session, gemini_flash_model, reply, monkeypatch):
    df = dataframe.DataFrame(
        data={
            "Movies": [
                "Titanic",
                "The Wolf of Wall Street",
                "Killers of the Flower Moon",
                "The Revenant",
                "Inception",
                "Shuttle Island",
                "The Great Gatsby",
            ],
            "Years": [1997, 2013, 2023, 2015, 2010, 2010, 2013],
        },
        session=session,
    )
    instruction = "Find the shared first name of actors in {Movies}. One word answer."
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        df.semantics.agg(
            instruction,
            model=gemini_flash_model,
        )


def test_agg_w_int_column(session, gemini_flash_model):
    df = dataframe.DataFrame(
        data={
            "Movies": [
                "Killers of the Flower Moon",
                "The Great Gatsby",
                "The Wolf of Wall Street",
            ],
            "Years": [2023, 2013, 2013],
        },
        session=session,
    )
    instruction = "Find the {Years} Leonardo DiCaprio acted in the most movies. Your answer should be the four-digit year, returned as a string."

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        actual_s = df.semantics.agg(
            instruction,
            model=gemini_flash_model,
        ).to_pandas()

    expected_s = pd.Series(["2013\n"], dtype=dtypes.STRING_DTYPE)
    expected_s.name = "Years"
    pandas.testing.assert_series_equal(actual_s, expected_s, check_index_type=False)


@pytest.mark.parametrize(
    "instruction",
    [
        pytest.param(
            "No column reference",
            id="zero_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{Movies} is good",
            id="non_existing_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{Movies} is better than {Movies}",
            id="two_columns",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
    ],
)
def test_agg_invalid_instruction_raise_error(instruction, gemini_flash_model):
    df = dataframe.DataFrame(
        data={
            "Movies": [
                "Titanic",
                "The Wolf of Wall Street",
                "Killers of the Flower Moon",
            ],
            "Year": [1997, 2013, 2023],
        },
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        df.semantics.agg(instruction, gemini_flash_model)


@pytest.mark.parametrize(
    "cluster_column",
    [
        pytest.param(
            "non_existing_column",
            id="non_existing_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "Movies", id="non_int_column", marks=pytest.mark.xfail(raises=TypeError)
        ),
    ],
)
def test_agg_invalid_cluster_column_raise_error(gemini_flash_model, cluster_column):
    df = dataframe.DataFrame(
        data={
            "Movies": [
                "Titanic",
                "The Wolf of Wall Street",
                "Killers of the Flower Moon",
                "The Revenant",
            ],
        },
    )
    instruction = "Find the shared first name of actors in {Movies}. One word answer."

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        df.semantics.agg(instruction, gemini_flash_model, cluster_column=cluster_column)


@pytest.mark.parametrize(
    ("n_clusters"),
    [
        pytest.param(1, id="one", marks=pytest.mark.xfail(raises=ValueError)),
        pytest.param(2, id="two"),
    ],
)
def test_cluster_by(session, text_embedding_generator, n_clusters):
    df = dataframe.DataFrame(
        (
            {
                "Item": [
                    "Orange",
                    "Cantaloupe",
                    "Watermelon",
                    "Chicken",
                    "Duck",
                    "Hen",
                    "Rooster",
                ]
            }
        ),
        session=session,
    )
    output_column = "cluster id"

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        result = df.semantics.cluster_by(
            "Item",
            output_column,
            text_embedding_generator,
            n_clusters=n_clusters,
        )

    assert output_column in result
    # In rare cases, it's possible to have fewer than K clusters due to randomness.
    assert len(result[output_column].unique()) <= n_clusters


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_cluster_by_with_confirmation(
    session, text_embedding_generator, reply, monkeypatch
):
    df = dataframe.DataFrame(
        (
            {
                "Item": [
                    "Orange",
                    "Cantaloupe",
                    "Watermelon",
                    "Chicken",
                    "Duck",
                    "Hen",
                    "Rooster",
                ]
            }
        ),
        session=session,
    )
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        df.semantics.cluster_by(
            "Item",
            "cluster id",
            text_embedding_generator,
            n_clusters=2,
        )


def test_cluster_by_invalid_column(session, text_embedding_generator):
    df = dataframe.DataFrame(
        ({"Product": ["Smartphone", "Laptop", "Coffee Maker", "T-shirt", "Jeans"]}),
        session=session,
    )
    output_column = "cluster id"

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df.semantics.cluster_by(
            "unknown_column",
            output_column,
            text_embedding_generator,
            n_clusters=3,
        )


def test_cluster_by_invalid_model(session, gemini_flash_model):
    df = dataframe.DataFrame(
        ({"Product": ["Smartphone", "Laptop", "Coffee Maker", "T-shirt", "Jeans"]}),
        session=session,
    )
    output_column = "cluster id"

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(TypeError):
        df.semantics.cluster_by(
            "Product",
            output_column,
            gemini_flash_model,
            n_clusters=3,
        )


def test_filter(session, gemini_flash_model):
    df = dataframe.DataFrame(
        data={
            "country": ["USA", "Germany"],
            "city": ["Seattle", "Berlin"],
            "year": [2023, 2024],
        },
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        actual_df = df.semantics.filter(
            "{city} is the capital of {country} in {year}", gemini_flash_model
        ).to_pandas()

    expected_df = pd.DataFrame(
        {"country": ["Germany"], "city": ["Berlin"], "year": [2024]}, index=[1]
    )
    pandas.testing.assert_frame_equal(
        actual_df, expected_df, check_dtype=False, check_index_type=False
    )


def test_filter_multi_model(session, gemini_flash_model):
    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        BLOB_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        df = session.from_glob_path(
            "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
        )
        df["prey"] = series.Series(
            ["building", "cross road", "rock", "squirrel", "rabbit"], session=session
        )
        result = df.semantics.filter(
            "The object in {image} feeds on {prey}",
            gemini_flash_model,
        ).to_pandas()

    assert len(result) <= len(df)


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_filter_with_confirmation(session, gemini_flash_model, reply, monkeypatch):
    df = dataframe.DataFrame(
        data={
            "country": ["USA", "Germany"],
            "city": ["Seattle", "Berlin"],
            "year": [2023, 2024],
        },
        session=session,
    )
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        df.semantics.filter(
            "{city} is the capital of {country} in {year}", gemini_flash_model
        )


def test_filter_single_column_reference(session, gemini_flash_model):
    df = dataframe.DataFrame(
        data={"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
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
        pytest.param(
            "No column reference",
            id="zero_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{city} is in the {non_existing_column}",
            id="non_existing_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{id}",
            id="invalid_type",
            marks=pytest.mark.xfail(raises=TypeError),
        ),
    ],
)
def test_filter_invalid_instruction_raise_error(instruction, gemini_flash_model):
    df = dataframe.DataFrame({"id": [1, 2], "city": ["Seattle", "Berlin"]})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df.semantics.filter(instruction, gemini_flash_model)


def test_filter_invalid_model_raise_error():
    df = dataframe.DataFrame(
        {"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]}
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(TypeError):
        df.semantics.filter("{city} is the capital of {country}", None)


def test_map(session, gemini_flash_model):
    df = dataframe.DataFrame(
        data={
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
            "gluten-free": [True, True],
        },
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        actual_df = df.semantics.map(
            "What is the {gluten-free} food made from {ingredient_1} and {ingredient_2}? One word only.",
            "food",
            gemini_flash_model,
        ).to_pandas()
    # Result sanitation
    actual_df["food"] = actual_df["food"].str.strip().str.lower()

    expected_df = pd.DataFrame(
        {
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
            "gluten-free": [True, True],
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


def test_map_multimodel(session, gemini_flash_model):
    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        BLOB_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        df = session.from_glob_path(
            "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
        )
        df["scenario"] = series.Series(
            ["building", "cross road", "tree", "squirrel", "rabbit"], session=session
        )
        result = df.semantics.map(
            "What is the object in {image} combined with {scenario}? One word only.",
            "object",
            gemini_flash_model,
        ).to_pandas()

    assert len(result) == len(df)


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_map_with_confirmation(session, gemini_flash_model, reply, monkeypatch):
    df = dataframe.DataFrame(
        data={
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
            "gluten-free": [True, True],
        },
        session=session,
    )
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        df.semantics.map(
            "What is the {gluten-free} food made from {ingredient_1} and {ingredient_2}? One word only.",
            "food",
            gemini_flash_model,
        )


@pytest.mark.parametrize(
    "instruction",
    [
        pytest.param(
            "No column reference",
            id="zero_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "What is the food made from {ingredient_1} and {non_existing_column}?}",
            id="non_existing_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{id}",
            id="invalid_type",
            marks=pytest.mark.xfail(raises=TypeError),
        ),
    ],
)
def test_map_invalid_instruction_raise_error(instruction, gemini_flash_model):
    df = dataframe.DataFrame(
        data={
            "id": [1, 2],
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
        }
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df.semantics.map(instruction, "food", gemini_flash_model)


def test_map_invalid_model_raise_error():
    df = dataframe.DataFrame(
        data={
            "ingredient_1": ["Burger Bun", "Soy Bean"],
            "ingredient_2": ["Beef Patty", "Bittern"],
        },
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(TypeError):
        df.semantics.map(
            "What is the food made from {ingredient_1} and {ingredient_2}? One word only.",
            "food",
            None,
        )


@pytest.mark.parametrize(
    "instruction",
    [
        pytest.param("{city} is in {country}", id="no_dataframe_reference"),
        pytest.param("{left.city} is in {country}", id="has_left_dataframe_reference"),
        pytest.param(
            "{city} is in {right.country}",
            id="has_right_dataframe_reference",
        ),
        pytest.param(
            "{left.city} is in {right.country}", id="has_both_dataframe_references"
        ),
    ],
)
def test_join(instruction, session, gemini_flash_model):
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

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        actual_df = cities.semantics.join(
            countries,
            instruction,
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


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_join_with_confirmation(session, gemini_flash_model, reply, monkeypatch):
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
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        cities.semantics.join(
            countries,
            "{city} is in {country}",
            gemini_flash_model,
        )


def test_self_join(session, gemini_flash_model):
    animals = dataframe.DataFrame(
        data={
            "animal": ["ant", "elephant"],
        },
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        actual_df = animals.semantics.join(
            animals,
            "{left.animal} is heavier than {right.animal}",
            gemini_flash_model,
        ).to_pandas()

    expected_df = pd.DataFrame(
        {
            "animal_left": ["elephant"],
            "animal_right": ["ant"],
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
            "{right.city} is in {country}", r"Column .+ not found", id="wrong_prefix"
        ),
        pytest.param(
            "{city} is in {right.continent}",
            r"Column .+ not found",
            id="prefix_on_non_existing_column",
        ),
    ],
)
def test_join_invalid_instruction_raise_error(
    instruction, error_pattern, gemini_flash_model
):
    df1 = dataframe.DataFrame(
        {"city": ["Seattle", "Berlin"], "country": ["USA", "Germany"]}
    )
    df2 = dataframe.DataFrame(
        {
            "country": ["USA", "UK", "Germany"],
            "region": ["North America", "Europe", "Europe"],
        }
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError, match=error_pattern):
        df1.semantics.join(df2, instruction, gemini_flash_model)


def test_join_invalid_model_raise_error():
    cities = dataframe.DataFrame({"city": ["Seattle", "Berlin"]})
    countries = dataframe.DataFrame({"country": ["USA", "UK", "Germany"]})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(TypeError):
        cities.semantics.join(countries, "{city} is in {country}", None)


@pytest.mark.parametrize(
    "score_column",
    [
        pytest.param(None, id="no_score_column"),
        pytest.param("distance", id="has_score_column"),
    ],
)
def test_search(session, text_embedding_generator, score_column):
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
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


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_search_with_confirmation(
    session, text_embedding_generator, reply, monkeypatch
):
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        df.semantics.search(
            "creatures",
            "monkey",
            top_k=2,
            model=text_embedding_generator,
        )


def test_search_invalid_column_raises_error(session, text_embedding_generator):
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df.semantics.search(
            "whatever", "monkey", top_k=2, model=text_embedding_generator
        )


def test_search_invalid_model_raises_error(session):
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(TypeError):
        df.semantics.search("creatures", "monkey", top_k=2, model=None)


def test_search_invalid_top_k_raises_error(session, text_embedding_generator):
    df = dataframe.DataFrame(
        data={"creatures": ["salmon", "sea urchin", "baboons", "frog", "chimpanzee"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df.semantics.search(
            "creatures", "monkey", top_k=0, model=text_embedding_generator
        )


@pytest.mark.parametrize(
    "score_column",
    [
        pytest.param(None, id="no_score_column"),
        pytest.param("distance", id="has_score_column"),
    ],
)
def test_sim_join(session, text_embedding_generator, score_column):
    df1 = dataframe.DataFrame(
        data={"creatures": ["salmon", "cat"]},
        session=session,
    )
    df2 = dataframe.DataFrame(
        data={"creatures": ["dog", "tuna"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        actual_result = df1.semantics.sim_join(
            df2,
            left_on="creatures",
            right_on="creatures",
            model=text_embedding_generator,
            top_k=1,
            score_column=score_column,
        ).to_pandas()

    expected_result = pd.DataFrame(
        {"creatures": ["salmon", "cat"], "creatures_1": ["tuna", "dog"]}
    )
    pandas.testing.assert_frame_equal(
        actual_result[["creatures", "creatures_1"]],
        expected_result,
        check_dtype=False,
        check_index_type=False,
    )

    if score_column is None:
        assert len(actual_result.columns) == 2
    else:
        assert score_column in actual_result.columns


@pytest.mark.parametrize(
    ("reply"),
    [
        pytest.param("y"),
        pytest.param(
            "n", marks=pytest.mark.xfail(raises=exceptions.OperationAbortedError)
        ),
    ],
)
def test_sim_join_with_confirmation(
    session, text_embedding_generator, reply, monkeypatch
):
    df1 = dataframe.DataFrame(
        data={"creatures": ["salmon", "cat"]},
        session=session,
    )
    df2 = dataframe.DataFrame(
        data={"creatures": ["dog", "tuna"]},
        session=session,
    )
    monkeypatch.setattr("builtins.input", lambda: reply)

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        0,
    ):
        df1.semantics.sim_join(
            df2,
            left_on="creatures",
            right_on="creatures",
            model=text_embedding_generator,
            top_k=1,
        )


@pytest.mark.parametrize(
    ("left_on", "right_on"),
    [
        pytest.param("whatever", "creatures", id="incorrect_left_column"),
        pytest.param("creatures", "whatever", id="incorrect_right_column"),
    ],
)
def test_sim_join_invalid_column_raises_error(
    session, text_embedding_generator, left_on, right_on
):
    df1 = dataframe.DataFrame(
        data={"creatures": ["salmon", "cat"]},
        session=session,
    )
    df2 = dataframe.DataFrame(
        data={"creatures": ["dog", "tuna"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df1.semantics.sim_join(
            df2, left_on=left_on, right_on=right_on, model=text_embedding_generator
        )


def test_sim_join_invalid_model_raises_error(session):
    df1 = dataframe.DataFrame(
        data={"creatures": ["salmon", "cat"]},
        session=session,
    )
    df2 = dataframe.DataFrame(
        data={"creatures": ["dog", "tuna"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(TypeError):
        df1.semantics.sim_join(
            df2, left_on="creatures", right_on="creatures", model=None
        )


def test_sim_join_invalid_top_k_raises_error(session, text_embedding_generator):
    df1 = dataframe.DataFrame(
        data={"creatures": ["salmon", "cat"]},
        session=session,
    )
    df2 = dataframe.DataFrame(
        data={"creatures": ["dog", "tuna"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df1.semantics.sim_join(
            df2,
            left_on="creatures",
            right_on="creatures",
            top_k=0,
            model=text_embedding_generator,
        )


def test_sim_join_data_too_large_raises_error(session, text_embedding_generator):
    df1 = dataframe.DataFrame(
        data={"creatures": ["salmon", "cat"]},
        session=session,
    )
    df2 = dataframe.DataFrame(
        data={"creatures": ["dog", "tuna"]},
        session=session,
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df1.semantics.sim_join(
            df2,
            left_on="creatures",
            right_on="creatures",
            model=text_embedding_generator,
            max_rows=1,
        )


@pytest.mark.parametrize(
    "instruction",
    [
        pytest.param(
            "No column reference",
            id="zero_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{Animals}",
            id="non_existing_column",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "{Animals} and {Animals}",
            id="two_columns",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
        pytest.param(
            "{index}",
            id="preserved",
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ],
)
def test_top_k_invalid_instruction_raise_error(instruction, gemini_flash_model):
    df = dataframe.DataFrame(
        {
            "Animals": ["Dog", "Cat", "Bird", "Horse"],
            "ID": [1, 2, 3, 4],
            "index": ["a", "b", "c", "d"],
        }
    )

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ):
        df.semantics.top_k(instruction, model=gemini_flash_model, k=2)


def test_top_k_invalid_k_raise_error(gemini_flash_model):
    df = dataframe.DataFrame({"Animals": ["Dog", "Cat", "Bird", "Horse"]})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        10,
    ), pytest.raises(ValueError):
        df.semantics.top_k(
            "{Animals} are more popular as pets",
            gemini_flash_model,
            k=0,
        )


@patch("builtins.input", return_value="")
def test_confirm_operation__below_threshold_do_not_confirm(mock_input):
    df = dataframe.DataFrame({})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        3,
    ):
        df.semantics._confirm_operation(1)

    mock_input.assert_not_called()


@patch("builtins.input", return_value="")
def test_confirm_operation__threshold_is_none_do_not_confirm(mock_input):
    df = dataframe.DataFrame({})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        None,
    ):
        df.semantics._confirm_operation(100)

    mock_input.assert_not_called()


@patch("builtins.input", return_value="")
def test_confirm_operation__threshold_autofail_do_not_confirm(mock_input):
    df = dataframe.DataFrame({})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        1,
        "compute.semantic_ops_threshold_autofail",
        True,
    ), pytest.raises(exceptions.OperationAbortedError):
        df.semantics._confirm_operation(100)

    mock_input.assert_not_called()


@pytest.mark.parametrize(
    ("reply", "expectation"),
    [
        ("y", nullcontext()),
        ("yes", nullcontext()),
        ("", nullcontext()),
        ("n", pytest.raises(exceptions.OperationAbortedError)),
        ("something", pytest.raises(exceptions.OperationAbortedError)),
    ],
)
def test_confirm_operation__above_threshold_confirm(reply, expectation, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: reply)
    df = dataframe.DataFrame({})

    with bigframes.option_context(
        SEM_OP_EXP_OPTION,
        True,
        THRESHOLD_OPTION,
        3,
    ), expectation as e:
        assert df.semantics._confirm_operation(4) == e
