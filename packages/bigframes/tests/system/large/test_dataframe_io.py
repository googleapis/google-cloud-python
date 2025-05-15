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

import google.api_core.exceptions
import pytest

import bigframes

WIKIPEDIA_TABLE = "bigquery-public-data.samples.wikipedia"
LARGE_TABLE_OPTION = "compute.allow_large_results"


def test_to_pandas_batches_raise_when_large_result_not_allowed(session):
    with bigframes.option_context(LARGE_TABLE_OPTION, False), pytest.raises(
        google.api_core.exceptions.Forbidden
    ):
        df = session.read_gbq(WIKIPEDIA_TABLE)
        next(df.to_pandas_batches(page_size=500, max_results=1500))


def test_large_df_peek_no_job(session):
    execution_count_before = session._metrics.execution_count

    # only works with null index, as sequential index requires row_number over full table scan.
    df = session.read_gbq(
        WIKIPEDIA_TABLE, index_col=bigframes.enums.DefaultIndexKind.NULL
    )
    result = df.peek(50)
    execution_count_after = session._metrics.execution_count

    assert len(result) == 50
    assert execution_count_after == execution_count_before


def test_to_pandas_batches_override_global_option(
    session,
):
    with bigframes.option_context(LARGE_TABLE_OPTION, False):
        df = session.read_gbq(WIKIPEDIA_TABLE)
        pages = list(
            df.to_pandas_batches(
                page_size=500, max_results=1500, allow_large_results=True
            )
        )
        assert all((len(page) <= 500) for page in pages)
        assert sum(len(page) for page in pages) == 1500


def test_to_pandas_raise_when_large_result_not_allowed(session):
    with bigframes.option_context(LARGE_TABLE_OPTION, False), pytest.raises(
        google.api_core.exceptions.Forbidden
    ):
        df = session.read_gbq(WIKIPEDIA_TABLE)
        next(df.to_pandas())
