# Copyright 2024 Google LLC
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

from bigframes.core.rewrite.fold_row_count import fold_row_counts
from bigframes.core.rewrite.identifiers import remap_variables
from bigframes.core.rewrite.implicit_align import try_row_join
from bigframes.core.rewrite.legacy_align import legacy_join_as_projection
from bigframes.core.rewrite.order import bake_order, defer_order
from bigframes.core.rewrite.pruning import column_pruning
from bigframes.core.rewrite.scan_reduction import (
    try_reduce_to_local_scan,
    try_reduce_to_table_scan,
)
from bigframes.core.rewrite.select_pullup import defer_selection
from bigframes.core.rewrite.slices import pull_out_limit, pull_up_limits, rewrite_slice
from bigframes.core.rewrite.timedeltas import rewrite_timedelta_expressions
from bigframes.core.rewrite.windows import pull_out_window_order, rewrite_range_rolling

__all__ = [
    "legacy_join_as_projection",
    "try_row_join",
    "rewrite_slice",
    "rewrite_timedelta_expressions",
    "pull_up_limits",
    "pull_out_limit",
    "remap_variables",
    "defer_order",
    "column_pruning",
    "rewrite_range_rolling",
    "try_reduce_to_table_scan",
    "bake_order",
    "try_reduce_to_local_scan",
    "fold_row_counts",
    "pull_out_window_order",
    "defer_selection",
]
