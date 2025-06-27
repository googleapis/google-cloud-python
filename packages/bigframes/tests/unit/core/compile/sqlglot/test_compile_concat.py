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

import bigframes
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_compile_concat(
    scalar_types_pandas_df: pd.DataFrame, compiler_session: bigframes.Session, snapshot
):
    # TODO: concat two same dataframes, which SQL does not get reused.
    # TODO: concat dataframes from a gbq table but trigger a windows compiler.
    df1 = bpd.DataFrame(scalar_types_pandas_df, session=compiler_session)
    df1 = df1[["rowindex", "int64_col", "string_col"]]
    concat_df = bpd.concat([df1, df1])
    snapshot.assert_match(concat_df.sql, "out.sql")
