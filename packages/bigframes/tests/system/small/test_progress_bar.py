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

import re
import tempfile

import numpy as np
import pandas as pd
import pytest

import bigframes as bf
import bigframes.formatting_helpers as formatting_helpers
from bigframes.session import MAX_INLINE_DF_BYTES

job_load_message_regex = r"\w+ job [\w-]+ is \w+\."
EXPECTED_DRY_RUN_MESSAGE = "Computation deferred. Computation will process"


def test_progress_bar_dataframe(
    penguins_df_default_index: bf.dataframe.DataFrame, capsys
):
    capsys.readouterr()  # clear output

    with bf.option_context("display.progress_bar", "terminal"):
        penguins_df_default_index.to_pandas(allow_large_results=True)

    assert_loading_msg_exist(capsys.readouterr().out)
    assert penguins_df_default_index.query_job is not None


def test_progress_bar_series(penguins_df_default_index: bf.dataframe.DataFrame, capsys):
    series = penguins_df_default_index["body_mass_g"].head(10)
    capsys.readouterr()  # clear output

    with bf.option_context("display.progress_bar", "terminal"):
        series.to_pandas(allow_large_results=True)

    assert_loading_msg_exist(capsys.readouterr().out)
    assert series.query_job is not None


def test_progress_bar_scalar(penguins_df_default_index: bf.dataframe.DataFrame, capsys):
    capsys.readouterr()  # clear output

    with bf.option_context("display.progress_bar", "terminal"):
        penguins_df_default_index["body_mass_g"].head(10).mean()

    assert capsys.readouterr().out == ""


def test_progress_bar_scalar_allow_large_results(
    penguins_df_default_index: bf.dataframe.DataFrame, capsys
):
    capsys.readouterr()  # clear output

    with bf.option_context(
        "display.progress_bar", "terminal", "compute.allow_large_results", "True"
    ):
        penguins_df_default_index["body_mass_g"].head(10).mean()

    assert_loading_msg_exist(capsys.readouterr().out)


def test_progress_bar_extract_jobs(
    penguins_df_default_index: bf.dataframe.DataFrame, gcs_folder, capsys
):
    path = gcs_folder + "test_read_csv_progress_bar*.csv"
    capsys.readouterr()  # clear output

    with bf.option_context("display.progress_bar", "terminal"):
        penguins_df_default_index.to_csv(path)

    assert_loading_msg_exist(capsys.readouterr().out)


def test_progress_bar_load_jobs(
    session: bf.Session, penguins_pandas_df_default_index: pd.DataFrame, capsys
):
    # repeat the DF to be big enough to trigger the load job.
    df = penguins_pandas_df_default_index
    while len(df) < MAX_INLINE_DF_BYTES:
        df = pd.DataFrame(np.repeat(df.values, 2, axis=0))

    with bf.option_context(
        "display.progress_bar", "terminal"
    ), tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_progress_bar*.csv"
        df.to_csv(path, index=False)
        capsys.readouterr()  # clear output
        session.read_csv(path)

    assert_loading_msg_exist(capsys.readouterr().out)


def assert_loading_msg_exist(capystOut: str, pattern=job_load_message_regex):
    numLoadingMsg = 0
    lines = capystOut.split("\n")
    lines = [line for line in lines if len(line) > 0]

    assert len(lines) > 0
    for line in lines:
        if re.match(pattern, line) is not None:
            numLoadingMsg += 1
    assert numLoadingMsg > 0


def test_query_job_repr_html(penguins_df_default_index: bf.dataframe.DataFrame):
    with bf.option_context("display.progress_bar", "terminal"):
        penguins_df_default_index.to_pandas(allow_large_results=True)
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
    penguins_df_default_index.to_pandas(allow_large_results=True)
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


def test_query_job_dry_run_dataframe(penguins_df_default_index: bf.dataframe.DataFrame):
    with bf.option_context("display.repr_mode", "deferred"):
        df_result = repr(penguins_df_default_index)
        assert EXPECTED_DRY_RUN_MESSAGE in df_result


def test_query_job_dry_run_index(penguins_df_default_index: bf.dataframe.DataFrame):
    with bf.option_context("display.repr_mode", "deferred"):
        index_result = repr(penguins_df_default_index.index)
        assert EXPECTED_DRY_RUN_MESSAGE in index_result


def test_query_job_dry_run_series(penguins_df_default_index: bf.dataframe.DataFrame):
    with bf.option_context("display.repr_mode", "deferred"):
        series_result = repr(penguins_df_default_index["body_mass_g"])
        assert EXPECTED_DRY_RUN_MESSAGE in series_result


def test_repr_anywidget_dataframe(penguins_df_default_index: bf.dataframe.DataFrame):
    pytest.importorskip("anywidget")
    with bf.option_context("display.repr_mode", "anywidget"):
        actual_repr = repr(penguins_df_default_index)
        assert EXPECTED_DRY_RUN_MESSAGE in actual_repr


def test_repr_anywidget_idex(penguins_df_default_index: bf.dataframe.DataFrame):
    pytest.importorskip("anywidget")
    with bf.option_context("display.repr_mode", "anywidget"):
        index = penguins_df_default_index.index
        actual_repr = repr(index)
        assert EXPECTED_DRY_RUN_MESSAGE in actual_repr
