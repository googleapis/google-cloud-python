# Copyright 2023 Google LLC
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


pyarrow = pytest.importorskip("pyarrow", minversion="3.0.0")


@pytest.fixture
def module_under_test():
    from google.cloud.bigquery import _pyarrow_helpers

    return _pyarrow_helpers


def test_bq_to_arrow_scalars(module_under_test):
    assert (
        module_under_test.bq_to_arrow_scalars("BIGNUMERIC")
        == module_under_test.pyarrow_bignumeric
    )
    assert module_under_test.bq_to_arrow_scalars("UNKNOWN_TYPE") is None


def test_arrow_scalar_ids_to_bq(module_under_test):
    assert module_under_test.arrow_scalar_ids_to_bq(pyarrow.bool_().id) == "BOOL"
    assert module_under_test.arrow_scalar_ids_to_bq("UNKNOWN_TYPE") is None
