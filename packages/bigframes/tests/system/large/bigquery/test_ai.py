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

import pandas as pd
import pandas.testing

import bigframes.bigquery as bbq


def test_ai_generate_bool_multi_model(session):
    df = session.from_glob_path(
        "gs://bigframes-dev-testing/a_multimodel/images/*", name="image"
    )

    result = bbq.ai.generate_bool((df["image"], " contains an animal")).struct.field(
        "result"
    )

    pandas.testing.assert_series_equal(
        result.to_pandas(),
        pd.Series([True, True, False, False, False], name="result"),
        check_dtype=False,
        check_index=False,
    )
