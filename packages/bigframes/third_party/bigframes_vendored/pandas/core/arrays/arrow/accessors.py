# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/arrays/arrow/accessors.py
"""Accessors for arrow-backed data."""

from __future__ import annotations

from bigframes import constants


class ListAccessor:
    """Accessor object for list data properties of the Series values."""

    def len(self):
        """Compute the length of each list in the Series.

        **See Also:**

            - :func:`StringMethods.len` : Compute the length of each element in the Series/Index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pyarrow as pa
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     [
            ...         [1, 2, 3],
            ...         [3],
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.list_(pa.int64())),
            ... )
            >>> s.list.len()
            0    3
            1    1
            dtype: Int64

        Returns:
            bigframes.series.Series: A Series or Index of integer values indicating
                the length of each element in the Series or Index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __getitem__(self, key: int | slice):
        """Index or slice lists in the Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pyarrow as pa
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series(
            ...     [
            ...         [1, 2, 3],
            ...         [3],
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.list_(pa.int64())),
            ... )
            >>> s.list[0]
            0    1
            1    3
            dtype: Int64

        Args:
            key (int | slice): Index or slice of indices to access from each list.
                For integer indices, only non-negative values are accepted. For
                slices, you must use a non-negative start, a non-negative end, and
                a step of 1.

        Returns:
            bigframes.series.Series: The list at requested index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


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

    def dtypes(self):
        """
        Return the dtype object of each child field of the struct.

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
            >>> s.struct.dtypes()
            version              Int64
            project    string[pyarrow]
            dtype: object

        Returns:
            A *pandas* Series with the data type of all child fields.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class StructFrameAccessor:
    """
    Accessor object for structured data properties of the DataFrame values.
    """

    def explode(self, column, *, separator: str = "."):
        """
        Extract all child fields of struct column(s) and add to the DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pyarrow as pa
            >>> bpd.options.display.progress_bar = None
            >>> countries = bpd.Series(["cn", "es", "us"])
            >>> files = bpd.Series(
            ...     [
            ...         {"version": 1, "project": "pandas"},
            ...         {"version": 2, "project": "pandas"},
            ...         {"version": 1, "project": "numpy"},
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.struct(
            ...         [("version", pa.int64()), ("project", pa.string())]
            ...     ))
            ... )
            >>> downloads = bpd.Series([100, 200, 300])
            >>> df = bpd.DataFrame({"country": countries, "file": files, "download_count": downloads})
            >>> df.struct.explode("file")
              country  file.version file.project  download_count
            0      cn             1       pandas             100
            1      es             2       pandas             200
            2      us             1        numpy             300
            <BLANKLINE>
            [3 rows x 4 columns]

        Args:
            column:
                Column(s) to explode. For multiple columns, specify a non-empty
                list with each element be str or tuple, and all specified
                columns their list-like data on same row of the frame must
                have matching length.
            separator:
                Separator/delimiter to use to separate the original column name
                from the sub-field column name.


        Returns:
            DataFrame:
                Original DataFrame with exploded struct column(s).
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
