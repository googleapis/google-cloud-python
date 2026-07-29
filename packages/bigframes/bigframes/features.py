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

from typing import Tuple


class PandasVersions:
    """Version comparisons for pandas package"""

    def __init__(self):
        self._installed_version = None

    @property
    def installed_version(self) -> Tuple[str, ...]:
        """pandas version"""
        if self._installed_version is None:
            import pandas

            self._installed_version = tuple(pandas.__version__.split("."))
        return self._installed_version

    @property
    def is_arrow_list_dtype_usable(self):
        """True if pandas.ArrowDtype is usable."""
        version = self.installed_version
        return version[0] != "1"


PANDAS_VERSIONS = PandasVersions()
