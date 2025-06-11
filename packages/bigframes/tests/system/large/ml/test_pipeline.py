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

import pandas as pd
import pytest

from bigframes.ml import (
    cluster,
    compose,
    decomposition,
    ensemble,
    impute,
    linear_model,
    pipeline,
    preprocessing,
)
from bigframes.testing import utils


def test_pipeline_linear_regression_fit_score_predict(
    session, penguins_df_default_index
):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("linreg", linear_model.LinearRegression()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    score_result = pl.score(X_train, y_train).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Chinstrap penguin (Pygoscelis antarctica)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
                "sex": ["MALE", "FEMALE", "FEMALE"],
            }
        ).set_index("tag_number")
    )
    predictions = pl.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_body_mass_g"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


def test_pipeline_linear_regression_series_fit_score_predict(
    session, penguins_df_default_index
):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("linreg", linear_model.LinearRegression()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df["culmen_length_mm"]
    y_train = df["body_mass_g"]
    pl.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    score_result = pl.score(X_train, y_train).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "culmen_length_mm": [39.5, 38.5, 37.9],
            }
        ).set_index("tag_number")
    )
    predictions = pl.predict(new_penguins["culmen_length_mm"]).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_body_mass_g"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


def test_pipeline_logistic_regression_fit_score_predict(
    session, penguins_df_default_index
):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("logreg", linear_model.LogisticRegression()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["sex"]]
    pl.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    score_result = pl.score(X_train, y_train).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=utils.ML_CLASSFICATION_METRICS, index=1
    )

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Chinstrap penguin (Pygoscelis antarctica)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
            }
        ).set_index("tag_number")
    )
    predictions = pl.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_sex"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


@pytest.mark.flaky(retries=2)
def test_pipeline_xgbregressor_fit_score_predict(session, penguins_df_default_index):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("xgbreg", ensemble.XGBRegressor()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    score_result = pl.score(X_train, y_train).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Chinstrap penguin (Pygoscelis antarctica)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
                "sex": ["MALE", "FEMALE", "FEMALE"],
            }
        ).set_index("tag_number")
    )
    predictions = pl.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_body_mass_g"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


@pytest.mark.flaky(retries=2)
def test_pipeline_random_forest_classifier_fit_score_predict(
    session, penguins_df_default_index
):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("rfcls", ensemble.RandomForestClassifier()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["sex"]]
    pl.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    score_result = pl.score(X_train, y_train).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=utils.ML_CLASSFICATION_METRICS, index=1
    )

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Chinstrap penguin (Pygoscelis antarctica)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
            }
        ).set_index("tag_number")
    )
    predictions = pl.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_sex"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


def test_pipeline_PCA_fit_score_predict(session, penguins_df_default_index):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("pca", decomposition.PCA()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    pl.fit(X_train)

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Chinstrap penguin (Pygoscelis antarctica)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
                "sex": ["MALE", "FEMALE", "FEMALE"],
            }
        ).set_index("tag_number")
    )

    # Check score to ensure the model was fitted
    score_result = pl.score(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result, columns=["total_explained_variance_ratio"], index=1
    )

    predictions = pl.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=[
            "principal_component_1",
            "principal_component_2",
            "principal_component_3",
        ],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


