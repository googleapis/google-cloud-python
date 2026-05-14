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

import pytest

from google.cloud import bigquery


@pytest.mark.parametrize(
    ("value", "default_project", "expected_project_id", "expected_dataset_id"),
    (
        (
            "string-project.string_dataset",
            None,
            "string-project",
            "string_dataset",
        ),
        (
            "google.com:string-project.string_dataset",
            None,
            "google.com:string-project",
            "string_dataset",
        ),
        (
            "string_dataset",
            "default-project",
            "default-project",
            "string_dataset",
        ),
        (
            "string-project.string_dataset",
            "default-project",
            "string-project",
            "string_dataset",
        ),
    ),
)
def test_dataset_reference(value, default_project, expected_project_id, expected_dataset_id):
    got = bigquery.DatasetReference.from_string(value, default_project=default_project)
    assert got.project == expected_project_id
    assert got.dataset_id == expected_dataset_id


@pytest.mark.parametrize(
    ("value", "expected_error_message"),
    (
        (
            "string_dataset",
            "dataset_id must be a fully-qualified dataset ID",
        ),
        (
            "string-project:string_dataset",
            "dataset_id must be a fully-qualified dataset ID",
        ),
        (
            "google.com.string-project.dataset_id",
            "Too many parts in dataset_id.",
        ),
        (
            "google.com:string-project.dataset_id.table_id",
            "Too many parts in dataset_id.",
        )
    ),
)
def test_dataset_reference_without_default_project_value_error(value, expected_error_message):
    with pytest.raises(ValueError, match=expected_error_message):
        bigquery.DatasetReference.from_string(value, default_project=None)


@pytest.mark.parametrize(
    ("value", "default_project", "expected_project_id", "expected_dataset_id", "expected_table_id"),
    (
        (
            "string-project.string_dataset.string_table",
            None,
            "string-project",
            "string_dataset",
            "string_table",
        ),
        (
            "google.com:string-project.string_dataset.string_table",
            None,
            "google.com:string-project",
            "string_dataset",
            "string_table",
        ),
        (
            "string_dataset.string_table",
            "default-project",
            "default-project",
            "string_dataset",
            "string_table",
        ),
        (
            "my-project.string_dataset.string_table",
            "ignored-default-project",
            "my-project",
            "string_dataset",
            "string_table",
        ),
    ),
)
def test_table_reference(value, default_project, expected_project_id, expected_dataset_id, expected_table_id):
    got = bigquery.TableReference.from_string(value, default_project=default_project)
    assert got.project == expected_project_id
    assert got.dataset_id == expected_dataset_id
    assert got.table_id == expected_table_id


@pytest.mark.parametrize(
    ("value",),
    (
        (
            "string_table",
        ),
        (
            "string_dataset.string_table",
        ),
        (
            "string-project:string_dataset.string_table",
        ),
        (
            "google.com.string-project.dataset_id",
        ),
        (
            "a.b.c.d",
        )
    ),
)
def test_table_reference_without_default_project_value_error(value):
    with pytest.raises(ValueError, match="table_id must be a fully-qualified ID in standard SQL format"):
        bigquery.TableReference.from_string(value, default_project=None)
