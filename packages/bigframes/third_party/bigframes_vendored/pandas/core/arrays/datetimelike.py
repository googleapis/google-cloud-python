# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/arrays/datetimelike.py

from bigframes import constants


class DatelikeOps:
    def strftime(self, date_format: str):
        """
        Convert to string Series using specified date_format.

        Return a Series of formatted strings specified by date_format. Details
        of the string format can be found in `BigQuery format elements doc
        <%(https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements)s>`__.

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
            Name: 0, dtype: string

        Args:
            date_format (str):
                Date format string (e.g. "%Y-%m-%d").

        Returns:
            bigframes.series.Series of formatted strings.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
