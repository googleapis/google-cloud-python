# Copyright 2015 Google LLC
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

import copy
import datetime
import decimal
import email
import gzip
import io
import json
import unittest
import warnings

import mock
import requests
import six
from six.moves import http_client
import pytest
import pytz

try:
    import pandas
except (ImportError, AttributeError):  # pragma: NO COVER
    pandas = None
try:
    import pyarrow
except (ImportError, AttributeError):  # pragma: NO COVER
    pyarrow = None

import google.api_core.exceptions
from google.api_core.gapic_v1 import client_info
import google.cloud._helpers
from google.cloud import bigquery_v2
from google.cloud.bigquery.dataset import DatasetReference
from tests.unit.helpers import make_connection


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_list_partitons_meta_info(project, dataset_id, table_id, num_rows=0):
    return {
        "tableReference": {
            "projectId": project,
            "datasetId": dataset_id,
            "tableId": "{}$__PARTITIONS_SUMMARY__".format(table_id),
        },
        "schema": {
            "fields": [
                {"name": "project_id", "type": "STRING", "mode": "NULLABLE"},
                {"name": "dataset_id", "type": "STRING", "mode": "NULLABLE"},
                {"name": "table_id", "type": "STRING", "mode": "NULLABLE"},
                {"name": "partition_id", "type": "STRING", "mode": "NULLABLE"},
            ]
        },
        "etag": "ETAG",
        "numRows": num_rows,
    }


