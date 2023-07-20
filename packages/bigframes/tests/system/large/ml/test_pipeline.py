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

from bigframes.ml import (
    cluster,
    compose,
    decomposition,
    ensemble,
    linear_model,
    pipeline,
    preprocessing,
)
from tests.system.utils import assert_pandas_df_equal_ignore_ordering


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
    train_X = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    train_y = df[["body_mass_g"]]
    pl.fit(train_X, train_y)

    # Check score to ensure the model was fitted
    score_result = pl.score(train_X, train_y).compute()
    score_expected = pd.DataFrame(
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
    score_expected = score_expected.reindex(index=score_expected.index.astype("Int64"))

    pd.testing.assert_frame_equal(
        score_result, score_expected, check_exact=False, rtol=0.1
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
    expected = pd.DataFrame(
        {"predicted_body_mass_g": [3968.8, 3176.3, 3545.2]},
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]], expected, check_exact=False, rtol=0.1
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
    train_X = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    train_y = df[["sex"]]
    pl.fit(train_X, train_y)

    # Check score to ensure the model was fitted
    score_result = pl.score(train_X, train_y).compute()
    score_expected = pd.DataFrame(
        {
            "precision": [0.537091],
            "recall": [0.538636],
            "accuracy": [0.805389],
            "f1_score": [0.537716],
            "log_loss": [1.445433],
            "roc_auc": [0.917818],
        },
        dtype="Float64",
    )
    score_expected = score_expected.reindex(index=score_expected.index.astype("Int64"))

    pd.testing.assert_frame_equal(
        score_result, score_expected, check_exact=False, rtol=0.1
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
    expected = pd.DataFrame(
        {"predicted_sex": ["MALE", "FEMALE", "FEMALE"]},
        dtype=pd.StringDtype(storage="pyarrow"),
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_sex"]],
        expected,
    )


def test_pipeline_xgbregressor_fit_score_predict(session, penguins_df_default_index):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("xgbreg", ensemble.XGBRegressor()),
        ]
    )

    df = penguins_df_default_index.dropna()
    train_X = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    train_y = df[["body_mass_g"]]
    pl.fit(train_X, train_y)

    # Check score to ensure the model was fitted
    score_result = pl.score(train_X, train_y).compute()
    score_expected = pd.DataFrame(
        {
            "mean_absolute_error": [203.4001727989334],
            "mean_squared_error": [74898.80551717622],
            "mean_squared_log_error": [0.004394266810531861],
            "median_absolute_error": [152.01806640625],
            "r2_score": [0.8840255831308607],
            "explained_variance": [0.8858505311591299],
        },
        dtype="Float64",
    )
    score_expected = score_expected.reindex(index=score_expected.index.astype("Int64"))

    pd.testing.assert_frame_equal(
        score_result, score_expected, check_exact=False, rtol=0.1
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
    expected = pd.DataFrame(
        {
            "predicted_body_mass_g": [
                4287.34521484375,
                3198.351806640625,
                3385.34130859375,
            ]
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]], expected, check_exact=False, rtol=0.1
    )


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
    train_X = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    train_y = df[["sex"]]
    pl.fit(train_X, train_y)

    # Check score to ensure the model was fitted
    score_result = pl.score(train_X, train_y).compute()
    score_expected = pd.DataFrame(
        {
            "precision": [0.587673],
            "recall": [0.588781],
            "accuracy": [0.88024],
            "f1_score": [0.587644],
            "log_loss": [0.859459],
            "roc_auc": [0.971737],
        },
        dtype="Float64",
    )
    score_expected = score_expected.reindex(index=score_expected.index.astype("Int64"))

    pd.testing.assert_frame_equal(
        score_result, score_expected, check_exact=False, rtol=0.1
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
    expected = pd.DataFrame(
        {"predicted_sex": ["MALE", "FEMALE", "FEMALE"]},
        dtype=pd.StringDtype(storage="pyarrow"),
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_sex"]],
        expected,
    )


def test_pipeline_PCA_fit_predict(session, penguins_df_default_index):
    """Test a supervised model with a minimal preprocessing step"""
    pl = pipeline.Pipeline(
        [
            ("scale", preprocessing.StandardScaler()),
            ("pca", decomposition.PCA()),
        ]
    )

    df = penguins_df_default_index.dropna()
    train_X = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    pl.fit(train_X)

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
    expected = pd.DataFrame(
        {
            "principal_component_1": [-1.115259, -1.506141, -1.471174],
            "principal_component_2": [-0.074824, 0.69664, 0.406104],
            "principal_component_3": [0.500012, -0.544479, 0.075849],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[
            ["principal_component_1", "principal_component_2", "principal_component_3"]
        ],
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_pipeline_standard_scaler_kmeans_fit_predict(
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
    train_X = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    pl.fit(train_X)

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
    result = pl.predict(new_penguins).to_pandas().sort_index()
    expected = pd.DataFrame(
        {"CENTROID_ID": [1, 2, 1, 2, 1, 2]},
        dtype="Int64",
        index=pd.Index(
            ["test1", "test2", "test3", "test4", "test5", "test6"],
            dtype="string[pyarrow]",
        ),
    )
    expected.index.name = "observation"
    assert_pandas_df_equal_ignore_ordering(result, expected)


def test_pipeline_columntransformer_fit_predict(session, penguins_df_default_index):
    """Test a preprocessing step that manages heterogenous data with ColumnTransformer"""
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
                            "scale",
                            preprocessing.StandardScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                    ]
                ),
            ),
            ("linreg", linear_model.LinearRegression()),
        ]
    )

    df = penguins_df_default_index.dropna()
    train_X = df[["species", "culmen_length_mm", "flipper_length_mm"]]
    train_y = df[["body_mass_g"]]
    pl.fit(train_X, train_y)

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
    expected = pd.DataFrame(
        {"predicted_body_mass_g": [3909.2, 3436.0, 2860.0]},
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]], expected, check_exact=False, rtol=0.1
    )
