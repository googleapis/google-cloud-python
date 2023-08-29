# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexing.py

from bigframes import constants


class IndexingMixin:
    """
    Mixin for adding .loc/.iloc/.at/.iat to Dataframes and Series.
    """

    @property
    def iloc(self):
        """Purely integer-location based indexing for selection by position.

        ``.iloc[]`` is primarily integer position based (from ``0`` to
        ``length-1`` of the axis), but may also be used with a boolean
        array.

        Allowed inputs are:

        - **Not supported yet** An integer, e.g. ``5``.
        - **Not supported yet** A list or array of integers, e.g. ``[4, 3, 0]``.
        - A slice object with ints, e.g. ``1:7``.
        - **Not supported yet** A boolean array.
        - **Not supported yet** A ``callable`` function with one argument (the
          calling Series or DataFrame) that returns valid output for
          indexing (one of the above). This is useful in method chains, when you
          don't have a reference to the calling object, but would like to base
          your selection on some value.
        - **Not supported yet** A tuple of row and column indexes. The tuple
          elements consist of one of the above inputs, e.g. ``(0, 1)``.

        ``.iloc`` will raise ``IndexError`` if a requested indexer is
        out-of-bounds, except *slice* indexers which allow out-of-bounds
        indexing (this conforms with python/numpy *slice* semantics).
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def loc(self):
        """Access a group of rows and columns by label(s) or a boolean array.

        ``.loc[]`` is primarily label based, but may also be used with a
        boolean array.

        Allowed inputs are:

        - A single label, e.g. ``5`` or ``'a'``, (note
          that ``5`` is interpreted as a *label* of the index, and **never** as
          an integer position along the index).
        - A list of labels, e.g. ``['a', 'b', 'c']``.
        - A boolean series of the same length as the axis being sliced,
          e.g. ``[True, False, True]``.
        - An alignable Index. The index of the returned
          selection will be the input.
        - **Not supported yet** An alignable boolean Series. The index of the key will be aligned before
          masking.
        - **Not supported yet** A slice object with labels, e.g. ``'a':'f'``.
          Note: contrary to usual python slices, **both** the start and the stop are included.
        - **Not supported yet** A ``callable`` function with one argument (the
          calling Series or DataFrame) that returns valid output for indexing
          (one of the above).

        Raises:
            NotImplementError: if the inputs are not supported.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