class TestClient(unittest.TestCase):

    PROJECT = "PROJECT"
    DS_ID = "DATASET_ID"
    TABLE_ID = "TABLE_ID"
    MODEL_ID = "MODEL_ID"
    TABLE_REF = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
    KMS_KEY_NAME = "projects/1/locations/global/keyRings/1/cryptoKeys/1"
    LOCATION = "us-central"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_table_resource(self):
        return {
            "id": "%s:%s:%s" % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            "tableReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "tableId": self.TABLE_ID,
            },
        }

    def test_ctor_defaults(self):
        from google.cloud.bigquery._http import Connection

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertIsNone(client.location)

    def test_ctor_w_location(self):
        from google.cloud.bigquery._http import Connection

        creds = _make_credentials()
        http = object()
        location = "us-central"
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http, location=location
        )
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertEqual(client.location, location)

    def test_ctor_w_query_job_config(self):
        from google.cloud.bigquery._http import Connection
        from google.cloud.bigquery import QueryJobConfig

        creds = _make_credentials()
        http = object()
        location = "us-central"
        job_config = QueryJobConfig()
        job_config.dry_run = True

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            location=location,
            default_query_job_config=job_config,
        )
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertEqual(client.location, location)

        self.assertIsInstance(client._default_query_job_config, QueryJobConfig)
        self.assertTrue(client._default_query_job_config.dry_run)

    def test__get_query_results_miss_w_explicit_project_and_timeout(self):
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection()

        with self.assertRaises(NotFound):
            client._get_query_results(
                "nothere",
                None,
                project="other-project",
                location=self.LOCATION,
                timeout_ms=500,
            )

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/other-project/queries/nothere",
            query_params={"maxResults": 0, "timeoutMs": 500, "location": self.LOCATION},
        )

    def test__get_query_results_miss_w_client_location(self):
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds, location=self.LOCATION)
        conn = client._connection = make_connection()

        with self.assertRaises(NotFound):
            client._get_query_results("nothere", None)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/PROJECT/queries/nothere",
            query_params={"maxResults": 0, "location": self.LOCATION},
        )

    def test__get_query_results_hit(self):
        job_id = "query_job"
        data = {
            "kind": "bigquery#getQueryResultsResponse",
            "etag": "some-tag",
            "schema": {
                "fields": [
                    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
                    {"name": "unique_words", "type": "INTEGER", "mode": "NULLABLE"},
                ]
            },
            "jobReference": {"projectId": self.PROJECT, "jobId": job_id},
            "totalRows": "10",
            "totalBytesProcessed": "2464625",
            "jobComplete": True,
            "cacheHit": False,
        }

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        client._connection = make_connection(data)
        query_results = client._get_query_results(job_id, None)

        self.assertEqual(query_results.total_rows, 10)
        self.assertTrue(query_results.complete)

    def test_get_service_account_email(self):
        path = "/projects/%s/serviceAccount" % (self.PROJECT,)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        email = "bq-123@bigquery-encryption.iam.gserviceaccount.com"
        resource = {"kind": "bigquery#getServiceAccountResponse", "email": email}
        conn = client._connection = make_connection(resource)

        service_account_email = client.get_service_account_email()

        conn.api_request.assert_called_once_with(method="GET", path=path)
        self.assertEqual(service_account_email, email)

    def test_get_service_account_email_w_alternate_project(self):
        project = "my-alternate-project"
        path = "/projects/%s/serviceAccount" % (project,)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        email = "bq-123@bigquery-encryption.iam.gserviceaccount.com"
        resource = {"kind": "bigquery#getServiceAccountResponse", "email": email}
        conn = client._connection = make_connection(resource)

        service_account_email = client.get_service_account_email(project=project)

        conn.api_request.assert_called_once_with(method="GET", path=path)
        self.assertEqual(service_account_email, email)

    def test_list_projects_defaults(self):
        from google.cloud.bigquery.client import Project

        PROJECT_1 = "PROJECT_ONE"
        PROJECT_2 = "PROJECT_TWO"
        TOKEN = "TOKEN"
        DATA = {
            "nextPageToken": TOKEN,
            "projects": [
                {
                    "kind": "bigquery#project",
                    "id": PROJECT_1,
                    "numericId": 1,
                    "projectReference": {"projectId": PROJECT_1},
                    "friendlyName": "One",
                },
                {
                    "kind": "bigquery#project",
                    "id": PROJECT_2,
                    "numericId": 2,
                    "projectReference": {"projectId": PROJECT_2},
                    "friendlyName": "Two",
                },
            ],
        }
        creds = _make_credentials()
        client = self._make_one(PROJECT_1, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_projects()
        page = six.next(iterator.pages)
        projects = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(projects), len(DATA["projects"]))
        for found, expected in zip(projects, DATA["projects"]):
            self.assertIsInstance(found, Project)
            self.assertEqual(found.project_id, expected["id"])
            self.assertEqual(found.numeric_id, expected["numericId"])
            self.assertEqual(found.friendly_name, expected["friendlyName"])
        self.assertEqual(token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/projects", query_params={}
        )

    def test_list_projects_explicit_response_missing_projects_key(self):
        TOKEN = "TOKEN"
        DATA = {}
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_projects(max_results=3, page_token=TOKEN)
        page = six.next(iterator.pages)
        projects = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(projects), 0)
        self.assertIsNone(token)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects",
            query_params={"maxResults": 3, "pageToken": TOKEN},
        )

    def test_list_datasets_defaults(self):
        from google.cloud.bigquery.dataset import DatasetListItem

        DATASET_1 = "dataset_one"
        DATASET_2 = "dataset_two"
        PATH = "projects/%s/datasets" % self.PROJECT
        TOKEN = "TOKEN"
        DATA = {
            "nextPageToken": TOKEN,
            "datasets": [
                {
                    "kind": "bigquery#dataset",
                    "id": "%s:%s" % (self.PROJECT, DATASET_1),
                    "datasetReference": {
                        "datasetId": DATASET_1,
                        "projectId": self.PROJECT,
                    },
                    "friendlyName": None,
                },
                {
                    "kind": "bigquery#dataset",
                    "id": "%s:%s" % (self.PROJECT, DATASET_2),
                    "datasetReference": {
                        "datasetId": DATASET_2,
                        "projectId": self.PROJECT,
                    },
                    "friendlyName": "Two",
                },
            ],
        }
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_datasets()
        page = six.next(iterator.pages)
        datasets = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(datasets), len(DATA["datasets"]))
        for found, expected in zip(datasets, DATA["datasets"]):
            self.assertIsInstance(found, DatasetListItem)
            self.assertEqual(found.full_dataset_id, expected["id"])
            self.assertEqual(found.friendly_name, expected["friendlyName"])
        self.assertEqual(token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={}
        )

    def test_list_datasets_w_project(self):
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection({})

        list(client.list_datasets(project="other-project"))

        conn.api_request.assert_called_once_with(
            method="GET", path="/projects/other-project/datasets", query_params={}
        )

    def test_list_datasets_explicit_response_missing_datasets_key(self):
        PATH = "projects/%s/datasets" % self.PROJECT
        TOKEN = "TOKEN"
        FILTER = "FILTER"
        DATA = {}
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_datasets(
            include_all=True, filter=FILTER, max_results=3, page_token=TOKEN
        )
        page = six.next(iterator.pages)
        datasets = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(datasets), 0)
        self.assertIsNone(token)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/%s" % PATH,
            query_params={
                "all": True,
                "filter": FILTER,
                "maxResults": 3,
                "pageToken": TOKEN,
            },
        )

    def test_dataset_with_specified_project(self):
        from google.cloud.bigquery.dataset import DatasetReference

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        dataset = client.dataset(self.DS_ID, self.PROJECT)
        self.assertIsInstance(dataset, DatasetReference)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)

    def test_dataset_with_default_project(self):
        from google.cloud.bigquery.dataset import DatasetReference

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        dataset = client.dataset(self.DS_ID)
        self.assertIsInstance(dataset, DatasetReference)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)

    def test_get_dataset(self):
        from google.cloud.exceptions import ServerError

        path = "projects/%s/datasets/%s" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        resource = {
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
        }
        conn = client._connection = make_connection(resource)
        dataset_ref = client.dataset(self.DS_ID)

        dataset = client.get_dataset(dataset_ref)

        conn.api_request.assert_called_once_with(method="GET", path="/%s" % path)
        self.assertEqual(dataset.dataset_id, self.DS_ID)

        # Test retry.

        # Not a cloud API exception (missing 'errors' field).
        client._connection = make_connection(Exception(""), resource)
        with self.assertRaises(Exception):
            client.get_dataset(dataset_ref)

        # Zero-length errors field.
        client._connection = make_connection(ServerError(""), resource)
        with self.assertRaises(ServerError):
            client.get_dataset(dataset_ref)

        # Non-retryable reason.
        client._connection = make_connection(
            ServerError("", errors=[{"reason": "serious"}]), resource
        )
        with self.assertRaises(ServerError):
            client.get_dataset(dataset_ref)

        # Retryable reason, but retry is disabled.
        client._connection = make_connection(
            ServerError("", errors=[{"reason": "backendError"}]), resource
        )
        with self.assertRaises(ServerError):
            client.get_dataset(dataset_ref, retry=None)

        # Retryable reason, default retry: success.
        client._connection = make_connection(
            ServerError("", errors=[{"reason": "backendError"}]), resource
        )
        dataset = client.get_dataset(
            # Test with a string for dataset ID.
            dataset_ref.dataset_id
        )
        self.assertEqual(dataset.dataset_id, self.DS_ID)

    def test_create_dataset_minimal(self):
        from google.cloud.bigquery.dataset import Dataset

        PATH = "projects/%s/datasets" % self.PROJECT
        RESOURCE = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(RESOURCE)

        ds_ref = client.dataset(self.DS_ID)
        before = Dataset(ds_ref)

        after = client.create_dataset(before)

        self.assertEqual(after.dataset_id, self.DS_ID)
        self.assertEqual(after.project, self.PROJECT)
        self.assertEqual(after.etag, RESOURCE["etag"])
        self.assertEqual(after.full_dataset_id, RESOURCE["id"])

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % PATH,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "labels": {},
            },
        )

    def test_create_dataset_w_attrs(self):
        from google.cloud.bigquery.dataset import Dataset, AccessEntry

        PATH = "projects/%s/datasets" % self.PROJECT
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
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "description": DESCRIPTION,
            "friendlyName": FRIENDLY_NAME,
            "location": LOCATION,
            "defaultTableExpirationMs": "3600",
            "labels": LABELS,
            "access": [{"role": "OWNER", "userByEmail": USER_EMAIL}, {"view": VIEW}],
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(RESOURCE)
        entries = [
            AccessEntry("OWNER", "userByEmail", USER_EMAIL),
            AccessEntry(None, "view", VIEW),
        ]

        ds_ref = client.dataset(self.DS_ID)
        before = Dataset(ds_ref)
        before.access_entries = entries
        before.description = DESCRIPTION
        before.friendly_name = FRIENDLY_NAME
        before.default_table_expiration_ms = 3600
        before.location = LOCATION
        before.labels = LABELS

        after = client.create_dataset(before)

        self.assertEqual(after.dataset_id, self.DS_ID)
        self.assertEqual(after.project, self.PROJECT)
        self.assertEqual(after.etag, RESOURCE["etag"])
        self.assertEqual(after.full_dataset_id, RESOURCE["id"])
        self.assertEqual(after.description, DESCRIPTION)
        self.assertEqual(after.friendly_name, FRIENDLY_NAME)
        self.assertEqual(after.location, LOCATION)
        self.assertEqual(after.default_table_expiration_ms, 3600)
        self.assertEqual(after.labels, LABELS)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % PATH,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "description": DESCRIPTION,
                "friendlyName": FRIENDLY_NAME,
                "location": LOCATION,
                "defaultTableExpirationMs": "3600",
                "access": [
                    {"role": "OWNER", "userByEmail": USER_EMAIL},
                    {"view": VIEW},
                ],
                "labels": LABELS,
            },
        )

    def test_create_dataset_w_custom_property(self):
        # The library should handle sending properties to the API that are not
        # yet part of the library
        from google.cloud.bigquery.dataset import Dataset

        path = "/projects/%s/datasets" % self.PROJECT
        resource = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "newAlphaProperty": "unreleased property",
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource)

        ds_ref = client.dataset(self.DS_ID)
        before = Dataset(ds_ref)
        before._properties["newAlphaProperty"] = "unreleased property"

        after = client.create_dataset(before)

        self.assertEqual(after.dataset_id, self.DS_ID)
        self.assertEqual(after.project, self.PROJECT)
        self.assertEqual(after._properties["newAlphaProperty"], "unreleased property")

        conn.api_request.assert_called_once_with(
            method="POST",
            path=path,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "newAlphaProperty": "unreleased property",
                "labels": {},
            },
        )

    def test_create_dataset_w_client_location_wo_dataset_location(self):
        from google.cloud.bigquery.dataset import Dataset

        PATH = "projects/%s/datasets" % self.PROJECT
        RESOURCE = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "location": self.LOCATION,
        }
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(RESOURCE)

        ds_ref = client.dataset(self.DS_ID)
        before = Dataset(ds_ref)

        after = client.create_dataset(before)

        self.assertEqual(after.dataset_id, self.DS_ID)
        self.assertEqual(after.project, self.PROJECT)
        self.assertEqual(after.etag, RESOURCE["etag"])
        self.assertEqual(after.full_dataset_id, RESOURCE["id"])
        self.assertEqual(after.location, self.LOCATION)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % PATH,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "labels": {},
                "location": self.LOCATION,
            },
        )

    def test_create_dataset_w_client_location_w_dataset_location(self):
        from google.cloud.bigquery.dataset import Dataset

        PATH = "projects/%s/datasets" % self.PROJECT
        OTHER_LOCATION = "EU"
        RESOURCE = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "location": OTHER_LOCATION,
        }
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(RESOURCE)

        ds_ref = client.dataset(self.DS_ID)
        before = Dataset(ds_ref)
        before.location = OTHER_LOCATION

        after = client.create_dataset(before)

        self.assertEqual(after.dataset_id, self.DS_ID)
        self.assertEqual(after.project, self.PROJECT)
        self.assertEqual(after.etag, RESOURCE["etag"])
        self.assertEqual(after.full_dataset_id, RESOURCE["id"])
        self.assertEqual(after.location, OTHER_LOCATION)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % PATH,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "labels": {},
                "location": OTHER_LOCATION,
            },
        )

    def test_create_dataset_w_reference(self):
        path = "/projects/%s/datasets" % self.PROJECT
        resource = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "location": self.LOCATION,
        }
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        dataset = client.create_dataset(client.dataset(self.DS_ID))

        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(dataset.etag, resource["etag"])
        self.assertEqual(dataset.full_dataset_id, resource["id"])
        self.assertEqual(dataset.location, self.LOCATION)

        conn.api_request.assert_called_once_with(
            method="POST",
            path=path,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "labels": {},
                "location": self.LOCATION,
            },
        )

    def test_create_dataset_w_fully_qualified_string(self):
        path = "/projects/%s/datasets" % self.PROJECT
        resource = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "location": self.LOCATION,
        }
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        dataset = client.create_dataset("{}.{}".format(self.PROJECT, self.DS_ID))

        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(dataset.etag, resource["etag"])
        self.assertEqual(dataset.full_dataset_id, resource["id"])
        self.assertEqual(dataset.location, self.LOCATION)

        conn.api_request.assert_called_once_with(
            method="POST",
            path=path,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "labels": {},
                "location": self.LOCATION,
            },
        )

    def test_create_dataset_w_string(self):
        path = "/projects/%s/datasets" % self.PROJECT
        resource = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "location": self.LOCATION,
        }
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        dataset = client.create_dataset(self.DS_ID)

        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(dataset.etag, resource["etag"])
        self.assertEqual(dataset.full_dataset_id, resource["id"])
        self.assertEqual(dataset.location, self.LOCATION)

        conn.api_request.assert_called_once_with(
            method="POST",
            path=path,
            data={
                "datasetReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                },
                "labels": {},
                "location": self.LOCATION,
            },
        )

    def test_create_dataset_alreadyexists_w_exists_ok_false(self):
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        client._connection = make_connection(
            google.api_core.exceptions.AlreadyExists("dataset already exists")
        )

        with pytest.raises(google.api_core.exceptions.AlreadyExists):
            client.create_dataset(self.DS_ID)

    def test_create_dataset_alreadyexists_w_exists_ok_true(self):
        post_path = "/projects/{}/datasets".format(self.PROJECT)
        get_path = "/projects/{}/datasets/{}".format(self.PROJECT, self.DS_ID)
        resource = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "id": "{}:{}".format(self.PROJECT, self.DS_ID),
            "location": self.LOCATION,
        }
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(
            google.api_core.exceptions.AlreadyExists("dataset already exists"), resource
        )

        dataset = client.create_dataset(self.DS_ID, exists_ok=True)

        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(dataset.etag, resource["etag"])
        self.assertEqual(dataset.full_dataset_id, resource["id"])
        self.assertEqual(dataset.location, self.LOCATION)

        conn.api_request.assert_has_calls(
            [
                mock.call(
                    method="POST",
                    path=post_path,
                    data={
                        "datasetReference": {
                            "projectId": self.PROJECT,
                            "datasetId": self.DS_ID,
                        },
                        "labels": {},
                        "location": self.LOCATION,
                    },
                ),
                mock.call(method="GET", path=get_path),
            ]
        )

    def test_create_routine_w_minimal_resource(self):
        from google.cloud.bigquery.routine import Routine
        from google.cloud.bigquery.routine import RoutineReference

        creds = _make_credentials()
        resource = {
            "routineReference": {
                "projectId": "test-routine-project",
                "datasetId": "test_routines",
                "routineId": "minimal_routine",
            }
        }
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource)
        full_routine_id = "test-routine-project.test_routines.minimal_routine"
        routine = Routine(full_routine_id)

        actual_routine = client.create_routine(routine)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/test-routine-project/datasets/test_routines/routines",
            data=resource,
        )
        self.assertEqual(
            actual_routine.reference, RoutineReference.from_string(full_routine_id)
        )

    def test_create_routine_w_conflict(self):
        from google.cloud.bigquery.routine import Routine

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(
            google.api_core.exceptions.AlreadyExists("routine already exists")
        )
        full_routine_id = "test-routine-project.test_routines.minimal_routine"
        routine = Routine(full_routine_id)

        with pytest.raises(google.api_core.exceptions.AlreadyExists):
            client.create_routine(routine)

        resource = {
            "routineReference": {
                "projectId": "test-routine-project",
                "datasetId": "test_routines",
                "routineId": "minimal_routine",
            }
        }
        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/test-routine-project/datasets/test_routines/routines",
            data=resource,
        )

    def test_create_routine_w_conflict_exists_ok(self):
        from google.cloud.bigquery.routine import Routine

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = {
            "routineReference": {
                "projectId": "test-routine-project",
                "datasetId": "test_routines",
                "routineId": "minimal_routine",
            }
        }
        conn = client._connection = make_connection(
            google.api_core.exceptions.AlreadyExists("routine already exists"), resource
        )
        full_routine_id = "test-routine-project.test_routines.minimal_routine"
        routine = Routine(full_routine_id)

        actual_routine = client.create_routine(routine, exists_ok=True)

        self.assertEqual(actual_routine.project, "test-routine-project")
        self.assertEqual(actual_routine.dataset_id, "test_routines")
        self.assertEqual(actual_routine.routine_id, "minimal_routine")
        conn.api_request.assert_has_calls(
            [
                mock.call(
                    method="POST",
                    path="/projects/test-routine-project/datasets/test_routines/routines",
                    data=resource,
                ),
                mock.call(
                    method="GET",
                    path="/projects/test-routine-project/datasets/test_routines/routines/minimal_routine",
                ),
            ]
        )

    def test_create_table_w_day_partition(self):
        from google.cloud.bigquery.table import Table
        from google.cloud.bigquery.table import TimePartitioning

        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        table.time_partitioning = TimePartitioning()

        got = client.create_table(table)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "timePartitioning": {"type": "DAY"},
                "labels": {},
            },
        )
        self.assertEqual(table.time_partitioning.type_, "DAY")
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_custom_property(self):
        # The library should handle sending properties to the API that are not
        # yet part of the library
        from google.cloud.bigquery.table import Table

        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        resource["newAlphaProperty"] = "unreleased property"
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        table._properties["newAlphaProperty"] = "unreleased property"

        got = client.create_table(table)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "newAlphaProperty": "unreleased property",
                "labels": {},
            },
        )
        self.assertEqual(got._properties["newAlphaProperty"], "unreleased property")
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_encryption_configuration(self):
        from google.cloud.bigquery.table import EncryptionConfiguration
        from google.cloud.bigquery.table import Table

        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        table.encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME
        )

        got = client.create_table(table)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "labels": {},
                "encryptionConfiguration": {"kmsKeyName": self.KMS_KEY_NAME},
            },
        )
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_day_partition_and_expire(self):
        from google.cloud.bigquery.table import Table
        from google.cloud.bigquery.table import TimePartitioning

        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        table.time_partitioning = TimePartitioning(expiration_ms=100)

        got = client.create_table(table)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "timePartitioning": {"type": "DAY", "expirationMs": "100"},
                "labels": {},
            },
        )
        self.assertEqual(table.time_partitioning.type_, "DAY")
        self.assertEqual(table.time_partitioning.expiration_ms, 100)
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_schema_and_query(self):
        from google.cloud.bigquery.table import Table, SchemaField

        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        query = "SELECT * from %s:%s" % (self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        resource.update(
            {
                "schema": {
                    "fields": [
                        {
                            "name": "full_name",
                            "type": "STRING",
                            "mode": "REQUIRED",
                            "description": None,
                        },
                        {
                            "name": "age",
                            "type": "INTEGER",
                            "mode": "REQUIRED",
                            "description": None,
                        },
                    ]
                },
                "view": {"query": query},
            }
        )
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF, schema=schema)
        table.view_query = query

        got = client.create_table(table)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "schema": {
                    "fields": [
                        {
                            "name": "full_name",
                            "type": "STRING",
                            "mode": "REQUIRED",
                            "description": None,
                        },
                        {
                            "name": "age",
                            "type": "INTEGER",
                            "mode": "REQUIRED",
                            "description": None,
                        },
                    ]
                },
                "view": {"query": query, "useLegacySql": False},
                "labels": {},
            },
        )
        self.assertEqual(got.table_id, self.TABLE_ID)
        self.assertEqual(got.project, self.PROJECT)
        self.assertEqual(got.dataset_id, self.DS_ID)
        self.assertEqual(got.schema, schema)
        self.assertEqual(got.view_query, query)

    def test_create_table_w_external(self):
        from google.cloud.bigquery.external_config import ExternalConfig
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.table import Table

        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        resource.update(
            {
                "externalDataConfiguration": {
                    "sourceFormat": SourceFormat.CSV,
                    "autodetect": True,
                }
            }
        )
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        ec = ExternalConfig("CSV")
        ec.autodetect = True
        table.external_data_configuration = ec

        got = client.create_table(table)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "externalDataConfiguration": {
                    "sourceFormat": SourceFormat.CSV,
                    "autodetect": True,
                },
                "labels": {},
            },
        )
        self.assertEqual(got.table_id, self.TABLE_ID)
        self.assertEqual(got.project, self.PROJECT)
        self.assertEqual(got.dataset_id, self.DS_ID)
        self.assertEqual(
            got.external_data_configuration.source_format, SourceFormat.CSV
        )
        self.assertEqual(got.external_data_configuration.autodetect, True)

    def test_create_table_w_reference(self):
        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)

        got = client.create_table(self.TABLE_REF)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "labels": {},
            },
        )
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_fully_qualified_string(self):
        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)

        got = client.create_table(
            "{}.{}.{}".format(self.PROJECT, self.DS_ID, self.TABLE_ID)
        )

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "labels": {},
            },
        )
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_string(self):
        path = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)

        got = client.create_table("{}.{}".format(self.DS_ID, self.TABLE_ID))

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/%s" % path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "labels": {},
            },
        )
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_alreadyexists_w_exists_ok_false(self):
        post_path = "/projects/{}/datasets/{}/tables".format(self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(
            google.api_core.exceptions.AlreadyExists("table already exists")
        )

        with pytest.raises(google.api_core.exceptions.AlreadyExists):
            client.create_table("{}.{}".format(self.DS_ID, self.TABLE_ID))

        conn.api_request.assert_called_once_with(
            method="POST",
            path=post_path,
            data={
                "tableReference": {
                    "projectId": self.PROJECT,
                    "datasetId": self.DS_ID,
                    "tableId": self.TABLE_ID,
                },
                "labels": {},
            },
        )

    def test_create_table_alreadyexists_w_exists_ok_true(self):
        post_path = "/projects/{}/datasets/{}/tables".format(self.PROJECT, self.DS_ID)
        get_path = "/projects/{}/datasets/{}/tables/{}".format(
            self.PROJECT, self.DS_ID, self.TABLE_ID
        )
        resource = self._make_table_resource()
        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, location=self.LOCATION
        )
        conn = client._connection = make_connection(
            google.api_core.exceptions.AlreadyExists("table already exists"), resource
        )

        got = client.create_table(
            "{}.{}".format(self.DS_ID, self.TABLE_ID), exists_ok=True
        )

        self.assertEqual(got.project, self.PROJECT)
        self.assertEqual(got.dataset_id, self.DS_ID)
        self.assertEqual(got.table_id, self.TABLE_ID)

        conn.api_request.assert_has_calls(
            [
                mock.call(
                    method="POST",
                    path=post_path,
                    data={
                        "tableReference": {
                            "projectId": self.PROJECT,
                            "datasetId": self.DS_ID,
                            "tableId": self.TABLE_ID,
                        },
                        "labels": {},
                    },
                ),
                mock.call(method="GET", path=get_path),
            ]
        )

    def test_get_model(self):
        path = "projects/%s/datasets/%s/models/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.MODEL_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        resource = {
            "modelReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "modelId": self.MODEL_ID,
            }
        }
        conn = client._connection = make_connection(resource)

        model_ref = client.dataset(self.DS_ID).model(self.MODEL_ID)
        got = client.get_model(model_ref)

        conn.api_request.assert_called_once_with(method="GET", path="/%s" % path)
        self.assertEqual(got.model_id, self.MODEL_ID)

    def test_get_model_w_string(self):
        path = "projects/%s/datasets/%s/models/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.MODEL_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        resource = {
            "modelReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "modelId": self.MODEL_ID,
            }
        }
        conn = client._connection = make_connection(resource)

        model_id = "{}.{}.{}".format(self.PROJECT, self.DS_ID, self.MODEL_ID)
        got = client.get_model(model_id)

        conn.api_request.assert_called_once_with(method="GET", path="/%s" % path)
        self.assertEqual(got.model_id, self.MODEL_ID)

    def test_get_routine(self):
        from google.cloud.bigquery.routine import Routine
        from google.cloud.bigquery.routine import RoutineReference

        full_routine_id = "test-routine-project.test_routines.minimal_routine"
        routines = [
            full_routine_id,
            Routine(full_routine_id),
            RoutineReference.from_string(full_routine_id),
        ]
        for routine in routines:
            creds = _make_credentials()
            resource = {
                "etag": "im-an-etag",
                "routineReference": {
                    "projectId": "test-routine-project",
                    "datasetId": "test_routines",
                    "routineId": "minimal_routine",
                },
                "routineType": "SCALAR_FUNCTION",
            }
            client = self._make_one(project=self.PROJECT, credentials=creds)
            conn = client._connection = make_connection(resource)

            actual_routine = client.get_routine(routine)

            conn.api_request.assert_called_once_with(
                method="GET",
                path="/projects/test-routine-project/datasets/test_routines/routines/minimal_routine",
            )
            self.assertEqual(
                actual_routine.reference,
                RoutineReference.from_string(full_routine_id),
                msg="routine={}".format(repr(routine)),
            )
            self.assertEqual(
                actual_routine.etag,
                "im-an-etag",
                msg="routine={}".format(repr(routine)),
            )
            self.assertEqual(
                actual_routine.type_,
                "SCALAR_FUNCTION",
                msg="routine={}".format(repr(routine)),
            )

    def test_get_table(self):
        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        resource = self._make_table_resource()
        conn = client._connection = make_connection(resource)
        table = client.get_table(self.TABLE_REF)

        conn.api_request.assert_called_once_with(method="GET", path="/%s" % path)
        self.assertEqual(table.table_id, self.TABLE_ID)

    def test_get_table_sets_user_agent(self):
        creds = _make_credentials()
        http = mock.create_autospec(requests.Session)
        mock_response = http.request(
            url=mock.ANY, method=mock.ANY, headers=mock.ANY, data=mock.ANY
        )
        http.reset_mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self._make_table_resource()
        user_agent_override = client_info.ClientInfo(user_agent="my-application/1.2.3")
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            client_info=user_agent_override,
            _http=http,
        )

        client.get_table(self.TABLE_REF)

        expected_user_agent = user_agent_override.to_user_agent()
        http.request.assert_called_once_with(
            url=mock.ANY,
            method="GET",
            headers={
                "X-Goog-API-Client": expected_user_agent,
                "Accept-Encoding": "gzip",
                "User-Agent": expected_user_agent,
            },
            data=mock.ANY,
        )
        self.assertIn("my-application/1.2.3", expected_user_agent)

    def test_update_dataset_w_invalid_field(self):
        from google.cloud.bigquery.dataset import Dataset

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(ValueError):
            client.update_dataset(Dataset(client.dataset(self.DS_ID)), ["foo"])

    def test_update_dataset(self):
        from google.cloud.bigquery.dataset import Dataset, AccessEntry

        PATH = "projects/%s/datasets/%s" % (self.PROJECT, self.DS_ID)
        DESCRIPTION = "DESCRIPTION"
        FRIENDLY_NAME = "TITLE"
        LOCATION = "loc"
        LABELS = {"priority": "high"}
        ACCESS = [{"role": "OWNER", "userByEmail": "phred@example.com"}]
        EXP = 17
        RESOURCE = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": "etag",
            "description": DESCRIPTION,
            "friendlyName": FRIENDLY_NAME,
            "location": LOCATION,
            "defaultTableExpirationMs": EXP,
            "labels": LABELS,
            "access": ACCESS,
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(RESOURCE, RESOURCE)
        ds = Dataset(client.dataset(self.DS_ID))
        ds.description = DESCRIPTION
        ds.friendly_name = FRIENDLY_NAME
        ds.location = LOCATION
        ds.default_table_expiration_ms = EXP
        ds.labels = LABELS
        ds.access_entries = [AccessEntry("OWNER", "userByEmail", "phred@example.com")]
        ds2 = client.update_dataset(
            ds, ["description", "friendly_name", "location", "labels", "access_entries"]
        )
        conn.api_request.assert_called_once_with(
            method="PATCH",
            data={
                "description": DESCRIPTION,
                "friendlyName": FRIENDLY_NAME,
                "location": LOCATION,
                "labels": LABELS,
                "access": ACCESS,
            },
            path="/" + PATH,
            headers=None,
        )
        self.assertEqual(ds2.description, ds.description)
        self.assertEqual(ds2.friendly_name, ds.friendly_name)
        self.assertEqual(ds2.location, ds.location)
        self.assertEqual(ds2.labels, ds.labels)
        self.assertEqual(ds2.access_entries, ds.access_entries)

        # ETag becomes If-Match header.
        ds._properties["etag"] = "etag"
        client.update_dataset(ds, [])
        req = conn.api_request.call_args
        self.assertEqual(req[1]["headers"]["If-Match"], "etag")

    def test_update_dataset_w_custom_property(self):
        # The library should handle sending properties to the API that are not
        # yet part of the library
        from google.cloud.bigquery.dataset import Dataset

        path = "/projects/%s/datasets/%s" % (self.PROJECT, self.DS_ID)
        resource = {
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "newAlphaProperty": "unreleased property",
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource)
        dataset = Dataset(client.dataset(self.DS_ID))
        dataset._properties["newAlphaProperty"] = "unreleased property"

        dataset = client.update_dataset(dataset, ["newAlphaProperty"])
        conn.api_request.assert_called_once_with(
            method="PATCH",
            data={"newAlphaProperty": "unreleased property"},
            path=path,
            headers=None,
        )

        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(dataset._properties["newAlphaProperty"], "unreleased property")

    def test_update_model(self):
        from google.cloud.bigquery.model import Model

        path = "projects/%s/datasets/%s/models/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.MODEL_ID,
        )
        description = "description"
        title = "title"
        expires = datetime.datetime(
            2012, 12, 21, 16, 0, 0, tzinfo=google.cloud._helpers.UTC
        )
        resource = {
            "modelReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "modelId": self.MODEL_ID,
            },
            "description": description,
            "etag": "etag",
            "expirationTime": str(google.cloud._helpers._millis(expires)),
            "friendlyName": title,
            "labels": {"x": "y"},
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource, resource)
        model_id = "{}.{}.{}".format(self.PROJECT, self.DS_ID, self.MODEL_ID)
        model = Model(model_id)
        model.description = description
        model.friendly_name = title
        model.expires = expires
        model.labels = {"x": "y"}

        updated_model = client.update_model(
            model, ["description", "friendly_name", "labels", "expires"]
        )

        sent = {
            "description": description,
            "expirationTime": str(google.cloud._helpers._millis(expires)),
            "friendlyName": title,
            "labels": {"x": "y"},
        }
        conn.api_request.assert_called_once_with(
            method="PATCH", data=sent, path="/" + path, headers=None
        )
        self.assertEqual(updated_model.model_id, model.model_id)
        self.assertEqual(updated_model.description, model.description)
        self.assertEqual(updated_model.friendly_name, model.friendly_name)
        self.assertEqual(updated_model.labels, model.labels)
        self.assertEqual(updated_model.expires, model.expires)

        # ETag becomes If-Match header.
        model._proto.etag = "etag"
        client.update_model(model, [])
        req = conn.api_request.call_args
        self.assertEqual(req[1]["headers"]["If-Match"], "etag")

    def test_update_routine(self):
        from google.cloud.bigquery.routine import Routine
        from google.cloud.bigquery.routine import RoutineArgument

        full_routine_id = "routines-project.test_routines.updated_routine"
        resource = {
            "routineReference": {
                "projectId": "routines-project",
                "datasetId": "test_routines",
                "routineId": "updated_routine",
            },
            "routineType": "SCALAR_FUNCTION",
            "language": "SQL",
            "definitionBody": "x * 3",
            "arguments": [{"name": "x", "dataType": {"typeKind": "INT64"}}],
            "returnType": None,
            "someNewField": "someValue",
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource, resource)
        routine = Routine(full_routine_id)
        routine.arguments = [
            RoutineArgument(
                name="x",
                data_type=bigquery_v2.types.StandardSqlDataType(
                    type_kind=bigquery_v2.enums.StandardSqlDataType.TypeKind.INT64
                ),
            )
        ]
        routine.body = "x * 3"
        routine.language = "SQL"
        routine.type_ = "SCALAR_FUNCTION"
        routine._properties["someNewField"] = "someValue"

        actual_routine = client.update_routine(
            routine,
            ["arguments", "language", "body", "type_", "return_type", "someNewField"],
        )

        # TODO: routineReference isn't needed when the Routines API supports
        #       partial updates.
        sent = resource
        conn.api_request.assert_called_once_with(
            method="PUT",
            data=sent,
            path="/projects/routines-project/datasets/test_routines/routines/updated_routine",
            headers=None,
        )
        self.assertEqual(actual_routine.arguments, routine.arguments)
        self.assertEqual(actual_routine.body, routine.body)
        self.assertEqual(actual_routine.language, routine.language)
        self.assertEqual(actual_routine.type_, routine.type_)

        # ETag becomes If-Match header.
        routine._properties["etag"] = "im-an-etag"
        client.update_routine(routine, [])
        req = conn.api_request.call_args
        self.assertEqual(req[1]["headers"]["If-Match"], "im-an-etag")

    def test_update_table(self):
        from google.cloud.bigquery.table import Table, SchemaField

        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        description = "description"
        title = "title"
        resource = self._make_table_resource()
        resource.update(
            {
                "schema": {
                    "fields": [
                        {
                            "name": "full_name",
                            "type": "STRING",
                            "mode": "REQUIRED",
                            "description": None,
                        },
                        {
                            "name": "age",
                            "type": "INTEGER",
                            "mode": "REQUIRED",
                            "description": None,
                        },
                    ]
                },
                "etag": "etag",
                "description": description,
                "friendlyName": title,
                "labels": {"x": "y"},
            }
        )
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource, resource)
        table = Table(self.TABLE_REF, schema=schema)
        table.description = description
        table.friendly_name = title
        table.labels = {"x": "y"}

        updated_table = client.update_table(
            table, ["schema", "description", "friendly_name", "labels"]
        )

        sent = {
            "schema": {
                "fields": [
                    {
                        "name": "full_name",
                        "type": "STRING",
                        "mode": "REQUIRED",
                        "description": None,
                    },
                    {
                        "name": "age",
                        "type": "INTEGER",
                        "mode": "REQUIRED",
                        "description": None,
                    },
                ]
            },
            "description": description,
            "friendlyName": title,
            "labels": {"x": "y"},
        }
        conn.api_request.assert_called_once_with(
            method="PATCH", data=sent, path="/" + path, headers=None
        )
        self.assertEqual(updated_table.description, table.description)
        self.assertEqual(updated_table.friendly_name, table.friendly_name)
        self.assertEqual(updated_table.schema, table.schema)
        self.assertEqual(updated_table.labels, table.labels)

        # ETag becomes If-Match header.
        table._properties["etag"] = "etag"
        client.update_table(table, [])
        req = conn.api_request.call_args
        self.assertEqual(req[1]["headers"]["If-Match"], "etag")

    def test_update_table_w_custom_property(self):
        from google.cloud.bigquery.table import Table

        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        resource = self._make_table_resource()
        resource["newAlphaProperty"] = "unreleased property"
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        table._properties["newAlphaProperty"] = "unreleased property"

        updated_table = client.update_table(table, ["newAlphaProperty"])

        conn.api_request.assert_called_once_with(
            method="PATCH",
            path="/%s" % path,
            data={"newAlphaProperty": "unreleased property"},
            headers=None,
        )
        self.assertEqual(
            updated_table._properties["newAlphaProperty"], "unreleased property"
        )

    def test_update_table_only_use_legacy_sql(self):
        from google.cloud.bigquery.table import Table

        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        resource = self._make_table_resource()
        resource["view"] = {"useLegacySql": True}
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF)
        table.view_use_legacy_sql = True

        updated_table = client.update_table(table, ["view_use_legacy_sql"])

        conn.api_request.assert_called_once_with(
            method="PATCH",
            path="/%s" % path,
            data={"view": {"useLegacySql": True}},
            headers=None,
        )
        self.assertEqual(updated_table.view_use_legacy_sql, table.view_use_legacy_sql)

    def test_update_table_w_query(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis
        from google.cloud.bigquery.table import Table, SchemaField

        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        query = "select fullname, age from person_ages"
        location = "EU"
        exp_time = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)
        schema_resource = {
            "fields": [
                {
                    "name": "full_name",
                    "type": "STRING",
                    "mode": "REQUIRED",
                    "description": None,
                },
                {
                    "name": "age",
                    "type": "INTEGER",
                    "mode": "REQUIRED",
                    "description": None,
                },
            ]
        }
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        resource = self._make_table_resource()
        resource.update(
            {
                "schema": schema_resource,
                "view": {"query": query, "useLegacySql": True},
                "location": location,
                "expirationTime": _millis(exp_time),
            }
        )
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource)
        table = Table(self.TABLE_REF, schema=schema)
        table.expires = exp_time
        table.view_query = query
        table.view_use_legacy_sql = True
        updated_properties = ["schema", "view_query", "expires", "view_use_legacy_sql"]

        updated_table = client.update_table(table, updated_properties)

        self.assertEqual(updated_table.schema, table.schema)
        self.assertEqual(updated_table.view_query, table.view_query)
        self.assertEqual(updated_table.expires, table.expires)
        self.assertEqual(updated_table.view_use_legacy_sql, table.view_use_legacy_sql)
        self.assertEqual(updated_table.location, location)

        conn.api_request.assert_called_once_with(
            method="PATCH",
            path="/%s" % path,
            data={
                "view": {"query": query, "useLegacySql": True},
                "expirationTime": str(_millis(exp_time)),
                "schema": schema_resource,
            },
            headers=None,
        )

    def test_update_table_w_schema_None(self):
        # Simulate deleting schema:  not sure if back-end will actually
        # allow this operation, but the spec says it is optional.
        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        resource1 = self._make_table_resource()
        resource1.update(
            {
                "schema": {
                    "fields": [
                        {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                        {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
                    ]
                }
            }
        )
        resource2 = self._make_table_resource()
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource1, resource2)
        table = client.get_table(
            # Test with string for table ID
            "{}.{}.{}".format(
                self.TABLE_REF.project,
                self.TABLE_REF.dataset_id,
                self.TABLE_REF.table_id,
            )
        )
        table.schema = None

        updated_table = client.update_table(table, ["schema"])

        self.assertEqual(len(conn.api_request.call_args_list), 2)
        req = conn.api_request.call_args_list[1]
        self.assertEqual(req[1]["method"], "PATCH")
        sent = {"schema": None}
        self.assertEqual(req[1]["data"], sent)
        self.assertEqual(req[1]["path"], "/%s" % path)
        self.assertEqual(len(updated_table.schema), 0)

    def test_update_table_delete_property(self):
        from google.cloud.bigquery.table import Table

        description = "description"
        title = "title"
        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        resource1 = self._make_table_resource()
        resource1.update({"description": description, "friendlyName": title})
        resource2 = self._make_table_resource()
        resource2["description"] = None
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(resource1, resource2)
        table = Table(self.TABLE_REF)
        table.description = description
        table.friendly_name = title
        table2 = client.update_table(table, ["description", "friendly_name"])
        self.assertEqual(table2.description, table.description)
        table2.description = None

        table3 = client.update_table(table2, ["description"])
        self.assertEqual(len(conn.api_request.call_args_list), 2)
        req = conn.api_request.call_args_list[1]
        self.assertEqual(req[1]["method"], "PATCH")
        self.assertEqual(req[1]["path"], "/%s" % path)
        sent = {"description": None}
        self.assertEqual(req[1]["data"], sent)
        self.assertIsNone(table3.description)

    def test_list_tables_empty(self):
        path = "/projects/{}/datasets/{}/tables".format(self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection({})

        dataset = client.dataset(self.DS_ID)
        iterator = client.list_tables(dataset)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        tables = list(page)
        token = iterator.next_page_token

        self.assertEqual(tables, [])
        self.assertIsNone(token)
        conn.api_request.assert_called_once_with(
            method="GET", path=path, query_params={}
        )

    def test_list_models_empty(self):
        path = "/projects/{}/datasets/{}/models".format(self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection({})

        dataset_id = "{}.{}".format(self.PROJECT, self.DS_ID)
        iterator = client.list_models(dataset_id)
        page = six.next(iterator.pages)
        models = list(page)
        token = iterator.next_page_token

        self.assertEqual(models, [])
        self.assertIsNone(token)
        conn.api_request.assert_called_once_with(
            method="GET", path=path, query_params={}
        )

    def test_list_models_defaults(self):
        from google.cloud.bigquery.model import Model

        MODEL_1 = "model_one"
        MODEL_2 = "model_two"
        PATH = "projects/%s/datasets/%s/models" % (self.PROJECT, self.DS_ID)
        TOKEN = "TOKEN"
        DATA = {
            "nextPageToken": TOKEN,
            "models": [
                {
                    "modelReference": {
                        "modelId": MODEL_1,
                        "datasetId": self.DS_ID,
                        "projectId": self.PROJECT,
                    }
                },
                {
                    "modelReference": {
                        "modelId": MODEL_2,
                        "datasetId": self.DS_ID,
                        "projectId": self.PROJECT,
                    }
                },
            ],
        }

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(DATA)
        dataset = client.dataset(self.DS_ID)

        iterator = client.list_models(dataset)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        models = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(models), len(DATA["models"]))
        for found, expected in zip(models, DATA["models"]):
            self.assertIsInstance(found, Model)
            self.assertEqual(found.model_id, expected["modelReference"]["modelId"])
        self.assertEqual(token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={}
        )

    def test_list_models_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.list_models(client.dataset(self.DS_ID).model("foo"))

    def test_list_routines_empty(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection({})

        iterator = client.list_routines("test-routines.test_routines")
        page = six.next(iterator.pages)
        routines = list(page)
        token = iterator.next_page_token

        self.assertEqual(routines, [])
        self.assertIsNone(token)
        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/test-routines/datasets/test_routines/routines",
            query_params={},
        )

    def test_list_routines_defaults(self):
        from google.cloud.bigquery.routine import Routine

        project_id = "test-routines"
        dataset_id = "test_routines"
        path = "/projects/test-routines/datasets/test_routines/routines"
        routine_1 = "routine_one"
        routine_2 = "routine_two"
        token = "TOKEN"
        resource = {
            "nextPageToken": token,
            "routines": [
                {
                    "routineReference": {
                        "routineId": routine_1,
                        "datasetId": dataset_id,
                        "projectId": project_id,
                    }
                },
                {
                    "routineReference": {
                        "routineId": routine_2,
                        "datasetId": dataset_id,
                        "projectId": project_id,
                    }
                },
            ],
        }

        creds = _make_credentials()
        client = self._make_one(project=project_id, credentials=creds)
        conn = client._connection = make_connection(resource)
        dataset = client.dataset(dataset_id)

        iterator = client.list_routines(dataset)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        routines = list(page)
        actual_token = iterator.next_page_token

        self.assertEqual(len(routines), len(resource["routines"]))
        for found, expected in zip(routines, resource["routines"]):
            self.assertIsInstance(found, Routine)
            self.assertEqual(
                found.routine_id, expected["routineReference"]["routineId"]
            )
        self.assertEqual(actual_token, token)

        conn.api_request.assert_called_once_with(
            method="GET", path=path, query_params={}
        )

    def test_list_routines_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.list_routines(client.dataset(self.DS_ID).table("foo"))

    def test_list_tables_defaults(self):
        from google.cloud.bigquery.table import TableListItem

        TABLE_1 = "table_one"
        TABLE_2 = "table_two"
        PATH = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        TOKEN = "TOKEN"
        DATA = {
            "nextPageToken": TOKEN,
            "tables": [
                {
                    "kind": "bigquery#table",
                    "id": "%s:%s.%s" % (self.PROJECT, self.DS_ID, TABLE_1),
                    "tableReference": {
                        "tableId": TABLE_1,
                        "datasetId": self.DS_ID,
                        "projectId": self.PROJECT,
                    },
                    "type": "TABLE",
                },
                {
                    "kind": "bigquery#table",
                    "id": "%s:%s.%s" % (self.PROJECT, self.DS_ID, TABLE_2),
                    "tableReference": {
                        "tableId": TABLE_2,
                        "datasetId": self.DS_ID,
                        "projectId": self.PROJECT,
                    },
                    "type": "TABLE",
                },
            ],
        }

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(DATA)
        dataset = client.dataset(self.DS_ID)

        iterator = client.list_tables(dataset)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        tables = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(tables), len(DATA["tables"]))
        for found, expected in zip(tables, DATA["tables"]):
            self.assertIsInstance(found, TableListItem)
            self.assertEqual(found.full_table_id, expected["id"])
            self.assertEqual(found.table_type, expected["type"])
        self.assertEqual(token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={}
        )

    def test_list_tables_explicit(self):
        from google.cloud.bigquery.table import TableListItem

        TABLE_1 = "table_one"
        TABLE_2 = "table_two"
        PATH = "projects/%s/datasets/%s/tables" % (self.PROJECT, self.DS_ID)
        TOKEN = "TOKEN"
        DATA = {
            "tables": [
                {
                    "kind": "bigquery#dataset",
                    "id": "%s:%s.%s" % (self.PROJECT, self.DS_ID, TABLE_1),
                    "tableReference": {
                        "tableId": TABLE_1,
                        "datasetId": self.DS_ID,
                        "projectId": self.PROJECT,
                    },
                    "type": "TABLE",
                },
                {
                    "kind": "bigquery#dataset",
                    "id": "%s:%s.%s" % (self.PROJECT, self.DS_ID, TABLE_2),
                    "tableReference": {
                        "tableId": TABLE_2,
                        "datasetId": self.DS_ID,
                        "projectId": self.PROJECT,
                    },
                    "type": "TABLE",
                },
            ]
        }

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(DATA)
        dataset = client.dataset(self.DS_ID)

        iterator = client.list_tables(
            # Test with string for dataset ID.
            self.DS_ID,
            max_results=3,
            page_token=TOKEN,
        )
        self.assertEqual(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        tables = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(tables), len(DATA["tables"]))
        for found, expected in zip(tables, DATA["tables"]):
            self.assertIsInstance(found, TableListItem)
            self.assertEqual(found.full_table_id, expected["id"])
            self.assertEqual(found.table_type, expected["type"])
        self.assertIsNone(token)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/%s" % PATH,
            query_params={"maxResults": 3, "pageToken": TOKEN},
        )

    def test_list_tables_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.list_tables(client.dataset(self.DS_ID).table("foo"))

    def test_delete_dataset(self):
        from google.cloud.bigquery.dataset import Dataset
        from google.cloud.bigquery.dataset import DatasetReference

        ds_ref = DatasetReference(self.PROJECT, self.DS_ID)
        datasets = (ds_ref, Dataset(ds_ref), "{}.{}".format(self.PROJECT, self.DS_ID))
        PATH = "projects/%s/datasets/%s" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection(*([{}] * len(datasets)))
        for arg in datasets:
            client.delete_dataset(arg)
            conn.api_request.assert_called_with(
                method="DELETE", path="/%s" % PATH, query_params={}
            )

    def test_delete_dataset_delete_contents(self):
        from google.cloud.bigquery.dataset import Dataset

        PATH = "projects/%s/datasets/%s" % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = make_connection({}, {})
        ds_ref = client.dataset(self.DS_ID)
        for arg in (ds_ref, Dataset(ds_ref)):
            client.delete_dataset(arg, delete_contents=True)
            conn.api_request.assert_called_with(
                method="DELETE",
                path="/%s" % PATH,
                query_params={"deleteContents": "true"},
            )

    def test_delete_dataset_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_dataset(client.dataset(self.DS_ID).table("foo"))

    def test_delete_dataset_w_not_found_ok_false(self):
        path = "/projects/{}/datasets/{}".format(self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("dataset not found")
        )

        with self.assertRaises(google.api_core.exceptions.NotFound):
            client.delete_dataset(self.DS_ID)

        conn.api_request.assert_called_with(method="DELETE", path=path, query_params={})

    def test_delete_dataset_w_not_found_ok_true(self):
        path = "/projects/{}/datasets/{}".format(self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("dataset not found")
        )

        client.delete_dataset(self.DS_ID, not_found_ok=True)

        conn.api_request.assert_called_with(method="DELETE", path=path, query_params={})

    def test_delete_model(self):
        from google.cloud.bigquery.model import Model

        path = "projects/%s/datasets/%s/models/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.MODEL_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        model_id = "{}.{}.{}".format(self.PROJECT, self.DS_ID, self.MODEL_ID)
        models = (
            model_id,
            client.dataset(self.DS_ID).model(self.MODEL_ID),
            Model(model_id),
        )
        conn = client._connection = make_connection(*([{}] * len(models)))

        for arg in models:
            client.delete_model(arg)
            conn.api_request.assert_called_with(method="DELETE", path="/%s" % path)

    def test_delete_model_w_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_model(client.dataset(self.DS_ID))

    def test_delete_model_w_not_found_ok_false(self):
        path = "/projects/{}/datasets/{}/models/{}".format(
            self.PROJECT, self.DS_ID, self.MODEL_ID
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("model not found")
        )

        with self.assertRaises(google.api_core.exceptions.NotFound):
            client.delete_model("{}.{}".format(self.DS_ID, self.MODEL_ID))

        conn.api_request.assert_called_with(method="DELETE", path=path)

    def test_delete_model_w_not_found_ok_true(self):
        path = "/projects/{}/datasets/{}/models/{}".format(
            self.PROJECT, self.DS_ID, self.MODEL_ID
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("model not found")
        )

        client.delete_model(
            "{}.{}".format(self.DS_ID, self.MODEL_ID), not_found_ok=True
        )

        conn.api_request.assert_called_with(method="DELETE", path=path)

    def test_delete_routine(self):
        from google.cloud.bigquery.routine import Routine
        from google.cloud.bigquery.routine import RoutineReference

        full_routine_id = "test-routine-project.test_routines.minimal_routine"
        routines = [
            full_routine_id,
            Routine(full_routine_id),
            RoutineReference.from_string(full_routine_id),
        ]
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(*([{}] * len(routines)))

        for routine in routines:
            client.delete_routine(routine)
            conn.api_request.assert_called_with(
                method="DELETE",
                path="/projects/test-routine-project/datasets/test_routines/routines/minimal_routine",
            )

    def test_delete_routine_w_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_routine(client.dataset(self.DS_ID))

    def test_delete_routine_w_not_found_ok_false(self):
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("routine not found")
        )

        with self.assertRaises(google.api_core.exceptions.NotFound):
            client.delete_routine("routines-project.test_routines.test_routine")

        conn.api_request.assert_called_with(
            method="DELETE",
            path="/projects/routines-project/datasets/test_routines/routines/test_routine",
        )

    def test_delete_routine_w_not_found_ok_true(self):
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("routine not found")
        )

        client.delete_routine(
            "routines-project.test_routines.test_routine", not_found_ok=True
        )

        conn.api_request.assert_called_with(
            method="DELETE",
            path="/projects/routines-project/datasets/test_routines/routines/test_routine",
        )

    def test_delete_table(self):
        from google.cloud.bigquery.table import Table

        tables = (
            self.TABLE_REF,
            Table(self.TABLE_REF),
            "{}.{}.{}".format(
                self.TABLE_REF.project,
                self.TABLE_REF.dataset_id,
                self.TABLE_REF.table_id,
            ),
        )
        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(*([{}] * len(tables)))

        for arg in tables:
            client.delete_table(arg)
            conn.api_request.assert_called_with(method="DELETE", path="/%s" % path)

    def test_delete_table_w_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_table(client.dataset(self.DS_ID))

    def test_delete_table_w_not_found_ok_false(self):
        path = "/projects/{}/datasets/{}/tables/{}".format(
            self.PROJECT, self.DS_ID, self.TABLE_ID
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("table not found")
        )

        with self.assertRaises(google.api_core.exceptions.NotFound):
            client.delete_table("{}.{}".format(self.DS_ID, self.TABLE_ID))

        conn.api_request.assert_called_with(method="DELETE", path=path)

    def test_delete_table_w_not_found_ok_true(self):
        path = "/projects/{}/datasets/{}/tables/{}".format(
            self.PROJECT, self.DS_ID, self.TABLE_ID
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(
            google.api_core.exceptions.NotFound("table not found")
        )

        client.delete_table(
            "{}.{}".format(self.DS_ID, self.TABLE_ID), not_found_ok=True
        )

        conn.api_request.assert_called_with(method="DELETE", path=path)

    def test_job_from_resource_unknown_type(self):
        from google.cloud.bigquery.job import UnknownJob

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        got = client.job_from_resource({})  # Can parse redacted job.
        self.assertIsInstance(got, UnknownJob)
        self.assertEqual(got.project, self.PROJECT)

    def test_get_job_miss_w_explict_project(self):
        from google.cloud.exceptions import NotFound

        OTHER_PROJECT = "OTHER_PROJECT"
        JOB_ID = "NONESUCH"
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection()

        with self.assertRaises(NotFound):
            client.get_job(JOB_ID, project=OTHER_PROJECT, location=self.LOCATION)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/OTHER_PROJECT/jobs/NONESUCH",
            query_params={"projection": "full", "location": self.LOCATION},
        )

    def test_get_job_miss_w_client_location(self):
        from google.cloud.exceptions import NotFound

        OTHER_PROJECT = "OTHER_PROJECT"
        JOB_ID = "NONESUCH"
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds, location=self.LOCATION)
        conn = client._connection = make_connection()

        with self.assertRaises(NotFound):
            client.get_job(JOB_ID, project=OTHER_PROJECT)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/OTHER_PROJECT/jobs/NONESUCH",
            query_params={"projection": "full", "location": self.LOCATION},
        )

    def test_get_job_hit(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import WriteDisposition

        JOB_ID = "query_job"
        QUERY_DESTINATION_TABLE = "query_destination_table"
        QUERY = "SELECT * from test_dataset:test_table"
        ASYNC_QUERY_DATA = {
            "id": "{}:{}".format(self.PROJECT, JOB_ID),
            "jobReference": {"projectId": self.PROJECT, "jobId": "query_job"},
            "state": "DONE",
            "configuration": {
                "query": {
                    "query": QUERY,
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": QUERY_DESTINATION_TABLE,
                    },
                    "createDisposition": CreateDisposition.CREATE_IF_NEEDED,
                    "writeDisposition": WriteDisposition.WRITE_TRUNCATE,
                }
            },
        }
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(ASYNC_QUERY_DATA)

        job = client.get_job(JOB_ID)

        self.assertIsInstance(job, QueryJob)
        self.assertEqual(job.job_id, JOB_ID)
        self.assertEqual(job.create_disposition, CreateDisposition.CREATE_IF_NEEDED)
        self.assertEqual(job.write_disposition, WriteDisposition.WRITE_TRUNCATE)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/PROJECT/jobs/query_job",
            query_params={"projection": "full"},
        )

    def test_cancel_job_miss_w_explict_project(self):
        from google.cloud.exceptions import NotFound

        OTHER_PROJECT = "OTHER_PROJECT"
        JOB_ID = "NONESUCH"
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection()

        with self.assertRaises(NotFound):
            client.cancel_job(JOB_ID, project=OTHER_PROJECT, location=self.LOCATION)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/OTHER_PROJECT/jobs/NONESUCH/cancel",
            query_params={"projection": "full", "location": self.LOCATION},
        )

    def test_cancel_job_miss_w_client_location(self):
        from google.cloud.exceptions import NotFound

        OTHER_PROJECT = "OTHER_PROJECT"
        JOB_ID = "NONESUCH"
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds, location=self.LOCATION)
        conn = client._connection = make_connection()

        with self.assertRaises(NotFound):
            client.cancel_job(JOB_ID, project=OTHER_PROJECT)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/OTHER_PROJECT/jobs/NONESUCH/cancel",
            query_params={"projection": "full", "location": self.LOCATION},
        )

    def test_cancel_job_hit(self):
        from google.cloud.bigquery.job import QueryJob

        JOB_ID = "query_job"
        QUERY = "SELECT * from test_dataset:test_table"
        QUERY_JOB_RESOURCE = {
            "id": "{}:{}".format(self.PROJECT, JOB_ID),
            "jobReference": {"projectId": self.PROJECT, "jobId": "query_job"},
            "state": "RUNNING",
            "configuration": {"query": {"query": QUERY}},
        }
        RESOURCE = {"job": QUERY_JOB_RESOURCE}
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(RESOURCE)

        job = client.cancel_job(JOB_ID)

        self.assertIsInstance(job, QueryJob)
        self.assertEqual(job.job_id, JOB_ID)
        self.assertEqual(job.query, QUERY)

        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/PROJECT/jobs/query_job/cancel",
            query_params={"projection": "full"},
        )

    def test_list_jobs_defaults(self):
        from google.cloud.bigquery.job import CopyJob
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import ExtractJob
        from google.cloud.bigquery.job import LoadJob
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import WriteDisposition

        SOURCE_TABLE = "source_table"
        DESTINATION_TABLE = "destination_table"
        QUERY_DESTINATION_TABLE = "query_destination_table"
        SOURCE_URI = "gs://test_bucket/src_object*"
        DESTINATION_URI = "gs://test_bucket/dst_object*"
        JOB_TYPES = {
            "load_job": LoadJob,
            "copy_job": CopyJob,
            "extract_job": ExtractJob,
            "query_job": QueryJob,
        }
        PATH = "projects/%s/jobs" % self.PROJECT
        TOKEN = "TOKEN"
        QUERY = "SELECT * from test_dataset:test_table"
        ASYNC_QUERY_DATA = {
            "id": "%s:%s" % (self.PROJECT, "query_job"),
            "jobReference": {"projectId": self.PROJECT, "jobId": "query_job"},
            "state": "DONE",
            "configuration": {
                "query": {
                    "query": QUERY,
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": QUERY_DESTINATION_TABLE,
                    },
                    "createDisposition": CreateDisposition.CREATE_IF_NEEDED,
                    "writeDisposition": WriteDisposition.WRITE_TRUNCATE,
                }
            },
        }
        EXTRACT_DATA = {
            "id": "%s:%s" % (self.PROJECT, "extract_job"),
            "jobReference": {"projectId": self.PROJECT, "jobId": "extract_job"},
            "state": "DONE",
            "configuration": {
                "extract": {
                    "sourceTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": SOURCE_TABLE,
                    },
                    "destinationUris": [DESTINATION_URI],
                }
            },
        }
        COPY_DATA = {
            "id": "%s:%s" % (self.PROJECT, "copy_job"),
            "jobReference": {"projectId": self.PROJECT, "jobId": "copy_job"},
            "state": "DONE",
            "configuration": {
                "copy": {
                    "sourceTables": [
                        {
                            "projectId": self.PROJECT,
                            "datasetId": self.DS_ID,
                            "tableId": SOURCE_TABLE,
                        }
                    ],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": DESTINATION_TABLE,
                    },
                }
            },
        }
        LOAD_DATA = {
            "id": "%s:%s" % (self.PROJECT, "load_job"),
            "jobReference": {"projectId": self.PROJECT, "jobId": "load_job"},
            "state": "DONE",
            "configuration": {
                "load": {
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": SOURCE_TABLE,
                    },
                    "sourceUris": [SOURCE_URI],
                }
            },
        }
        DATA = {
            "nextPageToken": TOKEN,
            "jobs": [ASYNC_QUERY_DATA, EXTRACT_DATA, COPY_DATA, LOAD_DATA],
        }
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_jobs()
        page = six.next(iterator.pages)
        jobs = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(jobs), len(DATA["jobs"]))
        for found, expected in zip(jobs, DATA["jobs"]):
            name = expected["jobReference"]["jobId"]
            self.assertIsInstance(found, JOB_TYPES[name])
            self.assertEqual(found.job_id, name)
        self.assertEqual(token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={"projection": "full"}
        )

    def test_list_jobs_load_job_wo_sourceUris(self):
        from google.cloud.bigquery.job import LoadJob

        SOURCE_TABLE = "source_table"
        JOB_TYPES = {"load_job": LoadJob}
        PATH = "projects/%s/jobs" % self.PROJECT
        TOKEN = "TOKEN"
        LOAD_DATA = {
            "id": "%s:%s" % (self.PROJECT, "load_job"),
            "jobReference": {"projectId": self.PROJECT, "jobId": "load_job"},
            "state": "DONE",
            "configuration": {
                "load": {
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": SOURCE_TABLE,
                    }
                }
            },
        }
        DATA = {"nextPageToken": TOKEN, "jobs": [LOAD_DATA]}
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_jobs()
        page = six.next(iterator.pages)
        jobs = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(jobs), len(DATA["jobs"]))
        for found, expected in zip(jobs, DATA["jobs"]):
            name = expected["jobReference"]["jobId"]
            self.assertIsInstance(found, JOB_TYPES[name])
            self.assertEqual(found.job_id, name)
        self.assertEqual(token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={"projection": "full"}
        )

    def test_list_jobs_explicit_missing(self):
        PATH = "projects/%s/jobs" % self.PROJECT
        DATA = {}
        TOKEN = "TOKEN"
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection(DATA)

        iterator = client.list_jobs(
            max_results=1000, page_token=TOKEN, all_users=True, state_filter="done"
        )
        page = six.next(iterator.pages)
        jobs = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(jobs), 0)
        self.assertIsNone(token)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/%s" % PATH,
            query_params={
                "projection": "full",
                "maxResults": 1000,
                "pageToken": TOKEN,
                "allUsers": True,
                "stateFilter": "done",
            },
        )

    def test_list_jobs_w_project(self):
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection({})

        list(client.list_jobs(project="other-project"))

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/other-project/jobs",
            query_params={"projection": "full"},
        )

    def test_list_jobs_w_time_filter(self):
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = make_connection({})

        # One millisecond after the unix epoch.
        start_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 1000)
        # One millisecond after the the 2038 31-bit signed int rollover
        end_time = datetime.datetime(2038, 1, 19, 3, 14, 7, 1000)
        end_time_millis = (((2 ** 31) - 1) * 1000) + 1

        list(client.list_jobs(min_creation_time=start_time, max_creation_time=end_time))

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/%s/jobs" % self.PROJECT,
            query_params={
                "projection": "full",
                "minCreationTime": "1",
                "maxCreationTime": str(end_time_millis),
            },
        )

    def test_load_table_from_uri(self):
        from google.cloud.bigquery.job import LoadJob

        JOB = "job_name"
        DESTINATION = "destination_table"
        SOURCE_URI = "http://example.com/source.csv"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "load": {
                    "sourceUris": [SOURCE_URI],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": DESTINATION,
                    },
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        destination = client.dataset(self.DS_ID).table(DESTINATION)

        job = client.load_table_from_uri(SOURCE_URI, destination, job_id=JOB)

        # Check that load_table_from_uri actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/%s/jobs" % self.PROJECT, data=RESOURCE
        )

        self.assertIsInstance(job, LoadJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertIs(job.destination, destination)

        conn = client._connection = make_connection(RESOURCE)

        job = client.load_table_from_uri([SOURCE_URI], destination, job_id=JOB)
        self.assertIsInstance(job, LoadJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertIs(job.destination, destination)

    def test_load_table_from_uri_w_explicit_project(self):
        job_id = "this-is-a-job-id"
        destination_id = "destination_table"
        source_uri = "gs://example/source.csv"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {
                "load": {
                    "sourceUris": [source_uri],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": destination_id,
                    },
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(resource)
        destination = client.dataset(self.DS_ID).table(destination_id)

        client.load_table_from_uri(
            source_uri,
            destination,
            job_id=job_id,
            project="other-project",
            location=self.LOCATION,
        )

        # Check that load_table_from_uri actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_load_table_from_uri_w_client_location(self):
        job_id = "this-is-a-job-id"
        destination_id = "destination_table"
        source_uri = "gs://example/source.csv"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {
                "load": {
                    "sourceUris": [source_uri],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": destination_id,
                    },
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        client.load_table_from_uri(
            source_uri,
            # Test with string for table ID.
            "{}.{}".format(self.DS_ID, destination_id),
            job_id=job_id,
            project="other-project",
        )

        # Check that load_table_from_uri actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    @staticmethod
    def _mock_requests_response(status_code, headers, content=b""):
        return mock.Mock(
            content=content,
            headers=headers,
            status_code=status_code,
            spec=["content", "headers", "status_code"],
        )

    def _mock_transport(self, status_code, headers, content=b""):
        fake_transport = mock.Mock(spec=["request"])
        fake_response = self._mock_requests_response(
            status_code, headers, content=content
        )
        fake_transport.request.return_value = fake_response
        return fake_transport

    def _initiate_resumable_upload_helper(self, num_retries=None):
        from google.resumable_media.requests import ResumableUpload
        from google.cloud.bigquery.client import _DEFAULT_CHUNKSIZE
        from google.cloud.bigquery.client import _GENERIC_CONTENT_TYPE
        from google.cloud.bigquery.client import _get_upload_headers
        from google.cloud.bigquery.job import LoadJob
        from google.cloud.bigquery.job import LoadJobConfig
        from google.cloud.bigquery.job import SourceFormat

        # Create mocks to be checked for doing transport.
        resumable_url = "http://test.invalid?upload_id=hey-you"
        response_headers = {"location": resumable_url}
        fake_transport = self._mock_transport(http_client.OK, response_headers)
        client = self._make_one(project=self.PROJECT, _http=fake_transport)
        conn = client._connection = make_connection()

        # Create some mock arguments and call the method under test.
        data = b"goodbye gudbi gootbee"
        stream = io.BytesIO(data)
        config = LoadJobConfig()
        config.source_format = SourceFormat.CSV
        job = LoadJob(None, None, self.TABLE_REF, client, job_config=config)
        metadata = job.to_api_repr()
        upload, transport = client._initiate_resumable_upload(
            stream, metadata, num_retries
        )

        # Check the returned values.
        self.assertIsInstance(upload, ResumableUpload)
        upload_url = (
            "https://www.googleapis.com/upload/bigquery/v2/projects/"
            + self.PROJECT
            + "/jobs?uploadType=resumable"
        )
        self.assertEqual(upload.upload_url, upload_url)
        expected_headers = _get_upload_headers(conn.user_agent)
        self.assertEqual(upload._headers, expected_headers)
        self.assertFalse(upload.finished)
        self.assertEqual(upload._chunk_size, _DEFAULT_CHUNKSIZE)
        self.assertIs(upload._stream, stream)
        self.assertIsNone(upload._total_bytes)
        self.assertEqual(upload._content_type, _GENERIC_CONTENT_TYPE)
        self.assertEqual(upload.resumable_url, resumable_url)

        retry_strategy = upload._retry_strategy
        self.assertEqual(retry_strategy.max_sleep, 64.0)
        if num_retries is None:
            self.assertEqual(retry_strategy.max_cumulative_retry, 600.0)
            self.assertIsNone(retry_strategy.max_retries)
        else:
            self.assertIsNone(retry_strategy.max_cumulative_retry)
            self.assertEqual(retry_strategy.max_retries, num_retries)
        self.assertIs(transport, fake_transport)
        # Make sure we never read from the stream.
        self.assertEqual(stream.tell(), 0)

        # Check the mocks.
        request_headers = expected_headers.copy()
        request_headers["x-upload-content-type"] = _GENERIC_CONTENT_TYPE
        fake_transport.request.assert_called_once_with(
            "POST",
            upload_url,
            data=json.dumps(metadata).encode("utf-8"),
            headers=request_headers,
        )

    def test__initiate_resumable_upload(self):
        self._initiate_resumable_upload_helper()

    def test__initiate_resumable_upload_with_retry(self):
        self._initiate_resumable_upload_helper(num_retries=11)

    def _do_multipart_upload_success_helper(self, get_boundary, num_retries=None):
        from google.cloud.bigquery.client import _get_upload_headers
        from google.cloud.bigquery.job import LoadJob
        from google.cloud.bigquery.job import LoadJobConfig
        from google.cloud.bigquery.job import SourceFormat

        fake_transport = self._mock_transport(http_client.OK, {})
        client = self._make_one(project=self.PROJECT, _http=fake_transport)
        conn = client._connection = make_connection()

        # Create some mock arguments.
        data = b"Bzzzz-zap \x00\x01\xf4"
        stream = io.BytesIO(data)
        config = LoadJobConfig()
        config.source_format = SourceFormat.CSV
        job = LoadJob(None, None, self.TABLE_REF, client, job_config=config)
        metadata = job.to_api_repr()
        size = len(data)
        response = client._do_multipart_upload(stream, metadata, size, num_retries)

        # Check the mocks and the returned value.
        self.assertIs(response, fake_transport.request.return_value)
        self.assertEqual(stream.tell(), size)
        get_boundary.assert_called_once_with()

        upload_url = (
            "https://www.googleapis.com/upload/bigquery/v2/projects/"
            + self.PROJECT
            + "/jobs?uploadType=multipart"
        )
        payload = (
            b"--==0==\r\n"
            + b"content-type: application/json; charset=UTF-8\r\n\r\n"
            + json.dumps(metadata).encode("utf-8")
            + b"\r\n"
            + b"--==0==\r\n"
            + b"content-type: */*\r\n\r\n"
            + data
            + b"\r\n"
            + b"--==0==--"
        )
        headers = _get_upload_headers(conn.user_agent)
        headers["content-type"] = b'multipart/related; boundary="==0=="'
        fake_transport.request.assert_called_once_with(
            "POST", upload_url, data=payload, headers=headers
        )

    @mock.patch(u"google.resumable_media._upload.get_boundary", return_value=b"==0==")
    def test__do_multipart_upload(self, get_boundary):
        self._do_multipart_upload_success_helper(get_boundary)

    @mock.patch(u"google.resumable_media._upload.get_boundary", return_value=b"==0==")
    def test__do_multipart_upload_with_retry(self, get_boundary):
        self._do_multipart_upload_success_helper(get_boundary, num_retries=8)

    def test_copy_table(self):
        from google.cloud.bigquery.job import CopyJob

        JOB = "job_name"
        SOURCE = "source_table"
        DESTINATION = "destination_table"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "copy": {
                    "sourceTables": [
                        {
                            "projectId": self.PROJECT,
                            "datasetId": self.DS_ID,
                            "tableId": SOURCE,
                        }
                    ],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": DESTINATION,
                    },
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(SOURCE)
        destination = dataset.table(DESTINATION)

        job = client.copy_table(source, destination, job_id=JOB)

        # Check that copy_table actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/%s/jobs" % self.PROJECT, data=RESOURCE
        )

        self.assertIsInstance(job, CopyJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.sources), [source])
        self.assertIs(job.destination, destination)

        conn = client._connection = make_connection(RESOURCE)
        source2 = dataset.table(SOURCE + "2")
        job = client.copy_table([source, source2], destination, job_id=JOB)
        self.assertIsInstance(job, CopyJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.sources), [source, source2])
        self.assertIs(job.destination, destination)

    def test_copy_table_w_explicit_project(self):
        job_id = "this-is-a-job-id"
        source_id = "source_table"
        destination_id = "destination_table"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {
                "copy": {
                    "sourceTables": [
                        {
                            "projectId": self.PROJECT,
                            "datasetId": self.DS_ID,
                            "tableId": source_id,
                        }
                    ],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": destination_id,
                    },
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(resource)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(source_id)
        destination = dataset.table(destination_id)

        client.copy_table(
            source,
            destination,
            job_id=job_id,
            project="other-project",
            location=self.LOCATION,
        )

        # Check that copy_table actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_copy_table_w_client_location(self):
        job_id = "this-is-a-job-id"
        source_id = "source_table"
        destination_id = "destination_table"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {
                "copy": {
                    "sourceTables": [
                        {
                            "projectId": self.PROJECT,
                            "datasetId": self.DS_ID,
                            "tableId": source_id,
                        }
                    ],
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": destination_id,
                    },
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        client.copy_table(
            # Test with string for table IDs.
            "{}.{}".format(self.DS_ID, source_id),
            "{}.{}".format(self.DS_ID, destination_id),
            job_id=job_id,
            project="other-project",
        )

        # Check that copy_table actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_copy_table_w_source_strings(self):
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        client._connection = make_connection({})
        sources = [
            "dataset_wo_proj.some_table",
            "other_project.other_dataset.other_table",
            client.dataset("dataset_from_ref").table("table_from_ref"),
        ]
        destination = "some_project.some_dataset.destination_table"

        job = client.copy_table(sources, destination)

        expected_sources = [
            client.dataset("dataset_wo_proj").table("some_table"),
            client.dataset("other_dataset", project="other_project").table(
                "other_table"
            ),
            client.dataset("dataset_from_ref").table("table_from_ref"),
        ]
        self.assertEqual(list(job.sources), expected_sources)
        expected_destination = client.dataset(
            "some_dataset", project="some_project"
        ).table("destination_table")
        self.assertEqual(job.destination, expected_destination)

    def test_extract_table(self):
        from google.cloud.bigquery.job import ExtractJob

        JOB = "job_id"
        SOURCE = "source_table"
        DESTINATION = "gs://bucket_name/object_name"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "extract": {
                    "sourceTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": SOURCE,
                    },
                    "destinationUris": [DESTINATION],
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(SOURCE)

        job = client.extract_table(source, DESTINATION, job_id=JOB)

        # Check that extract_table actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/PROJECT/jobs", data=RESOURCE
        )

        # Check the job resource.
        self.assertIsInstance(job, ExtractJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION])

    def test_extract_table_w_explicit_project(self):
        job_id = "job_id"
        source_id = "source_table"
        destination = "gs://bucket_name/object_name"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {
                "extract": {
                    "sourceTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": source_id,
                    },
                    "destinationUris": [destination],
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(resource)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(source_id)

        client.extract_table(
            source,
            destination,
            job_id=job_id,
            project="other-project",
            location=self.LOCATION,
        )

        # Check that extract_table actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_extract_table_w_client_location(self):
        job_id = "job_id"
        source_id = "source_table"
        destination = "gs://bucket_name/object_name"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {
                "extract": {
                    "sourceTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": source_id,
                    },
                    "destinationUris": [destination],
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        client.extract_table(
            # Test with string for table ID.
            "{}.{}".format(self.DS_ID, source_id),
            destination,
            job_id=job_id,
            project="other-project",
        )

        # Check that extract_table actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_extract_table_generated_job_id(self):
        from google.cloud.bigquery.job import ExtractJob
        from google.cloud.bigquery.job import ExtractJobConfig
        from google.cloud.bigquery.job import DestinationFormat

        JOB = "job_id"
        SOURCE = "source_table"
        DESTINATION = "gs://bucket_name/object_name"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "extract": {
                    "sourceTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": SOURCE,
                    },
                    "destinationUris": [DESTINATION],
                    "destinationFormat": "NEWLINE_DELIMITED_JSON",
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(SOURCE)
        job_config = ExtractJobConfig()
        job_config.destination_format = DestinationFormat.NEWLINE_DELIMITED_JSON

        job = client.extract_table(source, DESTINATION, job_config=job_config)

        # Check that extract_table actually starts the job.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/PROJECT/jobs")
        self.assertIsInstance(req["data"]["jobReference"]["jobId"], six.string_types)

        # Check the job resource.
        self.assertIsInstance(job, ExtractJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION])

    def test_extract_table_w_destination_uris(self):
        from google.cloud.bigquery.job import ExtractJob

        JOB = "job_id"
        SOURCE = "source_table"
        DESTINATION1 = "gs://bucket_name/object_one"
        DESTINATION2 = "gs://bucket_name/object_two"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "extract": {
                    "sourceTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": SOURCE,
                    },
                    "destinationUris": [DESTINATION1, DESTINATION2],
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(SOURCE)

        job = client.extract_table(source, [DESTINATION1, DESTINATION2], job_id=JOB)

        # Check that extract_table actually starts the job.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/PROJECT/jobs")

        # Check the job resource.
        self.assertIsInstance(job, ExtractJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION1, DESTINATION2])

    def test_query_defaults(self):
        from google.cloud.bigquery.job import QueryJob

        QUERY = "select count(*) from persons"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": "some-random-id"},
            "configuration": {"query": {"query": QUERY, "useLegacySql": False}},
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)

        job = client.query(QUERY)

        self.assertIsInstance(job, QueryJob)
        self.assertIsInstance(job.job_id, six.string_types)
        self.assertIs(job._client, client)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, [])

        # Check that query actually starts the job.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/PROJECT/jobs")
        sent = req["data"]
        self.assertIsInstance(sent["jobReference"]["jobId"], six.string_types)
        sent_config = sent["configuration"]["query"]
        self.assertEqual(sent_config["query"], QUERY)
        self.assertFalse(sent_config["useLegacySql"])

    def test_query_w_explicit_project(self):
        job_id = "some-job-id"
        query = "select count(*) from persons"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {"query": {"query": query, "useLegacySql": False}},
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(resource)

        client.query(
            query, job_id=job_id, project="other-project", location=self.LOCATION
        )

        # Check that query actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_query_w_explicit_job_config(self):
        job_id = "some-job-id"
        query = "select count(*) from persons"
        resource = {
            "jobReference": {
                "jobId": job_id,
                "projectId": self.PROJECT,
                "location": self.LOCATION,
            },
            "configuration": {
                "query": {
                    "query": query,
                    "defaultDataset": {
                        "projectId": self.PROJECT,
                        "datasetId": "some-dataset",
                    },
                    "useLegacySql": False,
                    "useQueryCache": True,
                    "maximumBytesBilled": "2000",
                }
            },
        }

        creds = _make_credentials()
        http = object()

        from google.cloud.bigquery import QueryJobConfig, DatasetReference

        default_job_config = QueryJobConfig()
        default_job_config.default_dataset = DatasetReference(
            self.PROJECT, "some-dataset"
        )
        default_job_config.maximum_bytes_billed = 1000

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            default_query_job_config=default_job_config,
        )
        conn = client._connection = make_connection(resource)

        job_config = QueryJobConfig()
        job_config.use_query_cache = True
        job_config.maximum_bytes_billed = 2000

        client.query(
            query, job_id=job_id, location=self.LOCATION, job_config=job_config
        )

        # Check that query actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/PROJECT/jobs", data=resource
        )

    def test_query_w_explicit_job_config_override(self):
        job_id = "some-job-id"
        query = "select count(*) from persons"
        resource = {
            "jobReference": {
                "jobId": job_id,
                "projectId": self.PROJECT,
                "location": self.LOCATION,
            },
            "configuration": {
                "query": {
                    "query": query,
                    "defaultDataset": None,
                    "useLegacySql": False,
                    "useQueryCache": True,
                    "maximumBytesBilled": "2000",
                }
            },
        }

        creds = _make_credentials()
        http = object()

        from google.cloud.bigquery import QueryJobConfig, DatasetReference

        default_job_config = QueryJobConfig()
        default_job_config.default_dataset = DatasetReference(
            self.PROJECT, "some-dataset"
        )
        default_job_config.maximum_bytes_billed = 1000

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            default_query_job_config=default_job_config,
        )
        conn = client._connection = make_connection(resource)

        job_config = QueryJobConfig()
        job_config.use_query_cache = True
        job_config.maximum_bytes_billed = 2000
        job_config.default_dataset = None

        client.query(
            query, job_id=job_id, location=self.LOCATION, job_config=job_config
        )

        # Check that query actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/PROJECT/jobs", data=resource
        )

    def test_query_w_client_default_config_no_incoming(self):
        job_id = "some-job-id"
        query = "select count(*) from persons"
        resource = {
            "jobReference": {
                "jobId": job_id,
                "projectId": self.PROJECT,
                "location": self.LOCATION,
            },
            "configuration": {
                "query": {
                    "query": query,
                    "useLegacySql": False,
                    "maximumBytesBilled": "1000",
                }
            },
        }

        creds = _make_credentials()
        http = object()

        from google.cloud.bigquery import QueryJobConfig

        default_job_config = QueryJobConfig()
        default_job_config.maximum_bytes_billed = 1000

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            default_query_job_config=default_job_config,
        )
        conn = client._connection = make_connection(resource)

        client.query(query, job_id=job_id, location=self.LOCATION)

        # Check that query actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/PROJECT/jobs", data=resource
        )

    def test_query_w_client_location(self):
        job_id = "some-job-id"
        query = "select count(*) from persons"
        resource = {
            "jobReference": {
                "projectId": "other-project",
                "location": self.LOCATION,
                "jobId": job_id,
            },
            "configuration": {"query": {"query": query, "useLegacySql": False}},
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http, location=self.LOCATION
        )
        conn = client._connection = make_connection(resource)

        client.query(query, job_id=job_id, project="other-project")

        # Check that query actually starts the job.
        conn.api_request.assert_called_once_with(
            method="POST", path="/projects/other-project/jobs", data=resource
        )

    def test_query_detect_location(self):
        query = "select count(*) from persons"
        resource_location = "EU"
        resource = {
            "jobReference": {
                "projectId": self.PROJECT,
                # Location not set in request, but present in the response.
                "location": resource_location,
                "jobId": "some-random-id",
            },
            "configuration": {"query": {"query": query, "useLegacySql": False}},
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(resource)

        job = client.query(query)

        self.assertEqual(job.location, resource_location)

        # Check that request did not contain a location.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        sent = req["data"]
        self.assertIsNone(sent["jobReference"].get("location"))

    def test_query_w_udf_resources(self):
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = "gs://some-bucket/js/lib.js"
        JOB = "job_name"
        QUERY = "select count(*) from persons"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "query": {
                    "query": QUERY,
                    "useLegacySql": True,
                    "userDefinedFunctionResources": [{"resourceUri": RESOURCE_URI}],
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        config.use_legacy_sql = True

        job = client.query(QUERY, job_config=config, job_id=JOB)

        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, udf_resources)
        self.assertEqual(job.query_parameters, [])

        # Check that query actually starts the job.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/PROJECT/jobs")
        sent = req["data"]
        self.assertIsInstance(sent["jobReference"]["jobId"], six.string_types)
        sent_config = sent["configuration"]["query"]
        self.assertEqual(sent_config["query"], QUERY)
        self.assertTrue(sent_config["useLegacySql"])
        self.assertEqual(
            sent_config["userDefinedFunctionResources"][0],
            {"resourceUri": RESOURCE_URI},
        )

    def test_query_w_query_parameters(self):
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        JOB = "job_name"
        QUERY = "select count(*) from persons"
        RESOURCE = {
            "jobReference": {"projectId": self.PROJECT, "jobId": JOB},
            "configuration": {
                "query": {
                    "query": QUERY,
                    "useLegacySql": False,
                    "queryParameters": [
                        {
                            "name": "foo",
                            "parameterType": {"type": "INT64"},
                            "parameterValue": {"value": "123"},
                        }
                    ],
                }
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESOURCE)
        query_parameters = [ScalarQueryParameter("foo", "INT64", 123)]
        config = QueryJobConfig()
        config.query_parameters = query_parameters

        job = client.query(QUERY, job_config=config, job_id=JOB)

        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, query_parameters)

        # Check that query actually starts the job.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/PROJECT/jobs")
        sent = req["data"]
        self.assertEqual(sent["jobReference"]["jobId"], JOB)
        sent_config = sent["configuration"]["query"]
        self.assertEqual(sent_config["query"], QUERY)
        self.assertFalse(sent_config["useLegacySql"])
        self.assertEqual(
            sent_config["queryParameters"][0],
            {
                "name": "foo",
                "parameterType": {"type": "INT64"},
                "parameterValue": {"value": "123"},
            },
        )

    def test_insert_rows_wo_schema(self):
        from google.cloud.bigquery.table import Table

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        table = Table(self.TABLE_REF)
        ROWS = [
            ("Phred Phlyntstone", 32),
            ("Bharney Rhubble", 33),
            ("Wylma Phlyntstone", 29),
            ("Bhettye Rhubble", 27),
        ]

        with self.assertRaises(ValueError) as exc:
            client.insert_rows(table, ROWS)

        self.assertIn("Could not determine schema for table", exc.exception.args[0])

    def test_insert_rows_w_schema(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import _microseconds_from_datetime
        from google.cloud.bigquery.table import SchemaField

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(tzinfo=UTC)
        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField("joined", "TIMESTAMP", mode="NULLABLE"),
        ]
        ROWS = [
            ("Phred Phlyntstone", 32, _datetime_to_rfc3339(WHEN)),
            ("Bharney Rhubble", 33, WHEN + datetime.timedelta(seconds=1)),
            ("Wylma Phlyntstone", 29, WHEN + datetime.timedelta(seconds=2)),
            ("Bhettye Rhubble", 27, None),
        ]

        def _row_data(row):
            joined = row[2]
            if isinstance(row[2], datetime.datetime):
                joined = _microseconds_from_datetime(joined) * 1e-6
            return {"full_name": row[0], "age": str(row[1]), "joined": joined}

        SENT = {
            "rows": [
                {"json": _row_data(row), "insertId": str(i)}
                for i, row in enumerate(ROWS)
            ]
        }

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(ROWS)))):
            # Test with using string IDs for the table.
            errors = client.insert_rows(
                "{}.{}".format(self.DS_ID, self.TABLE_ID), ROWS, selected_fields=schema
            )

        self.assertEqual(len(errors), 0)
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/%s" % PATH)
        self.assertEqual(req["data"], SENT)

    def test_insert_rows_w_list_of_dictionaries(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import _microseconds_from_datetime
        from google.cloud.bigquery.table import Table, SchemaField

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(tzinfo=UTC)
        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField("joined", "TIMESTAMP", mode="NULLABLE"),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        ROWS = [
            {
                "full_name": "Phred Phlyntstone",
                "age": 32,
                "joined": _datetime_to_rfc3339(WHEN),
            },
            {
                "full_name": "Bharney Rhubble",
                "age": 33,
                "joined": WHEN + datetime.timedelta(seconds=1),
            },
            {
                "full_name": "Wylma Phlyntstone",
                "age": 29,
                "joined": WHEN + datetime.timedelta(seconds=2),
            },
            {"full_name": "Bhettye Rhubble", "age": 27, "joined": None},
        ]

        def _row_data(row):
            joined = row["joined"]
            if isinstance(joined, datetime.datetime):
                row["joined"] = _microseconds_from_datetime(joined) * 1e-6
            row["age"] = str(row["age"])
            return row

        SENT = {
            "rows": [
                {"json": _row_data(row), "insertId": str(i)}
                for i, row in enumerate(ROWS)
            ]
        }

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(ROWS)))):
            errors = client.insert_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        conn.api_request.assert_called_once_with(
            method="POST", path="/%s" % PATH, data=SENT
        )

    def test_insert_rows_w_list_of_Rows(self):
        from google.cloud.bigquery.table import Table
        from google.cloud.bigquery.table import SchemaField
        from google.cloud.bigquery.table import Row

        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        f2i = {"full_name": 0, "age": 1}
        ROWS = [
            Row(("Phred Phlyntstone", 32), f2i),
            Row(("Bharney Rhubble", 33), f2i),
            Row(("Wylma Phlyntstone", 29), f2i),
            Row(("Bhettye Rhubble", 27), f2i),
        ]

        def _row_data(row):
            return {"full_name": row[0], "age": str(row[1])}

        SENT = {
            "rows": [
                {"json": _row_data(row), "insertId": str(i)}
                for i, row in enumerate(ROWS)
            ]
        }

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(ROWS)))):
            errors = client.insert_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        conn.api_request.assert_called_once_with(
            method="POST", path="/%s" % PATH, data=SENT
        )

    def test_insert_rows_w_skip_invalid_and_ignore_unknown(self):
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        RESPONSE = {
            "insertErrors": [
                {
                    "index": 1,
                    "errors": [
                        {
                            "reason": "REASON",
                            "location": "LOCATION",
                            "debugInfo": "INFO",
                            "message": "MESSAGE",
                        }
                    ],
                }
            ]
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(RESPONSE)
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField("voter", "BOOLEAN", mode="NULLABLE"),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        ROWS = [
            ("Phred Phlyntstone", 32, True),
            ("Bharney Rhubble", 33, False),
            ("Wylma Phlyntstone", 29, True),
            ("Bhettye Rhubble", 27, True),
        ]

        def _row_data(row):
            return {
                "full_name": row[0],
                "age": str(row[1]),
                "voter": row[2] and "true" or "false",
            }

        SENT = {
            "skipInvalidRows": True,
            "ignoreUnknownValues": True,
            "templateSuffix": "20160303",
            "rows": [
                {"insertId": index, "json": _row_data(row)}
                for index, row in enumerate(ROWS)
            ],
        }

        errors = client.insert_rows(
            table,
            ROWS,
            row_ids=[index for index, _ in enumerate(ROWS)],
            skip_invalid_rows=True,
            ignore_unknown_values=True,
            template_suffix="20160303",
        )

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["index"], 1)
        self.assertEqual(len(errors[0]["errors"]), 1)
        self.assertEqual(
            errors[0]["errors"][0], RESPONSE["insertErrors"][0]["errors"][0]
        )
        conn.api_request.assert_called_once_with(
            method="POST", path="/%s" % PATH, data=SENT
        )

    def test_insert_rows_w_repeated_fields(self):
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        color = SchemaField("color", "STRING", mode="REPEATED")
        items = SchemaField("items", "INTEGER", mode="REPEATED")
        score = SchemaField("score", "INTEGER")
        times = SchemaField("times", "TIMESTAMP", mode="REPEATED")
        distances = SchemaField("distances", "FLOAT", mode="REPEATED")
        structs = SchemaField(
            "structs", "RECORD", mode="REPEATED", fields=[score, times, distances]
        )
        table = Table(self.TABLE_REF, schema=[color, items, structs])
        ROWS = [
            (
                ["red", "green"],
                [1, 2],
                [
                    (
                        12,
                        [
                            datetime.datetime(2018, 12, 1, 12, 0, 0, tzinfo=pytz.utc),
                            datetime.datetime(2018, 12, 1, 13, 0, 0, tzinfo=pytz.utc),
                        ],
                        [1.25, 2.5],
                    ),
                    {
                        "score": 13,
                        "times": [
                            datetime.datetime(2018, 12, 2, 12, 0, 0, tzinfo=pytz.utc),
                            datetime.datetime(2018, 12, 2, 13, 0, 0, tzinfo=pytz.utc),
                        ],
                        "distances": [-1.25, -2.5],
                    },
                ],
            ),
            {"color": None, "items": [], "structs": [(None, [], [3.5])]},
        ]

        SENT = {
            "rows": [
                {
                    "json": {
                        "color": ["red", "green"],
                        "items": ["1", "2"],
                        "structs": [
                            {
                                "score": "12",
                                "times": [
                                    1543665600.0,  # 2018-12-01 12:00 UTC
                                    1543669200.0,  # 2018-12-01 13:00 UTC
                                ],
                                "distances": [1.25, 2.5],
                            },
                            {
                                "score": "13",
                                "times": [
                                    1543752000.0,  # 2018-12-02 12:00 UTC
                                    1543755600.0,  # 2018-12-02 13:00 UTC
                                ],
                                "distances": [-1.25, -2.5],
                            },
                        ],
                    },
                    "insertId": "0",
                },
                {
                    "json": {
                        "color": None,
                        "items": [],
                        "structs": [{"score": None, "times": [], "distances": [3.5]}],
                    },
                    "insertId": "1",
                },
            ]
        }

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(ROWS)))):
            errors = client.insert_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        conn.api_request.assert_called_once_with(
            method="POST", path="/%s" % PATH, data=SENT
        )

    def test_insert_rows_w_record_schema(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        area_code = SchemaField("area_code", "STRING", "REQUIRED")
        local_number = SchemaField("local_number", "STRING", "REQUIRED")
        rank = SchemaField("rank", "INTEGER", "REQUIRED")
        phone = SchemaField(
            "phone", "RECORD", mode="NULLABLE", fields=[area_code, local_number, rank]
        )
        ROWS = [
            (
                "Phred Phlyntstone",
                {"area_code": "800", "local_number": "555-1212", "rank": 1},
            ),
            ("Bharney Rhubble", ("877", "768-5309", 2)),
            ("Wylma Phlyntstone", None),
        ]

        SENT = {
            "rows": [
                {
                    "json": {
                        "full_name": "Phred Phlyntstone",
                        "phone": {
                            "area_code": "800",
                            "local_number": "555-1212",
                            "rank": "1",
                        },
                    },
                    "insertId": "0",
                },
                {
                    "json": {
                        "full_name": "Bharney Rhubble",
                        "phone": {
                            "area_code": "877",
                            "local_number": "768-5309",
                            "rank": "2",
                        },
                    },
                    "insertId": "1",
                },
                {
                    "json": {"full_name": "Wylma Phlyntstone", "phone": None},
                    "insertId": "2",
                },
            ]
        }

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(ROWS)))):
            errors = client.insert_rows(
                self.TABLE_REF, ROWS, selected_fields=[full_name, phone]
            )

        self.assertEqual(len(errors), 0)
        conn.api_request.assert_called_once_with(
            method="POST", path="/%s" % PATH, data=SENT
        )

    def test_insert_rows_errors(self):
        from google.cloud.bigquery.table import Table

        ROWS = [
            ("Phred Phlyntstone", 32, True),
            ("Bharney Rhubble", 33, False),
            ("Wylma Phlyntstone", 29, True),
            ("Bhettye Rhubble", 27, True),
        ]
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)

        # table ref with no selected fields
        with self.assertRaises(ValueError):
            client.insert_rows(self.TABLE_REF, ROWS)

        # table with no schema
        with self.assertRaises(ValueError):
            client.insert_rows(Table(self.TABLE_REF), ROWS)

        # neither Table nor tableReference
        with self.assertRaises(TypeError):
            client.insert_rows(1, ROWS)

    def test_insert_rows_w_numeric(self):
        from google.cloud.bigquery import table

        project = "PROJECT"
        ds_id = "DS_ID"
        table_id = "TABLE_ID"
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=project, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        table_ref = DatasetReference(project, ds_id).table(table_id)
        schema = [
            table.SchemaField("account", "STRING"),
            table.SchemaField("balance", "NUMERIC"),
        ]
        insert_table = table.Table(table_ref, schema=schema)
        rows = [
            ("Savings", decimal.Decimal("23.47")),
            ("Checking", decimal.Decimal("1.98")),
            ("Mortgage", decimal.Decimal("-12345678909.87654321")),
        ]

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(rows)))):
            errors = client.insert_rows(insert_table, rows)

        self.assertEqual(len(errors), 0)
        rows_json = [
            {"account": "Savings", "balance": "23.47"},
            {"account": "Checking", "balance": "1.98"},
            {"account": "Mortgage", "balance": "-12345678909.87654321"},
        ]
        sent = {
            "rows": [
                {"json": row, "insertId": str(i)} for i, row in enumerate(rows_json)
            ]
        }
        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/{}/datasets/{}/tables/{}/insertAll".format(
                project, ds_id, table_id
            ),
            data=sent,
        )

    def test_insert_rows_json(self):
        from google.cloud.bigquery.table import Table, SchemaField
        from google.cloud.bigquery.dataset import DatasetReference

        PROJECT = "PROJECT"
        DS_ID = "DS_ID"
        TABLE_ID = "TABLE_ID"
        PATH = "projects/%s/datasets/%s/tables/%s/insertAll" % (
            PROJECT,
            DS_ID,
            TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection({})
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField("joined", "TIMESTAMP", mode="NULLABLE"),
        ]
        table = Table(table_ref, schema=schema)
        ROWS = [
            {
                "full_name": "Phred Phlyntstone",
                "age": "32",
                "joined": "2015-07-24T19:53:19.006000Z",
            },
            {"full_name": "Bharney Rhubble", "age": "33", "joined": 1437767600.006},
            {"full_name": "Wylma Phlyntstone", "age": "29", "joined": 1437767601.006},
            {"full_name": "Bhettye Rhubble", "age": "27", "joined": None},
        ]

        SENT = {
            "rows": [{"json": row, "insertId": str(i)} for i, row in enumerate(ROWS)]
        }

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(ROWS)))):
            errors = client.insert_rows_json(table, ROWS)

        self.assertEqual(len(errors), 0)
        conn.api_request.assert_called_once_with(
            method="POST", path="/%s" % PATH, data=SENT
        )

    def test_insert_rows_json_with_string_id(self):
        rows = [{"col1": "val1"}]
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project="default-project", credentials=creds, _http=http
        )
        conn = client._connection = make_connection({})

        with mock.patch("uuid.uuid4", side_effect=map(str, range(len(rows)))):
            errors = client.insert_rows_json("proj.dset.tbl", rows)

        self.assertEqual(len(errors), 0)
        expected = {
            "rows": [{"json": row, "insertId": str(i)} for i, row in enumerate(rows)]
        }
        conn.api_request.assert_called_once_with(
            method="POST",
            path="/projects/proj/datasets/dset/tables/tbl/insertAll",
            data=expected,
        )

    def test_list_partitions(self):
        from google.cloud.bigquery.table import Table

        rows = 3
        meta_info = _make_list_partitons_meta_info(
            self.PROJECT, self.DS_ID, self.TABLE_ID, rows
        )

        data = {
            "totalRows": str(rows),
            "rows": [
                {"f": [{"v": "20180101"}]},
                {"f": [{"v": "20180102"}]},
                {"f": [{"v": "20180103"}]},
            ],
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        client._connection = make_connection(meta_info, data)
        table = Table(self.TABLE_REF)

        partition_list = client.list_partitions(table)
        self.assertEqual(len(partition_list), rows)
        self.assertIn("20180102", partition_list)

    def test_list_partitions_with_string_id(self):
        meta_info = _make_list_partitons_meta_info(
            self.PROJECT, self.DS_ID, self.TABLE_ID, 0
        )

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        client._connection = make_connection(meta_info, {})

        partition_list = client.list_partitions(
            "{}.{}".format(self.DS_ID, self.TABLE_ID)
        )

        self.assertEqual(len(partition_list), 0)

    def test_list_rows(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.table import Table
        from google.cloud.bigquery.table import SchemaField
        from google.cloud.bigquery.table import Row

        PATH = "projects/%s/datasets/%s/tables/%s/data" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(tzinfo=UTC)
        WHEN_1 = WHEN + datetime.timedelta(seconds=1)
        WHEN_2 = WHEN + datetime.timedelta(seconds=2)
        ROWS = 1234
        TOKEN = "TOKEN"

        def _bigquery_timestamp_float_repr(ts_float):
            # Preserve microsecond precision for E+09 timestamps
            return "%0.15E" % (ts_float,)

        DATA = {
            "totalRows": str(ROWS),
            "pageToken": TOKEN,
            "rows": [
                {
                    "f": [
                        {"v": "Phred Phlyntstone"},
                        {"v": "32"},
                        {"v": _bigquery_timestamp_float_repr(WHEN_TS)},
                    ]
                },
                {
                    "f": [
                        {"v": "Bharney Rhubble"},
                        {"v": "33"},
                        {"v": _bigquery_timestamp_float_repr(WHEN_TS + 1)},
                    ]
                },
                {
                    "f": [
                        {"v": "Wylma Phlyntstone"},
                        {"v": "29"},
                        {"v": _bigquery_timestamp_float_repr(WHEN_TS + 2)},
                    ]
                },
                {"f": [{"v": "Bhettye Rhubble"}, {"v": None}, {"v": None}]},
            ],
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(DATA, DATA)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="NULLABLE")
        joined = SchemaField("joined", "TIMESTAMP", mode="NULLABLE")
        table = Table(self.TABLE_REF, schema=[full_name, age, joined])

        iterator = client.list_rows(table)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        f2i = {"full_name": 0, "age": 1, "joined": 2}
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], Row(("Phred Phlyntstone", 32, WHEN), f2i))
        self.assertEqual(rows[1], Row(("Bharney Rhubble", 33, WHEN_1), f2i))
        self.assertEqual(rows[2], Row(("Wylma Phlyntstone", 29, WHEN_2), f2i))
        self.assertEqual(rows[3], Row(("Bhettye Rhubble", None, None), f2i))
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={}
        )

    def test_list_rows_empty_table(self):
        response = {"totalRows": "0", "rows": []}
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        client._connection = make_connection(response, response)

        # Table that has no schema because it's an empty table.
        rows = client.list_rows(
            # Test with using a string for the table ID.
            "{}.{}.{}".format(
                self.TABLE_REF.project,
                self.TABLE_REF.dataset_id,
                self.TABLE_REF.table_id,
            ),
            selected_fields=[],
        )

        # When a table reference / string and selected_fields is provided,
        # total_rows can't be populated until iteration starts.
        self.assertIsNone(rows.total_rows)
        self.assertEqual(tuple(rows), ())
        self.assertEqual(rows.total_rows, 0)

    def test_list_rows_query_params(self):
        from google.cloud.bigquery.table import Table, SchemaField

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        table = Table(
            self.TABLE_REF, schema=[SchemaField("age", "INTEGER", mode="NULLABLE")]
        )
        tests = [
            ({}, {}),
            ({"start_index": 1}, {"startIndex": 1}),
            ({"max_results": 2}, {"maxResults": 2}),
            ({"start_index": 1, "max_results": 2}, {"startIndex": 1, "maxResults": 2}),
        ]
        conn = client._connection = make_connection(*len(tests) * [{}])
        for i, test in enumerate(tests):
            iterator = client.list_rows(table, **test[0])
            six.next(iterator.pages)
            req = conn.api_request.call_args_list[i]
            self.assertEqual(req[1]["query_params"], test[1], "for kwargs %s" % test[0])

    def test_list_rows_repeated_fields(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = "projects/%s/datasets/%s/tables/%s/data" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        ROWS = 1234
        TOKEN = "TOKEN"
        DATA = {
            "totalRows": ROWS,
            "pageToken": TOKEN,
            "rows": [
                {
                    "f": [
                        {"v": [{"v": "red"}, {"v": "green"}]},
                        {
                            "v": [
                                {
                                    "v": {
                                        "f": [
                                            {"v": [{"v": "1"}, {"v": "2"}]},
                                            {"v": [{"v": "3.1415"}, {"v": "1.414"}]},
                                        ]
                                    }
                                }
                            ]
                        },
                    ]
                }
            ],
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(DATA)
        color = SchemaField("color", "STRING", mode="REPEATED")
        index = SchemaField("index", "INTEGER", "REPEATED")
        score = SchemaField("score", "FLOAT", "REPEATED")
        struct = SchemaField("struct", "RECORD", mode="REPEATED", fields=[index, score])

        iterator = client.list_rows(self.TABLE_REF, selected_fields=[color, struct])
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], ["red", "green"])
        self.assertEqual(rows[0][1], [{"index": [1, 2], "score": [3.1415, 1.414]}])
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/%s" % PATH,
            query_params={"selectedFields": "color,struct"},
        )

    def test_list_rows_w_record_schema(self):
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = "projects/%s/datasets/%s/tables/%s/data" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        ROWS = 1234
        TOKEN = "TOKEN"
        DATA = {
            "totalRows": ROWS,
            "pageToken": TOKEN,
            "rows": [
                {
                    "f": [
                        {"v": "Phred Phlyntstone"},
                        {"v": {"f": [{"v": "800"}, {"v": "555-1212"}, {"v": 1}]}},
                    ]
                },
                {
                    "f": [
                        {"v": "Bharney Rhubble"},
                        {"v": {"f": [{"v": "877"}, {"v": "768-5309"}, {"v": 2}]}},
                    ]
                },
                {"f": [{"v": "Wylma Phlyntstone"}, {"v": None}]},
            ],
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._connection = make_connection(DATA)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        area_code = SchemaField("area_code", "STRING", "REQUIRED")
        local_number = SchemaField("local_number", "STRING", "REQUIRED")
        rank = SchemaField("rank", "INTEGER", "REQUIRED")
        phone = SchemaField(
            "phone", "RECORD", mode="NULLABLE", fields=[area_code, local_number, rank]
        )
        table = Table(self.TABLE_REF, schema=[full_name, phone])

        iterator = client.list_rows(table)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][0], "Phred Phlyntstone")
        self.assertEqual(
            rows[0][1], {"area_code": "800", "local_number": "555-1212", "rank": 1}
        )
        self.assertEqual(rows[1][0], "Bharney Rhubble")
        self.assertEqual(
            rows[1][1], {"area_code": "877", "local_number": "768-5309", "rank": 2}
        )
        self.assertEqual(rows[2][0], "Wylma Phlyntstone")
        self.assertIsNone(rows[2][1])
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % PATH, query_params={}
        )

    def test_list_rows_with_missing_schema(self):
        from google.cloud.bigquery.table import Table, TableListItem

        table_path = "/projects/{}/datasets/{}/tables/{}".format(
            self.PROJECT, self.DS_ID, self.TABLE_ID
        )
        tabledata_path = "{}/data".format(table_path)

        table_list_item_data = {
            "id": "%s:%s:%s" % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            "tableReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "tableId": self.TABLE_ID,
            },
        }
        table_data = copy.deepcopy(table_list_item_data)
        # Intentionally make wrong, since total_rows can update during iteration.
        table_data["numRows"] = 2
        table_data["schema"] = {
            "fields": [
                {"name": "name", "type": "STRING"},
                {"name": "age", "type": "INTEGER"},
            ]
        }
        rows_data = {
            "totalRows": 3,
            "pageToken": None,
            "rows": [
                {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
                {"f": [{"v": "Bharney Rhubble"}, {"v": "31"}]},
                {"f": [{"v": "Wylma Phlyntstone"}, {"v": None}]},
            ],
        }

        creds = _make_credentials()
        http = object()

        schemaless_tables = (
            "{}.{}".format(self.DS_ID, self.TABLE_ID),
            self.TABLE_REF,
            Table(self.TABLE_REF),
            TableListItem(table_list_item_data),
        )

        for table in schemaless_tables:
            client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
            conn = client._connection = make_connection(table_data, rows_data)

            row_iter = client.list_rows(table)

            conn.api_request.assert_called_once_with(method="GET", path=table_path)
            conn.api_request.reset_mock()
            self.assertEqual(row_iter.total_rows, 2, msg=repr(table))

            rows = list(row_iter)
            conn.api_request.assert_called_once_with(
                method="GET", path=tabledata_path, query_params={}
            )
            self.assertEqual(row_iter.total_rows, 3, msg=repr(table))
            self.assertEqual(rows[0].name, "Phred Phlyntstone", msg=repr(table))
            self.assertEqual(rows[1].age, 31, msg=repr(table))
            self.assertIsNone(rows[2].age, msg=repr(table))

    def test_list_rows_error(self):
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)

        # neither Table nor tableReference
        with self.assertRaises(TypeError):
            client.list_rows(1)


