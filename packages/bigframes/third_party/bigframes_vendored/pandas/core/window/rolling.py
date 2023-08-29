# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/window/rolling.py
"""
Provide a generic structure to support window functions,
similar to how we have a Groupby object.
"""

from bigframes import constants


class Window:
    """Provide window calculations."""

    def count(self):
        """Calculate the window count of non-NULL observations."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sum(self):
        """Calculate the weighted window sum."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mean(self):
        """Calculate the weighted window mean."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def var(self):
        """Calculate the weighted window variance."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def std(self):
        """Calculate the weighted window standard deviation."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(self):
        """Calculate the weighted window maximum."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(self):
        """Calculate the weighted window minimum."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
