from bigframes import constants


class DatetimeProperties:
    """
    Accessor object for datetime-like properties of the Series values.
    """

    @property
    def day(self):
        """The day of the datetime.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range("2000-01-01", periods=3, freq="D")
            ... )
            >>> s
            0    2000-01-01 00:00:00
            1    2000-01-02 00:00:00
            2    2000-01-03 00:00:00
            dtype: timestamp[us][pyarrow]
            >>> s.dt.day
            0    1
            1    2
            2    3
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dayofweek(self):
        """The day of the week with Monday=0, Sunday=6.

        Return the day of the week. It is assumed the week starts on
        Monday, which is denoted by 0 and ends on Sunday, which is denoted
        by 6.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range('2016-12-31', '2017-01-08', freq='D').to_series()
            ... )
            >>> s.dt.dayofweek
            2016-12-31 00:00:00    5
            2017-01-01 00:00:00    6
            2017-01-02 00:00:00    0
            2017-01-03 00:00:00    1
            2017-01-04 00:00:00    2
            2017-01-05 00:00:00    3
            2017-01-06 00:00:00    4
            2017-01-07 00:00:00    5
            2017-01-08 00:00:00    6
            dtype: Int64

        Returns:
            Series: Containing integers indicating the day number.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dayofyear(self):
        """The ordinal day of the year.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range('2016-12-28', '2017-01-03', freq='D').to_series()
            ... )
            >>> s.dt.dayofyear
            2016-12-28 00:00:00    363
            2016-12-29 00:00:00    364
            2016-12-30 00:00:00    365
            2016-12-31 00:00:00    366
            2017-01-01 00:00:00      1
            2017-01-02 00:00:00      2
            2017-01-03 00:00:00      3
            dtype: Int64

        Returns:
            Series: Containing integers indicating the day number.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def date(self):
        """Returns a Series with the date part of Timestamps without time and
        timezone information.

        .. warning::
            This method returns a Series whereas pandas returns
            a numpy array.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(["1/1/2020 10:00:00+00:00", "2/1/2020 11:00:00+00:00"])
            >>> s = bpd.to_datetime(s, utc=True, format="%d/%m/%Y %H:%M:%S%Ez")
            >>> s
            0    2020-01-01 10:00:00+00:00
            1    2020-01-02 11:00:00+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]
            >>> s.dt.date
            0   2020-01-01
            1   2020-01-02
            dtype: date32[day][pyarrow]
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def hour(self):
        """The hours of the datetime.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range("2000-01-01", periods=3, freq="h")
            ... )
            >>> s
            0    2000-01-01 00:00:00
            1    2000-01-01 01:00:00
            2    2000-01-01 02:00:00
            dtype: timestamp[us][pyarrow]
            >>> s.dt.hour
            0    0
            1    1
            2    2
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def minute(self):
        """The minutes of the datetime.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range("2000-01-01", periods=3, freq="min")
            ... )
            >>> s
            0    2000-01-01 00:00:00
            1    2000-01-01 00:01:00
            2    2000-01-01 00:02:00
            dtype: timestamp[us][pyarrow]
            >>> s.dt.minute
            0    0
            1    1
            2    2
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def month(self):
        """The month as January=1, December=12.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range("2000-01-01", periods=3, freq="M")
            ... )
            >>> s
            0    2000-01-31 00:00:00
            1    2000-02-29 00:00:00
            2    2000-03-31 00:00:00
            dtype: timestamp[us][pyarrow]
            >>> s.dt.month
            0    1
            1    2
            2    3
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isocalendar(self):
        """
        Calculate year, week, and day according to the ISO 8601 standard.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range('2009-12-27', '2010-01-04', freq='d').to_series()
            ... )
            >>> s.dt.isocalendar()
                                 year  week  day
            2009-12-27 00:00:00  2009    52    7
            2009-12-28 00:00:00  2009    53    1
            2009-12-29 00:00:00  2009    53    2
            2009-12-30 00:00:00  2009    53    3
            2009-12-31 00:00:00  2009    53    4
            2010-01-01 00:00:00  2009    53    5
            2010-01-02 00:00:00  2009    53    6
            2010-01-03 00:00:00  2009    53    7
            2010-01-04 00:00:00  2010     1    1
            <BLANKLINE>
            [9 rows x 3 columns]


        Returns: DataFrame
            With columns year, week and day.


        """

    @property
    def second(self):
        """The seconds of the datetime.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range("2000-01-01", periods=3, freq="s")
            ... )
            >>> s
            0    2000-01-01 00:00:00
            1    2000-01-01 00:00:01
            2    2000-01-01 00:00:02
            dtype: timestamp[us][pyarrow]
            >>> s.dt.second
            0    0
            1    1
            2    2
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def time(self):
        """Returns a Series with the time part of the Timestamps.

        .. warning::
            This method returns a Series whereas pandas returns
            a numpy array.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(["1/1/2020 10:00:00+00:00", "2/1/2020 11:00:00+00:00"])
            >>> s = bpd.to_datetime(s, utc=True, format="%m/%d/%Y %H:%M:%S%Ez")
            >>> s
            0    2020-01-01 10:00:00+00:00
            1    2020-02-01 11:00:00+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]
            >>> s.dt.time
            0    10:00:00
            1    11:00:00
            dtype: time64[us][pyarrow]
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def quarter(self):
        """The quarter of the date.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(["1/1/2020 10:00:00+00:00", "4/1/2020 11:00:00+00:00"])
            >>> s = bpd.to_datetime(s, utc=True, format="%m/%d/%Y %H:%M:%S%Ez")
            >>> s
            0    2020-01-01 10:00:00+00:00
            1    2020-04-01 11:00:00+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]
            >>> s.dt.quarter
            0    1
            1    2
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def year(self):
        """The year of the datetime.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     pd.date_range("2000-01-01", periods=3, freq="Y")
            ... )
            >>> s
            0    2000-12-31 00:00:00
            1    2001-12-31 00:00:00
            2    2002-12-31 00:00:00
            dtype: timestamp[us][pyarrow]
            >>> s.dt.year
            0    2000
            1    2001
            2    2002
            dtype: Int64
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def days(self):
        """The numebr of days for each element

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([pd.Timedelta("4d3m2s1us")])
            >>> s
            0    4 days 00:03:02.000001
            dtype: duration[us][pyarrow]
            >>> s.dt.days
            0    4
            dtype: Int64
        """

    @property
    def seconds(self):
        """Number of seconds (>= 0 and less than 1 day) for each element.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([pd.Timedelta("4d3m2s1us")])
            >>> s
            0    4 days 00:03:02.000001
            dtype: duration[us][pyarrow]
            >>> s.dt.seconds
            0    182
            dtype: Int64
        """

    @property
    def microseconds(self):
        """Number of microseconds (>= 0 and less than 1 second) for each element.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([pd.Timedelta("4d3m2s1us")])
            >>> s
            0    4 days 00:03:02.000001
            dtype: duration[us][pyarrow]
            >>> s.dt.microseconds
            0    1
            dtype: Int64
        """

    def total_seconds(self):
        """Return total duration of each element expressed in seconds.

        **Examples:**

            >>> import pandas as pd
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([pd.Timedelta("1d1m1s1us")])
            >>> s
            0    1 days 00:01:01.000001
            dtype: duration[us][pyarrow]
            >>> s.dt.total_seconds()
            0    86461.000001
            dtype: Float64
        """

    @property
    def tz(self):
        """Return the timezone.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(["1/1/2020 10:00:00+00:00", "2/1/2020 11:00:00+00:00"])
            >>> s = bpd.to_datetime(s, utc=True, format="%m/%d/%Y %H:%M:%S%Ez")
            >>> s
            0    2020-01-01 10:00:00+00:00
            1    2020-02-01 11:00:00+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]
            >>> s.dt.tz
            datetime.timezone.utc

        Returns:
            datetime.tzinfo, pytz.tzinfo.BaseTZInfo, dateutil.tz.tz.tzfile, or None
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def unit(self) -> str:
        """Returns the unit of time precision.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(["1/1/2020 10:00:00+00:00", "2/1/2020 11:00:00+00:00"])
            >>> s = bpd.to_datetime(s, utc=True, format="%m/%d/%Y %H:%M:%S%Ez")
            >>> s
            0    2020-01-01 10:00:00+00:00
            1    2020-02-01 11:00:00+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]
            >>> s.dt.unit
            'us'

        Returns:
            Unit as string (eg. "us").
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
