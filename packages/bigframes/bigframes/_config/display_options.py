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
import dataclasses
from typing import Literal, Optional

import pandas as pd

import third_party.bigframes_vendored.pandas.core.config_init as vendored_pandas_config


@dataclasses.dataclass
class DisplayOptions:
    __doc__ = vendored_pandas_config.display_options_doc

    max_columns: int = 20
    max_rows: int = 25
    progress_bar: Optional[str] = "auto"
    repr_mode: Literal["head", "deferred"] = "head"

    max_info_columns: int = 100
    max_info_rows: Optional[int] = 200000
    memory_usage: bool = True


@contextlib.contextmanager
def pandas_repr(display_options: DisplayOptions):
    """Use this when visualizing with pandas.

    This context manager makes sure we reset the pandas options when we're done
    so that we don't override pandas behavior.
    """
    with pd.option_context(
        "display.max_columns",
        display_options.max_columns,
        "display.max_rows",
        display_options.max_rows,
        "display.show_dimensions",
        True,
    ) as pandas_context:
        yield (pandas_context)
