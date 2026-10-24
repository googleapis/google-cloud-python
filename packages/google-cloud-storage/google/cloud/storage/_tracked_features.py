# Copyright 2026 Google LLC
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

"""Registry of client-side features reported to the Cloud Storage service.

Each member of :class:`TrackedFeature` is a bit position in a 32-bit feature
mask. The mask is sent on the ``x-goog-storage-python-features`` header so the
service can attribute usage of purely client-side features (which are otherwise
invisible on the wire) to the Python SDK.

This file is the single source of truth for the bit assignments; keep each
member on its own line in the form ``NAME = <bit>`` so that tooling can parse
it.
"""

import enum


class TrackedFeature(enum.IntEnum):
    """Client-side features reported via x-goog-storage-python-features."""

    MULTI_RANGE_DOWNLOADER = 0
    # Bit 1 is reserved for parallel composite upload (PCU).
