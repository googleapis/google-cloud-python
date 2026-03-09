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


from pandas import testing
import pandas as pd
import pytest

from bigframes import dataframe
from bigframes.core import convert


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        pytest.param(pd.Series([1, 2, 3], name="test"), True, id="pd.Series"),
        pytest.param(pd.Index([1, 2, 3], name="test"), True, id="pd.Index"),
        pytest.param(pd.DataFrame({"test": [1, 2, 3]}), True, id="pd.DataFrame"),
        pytest.param("something", False, id="string"),
    ],
)
def test_can_convert_to_dataframe(input, expected):
    assert convert.can_convert_to_dataframe(input) is expected


@pytest.mark.parametrize(
    "input",
    [
        pytest.param(pd.Series([1, 2, 3], name="test"), id="pd.Series"),
        pytest.param(pd.Index([1, 2, 3], name="test"), id="pd.Index"),
        pytest.param(pd.DataFrame({"test": [1, 2, 3]}), id="pd.DataFrame"),
    ],
)
def test_to_bf_dataframe(input, session):
    result = convert.to_bf_dataframe(input, None, session)

    testing.assert_frame_equal(
        result.to_pandas(),
        pd.DataFrame({"test": [1, 2, 3]}),
        check_dtype=False,
        check_index_type=False,
    )


def test_to_bf_dataframe_with_bf_dataframe(session):
    bf = dataframe.DataFrame({"test": [1, 2, 3]}, session=session)

    testing.assert_frame_equal(
        convert.to_bf_dataframe(bf, None, session).to_pandas(),
        bf.to_pandas(),
    )
