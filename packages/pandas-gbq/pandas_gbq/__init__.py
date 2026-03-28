# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import logging
import warnings

from pandas_gbq import version as pandas_gbq_version
from pandas_gbq.contexts import Context, context
from pandas_gbq.core.sample import sample

from . import _versions_helpers
from .gbq import read_gbq, to_gbq  # noqa

sys_major, sys_minor, sys_micro = _versions_helpers.extract_runtime_version()
if sys_major == 3 and sys_minor < 9:
    warnings.warn(
        "pandas-gbq no longer supports Python versions older than 3.9. "
        "Your Python version is "
        f"{sys_major}.{sys_minor}.{sys_micro}. Please update "
        "to Python 3.9 or newer to ensure ongoing support. For more details, "
        "see: https://cloud.google.com/python/docs/supported-python-versions",
        FutureWarning,
    )

logger = logging.Logger(__name__)

__version__ = pandas_gbq_version.__version__

__all__ = [
    "__version__",
    "to_gbq",
    "read_gbq",
    "Context",
    "context",
    "sample",
]
