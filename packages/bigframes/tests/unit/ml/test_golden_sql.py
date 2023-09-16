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

from unittest import mock

import pytest_mock

import bigframes
from bigframes.ml import linear_model
import bigframes.pandas as bpd


def test_linear_regression_default_fit(mocker: pytest_mock.MockerFixture):
    mock_session = mock.create_autospec(spec=bigframes.Session)

    mock_X = mock.create_autospec(spec=bpd.DataFrame)
    mock_X._get_block().expr._session = mock_session

    mock_y = mock.create_autospec(spec=bpd.DataFrame)
    mock_y.columns.tolist.return_value = ["input_label_column"]

    mock_X.join(mock_y).sql = "input_dataframe_sql"

    # return values we don't care about, but need to provide to continue the program
    mock_session._start_query.return_value = (None, mock.MagicMock())

    mocker.patch(
        "bigframes.ml.core._create_temp_model_name", return_value="temp_model_name"
    )

    model = linear_model.LinearRegression()
    model.fit(mock_X, mock_y)

    mock_session._start_query.assert_called_once_with(
        'CREATE TEMP MODEL `temp_model_name`\nOPTIONS(\n  model_type="LINEAR_REG",\n  data_split_method="NO_SPLIT",\n  fit_intercept=True,\n  INPUT_LABEL_COLS=["input_label_column"])\nAS input_dataframe_sql'
    )
