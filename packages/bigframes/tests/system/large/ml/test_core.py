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

from bigframes.ml import globals
from bigframes.testing import utils


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

    eval_metrics = [
        "mean_absolute_error",
        "mean_squared_error",
        "mean_squared_log_error",
        "median_absolute_error",
        "r2_score",
        "explained_variance",
    ]
    # no data - report evaluation from the automatic data split
    evaluate_result = model.evaluate().to_pandas()
    utils.check_pandas_df_schema_and_index(
        evaluate_result, columns=eval_metrics, index=1
    )

    # evaluate on all training data
    evaluate_result = model.evaluate(df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        evaluate_result, columns=eval_metrics, index=1
    )

    # predict new labels
    predictions = model.predict(new_penguins_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_body_mass_g"],
        index=[1633, 1672, 1690],
        col_exact=False,
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

    eval_metrics = [
        "mean_absolute_error",
        "mean_squared_error",
        "mean_squared_log_error",
        "median_absolute_error",
        "r2_score",
        "explained_variance",
    ]

    # no data - report evaluation from the automatic data split
    evaluate_result = model.evaluate().to_pandas()
    utils.check_pandas_df_schema_and_index(
        evaluate_result, columns=eval_metrics, index=1
    )

    # evaluate on all training data
    evaluate_result = model.evaluate(df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        evaluate_result, columns=eval_metrics, index=1
    )

    # predict new labels
    predictions = model.predict(new_penguins_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_body_mass_g"],
        index=[1633, 1672, 1690],
        col_exact=False,
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
    start_execution_count = model.session._metrics.execution_count

    transformed = model.transform(new_penguins_df)

    end_execution_count = model.session._metrics.execution_count
    assert end_execution_count - start_execution_count == 1

    utils.check_pandas_df_schema_and_index(
        transformed.to_pandas(),
        columns=["scaled_culmen_length_mm", "onehotencoded_species"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )
