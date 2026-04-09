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

import pandas as pd
import pytest

import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_compile_fromrange(compiler_session, snapshot):
    data = {
        "timestamp_col": pd.date_range(
            start="2021-01-01 13:00:00", periods=30, freq="1s"
        ),
        "int64_col": range(30),
        "int64_too": range(10, 40),
    }
    df = bpd.DataFrame(data, session=compiler_session).set_index("timestamp_col")
    sql, _, _ = df.resample(rule="7s")._block.to_sql_query(
        include_index=True, enable_cache=False
    )
    snapshot.assert_match(sql, "out.sql")
