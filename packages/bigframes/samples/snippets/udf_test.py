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

import pytest

import bigframes.pandas

from . import udf


def test_udf_and_read_gbq_function(
    capsys: pytest.CaptureFixture[str],
    dataset_id: str,
    routine_id: str,
) -> None:
    # We need a fresh session since we're modifying connection options.
    bigframes.pandas.close_session()

    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    your_project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")

    udf.run_udf_and_read_gbq_function(your_project_id, dataset_id, routine_id)
    out, _ = capsys.readouterr()
    assert "Created BQ Python UDF:" in out
