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
import tests.system.utils


def test_pca_predict(penguins_pca_model, new_penguins_df):
    predictions = penguins_pca_model.predict(new_penguins_df).to_pandas()
    expected = pd.DataFrame(
        {
            "principal_component_1": [-1.314041, -0.855813, -1.848786],
            "principal_component_2": [-0.889106, -1.259753, -0.983304],
            "principal_component_3": [-0.704345, 0.322555, -0.095759],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions.sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_pca_score(penguins_pca_model: decomposition.PCA):
    result = penguins_pca_model.score().to_pandas()
    expected = pd.DataFrame(
        {"total_explained_variance_ratio": [0.812383]},
        dtype="Float64",
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
    )


def test_pca_components_(penguins_pca_model: decomposition.PCA):
    result = penguins_pca_model.components_.to_pandas()

    # result is too long, only check the first principal component here.
    result = result.head(7)
    expected = (
        pd.DataFrame(
            {
                "principal_component_id": [0] * 7,
                "feature": [
                    "species",
                    "island",
                    "culmen_length_mm",
                    "culmen_depth_mm",
                    "flipper_length_mm",
                    "body_mass_g",
                    "sex",
                ],
                "numerical_value": [
                    pd.NA,
                    pd.NA,
                    0.401489,
                    -0.377482,
                    0.524052,
                    0.501174,
                    pd.NA,
                ],
                "categorical_value": [
                    [
                        {
                            "category": "Gentoo penguin (Pygoscelis papua)",
                            "value": 0.25068877125667804,
                        },
                        {
                            "category": "Adelie Penguin (Pygoscelis adeliae)",
                            "value": -0.20622291900416198,
                        },
                        {
                            "category": "Chinstrap penguin (Pygoscelis antarctica)",
                            "value": -0.030161149275185855,
                        },
                    ],
                    [
                        {"category": "Biscoe", "value": 0.19761120114410635},
                        {"category": "Dream", "value": -0.11264736305259061},
                        {"category": "Torgersen", "value": -0.07065913511418596},
                    ],
                    [],
                    [],
                    [],
                    [],
                    [
                        {"category": ".", "value": 0.0015916894448071784},
                        {"category": "MALE", "value": 0.06869704739750442},
                        {"category": "FEMALE", "value": -0.052521171596813174},
                        {"category": "_null_filler", "value": -0.0034628622681684906},
                    ],
                ],
            },
        )
        .sort_values(["principal_component_id", "feature"])
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
    )


def test_pca_explained_variance_(penguins_pca_model: decomposition.PCA):
    result = penguins_pca_model.explained_variance_.to_pandas()

    expected = pd.DataFrame(
        {
            "principal_component_id": [0, 1, 2],
            "explained_variance": [3.278657, 1.270829, 1.125354],
        },
    )
    tests.system.utils.assert_pandas_df_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
        ignore_order=True,
    )


def test_pca_explained_variance_ratio_(penguins_pca_model: decomposition.PCA):
    result = penguins_pca_model.explained_variance_ratio_.to_pandas()

    expected = pd.DataFrame(
        {
            "principal_component_id": [0, 1, 2],
            "explained_variance_ratio": [0.469357, 0.181926, 0.1611],
        },
    )
    tests.system.utils.assert_pandas_df_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
        ignore_order=True,
    )
