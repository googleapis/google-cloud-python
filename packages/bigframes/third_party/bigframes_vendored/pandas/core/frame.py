# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/frame.py
"""
DataFrame
---------
An efficient 2D container for potentially mixed-type time series or other
labeled data series.

Similar to its R counterpart, data.frame, except providing automatic data
alignment and a host of useful data manipulation methods having to do with the
labeling information
"""
from __future__ import annotations

from typing import Iterable, Literal, Mapping, Optional, Sequence, Union

from third_party.bigframes_vendored.pandas.core.generic import NDFrame

# -----------------------------------------------------------------------
# DataFrame class


class DataFrame(NDFrame):
    """Two-dimensional, size-mutable, potentially heterogeneous tabular data.

    Data structure also contains labeled axes (rows and columns).
    Arithmetic operations align on both row and column labels. Can be
    thought of as a dict-like container for Series objects. The primary
    pandas data structure.
    """

    @property
    def shape(self) -> tuple[int, int]:
        """Return a tuple representing the dimensionality of the DataFrame."""
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # IO methods (to / from other formats)

    def to_gbq(
        self,
        destination_table: str,
        *,
        if_exists: Optional[Literal["fail", "replace", "append"]] = "fail",
        index: bool = True,
    ) -> None:
        """Write a DataFrame to a Google BigQuery table.

        Args:
            destination_table : str
                Name of table to be written, in the form ``dataset.tablename``
                or ``project.dataset.tablename``.

            if_exists : str, default 'fail'
                Behavior when the destination table exists. Value can be one of:

                ``'fail'``
                    If table exists raise pandas_gbq.gbq.TableCreationError.
                ``'replace'``
                    If table exists, drop it, recreate it, and insert data.
                ``'append'``
                    If table exists, insert data. Create if does not exist.

            index: whether write row names (index) or not.
        """
        raise NotImplementedError("abstract method")

    def to_parquet(
        self,
        path: str,
        *,
        index: bool = True,
    ) -> None:
        """Write a DataFrame to the binary parquet format.

        This function writes the dataframe as a `parquet file
        <https://parquet.apache.org/>`_ to Google Cloud Storage.

        Args:
            path:
                Destination URI(s) of GCS files(s) to store the extracted dataframe
                in format of ``gs://<bucket_name>/<object_name_or_glob>``.
                If the data size is more than 1GB, you must use a wildcard to export
                the data into multiple files and the size of the files varies.

            index : bool, default None
                If ``True``, include the dataframe's index(es) in the file output.
                If ``False``, they will not be written to the file.

        Returns:
            None.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Unsorted

    def assign(self, **kwargs) -> DataFrame:
        r"""
        Assign new columns to a DataFrame.

        Returns a new object with all original columns in addition to new ones.
        Existing columns that are re-assigned will be overwritten.

        Args:
            kwargs:
                A dictionary of ``{str: values}``. The column names are
                keywords. If the values (e.g. a Series, scalar, or array), they
                are simply assigned to the column.

        Returns:
            A new DataFrame with the new columns in addition to
            all the existing columns.

        Notes:
            Assigning multiple columns within the same ``assign`` is possible.
            Later items in '\*\*kwargs' may refer to newly created or modified
            columns in 'df'; items are computed and assigned into 'df' in
            order.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Reindexing and alignment

    def drop(
        self,
        *,
        columns: Union[str, Iterable[str]],
    ) -> DataFrame | None:
        """Drop specified labels from columns.

        Remove columns by directly specifying column names.

        Args:
            columns:
                Single label or list-like.

        Returns:
            DataFrame without the removed column labels.

        Raises:
            KeyError:
                If any of the labels is not found in the selected axis.
        """
        raise NotImplementedError("abstract method")

    def rename(
        self,
        *,
        columns: Mapping,
    ) -> DataFrame:
        """Rename columns.

        Dict values must be unique (1-to-1). Labels not contained in a dict
        will be left as-is. Extra labels listed don't throw an error.

        Args:
            columns:
                Dict-like from old column labels to new column labels.

        Returns:
            DataFrame with the renamed axis labels.

        Raises:
            KeyError:
                If any of the labels is not found.
        """
        raise NotImplementedError("abstract method")

    def rename_axis(self, mapper: Optional[str], **kwargs) -> DataFrame:
        """
        Set the name of the axis for the index.

        Note: currently only accepts a single string parameter (the new name of the index)

        Args:
            mapper : str
                Value to set the axis name attribute.

        Returns:
            DataFrame with the new index name
        """
        raise NotImplementedError("abstract method")

    def set_index(
        self,
        keys,
        *,
        drop: bool = True,
    ) -> DataFrame | None:
        """
        Set the DataFrame index using existing columns.

        Set the DataFrame index (row labels) using one existing column. The
        index can replace the existing index.

        Args:
            keys:
                A label. This parameter can be a single column key.
            drop:
                Delete columns to be used as the new index.

        Returns:
            DataFrame:
                Changed row labels.
        """
        raise NotImplementedError("abstract method")

    def reorder_levels(self, order: Sequence[int | str]) -> DataFrame:
        """
        Rearrange index levels using input order. May not drop or duplicate levels.

        Args:
            order: list of int or list of str
                List representing new level order. Reference level by number
                (position) or by key (label).

        Returns:
            DataFrame
        """
        raise NotImplementedError("abstract method")

    def droplevel(self, level):
        """
        Return DataFrame with requested index / column level(s) removed.

        Args:
            level: int, str, or list-like
                If a string is given, must be the name of a level
                If list-like, elements must be names or positional indexes
                of levels.
        Returns:
            DataFrame with requested index / column level(s) removed.
        """
        raise NotImplementedError("abstract method")

    def reset_index(
        self,
        *,
        drop: bool = False,
    ) -> DataFrame | None:
        """Reset the index.

        Reset the index of the DataFrame, and use the default one instead.

        Args:
            drop:
                Do not try to insert index into dataframe columns. This resets
                the index to the default integer index.

        Returns:
            DataFrame with the new index.
        """
        raise NotImplementedError("abstract method")

    def drop_duplicates(
        self,
        *,
        keep="first",
    ) -> DataFrame:
        """
        Return DataFrame with duplicate rows removed.

        Considering certain columns is optional. Indexes, including time indexes
        are ignored.

        Args:
            subset : column label or sequence of labels, optional
                Only consider certain columns for identifying duplicates, by
                default use all of the columns.
            keep : {'first', 'last', ``False``}, default 'first'
                Determines which duplicates (if any) to keep.

                - 'first' : Drop duplicates except for the first occurrence.
                - 'last' : Drop duplicates except for the last occurrence.
                - ``False`` : Drop all duplicates.

        Returns:
            DataFrame with duplicates removed
        """
        raise NotImplementedError("abstract method")

    def duplicated(self, subset=None, keep="first"):
        """
        Return boolean Series denoting duplicate rows.

        Considering certain columns is optional.

        Args:
            subset : column label or sequence of labels, optional
                Only consider certain columns for identifying duplicates, by
                default use all of the columns.
            keep : {'first', 'last', False}, default 'first'
                Determines which duplicates (if any) to mark.

                - ``first`` : Mark duplicates as ``True`` except for the first occurrence.
                - ``last`` : Mark duplicates as ``True`` except for the last occurrence.
                - False : Mark all duplicates as ``True``.

        Returns:
            Boolean series for each duplicated rows.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Reindex-based selection methods

    def dropna(
        self,
    ) -> DataFrame:
        """Remove missing values.

        Returns:
            DataFrame with NA entries dropped from it.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Sorting

    def sort_values(
        self,
        by: str | Sequence[str],
        *,
        ascending: bool | Sequence[bool] = True,
        na_position="last",
    ) -> DataFrame:
        """Sort by the values along row axis.

        Args:
            by:
                Name or list of names to sort by.
            ascending:
                Sort ascending vs. descending. Specify list for multiple sort
                orders.  If this is a list of bools, must match the length of
                the by.
            na_position:
             ``{'first', 'last'}``, default 'last' Puts NaNs at the beginning
             if `first`; `last` puts NaNs at the end.

        Returns:
            DataFrame with sorted values.
        """
        raise NotImplementedError("abstract method")

    def sort_index(
        self,
    ) -> DataFrame:
        """Sort object by labels (along an axis).

        Returns:
            The original DataFrame sorted by the labels.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Arithmetic Methods

    def le(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'less than or equal to' of dataframe and other, element-wise (binary operator `<=`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        Args:
            other: scalar, sequence, Series, or DataFrame
                Any single or multiple element data structure, or list-like object.
            axis: {{0 or 'index', 1 or 'columns'}}, default 'columns'
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame of bool. The result of the comparison.

        Notes:
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).
        """
        raise NotImplementedError("abstract method")

    def lt(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'less than' of dataframe and other, element-wise (binary operator `<`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        Args:
            other: scalar, sequence, Series, or DataFrame
                Any single or multiple element data structure, or list-like object.
            axis: {{0 or 'index', 1 or 'columns'}}, default 'columns'
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame of bool. The result of the comparison.

        Notes:
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).
        """
        raise NotImplementedError("abstract method")

    def ge(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'greater than or equal to' of dataframe and other, element-wise (binary operator `>=`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        Args:
            other: scalar, sequence, Series, or DataFrame
                Any single or multiple element data structure, or list-like object.
            axis: {{0 or 'index', 1 or 'columns'}}, default 'columns'
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame of bool. The result of the comparison.

        Notes:
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).
        """
        raise NotImplementedError("abstract method")

    def gt(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'greater than' of dataframe and other, element-wise (binary operator `>`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        Args:
            other: scalar, sequence, Series, or DataFrame
                Any single or multiple element data structure, or list-like object.
            axis: {{0 or 'index', 1 or 'columns'}}, default 'columns'
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame of bool. The result of the comparison.

        Notes:
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).
        """
        raise NotImplementedError("abstract method")

    def add(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'addition' of dataframe and other, element-wise (binary operator `+`).

        Equivalent to ``dataframe + other``. With reverse version, `radd`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def sub(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'subtraction' of dataframe and other, element-wise (binary operator `-`).

        Equivalent to ``dataframe - other``. With reverse version, `rsub`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def rsub(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'subtraction' of dataframe and other, element-wise (binary operator `-`).

        Equivalent to ``other - dataframe``. With reverse version, `sub`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def mul(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'multiplication' of dataframe and other, element-wise (binary operator `*`).

        Equivalent to ``dataframe * other``. With reverse version, `rmul`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def truediv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'floating division' of dataframe and other, element-wise (binary operator `/`).

        Equivalent to ``dataframe / other``. With reverse version, `rtruediv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def rtruediv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'floating division' of dataframe and other, element-wise (binary operator `/`).

        Equivalent to ``other / dataframe``. With reverse version, `truediv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def floordiv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'integer division' of dataframe and other, element-wise (binary operator `//`).

        Equivalent to ``dataframe // other``. With reverse version, `rfloordiv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def rfloordiv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'integer division' of dataframe and other, element-wise (binary operator `//`).

        Equivalent to ``other // dataframe``. With reverse version, `rfloordiv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def mod(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'modulo' of dataframe and other, element-wise (binary operator `%`).

        Equivalent to ``dataframe % other``. With reverse version, `rmod`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    def rmod(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'modulo' of dataframe and other, element-wise (binary operator `%`).

        Equivalent to ``other % dataframe``. With reverse version, `mod`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis:
                ``{{0 or 'index', 1 or 'columns'}}``. Whether to compare by the
                index (0 or 'index') or columns. (1 or 'columns'). For Series
                input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.

        Notes:
            Mismatched indices will be unioned together.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Data reshaping

    def groupby(
        self,
        by: Union[str, Sequence[str]],
        *,
        level=None,
        as_index: bool = True,
        dropna: bool = True,
    ):
        """Group DataFrame by columns.

        A groupby operation involves some combination of splitting the
        object, applying a function, and combining the results. This can be
        used to group large amounts of data and compute operations on these
        groups.

        Args:
            by:
                A label or list of labels may be passed to group by the columns
                in ``self``. Notice that a tuple is interpreted as a (single)
                key.
            level : int, level name, or sequence of such, default None
                If the axis is a MultiIndex (hierarchical), group by a particular
                level or levels. Do not specify both ``by`` and ``level``.
            as_index:
                Default True. Return object with group labels as the index.
                Only relevant for DataFrame input. ``as_index=False`` is
                effectively "SQL-style" grouped output. This argument has no
                effect on filtrations such as ``head()``, ``tail()``, ``nth()``
                and in transformations.
            dropna:
                Default True. If True, and if group keys contain NA values, NA
                values together with row/column will be dropped. If False, NA
                values will also be treated as the key in groups.

        Returns:
            A groupby object that contains information about the groups.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Function application

    def map(self, func, na_action: Optional[str] = None) -> DataFrame:
        """Apply a function to a Dataframe elementwise.

        .. note::

           In pandas 2.1.0, DataFrame.applymap is deprecated and renamed to
           DataFrame.map.

        This method applies a function that accepts and returns a scalar
        to every element of a DataFrame.

        Args:
            func:
                Python function wrapped by ``remote_function`` decorator,
                returns a single value from a single value.
            na_action:
                ``{None, 'ignore'}``, default None. If ‘ignore’, propagate NaN
                values, without passing them to func.

        Returns:
            Transformed DataFrame.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Merging / joining methods

    def join(self, other, *, how: str) -> DataFrame:
        """Join columns of another DataFrame.

        Join columns with `other` DataFrame on index

        Args:
            other:
                DataFrame with an Index similar to the Index of this one.
            how:
                ``{'left', 'right', 'outer', 'inner'}, default 'left'``

                How to handle the operation of the two objects.

                * left: use calling frame's index (or column if on is specified)
                * right: use `other`'s index.
                * outer: form union of calling frame's index (or column if on is
                  specified) with `other`'s index, and sort it.
                  lexicographically.
                * inner: form intersection of calling frame's index (or column if
                  on is specified) with `other`'s index, preserving the order
                  of the calling's one.

        Returns:
            A dataframe containing columns from both the caller and `other`.
        """
        raise NotImplementedError("abstract method")

    def merge(
        self,
        right,
        how: Literal[
            "inner",
            "left",
            "outer",
            "right",
        ] = "inner",
        on: Optional[str] = None,
        *,
        left_on: Optional[str] = None,
        right_on: Optional[str] = None,
        sort: bool = False,
        suffixes: tuple[str, str] = ("_x", "_y"),
    ) -> DataFrame:
        """Merge DataFrame objects with a database-style join.

        The join is done on columns or indexes. If joining columns on
        columns, the DataFrame indexes *will be ignored*. Otherwise if joining indexes
        on indexes or indexes on a column or columns, the index will be passed on.
        When performing a cross merge, no column specifications to merge on are
        allowed.

        .. warning::

            If both key columns contain rows where the key is a null value, those
            rows will be matched against each other. This is different from usual SQL
            join behaviour and can lead to unexpected results.

        Args:
            right:
                Object to merge with.
            how:
                ``{'left', 'right', 'outer', 'inner'}, default 'inner'``
                Type of merge to be performed.

                * left: use only keys from left frame, similar to a SQL left outer join;
                  preserve key order.
                * right: use only keys from right frame, similar to a SQL right outer join;
                  preserve key order.
                * outer: use union of keys from both frames, similar to a SQL full outer
                  join; sort keys lexicographically.
                * inner: use intersection of keys from both frames, similar to a SQL inner
                  join; preserve the order of the left keys.

            on:
                Column join on. It must be found in both DataFrames. Either on or left_on + right_on
                must be passed in.
            left_on:
                Column join on in the left DataFrame. Either on or left_on + right_on
                must be passed in.
            right_on:
                Column join on in the right DataFrame. Either on or left_on + right_on
                must be passed in.
            sort:
                Default False. Sort the join keys lexicographically in the
                result DataFrame. If False, the order of the join keys depends
                on the join type (how keyword).
            suffixes:
                Default ``("_x", "_y")``. A length-2 sequence where each
                element is optionally a string indicating the suffix to add to
                overlapping column names in `left` and `right` respectively.
                Pass a value of `None` instead of a string to indicate that the
                column name from `left` or `right` should be left as-is, with
                no suffix. At least one of the values must not be None.

        Returns:
            A DataFrame of the two merged objects.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # ndarray-like stats methods

    def any(self, *, bool_only: bool = False):
        """
        Return whether any element is True, potentially over an axis.

        Returns False unless there is at least one element within a series or
        along a Dataframe axis that is True or equivalent (e.g. non-zero or
        non-empty).

        Args:
            bool_only:
                Include only boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def all(self, *, bool_only: bool = False):
        """
        Return whether all elements are True, potentially over an axis.

        Returns True unless there at least one element within a series or
        along a Dataframe axis that is False or equivalent (e.g. zero or
        empty).

        Args:
            bool_only:
                Include only boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def prod(self, *, numeric_only: bool = False):
        """
        Return the product of the values over the requested axis.

        Args:
            numeric_only:
                Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def min(self, *, numeric_only: bool = False):
        """Return the minimum of the values over the requested axis.

        If you want the *index* of the minimum, use ``idxmin``. This is the
        equivalent of the ``numpy.ndarray`` method ``argmin``.

        Args:
            numeric_only:
                Default False. Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def max(self, *, numeric_only: bool = False):
        """Return the maximum of the values over the requested axis.

        If you want the *index* of the maximum, use ``idxmax``. This is
        the equivalent of the ``numpy.ndarray`` method ``argmax``.

        Args:
            numeric_only:
                Default False. Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def sum(self, *, numeric_only: bool = False):
        """Return the sum of the values over the requested axis.

        This is equivalent to the method ``numpy.sum``.

        Args:
            numeric_only:
                Default False. Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def mean(self, *, numeric_only: bool = False):
        """Return the mean of the values over the requested axis.

        Args:
            numeric_only:
                Default False. Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def var(self, *, numeric_only: bool = False):
        """Return unbiased variance over requested axis.

        Normalized by N-1 by default.

        Args:
            numeric_only:
                Default False. Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def std(self, *, numeric_only: bool = False):
        """Return sample standard deviation over requested axis.

        Normalized by N-1 by default.

        Args:
            numeric_only:
                Default False. Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def count(self, *, numeric_only: bool = False):
        """
        Count non-NA cells for each column or row.

        The values `None`, `NaN`, `NaT`, and optionally `numpy.inf` (depending
        on `pandas.options.mode.use_inf_as_na`) are considered NA.

        Args:
            numeric_only : bool, default False
                Include only `float`, `int` or `boolean` data.

        Returns:
            For each column/row the number of non-NA/null entries.
            If `level` is specified returns a `DataFrame`.
        """
        raise NotImplementedError("abstract method")

    def nunique(self):
        """
        Count number of distinct elements in specified axis.

        Return Series with number of distinct elements.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")

    def cummin(self) -> DataFrame:
        """Return cumulative minimum over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative minimum.

        Returns:
            Return cumulative minimum of DataFrame.
        """
        raise NotImplementedError("abstract method")

    def cummax(self) -> DataFrame:
        """Return cumulative maximum over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative maximum.

        Returns:
            Return cumulative maximum of DataFrame.
        """
        raise NotImplementedError("abstract method")

    def cumsum(self) -> DataFrame:
        """Return cumulative sum over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative sum.

        Returns:
            Return cumulative sum of DataFrame.
        """
        raise NotImplementedError("abstract method")

    def cumprod(self) -> DataFrame:
        """Return cumulative product over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative product.

        Returns:
            Return cumulative product of DataFrame.
        """
        raise NotImplementedError("abstract method")

    # ----------------------------------------------------------------------
    # Add index and columns

    @property
    def index(self):
        """The index (row labels) of the DataFrame.

        The index of a DataFrame is a series of labels that identify each row.
        The labels can be integers, strings, or any other hashable type. The
        index is used for label-based access and alignment, and can be accessed
        or modified using this attribute.

        Returns:
            The index labels of the DataFrame.
        """
        raise NotImplementedError("abstract method")

    @property
    def columns(self):
        "The column labels of the DataFrame."
        raise NotImplementedError("abstract method")

    def value_counts(
        self,
        subset=None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ):
        """
        Return a Series containing counts of unique rows in the DataFrame.

        Args:
            subset : label or list of labels, optional
                Columns to use when counting unique combinations.
            normalize : bool, default False
                Return proportions rather than frequencies.
            sort : bool, default True
                Sort by frequencies.
            ascending : bool, default False
                Sort in ascending order.
            dropna : bool, default True
                Don’t include counts of rows that contain NA values.

        Returns:
            Series
        """
        raise NotImplementedError("abstract method")
