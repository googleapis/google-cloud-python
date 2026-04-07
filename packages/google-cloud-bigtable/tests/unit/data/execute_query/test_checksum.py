# Copyright 2025 Google LLC
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
import pytest

import sys
from unittest import mock
import warnings

with warnings.catch_warnings(record=True) as suppressed_warning:
    warnings.warn("Supressed warning", RuntimeWarning)


def test_import_warning_is_rewritten():
    with mock.patch(
        "google.cloud.bigtable.data.execute_query._checksum.import_warning",
        suppressed_warning,
    ):
        with warnings.catch_warnings(record=True) as import_warning:
            from google.cloud.bigtable.data.execute_query._checksum import _CRC32C

            # reset this in case the warning has been emitted in other tests
            _CRC32C.warn_emitted = False

            assert import_warning == []
            with warnings.catch_warnings(record=True) as first_call_warning:
                assert _CRC32C.checksum(b"test") == 2258662080
                assert (
                    "Using pure python implementation of `google-crc32` for ExecuteQuery response validation"
                    in str(first_call_warning[0])
                )
            with warnings.catch_warnings(record=True) as second_call_warning:
                assert _CRC32C.checksum(b"test") == 2258662080
                assert second_call_warning == []


@pytest.mark.skipif(
    sys.version_info < (3, 9) or sys.version_info > (3, 12),
    reason="google_crc32c currently uses pure python for versions not between 3.9 & 3.12",
)
def test_no_warning():
    with warnings.catch_warnings(record=True) as first_call_warning:
        from google.cloud.bigtable.data.execute_query._checksum import _CRC32C

        # reset this in case the warning has been emitted in other tests
        _CRC32C.warn_emitted = False

        assert _CRC32C.checksum(b"test") == 2258662080
        assert first_call_warning == []
