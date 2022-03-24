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

import pandas
from pandas.tests.extension import base
import pytest

import db_dtypes


# TODO(https://github.com/googleapis/python-db-dtypes-pandas/issues/87): Add
# compliance tests for arithmetic operations.

# TODO(https://github.com/googleapis/python-db-dtypes-pandas/issues/78): Add
# compliance tests for reduction operations.


class TestComparisonOps(base.BaseComparisonOpsTests):
    pass


class TestCasting(base.BaseCastingTests):
    pass


class TestConstructors(base.BaseConstructorsTests):
    pass


class TestDtype(base.BaseDtypeTests):
    pass


class TestGetitem(base.BaseGetitemTests):
    pass


class TestGroupby(base.BaseGroupbyTests):
    pass


class TestIndex(base.BaseIndexTests):
    pass


class TestInterface(base.BaseInterfaceTests):
    pass


class TestMissing(base.BaseMissingTests):
    pass


class TestMethods(base.BaseMethodsTests):
    def test_combine_add(self):
        pytest.skip("Cannot add dates.")

    @pytest.mark.parametrize("dropna", [True, False])
    def test_value_counts(self, all_data, dropna):
        all_data = all_data[:10]
        if dropna:
            # Overridden from
            # https://github.com/pandas-dev/pandas/blob/main/pandas/tests/extension/base/methods.py
            # to avoid difference in dtypes.
            other = db_dtypes.DateArray(all_data[~all_data.isna()])
        else:
            other = all_data

        result = pandas.Series(all_data).value_counts(dropna=dropna).sort_index()
        expected = pandas.Series(other).value_counts(dropna=dropna).sort_index()

        self.assert_series_equal(result, expected)


class TestParsing(base.BaseParsingTests):
    pass


class TestPrinting(base.BasePrintingTests):
    pass


class TestReshaping(base.BaseReshapingTests):
    pass


class TestSetitem(base.BaseSetitemTests):
    pass
