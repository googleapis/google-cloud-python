# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from pandas_gbq import version as pandas_gbq_version

from .gbq import Context, context, read_gbq, to_gbq  # noqa

__version__ = pandas_gbq_version.__version__

__all__ = [
    "__version__",
    "to_gbq",
    "read_gbq",
    "Context",
    "context",
]
