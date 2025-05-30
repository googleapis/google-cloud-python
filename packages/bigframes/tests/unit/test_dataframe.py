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
from bigframes.testing import mocks


def test_dataframe_dropna_axis_1_subset_not_implememented(
    monkeypatch: pytest.MonkeyPatch,
):
    dataframe = mocks.create_dataframe(monkeypatch)

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


def test_dataframe_setattr_with_uninitialized_object():
    """Ensures DataFrame can be subclassed without trying to set attributes as columns."""
    # Avoid calling __init__ since it might be called later in a subclass.
    # https://stackoverflow.com/a/6384982/101923
    dataframe = bigframes.dataframe.DataFrame.__new__(bigframes.dataframe.DataFrame)
    dataframe.lineage = "my-test-value"
    assert dataframe.lineage == "my-test-value"  # Should just be a regular attribute.


def test_dataframe_to_gbq_invalid_destination(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(monkeypatch)

    with pytest.raises(ValueError, match="no_dataset_or_project"):
        dataframe.to_gbq("no_dataset_or_project")


def test_dataframe_to_gbq_invalid_if_exists(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(monkeypatch)

    with pytest.raises(ValueError, match="notreallyanoption"):
        # Even though the type is annotated with the literals we accept, users
        # might not be using a type checker, especially not in an interactive
        # notebook.
        dataframe.to_gbq(if_exists="notreallyanoption")  # type: ignore


def test_dataframe_to_gbq_invalid_if_exists_no_destination(
    monkeypatch: pytest.MonkeyPatch,
):
    dataframe = mocks.create_dataframe(monkeypatch)

    with pytest.raises(ValueError, match="append"):
        dataframe.to_gbq(if_exists="append")


def test_dataframe_to_gbq_writes_to_anonymous_dataset(
    monkeypatch: pytest.MonkeyPatch,
):
    anonymous_dataset_id = "my-anonymous-project.my_anonymous_dataset"
    anonymous_dataset = google.cloud.bigquery.DatasetReference.from_string(
        anonymous_dataset_id
    )
    session = mocks.create_bigquery_session(anonymous_dataset=anonymous_dataset)
    dataframe = mocks.create_dataframe(monkeypatch, session=session)

    destination = dataframe.to_gbq()

    assert destination.startswith(anonymous_dataset_id)


def test_dataframe_rename_columns(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(
        monkeypatch, data={"col1": [], "col2": [], "col3": []}
    )
    assert dataframe.columns.to_list() == ["col1", "col2", "col3"]
    renamed = dataframe.rename(columns={"col1": "a", "col2": "b", "col3": "c"})
    assert renamed.columns.to_list() == ["a", "b", "c"]


def test_dataframe_rename_columns_inplace_returns_none(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(
        monkeypatch, data={"col1": [], "col2": [], "col3": []}
    )
    assert dataframe.columns.to_list() == ["col1", "col2", "col3"]
    assert (
        dataframe.rename(columns={"col1": "a", "col2": "b", "col3": "c"}, inplace=True)
        is None
    )
    assert dataframe.columns.to_list() == ["a", "b", "c"]


def test_dataframe_rename_axis(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(
        monkeypatch, data={"index1": [], "index2": [], "col1": [], "col2": []}
    ).set_index(["index1", "index2"])
    assert list(dataframe.index.names) == ["index1", "index2"]
    renamed = dataframe.rename_axis(["a", "b"])
    assert list(renamed.index.names) == ["a", "b"]


def test_dataframe_rename_axis_inplace_returns_none(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(
        monkeypatch, data={"index1": [], "index2": [], "col1": [], "col2": []}
    ).set_index(["index1", "index2"])
    assert list(dataframe.index.names) == ["index1", "index2"]
    assert dataframe.rename_axis(["a", "b"], inplace=True) is None
    assert list(dataframe.index.names) == ["a", "b"]


def test_dataframe_semantics_property_future_warning(
    monkeypatch: pytest.MonkeyPatch,
):
    dataframe = mocks.create_dataframe(monkeypatch)

    with bigframes.option_context("experiments.semantic_operators", True), pytest.warns(
        FutureWarning
    ):
        dataframe.semantics
