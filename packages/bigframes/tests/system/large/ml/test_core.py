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

from bigframes.ml import globals


def test_bqml_e2e(session, dataset_id, penguins_df_default_index, new_penguins_df):
    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_train = df[["body_mass_g"]]

    model = globals.bqml_model_factory().create_model(
        X_train, y_train, options={"model_type": "linear_reg"}
    )

    # no data - report evaluation from the automatic data split
    evaluate_result = model.evaluate().to_pandas()
    evaluate_expected = pandas.DataFrame(
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
    evaluate_expected = evaluate_expected.reindex(
        index=evaluate_expected.index.astype("Int64")
    )
    pandas.testing.assert_frame_equal(
        evaluate_result, evaluate_expected, check_exact=False, rtol=0.1
    )

    # evaluate on all training data
    evaluate_result = model.evaluate(df).to_pandas()
    pandas.testing.assert_frame_equal(
        evaluate_result, evaluate_expected, check_exact=False, rtol=0.1
    )

    # predict new labels
    predictions = model.predict(new_penguins_df).to_pandas()
    expected = pandas.DataFrame(
        {"predicted_body_mass_g": [4030.1, 3280.8, 3177.9]},
        dtype="Float64",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]], expected, check_exact=False, rtol=0.1
    )

    new_name = f"{dataset_id}.my_model"
    new_model = model.copy(new_name, True)
    assert new_model.model_name == new_name

    fetch_result = session.bqclient.get_model(new_name)
    assert fetch_result.model_type == "LINEAR_REGRESSION"


def test_bqml_manual_preprocessing_e2e(
    session, dataset_id, penguins_df_default_index, new_penguins_df
):
    base_sql_generator = globals.base_sql_generator()
    bqml_model_factory = globals.bqml_model_factory()

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    transforms = [
        base_sql_generator.ml_standard_scaler(column, column)
        for column in X_train.columns.tolist()
    ]
    transforms.extend(y_train.columns.tolist())
    options = {"model_type": "linear_reg"}
    model = bqml_model_factory.create_model(
        X_train, y_train, transforms=transforms, options=options
    )

    # no data - report evaluation from the automatic data split
    evaluate_result = model.evaluate().to_pandas()
    evaluate_expected = pandas.DataFrame(
        {
            "mean_absolute_error": [309.477334],
            "mean_squared_error": [152184.227218],
            "mean_squared_log_error": [0.009524],
            "median_absolute_error": [257.727777],
            "r2_score": [0.764356],
            "explained_variance": [0.764356],
        },
        dtype="Float64",
    )
    evaluate_expected = evaluate_expected.reindex(
        index=evaluate_expected.index.astype("Int64")
    )

    pandas.testing.assert_frame_equal(
        evaluate_result, evaluate_expected, check_exact=False, rtol=0.1
    )

    # evaluate on all training data
    evaluate_result = model.evaluate(df).to_pandas()
    pandas.testing.assert_frame_equal(
        evaluate_result, evaluate_expected, check_exact=False, rtol=0.1
    )

    # predict new labels
    predictions = model.predict(new_penguins_df).to_pandas()
    expected = pandas.DataFrame(
        {"predicted_body_mass_g": [3968.8, 3176.3, 3545.2]},
        dtype="Float64",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]], expected, check_exact=False, rtol=0.1
    )

    new_name = f"{dataset_id}.my_model"
    new_model = model.copy(new_name, True)
    assert new_model.model_name == new_name

    fetch_result = session.bqclient.get_model(new_name)
    assert fetch_result.model_type == "LINEAR_REGRESSION"


def test_bqml_standalone_transform(penguins_df_default_index, new_penguins_df):
    bqml_model_factory = globals.bqml_model_factory()

    X = penguins_df_default_index[["culmen_length_mm", "species"]]
    model = bqml_model_factory.create_model(
        X,
        options={"model_type": "transform_only"},
        transforms=[
            "ML.STANDARD_SCALER(culmen_length_mm) OVER() AS scaled_culmen_length_mm",
            "ML.ONE_HOT_ENCODER(species, 'none', 1000000, 0) OVER() AS onehotencoded_species",
        ],
    )

    transformed = model.transform(new_penguins_df).to_pandas()
    expected = pandas.DataFrame(
        {
            "scaled_culmen_length_mm": [-0.8099, -0.9931, -1.103],
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    expected["scaled_culmen_length_mm"] = expected["scaled_culmen_length_mm"].astype(
        "Float64"
    )
    pandas.testing.assert_frame_equal(
        transformed[["scaled_culmen_length_mm", "onehotencoded_species"]],
        expected,
        check_exact=False,
        rtol=0.1,
    )
