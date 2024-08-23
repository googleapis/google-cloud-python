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

"""Utility functions for implementing 'explode' functions."""

from typing import cast, Sequence, Union

import bigframes.core.blocks as blocks
import bigframes.core.utils as utils


def check_column(
    column: Union[blocks.Label, Sequence[blocks.Label]],
) -> Sequence[blocks.Label]:
    if not utils.is_list_like(column):
        column_labels = cast(Sequence[blocks.Label], (column,))
    else:
        column_labels = cast(Sequence[blocks.Label], tuple(column))

    if not column_labels:
        raise ValueError("column must be nonempty")
    if len(column_labels) > len(set(column_labels)):
        raise ValueError("column must be unique")

    return column_labels
