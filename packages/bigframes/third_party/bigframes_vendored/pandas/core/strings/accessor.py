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

    def __getitem__(self, key: typing.Union[int, slice]):
        """
        Index or slice string or list in the Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['Alice', 'Bob', 'Charlie'])
            >>> s.str[0]
            0     A
            1     B
            2     C
            dtype: string

            >>> s.str[0:3]
            0     Ali
            1     Bob
            2     Cha
            dtype: string

        Args:
            key (int | slice):
                Index or slice of indices to access from each string or list.

        Returns:
            bigframes.series.Series: The list at requested index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def extract(self, pat: str, flags: int = 0):
        """
        Extract capture groups in the regex `pat` as columns in a DataFrame.

        For each subject string in the Series, extract groups from the
        first match of regular expression `pat`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        A pattern with two groups will return a DataFrame with two columns.
        Non-matches will be `NaN`.

            >>> s = bpd.Series(['a1', 'b2', 'c3'])
            >>> s.str.extract(r'([ab])(\\d)')
                  0     1
            0     a     1
            1     b     2
            2  <NA>  <NA>
            <BLANKLINE>
            [3 rows x 2 columns]

        Named groups will become column names in the result.

            >>> s.str.extract(r'(?P<letter>[ab])(?P<digit>\\d)')
              letter digit
            0      a     1
            1      b     2
            2   <NA>  <NA>
            <BLANKLINE>
            [3 rows x 2 columns]

        A pattern with one group will return a DataFrame with one column.

            >>> s.str.extract(r'[ab](\\d)')
                  0
            0     1
            1     2
            2  <NA>
            <BLANKLINE>
            [3 rows x 1 columns]

        Args:
            pat (str):
                Regular expression pattern with capturing groups.
            flags (int, default 0 (no flags)):
                Flags from the ``re`` module, e.g. ``re.IGNORECASE``, that
                modify regular expression matching for things like case,
                spaces, etc. For more details, see :mod:`re`.

        Returns:
            bigframes.dataframe.DataFrame:
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(["cow_", "duck_", "do_ve"])
            >>> ser.str.find("_")
            0    3
            1    4
            2    2
            dtype: Int64

        Args:
            sub (str):
                Substring being searched.
            start (int, default 0):
                Left edge index.
            end (int, default None):
                Right edge index.

        Returns:
            bigframes.series.Series: Series with lowest indexes in each strings.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def len(self):
        """Compute the length of each element in the Series/Index.

        The element may be a sequence (such as a string, tuple or list) or a collection
        (such as a dictionary).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Returns the length (number of characters) in a string.

            >>> s = bpd.Series(['dog', '', bpd.NA])
            >>> s.str.len()
            0       3
            1       0
            2    <NA>
            dtype: Int64

        Returns:
            bigframes.series.Series: A Series or Index of integer values indicating
                the length of each element in the Series or Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lower(self):
        """Convert strings in the Series/Index to lowercase.

        Equivalent to :meth:`str.lower`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['lower',
            ...                 'CAPITALS',
            ...                 'this is a sentence',
            ...                 'SwApCaSe'])
            >>> s.str.lower()
            0                 lower
            1              capitals
            2    this is a sentence
            3              swapcase
            dtype: string

        Returns:
            bigframes.series.Series: Series with lowercase.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def slice(self, start=None, stop=None):
        """Slice substrings from each element in the Series or Index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["koala", "dog", "chameleon"])
            >>> s
            0        koala
            1          dog
            2    chameleon
            dtype: string

            >>> s.str.slice(start=1)
            0        oala
            1          og
            2    hameleon
            dtype: string

            >>> s.str.slice(stop=2)
            0    ko
            1    do
            2    ch
            dtype: string

            >>> s.str.slice(start=2, stop=5)
            0    ala
            1      g
            2    ame
            dtype: string

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

    def strip(self, to_strip: typing.Optional[str] = None):
        """Remove leading and trailing characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from left and right sides.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.strip`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([
            ...     '1. Ant.',
            ...     '  2. Bee? ',
            ...     '\\t3. Cat!\\n',
            ...     bpd.NA,
            ... ])
            >>> s.str.strip()
            0    1. Ant.
            1    2. Bee?
            2    3. Cat!
            3       <NA>
            dtype: string

            >>> s.str.strip('123.!? \\n\\t')
            0       Ant
            1       Bee
            2       Cat
            3       <NA>
            dtype: string

        Args:
            to_strip (str, default None):
                Specifying the set of characters to be removed. All combinations
                of this set of characters will be stripped. If None then
                whitespaces are removed.

        Returns:
            bigframes.series.Series: Series or Index without leading
                and trailing characters.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def upper(self):
        """Convert strings in the Series/Index to uppercase.

        Equivalent to :meth:`str.upper`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['lower',
            ...                 'CAPITALS',
            ...                 'this is a sentence',
            ...                 'SwApCaSe'])
            >>> s.str.upper()
            0                 LOWER
            1              CAPITALS
            2    THIS IS A SENTENCE
            3              SWAPCASE
            dtype: string

        Returns:
            bigframes.series.Series: Series with uppercase strings.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isnumeric(self):
        """Check whether all characters in each string are numeric.

        This is equivalent to running the Python string method
        :meth:`str.isnumeric` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s1 = bpd.Series(['one', 'one1', '1', ''])
            >>> s1.str.isnumeric()
            0    False
            1    False
            2     True
            3    False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s1 = bpd.Series(['one', 'one1', '1', ''])
            >>> s1.str.isalpha()
            0     True
            1    False
            2    False
            3    False
            dtype: boolean

        Returns:
            bigframes.series.Series: Series with the same length as the originalSeries/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isdigit(self):
        """Check whether all characters in each string are digits.

        This is equivalent to running the Python string method
        :meth:`str.isdigit` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['23', '1a', '1/5', ''])
            >>> s.str.isdigit()
            0     True
            1    False
            2    False
            3    False
            dtype: boolean

        Returns:
            bigframes.series.Series: Series with the same length as the originalSeries/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isalnum(self):
        """Check whether all characters in each string are alphanumeric.

        This is equivalent to running the Python string method
        :meth:`str.isalnum` for each element of the Series/Index. If a string
        has zero characters, ``False`` is returned for that check.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s1 = bpd.Series(['one', 'one1', '1', ''])
            >>> s1.str.isalnum()
            0     True
            1     True
            2     True
            3    False
            dtype: boolean

        Note that checks against characters mixed with any additional
        punctuation or whitespace will evaluate to false for an alphanumeric
        check.

            >>> s2 = bpd.Series(['A B', '1.5', '3,000'])
            >>> s2.str.isalnum()
            0    False
            1    False
            2    False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([' ', '\\t\\r\\n ', ''])
            >>> s.str.isspace()
            0     True
            1     True
            2    False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['leopard', 'Golden Eagle', 'SNAKE', ''])
            >>> s.str.islower()
            0     True
            1    False
            2    False
            3    False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['leopard', 'Golden Eagle', 'SNAKE', ''])
            >>> s.str.isupper()
            0    False
            1    False
            2     True
            3    False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        The `isdecimal` method checks for characters used to form numbers in
        base 10.

            >>> s = bpd.Series(['23', '³', '⅕', ''])
            >>> s.str.isdecimal()
            0     True
            1    False
            2    False
            3    False
            dtype: boolean

        Returns:
            bigframes.series.Series: Series or Index of boolean values with the
                same length as the original Series/Index.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rstrip(self, to_strip: typing.Optional[str] = None):
        r"""Remove trailing characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from right side.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.rstrip`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['Ant', '  Bee ', '\tCat\n', bpd.NA])
            >>> s.str.rstrip()
            0      Ant
            1      Bee
            2    \tCat
            3     <NA>
            dtype: string

        Args:
            to_strip (str, default None):
                Specifying the set of characters to be removed. All combinations
                of this set of characters will be stripped. If None then
                whitespaces are removed.

        Returns:
            bigframes.series.Series: Series without trailing characters.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lstrip(self, to_strip: typing.Optional[str] = None):
        r"""Remove leading characters.

        Strip whitespaces (including newlines) or a set of specified characters
        from each string in the Series/Index from left side.
        Replaces any non-strings in Series with NaNs.
        Equivalent to :meth:`str.lstrip`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['Ant', '  Bee ', '\tCat\n', bpd.NA])
            >>> s.str.lstrip()
            0      Ant
            1     Bee
            2    Cat\n
            3     <NA>
            dtype: string

        Args:
            to_strip (str, default None):
                Specifying the set of characters to be removed. All combinations
                of this set of characters will be stripped. If None then
                whitespaces are removed.

        Returns:
            bigframes.series.Series: Series without leading characters.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def repeat(self, repeats: int):
        """Duplicate each string in the Series or Index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['a', 'b', 'c'])
            >>> s
            0    a
            1    b
            2    c
            dtype: string

            >>> s.str.repeat(repeats=2)
            0    aa
            1    bb
            2    cc
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['lower',
            ...                 'CAPITALS',
            ...                 'this is a sentence',
            ...                 'SwApCaSe'])
            >>> s.str.capitalize()
            0                 Lower
            1              Capitals
            2    This is a sentence
            3              Swapcase
            dtype: string

        Returns:
            bigframes.series.Series: Series with captitalized strings.
        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cat(self, others, *, join):
        """Concatenate strings in the Series/Index with given separator.

        If `others` is specified, this function concatenates the Series/Index
        and elements of `others` element-wise.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can concatenate each string in a Series to another string.

            >>> s = bpd.Series(['Jane', 'John'])
            >>> s.str.cat(" Doe")
            0    Jane Doe
            1    John Doe
            dtype: string

        You can concatenate another Series. By default left join is performed to
        align the corresponding elements.

            >>> s.str.cat(bpd.Series([" Doe", " Foe", " Roe"]))
            0    Jane Doe
            1    John Foe
            dtype: string

            >>> s.str.cat(bpd.Series([" Doe", " Foe", " Roe"], index=[2, 0, 1]))
            0    Jane Foe
            1    John Roe
            dtype: string

        You can enforce an outer join.

            >>> s.str.cat(bpd.Series([" Doe", " Foe", " Roe"]), join="outer")
            0    Jane Doe
            1    John Foe
            2        <NA>
            dtype: string

        Args:
            others (str or Series):
                A string or a Series of strings.

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Returning a Series of booleans using only a literal pattern.

            >>> s1 = bpd.Series(['Mouse', 'dog', 'house and parrot', '23', None])
            >>> s1.str.contains('og')
            0    False
            1     True
            2    False
            3    False
            4     <NA>
            dtype: boolean

        Specifying case sensitivity using `case`.

            >>> s1.str.contains('oG', case=True)
            0    False
            1    False
            2    False
            3    False
            4     <NA>
            dtype: boolean

        Returning 'house' or 'dog' when either expression occurs in a string.

            >>> s1.str.contains('house|dog', regex=True)
            0    False
            1     True
            2     True
            3    False
            4     <NA>
            dtype: boolean

        Ignoring case sensitivity using `flags` with regex.

            >>> import re
            >>> s1.str.contains('PARROT', flags=re.IGNORECASE, regex=True)
            0    False
            1    False
            2     True
            3    False
            4     <NA>
            dtype: boolean

        Returning any digit using regular expression.

            >>> s1.str.contains('\\d', regex=True)
            0    False
            1    False
            2    False
            3     True
            4     <NA>
            dtype: boolean

        Ensure `pat` is a not a literal pattern when `regex` is set to True.
        Note in the following example one might expect only *s2[1]* and *s2[3]*
        to return `True`. However, '.0' as a regex matches any character
        followed by a 0.

            >>> s2 = bpd.Series(['40', '40.0', '41', '41.0', '35'])
            >>> s2.str.contains('.0', regex=True)
            0     True
            1     True
            2    False
            3     True
            4    False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        When *pat* is a string and *regex* is True, the given *pat* is compiled
        as a regex. When *repl* is a string, it replaces matching regex patterns
        as with `re.sub()`. NaN value(s) in the Series are left as is:

            >>> s = bpd.Series(['foo', 'fuz', bpd.NA])
            >>> s.str.replace('f.', 'ba', regex=True)
            0     bao
            1     baz
            2    <NA>
            dtype: string

        When *pat* is a string and *regex* is False, every *pat* is replaced
        with *repl* as with `str.replace()`:

            >>> s = bpd.Series(['f.o', 'fuz', bpd.NA])
            >>> s.str.replace('f.', 'ba', regex=False)
            0     bao
            1     fuz
            2    <NA>
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['bat', 'Bear', 'caT', bpd.NA])
            >>> s
            0     bat
            1    Bear
            2     caT
            3    <NA>
            dtype: string

            >>> s.str.startswith('b')
            0     True
            1    False
            2    False
            3     <NA>
            dtype: boolean

            >>> s.str.startswith(('b', 'B'))
            0     True
            1     True
            2    False
            3     <NA>
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['bat', 'bear', 'caT', bpd.NA])
            >>> s
            0     bat
            1    bear
            2     caT
            3    <NA>
            dtype: string

            >>> s.str.endswith('t')
            0     True
            1    False
            2    False
            3     <NA>
            dtype: boolean

            >>> s.str.endswith(('t', 'T'))
            0     True
            1    False
            2     True
            3     <NA>
            dtype: boolean

        Args:
            pat (str, tuple[str, ...]):
                Character sequence or tuple of strings. Regular expressions are not
                accepted.

        Returns:
            bigframes.series.Series: A Series of booleans indicating whether the given
                pattern matches the end of each string element.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def split(
        self,
        pat: str = " ",
        regex: typing.Union[bool, None] = None,
    ):
        """
        Split strings around given separator/delimiter.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(
            ...     [
            ...         "a regular sentence",
            ...         "https://docs.python.org/index.html",
            ...         np.nan
            ...     ]
            ... )
            >>> s.str.split()
            0                ['a' 'regular' 'sentence']
            1    ['https://docs.python.org/index.html']
            2                                        []
            dtype: list<item: string>[pyarrow]

            The pat parameter can be used to split by other characters.

            >>> s.str.split("//", regex=False)
            0                     ['a regular sentence']
            1    ['https:' 'docs.python.org/index.html']
            2                                         []
            dtype: list<item: string>[pyarrow]

        Args:
            pat (str, default " "):
                String to split on. If not specified, split on whitespace.
            regex (bool, default None):
                Determines if the passed-in pattern is a regular expression. Regular
                expressions aren't currently supported. Please set `regex=False` when
                `pat` length is not 1.

        Returns:
            bigframes.series.Series: Type matches caller.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def match(self, pat: str, case: bool = True, flags: int = 0):
        """
        Determine if each string starts with a match of a regular expression.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(["horse", "eagle", "donkey"])
            >>> ser.str.match("e")
            0   False
            1   True
            2   False
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(["cat", "duck", "dove"])
            >>> ser.str.fullmatch(r'd.+')
            0    False
            1     True
            2     True
            dtype: boolean

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["apple", "banana", "fig"])
            >>> s.str.get(3)
            0       l
            1       a
            2    <NA>
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["caribou", "tiger"])
            >>> s
            0    caribou
            1      tiger
            dtype: string

            >>> s.str.pad(width=10)
            0       caribou
            1         tiger
            dtype: string

            >>> s.str.pad(width=10, side='right', fillchar='-')
            0    caribou---
            1    tiger-----
            dtype: string

            >>> s.str.pad(width=10, side='both', fillchar='-')
            0    -caribou--
            1    --tiger---
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(['dog', 'bird', 'mouse'])
            >>> ser.str.ljust(8, fillchar='.')
            0    dog.....
            1    bird....
            2    mouse...
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(['dog', 'bird', 'mouse'])
            >>> ser.str.rjust(8, fillchar='.')
            0    .....dog
            1    ....bird
            2    ...mouse
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['-1', '1', '1000', bpd.NA])
            >>> s
            0      -1
            1       1
            2    1000
            3    <NA>
            dtype: string

            >>> s.str.zfill(3)
            0     -01
            1     001
            2    1000
            3    <NA>
            dtype: string

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(['dog', 'bird', 'mouse'])
            >>> ser.str.center(8, fillchar='.')
            0    ..dog...
            1    ..bird..
            2    .mouse..
            dtype: string

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
