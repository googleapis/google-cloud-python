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


def test_get_connection_name_full_connection_id():
    connection_name = clients.BqConnectionManager.resolve_full_connection_name(
        "connection-id", default_project="default-project", default_location="us"
    )
    assert connection_name == "default-project.us.connection-id"


def test_get_connection_name_full_location_connection_id():
    connection_name = clients.BqConnectionManager.resolve_full_connection_name(
        "eu.connection-id", default_project="default-project", default_location="us"
    )
    assert connection_name == "default-project.eu.connection-id"


def test_get_connection_name_full_all():
    connection_name = clients.BqConnectionManager.resolve_full_connection_name(
        "my-project.eu.connection-id",
        default_project="default-project",
        default_location="us",
    )
    assert connection_name == "my-project.eu.connection-id"


def test_get_connection_name_full_raise_value_error():
    with pytest.raises(ValueError):
        clients.BqConnectionManager.resolve_full_connection_name(
            "my-project.eu.connection-id.extra_field",
            default_project="default-project",
            default_location="us",
        )
