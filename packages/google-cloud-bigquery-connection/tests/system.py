# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest

from google.cloud import bigquery_connection


@pytest.fixture(scope="session")
def project_id():
    return os.environ["PROJECT_ID"]


def test_list_connections(project_id):
    client = bigquery_connection.ConnectionServiceClient()

    parent = f"projects/{project_id}/locations/US"
    connections = list(client.list_connections(parent=parent))

    assert len(connections) >= 0
