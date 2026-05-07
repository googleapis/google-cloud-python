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

"""Shared helper functions for verifying versions of installed modules."""


import sys
from typing import Tuple


def extract_runtime_version() -> Tuple[int, int, int]:
    # Retrieve the version information
    version_info = sys.version_info

    # Extract the major, minor, and micro components
    major = version_info.major
    minor = version_info.minor
    micro = version_info.micro

    # Display the version number in a clear format
    return major, minor, micro
