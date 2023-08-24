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

import math

import pandas as pd

import bigframes.ml.preprocessing


def test_standard_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.StandardScaler, when BQML's change is in prod.
    scaler = bigframes.ml.preprocessing.StandardScaler()
    scaler.fit(
        penguins_df_default_index[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    )

    result = scaler.transform(
        penguins_df_default_index[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    ).to_pandas()

    # If standard-scaled correctly, mean should be 0.0
    for column in result.columns:
        assert math.isclose(result[column].mean(), 0.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "scaled_culmen_depth_mm": [0.836148, 0.024748, 0.48116],
            "scaled_culmen_length_mm": [-0.81112, -0.994552, -1.104611],
            "scaled_flipper_length_mm": [-0.350044, -1.418336, -0.9198],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_standard_scaler_normalizeds_fit_transform(new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.StandardScaler, when BQML's change is in prod.
    scaler = bigframes.ml.preprocessing.StandardScaler()
    result = scaler.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    # If standard-scaled correctly, mean should be 0.0
    for column in result.columns:
        assert math.isclose(result[column].mean(), 0.0, abs_tol=1e-3)

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "scaled_culmen_depth_mm": [1.17072, -1.272416, 0.101848],
            "scaled_culmen_length_mm": [1.313249, -0.20198, -1.111118],
            "scaled_flipper_length_mm": [1.251089, -1.196588, -0.054338],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_standard_scaler_series_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.StandardScaler, when BQML's change is in prod.
    scaler = bigframes.ml.preprocessing.StandardScaler()
    scaler.fit(penguins_df_default_index["culmen_length_mm"])

    result = scaler.transform(penguins_df_default_index["culmen_length_mm"]).to_pandas()

    # If standard-scaled correctly, mean should be 0.0
    for column in result.columns:
        assert math.isclose(result[column].mean(), 0.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "scaled_culmen_length_mm": [
                -0.811119671289163,
                -0.9945520581113803,
                -1.104611490204711,
            ],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_one_hot_encoder_default_params(new_penguins_df):
    encoder = bigframes.ml.preprocessing.OneHotEncoder()
    encoder.fit(new_penguins_df[["species", "sex"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "onehotencoded_sex": [
                [{"index": 2, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
            ],
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_default_params_fit_transform(new_penguins_df):
    encoder = bigframes.ml.preprocessing.OneHotEncoder()

    result = encoder.fit_transform(new_penguins_df[["species", "sex"]]).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "onehotencoded_sex": [
                [{"index": 2, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
            ],
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_series_default_params(new_penguins_df):
    encoder = bigframes.ml.preprocessing.OneHotEncoder()
    encoder.fit(new_penguins_df["species"])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_params(new_penguins_df):
    encoder = bigframes.ml.preprocessing.OneHotEncoder("most_frequent", 100, 2)
    encoder.fit(new_penguins_df[["species", "sex"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "onehotencoded_sex": [
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
            ],
            "onehotencoded_species": [
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
            ],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_different_data(penguins_df_default_index, new_penguins_df):
    encoder = bigframes.ml.preprocessing.OneHotEncoder()
    encoder.fit(penguins_df_default_index[["species", "sex"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "onehotencoded_sex": [
                [{"index": 3, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


# TODO(garrettwu): add OneHotEncoder tests to compare with sklearn.
