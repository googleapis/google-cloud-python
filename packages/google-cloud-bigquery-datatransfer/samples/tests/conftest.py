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

import datetime
import os
import uuid

import google.auth
import google.cloud.bigquery
import pytest


@pytest.fixture
def project_id():
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="module")
def credentials():
    # If using a service account, the BQ DTS robot associated with your project
    # requires the roles/iam.serviceAccountShortTermTokenMinter permission to
    # act on behalf of the account.
    creds, _ = google.auth.default(["https://www.googleapis.com/auth/cloud-platform"])
    return creds


@pytest.fixture(scope="module")
def bqdts_client(credentials):
    from google.cloud import bigquery_datatransfer

    return bigquery_datatransfer.DataTransferServiceClient(credentials=credentials)


@pytest.fixture(scope="module")
def bigquery_client(credentials):
    return google.cloud.bigquery.Client(credentials=credentials)


@pytest.fixture(scope="module")
def dataset_id(bigquery_client):
    # Ensure the test account has owner permissions on the dataset by creating
    # one from scratch.
    now = datetime.datetime.now()
    temp_ds_id = "bqdts_{}_{}".format(
        now.strftime("%Y%m%d%H%M%S"), uuid.uuid4().hex[:8]
    )
    bigquery_client.create_dataset(temp_ds_id)
    yield temp_ds_id
    bigquery_client.delete_dataset(temp_ds_id)


@pytest.fixture
def to_delete(bqdts_client):
    doomed = []
    yield doomed

    for resource_name in doomed:
        try:
            bqdts_client.delete_transfer_config(name=resource_name)
        except Exception:
            pass
