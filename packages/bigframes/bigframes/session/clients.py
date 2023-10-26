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

"""Clients manages the connection to Google APIs."""

import os
import typing
from typing import Optional

import google.api_core.client_info
import google.api_core.client_options
import google.api_core.exceptions
import google.api_core.gapic_v1.client_info
import google.auth.credentials
import google.cloud.bigquery as bigquery
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3
import ibis
import pydata_google_auth

import bigframes.version

_ENV_DEFAULT_PROJECT = "GOOGLE_CLOUD_PROJECT"
_APPLICATION_NAME = f"bigframes/{bigframes.version.__version__} ibis/{ibis.__version__}"
_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# BigQuery is a REST API, which requires the protocol as part of the URL.
_BIGQUERY_REGIONAL_ENDPOINT = "https://{location}-bigquery.googleapis.com"

# BigQuery Connection and Storage are gRPC APIs, which don't support the
# https:// protocol in the API endpoint URL.
_BIGQUERYCONNECTION_REGIONAL_ENDPOINT = "{location}-bigqueryconnection.googleapis.com"
_BIGQUERYSTORAGE_REGIONAL_ENDPOINT = "{location}-bigquerystorage.googleapis.com"


def _get_default_credentials_with_project():
    return pydata_google_auth.default(scopes=_SCOPES, use_local_webserver=False)


class ClientsProvider:
    """Provides client instances necessary to perform cloud operations."""

    def __init__(
        self,
        project: Optional[str],
        location: Optional[str],
        use_regional_endpoints: Optional[bool],
        credentials: Optional[google.auth.credentials.Credentials],
        application_name: Optional[str],
    ):
        credentials_project = None
        if credentials is None:
            credentials, credentials_project = _get_default_credentials_with_project()

        # Prefer the project in this order:
        # 1. Project explicitly specified by the user
        # 2. Project set in the environment
        # 3. Project associated with the default credentials
        project = (
            project
            or os.getenv(_ENV_DEFAULT_PROJECT)
            or typing.cast(Optional[str], credentials_project)
        )

        if not project:
            raise ValueError(
                "Project must be set to initialize BigQuery client. "
                "Try setting `bigframes.options.bigquery.project` first."
            )

        self._application_name = (
            f"{_APPLICATION_NAME} {application_name}"
            if application_name
            else _APPLICATION_NAME
        )
        self._project = project
        self._location = location
        self._use_regional_endpoints = use_regional_endpoints
        self._credentials = credentials

        # cloud clients initialized for lazy load
        self._bqclient = None
        self._bqconnectionclient = None
        self._bqstoragereadclient = None
        self._cloudfunctionsclient = None
        self._resourcemanagerclient = None

    @property
    def bqclient(self):
        if not self._bqclient:
            bq_options = None
            if self._use_regional_endpoints:
                bq_options = google.api_core.client_options.ClientOptions(
                    api_endpoint=_BIGQUERY_REGIONAL_ENDPOINT.format(
                        location=self._location
                    ),
                )
            bq_info = google.api_core.client_info.ClientInfo(
                user_agent=self._application_name
            )
            self._bqclient = bigquery.Client(
                client_info=bq_info,
                client_options=bq_options,
                credentials=self._credentials,
                project=self._project,
                location=self._location,
            )

        return self._bqclient

    @property
    def bqconnectionclient(self):
        if not self._bqconnectionclient:
            bqconnection_options = None
            if self._use_regional_endpoints:
                bqconnection_options = google.api_core.client_options.ClientOptions(
                    api_endpoint=_BIGQUERYCONNECTION_REGIONAL_ENDPOINT.format(
                        location=self._location
                    )
                )
            bqconnection_info = google.api_core.gapic_v1.client_info.ClientInfo(
                user_agent=self._application_name
            )
            self._bqconnectionclient = (
                google.cloud.bigquery_connection_v1.ConnectionServiceClient(
                    client_info=bqconnection_info,
                    client_options=bqconnection_options,
                    credentials=self._credentials,
                )
            )

        return self._bqconnectionclient

    @property
    def bqstoragereadclient(self):
        if not self._bqstoragereadclient:
            bqstorage_options = None
            if self._use_regional_endpoints:
                bqstorage_options = google.api_core.client_options.ClientOptions(
                    api_endpoint=_BIGQUERYSTORAGE_REGIONAL_ENDPOINT.format(
                        location=self._location
                    )
                )
            bqstorage_info = google.api_core.gapic_v1.client_info.ClientInfo(
                user_agent=self._application_name
            )
            self._bqstoragereadclient = (
                google.cloud.bigquery_storage_v1.BigQueryReadClient(
                    client_info=bqstorage_info,
                    client_options=bqstorage_options,
                    credentials=self._credentials,
                )
            )

        return self._bqstoragereadclient

    @property
    def cloudfunctionsclient(self):
        if not self._cloudfunctionsclient:
            functions_info = google.api_core.gapic_v1.client_info.ClientInfo(
                user_agent=self._application_name
            )
            self._cloudfunctionsclient = (
                google.cloud.functions_v2.FunctionServiceClient(
                    client_info=functions_info,
                    credentials=self._credentials,
                )
            )

        return self._cloudfunctionsclient

    @property
    def resourcemanagerclient(self):
        if not self._resourcemanagerclient:
            resourcemanager_info = google.api_core.gapic_v1.client_info.ClientInfo(
                user_agent=self._application_name
            )
            self._resourcemanagerclient = (
                google.cloud.resourcemanager_v3.ProjectsClient(
                    credentials=self._credentials, client_info=resourcemanager_info
                )
            )

        return self._resourcemanagerclient
