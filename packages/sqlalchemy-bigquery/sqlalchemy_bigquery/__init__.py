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

from .version import __version__  # noqa

from .base import BigQueryDialect, dialect  # noqa
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

__all__ = [
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
except ImportError:
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
