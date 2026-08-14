# Copyright 2023 Google LLC
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

from bigframes.ml import decomposition
from bigframes.testing import utils


def test_decomposition_configure_fit_score_predict(
    session, penguins_df_default_index, dataset_id
):
    model = decomposition.PCA(n_components=3)
    model.fit(penguins_df_default_index)

    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Gentoo penguin (Pygoscelis papua)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                ],
                "island": ["Dream", "Biscoe", "Torgersen"],
                "culmen_length_mm": [37.8, 46.5, 41.1],
                "culmen_depth_mm": [18.1, 14.8, 18.6],
                "flipper_length_mm": [193.0, 217.0, 189.0],
                "body_mass_g": [3750.0, 5200.0, 3325.0],
                "sex": ["MALE", "FEMALE", "MALE"],
            }
        ).set_index("tag_number")
    )

    # Check score to ensure the model was fitted
    score_result = model.score(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=["total_explained_variance_ratio"], index=1
    )

    result = model.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        result,
        columns=[
            "principal_component_1",
            "principal_component_2",
            "principal_component_3",
        ],
        index=[1633, 1672, 1690],
    )

    # save, load, check n_components to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_pca_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_pca_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_components == 3


def test_decomposition_configure_fit_score_predict_params(
    session, penguins_df_default_index, dataset_id
):
    model = decomposition.PCA(n_components=5, svd_solver="randomized")
    model.fit(penguins_df_default_index)

    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Gentoo penguin (Pygoscelis papua)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                ],
                "island": ["Dream", "Biscoe", "Torgersen"],
                "culmen_length_mm": [37.8, 46.5, 41.1],
                "culmen_depth_mm": [18.1, 14.8, 18.6],
                "flipper_length_mm": [193.0, 217.0, 189.0],
                "body_mass_g": [3750.0, 5200.0, 3325.0],
                "sex": ["MALE", "FEMALE", "MALE"],
            }
        ).set_index("tag_number")
    )

    # Check score to ensure the model was fitted
    score_result = model.score(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=["total_explained_variance_ratio"], index=1
    )

    result = model.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        result,
        columns=[
            "principal_component_1",
            "principal_component_2",
            "principal_component_3",
            "principal_component_4",
            "principal_component_5",
        ],
        index=[1633, 1672, 1690],
    )

    # save, load, check n_components to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_pca_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_pca_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_components == 5
    assert reloaded_model.svd_solver == "RANDOMIZED"


def test_decomposition_configure_fit_load_float_component(
    penguins_df_default_index, dataset_id
):
    model = decomposition.PCA(n_components=0.2)
    model.fit(penguins_df_default_index)

    # save, load, check n_components to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_pca_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_pca_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_components == 0.2


def test_decomposition_configure_fit_load_none_component(
    penguins_df_default_index, dataset_id
):
    model = decomposition.PCA(n_components=None)
    model.fit(penguins_df_default_index)

    # save, load, check n_components. Here n_components is the column size of the training input.
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_pca_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_pca_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_components == 7


def test_decomposition_mf_configure_fit_load(
    session, ratings_df_default_index, dataset_id
):
    model = decomposition.MatrixFactorization(
        num_factors=6,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_id",
        rating_col="rating",
        l2_reg=9.83,
    )

    model.fit(ratings_df_default_index)

    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_mf_model", replace=True
    )

    new_ratings = session.read_pandas(
        pd.DataFrame(
            {
                "user_id": ["11", "12", "13"],
                "item_id": [1, 2, 3],
                "rating": [1.0, 2.0, 3.0],
            }
        )
    )

    # Make sure the input to score is not ignored.
    scores_training_data = reloaded_model.score().to_pandas()
    scores_new_ratings = reloaded_model.score(new_ratings).to_pandas()
    pandas.testing.assert_index_equal(
        scores_training_data.columns, scores_new_ratings.columns
    )
    assert (
        scores_training_data["mean_squared_error"].iloc[0]
        != scores_new_ratings["mean_squared_error"].iloc[0]
    )

    result = reloaded_model.predict(new_ratings).to_pandas()

    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_mf_model"
        in reloaded_model._bqml_model.model_name
    )
    assert result is not None
    assert reloaded_model.feedback_type == "explicit"
    assert reloaded_model.num_factors == 6
    assert reloaded_model.user_col == "user_id"
    assert reloaded_model.item_col == "item_id"
    assert reloaded_model.rating_col == "rating"
    assert reloaded_model.l2_reg == 9.83
