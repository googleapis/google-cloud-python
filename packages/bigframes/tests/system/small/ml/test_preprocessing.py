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
            "standard_scaled_culmen_depth_mm": [0.836148, 0.024748, 0.48116],
            "standard_scaled_culmen_length_mm": [-0.81112, -0.994552, -1.104611],
            "standard_scaled_flipper_length_mm": [-0.350044, -1.418336, -0.9198],
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
            "standard_scaled_culmen_depth_mm": [1.17072, -1.272416, 0.101848],
            "standard_scaled_culmen_length_mm": [1.313249, -0.20198, -1.111118],
            "standard_scaled_flipper_length_mm": [1.251089, -1.196588, -0.054338],
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
            "standard_scaled_culmen_length_mm": [
                -0.811119671289163,
                -0.9945520581113803,
                -1.104611490204711,
            ],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_max_abs_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.MaxAbsScaler, when BQML's change is in prod.
    scaler = bigframes.ml.preprocessing.MaxAbsScaler()
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

    # If maxabs-scaled correctly, max should be 1.0
    for column in result.columns:
        assert math.isclose(result[column].max(), 1.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_depth_mm": [0.874419, 0.8, 0.84186],
            "max_abs_scaled_culmen_length_mm": [0.662752, 0.645973, 0.635906],
            "max_abs_scaled_flipper_length_mm": [0.848485, 0.78355, 0.813853],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_max_abs_scaler_normalizeds_fit_transform(new_penguins_df):
    scaler = bigframes.ml.preprocessing.MaxAbsScaler()
    result = scaler.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_depth_mm": [1.0, 0.914894, 0.962766],
            "max_abs_scaled_culmen_length_mm": [1.0, 0.974684, 0.959494],
            "max_abs_scaled_flipper_length_mm": [1.0, 0.923469, 0.959184],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_max_abs_scaler_series_normalizes(penguins_df_default_index, new_penguins_df):
    scaler = bigframes.ml.preprocessing.MaxAbsScaler()
    scaler.fit(penguins_df_default_index["culmen_length_mm"])

    result = scaler.transform(penguins_df_default_index["culmen_length_mm"]).to_pandas()

    # If maxabs-scaled correctly, max should be 1.0
    for column in result.columns:
        assert math.isclose(result[column].max(), 1.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_length_mm": [0.662752, 0.645973, 0.635906],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_min_max_scaler_normalized_fit_transform(new_penguins_df):
    scaler = bigframes.ml.preprocessing.MinMaxScaler()
    result = scaler.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_depth_mm": [1.0, 0.0, 0.5625],
            "min_max_scaled_culmen_length_mm": [1.0, 0.375, 0.0],
            "min_max_scaled_flipper_length_mm": [1.0, 0.0, 0.466667],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_min_max_scaler_series_normalizes(penguins_df_default_index, new_penguins_df):
    scaler = bigframes.ml.preprocessing.MinMaxScaler()
    scaler.fit(penguins_df_default_index["culmen_length_mm"])

    result = scaler.transform(penguins_df_default_index["culmen_length_mm"]).to_pandas()

    # If minmax-scaled correctly, min should be 0 and max should be 1.
    for column in result.columns:
        assert math.isclose(result[column].max(), 1.0, abs_tol=1e-3)
        assert math.isclose(result[column].min(), 0.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_length_mm": [0.269091, 0.232727, 0.210909],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_min_max_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.MinMaxScaler, when BQML's change is in prod.
    scaler = bigframes.ml.preprocessing.MinMaxScaler()
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

    # If minmax-scaled correctly, min should be 0 and max should be 1.
    for column in result.columns:
        assert math.isclose(result[column].max(), 1.0, abs_tol=1e-3)
        assert math.isclose(result[column].min(), 0.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_depth_mm": [0.678571, 0.4880952, 0.595238],
            "min_max_scaled_culmen_length_mm": [0.269091, 0.232727, 0.210909],
            "min_max_scaled_flipper_length_mm": [0.40678, 0.152542, 0.271186],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_k_bins_discretizer_normalized_fit_transform_default_params(new_penguins_df):
    discretizer = bigframes.ml.preprocessing.KBinsDiscretizer(strategy="uniform")
    result = discretizer.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_depth_mm": ["bin_5", "bin_2", "bin_4"],
            "kbinsdiscretizer_culmen_length_mm": ["bin_5", "bin_3", "bin_2"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_5", "bin_2", "bin_4"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_k_bins_discretizer_series_normalizes(
    penguins_df_default_index, new_penguins_df
):
    discretizer = bigframes.ml.preprocessing.KBinsDiscretizer(strategy="uniform")
    discretizer.fit(penguins_df_default_index["culmen_length_mm"])

    result = discretizer.transform(
        penguins_df_default_index["culmen_length_mm"]
    ).to_pandas()
    result = discretizer.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_3", "bin_3", "bin_3"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_k_bins_discretizer_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.KBinsDiscretizer, when BQML's change is in prod.
    discretizer = bigframes.ml.preprocessing.KBinsDiscretizer(strategy="uniform")
    discretizer.fit(
        penguins_df_default_index[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    )

    result = discretizer.transform(
        penguins_df_default_index[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    ).to_pandas()

    result = discretizer.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_depth_mm": ["bin_5", "bin_4", "bin_4"],
            "kbinsdiscretizer_culmen_length_mm": ["bin_3", "bin_3", "bin_3"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_4", "bin_2", "bin_3"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_k_bins_discretizer_normalizes_different_params(
    penguins_df_default_index, new_penguins_df
):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.KBinsDiscretizer, when BQML's change is in prod.
    discretizer = bigframes.ml.preprocessing.KBinsDiscretizer(
        n_bins=6, strategy="uniform"
    )
    discretizer.fit(
        penguins_df_default_index[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    )

    result = discretizer.transform(
        penguins_df_default_index[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]
        ]
    ).to_pandas()

    result = discretizer.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_depth_mm": ["bin_6", "bin_4", "bin_5"],
            "kbinsdiscretizer_culmen_length_mm": ["bin_3", "bin_3", "bin_3"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_4", "bin_2", "bin_3"],
        },
        dtype="string[pyarrow]",
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


def test_label_encoder_default_params(new_penguins_df):
    encoder = bigframes.ml.preprocessing.LabelEncoder()
    encoder.fit(new_penguins_df["species"])

    result = encoder.transform(new_penguins_df["species"]).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "labelencoded_species": [
                1,
                1,
                2,
            ],
        },
        dtype="Int64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_label_encoder_default_params_fit_transform(new_penguins_df):
    encoder = bigframes.ml.preprocessing.LabelEncoder()

    result = encoder.fit_transform(new_penguins_df[["species"]]).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "labelencoded_species": [
                1,
                1,
                2,
            ],
        },
        dtype="Int64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_label_encoder_series_default_params(new_penguins_df):
    encoder = bigframes.ml.preprocessing.LabelEncoder()
    encoder.fit(new_penguins_df["species"])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "labelencoded_species": [
                1,
                1,
                2,
            ],
        },
        dtype="Int64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_label_encoder_params(new_penguins_df):
    encoder = bigframes.ml.preprocessing.LabelEncoder(100, 2)
    encoder.fit(new_penguins_df[["species"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "labelencoded_species": [
                0,
                0,
                0,
            ],
        },
        dtype="Int64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_label_encoder_different_data(penguins_df_default_index, new_penguins_df):
    encoder = bigframes.ml.preprocessing.LabelEncoder()
    encoder.fit(penguins_df_default_index[["species"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "labelencoded_species": [
                1,
                1,
                2,
            ],
        },
        dtype="Int64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


# TODO(garrettwu): add OneHotEncoder tests to compare with sklearn.
