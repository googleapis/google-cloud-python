# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""High-performance Apache Arrow accelerator for Google Cloud Spanner."""

import os
import warnings

_SLOW_SPANNER_ARROW_WARNING = (
    "As the C extension couldn't be imported, `google-cloud-spanner-arrow` is using a "
    "pure Python implementation that is significantly slower. If possible, "
    "please compile the C extension for maximum throughput."
)

_DISABLE_CEXT = os.getenv("SPANNER_ARROW_PURE_PYTHON", "0").lower() in ("1", "true", "yes")

if not _DISABLE_CEXT:
    try:
        from google_cloud_spanner_arrow import cext as impl
        implementation = "c"
    except ImportError:
        from google_cloud_spanner_arrow import python as impl  # type: ignore
        warnings.warn(_SLOW_SPANNER_ARROW_WARNING, RuntimeWarning)
        implementation = "python"
else:
    from google_cloud_spanner_arrow import python as impl
    implementation = "python"

rows_to_arrow_batch = impl.rows_to_arrow_batch
fields_to_arrow_schema = impl.fields_to_arrow_schema
spanner_type_to_arrow_type = impl.spanner_type_to_arrow_type

__all__ = [
    "rows_to_arrow_batch",
    "fields_to_arrow_schema",
    "spanner_type_to_arrow_type",
    "implementation",
]
