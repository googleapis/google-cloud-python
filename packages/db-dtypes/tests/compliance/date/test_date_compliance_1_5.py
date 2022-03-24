# Copyright 2022 Google LLC
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
"""
Tests for extension interface compliance, inherited from pandas.

See:
https://github.com/pandas-dev/pandas/blob/main/pandas/tests/extension/decimal/test_decimal.py
and
https://github.com/pandas-dev/pandas/blob/main/pandas/tests/extension/test_period.py
"""

from pandas.tests.extension import base
import pytest

# NDArrayBacked2DTests suite added in https://github.com/pandas-dev/pandas/pull/44974
pytest.importorskip("pandas", minversion="1.5.0dev")


class Test2DCompat(base.NDArrayBacked2DTests):
    pass
