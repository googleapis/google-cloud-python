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

from bigframes import operations as ops
from bigframes import series


def unix_seconds(input: series.Series) -> series.Series:
    """Converts a timestmap series to unix epoch seconds

    **Examples:**

        >>> import pandas as pd
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([pd.Timestamp("1970-01-02", tz="UTC"), pd.Timestamp("1970-01-03", tz="UTC")])
        >>> bbq.unix_seconds(s)
        0     86400
        1    172800
        dtype: Int64

    Args:
        input (bigframes.pandas.Series):
            A timestamp series.

    Returns:
        bigframes.pandas.Series: A new series of unix epoch in seconds.

    """
    return input._apply_unary_op(ops.UnixSeconds())


def unix_millis(input: series.Series) -> series.Series:
    """Converts a timestmap series to unix epoch milliseconds

    **Examples:**

        >>> import pandas as pd
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([pd.Timestamp("1970-01-02", tz="UTC"), pd.Timestamp("1970-01-03", tz="UTC")])
        >>> bbq.unix_millis(s)
        0     86400000
        1    172800000
        dtype: Int64

    Args:
        input (bigframes.pandas.Series):
            A timestamp series.

    Returns:
        bigframes.pandas.Series: A new series of unix epoch in milliseconds.

    """
    return input._apply_unary_op(ops.UnixMillis())


def unix_micros(input: series.Series) -> series.Series:
    """Converts a timestmap series to unix epoch microseconds

    **Examples:**

        >>> import pandas as pd
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([pd.Timestamp("1970-01-02", tz="UTC"), pd.Timestamp("1970-01-03", tz="UTC")])
        >>> bbq.unix_micros(s)
        0     86400000000
        1    172800000000
        dtype: Int64

    Args:
        input (bigframes.pandas.Series):
            A timestamp series.

    Returns:
        bigframes.pandas.Series: A new series of unix epoch in microseconds.

    """
    return input._apply_unary_op(ops.UnixMicros())
