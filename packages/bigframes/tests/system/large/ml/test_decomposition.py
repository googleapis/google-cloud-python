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

from bigframes.ml import decomposition


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
    score_expected = pd.DataFrame(
        {
            "total_explained_variance_ratio": [0.812383],
        },
        dtype="Float64",
    )
    score_expected = score_expected.reindex(index=score_expected.index.astype("Int64"))

    pd.testing.assert_frame_equal(
        score_result, score_expected, check_exact=False, rtol=0.1
    )

    result = model.predict(new_penguins).to_pandas()
    expected = pd.DataFrame(
        {
            "principal_component_1": [-1.459, 2.258, -1.685],
            "principal_component_2": [-1.120, -1.351, -0.874],
            "principal_component_3": [-0.646, 0.443, -0.704],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        abs(result.sort_index()),  # results may differ by a minus sign
        abs(expected),
        check_exact=False,
        rtol=0.1,
    )

    # save, load, check n_components to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_pca_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_pca_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.n_components == 3
