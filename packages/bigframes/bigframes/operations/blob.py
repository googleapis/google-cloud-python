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

import bigframes.dataframe
import bigframes.operations as ops
import bigframes.series
from bigframes.core.logging import log_adapter

FILE_FOLDER_REGEX = r"^.*\/(.*)$"
FILE_EXT_REGEX = r"(\.[0-9a-zA-Z]+$)"


@log_adapter.class_logger
class _BlobAccessor:
    """
    Internal blob functions for Series and Index.
    """

    def __init__(self, data: bigframes.series.Series):
        self._data = data

    def _get_runtime(
        self, mode: str, with_metadata: bool = False
    ) -> bigframes.series.Series:
        s = (
            self._data._apply_unary_op(ops.obj_fetch_metadata_op)
            if with_metadata
            else self._data
        )

        return s._apply_unary_op(ops.ObjGetAccessUrl(mode=mode))

    def _read_url(self) -> bigframes.series.Series:
        return self._get_runtime(mode="R")._apply_unary_op(
            ops.JSONValue(json_path="$.access_urls.read_url")
        )
