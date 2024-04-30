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

import numpy as np
import pandas as pd

import bigframes.bigquery as bbq
import bigframes.pandas as bpd


def test_array_length():
    series = bpd.Series([["A", "AA", "AAA"], ["BB", "B"], np.nan, [], ["C"]])
    # TODO(b/336880368): Allow for NULL values to be input for ARRAY columns.
    # Once we actually store NULL values, this will be NULL where the input is NULL.
    expected = pd.Series([3, 2, 0, 0, 1])
    pd.testing.assert_series_equal(
        bbq.array_length(series).to_pandas(),
        expected,
        check_dtype=False,
        check_index_type=False,
    )
