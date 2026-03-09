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

from __future__ import annotations

import pathlib
from typing import Generator, TYPE_CHECKING

import pandas as pd
import pandas.testing
import pyarrow as pa  # type: ignore
import pytest

import bigframes

if TYPE_CHECKING:
    from bigframes.testing import polars_session

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="2.2.0")

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"


@pytest.fixture(scope="module", autouse=True)
def session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session
    from bigframes.testing import polars_session

    session = polars_session.TestSession()
    with bigframes.core.global_session._GlobalSessionContext(session):
        yield session


@pytest.fixture
def struct_df(session: polars_session.TestSession):
    pa_type = pa.struct(
        [
            ("str_field", pa.string()),
            ("int_field", pa.int64()),
        ]
    )
    return session.DataFrame(
        {
            "struct_col": pd.Series(
                pa.array(
                    [
                        {
                            "str_field": "my string",
                            "int_field": 1,
                        },
                        {
                            "str_field": None,
                            "int_field": 2,
                        },
                        {
                            "str_field": "another string",
                            "int_field": None,
                        },
                        {
                            "str_field": "some string",
                            "int_field": 3,
                        },
                    ],
                    pa_type,
                ),
                dtype=pd.ArrowDtype(pa_type),
            ),
        }
    )


@pytest.fixture
def struct_series(struct_df):
    return struct_df["struct_col"]


def test_struct_dtypes(struct_series):
    bf_series = struct_series
    pd_series = struct_series.to_pandas()
    assert isinstance(pd_series.dtype, pd.ArrowDtype)

    bf_result = bf_series.struct.dtypes
    pd_result = pd_series.struct.dtypes

    pandas.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("field_name", "common_dtype"),
    (
        ("str_field", "string[pyarrow]"),
        ("int_field", "int64[pyarrow]"),
        # TODO(tswast): Support referencing fields by number, too.
    ),
)
def test_struct_field(struct_series, field_name, common_dtype):
    bf_series = struct_series
    pd_series = struct_series.to_pandas()
    assert isinstance(pd_series.dtype, pd.ArrowDtype)

    bf_result = bf_series.struct.field(field_name).to_pandas()
    pd_result = pd_series.struct.field(field_name)

    # TODO(tswast): if/when we support arrowdtype for int/string, we can remove
    # this cast.
    bf_result = bf_result.astype(common_dtype)
    pd_result = pd_result.astype(common_dtype)

    pandas.testing.assert_series_equal(bf_result, pd_result)


def test_struct_explode(struct_series):
    bf_series = struct_series
    pd_series = struct_series.to_pandas()
    assert isinstance(pd_series.dtype, pd.ArrowDtype)

    bf_result = bf_series.struct.explode().to_pandas()
    pd_result = pd_series.struct.explode()

    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
        # TODO(tswast): remove if/when we support arrowdtype for int/string.
        check_dtype=False,
    )
