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

import json

import pandas as pd
import pandas.testing
import pytest

import bigframes.functions.remote_function_template as remote_function_template


@pytest.mark.parametrize(
    ["row_json", "expected"],
    (
        pytest.param(
            json.dumps(
                {
                    "names": ["'my-index'", "'col1'", "'col2'", "'col3'"],
                    "types": ["string", "Int64", "Int64", "Int64"],
                    "values": ["my-index-value", "1", None, "-1"],
                    "indexlength": 1,
                    "dtype": "Int64",
                }
            ),
            pd.Series(
                [1, pd.NA, -1],
                dtype="Int64",
                index=["col1", "col2", "col3"],
                name="my-index-value",
            ),
            id="int64-string-index",
        ),
        # TODO: test more types and indexes
    ),
)
def test_get_pd_series(row_json, expected):
    got = remote_function_template.get_pd_series(row_json)
    pandas.testing.assert_series_equal(got, expected)
