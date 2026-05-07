# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import sys
from unittest import mock
import warnings

import pytest

import google.auth
import google.oauth2


@pytest.mark.parametrize("module", [google.auth, google.oauth2])
@pytest.mark.parametrize(
    "version, expected_warning",
    [
        ((3, 8), True),
        ((3, 9), True),
        ((3, 10), False),
        ((3, 13), False),
    ],
)
def test_python_version_warnings(module, version, expected_warning):
    # Mock sys.version_info
    # We use a MagicMock that has major and minor attributes
    mock_version = mock.Mock()
    mock_version.major = version[0]
    mock_version.minor = version[1]

    with mock.patch.object(sys, "version_info", mock_version):
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            importlib.reload(module)

            future_warnings = [
                w
                for w in caught_warnings
                if issubclass(w.category, FutureWarning)
                and "past its end of life" in str(w.message)
            ]

            if expected_warning:
                assert (
                    len(future_warnings) > 0
                ), f"Expected FutureWarning for Python {version} in {module.__name__}"
                assert str(version[1]) in str(future_warnings[0].message)
            else:
                assert (
                    len(future_warnings) == 0
                ), f"Did not expect FutureWarning for Python {version} in {module.__name__}"
