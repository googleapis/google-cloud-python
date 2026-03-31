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

from unittest import mock

from google.cloud import bigquery_connection_v1, resourcemanager_v3
from google.iam.v1 import policy_pb2
import pytest

from bigframes import clients


def test_get_canonical_bq_connection_id_connection_id_only():
    connection_id = clients.get_canonical_bq_connection_id(
        "connection-id", default_project="default-project", default_location="us"
    )
    assert connection_id == "default-project.us.connection-id"


def test_get_canonical_bq_connection_id_location_and_connection_id():
    connection_id = clients.get_canonical_bq_connection_id(
        "eu.connection-id", default_project="default-project", default_location="us"
    )
    assert connection_id == "default-project.eu.connection-id"


def test_get_canonical_bq_connection_id_already_canonical():
    connection_id = clients.get_canonical_bq_connection_id(
        "my-project.eu.connection-id",
        default_project="default-project",
        default_location="us",
    )
    assert connection_id == "my-project.eu.connection-id"


def test_get_canonical_bq_connection_id_invalid():
    with pytest.raises(ValueError, match="Invalid connection id format"):
        clients.get_canonical_bq_connection_id(
            "my-project.eu.connection-id.extra_field",
            default_project="default-project",
            default_location="us",
        )


def test_get_canonical_bq_connection_id_valid_path():
    connection_id = clients.get_canonical_bq_connection_id(
        "projects/project_id/locations/northamerica-northeast1/connections/connection-id",
        default_project="default-project",
        default_location="us",
    )
    assert connection_id == "project_id.northamerica-northeast1.connection-id"


def test_get_canonical_bq_connection_id_invalid_path():
    with pytest.raises(ValueError, match="Invalid connection id format"):
        clients.get_canonical_bq_connection_id(
            "/projects/project_id/locations/northamerica-northeast1/connections/connection-id",
            default_project="default-project",
            default_location="us",
        )


def test_ensure_iam_binding():
    bq_connection_client = mock.create_autospec(
        bigquery_connection_v1.ConnectionServiceClient, instance=True
    )
    resource_manager_client = mock.create_autospec(
        resourcemanager_v3.ProjectsClient, instance=True
    )
    resource_manager_client.get_iam_policy.return_value = policy_pb2.Policy(
        bindings=[
            policy_pb2.Binding(
                role="roles/test.role1", members=["serviceAccount:serviceAccount1"]
            )
        ]
    )
    bq_connection_manager = clients.BqConnectionManager(
        bq_connection_client, resource_manager_client
    )
    bq_connection_manager._IAM_WAIT_SECONDS = 0  # no need to wait in test
    bq_connection_manager._ensure_iam_binding(
        "test-project", "serviceAccount2", "roles/test.role2"
    )
    resource_manager_client.set_iam_policy.assert_called_once()
