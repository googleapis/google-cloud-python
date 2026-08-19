# Copyright 2024 Google LLC
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

from bigframes.ml import linear_model, model_selection
from bigframes.testing import utils


@pytest.mark.parametrize(
    ("cv", "n_fold"),
    (
        pytest.param(
            None,
            5,
        ),
        pytest.param(
            4,
            4,
        ),
        pytest.param(
            model_selection.KFold(3),
            3,
        ),
    ),
)
def test_cross_validate(penguins_df_default_index, cv, n_fold):
    model = linear_model.LinearRegression()
    df = penguins_df_default_index.dropna()
    X = df[
        [
            "species",
            "island",
            "culmen_length_mm",
        ]
    ]
    y = df["body_mass_g"]

    cv_results = model_selection.cross_validate(model, X, y, cv=cv)

    assert "test_score" in cv_results
    assert "fit_time" in cv_results
    assert "score_time" in cv_results

    assert len(cv_results["test_score"]) == n_fold
    assert len(cv_results["fit_time"]) == n_fold
    assert len(cv_results["score_time"]) == n_fold

    utils.check_pandas_df_schema_and_index(
        cv_results["test_score"][0].to_pandas(),
        columns=utils.ML_REGRESSION_METRICS,
        index=1,
    )
