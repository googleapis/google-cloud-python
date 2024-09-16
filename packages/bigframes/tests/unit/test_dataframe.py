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

import google.cloud.bigquery
import pytest

import bigframes.dataframe

from . import resources


def test_dataframe_dropna_axis_1_subset_not_implememented(
    monkeypatch: pytest.MonkeyPatch,
):
    dataframe = resources.create_dataframe(monkeypatch)

    with pytest.raises(NotImplementedError, match="subset"):
        dataframe.dropna(axis=1, subset=["col1", "col2"])


def test_dataframe_repr_with_uninitialized_object():
    """Ensures DataFrame.__init__ can be paused in a visual debugger without crashing.

    Regression test for https://github.com/googleapis/python-bigquery-dataframes/issues/728
    """
    # Avoid calling __init__ to simulate pausing __init__ in a debugger.
    # https://stackoverflow.com/a/6384982/101923
    dataframe = bigframes.dataframe.DataFrame.__new__(bigframes.dataframe.DataFrame)
    got = repr(dataframe)
    assert "DataFrame" in got


def test_dataframe_to_gbq_invalid_destination(monkeypatch: pytest.MonkeyPatch):
    dataframe = resources.create_dataframe(monkeypatch)

    with pytest.raises(ValueError, match="no_dataset_or_project"):
        dataframe.to_gbq("no_dataset_or_project")


def test_dataframe_to_gbq_invalid_if_exists(monkeypatch: pytest.MonkeyPatch):
    dataframe = resources.create_dataframe(monkeypatch)

    with pytest.raises(ValueError, match="notreallyanoption"):
        # Even though the type is annotated with the literals we accept, users
        # might not be using a type checker, especially not in an interactive
        # notebook.
        dataframe.to_gbq(if_exists="notreallyanoption")  # type: ignore


def test_dataframe_to_gbq_invalid_if_exists_no_destination(
    monkeypatch: pytest.MonkeyPatch,
):
    dataframe = resources.create_dataframe(monkeypatch)

    with pytest.raises(ValueError, match="append"):
        dataframe.to_gbq(if_exists="append")


def test_dataframe_to_gbq_writes_to_anonymous_dataset(
    monkeypatch: pytest.MonkeyPatch,
):
    anonymous_dataset_id = "my-anonymous-project.my_anonymous_dataset"
    anonymous_dataset = google.cloud.bigquery.DatasetReference.from_string(
        anonymous_dataset_id
    )
    session = resources.create_bigquery_session(anonymous_dataset=anonymous_dataset)
    dataframe = resources.create_dataframe(monkeypatch, session=session)

    destination = dataframe.to_gbq()

    assert destination.startswith(anonymous_dataset_id)
