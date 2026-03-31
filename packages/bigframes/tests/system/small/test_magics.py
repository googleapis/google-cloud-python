# Copyright 2026 Google LLC
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
import pytest

import bigframes
import bigframes.pandas as bpd

IPython = pytest.importorskip("IPython")


MAGIC_NAME = "bqsql"


@pytest.fixture(scope="module")
def ip():
    """Provides a persistent IPython shell instance for the test session."""
    from IPython.testing.globalipapp import get_ipython

    shell = get_ipython()
    shell.extension_manager.load_extension("bigframes")
    return shell


def test_magic_select_lit_to_var(ip):
    bigframes.close_session()

    line = "dst_var"
    cell_body = "SELECT 3"

    ip.run_cell_magic(MAGIC_NAME, line, cell_body)

    assert "dst_var" in ip.user_ns
    result_df = ip.user_ns["dst_var"]
    assert result_df.shape == (1, 1)
    assert result_df.loc[0, 0] == 3


def test_magic_select_lit_dry_run(ip):
    bigframes.close_session()

    line = "dst_var --dry_run"
    cell_body = "SELECT 3"

    ip.run_cell_magic(MAGIC_NAME, line, cell_body)

    assert "dst_var" in ip.user_ns
    result_df = ip.user_ns["dst_var"]
    assert result_df.totalBytesProcessed == 0


def test_magic_select_lit_display(ip):
    from IPython.utils.capture import capture_output

    bigframes.close_session()

    cell_body = "SELECT 3"

    with capture_output() as io:
        ip.run_cell_magic(MAGIC_NAME, "", cell_body)
        assert len(io.outputs) > 0
        # Check that the output has data, regardless of the format (html, plain, etc)
        available_formats = io.outputs[0].data.keys()
        assert len(available_formats) > 0


def test_magic_select_interpolate(ip):
    bigframes.close_session()
    df = bpd.read_pandas(
        pd.DataFrame({"col_a": [1, 2, 3, 4, 5, 6], "col_b": [1, 2, 1, 3, 1, 2]})
    )
    const_val = 1

    ip.push({"df": df, "const_val": const_val})

    query = """
    SELECT
        SUM(col_a) AS total
    FROM
        {df}
    WHERE col_b={const_val}
    """

    ip.run_cell_magic(MAGIC_NAME, "dst_var", query)

    assert "dst_var" in ip.user_ns
    result_df = ip.user_ns["dst_var"]
    assert result_df.shape == (1, 1)
    assert result_df.loc[0, 0] == 9
