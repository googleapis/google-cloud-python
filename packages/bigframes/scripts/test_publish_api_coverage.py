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

import sys

import pandas
from publish_api_coverage import build_api_coverage_table
import pytest

pytest.importorskip("sklearn")


@pytest.fixture
def api_coverage_df():
    return build_api_coverage_table("my_bf_ver", "my_release_ver")


@pytest.mark.skipif(
    sys.version_info >= (3, 13),
    reason="Issues with installing sklearn for this test in python 3.13",
)
def test_api_coverage_produces_expected_schema(api_coverage_df):
    if sys.version.split(".")[:2] == ["3", "9"]:
        pytest.skip(
            "Python 3.9 uses older pandas without good microsecond timestamp support."
        )

    pandas.testing.assert_series_equal(
        api_coverage_df.dtypes,
        pandas.Series(
            data={
                # Note to developer: if you update this test, you will also
                # need to update schema of the API coverage BigQuery table in
                # the bigframes-metrics project.
                "api": "string",
                "pattern": "string",
                "kind": "string",
                "is_in_bigframes": "boolean",
                "missing_parameters": "string",
                "requires_index": "string",
                "requires_ordering": "string",
                "module": "string",
                "timestamp": "datetime64[us]",
                "bigframes_version": "string",
                "release_version": "string",
            },
        ),
    )


@pytest.mark.skipif(
    sys.version_info >= (3, 13),
    reason="Issues with installing sklearn for this test in python 3.13",
)
def test_api_coverage_produces_missing_parameters(api_coverage_df):
    """Make sure at least some functions have reported missing parameters."""
    assert (api_coverage_df["missing_parameters"].str.len() > 0).any()
