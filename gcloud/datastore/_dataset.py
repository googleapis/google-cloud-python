"""Needs module docstring."""


class _Dataset(object):
    """Needs class docstring."""

    def __init__(self, id, connection=None):
        self._connection = connection
        self._id = id

    def connection(self):
        """Needs method docstring."""
        return self._connection

    def id(self):
        """Needs method docstring."""
        return self._id
