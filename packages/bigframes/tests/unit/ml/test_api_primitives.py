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

import bigframes.ml.decomposition
import bigframes.ml.linear_model


def test_base_estimator_repr():
    estimator = bigframes.ml.linear_model.LinearRegression()
    assert estimator.__repr__() == "LinearRegression()"

    estimator = bigframes.ml.linear_model.LinearRegression(fit_intercept=False)
    assert estimator.__repr__() == "LinearRegression(fit_intercept=False)"

    estimator = bigframes.ml.linear_model.LinearRegression(fit_intercept=True)
    assert estimator.__repr__() == "LinearRegression()"

    # TODO(b/340891292): fix type error
    pca_estimator = bigframes.ml.decomposition.PCA(n_components=7)
    assert pca_estimator.__repr__() == "PCA(n_components=7)"


def test_base_estimator_repr_matches_sklearn():
    sklearn_decomposition = pytest.importorskip("sklearn.decomposition")
    sklearn_linear_model = pytest.importorskip("sklearn.linear_model")
    estimator = bigframes.ml.linear_model.LinearRegression()
    sklearn_estimator = sklearn_linear_model.LinearRegression()
    assert estimator.__repr__() == sklearn_estimator.__repr__()

    estimator = bigframes.ml.linear_model.LinearRegression(fit_intercept=False)
    sklearn_estimator = sklearn_linear_model.LinearRegression(fit_intercept=False)
    assert estimator.__repr__() == sklearn_estimator.__repr__()

    estimator = bigframes.ml.linear_model.LinearRegression(fit_intercept=True)
    sklearn_estimator = sklearn_linear_model.LinearRegression(fit_intercept=True)
    assert estimator.__repr__() == sklearn_estimator.__repr__()

    # TODO(b/340891292): fix type error
    pca_estimator = bigframes.ml.decomposition.PCA(n_components=7)
    sklearn_estimator = sklearn_decomposition.PCA(n_components=7)
    assert pca_estimator.__repr__() == sklearn_estimator.__repr__()
