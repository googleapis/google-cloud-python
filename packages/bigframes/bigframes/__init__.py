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

# import configuration and types.
# This ensures that when the deeper 'core' modules ask for 'dtypes','options', et. al.,
# they are already defined and available.
import bigframes.dtypes  # noqa: E402 # isort: skip
import bigframes._config  # noqa: E402 # isort: skip
from bigframes._config import option_context, options  # noqa: E402 # isort: skip

import bigframes.enums as enums  # noqa: E402
import bigframes.exceptions as exceptions  # noqa: E402

# We import operations early to resolve a circular dependency between
# bigframes.core.expression and bigframes.operations.
# This ensures the 'Expression' base class is defined before 'Aggregation'
# subclasses attempt to inherit from it.
import bigframes.operations  # noqa: E402 # isort: skip

# Register pandas extensions
import bigframes.extensions.pandas.dataframe_accessor  # noqa: F401, E402
from bigframes._config.bigquery_options import BigQueryOptions  # noqa: E402
from bigframes.core.global_session import (  # noqa: E402
    close_session,
    execution_history,
    get_global_session,
)
from bigframes.session import Session, connect  # noqa: E402
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
    "execution_history",
    "enums",
    "exceptions",
    "connect",
    "Session",
    "__version__",
    "option_context",
]
