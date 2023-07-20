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

import bigframes.ml.compose
import bigframes.ml.linear_model
import bigframes.ml.pipeline
import bigframes.ml.preprocessing


def test_pipeline_repr():
    pipeline = bigframes.ml.pipeline.Pipeline(
        [
            (
                "preproc",
                bigframes.ml.compose.ColumnTransformer(
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
                ),
            ),
            ("linreg", bigframes.ml.linear_model.LinearRegression()),
        ]
    )

    assert (
        pipeline.__repr__()
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
    bf_pipeline = bigframes.ml.pipeline.Pipeline(
        [
            (
                "preproc",
                bigframes.ml.compose.ColumnTransformer(
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
                ),
            ),
            ("linreg", bigframes.ml.linear_model.LinearRegression()),
        ]
    )
    sk_pipeline = sklearn_pipeline.Pipeline(
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

    assert bf_pipeline.__repr__() == sk_pipeline.__repr__()
