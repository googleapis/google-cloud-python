# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud.bigquery.dataset import Dataset, DatasetReference
from .helpers import make_connection, dataset_polymorphic, make_client
import google.cloud.bigquery.dataset
from google.cloud.bigquery.retry import DEFAULT_TIMEOUT
import mock
import pytest


@dataset_polymorphic
def test_create_dataset_minimal(make_dataset, get_reference, client, PROJECT, DS_ID):
    PATH = "projects/%s/datasets" % PROJECT
    RESOURCE = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
    }
    conn = client._connection = make_connection(RESOURCE)

    dataset = make_dataset(PROJECT, DS_ID)
    after = client.create_dataset(dataset, timeout=7.5)

    assert after.dataset_id == DS_ID
    assert after.project == PROJECT
    assert after.etag == RESOURCE["etag"]
    assert after.full_dataset_id == RESOURCE["id"]

    conn.api_request.assert_called_once_with(
        method="POST",
        path="/%s" % PATH,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "labels": {},
        },
        timeout=7.5,
    )


def test_create_dataset_w_attrs(client, PROJECT, DS_ID):
    from google.cloud.bigquery.dataset import AccessEntry

    PATH = "projects/%s/datasets" % PROJECT
    DESCRIPTION = "DESC"
    FRIENDLY_NAME = "FN"
    LOCATION = "US"
    USER_EMAIL = "phred@example.com"
    LABELS = {"color": "red"}
    VIEW = {
        "projectId": "my-proj",
        "datasetId": "starry-skies",
        "tableId": "northern-hemisphere",
    }
    RESOURCE = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
        "description": DESCRIPTION,
        "friendlyName": FRIENDLY_NAME,
        "location": LOCATION,
        "defaultTableExpirationMs": "3600",
        "labels": LABELS,
        "access": [{"role": "OWNER", "userByEmail": USER_EMAIL}, {"view": VIEW}],
    }
    conn = client._connection = make_connection(RESOURCE)
    entries = [
        AccessEntry("OWNER", "userByEmail", USER_EMAIL),
        AccessEntry(None, "view", VIEW),
    ]

    ds_ref = DatasetReference(PROJECT, DS_ID)
    before = Dataset(ds_ref)
    before.access_entries = entries
    before.description = DESCRIPTION
    before.friendly_name = FRIENDLY_NAME
    before.default_table_expiration_ms = 3600
    before.location = LOCATION
    before.labels = LABELS
    after = client.create_dataset(before)

    assert after.dataset_id == DS_ID
    assert after.project == PROJECT
    assert after.etag == RESOURCE["etag"]
    assert after.full_dataset_id == RESOURCE["id"]
    assert after.description == DESCRIPTION
    assert after.friendly_name == FRIENDLY_NAME
    assert after.location == LOCATION
    assert after.default_table_expiration_ms == 3600
    assert after.labels == LABELS

    conn.api_request.assert_called_once_with(
        method="POST",
        path="/%s" % PATH,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "description": DESCRIPTION,
            "friendlyName": FRIENDLY_NAME,
            "location": LOCATION,
            "defaultTableExpirationMs": "3600",
            "access": [
                {"role": "OWNER", "userByEmail": USER_EMAIL},
                {"view": VIEW, "role": None},
            ],
            "labels": LABELS,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_w_custom_property(client, PROJECT, DS_ID):
    # The library should handle sending properties to the API that are not
    # yet part of the library

    path = "/projects/%s/datasets" % PROJECT
    resource = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "newAlphaProperty": "unreleased property",
    }
    conn = client._connection = make_connection(resource)

    ds_ref = DatasetReference(PROJECT, DS_ID)
    before = Dataset(ds_ref)
    before._properties["newAlphaProperty"] = "unreleased property"
    after = client.create_dataset(before)

    assert after.dataset_id == DS_ID
    assert after.project == PROJECT
    assert after._properties["newAlphaProperty"] == "unreleased property"

    conn.api_request.assert_called_once_with(
        method="POST",
        path=path,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "newAlphaProperty": "unreleased property",
            "labels": {},
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_w_client_location_wo_dataset_location(PROJECT, DS_ID, LOCATION):
    PATH = "projects/%s/datasets" % PROJECT
    RESOURCE = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
        "location": LOCATION,
    }
    client = make_client(location=LOCATION)
    conn = client._connection = make_connection(RESOURCE)

    ds_ref = DatasetReference(PROJECT, DS_ID)
    before = Dataset(ds_ref)
    after = client.create_dataset(before)

    assert after.dataset_id == DS_ID
    assert after.project == PROJECT
    assert after.etag == RESOURCE["etag"]
    assert after.full_dataset_id == RESOURCE["id"]
    assert after.location == LOCATION

    conn.api_request.assert_called_once_with(
        method="POST",
        path="/%s" % PATH,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "labels": {},
            "location": LOCATION,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_w_client_location_w_dataset_location(PROJECT, DS_ID, LOCATION):
    PATH = "projects/%s/datasets" % PROJECT
    OTHER_LOCATION = "EU"
    RESOURCE = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
        "location": OTHER_LOCATION,
    }
    client = make_client(location=LOCATION)
    conn = client._connection = make_connection(RESOURCE)

    ds_ref = DatasetReference(PROJECT, DS_ID)
    before = Dataset(ds_ref)
    before.location = OTHER_LOCATION
    after = client.create_dataset(before)

    assert after.dataset_id == DS_ID
    assert after.project == PROJECT
    assert after.etag == RESOURCE["etag"]
    assert after.full_dataset_id == RESOURCE["id"]
    assert after.location == OTHER_LOCATION

    conn.api_request.assert_called_once_with(
        method="POST",
        path="/%s" % PATH,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "labels": {},
            "location": OTHER_LOCATION,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_w_reference(PROJECT, DS_ID, LOCATION):
    path = "/projects/%s/datasets" % PROJECT
    resource = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
        "location": LOCATION,
    }
    client = make_client(location=LOCATION)
    conn = client._connection = make_connection(resource)
    dataset = client.create_dataset(DatasetReference(PROJECT, DS_ID))

    assert dataset.dataset_id == DS_ID
    assert dataset.project == PROJECT
    assert dataset.etag == resource["etag"]
    assert dataset.full_dataset_id == resource["id"]
    assert dataset.location == LOCATION

    conn.api_request.assert_called_once_with(
        method="POST",
        path=path,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "labels": {},
            "location": LOCATION,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_w_fully_qualified_string(PROJECT, DS_ID, LOCATION):
    path = "/projects/%s/datasets" % PROJECT
    resource = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
        "location": LOCATION,
    }
    client = make_client(location=LOCATION)
    conn = client._connection = make_connection(resource)
    dataset = client.create_dataset("{}.{}".format(PROJECT, DS_ID))

    assert dataset.dataset_id == DS_ID
    assert dataset.project == PROJECT
    assert dataset.etag == resource["etag"]
    assert dataset.full_dataset_id == resource["id"]
    assert dataset.location == LOCATION

    conn.api_request.assert_called_once_with(
        method="POST",
        path=path,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "labels": {},
            "location": LOCATION,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_w_string(PROJECT, DS_ID, LOCATION):
    path = "/projects/%s/datasets" % PROJECT
    resource = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "%s:%s" % (PROJECT, DS_ID),
        "location": LOCATION,
    }
    client = make_client(location=LOCATION)
    conn = client._connection = make_connection(resource)
    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        dataset = client.create_dataset(DS_ID)

    final_attributes.assert_called_once_with({"path": path}, client, None)

    assert dataset.dataset_id == DS_ID
    assert dataset.project == PROJECT
    assert dataset.etag == resource["etag"]
    assert dataset.full_dataset_id == resource["id"]
    assert dataset.location == LOCATION

    conn.api_request.assert_called_once_with(
        method="POST",
        path=path,
        data={
            "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
            "labels": {},
            "location": LOCATION,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def test_create_dataset_alreadyexists_w_exists_ok_false(PROJECT, DS_ID, LOCATION):
    client = make_client(location=LOCATION)
    client._connection = make_connection(
        google.api_core.exceptions.AlreadyExists("dataset already exists")
    )

    with pytest.raises(google.api_core.exceptions.AlreadyExists):
        client.create_dataset(DS_ID)


def test_create_dataset_alreadyexists_w_exists_ok_true(PROJECT, DS_ID, LOCATION):
    post_path = "/projects/{}/datasets".format(PROJECT)
    get_path = "/projects/{}/datasets/{}".format(PROJECT, DS_ID)
    resource = {
        "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
        "etag": "etag",
        "id": "{}:{}".format(PROJECT, DS_ID),
        "location": LOCATION,
    }
    client = make_client(location=LOCATION)
    conn = client._connection = make_connection(
        google.api_core.exceptions.AlreadyExists("dataset already exists"), resource
    )
    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        dataset = client.create_dataset(DS_ID, exists_ok=True)

    final_attributes.assert_called_with({"path": get_path}, client, None)

    assert dataset.dataset_id == DS_ID
    assert dataset.project == PROJECT
    assert dataset.etag == resource["etag"]
    assert dataset.full_dataset_id == resource["id"]
    assert dataset.location == LOCATION

    conn.api_request.assert_has_calls(
        [
            mock.call(
                method="POST",
                path=post_path,
                data={
                    "datasetReference": {"projectId": PROJECT, "datasetId": DS_ID},
                    "labels": {},
                    "location": LOCATION,
                },
                timeout=DEFAULT_TIMEOUT,
            ),
            mock.call(method="GET", path=get_path, timeout=DEFAULT_TIMEOUT),
        ]
    )
