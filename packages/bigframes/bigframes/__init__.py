# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""BigQuery DataFrames provides a DataFrame API scaled by the BigQuery engine."""

import warnings

# Suppress Python version support warnings from google-cloud libraries.
# These are particularly noisy in Colab which still uses Python 3.10.
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=".*Google will stop supporting.*Python.*",
)

from bigframes._config import option_context, options  # noqa: E402
from bigframes._config.bigquery_options import BigQueryOptions  # noqa: E402
from bigframes.core.global_session import (  # noqa: E402
    close_session,
    get_global_session,
)
import bigframes.enums as enums  # noqa: E402
import bigframes.exceptions as exceptions  # noqa: E402
from bigframes.session import connect, Session  # noqa: E402
from bigframes.version import __version__  # noqa: E402

_MAGIC_NAMES = ["bqsql"]


def load_ipython_extension(ipython):
    """Called by IPython when this module is loaded as an IPython extension."""
    # Requires IPython to be installed for import to succeed
    from bigframes._magics import _cell_magic

    for magic_name in _MAGIC_NAMES:
        ipython.register_magic_function(
            _cell_magic, magic_kind="cell", magic_name=magic_name
        )


__all__ = [
    "options",
    "BigQueryOptions",
    "get_global_session",
    "close_session",
    "enums",
    "exceptions",
    "connect",
    "Session",
    "__version__",
    "option_context",
]
