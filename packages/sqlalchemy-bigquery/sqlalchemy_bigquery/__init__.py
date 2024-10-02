# Copyright (c) 2017 The sqlalchemy-bigquery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
SQLAlchemy dialect for Google BigQuery
"""

import warnings

from .version import __version__

from .base import BigQueryDialect, dialect
from ._types import (
    ARRAY,
    BIGNUMERIC,
    BOOL,
    BOOLEAN,
    BYTES,
    DATE,
    DATETIME,
    FLOAT,
    FLOAT64,
    INT64,
    INTEGER,
    NUMERIC,
    RECORD,
    STRING,
    STRUCT,
    TIME,
    TIMESTAMP,
)

from . import _versions_helpers

sys_major, sys_minor, sys_micro = _versions_helpers.extract_runtime_version()
if sys_major == 3 and sys_minor in (7, 8):
    warnings.warn(
        "The python-bigquery library will stop supporting Python 3.7 "
        "and Python 3.8 in a future major release expected in Q4 2024. "
        f"Your Python version is {sys_major}.{sys_minor}.{sys_micro}. We "
        "recommend that you update soon to ensure ongoing support. For "
        "more details, see: [Google Cloud Client Libraries Supported Python Versions policy](https://cloud.google.com/python/docs/supported-python-versions)",
        PendingDeprecationWarning,
    )


__all__ = [
    "__version__",
    "dialect",
    "ARRAY",
    "BIGNUMERIC",
    "BigQueryDialect",
    "BOOL",
    "BOOLEAN",
    "BYTES",
    "DATE",
    "DATETIME",
    "FLOAT",
    "FLOAT64",
    "INT64",
    "INTEGER",
    "NUMERIC",
    "RECORD",
    "STRING",
    "STRUCT",
    "TIME",
    "TIMESTAMP",
]

try:
    from .geography import GEOGRAPHY, WKB, WKT  # noqa
except ImportError:  # pragma: NO COVER
    pass
else:
    __all__.extend(["GEOGRAPHY", "WKB", "WKT"])

try:
    import pybigquery  # noqa
except ImportError:
    pass
else:  # pragma: NO COVER
    import warnings

    warnings.warn(
        "Obsolete pybigquery is installed, which is likely to\n"
        "interfere with sqlalchemy_bigquery.\n"
        "pybigquery should be uninstalled.",
        stacklevel=2,
    )
