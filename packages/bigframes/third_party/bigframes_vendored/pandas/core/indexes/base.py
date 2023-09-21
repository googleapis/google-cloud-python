# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexes/base.py
from __future__ import annotations

from bigframes import constants


class Index:
    """Immutable sequence used for indexing and alignment.

    The basic object storing axis labels for all objects.
    """

    @property
    def name(self):
        """Returns Index name."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def values(self):
        """Return an array representing the data in the Index."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def shape(self):
        """
        Return a tuple of the shape of the underlying data.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def nlevels(self) -> int:
        """Number of levels."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_unique(self) -> bool:
        """Return if the index has unique values."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def has_duplicates(self) -> bool:
        """Check if the Index has duplicate values."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtype(self):
        """Return the dtype object of the underlying data."""

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtypes(self):
        """Return the dtypes as a Series for the underlying MultiIndex."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def astype(self, dtype):
        """Create an Index with values cast to dtypes.

        The class of a new Index is determined by dtype. When conversion is
        impossible, a TypeError exception is raised.

        Args:
            dtype (numpy dtype or pandas type):

        Returns:
            Index: Index with values cast to specified dtype.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def all(self) -> bool:
        """Return whether all elements are Truthy.

        Returns:
            bool: A single element array-like may be converted to bool.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def any(self) -> bool:
        """Return whether any element is Truthy.

        Returns:
            bool: A single element array-like may be converted to bool.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(self):
        """Return the minimum value of the Index.

        Returns:
            scalar: Minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(self):
        """Return the maximum value of the Index.

        Returns:
            scalar: Maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self) -> int:
        """Return number of unique elements in the object.

        Excludes NA values by default.

        Returns:
            int
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def fillna(self, value) -> Index:
        """
        Fill NA/NaN values with the specified value.

        Args:
            value (scalar):
                Scalar value to use to fill holes (e.g. 0).
                This value cannot be a list-likes.

        Returns:
            Index
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename(self, name) -> Index:
        """
        Alter Index or MultiIndex name.

        Able to set new names without level. Defaults to returning new index.
        Length of names must match number of levels in MultiIndex.

        Args:
            name (label or list of labels):
                Name(s) to set.

        Returns:
            Index: The same type as the caller.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop(self, labels) -> Index:
        """
        Make new Index with passed list of labels deleted.

        Args:
            labels (array-like or scalar):

        Returns:
            Index: Will be same type as self
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_numpy(self, dtype):
        """
        A NumPy ndarray representing the values in this Series or Index.

        Args:
            dtype:
                The dtype to pass to :meth:`numpy.asarray`.
            **kwargs:
                Additional keywords passed through to the ``to_numpy`` method
                of the underlying array (for extension arrays).

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
