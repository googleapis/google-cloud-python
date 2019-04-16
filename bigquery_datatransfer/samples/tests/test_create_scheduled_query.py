# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

import google.api_core.exceptions
import pytest

from .. import create_scheduled_query


@pytest.fixture
def project_id():
    return os.environ["PROJECT_ID"]


@pytest.fixture(scope="module")
def client():
    from google.cloud import bigquery_datatransfer_v1

    return bigquery_datatransfer_v1.DataTransferServiceClient()


@pytest.fixture
def to_delete(client):
    doomed = []
    yield doomed

    for resource_name in doomed:
        try:
            client.delete_transfer_config(resource_name)
        except google.api_core.exceptions.NotFound:
            pass


def test_sample(project_id, capsys, to_delete):
    config_name = create_scheduled_query.sample_create_transfer_config(project_id)
    to_delete.append(config_name)
    out, err = capsys.readouterr()
    assert config_name in out
