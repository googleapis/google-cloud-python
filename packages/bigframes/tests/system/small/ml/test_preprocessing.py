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
import pyarrow as pa

import bigframes.features
from bigframes.ml import preprocessing
from bigframes.testing import utils

ONE_HOT_ENCODED_DTYPE = (
    pd.ArrowDtype(pa.list_(pa.struct([("index", pa.int64()), ("value", pa.float64())])))
    if bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable
    else "object"
)


def test_standard_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.StandardScaler, when BQML's change is in prod.
    scaler = preprocessing.StandardScaler()
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

    expected = pd.DataFrame(
        {
            "standard_scaled_culmen_length_mm": [-0.81112, -0.994552, -1.104611],
            "standard_scaled_culmen_depth_mm": [0.836148, 0.024748, 0.48116],
            "standard_scaled_flipper_length_mm": [-0.350044, -1.418336, -0.9198],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_standard_scaler_normalizeds_fit_transform(new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.StandardScaler, when BQML's change is in prod.
    scaler = preprocessing.StandardScaler()
    result = scaler.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    # If standard-scaled correctly, mean should be 0.0
    for column in result.columns:
        assert math.isclose(result[column].mean(), 0.0, abs_tol=1e-3)

    expected = pd.DataFrame(
        {
            "standard_scaled_culmen_length_mm": [1.313249, -0.20198, -1.111118],
            "standard_scaled_culmen_depth_mm": [1.17072, -1.272416, 0.101848],
            "standard_scaled_flipper_length_mm": [1.251089, -1.196588, -0.054338],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_standard_scaler_series_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.StandardScaler, when BQML's change is in prod.
    scaler = preprocessing.StandardScaler()
    scaler.fit(penguins_df_default_index["culmen_length_mm"])

    result = scaler.transform(penguins_df_default_index["culmen_length_mm"]).to_pandas()

    # If standard-scaled correctly, mean should be 0.0
    for column in result.columns:
        assert math.isclose(result[column].mean(), 0.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

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

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_standard_scaler_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.StandardScaler()
    transformer.fit(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.StandardScaler)
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "standard_scaled_culmen_length_mm": [1.313249, -0.20198, -1.111118],
            "standard_scaled_culmen_depth_mm": [1.17072, -1.272416, 0.101848],
            "standard_scaled_flipper_length_mm": [1.251089, -1.196588, -0.054338],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_max_abs_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.MaxAbsScaler, when BQML's change is in prod.
    scaler = preprocessing.MaxAbsScaler()
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

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_length_mm": [0.662752, 0.645973, 0.635906],
            "max_abs_scaled_culmen_depth_mm": [0.874419, 0.8, 0.84186],
            "max_abs_scaled_flipper_length_mm": [0.848485, 0.78355, 0.813853],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_max_abs_scaler_normalizeds_fit_transform(new_penguins_df):
    scaler = preprocessing.MaxAbsScaler()
    result = scaler.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_length_mm": [1.0, 0.974684, 0.959494],
            "max_abs_scaled_culmen_depth_mm": [1.0, 0.914894, 0.962766],
            "max_abs_scaled_flipper_length_mm": [1.0, 0.923469, 0.959184],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_max_abs_scaler_series_normalizes(penguins_df_default_index, new_penguins_df):
    scaler = preprocessing.MaxAbsScaler()
    scaler.fit(penguins_df_default_index["culmen_length_mm"])

    result = scaler.transform(penguins_df_default_index["culmen_length_mm"]).to_pandas()

    # If maxabs-scaled correctly, max should be 1.0
    for column in result.columns:
        assert math.isclose(result[column].max(), 1.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_length_mm": [0.662752, 0.645973, 0.635906],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_max_abs_scaler_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.MaxAbsScaler()
    transformer.fit(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.MaxAbsScaler)
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "max_abs_scaled_culmen_length_mm": [1.0, 0.974684, 0.959494],
            "max_abs_scaled_culmen_depth_mm": [1.0, 0.914894, 0.962766],
            "max_abs_scaled_flipper_length_mm": [1.0, 0.923469, 0.959184],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_min_max_scaler_normalized_fit_transform(new_penguins_df):
    scaler = preprocessing.MinMaxScaler()
    result = scaler.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_length_mm": [1.0, 0.375, 0.0],
            "min_max_scaled_culmen_depth_mm": [1.0, 0.0, 0.5625],
            "min_max_scaled_flipper_length_mm": [1.0, 0.0, 0.466667],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_min_max_scaler_series_normalizes(penguins_df_default_index, new_penguins_df):
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(penguins_df_default_index["culmen_length_mm"])

    result = scaler.transform(penguins_df_default_index["culmen_length_mm"]).to_pandas()

    # If minmax-scaled correctly, min should be 0 and max should be 1.
    for column in result.columns:
        assert math.isclose(result[column].max(), 1.0, abs_tol=1e-3)
        assert math.isclose(result[column].min(), 0.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_length_mm": [0.269091, 0.232727, 0.210909],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_min_max_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.MinMaxScaler, when BQML's change is in prod.
    scaler = preprocessing.MinMaxScaler()
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

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_length_mm": [0.269091, 0.232727, 0.210909],
            "min_max_scaled_culmen_depth_mm": [0.678571, 0.4880952, 0.595238],
            "min_max_scaled_flipper_length_mm": [0.40678, 0.152542, 0.271186],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_min_max_scaler_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.MinMaxScaler()
    transformer.fit(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.MinMaxScaler)
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "min_max_scaled_culmen_length_mm": [1.0, 0.375, 0.0],
            "min_max_scaled_culmen_depth_mm": [1.0, 0.0, 0.5625],
            "min_max_scaled_flipper_length_mm": [1.0, 0.0, 0.466667],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_normalized_fit_transform_default_params(new_penguins_df):
    discretizer = preprocessing.KBinsDiscretizer(strategy="uniform")
    result = discretizer.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_5", "bin_3", "bin_2"],
            "kbinsdiscretizer_culmen_depth_mm": ["bin_5", "bin_2", "bin_4"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_5", "bin_2", "bin_4"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_normalized_fit_transform_default_params_quantile(
    new_penguins_df,
):
    discretizer = preprocessing.KBinsDiscretizer(strategy="quantile")
    result = discretizer.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_2", "bin_2", "bin_1"],
            "kbinsdiscretizer_culmen_depth_mm": ["bin_2", "bin_1", "bin_2"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_2", "bin_1", "bin_2"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_series_normalizes(
    penguins_df_default_index, new_penguins_df
):
    discretizer = preprocessing.KBinsDiscretizer(strategy="uniform")
    discretizer.fit(penguins_df_default_index["culmen_length_mm"])

    result = discretizer.transform(
        penguins_df_default_index["culmen_length_mm"]
    ).to_pandas()
    result = discretizer.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_3", "bin_3", "bin_3"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_series_normalizes_quantile(
    penguins_df_default_index, new_penguins_df
):
    discretizer = preprocessing.KBinsDiscretizer(strategy="quantile")
    discretizer.fit(penguins_df_default_index["culmen_length_mm"])

    result = discretizer.transform(
        penguins_df_default_index["culmen_length_mm"]
    ).to_pandas()
    result = discretizer.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_2", "bin_2", "bin_1"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.KBinsDiscretizer, when BQML's change is in prod.
    discretizer = preprocessing.KBinsDiscretizer(strategy="uniform")
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

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_3", "bin_3", "bin_3"],
            "kbinsdiscretizer_culmen_depth_mm": ["bin_5", "bin_4", "bin_4"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_4", "bin_2", "bin_3"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_normalizes_different_params(
    penguins_df_default_index, new_penguins_df
):
    # TODO(http://b/292431644): add a second test that compares output to sklearn.preprocessing.KBinsDiscretizer, when BQML's change is in prod.
    discretizer = preprocessing.KBinsDiscretizer(n_bins=6, strategy="uniform")
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

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_3", "bin_3", "bin_3"],
            "kbinsdiscretizer_culmen_depth_mm": ["bin_6", "bin_4", "bin_5"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_4", "bin_2", "bin_3"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.KBinsDiscretizer(n_bins=6, strategy="uniform")
    transformer.fit(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.KBinsDiscretizer)
    assert reloaded_transformer.n_bins == transformer.n_bins
    assert reloaded_transformer.strategy == transformer.strategy
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.fit_transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "kbinsdiscretizer_culmen_length_mm": ["bin_6", "bin_4", "bin_2"],
            "kbinsdiscretizer_culmen_depth_mm": ["bin_6", "bin_2", "bin_5"],
            "kbinsdiscretizer_flipper_length_mm": ["bin_6", "bin_2", "bin_4"],
        },
        dtype="string[pyarrow]",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=0.1)


def test_k_bins_discretizer_save_load_quantile(new_penguins_df, dataset_id):
    transformer = preprocessing.KBinsDiscretizer(n_bins=6, strategy="quantile")
    transformer.fit(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    )

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.KBinsDiscretizer)
    assert reloaded_transformer.n_bins == transformer.n_bins
    assert reloaded_transformer.strategy == transformer.strategy
    assert reloaded_transformer._bqml_model is not None


def test_one_hot_encoder_default_params(new_penguins_df):
    encoder = preprocessing.OneHotEncoder()
    encoder.fit(new_penguins_df[["species", "sex"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "onehotencoded_sex": [
                [{"index": 2, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
            ],
        },
        dtype=ONE_HOT_ENCODED_DTYPE,
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_default_params_fit_transform(new_penguins_df):
    encoder = preprocessing.OneHotEncoder()

    result = encoder.fit_transform(new_penguins_df[["species", "sex"]]).to_pandas()

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "onehotencoded_sex": [
                [{"index": 2, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
            ],
        },
        dtype=ONE_HOT_ENCODED_DTYPE,
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_series_default_params(new_penguins_df):
    encoder = preprocessing.OneHotEncoder()
    encoder.fit(new_penguins_df["species"])

    result = encoder.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        dtype=ONE_HOT_ENCODED_DTYPE,
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_params(new_penguins_df):
    encoder = preprocessing.OneHotEncoder("most_frequent", 100, 2)
    encoder.fit(new_penguins_df[["species", "sex"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
            ],
            "onehotencoded_sex": [
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
                [{"index": 0, "value": 1.0}],
            ],
        },
        dtype=ONE_HOT_ENCODED_DTYPE,
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_different_data(penguins_df_default_index, new_penguins_df):
    encoder = preprocessing.OneHotEncoder()
    encoder.fit(penguins_df_default_index[["species", "sex"]])

    result = encoder.transform(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "onehotencoded_sex": [
                [{"index": 3, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        dtype=ONE_HOT_ENCODED_DTYPE,
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_one_hot_encoder_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.OneHotEncoder(min_frequency=1, max_categories=10)
    transformer.fit(new_penguins_df[["species", "sex"]])

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.OneHotEncoder)
    assert reloaded_transformer.min_frequency == transformer.min_frequency
    assert reloaded_transformer.max_categories == transformer.max_categories
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.fit_transform(
        new_penguins_df[["species", "sex"]]
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
            "onehotencoded_sex": [
                [{"index": 2, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
            ],
        },
        dtype=ONE_HOT_ENCODED_DTYPE,
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)


def test_label_encoder_default_params(new_penguins_df):
    encoder = preprocessing.LabelEncoder()
    encoder.fit(new_penguins_df["species"])

    result = encoder.transform(new_penguins_df["species"]).to_pandas()

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
    encoder = preprocessing.LabelEncoder()

    result = encoder.fit_transform(new_penguins_df[["species"]]).to_pandas()

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
    encoder = preprocessing.LabelEncoder()
    encoder.fit(new_penguins_df["species"])

    result = encoder.transform(new_penguins_df).to_pandas()

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
    encoder = preprocessing.LabelEncoder(100, 2)
    encoder.fit(new_penguins_df[["species"]])

    result = encoder.transform(new_penguins_df).to_pandas()

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
    encoder = preprocessing.LabelEncoder()
    encoder.fit(penguins_df_default_index[["species"]])

    result = encoder.transform(new_penguins_df).to_pandas()

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


def test_label_encoder_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.LabelEncoder(min_frequency=1, max_categories=10)
    transformer.fit(new_penguins_df[["species"]])

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.LabelEncoder)
    assert reloaded_transformer.min_frequency == transformer.min_frequency
    assert reloaded_transformer.max_categories == transformer.max_categories
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.transform(new_penguins_df).to_pandas()

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


def test_poly_features_default_params(new_penguins_df):
    transformer = preprocessing.PolynomialFeatures()
    df = new_penguins_df[["culmen_length_mm", "culmen_depth_mm"]]
    transformer.fit(df)

    result = transformer.transform(df).to_pandas()

    expected = pd.DataFrame(
        {
            "poly_feat_culmen_length_mm": [
                39.5,
                38.5,
                37.9,
            ],
            "poly_feat_culmen_length_mm_culmen_length_mm": [
                1560.25,
                1482.25,
                1436.41,
            ],
            "poly_feat_culmen_length_mm_culmen_depth_mm": [
                742.6,
                662.2,
                685.99,
            ],
            "poly_feat_culmen_depth_mm": [
                18.8,
                17.2,
                18.1,
            ],
            "poly_feat_culmen_depth_mm_culmen_depth_mm": [
                353.44,
                295.84,
                327.61,
            ],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)


def test_poly_features_params(new_penguins_df):
    transformer = preprocessing.PolynomialFeatures(degree=3)
    df = new_penguins_df[["culmen_length_mm", "culmen_depth_mm"]]
    transformer.fit(df)

    result = transformer.transform(df).to_pandas()

    utils.check_pandas_df_schema_and_index(
        result,
        [
            "poly_feat_culmen_length_mm",
            "poly_feat_culmen_length_mm_culmen_length_mm",
            "poly_feat_culmen_length_mm_culmen_length_mm_culmen_length_mm",
            "poly_feat_culmen_length_mm_culmen_length_mm_culmen_depth_mm",
            "poly_feat_culmen_length_mm_culmen_depth_mm",
            "poly_feat_culmen_length_mm_culmen_depth_mm_culmen_depth_mm",
            "poly_feat_culmen_depth_mm",
            "poly_feat_culmen_depth_mm_culmen_depth_mm",
            "poly_feat_culmen_depth_mm_culmen_depth_mm_culmen_depth_mm",
        ],
        [1633, 1672, 1690],
    )


def test_poly_features_save_load(new_penguins_df, dataset_id):
    transformer = preprocessing.PolynomialFeatures(degree=3)
    transformer.fit(new_penguins_df[["culmen_length_mm", "culmen_depth_mm"]])

    reloaded_transformer = transformer.to_gbq(
        f"{dataset_id}.temp_configured_model", replace=True
    )
    assert isinstance(reloaded_transformer, preprocessing.PolynomialFeatures)
    assert reloaded_transformer.degree == 3
    assert reloaded_transformer._bqml_model is not None

    result = reloaded_transformer.transform(
        new_penguins_df[["culmen_length_mm", "culmen_depth_mm"]]
    ).to_pandas()

    utils.check_pandas_df_schema_and_index(
        result,
        [
            "poly_feat_culmen_length_mm",
            "poly_feat_culmen_length_mm_culmen_length_mm",
            "poly_feat_culmen_length_mm_culmen_length_mm_culmen_length_mm",
            "poly_feat_culmen_length_mm_culmen_length_mm_culmen_depth_mm",
            "poly_feat_culmen_length_mm_culmen_depth_mm",
            "poly_feat_culmen_length_mm_culmen_depth_mm_culmen_depth_mm",
            "poly_feat_culmen_depth_mm",
            "poly_feat_culmen_depth_mm_culmen_depth_mm",
            "poly_feat_culmen_depth_mm_culmen_depth_mm_culmen_depth_mm",
        ],
        [1633, 1672, 1690],
    )
