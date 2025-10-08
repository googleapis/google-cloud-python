# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/_config/config.py
import contextlib
import operator


class option_context(contextlib.ContextDecorator):
    """
    Context manager to temporarily set thread-local options in the `with`
    statement context.

    You need to invoke as ``option_context(pat, val, [(pat, val), ...])``.

    .. note::

        `"bigquery"` options can't be changed on a running session. Setting any
        of these options creates a new thread-local session that only lives for
        the lifetime of the context manager.

    **Examples:**

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
        # Avoid problems with circular imports.
        import bigframes._config

        self.undo = [
            (pat, operator.attrgetter(pat)(bigframes._config.options))
            for pat, _ in self.ops
            # Don't try to undo changes to bigquery options. We're starting and
            # closing a new thread-local session if those are set.
            if not pat.startswith("bigquery.")
        ]

        for pat, val in self.ops:
            self._set_option(pat, val)

    def __exit__(self, *args) -> None:
        # Avoid problems with circular imports.
        import bigframes._config
        import bigframes.core.global_session

        if self.undo:
            for pat, val in self.undo:
                self._set_option(pat, val)

        # TODO(tswast): What to do if someone nests several context managers
        # with separate "bigquery" options? We might need a "stack" of
        # sessions if we allow that.
        if bigframes._config.options.is_bigquery_thread_local:
            bigframes.core.global_session.close_session()

            # Reset bigquery_options so that we're no longer thread-local.
            bigframes._config.options._local.bigquery_options = None

    def _set_option(self, pat, val):
        # Avoid problems with circular imports.
        import bigframes._config

        root, attr = pat.rsplit(".", 1)

        # We are now using a thread-specific session.
        if root == "bigquery":
            bigframes._config.options._init_bigquery_thread_local()

        parent = operator.attrgetter(root)(bigframes._config.options)
        setattr(parent, attr, val)
