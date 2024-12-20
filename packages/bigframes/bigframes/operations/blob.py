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

import IPython.display as ipy_display
import requests

from bigframes.operations import base
import bigframes.operations as ops
import bigframes.series


class BlobAccessor(base.SeriesMethods):
    def __init__(self, *args, **kwargs):
        if not bigframes.options.experiments.blob:
            raise NotImplementedError()

        super().__init__(*args, **kwargs)

    def metadata(self) -> bigframes.series.Series:
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

    def display(self, n: int = 3):
        """Display the blob content in the IPython Notebook environment. Only works for image type now.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Args:
            n (int, default 3): number of sample blob objects to display.
        """
        import bigframes.bigquery as bbq

        s = bigframes.series.Series(self._block).head(n)

        obj_ref_runtime = s._apply_unary_op(ops.ObjGetAccessUrl(mode="R"))
        read_urls = bbq.json_extract(
            obj_ref_runtime, json_path="$.access_urls.read_url"
        )

        for read_url in read_urls:
            read_url = str(read_url).strip('"')
            response = requests.get(read_url)
            ipy_display.display(ipy_display.Image(response.content))
