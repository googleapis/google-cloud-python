# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/__init__.py

"""Initialize Ibis module."""

from __future__ import annotations

__version__ = "9.2.0"

from typing import Any
import warnings

from bigframes_vendored.ibis import util
from bigframes_vendored.ibis.backends import BaseBackend
import bigframes_vendored.ibis.backends.bigquery as bigquery
from bigframes_vendored.ibis.common.exceptions import IbisError
from bigframes_vendored.ibis.config import options
from bigframes_vendored.ibis.expr import api
from bigframes_vendored.ibis.expr import types as ir
from bigframes_vendored.ibis.expr.api import *  # noqa: F403
from bigframes_vendored.ibis.expr.operations import udf

__all__ = [  # noqa: PLE0604
    "api",
    "ir",
    "udf",
    "util",
    "BaseBackend",
    "IbisError",
    "options",
    *api.__all__,
]

_KNOWN_BACKENDS = ["heavyai"]


def load_backend(name: str) -> BaseBackend:
    """Load backends in a lazy way with `ibis.<backend-name>`.

    This also registers the backend options.

    Examples
    --------
    >>> import ibis
    >>> con = ibis.sqlite.connect(...)

    When accessing the `sqlite` attribute of the `ibis` module, this function
    is called, and a backend with the `sqlite` name is tried to load from
    the `ibis.backends` entrypoints. If successful, the `ibis.sqlite`
    attribute is "cached", so this function is only called the first time.

    """
    backend = bigquery.Backend()
    # The first time a backend is loaded, we register its options, and we set
    # it as an attribute of `ibis`, so `__getattr__` is not called again for it
    backend.register_options()

    # We don't want to expose all the methods on an unconnected backend to the user.
    # In lieu of a full redesign, we create a proxy module and add only the methods
    # that are valid to call without a connect call. These are:
    #
    # - connect
    # - compile
    # - has_operation
    # - _from_url
    # - _to_sqlglot
    #
    # We also copy over the docstring from `do_connect` to the proxy `connect`
    # method, since that's where all the backend-specific kwargs are currently
    # documented. This is all admittedly gross, but it works and doesn't
    # require a backend redesign yet.

    def connect(*args, **kwargs):
        return backend.connect(*args, **kwargs)

    connect.__doc__ = backend.do_connect.__doc__
    connect.__wrapped__ = backend.do_connect
    connect.__module__ = f"bigframes_vendored.ibis.{name}"

    import types

    import bigframes_vendored.ibis

    proxy = types.ModuleType(f"bigframes_vendored.ibis.{name}")
    setattr(bigframes_vendored.ibis, name, proxy)
    proxy.connect = connect
    proxy.compile = backend.compile
    proxy.has_operation = backend.has_operation
    proxy.name = name
    proxy._from_url = backend._from_url
    proxy._to_sqlglot = backend._to_sqlglot
    # Add any additional methods that should be exposed at the top level
    for attr in getattr(backend, "_top_level_methods", ()):
        setattr(proxy, attr, getattr(backend, attr))

    return proxy


def __getattr__(name: str) -> Any:
    if name == "NA":
        warnings.warn(
            "The 'ibis.NA' constant is deprecated as of v9.1 and will be removed in a future "
            "version. Use 'ibis.null()' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return null()  # noqa: F405
    else:
        return load_backend(name)
