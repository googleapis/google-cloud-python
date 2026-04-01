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

from bigframes.ml import cluster
from bigframes.testing import utils


def test_cluster_configure_fit_score_predict(
    session, penguins_df_default_index, dataset_id
):
    model = cluster.KMeans(n_clusters=3, init="random")

    df = penguins_df_default_index.dropna()[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]

    # TODO(swast): How should we handle the default index? Currently, we get:
    # "Column bigframes_index_0_z is not found in the input data to the
    # EVALUATE function."
    df = df.reset_index(drop=True)

    model.fit(df)

    pd_new_penguins = pd.DataFrame.from_dict(
        {
            "test1": {
                "species": "Adelie Penguin (Pygoscelis adeliae)",
                "island": "Dream",
                "culmen_length_mm": 37.5,
                "culmen_depth_mm": 18.5,
                "flipper_length_mm": 199,
                "body_mass_g": 4475,
                "sex": "MALE",
            },
            "test2": {
                "species": "Chinstrap penguin (Pygoscelis antarctica)",
                "island": "Dream",
                "culmen_length_mm": 55.8,
                "culmen_depth_mm": 19.8,
                "flipper_length_mm": 207,
                "body_mass_g": 4000,
                "sex": "MALE",
            },
            "test3": {
                "species": "Adelie Penguin (Pygoscelis adeliae)",
                "island": "Biscoe",
                "culmen_length_mm": 39.7,
                "culmen_depth_mm": 18.9,
                "flipper_length_mm": 184,
                "body_mass_g": 3550,
                "sex": "MALE",
            },
            "test4": {
                "species": "Gentoo penguin (Pygoscelis papua)",
                "island": "Biscoe",
                "culmen_length_mm": 43.8,
                "culmen_depth_mm": 13.9,
                "flipper_length_mm": 208,
                "body_mass_g": 4300,
                "sex": "FEMALE",
            },
        },
        orient="index",
    )
    pd_new_penguins.index.name = "observation"

    new_penguins = session.read_pandas(pd_new_penguins)

    # Check score to ensure the model was fitted
    score_result = model.score(new_penguins).to_pandas()

    eval_metrics = ["davies_bouldin_index", "mean_squared_distance"]
    utils.check_pandas_df_schema_and_index(score_result, columns=eval_metrics, index=1)

    predictions = model.predict(new_penguins).to_pandas()
    assert predictions.shape == (4, 9)
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["CENTROID_ID"],
        index=["test1", "test2", "test3", "test4"],
        col_exact=False,
    )

    # save, load, check n_clusters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_cluster_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_cluster_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_clusters == 3
    assert reloaded_model.init == "RANDOM"
    assert reloaded_model.distance_type == "EUCLIDEAN"
    assert reloaded_model.max_iter == 20
    assert reloaded_model.tol == 0.01


def test_cluster_configure_fit_load_params(penguins_df_default_index, dataset_id):
    model = cluster.KMeans(
        n_clusters=4,
        init="random",
        distance_type="cosine",
        max_iter=30,
        tol=0.001,
    )

    df = penguins_df_default_index.dropna()[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]

    # TODO(swast): How should we handle the default index? Currently, we get:
    # "Column bigframes_index_0_z is not found in the input data to the
    # EVALUATE function."
    df = df.reset_index(drop=True)

    model.fit(df)

    # save, load, check n_clusters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_cluster_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_cluster_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_clusters == 4
    assert reloaded_model.init == "RANDOM"
    assert reloaded_model.distance_type == "COSINE"
    assert reloaded_model.max_iter == 30
    assert reloaded_model.tol == 0.001


def test_model_centroids_with_custom_index(penguins_df_default_index):
    model = cluster.KMeans(n_clusters=3)
    penguins = penguins_df_default_index.set_index(["species", "island", "sex"])
    model.fit(penguins)

    assert (
        not model.cluster_centers_["feature"].isin(["species", "island", "sex"]).any()
    )
