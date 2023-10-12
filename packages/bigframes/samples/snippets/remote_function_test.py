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

import bigframes.pandas

from . import remote_function


def test_remote_function_and_read_gbq_function(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # We need a fresh session since we're modifying connection options.
    bigframes.pandas.close_session()

    # TODO(swast): Get project from environment so contributors can run tests.
    remote_function.run_remote_function_and_read_gbq_function("bigframes-dev")
    out, _ = capsys.readouterr()
    assert "Created BQ remote function:" in out
    assert "Created cloud function:" in out