class Test_make_job_id(unittest.TestCase):
    def _call_fut(self, job_id, prefix=None):
        from google.cloud.bigquery.client import _make_job_id

        return _make_job_id(job_id, prefix=prefix)

    def test__make_job_id_wo_suffix(self):
        job_id = self._call_fut("job_id")

        self.assertEqual(job_id, "job_id")

    def test__make_job_id_w_suffix(self):
        with mock.patch("uuid.uuid4", side_effect=["212345"]):
            job_id = self._call_fut(None, prefix="job_id")

        self.assertEqual(job_id, "job_id212345")

    def test__make_random_job_id(self):
        with mock.patch("uuid.uuid4", side_effect=["212345"]):
            job_id = self._call_fut(None)

        self.assertEqual(job_id, "212345")

    def test__make_job_id_w_job_id_overrides_prefix(self):
        job_id = self._call_fut("job_id", prefix="unused_prefix")

        self.assertEqual(job_id, "job_id")


class TestClientUpload(object):
    # NOTE: This is a "partner" to `TestClient` meant to test some of the
    #       "load_table_from_file" portions of `Client`. It also uses
    #       `pytest`-style tests rather than `unittest`-style.
    from google.cloud.bigquery.job import SourceFormat

    TABLE_REF = DatasetReference("project_id", "test_dataset").table("test_table")

    LOCATION = "us-central"

    @staticmethod
    def _make_client(transport=None, location=None):
        from google.cloud.bigquery import _http
        from google.cloud.bigquery import client

        cl = client.Client(
            project="project_id",
            credentials=_make_credentials(),
            _http=transport,
            location=location,
        )
        cl._connection = mock.create_autospec(_http.Connection, instance=True)
        return cl

    @staticmethod
    def _make_response(status_code, content="", headers={}):
        """Make a mock HTTP response."""
        import requests

        response = requests.Response()
        response.request = requests.Request("POST", "http://example.com").prepare()
        response._content = content.encode("utf-8")
        response.headers.update(headers)
        response.status_code = status_code
        return response

    @classmethod
    def _make_do_upload_patch(cls, client, method, resource={}, side_effect=None):
        """Patches the low-level upload helpers."""
        if side_effect is None:
            side_effect = [
                cls._make_response(
                    http_client.OK,
                    json.dumps(resource),
                    {"Content-Type": "application/json"},
                )
            ]
        return mock.patch.object(client, method, side_effect=side_effect, autospec=True)

    EXPECTED_CONFIGURATION = {
        "jobReference": {"projectId": "project_id", "jobId": "job_id"},
        "configuration": {
            "load": {
                "sourceFormat": SourceFormat.CSV,
                "destinationTable": {
                    "projectId": "project_id",
                    "datasetId": "test_dataset",
                    "tableId": "test_table",
                },
            }
        },
    }

    @staticmethod
    def _make_file_obj():
        return io.BytesIO(b"hello, is it me you're looking for?")

    def _make_gzip_file_obj(self, writable):
        if writable:
            return gzip.GzipFile(mode="w", fileobj=io.BytesIO())
        else:
            return gzip.GzipFile(mode="r", fileobj=self._make_file_obj())

    @staticmethod
    def _make_config():
        from google.cloud.bigquery.job import LoadJobConfig
        from google.cloud.bigquery.job import SourceFormat

        config = LoadJobConfig()
        config.source_format = SourceFormat.CSV
        return config

    # High-level tests

    def test_load_table_from_file_resumable(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        file_obj = self._make_file_obj()

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", self.EXPECTED_CONFIGURATION
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj,
                self.TABLE_REF,
                job_id="job_id",
                job_config=self._make_config(),
            )

        do_upload.assert_called_once_with(
            file_obj, self.EXPECTED_CONFIGURATION, _DEFAULT_NUM_RETRIES
        )

    def test_load_table_from_file_w_explicit_project(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        file_obj = self._make_file_obj()

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", self.EXPECTED_CONFIGURATION
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj,
                self.TABLE_REF,
                job_id="job_id",
                project="other-project",
                location=self.LOCATION,
                job_config=self._make_config(),
            )

        expected_resource = copy.deepcopy(self.EXPECTED_CONFIGURATION)
        expected_resource["jobReference"]["location"] = self.LOCATION
        expected_resource["jobReference"]["projectId"] = "other-project"
        do_upload.assert_called_once_with(
            file_obj, expected_resource, _DEFAULT_NUM_RETRIES
        )

    def test_load_table_from_file_w_client_location(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client(location=self.LOCATION)
        file_obj = self._make_file_obj()

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", self.EXPECTED_CONFIGURATION
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj,
                # Test with string for table ID.
                "{}.{}.{}".format(
                    self.TABLE_REF.project,
                    self.TABLE_REF.dataset_id,
                    self.TABLE_REF.table_id,
                ),
                job_id="job_id",
                project="other-project",
                job_config=self._make_config(),
            )

        expected_resource = copy.deepcopy(self.EXPECTED_CONFIGURATION)
        expected_resource["jobReference"]["location"] = self.LOCATION
        expected_resource["jobReference"]["projectId"] = "other-project"
        do_upload.assert_called_once_with(
            file_obj, expected_resource, _DEFAULT_NUM_RETRIES
        )

    def test_load_table_from_file_resumable_metadata(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import WriteDisposition

        client = self._make_client()
        file_obj = self._make_file_obj()

        config = self._make_config()
        config.allow_jagged_rows = False
        config.allow_quoted_newlines = False
        config.create_disposition = CreateDisposition.CREATE_IF_NEEDED
        config.encoding = "utf8"
        config.field_delimiter = ","
        config.ignore_unknown_values = False
        config.max_bad_records = 0
        config.quote_character = '"'
        config.skip_leading_rows = 1
        config.write_disposition = WriteDisposition.WRITE_APPEND
        config.null_marker = r"\N"

        expected_config = {
            "jobReference": {"projectId": "project_id", "jobId": "job_id"},
            "configuration": {
                "load": {
                    "destinationTable": {
                        "projectId": self.TABLE_REF.project,
                        "datasetId": self.TABLE_REF.dataset_id,
                        "tableId": self.TABLE_REF.table_id,
                    },
                    "sourceFormat": config.source_format,
                    "allowJaggedRows": config.allow_jagged_rows,
                    "allowQuotedNewlines": config.allow_quoted_newlines,
                    "createDisposition": config.create_disposition,
                    "encoding": config.encoding,
                    "fieldDelimiter": config.field_delimiter,
                    "ignoreUnknownValues": config.ignore_unknown_values,
                    "maxBadRecords": config.max_bad_records,
                    "quote": config.quote_character,
                    "skipLeadingRows": str(config.skip_leading_rows),
                    "writeDisposition": config.write_disposition,
                    "nullMarker": config.null_marker,
                }
            },
        }

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", expected_config
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj, self.TABLE_REF, job_id="job_id", job_config=config
            )

        do_upload.assert_called_once_with(
            file_obj, expected_config, _DEFAULT_NUM_RETRIES
        )

    def test_load_table_from_file_multipart(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        file_obj = self._make_file_obj()
        file_obj_size = 10
        config = self._make_config()

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_multipart_upload", self.EXPECTED_CONFIGURATION
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj,
                self.TABLE_REF,
                job_id="job_id",
                job_config=config,
                size=file_obj_size,
            )

        do_upload.assert_called_once_with(
            file_obj, self.EXPECTED_CONFIGURATION, file_obj_size, _DEFAULT_NUM_RETRIES
        )

    def test_load_table_from_file_with_retries(self):
        client = self._make_client()
        file_obj = self._make_file_obj()
        num_retries = 20

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", self.EXPECTED_CONFIGURATION
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj,
                self.TABLE_REF,
                num_retries=num_retries,
                job_id="job_id",
                job_config=self._make_config(),
            )

        do_upload.assert_called_once_with(
            file_obj, self.EXPECTED_CONFIGURATION, num_retries
        )

    def test_load_table_from_file_with_rewind(self):
        client = self._make_client()
        file_obj = self._make_file_obj()
        file_obj.seek(2)

        with self._make_do_upload_patch(
            client, "_do_resumable_upload", self.EXPECTED_CONFIGURATION
        ):
            client.load_table_from_file(file_obj, self.TABLE_REF, rewind=True)

        assert file_obj.tell() == 0

    def test_load_table_from_file_with_readable_gzip(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        gzip_file = self._make_gzip_file_obj(writable=False)

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", self.EXPECTED_CONFIGURATION
        )
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                gzip_file,
                self.TABLE_REF,
                job_id="job_id",
                job_config=self._make_config(),
            )

        do_upload.assert_called_once_with(
            gzip_file, self.EXPECTED_CONFIGURATION, _DEFAULT_NUM_RETRIES
        )

    def test_load_table_from_file_with_writable_gzip(self):
        client = self._make_client()
        gzip_file = self._make_gzip_file_obj(writable=True)

        with pytest.raises(ValueError):
            client.load_table_from_file(
                gzip_file,
                self.TABLE_REF,
                job_id="job_id",
                job_config=self._make_config(),
            )

    def test_load_table_from_file_failure(self):
        from google.resumable_media import InvalidResponse
        from google.cloud import exceptions

        client = self._make_client()
        file_obj = self._make_file_obj()

        response = self._make_response(
            content="Someone is already in this spot.", status_code=http_client.CONFLICT
        )

        do_upload_patch = self._make_do_upload_patch(
            client, "_do_resumable_upload", side_effect=InvalidResponse(response)
        )

        with do_upload_patch, pytest.raises(exceptions.Conflict) as exc_info:
            client.load_table_from_file(file_obj, self.TABLE_REF, rewind=True)

        assert response.text in exc_info.value.message
        assert exc_info.value.errors == []

    def test_load_table_from_file_bad_mode(self):
        client = self._make_client()
        file_obj = mock.Mock(spec=["mode"])
        file_obj.mode = "x"

        with pytest.raises(ValueError):
            client.load_table_from_file(file_obj, self.TABLE_REF)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES
        from google.cloud.bigquery import job

        client = self._make_client()
        records = [{"name": "Monty", "age": 100}, {"name": "Python", "age": 60}]
        dataframe = pandas.DataFrame(records)

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        with load_patch as load_table_from_file:
            client.load_table_from_dataframe(dataframe, self.TABLE_REF)

        load_table_from_file.assert_called_once_with(
            client,
            mock.ANY,
            self.TABLE_REF,
            num_retries=_DEFAULT_NUM_RETRIES,
            rewind=True,
            job_id=mock.ANY,
            job_id_prefix=None,
            location=None,
            project=None,
            job_config=mock.ANY,
        )

        sent_file = load_table_from_file.mock_calls[0][1][1]
        assert sent_file.closed

        sent_config = load_table_from_file.mock_calls[0][2]["job_config"]
        assert sent_config.source_format == job.SourceFormat.PARQUET

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe_w_client_location(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES
        from google.cloud.bigquery import job

        client = self._make_client(location=self.LOCATION)
        records = [{"name": "Monty", "age": 100}, {"name": "Python", "age": 60}]
        dataframe = pandas.DataFrame(records)

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        with load_patch as load_table_from_file:
            client.load_table_from_dataframe(dataframe, self.TABLE_REF)

        load_table_from_file.assert_called_once_with(
            client,
            mock.ANY,
            self.TABLE_REF,
            num_retries=_DEFAULT_NUM_RETRIES,
            rewind=True,
            job_id=mock.ANY,
            job_id_prefix=None,
            location=self.LOCATION,
            project=None,
            job_config=mock.ANY,
        )

        sent_file = load_table_from_file.mock_calls[0][1][1]
        assert sent_file.closed

        sent_config = load_table_from_file.mock_calls[0][2]["job_config"]
        assert sent_config.source_format == job.SourceFormat.PARQUET

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe_w_custom_job_config(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES
        from google.cloud.bigquery import job

        client = self._make_client()
        records = [{"name": "Monty", "age": 100}, {"name": "Python", "age": 60}]
        dataframe = pandas.DataFrame(records)
        job_config = job.LoadJobConfig()

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        with load_patch as load_table_from_file:
            client.load_table_from_dataframe(
                dataframe, self.TABLE_REF, job_config=job_config, location=self.LOCATION
            )

        load_table_from_file.assert_called_once_with(
            client,
            mock.ANY,
            self.TABLE_REF,
            num_retries=_DEFAULT_NUM_RETRIES,
            rewind=True,
            job_id=mock.ANY,
            job_id_prefix=None,
            location=self.LOCATION,
            project=None,
            job_config=mock.ANY,
        )

        sent_config = load_table_from_file.mock_calls[0][2]["job_config"]
        assert sent_config is job_config
        assert sent_config.source_format == job.SourceFormat.PARQUET

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe_w_schema_wo_pyarrow(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES
        from google.cloud.bigquery import job
        from google.cloud.bigquery.schema import SchemaField

        client = self._make_client()
        records = [{"name": "Monty", "age": 100}, {"name": "Python", "age": 60}]
        dataframe = pandas.DataFrame(records)
        schema = (SchemaField("name", "STRING"), SchemaField("age", "INTEGER"))
        job_config = job.LoadJobConfig(schema=schema)

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        pyarrow_patch = mock.patch("google.cloud.bigquery.client.pyarrow", None)

        with load_patch as load_table_from_file, pyarrow_patch, warnings.catch_warnings(
            record=True
        ) as warned:
            client.load_table_from_dataframe(
                dataframe, self.TABLE_REF, job_config=job_config, location=self.LOCATION
            )

        assert warned  # there should be at least one warning
        for warning in warned:
            assert "pyarrow" in str(warning)
            assert warning.category in (DeprecationWarning, PendingDeprecationWarning)

        load_table_from_file.assert_called_once_with(
            client,
            mock.ANY,
            self.TABLE_REF,
            num_retries=_DEFAULT_NUM_RETRIES,
            rewind=True,
            job_id=mock.ANY,
            job_id_prefix=None,
            location=self.LOCATION,
            project=None,
            job_config=mock.ANY,
        )

        sent_config = load_table_from_file.mock_calls[0][2]["job_config"]
        assert sent_config.source_format == job.SourceFormat.PARQUET
        assert tuple(sent_config.schema) == schema

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe_w_schema_arrow_custom_compression(self):
        from google.cloud.bigquery import job
        from google.cloud.bigquery.schema import SchemaField

        client = self._make_client()
        records = [{"name": "Monty", "age": 100}, {"name": "Python", "age": 60}]
        dataframe = pandas.DataFrame(records)
        schema = (SchemaField("name", "STRING"), SchemaField("age", "INTEGER"))
        job_config = job.LoadJobConfig(schema=schema)

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        to_parquet_patch = mock.patch(
            "google.cloud.bigquery.client._pandas_helpers.dataframe_to_parquet",
            autospec=True,
        )

        with load_patch, to_parquet_patch as fake_to_parquet:
            client.load_table_from_dataframe(
                dataframe,
                self.TABLE_REF,
                job_config=job_config,
                location=self.LOCATION,
                parquet_compression="LZ4",
            )

        call_args = fake_to_parquet.call_args
        assert call_args is not None
        assert call_args.kwargs.get("parquet_compression") == "LZ4"

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe_wo_pyarrow_custom_compression(self):
        client = self._make_client()
        records = [{"name": "Monty", "age": 100}, {"name": "Python", "age": 60}]
        dataframe = pandas.DataFrame(records)

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        pyarrow_patch = mock.patch("google.cloud.bigquery.client.pyarrow", None)
        to_parquet_patch = mock.patch.object(
            dataframe, "to_parquet", wraps=dataframe.to_parquet
        )

        with load_patch, pyarrow_patch, to_parquet_patch as to_parquet_spy:
            client.load_table_from_dataframe(
                dataframe,
                self.TABLE_REF,
                location=self.LOCATION,
                parquet_compression="gzip",
            )

        call_args = to_parquet_spy.call_args
        assert call_args is not None
        assert call_args.kwargs.get("compression") == "gzip"

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_load_table_from_dataframe_w_nulls(self):
        """Test that a DataFrame with null columns can be uploaded if a
        BigQuery schema is specified.

        See: https://github.com/googleapis/google-cloud-python/issues/7370
        """
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES
        from google.cloud.bigquery import job

        client = self._make_client()
        records = [{"name": None, "age": None}, {"name": None, "age": None}]
        dataframe = pandas.DataFrame(records)
        schema = [SchemaField("name", "STRING"), SchemaField("age", "INTEGER")]
        job_config = job.LoadJobConfig(schema=schema)

        load_patch = mock.patch(
            "google.cloud.bigquery.client.Client.load_table_from_file", autospec=True
        )
        with load_patch as load_table_from_file:
            client.load_table_from_dataframe(
                dataframe, self.TABLE_REF, job_config=job_config, location=self.LOCATION
            )

        load_table_from_file.assert_called_once_with(
            client,
            mock.ANY,
            self.TABLE_REF,
            num_retries=_DEFAULT_NUM_RETRIES,
            rewind=True,
            job_id=mock.ANY,
            job_id_prefix=None,
            location=self.LOCATION,
            project=None,
            job_config=mock.ANY,
        )

        sent_config = load_table_from_file.mock_calls[0][2]["job_config"]
        assert sent_config is job_config
        assert sent_config.source_format == job.SourceFormat.PARQUET

    # Low-level tests

    @classmethod
    def _make_resumable_upload_responses(cls, size):
        """Make a series of responses for a successful resumable upload."""
        from google import resumable_media

        resumable_url = "http://test.invalid?upload_id=and-then-there-was-1"
        initial_response = cls._make_response(
            http_client.OK, "", {"location": resumable_url}
        )
        data_response = cls._make_response(
            resumable_media.PERMANENT_REDIRECT,
            "",
            {"range": "bytes=0-{:d}".format(size - 1)},
        )
        final_response = cls._make_response(
            http_client.OK,
            json.dumps({"size": size}),
            {"Content-Type": "application/json"},
        )
        return [initial_response, data_response, final_response]

    @staticmethod
    def _make_transport(responses=None):
        import google.auth.transport.requests

        transport = mock.create_autospec(
            google.auth.transport.requests.AuthorizedSession, instance=True
        )
        transport.request.side_effect = responses
        return transport

    def test__do_resumable_upload(self):
        file_obj = self._make_file_obj()
        file_obj_len = len(file_obj.getvalue())
        transport = self._make_transport(
            self._make_resumable_upload_responses(file_obj_len)
        )
        client = self._make_client(transport)

        result = client._do_resumable_upload(
            file_obj, self.EXPECTED_CONFIGURATION, None
        )

        content = result.content.decode("utf-8")
        assert json.loads(content) == {"size": file_obj_len}

        # Verify that configuration data was passed in with the initial
        # request.
        transport.request.assert_any_call(
            "POST",
            mock.ANY,
            data=json.dumps(self.EXPECTED_CONFIGURATION).encode("utf-8"),
            headers=mock.ANY,
        )

    def test__do_multipart_upload(self):
        transport = self._make_transport([self._make_response(http_client.OK)])
        client = self._make_client(transport)
        file_obj = self._make_file_obj()
        file_obj_len = len(file_obj.getvalue())

        client._do_multipart_upload(
            file_obj, self.EXPECTED_CONFIGURATION, file_obj_len, None
        )

        # Verify that configuration data was passed in with the initial
        # request.
        request_args = transport.request.mock_calls[0][2]
        request_data = request_args["data"].decode("utf-8")
        request_headers = request_args["headers"]

        request_content = email.message_from_string(
            "Content-Type: {}\r\n{}".format(
                request_headers["content-type"].decode("utf-8"), request_data
            )
        )

        # There should be two payloads: the configuration and the binary daya.
        configuration_data = request_content.get_payload(0).get_payload()
        binary_data = request_content.get_payload(1).get_payload()

        assert json.loads(configuration_data) == self.EXPECTED_CONFIGURATION
        assert binary_data.encode("utf-8") == file_obj.getvalue()

    def test__do_multipart_upload_wrong_size(self):
        client = self._make_client()
        file_obj = self._make_file_obj()
        file_obj_len = len(file_obj.getvalue())

        with pytest.raises(ValueError):
            client._do_multipart_upload(file_obj, {}, file_obj_len + 1, None)

    def test_schema_from_json_with_file_path(self):
        from google.cloud.bigquery.schema import SchemaField

        file_content = """[
          {
            "description": "quarter",
            "mode": "REQUIRED",
            "name": "qtr",
            "type": "STRING"
          },
          {
            "description": "sales representative",
            "mode": "NULLABLE",
            "name": "rep",
            "type": "STRING"
          },
          {
            "description": "total sales",
            "mode": "NULLABLE",
            "name": "sales",
            "type": "FLOAT"
          }
        ]"""

        expected = [
            SchemaField("qtr", "STRING", "REQUIRED", "quarter"),
            SchemaField("rep", "STRING", "NULLABLE", "sales representative"),
            SchemaField("sales", "FLOAT", "NULLABLE", "total sales"),
        ]

        client = self._make_client()
        mock_file_path = "/mocked/file.json"

        if six.PY2:
            open_patch = mock.patch(
                "__builtin__.open", mock.mock_open(read_data=file_content)
            )
        else:
            open_patch = mock.patch(
                "builtins.open", new=mock.mock_open(read_data=file_content)
            )

        with open_patch as _mock_file:
            actual = client.schema_from_json(mock_file_path)
            _mock_file.assert_called_once_with(mock_file_path)
            # This assert is to make sure __exit__ is called in the context
            # manager that opens the file in the function
            _mock_file().__exit__.assert_called_once()

        assert expected == actual

    def test_schema_from_json_with_file_object(self):
        from google.cloud.bigquery.schema import SchemaField

        file_content = """[
          {
            "description": "quarter",
            "mode": "REQUIRED",
            "name": "qtr",
            "type": "STRING"
          },
          {
            "description": "sales representative",
            "mode": "NULLABLE",
            "name": "rep",
            "type": "STRING"
          },
          {
            "description": "total sales",
            "mode": "NULLABLE",
            "name": "sales",
            "type": "FLOAT"
          }
        ]"""

        expected = [
            SchemaField("qtr", "STRING", "REQUIRED", "quarter"),
            SchemaField("rep", "STRING", "NULLABLE", "sales representative"),
            SchemaField("sales", "FLOAT", "NULLABLE", "total sales"),
        ]

        client = self._make_client()

        if six.PY2:
            fake_file = io.BytesIO(file_content)
        else:
            fake_file = io.StringIO(file_content)

        actual = client.schema_from_json(fake_file)

        assert expected == actual

    def test_schema_to_json_with_file_path(self):
        from google.cloud.bigquery.schema import SchemaField

        file_content = [
            {
                "description": "quarter",
                "mode": "REQUIRED",
                "name": "qtr",
                "type": "STRING",
            },
            {
                "description": "sales representative",
                "mode": "NULLABLE",
                "name": "rep",
                "type": "STRING",
            },
            {
                "description": "total sales",
                "mode": "NULLABLE",
                "name": "sales",
                "type": "FLOAT",
            },
        ]

        schema_list = [
            SchemaField("qtr", "STRING", "REQUIRED", "quarter"),
            SchemaField("rep", "STRING", "NULLABLE", "sales representative"),
            SchemaField("sales", "FLOAT", "NULLABLE", "total sales"),
        ]

        client = self._make_client()
        mock_file_path = "/mocked/file.json"

        if six.PY2:
            open_patch = mock.patch("__builtin__.open", mock.mock_open())
        else:
            open_patch = mock.patch("builtins.open", mock.mock_open())

        with open_patch as mock_file, mock.patch("json.dump") as mock_dump:
            client.schema_to_json(schema_list, mock_file_path)
            mock_file.assert_called_once_with(mock_file_path, mode="w")
            # This assert is to make sure __exit__ is called in the context
            # manager that opens the file in the function
            mock_file().__exit__.assert_called_once()
            mock_dump.assert_called_with(
                file_content, mock_file.return_value, indent=2, sort_keys=True
            )

    def test_schema_to_json_with_file_object(self):
        from google.cloud.bigquery.schema import SchemaField

        file_content = [
            {
                "description": "quarter",
                "mode": "REQUIRED",
                "name": "qtr",
                "type": "STRING",
            },
            {
                "description": "sales representative",
                "mode": "NULLABLE",
                "name": "rep",
                "type": "STRING",
            },
            {
                "description": "total sales",
                "mode": "NULLABLE",
                "name": "sales",
                "type": "FLOAT",
            },
        ]

        schema_list = [
            SchemaField("qtr", "STRING", "REQUIRED", "quarter"),
            SchemaField("rep", "STRING", "NULLABLE", "sales representative"),
            SchemaField("sales", "FLOAT", "NULLABLE", "total sales"),
        ]

        if six.PY2:
            fake_file = io.BytesIO()
        else:
            fake_file = io.StringIO()

        client = self._make_client()

        client.schema_to_json(schema_list, fake_file)
        assert file_content == json.loads(fake_file.getvalue())
