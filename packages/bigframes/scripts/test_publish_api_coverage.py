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

import pandas
import publish_api_coverage


def test_api_coverage_produces_expected_schema():
    df = publish_api_coverage.build_api_coverage_table("my_bf_ver", "my_release_ver")
    pandas.testing.assert_series_equal(
        df.dtypes,
        pandas.Series(
            data=[
                "string",
                "string",
                "string",
                "boolean",
                "string",
                "string",
                "datetime64[ns]",
                "string",
                "string",
            ],
            index=[
                "api",
                "pattern",
                "kind",
                "is_in_bigframes",
                "missing_parameters",
                "module",
                "timestamp",
                "bigframes_version",
                "release_version",
            ],
        ),
    )
