import re
import typing

from bigframes import constants


class StringMethods:
    """
    Vectorized string functions for Series and Index.

    NAs stay NA unless handled otherwise by a particular method.
    Patterned after Python's string methods, with some inspiration from
    R's stringr package.
    """

    def extract(self, pat: str, flags: int = 0):
        """
        Extract capture groups in the regex `pat` as columns in a DataFrame.

        For each subject string in the Series, extract groups from the
        first match of regular expression `pat`.

        Args:
            pat:
                Regular expression pattern with capturing groups.
            flags:
                Flags from the ``re`` module, e.g. ``re.IGNORECASE``, that
                modify regular expression matching for things like case,
                spaces, etc. For more details, see :mod:`re`.

        Returns:
            A DataFrame with one row for each subject string, and one
            column for each group. Any capture group names in regular
            expression pat will be used for column names; otherwise
            capture group numbers will be used.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def find(self, sub, start: int = 0, end=None):
        """Return lowest indexes in each strings in the Series/Index.

        Each of returned indexes corresponds to the position where the
        substring is fully contained between [start:end]. Return -1 on
        failure. Equivalent to standard :meth:`str.find`.

        Args:
            sub:
                Substring being searched.
            start (int, default 0):
                Left edge index.
            end (None):
                Right edge index.

        Returns:
            bigframes.series.Series: Series with lowest indexes in each strings.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def len(self):
        """Compute the length of each element in the Series/Index.

        The element may be a sequence (such as a string, tuple or list) or a collection
        (such as a dictionary).

        Returns:
            bigframes.series.Series: A Series or Index of integer values indicating
                the length of each element in the Series or Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lower(self):
        """Convert strings in the Series/Index to lowercase.

        Equivalent to :meth:`str.lower`.

        Returns:
            bigframes.series.Series: Series with lowercase.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def slice(self, start=None, stop=None):
        """Slice substrings from each element in the Series or Index.

        Args:
            start (int, optional):
                Start position for slice operation.
            stop (int, optional):
                Stop position for slice operation.
            step (int, optional):
                Step size for slice operation.

        Returns:
            bigframes.series.Series:: Series or Index from sliced
                substring from original string object.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def strip(self):
        """Remove leading and trailing characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from left and right sides.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.strip`.

        Returns:
            bigframes.series.Series: Series or Index without leading
                and trailing characters.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def upper(self):
        """Convert strings in the Series/Index to uppercase.

        Equivalent to :meth:`str.upper`.

        Returns:
            bigframes.series.Series: Series with uppercase strings.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isnumeric(self):
        """Check whether all characters in each string are numeric.

        This is equivalent to running the Python string method
        :meth:`str.isnumeric` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isalpha(self):
        """Check whether all characters in each string are alphabetic.

        This is equivalent to running the Python string method
        :meth:`str.isalpha` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series with the same length as the originalSeries/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isdigit(self):
        """Check whether all characters in each string are digits.

        This is equivalent to running the Python string method
        :meth:`str.isdigit` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series with the same length as the originalSeries/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isalnum(self):
        """Check whether all characters in each string are alphanumeric.

        This is equivalent to running the Python string method
        :meth:`str.isalnum` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isspace(self):
        """Check whether all characters in each string are whitespace.

        This is equivalent to running the Python string method
        :meth:`str.isspace` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def islower(self):
        """Check whether all characters in each string are lowercase.

        This is equivalent to running the Python string method
        :meth:`str.islower` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isupper(self):
        """Check whether all characters in each string are uppercase.

        This is equivalent to running the Python string method
        :meth:`str.isupper` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isdecimal(self):
        """Check whether all characters in each string are decimal.

        This is equivalent to running the Python string method
        :meth:`str.isdecimal` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rstrip(self):
        """Remove trailing characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from right side.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.rstrip`.

        Returns:
            bigframes.series.Series: Series without trailing characters.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lstrip(self):
        """Remove leading characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from left side.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.lstrip`.

        Returns:
            bigframes.series.Series: Series without leading characters.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def repeat(self, repeats: int):
        """Duplicate each string in the Series or Index.

        Args:
            repeats : int or sequence of int
                Same value for all (int) or different value per (sequence).

        Returns:
            bigframes.series.Series: Series or Index of repeated string
                objects specified by input parameter repeats.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def capitalize(self):
        """Convert strings in the Series/Index to be capitalized.

        Equivalent to :meth:`str.capitalize`.

        Returns:
            bigframes.series.Series: Series with captitalized strings.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cat(self, others, *, join):
        """Concatenate strings in the Series/Index with given separator.

        If `others` is specified, this function concatenates the Series/Index
        and elements of `others` element-wise.

        Args:
            others (Series):

            join ({'left', 'outer'}, default 'left'):
                Determines the join-style between the calling Series and any
                Series in `others` (objects without an index need
                to match the length of the calling Series). To disable
                alignment, use `.values` on any Series/Index/DataFrame in `others`.

        Returns:
            bigframes.series.Series: Series with concatenated strings.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def contains(self, pat, case: bool = True, flags: int = 0, *, regex: bool = True):
        """
        Test if pattern or regex is contained within a string of a Series or Index.

        Return boolean Series or Index based on whether a given pattern or regex is
        contained within a string of a Series or Index.

        Args:
            pat (str, re.Pattern):
                Character sequence or regular expression.
            case (bool, default True):
                If True, case sensitive.
            flags (int, default 0):
                Flags to pass through to the re module, e.g. re.IGNORECASE.
            regex (bool, default True):
                If True, assumes the pat is a regular expression.
                If False, treats the pat as a literal string.

        Returns:
            bigframes.series.Series: A Series or Index of boolean values indicating
                whether the given pattern is contained within the string of each
                element of the Series or Index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def replace(
        self,
        pat: typing.Union[str, re.Pattern],
        repl: str,
        *,
        case: typing.Optional[bool] = None,
        flags: int = 0,
        regex: bool = False,
    ):
        """
        Replace each occurrence of pattern/regex in the Series/Index.

        Equivalent to :meth:`str.replace` or :func:`re.sub`, depending on
        the regex value.

        Args:
            pat (str, re.Pattern):
                String can be a character sequence or regular expression.
            repl (str):
                Replacement string.
            case (default None):
                Determines if replace is case sensitive:

                - If True, case sensitive (the default if `pat` is a string)
                - Set to False for case insensitive
                - Cannot be set if `pat` is a compiled regex.
            flags (int, default 0):
                Regex module flags, e.g. re.IGNORECASE. Cannot be set if `pat` is a compiled
                regex.
            regex (bool: default False):
                Determines if the passed-in pattern is a regular expression:

                - If True, assumes the passed-in pattern is a regular expression.
                - If False, treats the pattern as a literal string
                - Cannot be set to False if `pat` is a compiled regex or `repl` is
                    a callable.

        Returns:
            bigframes.series.Series: A copy of the object with all matching occurrences
                of `pat` replaced by `repl`.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def startswith(
        self,
        pat: typing.Union[str, tuple[str, ...]],
    ):
        """
        Test if the start of each string element matches a pattern.

        Args:
            pat (str, tuple[str, ...]):
                Character sequence or tuple of strings. Regular expressions are not
                accepted.

        Returns:
            bigframes.series.Series: A Series of booleans indicating whether the given
                pattern matches the start of each string element.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def endswith(
        self,
        pat: typing.Union[str, tuple[str, ...]],
    ):
        """
        Test if the end of each string element matches a pattern.

        Args:
            pat (str, tuple[str, ...]):
                Character sequence or tuple of strings. Regular expressions are not
                accepted.

        Returns:
            bigframes.series.Series: A Series of booleans indicating whether the given
                pattern matches the end of each string element.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def match(self, pat: str, case: bool = True, flags: int = 0):
        """
        Determine if each string starts with a match of a regular expression.

        Args:
            pat (str):
                Character sequence or regular expression.
            case (bool):
                If True, case sensitive.
            flags (int, default 0):
                Regex module flags, e.g. re.IGNORECASE.

        Returns:
            bigframes.series.Series: Series of boolean values
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def fullmatch(self, pat: str, case: bool = True, flags: int = 0):
        """
        Determine if each string entirely matches a regular expression.

        Args:
            pat (str):
                Character sequence or regular expression.
            case (bool):
                If True, case sensitive.
            flags (int, default 0):
                Regex module flags, e.g. re.IGNORECASE.

        Returns:
            bigframes.series.Series: Series of boolean values
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def get(self, i: int):
        """
        Extract element from each component at specified position or with specified key.

        Extract element from lists, tuples, dict, or strings in each element in the
        Series/Index.

        Args:
            i (int):
                Position or key of element to extract.

        Returns:
            bigframes.series.Series: Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pad(
        self,
        width: int,
        side: typing.Literal["left", "right", "both"] = "left",
        fillchar: str = " ",
    ):
        """
        Pad strings in the Series/Index up to width.

        Args:
            width (int):
                Minimum width of resulting string; additional characters will be filled
                with character defined in `fillchar`.
            side ({'left', 'right', 'both'}, default 'left'):
                Side from which to fill resulting string.
            fillchar (str, default ' '):
                Additional character for filling, default is whitespace.

        Returns:
            bigframes.series.Series: Returns Series or Index with minimum number of char in object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ljust(
        self,
        width: int,
        fillchar: str = " ",
    ):
        """
        Pad right side of strings in the Series/Index up to width.

        Args:
            width (int):
                Minimum width of resulting string; additional characters will be filled
                with character defined in `fillchar`.
            fillchar (str, default ' '):
                Additional character for filling, default is whitespace.

        Returns:
            bigframes.series.Series: Returns Series or Index with minimum number of char in object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rjust(
        self,
        width: int,
        fillchar: str = " ",
    ):
        """
        Pad left side of strings in the Series/Index up to width.

        Args:
            width (int):
                Minimum width of resulting string; additional characters will be filled
                with character defined in `fillchar`.
            fillchar (str, default ' '):
                Additional character for filling, default is whitespace.

        Returns:
            bigframes.series.Series: Returns Series or Index with minimum number of char in object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def zfill(
        self,
        width: int,
    ):
        """
        Pad strings in the Series/Index by prepending '0' characters.

        Strings in the Series/Index are padded with '0' characters on the
        left of the string to reach a total string length  `width`. Strings
        in the Series/Index with length greater or equal to `width` are
        unchanged.

        Args:
            width (int):
                Minimum length of resulting string; strings with length less
                than `width` be prepended with '0' characters.

        Returns:
            bigframes.series.Series: Series of objects.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def center(
        self,
        width: int,
        fillchar: str = " ",
    ):
        """
        Pad left and right side of strings in the Series/Index.

        Equivalent to :meth:`str.center`.

        Args:
            width (int):
                Minimum width of resulting string; additional characters will be filled
                with character defined in `fillchar`.
            fillchar (str, default ' '):
                Additional character for filling, default is whitespace.

        Returns:
            bigframes.series.Series: Returns Series or Index with minimum number of char in object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
