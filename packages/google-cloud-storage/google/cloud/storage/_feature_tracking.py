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

"""Helpers for encoding the client feature-tracking header.

The ``x-goog-storage-python-features`` header carries a bitmask of
:class:`~google.cloud.storage._tracked_features.TrackedFeature` values,
encoded as a 4-byte big-endian unsigned integer in URL-safe base64 (with
padding). The header is omitted entirely when no feature is set.
"""

import base64
import struct
from typing import List, Tuple

from google.cloud.storage._tracked_features import TrackedFeature

FEATURES_HEADER = "x-goog-storage-python-features"
"""HTTP header / gRPC metadata key carrying the client feature mask."""

_MASK_BITS = 32
_MAX_MASK = (1 << _MASK_BITS) - 1


def feature_mask(*features: TrackedFeature) -> int:
    """Combine tracked features into a 32-bit mask.

    :type features: :class:`~google.cloud.storage._tracked_features.TrackedFeature`
    :param features: Features to set in the mask.

    :rtype: int
    :returns: Bitmask with one bit set per feature.
    """
    mask = 0
    for feature in features:
        bit = int(feature)
        if not 0 <= bit < _MASK_BITS:
            raise ValueError(f"Feature bit {bit} is out of range [0, {_MASK_BITS})")
        mask |= 1 << bit
    return mask


def encode_feature_mask(mask: int) -> str:
    """Encode a feature mask as a URL-safe base64 string.

    The mask is packed as a 4-byte big-endian unsigned integer and encoded
    with URL-safe base64 (``-``/``_`` alphabet, padded). The service rejects
    the standard ``+``/``/`` alphabet.

    :type mask: int
    :param mask: 32-bit feature mask.

    :rtype: str
    :returns: The encoded header value, e.g. ``"AAAAAQ=="`` for mask ``1``.
    """
    if not 0 <= mask <= _MAX_MASK:
        raise ValueError(f"Feature mask {mask} does not fit in {_MASK_BITS} bits")
    return base64.urlsafe_b64encode(struct.pack(">I", mask)).decode("ascii")


def features_metadata(*features: TrackedFeature) -> List[Tuple[str, str]]:
    """Build gRPC metadata for the given tracked features.

    :type features: :class:`~google.cloud.storage._tracked_features.TrackedFeature`
    :param features: Features in use for the request/stream.

    :rtype: List[Tuple[str, str]]
    :returns: ``[(FEATURES_HEADER, <encoded mask>)]``, or ``[]`` when no
              feature is set so that the header is omitted.
    """
    mask = feature_mask(*features)
    if mask == 0:
        return []
    return [(FEATURES_HEADER, encode_feature_mask(mask))]
