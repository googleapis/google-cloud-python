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

import pandas
import pytest


@pytest.fixture(params=["ffill", "bfill"])
def fillna_method(request):
    """
    Parametrized fixture giving method parameters 'ffill' and 'bfill' for
    Series.fillna(method=<method>) testing.

    See:
    https://github.com/pandas-dev/pandas/blob/main/pandas/tests/extension/conftest.py
    """
    return request.param


@pytest.fixture
def na_value():
    return pandas.NaT


@pytest.fixture
def na_cmp():
    """
    Binary operator for comparing NA values.

    Should return a function of two arguments that returns
    True if both arguments are (scalar) NA for your type.

    See:
    https://github.com/pandas-dev/pandas/blob/main/pandas/tests/extension/conftest.py
    and
    https://github.com/pandas-dev/pandas/blob/main/pandas/tests/extension/test_datetime.py
    """

    def cmp(a, b):
        return a is pandas.NaT and a is b

    return cmp
