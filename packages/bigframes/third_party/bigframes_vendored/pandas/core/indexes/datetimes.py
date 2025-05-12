# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexes/datetimes.py

from __future__ import annotations

from bigframes_vendored import constants
from bigframes_vendored.pandas.core.indexes import base


class DatetimeIndex(base.Index):
    """Immutable sequence used for indexing and alignment with datetime-like values"""

    @property
    def year(self) -> base.Index:
        """The year of the datetime

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([pd.Timestamp("20250215")])
            >>> idx.year
            Index([2025], dtype='Int64')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def month(self) -> base.Index:
        """The month as January=1, December=12.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([pd.Timestamp("20250215")])
            >>> idx.month
            Index([2], dtype='Int64')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def day(self) -> base.Index:
        """The day of the datetime.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([pd.Timestamp("20250215")])
            >>> idx.day
            Index([15], dtype='Int64')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def day_of_week(self) -> base.Index:
        """The day of the week with Monday=0, Sunday=6.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([pd.Timestamp("20250215")])
            >>> idx.day_of_week
            Index([5], dtype='Int64')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dayofweek(self) -> base.Index:
        """The day of the week with Monday=0, Sunday=6.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([pd.Timestamp("20250215")])
            >>> idx.dayofweek
            Index([5], dtype='Int64')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def weekday(self) -> base.Index:
        """The day of the week with Monday=0, Sunday=6.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([pd.Timestamp("20250215")])
            >>> idx.weekday
            Index([5], dtype='Int64')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
