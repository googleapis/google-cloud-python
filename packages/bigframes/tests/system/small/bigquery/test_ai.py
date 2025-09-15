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

import sys

import pandas as pd
import pandas.testing
import pytest

import bigframes.bigquery as bbq
import bigframes.pandas as bpd


def test_ai_generate_bool(session):
    s1 = bpd.Series(["apple", "bear"], session=session)
    s2 = bpd.Series(["fruit", "tree"], session=session)
    prompt = (s1, " is a ", s2)

    result = bbq.ai.generate_bool(prompt, endpoint="gemini-2.5-flash").struct.field(
        "result"
    )

    pandas.testing.assert_series_equal(
        result.to_pandas(),
        pd.Series([True, False], name="result"),
        check_dtype=False,
        check_index=False,
    )


def test_ai_generate_bool_with_model_params(session):
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skip test because SQLGLot cannot compile model params to JSON at this env."
        )

    s1 = bpd.Series(["apple", "bear"], session=session)
    s2 = bpd.Series(["fruit", "tree"], session=session)
    prompt = (s1, " is a ", s2)
    model_params = {"generation_config": {"thinking_config": {"thinking_budget": 0}}}

    result = bbq.ai.generate_bool(
        prompt, endpoint="gemini-2.5-flash", model_params=model_params
    ).struct.field("result")

    pandas.testing.assert_series_equal(
        result.to_pandas(),
        pd.Series([True, False], name="result"),
        check_dtype=False,
        check_index=False,
    )
