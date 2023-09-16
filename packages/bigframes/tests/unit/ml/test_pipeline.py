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

import pytest
import sklearn.compose as sklearn_compose  # type: ignore
import sklearn.linear_model as sklearn_linear_model  # type: ignore
import sklearn.pipeline as sklearn_pipeline  # type: ignore
import sklearn.preprocessing as sklearn_preprocessing  # type: ignore

from bigframes.ml import compose, forecasting, linear_model, pipeline, preprocessing


def test_pipeline_repr():
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

    assert (
        pl.__repr__()
        == """Pipeline(steps=[('preproc',
                 ColumnTransformer(transformers=[('onehot', OneHotEncoder(),
                                                  'species'),
                                                 ('scale', StandardScaler(),
                                                  ['culmen_length_mm',
                                                   'flipper_length_mm'])])),
                ('linreg', LinearRegression())])"""
    )


@pytest.mark.skipif(sklearn_pipeline is None, reason="requires sklearn")
def test_pipeline_repr_matches_sklearn():
    bf_pl = pipeline.Pipeline(
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
    sk_pl = sklearn_pipeline.Pipeline(
        [
            (
                "preproc",
                sklearn_compose.ColumnTransformer(
                    [
                        (
                            "onehot",
                            sklearn_preprocessing.OneHotEncoder(),
                            "species",
                        ),
                        (
                            "scale",
                            sklearn_preprocessing.StandardScaler(),
                            ["culmen_length_mm", "flipper_length_mm"],
                        ),
                    ]
                ),
            ),
            ("linreg", sklearn_linear_model.LinearRegression()),
        ]
    )

    assert bf_pl.__repr__() == sk_pl.__repr__()


def test_pipeline_arima_plus_not_implemented():
    with pytest.raises(NotImplementedError):
        pipeline.Pipeline(
            [
                (
                    "transform",
                    preprocessing.StandardScaler(),
                ),
                ("estimator", forecasting.ARIMAPlus()),
            ]
        )
