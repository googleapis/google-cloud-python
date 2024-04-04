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

import pandas

from bigframes.ml import compose, preprocessing


def test_columntransformer_standalone_fit_and_transform(
    penguins_df_default_index, new_penguins_df
):
    transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "starndard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                preprocessing.MinMaxScaler(),
                ["culmen_length_mm"],
            ),
        ]
    )

    transformer.fit(
        penguins_df_default_index[["species", "culmen_length_mm", "flipper_length_mm"]]
    )
    result = transformer.transform(new_penguins_df).to_pandas()

    expected = pandas.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "standard_scaled_culmen_length_mm": [
                -0.811119671289163,
                -0.9945520581113803,
                -1.104611490204711,
            ],
            "min_max_scaled_culmen_length_mm": [0.269, 0.232, 0.210],
            "standard_scaled_flipper_length_mm": [-0.350044, -1.418336, -0.9198],
        },
        index=pandas.Index([1633, 1672, 1690], dtype="Int64", name="tag_number"),
    )

    pandas.testing.assert_frame_equal(result, expected, rtol=0.1, check_dtype=False)


def test_columntransformer_standalone_fit_transform(new_penguins_df):
    transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    result = transformer.fit_transform(
        new_penguins_df[["species", "culmen_length_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pandas.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "standard_scaled_culmen_length_mm": [
                1.313249,
                -0.20198,
                -1.111118,
            ],
            "standard_scaled_flipper_length_mm": [1.251098, -1.196588, -0.054338],
        },
        index=pandas.Index([1633, 1672, 1690], dtype="Int64", name="tag_number"),
    )

    pandas.testing.assert_frame_equal(result, expected, rtol=0.1, check_dtype=False)


def test_columntransformer_save_load(new_penguins_df, dataset_id):
    transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )
    transformer.fit(
        new_penguins_df[["species", "culmen_length_mm", "flipper_length_mm"]]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )

    assert isinstance(reloaded_transformer, compose.ColumnTransformer)

    expected = [
        (
            "one_hot_encoder",
            preprocessing.OneHotEncoder(max_categories=1000001, min_frequency=0),
            "species",
        ),
        ("standard_scaler", preprocessing.StandardScaler(), "culmen_length_mm"),
        ("standard_scaler", preprocessing.StandardScaler(), "flipper_length_mm"),
    ]
    assert reloaded_transformer.transformers_ == expected
    assert reloaded_transformer._bqml_model is not None

    result = transformer.fit_transform(
        new_penguins_df[["species", "culmen_length_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pandas.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "standard_scaled_culmen_length_mm": [
                1.313249,
                -0.20198,
                -1.111118,
            ],
            "standard_scaled_flipper_length_mm": [1.251098, -1.196588, -0.054338],
        },
        index=pandas.Index([1633, 1672, 1690], dtype="Int64", name="tag_number"),
    )

    pandas.testing.assert_frame_equal(result, expected, rtol=0.1, check_dtype=False)
