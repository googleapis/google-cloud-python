# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/_config/config.py
import contextlib
import operator

import bigframes


class option_context(contextlib.ContextDecorator):
    """
    Context manager to temporarily set options in the `with` statement context.

    You need to invoke as ``option_context(pat, val, [(pat, val), ...])``.

    Examples
    --------
    >>> import bigframes
    >>> with bigframes.option_context('display.max_rows', 10, 'display.max_columns', 5):
    ...     pass
    """

    def __init__(self, *args) -> None:
        if len(args) % 2 != 0 or len(args) < 2:
            raise ValueError(
                "Need to invoke as option_context(pat, val, [(pat, val), ...])."
            )

        self.ops = list(zip(args[::2], args[1::2]))

    def __enter__(self) -> None:
        self.undo = [
            (pat, operator.attrgetter(pat)(bigframes.options)) for pat, val in self.ops
        ]

        for pat, val in self.ops:
            self._set_option(pat, val)

    def __exit__(self, *args) -> None:
        if self.undo:
            for pat, val in self.undo:
                self._set_option(pat, val)

    def _set_option(self, pat, val):
        root, attr = pat.rsplit(".", 1)
        parent = operator.attrgetter(root)(bigframes.options)
        setattr(parent, attr, val)
