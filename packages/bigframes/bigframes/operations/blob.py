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

import bigframes
from bigframes.operations import base
import bigframes.operations as ops


class BlobAccessor(base.SeriesMethods):
    def __init__(self, *args, **kwargs):
        if not bigframes.options.experiments.blob:
            raise NotImplementedError()

        super().__init__(*args, **kwargs)

    def metadata(self):
        """Retrive the metadata of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            JSON: metadata of the Blob. Contains fields: content_type, md5_hash, size and updated(time)."""
        details_json = self._apply_unary_op(ops.obj_fetch_metadata_op).struct.field(
            "details"
        )

        import bigframes.bigquery as bbq

        return bbq.json_extract(details_json, "$.gcs_metadata")
