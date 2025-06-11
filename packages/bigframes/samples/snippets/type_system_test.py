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

import pandas.testing

from bigframes import dtypes


def test_type_system_examples() -> None:
    # [START bigquery_dataframes_type_sytem_timestamp_local_type_conversion]
    import pandas as pd

    import bigframes.pandas as bpd

    s = pd.Series([pd.Timestamp("20250101")])
    assert s.dtype == "datetime64[ns]"
    assert bpd.read_pandas(s).dtype == "timestamp[us][pyarrow]"
    # [END bigquery_dataframes_type_sytem_timestamp_local_type_conversion]

    # [START bigquery_dataframes_type_system_pyarrow_preference]
    import datetime

    import pandas as pd

    import bigframes.pandas as bpd

    s = pd.Series([datetime.date(2025, 1, 1)])
    s + pd.Timedelta(hours=12)
    # 0	2025-01-01
    # dtype: object

    bpd.read_pandas(s) + pd.Timedelta(hours=12)
    # 0    2025-01-01 12:00:00
    # dtype: timestamp[us][pyarrow]
    # [END bigquery_dataframes_type_system_pyarrow_preference]
    pandas.testing.assert_series_equal(
        s + pd.Timedelta(hours=12), pd.Series([datetime.date(2025, 1, 1)])
    )
    pandas.testing.assert_series_equal(
        (bpd.read_pandas(s) + pd.Timedelta(hours=12)).to_pandas(),
        pd.Series([pd.Timestamp(2025, 1, 1, 12)], dtype=dtypes.DATETIME_DTYPE),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_load_timedelta]
    import pandas as pd

    import bigframes.pandas as bpd

    s = pd.Series([pd.Timedelta("1s"), pd.Timedelta("2m")])
    bpd.read_pandas(s)
    # 0    0 days 00:00:01
    # 1    0 days 00:02:00
    # dtype: duration[us][pyarrow]
    # [END bigquery_dataframes_type_system_load_timedelta]
    pandas.testing.assert_series_equal(
        bpd.read_pandas(s).to_pandas(),
        s.astype(dtypes.TIMEDELTA_DTYPE),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_timedelta_precision]
    import pandas as pd

    s = pd.Series([pd.Timedelta("999ns")])
    bpd.read_pandas(s.dt.round("us"))
    # 0    0 days 00:00:00.000001
    # dtype: duration[us][pyarrow]
    # [END bigquery_dataframes_type_system_timedelta_precision]
    pandas.testing.assert_series_equal(
        bpd.read_pandas(s.dt.round("us")).to_pandas(),
        s.dt.round("us").astype(dtypes.TIMEDELTA_DTYPE),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_cast_timedelta]
    import bigframes.pandas as bpd

    bpd.to_timedelta([1, 2, 3], unit="s")
    # 0    0 days 00:00:01
    # 1    0 days 00:00:02
    # 2    0 days 00:00:03
    # dtype: duration[us][pyarrow]
    # [END bigquery_dataframes_type_system_cast_timedelta]
    pandas.testing.assert_series_equal(
        bpd.to_timedelta([1, 2, 3], unit="s").to_pandas(),
        pd.Series(pd.to_timedelta([1, 2, 3], unit="s"), dtype=dtypes.TIMEDELTA_DTYPE),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_list_accessor]
    import bigframes.pandas as bpd

    s = bpd.Series([[1, 2, 3], [4, 5], [6]])  # dtype: list<item: int64>[pyarrow]

    # Access the first elements of each list
    s.list[0]
    # 0    1
    # 1    4
    # 2    6
    # dtype: Int64

    # Get the lengths of each list
    s.list.len()
    # 0    3
    # 1    2
    # 2    1
    # dtype: Int64
    # [END bigquery_dataframes_type_system_list_accessor]
    pandas.testing.assert_series_equal(
        s.list[0].to_pandas(),
        pd.Series([1, 4, 6], dtype="Int64"),
        check_index_type=False,
    )
    pandas.testing.assert_series_equal(
        s.list.len().to_pandas(),
        pd.Series([3, 2, 1], dtype="Int64"),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_struct_accessor]
    import bigframes.pandas as bpd

    structs = [
        {"id": 101, "category": "A"},
        {"id": 102, "category": "B"},
        {"id": 103, "category": "C"},
    ]
    s = bpd.Series(structs)
    # Get the 'id' field of each struct
    s.struct.field("id")
    # 0    101
    # 1    102
    # 2    103
    # Name: id, dtype: Int64
    # [END bigquery_dataframes_type_system_struct_accessor]

    # [START bigquery_dataframes_type_system_struct_accessor_shortcut]
    import bigframes.pandas as bpd

    structs = [
        {"id": 101, "category": "A"},
        {"id": 102, "category": "B"},
        {"id": 103, "category": "C"},
    ]
    s = bpd.Series(structs)

    # not explicitly using the "struct" property
    s.id
    # 0    101
    # 1    102
    # 2    103
    # Name: id, dtype: Int64
    # [END bigquery_dataframes_type_system_struct_accessor_shortcut]
    pandas.testing.assert_series_equal(
        s.struct.field("id").to_pandas(),
        pd.Series([101, 102, 103], dtype="Int64", name="id"),
        check_index_type=False,
    )
    pandas.testing.assert_series_equal(
        s.id.to_pandas(),
        pd.Series([101, 102, 103], dtype="Int64", name="id"),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_string_accessor]
    import bigframes.pandas as bpd

    s = bpd.Series(["abc", "de", "1"])  # dtype: string[pyarrow]

    # Get the first character of each string
    s.str[0]
    # 0    a
    # 1    d
    # 2    1
    # dtype: string

    # Check whether there are only alphabetic characters in each string
    s.str.isalpha()
    # 0     True
    # 1     True
    # 2     False
    # dtype: boolean

    # Cast the alphabetic characters to their upper cases for each string
    s.str.upper()
    # 0    ABC
    # 1     DE
    # 2      1
    # dtype: string
    # [END bigquery_dataframes_type_system_string_accessor]
    pandas.testing.assert_series_equal(
        s.str[0].to_pandas(),
        pd.Series(["a", "d", "1"], dtype=dtypes.STRING_DTYPE),
        check_index_type=False,
    )
    pandas.testing.assert_series_equal(
        s.str.isalpha().to_pandas(),
        pd.Series([True, True, False], dtype=dtypes.BOOL_DTYPE),
        check_index_type=False,
    )
    pandas.testing.assert_series_equal(
        s.str.upper().to_pandas(),
        pd.Series(["ABC", "DE", "1"], dtype=dtypes.STRING_DTYPE),
        check_index_type=False,
    )

    # [START bigquery_dataframes_type_system_geo_accessor]
    from shapely.geometry import Point

    import bigframes.pandas as bpd

    s = bpd.Series([Point(1, 0), Point(2, 1)])  # dtype: geometry

    s.geo.y
    # 0    0.0
    # 1    1.0
    # dtype: Float64
    # [END bigquery_dataframes_type_system_geo_accessor]
    pandas.testing.assert_series_equal(
        s.geo.y.to_pandas(),
        pd.Series([0.0, 1.0], dtype=dtypes.FLOAT_DTYPE),
        check_index_type=False,
    )
