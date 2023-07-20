class StringMethods:
    """
    Vectorized string functions for Series and Index.

    NAs stay NA unless handled otherwise by a particular method.
    Patterned after Python's string methods, with some inspiration from
    R's stringr package.
    """

    def find(self, sub, start: int = 0, end=None):
        """Return lowest indexes in each strings in the Series/Index.

        Each of returned indexes corresponds to the position where the
        substring is fully contained between [start:end]. Return -1 on
        failure. Equivalent to standard :meth:`str.find`.

        Args:
            sub:
                Substring being searched.
            start:
                Left edge index.
            end:
                Right edge index.

        Returns:
            Series or Index of int.
        """

        raise NotImplementedError("abstract method")

    def len(self):
        """Compute the length of each element in the Series/Index.

        The element may be a sequence (such as a string, tuple or list) or a collection
        (such as a dictionary).

        Returns:
            Series or Index of int
            A Series or Index of integer values indicating the length of each
            element in the Series or Index.
        """

        raise NotImplementedError("abstract method")

    def lower(self):
        """Convert strings in the Series/Index to lowercase.

        Equivalent to :meth:`str.lower`.

        Returns:
            Series or Index of object
        """

        raise NotImplementedError("abstract method")

    def slice(self, start=None, stop=None):
        """Slice substrings from each element in the Series or Index.

        Args:
            start : int, optional
                Start position for slice operation.
            stop : int, optional
                Stop position for slice operation.
            step : int, optional
                Step size for slice operation.

        Returns:
            Series or Index of object
                Series or Index from sliced substring from original string object.
        """

        raise NotImplementedError("abstract method")

    def strip(self):
        """Remove leading and trailing characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from left and right sides.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.strip`.

        Returns:
            Series or Index of object
        """

        raise NotImplementedError("abstract method")

    def upper(self):
        """Convert strings in the Series/Index to uppercase.

        Equivalent to :meth:`str.upper`.

        Returns:
            Series or Index of object
        """

        raise NotImplementedError("abstract method")

    def isnumeric(self):
        """Check whether all characters in each string are numeric.

        This is equivalent to running the Python string method
        :meth:`str.isnumeric` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            Series or Index of bool
                Series or Index of boolean values with the same length as the original
                Series/Index.
        """

        raise NotImplementedError("abstract method")

    def rstrip(self):
        """Remove trailing characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from right side.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.rstrip`.

        Returns:
            Series or Index of object
        """

        raise NotImplementedError("abstract method")

    def lstrip(self):
        """Remove leading characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from left side.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.lstrip`.

        Returns:
            Series or Index of object`
        """

        raise NotImplementedError("abstract method")

    def repeat(self, repeats: int):
        """Duplicate each string in the Series or Index.

        Args:
            repeats : int or sequence of int
                Same value for all (int) or different value per (sequence).

        Returns:
            Series or pandas.Index
                Series or Index of repeated string objects specified by
                input parameter repeats.
        """

        raise NotImplementedError("abstract method")

    def capitalize(self):
        """Convert strings in the Series/Index to be capitalized.

        Equivalent to :meth:`str.capitalize`.

        Returns:
            Series or Index of object
        """

        raise NotImplementedError("abstract method")

    def cat(self, others, *, join):
        """Concatenate strings in the Series/Index with given separator.

        If `others` is specified, this function concatenates the Series/Index
        and elements of `others` element-wise.

        Args:
            others : Series

            join : {'left', 'outer'}, default 'left'
                Determines the join-style between the calling Series and any
                Series in `others` (objects without an index need
                to match the length of the calling Series). To disable
                alignment, use `.values` on any Series/Index/DataFrame in `others`.

        Returns:
            Series
        """

        raise NotImplementedError("abstract method")
