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

import tempfile

import pandas as pd

import bigframes as bf
import bigframes.formatting_helpers as formatting_helpers


def test_progress_bar_dataframe(
    penguins_df_default_index: bf.dataframe.DataFrame, capsys
):
    bf.options.display.progress_bar = "notebook"
    penguins_df_default_index.to_pandas()
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = [line for line in lines if len(line) > 0]
    assert len(lines) > 0
    assert penguins_df_default_index.query_job is not None
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_series(penguins_df_default_index: bf.dataframe.DataFrame, capsys):
    bf.options.display.progress_bar = "notebook"
    series = penguins_df_default_index["body_mass_g"].head(10)
    series.to_pandas()
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = [line for line in lines if len(line) > 0]
    assert len(lines) > 0
    assert series.query_job is not None
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_scalar(penguins_df_default_index: bf.dataframe.DataFrame, capsys):
    bf.options.display.progress_bar = "notebook"
    penguins_df_default_index["body_mass_g"].head(10).mean()
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = [line for line in lines if len(line) > 0]
    assert len(lines) > 0
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_read_gbq(session: bf.Session, penguins_table_id: str, capsys):
    bf.options.display.progress_bar = "notebook"
    session.read_gbq(penguins_table_id)
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = [line for line in lines if len(line) > 0]
    assert len(lines) > 0
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_extract_jobs(
    penguins_df_default_index: bf.dataframe.DataFrame, gcs_folder, capsys
):
    bf.options.display.progress_bar = "notebook"
    path = gcs_folder + "test_read_csv_progress_bar*.csv"
    penguins_df_default_index.to_csv(path)
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = [line for line in lines if len(line) > 0]
    assert len(lines) > 0
    for line in lines:
        assert html_check in line and open_job_check in line


def test_progress_bar_load_jobs(
    session: bf.Session, penguins_pandas_df_default_index: pd.DataFrame, capsys
):
    bf.options.display.progress_bar = "notebook"
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_progress_bar*.csv"
        penguins_pandas_df_default_index.to_csv(path, index=False)
        session.read_csv(path)
    html_check = "HTML(value="
    open_job_check = "Open Job"
    lines = capsys.readouterr().out.split("\n")
    lines = [line for line in lines if len(line) > 0]
    assert len(lines) > 0
    for line in lines:
        assert html_check in line and open_job_check in line


def test_query_job_repr_html(penguins_df_default_index: bf.dataframe.DataFrame):
    bf.options.display.progress_bar = "notebook"
    penguins_df_default_index._block._expr._session.bqclient.default_query_job_config.use_query_cache = (
        False
    )
    penguins_df_default_index.to_pandas()
    query_job_repr = formatting_helpers.repr_query_job_html(
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


def test_query_job_repr(penguins_df_default_index: bf.dataframe.DataFrame):
    penguins_df_default_index._block._expr._session.bqclient.default_query_job_config.use_query_cache = (
        False
    )
    penguins_df_default_index.to_pandas()
    query_job_repr = formatting_helpers.repr_query_job(
        penguins_df_default_index.query_job
    )
    string_checks = [
        "Job",
        "Destination Table",
        "Slot Time",
        "Bytes Processed",
        "Cache hit",
    ]
    for string in string_checks:
        assert string in query_job_repr


def test_query_job_dry_run(
    penguins_df_default_index: bf.dataframe.DataFrame, capsys, deferred_repr
):
    repr(penguins_df_default_index)
    repr(penguins_df_default_index["body_mass_g"])
    lines = capsys.readouterr().out.split("\n")
    lines = filter(None, lines)
    for line in lines:
        assert "Computation deferred. Computation will process" in line
