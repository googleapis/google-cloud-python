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
from bigframes.testing import utils


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
            (
                "increment",
                compose.SQLScalarColumnTransformer("{0}+1"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "length",
                compose.SQLScalarColumnTransformer(
                    "CASE WHEN {0} IS NULL THEN -1 ELSE LENGTH({0}) END",
                    target_column="len_{0}",
                ),
                "species",
            ),
            (
                "ohe",
                compose.SQLScalarColumnTransformer(
                    "CASE WHEN {0}='Adelie Penguin (Pygoscelis adeliae)' THEN 1 ELSE 0 END",
                    target_column="ohe_adelie",
                ),
                "species",
            ),
            (
                "identity",
                compose.SQLScalarColumnTransformer("{0}", target_column="{0}"),
                ["culmen_length_mm", "flipper_length_mm"],
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
            "transformed_culmen_length_mm",
            "transformed_flipper_length_mm",
            "len_species",
            "ohe_adelie",
            "culmen_length_mm",
            "flipper_length_mm",
        ],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


def test_columntransformer_standalone_fit_transform(new_penguins_df):
    # rename column to ensure robustness to column names that must be escaped
    new_penguins_df = new_penguins_df.rename(columns={"species": "123 'species'"})
    transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "123 'species'",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "length",
                compose.SQLScalarColumnTransformer(
                    "CASE WHEN {0} IS NULL THEN -1 ELSE LENGTH({0}) END",
                    target_column="len_{0}",
                ),
                "123 'species'",
            ),
            (
                "identity",
                compose.SQLScalarColumnTransformer("{0}", target_column="{0}"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    result = transformer.fit_transform(
        new_penguins_df[["123 'species'", "culmen_length_mm", "flipper_length_mm"]]
    ).to_pandas()

    utils.check_pandas_df_schema_and_index(
        result,
        columns=[
            "onehotencoded_123 'species'",
            "standard_scaled_culmen_length_mm",
            "standard_scaled_flipper_length_mm",
            "len_123 'species'",
            "culmen_length_mm",
            "flipper_length_mm",
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
            (
                "length",
                compose.SQLScalarColumnTransformer(
                    "CASE WHEN {0} IS NULL THEN -1 ELSE LENGTH({0}) END",
                    target_column="len_{0}",
                ),
                "species",
            ),
            (
                "identity",
                compose.SQLScalarColumnTransformer("{0}", target_column="{0}"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "flexname",
                compose.SQLScalarColumnTransformer(
                    "CASE WHEN {0} IS NULL THEN -1 ELSE LENGTH({0}) END",
                    target_column="Flex {0} Name",
                ),
                "species",
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
        (
            "sql_scalar_column_transformer",
            compose.SQLScalarColumnTransformer(
                "CASE WHEN `species` IS NULL THEN -1 ELSE LENGTH(`species`) END",
                target_column="len_species",
            ),
            "?len_species",
        ),
        (
            "sql_scalar_column_transformer",
            compose.SQLScalarColumnTransformer(
                "`flipper_length_mm`", target_column="flipper_length_mm"
            ),
            "?flipper_length_mm",
        ),
        (
            "sql_scalar_column_transformer",
            compose.SQLScalarColumnTransformer(
                "`culmen_length_mm`", target_column="culmen_length_mm"
            ),
            "?culmen_length_mm",
        ),
        (
            "sql_scalar_column_transformer",
            compose.SQLScalarColumnTransformer(
                "CASE WHEN `species` IS NULL THEN -1 ELSE LENGTH(`species`) END",
                target_column="Flex species Name",
            ),
            "?Flex species Name",
        ),
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
            "len_species",
            "culmen_length_mm",
            "flipper_length_mm",
            "Flex species Name",
        ],
        index=[1633, 1672, 1690],
        col_exact=False,
    )
