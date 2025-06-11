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

from datetime import datetime
import typing

import pandas as pd
import pyarrow as pa
import pytest
import pytz

import bigframes
import bigframes.features
from bigframes.ml import core
from bigframes.testing import utils


def test_model_eval(
    penguins_bqml_linear_model,
):
    result = penguins_bqml_linear_model.evaluate().to_pandas()
    expected = pd.DataFrame(
        {
            "mean_absolute_error": [227.01223],
            "mean_squared_error": [81838.159892],
            "mean_squared_log_error": [0.00507],
            "median_absolute_error": [173.080816],
            "r2_score": [0.872377],
            "explained_variance": [0.872377],
        },
        dtype="Float64",
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_model_eval_with_data(penguins_bqml_linear_model, penguins_df_default_index):
    result = penguins_bqml_linear_model.evaluate(
        penguins_df_default_index.dropna()
    ).to_pandas()
    expected = pd.DataFrame(
        {
            "mean_absolute_error": [225.817334],
            "mean_squared_error": [80540.705944],
            "mean_squared_log_error": [0.004972],
            "median_absolute_error": [173.080816],
            "r2_score": [0.87529],
            "explained_variance": [0.87529],
        },
        dtype="Float64",
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_model_centroids(penguins_bqml_kmeans_model: core.BqmlModel):
    result = penguins_bqml_kmeans_model.centroids().to_pandas()
    expected = (
        pd.DataFrame(
            {
                "centroid_id": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
                "feature": [
                    "culmen_length_mm",
                    "culmen_depth_mm",
                    "flipper_length_mm",
                    "sex",
                ]
                * 3,
                "numerical_value": [
                    47.509677,
                    14.993548,
                    217.040123,
                    pd.NA,
                    38.207813,
                    18.03125,
                    187.992188,
                    pd.NA,
                    47.036346,
                    18.834808,
                    197.1612,
                    pd.NA,
                ],
                "categorical_value": [
                    [],
                    [],
                    [],
                    [
                        {"category": ".", "value": 0.008064516129032258},
                        {"category": "MALE", "value": 0.49193548387096775},
                        {"category": "FEMALE", "value": 0.47580645161290325},
                        {"category": "_null_filler", "value": 0.024193548387096774},
                    ],
                    [],
                    [],
                    [],
                    [
                        {"category": "MALE", "value": 0.34375},
                        {"category": "FEMALE", "value": 0.625},
                        {"category": "_null_filler", "value": 0.03125},
                    ],
                    [],
                    [],
                    [],
                    [
                        {"category": "MALE", "value": 0.6847826086956522},
                        {"category": "FEMALE", "value": 0.2826086956521739},
                        {"category": "_null_filler", "value": 0.03260869565217391},
                    ],
                ],
            },
        )
        .sort_values(["centroid_id", "feature"])
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
        check_dtype=False,
    )


def test_pca_model_principal_components(penguins_bqml_pca_model: core.BqmlModel):
    result = penguins_bqml_pca_model.principal_components().to_pandas()
    assert result.shape == (21, 4)

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

    utils.assert_pandas_df_equal_pca_components(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
    )


def test_pca_model_principal_component_info(penguins_bqml_pca_model: core.BqmlModel):
    result = penguins_bqml_pca_model.principal_component_info().to_pandas()
    assert result.shape == (3, 4)

    expected = pd.DataFrame(
        {
            "principal_component_id": [0, 1, 2],
            "eigenvalue": [3.278657, 1.270829, 1.125354],
            "explained_variance_ratio": [0.469357, 0.181926, 0.1611],
            "cumulative_explained_variance_ratio": [0.469357, 0.651283, 0.812383],
        },
    )
    utils.assert_pandas_df_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
        check_dtype=False,
        ignore_order=True,
    )


def test_model_predict(penguins_bqml_linear_model: core.BqmlModel, new_penguins_df):
    predictions = penguins_bqml_linear_model.predict(new_penguins_df).to_pandas()
    expected = pd.DataFrame(
        {"predicted_body_mass_g": [4030.1, 3280.8, 3177.9]},
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]].sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_model_predict_explain(
    penguins_bqml_linear_model: core.BqmlModel, new_penguins_df
):
    options = {"top_k_features": 3}
    predictions = penguins_bqml_linear_model.explain_predict(
        new_penguins_df, options
    ).to_pandas()
    expected = pd.DataFrame(
        {
            "predicted_body_mass_g": [4030.1, 3280.8, 3177.9],
            "approximation_error": [0.0, 0.0, 0.0],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g", "approximation_error"]].sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_model_predict_with_unnamed_index(
    penguins_bqml_linear_model: core.BqmlModel, new_penguins_df
):
    # This will result in an index that lacks a name, which the ML library will
    # need to persist through the call to ML.PREDICT
    new_penguins_df = new_penguins_df.reset_index()

    # remove the middle tag number to ensure we're really keeping the unnamed index
    new_penguins_df = typing.cast(
        bigframes.dataframe.DataFrame,
        new_penguins_df[new_penguins_df.tag_number != 1672],
    )

    predictions = penguins_bqml_linear_model.predict(new_penguins_df).to_pandas()

    expected = pd.DataFrame(
        {"predicted_body_mass_g": [4030.1, 3177.9]},
        dtype="Float64",
        index=pd.Index([0, 2], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]].sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_model_predict_explain_with_unnamed_index(
    penguins_bqml_linear_model: core.BqmlModel, new_penguins_df
):
    # This will result in an index that lacks a name, which the ML library will
    # need to persist through the call to ML.PREDICT
    new_penguins_df = new_penguins_df.reset_index()

    options = {"top_k_features": 3}
    # remove the middle tag number to ensure we're really keeping the unnamed index
    new_penguins_df = typing.cast(
        bigframes.dataframe.DataFrame,
        new_penguins_df[new_penguins_df.tag_number != 1672],
    )

    predictions = penguins_bqml_linear_model.explain_predict(
        new_penguins_df, options
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "predicted_body_mass_g": [4030.1, 3177.9],
            "approximation_error": [0.0, 0.0],
        },
        dtype="Float64",
        index=pd.Index([0, 2], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g", "approximation_error"]].sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_model_detect_anomalies(
    penguins_bqml_pca_model: core.BqmlModel, new_penguins_df
):
    options = {"contamination": 0.25}
    anomalies = penguins_bqml_pca_model.detect_anomalies(
        new_penguins_df, options
    ).to_pandas()
    expected = pd.DataFrame(
        {
            "is_anomaly": [True, True, True],
            "mean_squared_error": [0.254188, 0.731243, 0.298889],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        anomalies[["is_anomaly", "mean_squared_error"]].sort_index(),
        expected,
        check_exact=False,
        check_dtype=False,
        rtol=0.1,
    )


@pytest.mark.skip("b/353775058 BQML internal error")
def test_remote_model_predict(
    bqml_linear_remote_model: core.BqmlModel, new_penguins_df
):
    expected = pd.DataFrame(
        {"predicted_body_mass_g": [[3739.54], [3675.79], [3619.54]]},
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
        dtype=(
            pd.ArrowDtype(pa.list_(pa.float64()))
            if bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable
            else "object"
        ),
    )
    predictions = bqml_linear_remote_model.predict(new_penguins_df).to_pandas()
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]].sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_model_forecast(
    time_series_bqml_arima_plus_model: core.BqmlModel,
    time_series_bqml_arima_plus_model_w_id: core.BqmlModel,
    id_col_name,
):
    utc = pytz.utc
    forecast_cols = ["forecast_timestamp", "forecast_value"]
    if id_col_name:
        forecast_cols.insert(0, id_col_name)

    forecast = (
        time_series_bqml_arima_plus_model_w_id.forecast(
            {"horizon": 4, "confidence_level": 0.8}
        )
        if id_col_name
        else time_series_bqml_arima_plus_model.forecast(
            {"horizon": 4, "confidence_level": 0.8}
        )
    ).to_pandas()[forecast_cols]
    if id_col_name:
        expected = pd.DataFrame(
            {
                "id": ["1", "2", "1", "2", "1", "2", "1", "2"],
                "forecast_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 5, tzinfo=utc),
                    datetime(2017, 8, 5, tzinfo=utc),
                ],
                "forecast_value": [
                    2634.796023,
                    2634.796023,
                    2621.332462,
                    2621.332462,
                    2396.095463,
                    2396.095463,
                    1742.878278,
                    1742.878278,
                ],
            }
        )
        expected["id"] = expected["id"].astype("string[pyarrow]")
    else:
        expected = pd.DataFrame(
            {
                "forecast_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 5, tzinfo=utc),
                ],
                "forecast_value": [2634.796023, 2621.332462, 2396.095463, 1742.878278],
            }
        )
    expected["forecast_value"] = expected["forecast_value"].astype(pd.Float64Dtype())
    expected["forecast_timestamp"] = expected["forecast_timestamp"].astype(
        pd.ArrowDtype(pa.timestamp("us", tz="UTC"))
    )
    pd.testing.assert_frame_equal(
        forecast,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


def test_model_register(ephemera_penguins_bqml_linear_model: core.BqmlModel):
    model = ephemera_penguins_bqml_linear_model

    start_execution_count = model.session._metrics.execution_count

    model.register()

    end_execution_count = model.session._metrics.execution_count
    assert end_execution_count - start_execution_count == 1

    assert model.model.model_id is not None
    model_name = "bigframes_" + model.model.model_id
    # Only registered model contains the field, and the field includes project/dataset. Here only check model_id.
    assert model_name in model.model.training_runs[-1]["vertexAiModelId"]


def test_model_register_with_params(
    ephemera_penguins_bqml_linear_model: core.BqmlModel,
):
    model_name = "bigframes_system_test_model"
    model = ephemera_penguins_bqml_linear_model
    model.register(model_name)

    # Only registered model contains the field, and the field includes project/dataset. Here only check model_id.
    assert model_name in model.model.training_runs[-1]["vertexAiModelId"]
