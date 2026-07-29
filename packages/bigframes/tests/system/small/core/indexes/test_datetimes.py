# Copyright 2025 Google LLC
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
import pandas.testing
import pytest


@pytest.fixture(scope="module")
def datetime_indexes(session):
    pd_index = pandas.date_range("2024-12-25", periods=10, freq="d")
    bf_index = session.read_pandas(pd_index)

    return bf_index, pd_index


@pytest.mark.parametrize(
    "access",
    [
        pytest.param(lambda x: x.year, id="year"),
        pytest.param(lambda x: x.month, id="month"),
        pytest.param(lambda x: x.day, id="day"),
        pytest.param(lambda x: x.dayofweek, id="dayofweek"),
        pytest.param(lambda x: x.day_of_week, id="day_of_week"),
        pytest.param(lambda x: x.weekday, id="weekday"),
    ],
)
def test_datetime_index_properties(datetime_indexes, access):
    bf_index, pd_index = datetime_indexes

    actual_result = access(bf_index).to_pandas()

    expected_result = access(pd_index).astype(pandas.Int64Dtype())
    pandas.testing.assert_index_equal(actual_result, expected_result)
