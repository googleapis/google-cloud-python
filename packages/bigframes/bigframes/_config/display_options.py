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

"""Options for displaying objects."""

import contextlib

import bigframes_vendored.pandas.core.config_init as vendored_pandas_config
import pandas as pd

DisplayOptions = vendored_pandas_config.DisplayOptions


@contextlib.contextmanager
def pandas_repr(display_options: vendored_pandas_config.DisplayOptions):
    """Use this when visualizing with pandas.

    This context manager makes sure we reset the pandas options when we're done
    so that we don't override pandas behavior.
    """
    with pd.option_context(
        "display.max_colwidth",
        display_options.max_colwidth,
        "display.max_columns",
        display_options.max_columns,
        "display.max_rows",
        display_options.max_rows,
        "display.precision",
        display_options.precision,
        "display.show_dimensions",
        True,
    ) as pandas_context:
        yield (pandas_context)