@pytest.mark.flaky(retries=2)
def test_pipeline_standard_scaler_kmeans_fit_score_predict(
    session, penguins_pandas_df_default_index
):
    """Test an unsupervised model with a non-BQML implementation of StandardScaler"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("kmeans", cluster.KMeans(n_clusters=2)),
        ]
    )

    # kmeans is sensitive to the order with this configuration, so use ordered source data
    df = session.read_pandas(penguins_pandas_df_default_index).dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    pl.fit(X_train)

    # predict new labels
    pd_new_penguins = pd.DataFrame.from_dict(
        {
            "test1": {
                "species": "Adelie Penguin (Pygoscelis adeliae)",
                "island": "Dream",
                "culmen_length_mm": 27.5,
                "culmen_depth_mm": 8.5,
                "flipper_length_mm": 99,
                "body_mass_g": 4475,
                "sex": "MALE",
            },
            "test2": {
                "species": "Chinstrap penguin (Pygoscelis antarctica)",
                "island": "Dream",
                "culmen_length_mm": 55.8,
                "culmen_depth_mm": 29.8,
                "flipper_length_mm": 307,
                "body_mass_g": 4000,
                "sex": "MALE",
            },
            "test3": {
                "species": "Adelie Penguin (Pygoscelis adeliae)",
                "island": "Biscoe",
                "culmen_length_mm": 19.7,
                "culmen_depth_mm": 8.9,
                "flipper_length_mm": 84,
                "body_mass_g": 3550,
                "sex": "MALE",
            },
            "test4": {
                "species": "Gentoo penguin (Pygoscelis papua)",
                "island": "Biscoe",
                "culmen_length_mm": 63.8,
                "culmen_depth_mm": 33.9,
                "flipper_length_mm": 298,
                "body_mass_g": 4300,
                "sex": "FEMALE",
            },
            "test5": {
                "species": "Adelie Penguin (Pygoscelis adeliae)",
                "island": "Dream",
                "culmen_length_mm": 27.5,
                "culmen_depth_mm": 8.5,
                "flipper_length_mm": 99,
                "body_mass_g": 4475,
                "sex": "MALE",
            },
            "test6": {
                "species": "Chinstrap penguin (Pygoscelis antarctica)",
                "island": "Dream",
                "culmen_length_mm": 55.8,
                "culmen_depth_mm": 29.8,
                "flipper_length_mm": 307,
                "body_mass_g": 4000,
                "sex": "MALE",
            },
        },
        orient="index",
    )
    pd_new_penguins.index.name = "observation"

    new_penguins = session.read_pandas(pd_new_penguins)

    # Check score to ensure the model was fitted
    score_result = pl.score(new_penguins).to_pandas()
    eval_metrics = ["davies_bouldin_index", "mean_squared_distance"]
    utils.check_pandas_df_schema_and_index(score_result, columns=eval_metrics, index=1)

    predictions = pl.predict(new_penguins).to_pandas().sort_index()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["CENTROID_ID"],
        index=["test1", "test2", "test3", "test4", "test5", "test6"],
        col_exact=False,
    )


def test_pipeline_columntransformer_fit_predict(session, penguins_df_default_index):
    """Test a preprocessing step that manages heterogeneous data with ColumnTransformer"""
    pl = pipeline.Pipeline(
        [
            (
                "preproc",
                compose.ColumnTransformer(
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
                            "max_abs_scale",
                            preprocessing.MaxAbsScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "min_max_scale",
                            preprocessing.MinMaxScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "k_bins_discretizer",
                            preprocessing.KBinsDiscretizer(strategy="uniform"),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "simple_imputer",
                            impute.SimpleImputer(strategy="mean"),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "label",
                            preprocessing.LabelEncoder(),
                            "species",
                        ),
                        (
                            "poly_feats",
                            preprocessing.PolynomialFeatures(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                    ]
                ),
            ),
            ("linreg", linear_model.LinearRegression()),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[["species", "culmen_length_mm", "flipper_length_mm"]]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    # predict new labels
    new_penguins = session.read_pandas(
        pd.DataFrame(
            {
                "tag_number": [1633, 1672, 1690],
                "species": [
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Adelie Penguin (Pygoscelis adeliae)",
                    "Chinstrap penguin (Pygoscelis antarctica)",
                ],
                "island": ["Torgersen", "Torgersen", "Dream"],
                "culmen_length_mm": [39.5, 38.5, 37.9],
                "culmen_depth_mm": [18.8, 17.2, 18.1],
                "flipper_length_mm": [196.0, 181.0, 188.0],
                "sex": ["MALE", "FEMALE", "FEMALE"],
            }
        ).set_index("tag_number")
    )
    predictions = pl.predict(new_penguins).to_pandas()
    utils.check_pandas_df_schema_and_index(
        predictions,
        columns=["predicted_body_mass_g"],
        index=[1633, 1672, 1690],
        col_exact=False,
    )


def test_pipeline_columntransformer_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            (
                "transform",
                compose.ColumnTransformer(
                    [
                        (
                            "one_hot_encoder",
                            preprocessing.OneHotEncoder(
                                drop="most_frequent",
                                min_frequency=5,
                                max_categories=100,
                            ),
                            "species",
                        ),
                        (
                            "standard_scaler",
                            preprocessing.StandardScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "max_abs_scale",
                            preprocessing.MaxAbsScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "min_max_scale",
                            preprocessing.MinMaxScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "k_bins_discretizer",
                            preprocessing.KBinsDiscretizer(strategy="uniform"),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "simple_imputer",
                            impute.SimpleImputer(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "polynomial_features",
                            preprocessing.PolynomialFeatures(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                        (
                            "label",
                            preprocessing.LabelEncoder(),
                            "species",
                        ),
                    ]
                ),
            ),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[["species", "culmen_length_mm", "flipper_length_mm"]]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_col_transformer", replace=True
    )

    assert isinstance(pl_loaded._transform, compose.ColumnTransformer)
    transformers = pl_loaded._transform.transformers
    expected = [
        (
            "one_hot_encoder",
            preprocessing.OneHotEncoder(
                drop="most_frequent", max_categories=100, min_frequency=5
            ),
            "species",
        ),
        (
            "label_encoder",
            preprocessing.LabelEncoder(max_categories=1000001, min_frequency=0),
            "species",
        ),
        ("standard_scaler", preprocessing.StandardScaler(), "culmen_length_mm"),
        ("max_abs_scaler", preprocessing.MaxAbsScaler(), "culmen_length_mm"),
        ("min_max_scaler", preprocessing.MinMaxScaler(), "culmen_length_mm"),
        (
            "k_bins_discretizer",
            preprocessing.KBinsDiscretizer(strategy="uniform"),
            "culmen_length_mm",
        ),
        (
            "simple_imputer",
            impute.SimpleImputer(),
            "culmen_length_mm",
        ),
        ("standard_scaler", preprocessing.StandardScaler(), "flipper_length_mm"),
        ("max_abs_scaler", preprocessing.MaxAbsScaler(), "flipper_length_mm"),
        ("min_max_scaler", preprocessing.MinMaxScaler(), "flipper_length_mm"),
        (
            "k_bins_discretizer",
            preprocessing.KBinsDiscretizer(strategy="uniform"),
            "flipper_length_mm",
        ),
        (
            "simple_imputer",
            impute.SimpleImputer(),
            "flipper_length_mm",
        ),
        (
            "polynomial_features",
            preprocessing.PolynomialFeatures(),
            ("culmen_length_mm", "flipper_length_mm"),
        ),
    ]

    assert set(transformers) == set(expected)

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_standard_scaler_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            ("transform", preprocessing.StandardScaler()),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_standard_scaler", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.StandardScaler)

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_max_abs_scaler_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            ("transform", preprocessing.MaxAbsScaler()),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_min_max_scaler", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.MaxAbsScaler)

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_min_max_scaler_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            ("transform", preprocessing.MinMaxScaler()),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_min_max_scaler", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.MinMaxScaler)

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_k_bins_discretizer_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            ("transform", preprocessing.KBinsDiscretizer(strategy="uniform")),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_k_bins_discretizer", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.KBinsDiscretizer)

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_one_hot_encoder_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            (
                "transform",
                preprocessing.OneHotEncoder(
                    drop="most_frequent", min_frequency=5, max_categories=100
                ),
            ),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "sex",
            "species",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_one_hot_encoder", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.OneHotEncoder)

    one_hot_encoder = pl_loaded._transform
    assert one_hot_encoder.drop == "most_frequent"
    assert one_hot_encoder.min_frequency == 5
    assert one_hot_encoder.max_categories == 100

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_label_encoder_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            (
                "transform",
                preprocessing.LabelEncoder(min_frequency=5, max_categories=100),
            ),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "sex",
            "species",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_label_encoder", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.LabelEncoder)

    label_encoder = pl_loaded._transform
    assert label_encoder.min_frequency == 5
    assert label_encoder.max_categories == 100

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_simple_imputer_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            (
                "transform",
                impute.SimpleImputer(strategy="most_frequent"),
            ),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "sex",
            "species",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_simple_imputer", replace=True
    )
    assert isinstance(pl_loaded._transform, impute.SimpleImputer)

    simple_imputer = pl_loaded._transform
    assert simple_imputer.strategy == "most_frequent"

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False


def test_pipeline_poly_features_to_gbq(penguins_df_default_index, dataset_id):
    pl = pipeline.Pipeline(
        [
            (
                "transform",
                preprocessing.PolynomialFeatures(degree=3),
            ),
            ("estimator", linear_model.LinearRegression(fit_intercept=False)),
        ]
    )

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "culmen_length_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["body_mass_g"]]
    pl.fit(X_train, y_train)

    pl_loaded = pl.to_gbq(
        f"{dataset_id}.test_penguins_pipeline_poly_features", replace=True
    )
    assert isinstance(pl_loaded._transform, preprocessing.PolynomialFeatures)

    poly_features = pl_loaded._transform
    assert poly_features.degree == 3

    assert isinstance(pl_loaded._estimator, linear_model.LinearRegression)
    assert pl_loaded._estimator.fit_intercept is False
