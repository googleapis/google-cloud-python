# Copyright 2023 Google LLC
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

import datetime
from typing import Dict, Union

import geopandas  # type: ignore
import numpy
import pandas
import pandas.arrays
import pandas.testing
import pyarrow  # type: ignore
import pytest

import bigframes.session._io.pandas


@pytest.mark.parametrize(
    ("arrow_table", "dtypes", "expected"),
    (
        pytest.param(
            pyarrow.Table.from_pydict({}),
            {},
            pandas.DataFrame(),
            id="empty-df",
        ),
        pytest.param(
            pyarrow.Table.from_pydict(
                {
                    "bool": pyarrow.array([None, None, None], type=pyarrow.bool_()),
                    "float": pyarrow.array([None, None, None], type=pyarrow.float64()),
                    "int": pyarrow.array([None, None, None], type=pyarrow.int64()),
                    "string": pyarrow.array([None, None, None], type=pyarrow.string()),
                    "time": pyarrow.array(
                        [None, None, None], type=pyarrow.time64("us")
                    ),
                }
            ),
            {
                "bool": "boolean",
                "float": pandas.Float64Dtype(),
                "int": pandas.Int64Dtype(),
                "string": "string[pyarrow]",
                "time": pandas.ArrowDtype(pyarrow.time64("us")),
            },
            pandas.DataFrame(
                {
                    "bool": pandas.Series([None, None, None], dtype="boolean"),
                    "float": pandas.Series(
                        pandas.arrays.FloatingArray(  # type: ignore
                            numpy.array(
                                [float("nan"), float("nan"), float("nan")],
                                dtype="float64",
                            ),
                            numpy.array([True, True, True], dtype="bool"),
                        ),
                        dtype=pandas.Float64Dtype(),
                    ),
                    "int": pandas.Series(
                        [None, None, None],
                        dtype=pandas.Int64Dtype(),
                    ),
                    "string": pandas.Series(
                        [None, None, None], dtype="string[pyarrow]"
                    ),
                    "time": pandas.Series(
                        [
                            None,
                            None,
                            None,
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.time64("us")),
                    ),
                }
            ),
            id="nulls-df",
        ),
        pytest.param(
            pyarrow.Table.from_pydict(
                {
                    "date": pyarrow.array(
                        [
                            datetime.date(2023, 8, 29),
                            None,
                            datetime.date(2024, 4, 9),
                            datetime.date(1, 1, 1),
                        ],
                        type=pyarrow.date32(),
                    ),
                    "datetime": pyarrow.array(
                        [
                            datetime.datetime(2023, 8, 29),
                            None,
                            datetime.datetime(2024, 4, 9, 23, 59, 59),
                            datetime.datetime(1, 1, 1, 0, 0, 0, 1),
                        ],
                        type=pyarrow.timestamp("us"),
                    ),
                    "string": ["123", None, "abc", "xyz"],
                    "time": pyarrow.array(
                        [
                            datetime.time(0, 0, 0, 1),
                            datetime.time(12, 0, 0),
                            None,
                            datetime.time(23, 59, 59, 999999),
                        ],
                        type=pyarrow.time64("us"),
                    ),
                    "timestamp": pyarrow.array(
                        [
                            datetime.datetime(2023, 8, 29),
                            datetime.datetime(1, 1, 1, 0, 0, 0, 1),
                            None,
                            datetime.datetime(2024, 4, 9, 23, 59, 59),
                        ],
                        type=pyarrow.timestamp("us", datetime.timezone.utc),
                    ),
                }
            ),
            {
                "date": pandas.ArrowDtype(pyarrow.date32()),
                "datetime": pandas.ArrowDtype(pyarrow.timestamp("us")),
                "string": "string[pyarrow]",
                "time": pandas.ArrowDtype(pyarrow.time64("us")),
                "timestamp": pandas.ArrowDtype(
                    pyarrow.timestamp("us", datetime.timezone.utc)
                ),
            },
            pandas.DataFrame(
                {
                    "date": pandas.Series(
                        [
                            datetime.date(2023, 8, 29),
                            None,
                            datetime.date(2024, 4, 9),
                            datetime.date(1, 1, 1),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.date32()),
                    ),
                    "datetime": pandas.Series(
                        [
                            datetime.datetime(2023, 8, 29),
                            None,
                            datetime.datetime(2024, 4, 9, 23, 59, 59),
                            datetime.datetime(1, 1, 1, 0, 0, 0, 1),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.timestamp("us")),
                    ),
                    "string": pandas.Series(
                        ["123", None, "abc", "xyz"], dtype="string[pyarrow]"
                    ),
                    "time": pandas.Series(
                        [
                            datetime.time(0, 0, 0, 1),
                            datetime.time(12, 0, 0),
                            None,
                            datetime.time(23, 59, 59, 999999),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.time64("us")),
                    ),
                    "timestamp": pandas.Series(
                        [
                            datetime.datetime(2023, 8, 29),
                            datetime.datetime(1, 1, 1, 0, 0, 0, 1),
                            None,
                            datetime.datetime(2024, 4, 9, 23, 59, 59),
                        ],
                        dtype=pandas.ArrowDtype(
                            pyarrow.timestamp("us", datetime.timezone.utc)
                        ),
                    ),
                }
            ),
            id="arrow-dtypes",
        ),
        pytest.param(
            pyarrow.Table.from_pydict(
                {
                    "bool": [True, None, True, False],
                    "bytes": [b"123", None, b"abc", b"xyz"],
                    "float": pyarrow.array(
                        [1.0, None, float("nan"), -1.0],
                        type=pyarrow.float64(),
                    ),
                    "int": pyarrow.array(
                        [1, None, -1, 2**63 - 1],
                        type=pyarrow.int64(),
                    ),
                    "string": ["123", None, "abc", "xyz"],
                }
            ),
            {
                "bool": "boolean",
                "bytes": "object",
                "float": pandas.Float64Dtype(),
                "int": pandas.Int64Dtype(),
                "string": "string[pyarrow]",
            },
            pandas.DataFrame(
                {
                    "bool": pandas.Series([True, None, True, False], dtype="boolean"),
                    "bytes": [b"123", None, b"abc", b"xyz"],
                    "float": pandas.Series(
                        pandas.arrays.FloatingArray(  # type: ignore
                            numpy.array(
                                [1.0, float("nan"), float("nan"), -1.0], dtype="float64"
                            ),
                            numpy.array([False, True, False, False], dtype="bool"),
                        ),
                        dtype=pandas.Float64Dtype(),
                    ),
                    "int": pandas.Series(
                        [1, None, -1, 2**63 - 1],
                        dtype=pandas.Int64Dtype(),
                    ),
                    "string": pandas.Series(
                        ["123", None, "abc", "xyz"], dtype="string[pyarrow]"
                    ),
                }
            ),
            id="scalar-dtypes",
        ),
        pytest.param(
            pyarrow.Table.from_pydict(
                {
                    "bool": pyarrow.chunked_array(
                        [[True, None], [True, False]],
                        type=pyarrow.bool_(),
                    ),
                    "bytes": pyarrow.chunked_array(
                        [[b"123", None], [b"abc", b"xyz"]],
                        type=pyarrow.binary(),
                    ),
                    "float": pyarrow.chunked_array(
                        [[1.0, None], [float("nan"), -1.0]],
                        type=pyarrow.float64(),
                    ),
                    "int": pyarrow.chunked_array(
                        [[1, None], [-1, 2**63 - 1]],
                        type=pyarrow.int64(),
                    ),
                    "string": pyarrow.chunked_array(
                        [["123", None], ["abc", "xyz"]],
                        type=pyarrow.string(),
                    ),
                }
            ),
            {
                "bool": "boolean",
                "bytes": "object",
                "float": pandas.Float64Dtype(),
                "int": pandas.Int64Dtype(),
                "string": "string[pyarrow]",
            },
            pandas.DataFrame(
                {
                    "bool": pandas.Series([True, None, True, False], dtype="boolean"),
                    "bytes": [b"123", None, b"abc", b"xyz"],
                    "float": pandas.Series(
                        pandas.arrays.FloatingArray(  # type: ignore
                            numpy.array(
                                [1.0, float("nan"), float("nan"), -1.0], dtype="float64"
                            ),
                            numpy.array([False, True, False, False], dtype="bool"),
                        ),
                        dtype=pandas.Float64Dtype(),
                    ),
                    "int": pandas.Series(
                        [1, None, -1, 2**63 - 1],
                        dtype=pandas.Int64Dtype(),
                    ),
                    "string": pandas.Series(
                        ["123", None, "abc", "xyz"], dtype="string[pyarrow]"
                    ),
                }
            ),
            id="scalar-dtypes-chunked_array",
        ),
        pytest.param(
            pyarrow.Table.from_pydict(
                {
                    "geocol": [
                        "POINT(32 210)",
                        None,
                        "LINESTRING(1 1, 2 1, 3.1 2.88, 3 -3)",
                    ]
                }
            ),
            {"geocol": geopandas.array.GeometryDtype()},
            pandas.DataFrame(
                {
                    "geocol": geopandas.GeoSeries.from_wkt(
                        ["POINT(32 210)", None, "LINESTRING(1 1, 2 1, 3.1 2.88, 3 -3)"],
                        crs="EPSG:4326",
                    ),
                }
            ),
            id="geography-dtype",
        ),
    ),
)
def test_arrow_to_pandas(
    arrow_table: Union[pyarrow.Table, pyarrow.RecordBatch],
    dtypes: Dict,
    expected: pandas.DataFrame,
):
    actual = bigframes.session._io.pandas.arrow_to_pandas(arrow_table, dtypes)
    pandas.testing.assert_series_equal(actual.dtypes, expected.dtypes)

    # assert_frame_equal is converting to numpy internally, which causes some
    # loss of precision with the extreme values in this test.
    for column in actual.columns:
        assert tuple(
            (index, value) if (value is pandas.NA or value == value) else (index, "nan")
            for index, value in actual[column].items()
        ) == tuple(
            (index, value) if (value is pandas.NA or value == value) else (index, "nan")
            for index, value in expected[column].items()
        )


@pytest.mark.parametrize(
    ("arrow_table", "dtypes"),
    (
        pytest.param(
            pyarrow.Table.from_pydict({"col1": [1], "col2": [2]}),
            {"col1": "Int64"},
            id="too-few-dtypes",
        ),
        pytest.param(
            pyarrow.RecordBatch.from_pydict({"col1": [1]}),
            {"col1": "Int64", "col2": "string[pyarrow]"},
            id="too-many-dtypes",
        ),
    ),
)
def test_arrow_to_pandas_wrong_size_dtypes(
    arrow_table: Union[pyarrow.Table, pyarrow.RecordBatch], dtypes: Dict
):
    with pytest.raises(ValueError, match=f"Number of types {len(dtypes)}"):
        bigframes.session._io.pandas.arrow_to_pandas(arrow_table, dtypes)
