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
