# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/tools/datetimes.py

from datetime import datetime
from typing import List, Mapping, Tuple, Union

import pandas as pd

from bigframes import constants, series

local_iterables = Union[List, Tuple, pd.Series, pd.DataFrame, Mapping]


def to_datetime(
    arg,
    *,
    utc=False,
    format=None,
    unit=None,
) -> Union[pd.Timestamp, datetime, series.Series]:
    """
    This function converts a scalar, array-like or Series to a datetime object.

    .. note::
        BigQuery only supports precision up to microseconds (us). Therefore, when working
        with timestamps that have a finer granularity than microseconds, be aware that
        the additional precision will not be represented in BigQuery.

    .. note::
        The format strings for specifying datetime representations in BigQuery and pandas
        are not completely identical. Ensure that the format string provided is compatible
        with BigQuery (https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements#format_elements_date_time).

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None

    Converting a Scalar to datetime:

        >>> scalar = 123456.789
        >>> bpd.to_datetime(scalar, unit = 's')
        Timestamp('1970-01-02 10:17:36.789000')

    Converting a List of Strings without Timezone Information:

        >>> list_str = ["01-31-2021 14:30", "02-28-2021 15:45"]
        >>> bpd.to_datetime(list_str, format="%m-%d-%Y %H:%M", utc=True)
        0    2021-01-31 14:30:00+00:00
        1    2021-02-28 15:45:00+00:00
        dtype: timestamp[us, tz=UTC][pyarrow]

    Converting a Series of Strings with Timezone Information:

        >>> series_str = bpd.Series(["01-31-2021 14:30+08:00", "02-28-2021 15:45+00:00"])
        >>> bpd.to_datetime(series_str, format="%m-%d-%Y %H:%M%Z", utc=True)
        0    2021-01-31 06:30:00+00:00
        1    2021-02-28 15:45:00+00:00
        dtype: timestamp[us, tz=UTC][pyarrow]

    Args:
        arg (int, float, str, datetime, list, tuple, 1-d array, Series):
            The object to convert to a datetime.
        utc (bool, default False):
            Control timezone-related parsing, localization and conversion. If True, the
            function always returns a timezone-aware UTC-localized timestamp or series.
            If False (default), inputs will not be coerced to UTC.
        format (str, default None):
            The strftime to parse time, e.g. "%d/%m/%Y".
        unit (str, default 'ns'):
            The unit of the arg (D,s,ms,us,ns) denote the unit, which is an integer or
            float number.

    Returns:
        Union[pandas.Timestamp, datetime.datetime or bigframes.pandas.Series]:
            Return type depends on input.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
