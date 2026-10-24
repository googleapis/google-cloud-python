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

import base64
import enum
import re
import struct

import pytest

from google.cloud.storage import _tracked_features
from google.cloud.storage._feature_tracking import (
    FEATURES_HEADER,
    encode_feature_mask,
    feature_mask,
    features_metadata,
)
from google.cloud.storage._tracked_features import TrackedFeature


class TestTrackedFeature:
    def test_is_int_enum(self):
        assert issubclass(TrackedFeature, enum.IntEnum)

    def test_bit_assignments(self):
        assert TrackedFeature.MULTI_RANGE_DOWNLOADER == 0

    def test_bits_are_unique_and_in_range(self):
        bits = [int(f) for f in TrackedFeature]
        assert len(bits) == len(set(bits))
        assert all(0 <= b < 32 for b in bits)

    def test_source_is_tool_parseable(self):
        # The registry file is parsed by external tooling with this regex;
        # every enum member must appear on its own ``NAME = <bit>`` line.
        pattern = re.compile(r"^\s*([A-Z0-9_]+)\s*=\s*(\d+)", re.MULTILINE)
        with open(_tracked_features.__file__) as f:
            source = f.read()
        parsed = {name: int(bit) for name, bit in pattern.findall(source)}
        assert parsed == {f.name: int(f) for f in TrackedFeature}


class TestFeatureMask:
    def test_empty(self):
        assert feature_mask() == 0

    def test_single_feature(self):
        assert feature_mask(TrackedFeature.MULTI_RANGE_DOWNLOADER) == 1

    def test_duplicate_feature_is_idempotent(self):
        assert (
            feature_mask(
                TrackedFeature.MULTI_RANGE_DOWNLOADER,
                TrackedFeature.MULTI_RANGE_DOWNLOADER,
            )
            == 1
        )

    def test_out_of_range_bit(self):
        with pytest.raises(ValueError):
            feature_mask(32)
        with pytest.raises(ValueError):
            feature_mask(-1)


class TestEncodeFeatureMask:
    @pytest.mark.parametrize(
        "mask, expected",
        [
            (0, "AAAAAA=="),
            (1, "AAAAAQ=="),
            (4, "AAAABA=="),
            (0xF8, "AAAA-A=="),
            (0xFFFFFFFF, "_____w=="),
        ],
    )
    def test_known_values(self, mask, expected):
        assert encode_feature_mask(mask) == expected

    def test_matches_reference_encoding(self):
        mask = 0xF8
        expected = base64.urlsafe_b64encode(struct.pack(">I", mask)).decode("ascii")
        assert encode_feature_mask(mask) == expected

    def test_is_url_safe(self):
        for mask in (0xF8, 0xFC, 0xFF, 0xFFFFFFFF):
            value = encode_feature_mask(mask)
            assert "+" not in value
            assert "/" not in value

    def test_out_of_range_mask(self):
        with pytest.raises(ValueError):
            encode_feature_mask(1 << 32)
        with pytest.raises(ValueError):
            encode_feature_mask(-1)


class TestFeaturesMetadata:
    def test_header_name(self):
        assert FEATURES_HEADER == "x-goog-storage-python-features"
        assert FEATURES_HEADER == FEATURES_HEADER.lower()

    def test_omitted_when_no_features(self):
        assert features_metadata() == []

    def test_multi_range_downloader(self):
        assert features_metadata(TrackedFeature.MULTI_RANGE_DOWNLOADER) == [
            ("x-goog-storage-python-features", "AAAAAQ==")
        ]
