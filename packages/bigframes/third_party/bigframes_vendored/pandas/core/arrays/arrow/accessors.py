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
            ...         {"project": "pandas", "version": 1},
            ...         {"project": "pandas", "version": 2},
            ...         {"project": "numpy", "version": 1},
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.struct(
            ...         [("project", pa.string()), ("version", pa.int64())]
            ...     ))
            ... )

        Extract by field name.

            >>> s.struct.field("project")
            0    pandas
            1    pandas
            2     numpy
            Name: project, dtype: string

        Extract by field index.

            >>> s.struct.field(1)
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
            ...         {"project": "pandas", "version": 1},
            ...         {"project": "pandas", "version": 2},
            ...         {"project": "numpy", "version": 1},
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.struct(
            ...         [("project", pa.string()), ("version", pa.int64())]
            ...     ))
            ... )

        Extract all child fields.

            >>> s.struct.explode()
               project version
            0   pandas       1
            1   pandas       2
            2    numpy       1
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
            project    string[pyarrow]
            version              Int64
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
            ...         {"project": "pandas", "version": 1},
            ...         {"project": "pandas", "version": 2},
            ...         {"project": "numpy", "version": 1},
            ...     ],
            ...     dtype=bpd.ArrowDtype(pa.struct(
            ...         [("project", pa.string()), ("version", pa.int64())]
            ...     ))
            ... )
            >>> downloads = bpd.Series([100, 200, 300])
            >>> df = bpd.DataFrame({"country": countries, "file": files, "download_count": downloads})
            >>> df.struct.explode("file")
              country file.project  file.version  download_count
            0      cn       pandas             1             100
            1      es       pandas             2             200
            2      us        numpy             1             300
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
