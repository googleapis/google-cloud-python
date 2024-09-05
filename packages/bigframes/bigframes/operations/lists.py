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

from __future__ import annotations

import inspect
from typing import Union

import bigframes_vendored.pandas.core.arrays.arrow.accessors as vendoracessors

from bigframes.core import log_adapter
import bigframes.operations as ops
from bigframes.operations._op_converters import convert_index, convert_slice
import bigframes.operations.base
import bigframes.series as series


@log_adapter.class_logger
class ListAccessor(
    bigframes.operations.base.SeriesMethods, vendoracessors.ListAccessor
):
    __doc__ = vendoracessors.ListAccessor.__doc__

    def len(self):
        return self._apply_unary_op(ops.len_op)

    def __getitem__(self, key: Union[int, slice]) -> series.Series:
        if isinstance(key, int):
            return self._apply_unary_op(convert_index(key))
        elif isinstance(key, slice):
            return self._apply_unary_op(convert_slice(key))
        else:
            raise ValueError(f"key must be an int or slice, got {type(key).__name__}")

    __getitem__.__doc__ = inspect.getdoc(vendoracessors.ListAccessor.__getitem__)
