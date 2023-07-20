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

import bigframes as bf
import bigframes.formatting_helpers as formatting_helpers


def test_progress_bar_dataframe(
    penguins_df_default_index: bf.dataframe.DataFrame, capsys
):
    bf.options.display.progress_bar = "notebook"
    penguins_df_default_index.compute()
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = filter(None, lines)
    assert penguins_df_default_index.query_job is not None
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_series(penguins_df_default_index: bf.dataframe.DataFrame, capsys):
    bf.options.display.progress_bar = "notebook"
    series = penguins_df_default_index["body_mass_g"].head(10)
    series.compute()
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = filter(None, lines)
    assert series.query_job is not None
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_scalar(penguins_df_default_index: bf.dataframe.DataFrame, capsys):
    bf.options.display.progress_bar = "notebook"
    penguins_df_default_index["body_mass_g"].head(10).mean()
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = filter(None, lines)
    for line in lines:
        assert html_check in line and open_job_check in line


def test_query_job_repr(penguins_df_default_index: bf.dataframe.DataFrame):
    bf.options.display.progress_bar = "notebook"
    penguins_df_default_index._block._expr._session.bqclient.default_query_job_config.use_query_cache = (
        False
    )
    penguins_df_default_index.compute()
    query_job_repr = formatting_helpers.repr_query_job(
        penguins_df_default_index.query_job
    ).value
    string_checks = [
        "Job Id",
        "Destination Table",
        "Slot Time",
        "Bytes Processed",
        "Cache hit",
    ]
    for string in string_checks:
        assert string in query_job_repr
