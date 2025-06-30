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

import datetime
import decimal

import db_dtypes  # type: ignore
import geopandas  # type: ignore
import numpy
import pandas
import pyarrow
import pytest
import shapely.geometry  # type: ignore

from bigframes.pandas.io import api as module_under_test


@pytest.mark.parametrize(
    ("df_pd",),
    (
        # Regression tests for b/428190014.
        #
        # Test every BigQuery type we support, especially those where the legacy
        # SQL type name differs from the GoogleSQL type name.
        #
        # See:
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        # and compare to the legacy types at
        # https://cloud.google.com/bigquery/docs/data-types
        pytest.param(
            pandas.DataFrame(
                {
                    "ints": pandas.Series(
                        [[1], [2], [3]],
                        dtype=pandas.ArrowDtype(pyarrow.list_(pyarrow.int64())),
                    ),
                    "floats": pandas.Series(
                        [[1.0], [2.0], [3.0]],
                        dtype=pandas.ArrowDtype(pyarrow.list_(pyarrow.float64())),
                    ),
                }
            ),
            id="arrays",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "bool": pandas.Series([True, False, True], dtype="bool"),
                    "boolean": pandas.Series([True, None, True], dtype="boolean"),
                    "object": pandas.Series([True, None, True], dtype="object"),
                    "arrow": pandas.Series(
                        [True, None, True], dtype=pandas.ArrowDtype(pyarrow.bool_())
                    ),
                }
            ),
            id="bools",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "bytes": pandas.Series([b"a", b"b", b"c"], dtype=numpy.bytes_),
                    "object": pandas.Series([b"a", None, b"c"], dtype="object"),
                    "arrow": pandas.Series(
                        [b"a", None, b"c"], dtype=pandas.ArrowDtype(pyarrow.binary())
                    ),
                }
            ),
            id="bytes",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.date(2023, 11, 23),
                            None,
                            datetime.date(1970, 1, 1),
                        ],
                        dtype="object",
                    ),
                    "arrow": pandas.Series(
                        [
                            datetime.date(2023, 11, 23),
                            None,
                            datetime.date(1970, 1, 1),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.date32()),
                    ),
                }
            ),
            id="dates",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype="object",
                    ),
                    "datetime64": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype="datetime64[us]",
                    ),
                    "arrow": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.timestamp("us")),
                    ),
                }
            ),
            id="datetimes",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            shapely.geometry.Point(145.0, -37.8),
                            None,
                            shapely.geometry.Point(-122.3, 47.6),
                        ],
                        dtype="object",
                    ),
                    "geopandas": geopandas.GeoSeries(
                        [
                            shapely.geometry.Point(145.0, -37.8),
                            None,
                            shapely.geometry.Point(-122.3, 47.6),
                        ]
                    ),
                }
            ),
            id="geographys",
        ),
        # TODO(tswast): Add INTERVAL once BigFrames supports it.
        pytest.param(
            pandas.DataFrame(
                {
                    # TODO(tswast): Is there an equivalent object type we can use here?
                    # TODO(tswast): Add built-in Arrow extension type
                    "db_dtypes": pandas.Series(
                        ["{}", None, "123"],
                        dtype=pandas.ArrowDtype(db_dtypes.JSONArrowType()),
                    ),
                }
            ),
            id="jsons",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "int64": pandas.Series([1, 2, 3], dtype="int64"),
                    "Int64": pandas.Series([1, None, 3], dtype="Int64"),
                    "object": pandas.Series([1, None, 3], dtype="object"),
                    "arrow": pandas.Series(
                        [1, None, 3], dtype=pandas.ArrowDtype(pyarrow.int64())
                    ),
                }
            ),
            id="ints",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [decimal.Decimal("1.23"), None, decimal.Decimal("4.56")],
                        dtype="object",
                    ),
                    "arrow": pandas.Series(
                        [decimal.Decimal("1.23"), None, decimal.Decimal("4.56")],
                        dtype=pandas.ArrowDtype(pyarrow.decimal128(38, 9)),
                    ),
                }
            ),
            id="numerics",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    # TODO(tswast): Add object type for BIGNUMERIC. Can bigframes disambiguate?
                    "arrow": pandas.Series(
                        [decimal.Decimal("1.23"), None, decimal.Decimal("4.56")],
                        dtype=pandas.ArrowDtype(pyarrow.decimal256(76, 38)),
                    ),
                }
            ),
            id="bignumerics",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "float64": pandas.Series([1.23, None, 4.56], dtype="float64"),
                    "Float64": pandas.Series([1.23, None, 4.56], dtype="Float64"),
                    "object": pandas.Series([1.23, None, 4.56], dtype="object"),
                    "arrow": pandas.Series(
                        [1.23, None, 4.56], dtype=pandas.ArrowDtype(pyarrow.float64())
                    ),
                }
            ),
            id="floats",
        ),
        # TODO(tswast): Add RANGE once BigFrames supports it.
        pytest.param(
            pandas.DataFrame(
                {
                    "string": pandas.Series(["a", "b", "c"], dtype="string[python]"),
                    "object": pandas.Series(["a", None, "c"], dtype="object"),
                    "arrow": pandas.Series(["a", None, "c"], dtype="string[pyarrow]"),
                }
            ),
            id="strings",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    # TODO(tswast): Add object type for STRUCT? How to tell apart from JSON?
                    "arrow": pandas.Series(
                        [{"a": 1, "b": 1.0, "c": "c"}],
                        dtype=pandas.ArrowDtype(
                            pyarrow.struct(
                                [
                                    ("a", pyarrow.int64()),
                                    ("b", pyarrow.float64()),
                                    ("c", pyarrow.string()),
                                ]
                            )
                        ),
                    ),
                }
            ),
            id="structs",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.time(0, 0, 0),
                            None,
                            datetime.time(13, 7, 11),
                        ],
                        dtype="object",
                    ),
                    "arrow": pandas.Series(
                        [
                            datetime.time(0, 0, 0),
                            None,
                            datetime.time(13, 7, 11),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.time64("us")),
                    ),
                }
            ),
            id="times",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.datetime(
                                2023, 11, 23, 13, 14, 15, tzinfo=datetime.timezone.utc
                            ),
                            None,
                            datetime.datetime(
                                1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                        ],
                        dtype="object",
                    ),
                    "datetime64": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype="datetime64[us]",
                    ).dt.tz_localize("UTC"),
                    "arrow": pandas.Series(
                        [
                            datetime.datetime(
                                2023, 11, 23, 13, 14, 15, tzinfo=datetime.timezone.utc
                            ),
                            None,
                            datetime.datetime(
                                1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.timestamp("us", "UTC")),
                    ),
                }
            ),
            id="timestamps",
        ),
    ),
)
def test_read_gbq_colab_sessionless_dry_run_generates_valid_sql_for_local_dataframe(
    df_pd: pandas.DataFrame,
):
    # This method will fail with an exception if it receives invalid SQL.
    result = module_under_test._run_read_gbq_colab_sessionless_dry_run(
        query="SELECT * FROM {df_pd}",
        pyformat_args={"df_pd": df_pd},
    )
    assert isinstance(result, pandas.Series)
