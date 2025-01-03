# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/arrays/datetimelike.py

from bigframes import constants


class DatelikeOps:
    def strftime(self, date_format: str):
        """
        Convert to string Series using specified date_format.

        Return a Series of formatted strings specified by date_format. Details
        of the string format can be found in BigQuery format elements doc:
        https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements#format_elements_date_time.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.to_datetime(
            ...     ['2014-08-15 08:15:12', '2012-02-29 08:15:12+06:00', '2015-08-15 08:15:12+05:00'],
            ...     utc=True
            ... ).astype("timestamp[us, tz=UTC][pyarrow]")

            >>> s.dt.strftime("%B %d, %Y, %r")
            0      August 15, 2014, 08:15:12 AM
            1    February 29, 2012, 02:15:12 AM
            2      August 15, 2015, 03:15:12 AM
            dtype: string

        Args:
            date_format (str):
                Date format string (e.g. "%Y-%m-%d").

        Returns:
            bigframes.pandas.Series:
                Series of formatted strings.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def normalize(self):
        """
        Convert times to midnight.

        The time component of the date-time is converted to midnight i.e.
        00:00:00. This is useful in cases when the time does not matter.
        The return dtype will match the source series.

        This method is available on Series with datetime values under the
        .dt accessor.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> s = bpd.Series(pd.date_range(
            ...     start='2014-08-01 10:00',
            ...     freq='h',
            ...     periods=3,
            ...     tz='Asia/Calcutta')) # note timezones will be converted to UTC here
            >>> s.dt.normalize()
            0    2014-08-01 00:00:00+00:00
            1    2014-08-01 00:00:00+00:00
            2    2014-08-01 00:00:00+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]

        Returns:
            bigframes.pandas.Series:
                Series of the same dtype as the data.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def floor(self, freq: str):
        """
        Perform floor operation on the data to the specified freq.

        Supported freq arguments are: 'Y' (year), 'Q' (quarter), 'M'
        (month), 'W' (week), 'D' (day), 'h' (hour), 'min' (minute), 's'
        (second), 'ms' (microsecond), 'us' (nanosecond), 'ns' (nanosecond)

        Behavior around clock changes (i.e. daylight savings) is determined
        by the SQL engine, so "ambiguous" and "nonexistent" parameters are not
        supported. Y, Q, M, and W freqs are not supported by pandas as of
        version 2.2, but have been added here due to backend support.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> rng = pd.date_range('1/1/2018 11:59:00', periods=3, freq='min')
            >>> bpd.Series(rng).dt.floor("h")
            0    2018-01-01 11:00:00
            1    2018-01-01 12:00:00
            2    2018-01-01 12:00:00
            dtype: timestamp[us][pyarrow]

        Args:
            freq (str):
                Frequency string (e.g. "D", "min", "s").

        Returns:
            bigframes.pandas.Series:
                Series of the same dtype as the data.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
