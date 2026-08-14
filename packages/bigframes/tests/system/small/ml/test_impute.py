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

from bigframes.ml import impute


def test_simple_imputer_fit_transform_default_params(missing_values_penguins_df):
    imputer = impute.SimpleImputer(strategy="mean")
    result = imputer.fit_transform(
        missing_values_penguins_df[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "imputer_culmen_length_mm": [39.5, 38.5, 37.9],
            "imputer_culmen_depth_mm": [17.65, 17.2, 18.1],
            "imputer_flipper_length_mm": [184.5, 181.0, 188.0],
        },
        dtype="Float64",
        index=pd.Index([0, 1, 2], dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_simple_imputer_series(missing_values_penguins_df):
    imputer = impute.SimpleImputer(strategy="mean")
    imputer.fit(missing_values_penguins_df["culmen_depth_mm"])

    result = imputer.transform(
        missing_values_penguins_df["culmen_depth_mm"]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "imputer_culmen_depth_mm": [17.65, 17.2, 18.1],
        },
        dtype="Float64",
        index=pd.Index([0, 1, 2], dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_simple_imputer_save_load_mean(missing_values_penguins_df, dataset_id):
    transformer = impute.SimpleImputer(strategy="mean")
    transformer.fit(
        missing_values_penguins_df[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, impute.SimpleImputer)
    assert reloaded_transformer.strategy == transformer.strategy
    assert reloaded_transformer._bqml_model is not None


def test_simple_imputer_save_load_most_frequent(missing_values_penguins_df, dataset_id):
    transformer = impute.SimpleImputer(strategy="most_frequent")
    transformer.fit(
        missing_values_penguins_df[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, impute.SimpleImputer)
    assert reloaded_transformer.strategy == transformer.strategy
    assert reloaded_transformer._bqml_model is not None
