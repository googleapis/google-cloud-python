# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/window/rolling.py
"""
Provide a generic structure to support window functions,
similar to how we have a Groupby object.
"""


class Window:
    """Provide window calculations."""

    def count(self):
        """Calculate the window count of non-NULL observations."""
        raise NotImplementedError("abstract method")

    def sum(self):
        """Calculate the weighted window sum."""
        raise NotImplementedError("abstract method")

    def mean(self):
        """Calculate the weighted window mean."""
        raise NotImplementedError("abstract method")

    def var(self):
        """Calculate the weighted window variance."""
        raise NotImplementedError("abstract method")

    def std(self):
        """Calculate the weighted window standard deviation."""
        raise NotImplementedError("abstract method")

    def max(self):
        """Calculate the weighted window maximum."""
        raise NotImplementedError("abstract method")

    def min(self):
        """Calculate the weighted window minimum."""
        raise NotImplementedError("abstract method")
