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
"""Unit tests for the accelerator routing table in _routing.py."""

import pytest

from google.cloud.bigtable.data._accelerator._routing import (
    _ACCELERATOR_SUPPORTED,
    is_supported,
)


class TestIsSupported:
    def test_read_row_supported(self):
        assert is_supported("read_row") is True

    def test_mutate_row_supported(self):
        assert is_supported("mutate_row") is True

    def test_read_rows_not_supported(self):
        # read_rows (plural) is not in the supported set.
        assert is_supported("read_rows") is False

    def test_mutate_rows_not_supported(self):
        assert is_supported("mutate_rows") is False

    def test_sample_row_keys_not_supported(self):
        assert is_supported("sample_row_keys") is False

    def test_bulk_mutate_rows_not_supported(self):
        assert is_supported("bulk_mutate_rows") is False

    def test_empty_string_not_supported(self):
        assert is_supported("") is False

    def test_unknown_method_not_supported(self):
        assert is_supported("some_unknown_rpc") is False

    def test_supported_set_is_frozenset(self):
        assert isinstance(_ACCELERATOR_SUPPORTED, frozenset)

    def test_supported_set_contains_expected_methods(self):
        assert "read_row" in _ACCELERATOR_SUPPORTED
        assert "mutate_row" in _ACCELERATOR_SUPPORTED
