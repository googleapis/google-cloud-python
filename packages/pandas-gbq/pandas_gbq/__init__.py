# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import warnings

from pandas_gbq import version as pandas_gbq_version
from pandas_gbq.contexts import Context, context

from . import _versions_helpers
from .gbq import read_gbq, to_gbq  # noqa

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

__version__ = pandas_gbq_version.__version__

__all__ = [
    "__version__",
    "to_gbq",
    "read_gbq",
    "Context",
    "context",
]
