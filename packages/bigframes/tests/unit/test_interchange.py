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

import pathlib
from typing import Generator

import pandas as pd
import pandas.api.interchange as pd_interchange
import pandas.testing
import pytest

import bigframes
import bigframes.pandas as bpd
from bigframes.testing.utils import convert_pandas_dtypes

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="2.0.0")

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"


@pytest.fixture(scope="module", autouse=True)
def session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session
    from bigframes.testing import polars_session

    session = polars_session.TestSession()
    with bigframes.core.global_session._GlobalSessionContext(session):
        yield session


@pytest.fixture(scope="module")
def scalars_pandas_df_index() -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""

    df = pd.read_json(
        DATA_DIR / "scalars.jsonl",
        lines=True,
    )
    convert_pandas_dtypes(df, bytes_col=True)

    df = df.set_index("rowindex", drop=False)
    df.index.name = None
    return df.set_index("rowindex").sort_index()


def test_interchange_df_logical_properties(session):
    df = bpd.DataFrame({"a": [1, 2, 3], 2: [4, 5, 6]}, session=session)
    interchange_df = df.__dataframe__()
    assert interchange_df.num_columns() == 2
    assert interchange_df.num_rows() == 3
    assert interchange_df.column_names() == ["a", "2"]


def test_interchange_column_logical_properties(session):
    df = bpd.DataFrame(
        {
            "nums": [1, 2, 3, None, None],
            "animals": ["cat", "dog", "mouse", "horse", "turtle"],
        },
        session=session,
    )
    interchange_df = df.__dataframe__()

    assert interchange_df.get_column_by_name("nums").size() == 5
    assert interchange_df.get_column(0).null_count == 2

    assert interchange_df.get_column_by_name("animals").size() == 5
    assert interchange_df.get_column(1).null_count == 0


def test_interchange_to_pandas(session, scalars_pandas_df_index):
    # A few limitations:
    # 1) Limited datatype support
    # 2) Pandas converts null to NaN/False, rather than use nullable or pyarrow types
    # 3) Indices aren't preserved by interchange format
    unsupported_cols = [
        "bytes_col",
        "date_col",
        "numeric_col",
        "time_col",
        "duration_col",
        "geography_col",
    ]
    scalars_pandas_df_index = scalars_pandas_df_index.drop(columns=unsupported_cols)
    scalars_pandas_df_index = scalars_pandas_df_index.bfill().ffill()
    bf_df = session.read_pandas(scalars_pandas_df_index)

    from_ix = pd_interchange.from_dataframe(bf_df)

    # interchange format does not include index, so just reset both indices before comparison
    pandas.testing.assert_frame_equal(
        scalars_pandas_df_index.reset_index(drop=True),
        from_ix.reset_index(drop=True),
        check_dtype=False,
    )
