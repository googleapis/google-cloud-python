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
from tests.system.utils import assert_pandas_df_equal

_PD_NEW_PENGUINS = pd.DataFrame.from_dict(
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


def test_kmeans_predict(session, penguins_kmeans_model: cluster.KMeans):
    new_penguins = session.read_pandas(_PD_NEW_PENGUINS)
    predictions = penguins_kmeans_model.predict(new_penguins).to_pandas()
    assert predictions.shape == (4, 9)
    result = predictions[["CENTROID_ID"]]
    expected = pd.DataFrame(
        {"CENTROID_ID": [2, 3, 1, 2]},
        dtype="Int64",
        index=pd.Index(["test1", "test2", "test3", "test4"], dtype="string[pyarrow]"),
    )
    assert_pandas_df_equal(result, expected, ignore_order=True)


def test_kmeans_score(session, penguins_kmeans_model: cluster.KMeans):
    new_penguins = session.read_pandas(_PD_NEW_PENGUINS)
    result = penguins_kmeans_model.score(new_penguins).to_pandas()
    expected = pd.DataFrame(
        {"davies_bouldin_index": [1.523606], "mean_squared_distance": [1.965944]},
        dtype="Float64",
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_kmeans_cluster_centers(penguins_kmeans_model: cluster.KMeans):
    result = (
        penguins_kmeans_model.cluster_centers_.to_pandas()
        .sort_values(["centroid_id", "feature"])
        .reset_index(drop=True)
    )
    expected = (
        pd.DataFrame(
            {
                "centroid_id": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
                "feature": [
                    "culmen_length_mm",
                    "culmen_depth_mm",
                    "flipper_length_mm",
                    "sex",
                ]
                * 3,
                "numerical_value": [
                    47.509677,
                    14.993548,
                    217.040123,
                    pd.NA,
                    38.207813,
                    18.03125,
                    187.992188,
                    pd.NA,
                    47.036346,
                    18.834808,
                    197.1612,
                    pd.NA,
                ],
                "categorical_value": [
                    [],
                    [],
                    [],
                    [
                        {"category": ".", "value": 0.008064516129032258},
                        {"category": "MALE", "value": 0.49193548387096775},
                        {"category": "FEMALE", "value": 0.47580645161290325},
                        {"category": "_null_filler", "value": 0.024193548387096774},
                    ],
                    [],
                    [],
                    [],
                    [
                        {"category": "MALE", "value": 0.34375},
                        {"category": "FEMALE", "value": 0.625},
                        {"category": "_null_filler", "value": 0.03125},
                    ],
                    [],
                    [],
                    [],
                    [
                        {"category": "MALE", "value": 0.6847826086956522},
                        {"category": "FEMALE", "value": 0.2826086956521739},
                        {"category": "_null_filler", "value": 0.03260869565217391},
                    ],
                ],
            },
        )
        .sort_values(["centroid_id", "feature"])
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
        check_dtype=False,
    )


def test_loaded_config(penguins_kmeans_model):
    assert penguins_kmeans_model.n_clusters == 3
