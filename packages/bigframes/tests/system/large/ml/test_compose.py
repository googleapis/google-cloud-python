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

from bigframes.ml import compose, preprocessing
from tests.system import utils


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

    utils.check_pandas_df_schema_and_index(
        result,
        columns=[
            "onehotencoded_species",
            "standard_scaled_culmen_length_mm",
            "min_max_scaled_culmen_length_mm",
            "standard_scaled_flipper_length_mm",
        ],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


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

    utils.check_pandas_df_schema_and_index(
        result,
        columns=[
            "onehotencoded_species",
            "standard_scaled_culmen_length_mm",
            "standard_scaled_flipper_length_mm",
        ],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


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
    assert set(reloaded_transformer.transformers) == set(expected)
    assert reloaded_transformer._bqml_model is not None

    result = transformer.fit_transform(
        new_penguins_df[["species", "culmen_length_mm", "flipper_length_mm"]]
    ).to_pandas()

    utils.check_pandas_df_schema_and_index(
        result,
        columns=[
            "onehotencoded_species",
            "standard_scaled_culmen_length_mm",
            "standard_scaled_flipper_length_mm",
        ],
        index=[1633, 1672, 1690],
        col_exact=False,
    )
