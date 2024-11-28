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

import pandas as pd
import pandas.testing
import pytest

import bigframes.ml.utils as utils

_DATA_FRAME = pd.DataFrame({"column": [1, 2, 3]})
_SERIES = pd.Series([1, 2, 3], name="column")


@pytest.mark.parametrize(
    "data",
    [pytest.param(_DATA_FRAME, id="dataframe"), pytest.param(_SERIES, id="series")],
)
def test_convert_to_dataframe(session, data):
    bf_data = session.read_pandas(data)

    (actual_result,) = utils.batch_convert_to_dataframe(bf_data)

    pandas.testing.assert_frame_equal(
        actual_result.to_pandas(),
        _DATA_FRAME,
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize(
    "data",
    [pytest.param(_DATA_FRAME, id="dataframe"), pytest.param(_SERIES, id="series")],
)
def test_convert_pandas_to_dataframe(data, session):
    (actual_result,) = utils.batch_convert_to_dataframe(data, session=session)

    pandas.testing.assert_frame_equal(
        actual_result.to_pandas(),
        _DATA_FRAME,
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize(
    "data",
    [pytest.param(_DATA_FRAME, id="dataframe"), pytest.param(_SERIES, id="series")],
)
def test_convert_to_series(session, data):
    bf_data = session.read_pandas(data)

    (actual_result,) = utils.batch_convert_to_series(bf_data)

    pandas.testing.assert_series_equal(
        actual_result.to_pandas(), _SERIES, check_index_type=False, check_dtype=False
    )


@pytest.mark.parametrize(
    "data",
    [pytest.param(_DATA_FRAME, id="dataframe"), pytest.param(_SERIES, id="series")],
)
def test_convert_pandas_to_series(data, session):
    (actual_result,) = utils.batch_convert_to_series(data, session=session)

    pandas.testing.assert_series_equal(
        actual_result.to_pandas(), _SERIES, check_index_type=False, check_dtype=False
    )
