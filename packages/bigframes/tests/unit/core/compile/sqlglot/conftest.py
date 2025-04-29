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


@pytest.fixture(scope="module")
def compiler_session():
    from . import compiler_session

    return compiler_session.SQLCompilerSession()


@pytest.fixture(scope="module")
def all_types_df() -> pd.DataFrame:
    # TODO: all types pandas dataframes
    # TODO: add tests for empty dataframes
    df = pd.DataFrame(
        {
            "int1": pd.Series([1, 2, 3], dtype="Int64"),
            "int2": pd.Series([-10, 20, 30], dtype="Int64"),
            "bools": pd.Series([True, None, False], dtype="boolean"),
            "strings": pd.Series(["b", "aa", "ccc"], dtype="string[pyarrow]"),
        },
    )
    # add more complexity index.
    df.index = df.index.astype("Int64")
    return df
