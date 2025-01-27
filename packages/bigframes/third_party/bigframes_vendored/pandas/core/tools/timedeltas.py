# Contains code from https://github.com/pandas-dev/pandas/blob/v2.2.3/pandas/core/tools/timedeltas.py

import typing

from bigframes_vendored import constants
import pandas as pd

from bigframes import series

UnitChoices = typing.Literal[
    "W",
    "w",
    "D",
    "d",
    "days",
    "day",
    "hours",
    "hour",
    "hr",
    "h",
    "m",
    "minute",
    "min",
    "minutes",
    "s",
    "seconds",
    "sec",
    "second",
    "ms",
    "milliseconds",
    "millisecond",
    "milli",
    "millis",
    "us",
    "microseconds",
    "microsecond",
    "µs",
    "micro",
    "micros",
]


def to_timedelta(
    arg: typing.Union[series.Series, str, int, float],
    unit: typing.Optional[UnitChoices] = None,
) -> typing.Union[series.Series, pd.Timedelta]:
    """
    Converts a scalar or Series to a timedelta object.

    .. note::
        BigQuery only supports precision up to microseconds (us). Therefore, when working
        with timedeltas that have a finer granularity than microseconds, be aware that
        the additional precision will not be represented in BigQuery.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None

    Converting a Scalar to timedelta

        >>> scalar = 2
        >>> bpd.to_timedelta(scalar, unit='s')
        Timedelta('0 days 00:00:02')

    Converting a Series of integers to a Series of timedeltas

        >>> int_series = bpd.Series([1,2,3])
        >>> bpd.to_timedelta(int_series, unit='s')
        0    0 days 00:00:01
        1    0 days 00:00:02
        2    0 days 00:00:03
        dtype: duration[us][pyarrow]

    Args:
        arg (int, float, str, Series):
            The object to convert to a dataframe
        unit (str, default 'us'):
            Denotes the unit of the arg for numeric `arg`. Defaults to ``"us"``.

            Possible values:

            * 'W'
            * 'D' / 'days' / 'day'
            * 'hours' / 'hour' / 'hr' / 'h' / 'H'
            * 'm' / 'minute' / 'min' / 'minutes'
            * 's' / 'seconds' / 'sec' / 'second'
            * 'ms' / 'milliseconds' / 'millisecond' / 'milli' / 'millis'
            * 'us' / 'microseconds' / 'microsecond' / 'micro' / 'micros'

    Returns:
        Union[pandas.Timedelta, bigframes.pandas.Series]:
            Return type depends on input
            - Series: Series of duration[us][pyarrow] dtype
            - scalar: timedelta

    """

    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
