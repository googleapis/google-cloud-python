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

import bigframes.ml.cluster
import bigframes.ml.compose
import bigframes.ml.linear_model
import bigframes.ml.pipeline
import bigframes.ml.preprocessing


def test_columntransformer_standalone_fit_and_transform(
    penguins_df_default_index, new_penguins_df
):
    transformer = bigframes.ml.compose.ColumnTransformer(
        [
            (
                "onehot",
                bigframes.ml.preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "scale",
                bigframes.ml.preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    transformer.fit(
        penguins_df_default_index[["species", "culmen_length_mm", "flipper_length_mm"]]
    )
    result = transformer.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

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
            "standard_scaled_flipper_length_mm": [-0.350044, -1.418336, -0.9198],
        },
        index=pandas.Index([1633, 1672, 1690], dtype="Int64", name="tag_number"),
    )
    expected.standard_scaled_culmen_length_mm = (
        expected.standard_scaled_culmen_length_mm.astype("Float64")
    )
    expected.standard_scaled_flipper_length_mm = (
        expected.standard_scaled_flipper_length_mm.astype("Float64")
    )

    pandas.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_columntransformer_standalone_fit_transform(new_penguins_df):
    transformer = bigframes.ml.compose.ColumnTransformer(
        [
            (
                "onehot",
                bigframes.ml.preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "scale",
                bigframes.ml.preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    result = transformer.fit_transform(
        new_penguins_df[["species", "culmen_length_mm", "flipper_length_mm"]]
    ).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

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
    expected.standard_scaled_culmen_length_mm = (
        expected.standard_scaled_culmen_length_mm.astype("Float64")
    )
    expected.standard_scaled_flipper_length_mm = (
        expected.standard_scaled_flipper_length_mm.astype("Float64")
    )

    pandas.testing.assert_frame_equal(result, expected, rtol=1e-3)
