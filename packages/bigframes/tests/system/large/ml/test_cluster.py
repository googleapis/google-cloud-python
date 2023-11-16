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
import pytest

from bigframes.ml import cluster
from tests.system.utils import assert_pandas_df_equal


@pytest.mark.flaky(retries=2, delay=120)
def test_cluster_configure_fit_score_predict(
    session, penguins_df_default_index, dataset_id
):
    model = cluster.KMeans(n_clusters=3)

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
    score_expected = pd.DataFrame(
        {"davies_bouldin_index": [1.502182], "mean_squared_distance": [1.953408]},
        dtype="Float64",
    )
    score_expected = score_expected.reindex(index=score_expected.index.astype("Int64"))

    pd.testing.assert_frame_equal(
        score_result, score_expected, check_exact=False, rtol=0.1
    )

    predictions = model.predict(new_penguins).to_pandas()
    assert predictions.shape == (4, 9)
    result = predictions[["CENTROID_ID"]]
    expected = pd.DataFrame(
        {"CENTROID_ID": [2, 3, 1, 2]},
        dtype="Int64",
        index=pd.Index(["test1", "test2", "test3", "test4"], dtype="string[pyarrow]"),
    )
    expected.index.name = "observation"
    assert_pandas_df_equal(result, expected, ignore_order=True)

    # save, load, check n_clusters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_cluster_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_cluster_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_clusters == 3
