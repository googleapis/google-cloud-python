# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/arrays/arrow/accessors.py
"""Accessors for arrow-backed data."""

from __future__ import annotations

from bigframes import constants


class StructAccessor:
    """
    Accessor object for structured data properties of the Series values.
    """

    def field(self, name_or_index: str | int):
        """
        Extract a child field of a struct as a Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pyarrow as pa
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     [
            ...         {"version": 1, "project": "pandas"},
            ...         {"version": 2, "project": "pandas"},
            ...         {"version": 1, "project": "numpy"},
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.struct(
            ...         [("version", pa.int64()), ("project", pa.string())]
            ...     ))
            ... )

        Extract by field name.

            >>> s.struct.field("project")
            0    pandas
            1    pandas
            2     numpy
            Name: project, dtype: string

        Extract by field index.

            >>> s.struct.field(0)
            0    1
            1    2
            2    1
            Name: version, dtype: Int64

        Args:
            name_or_index:
                Name (str) or index (int) of the child field to extract.

        Returns:
            Series:
                The data corresponding to the selected child field.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def explode(self):
        """
        Extract all child fields of a struct as a DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pyarrow as pa
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     [
            ...         {"version": 1, "project": "pandas"},
            ...         {"version": 2, "project": "pandas"},
            ...         {"version": 1, "project": "numpy"},
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.struct(
            ...         [("version", pa.int64()), ("project", pa.string())]
            ...     ))
            ... )

        Extract all child fields.

            >>> s.struct.explode()
               version project
            0        1  pandas
            1        2  pandas
            2        1   numpy
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            DataFrame:
                The data corresponding to all child fields.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
