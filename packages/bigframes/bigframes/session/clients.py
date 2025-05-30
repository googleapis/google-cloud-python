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
import threading
import typing
from typing import Optional, Sequence, Tuple

import google.api_core.client_info
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.auth.credentials
import google.auth.transport.requests
import google.cloud.bigquery as bigquery
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3
import pydata_google_auth
import requests

import bigframes.constants
import bigframes.version

from . import environment

_ENV_DEFAULT_PROJECT = "GOOGLE_CLOUD_PROJECT"
_APPLICATION_NAME = f"bigframes/{bigframes.version.__version__} ibis/9.2.0"
_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


# BigQuery is a REST API, which requires the protocol as part of the URL.
_BIGQUERY_REGIONAL_ENDPOINT = "https://bigquery.{location}.rep.googleapis.com"

# BigQuery Connection and Storage are gRPC APIs, which don't support the
# https:// protocol in the API endpoint URL.
_BIGQUERYSTORAGE_REGIONAL_ENDPOINT = "bigquerystorage.{location}.rep.googleapis.com"


def _get_default_credentials_with_project():
    return pydata_google_auth.default(scopes=_SCOPES, use_local_webserver=False)


def _get_application_names():
    apps = [_APPLICATION_NAME]

    if environment.is_vscode():
        apps.append("vscode")
        if environment.is_vscode_google_cloud_code_extension_installed():
            apps.append(environment.GOOGLE_CLOUD_CODE_EXTENSION_NAME)
    elif environment.is_jupyter():
        apps.append("jupyter")
        if environment.is_jupyter_bigquery_plugin_installed():
            apps.append(environment.BIGQUERY_JUPYTER_PLUGIN_NAME)

    return " ".join(apps)


class ClientsProvider:
    """Provides client instances necessary to perform cloud operations."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
        use_regional_endpoints: Optional[bool] = None,
        credentials: Optional[google.auth.credentials.Credentials] = None,
        application_name: Optional[str] = None,
        bq_kms_key_name: Optional[str] = None,
        client_endpoints_override: dict = {},
        *,
        requests_transport_adapters: Sequence[
            Tuple[str, requests.adapters.BaseAdapter]
        ] = (),
    ):
        credentials_project = None
        if credentials is None:
            credentials, credentials_project = _get_default_credentials_with_project()

            # Ensure an access token is available.
            credentials.refresh(google.auth.transport.requests.Request())

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
            f"{_get_application_names()} {application_name}"
            if application_name
            else _get_application_names()
        )
        self._project = project

        if use_regional_endpoints:
            if location is None:
                raise ValueError(bigframes.constants.LOCATION_NEEDED_FOR_REP_MESSAGE)
            elif (
                location.lower()
                not in bigframes.constants.REP_ENABLED_BIGQUERY_LOCATIONS
            ):
                raise ValueError(
                    bigframes.constants.REP_NOT_SUPPORTED_MESSAGE.format(
                        location=location
                    )
                )
        self._location = location
        self._use_regional_endpoints = use_regional_endpoints
        self._requests_transport_adapters = requests_transport_adapters

        self._credentials = credentials
        self._bq_kms_key_name = bq_kms_key_name
        self._client_endpoints_override = client_endpoints_override

        # cloud clients initialized for lazy load
        self._bqclient_lock = threading.Lock()
        self._bqclient = None

        self._bqconnectionclient_lock = threading.Lock()
        self._bqconnectionclient: Optional[
            google.cloud.bigquery_connection_v1.ConnectionServiceClient
        ] = None

        self._bqstoragereadclient_lock = threading.Lock()
        self._bqstoragereadclient: Optional[
            google.cloud.bigquery_storage_v1.BigQueryReadClient
        ] = None

        self._bqstoragewriteclient_lock = threading.Lock()
        self._bqstoragewriteclient: Optional[
            google.cloud.bigquery_storage_v1.BigQueryWriteClient
        ] = None

        self._cloudfunctionsclient_lock = threading.Lock()
        self._cloudfunctionsclient: Optional[
            google.cloud.functions_v2.FunctionServiceClient
        ] = None

        self._resourcemanagerclient_lock = threading.Lock()
        self._resourcemanagerclient: Optional[
            google.cloud.resourcemanager_v3.ProjectsClient
        ] = None

    def _create_bigquery_client(self):
        bq_options = None
        if "bqclient" in self._client_endpoints_override:
            bq_options = google.api_core.client_options.ClientOptions(
                api_endpoint=self._client_endpoints_override["bqclient"]
            )
        elif self._use_regional_endpoints:
            bq_options = google.api_core.client_options.ClientOptions(
                api_endpoint=_BIGQUERY_REGIONAL_ENDPOINT.format(location=self._location)
            )

        bq_info = google.api_core.client_info.ClientInfo(
            user_agent=self._application_name
        )

        requests_session = google.auth.transport.requests.AuthorizedSession(
            self._credentials
        )
        for prefix, adapter in self._requests_transport_adapters:
            requests_session.mount(prefix, adapter)

        bq_client = bigquery.Client(
            client_info=bq_info,
            client_options=bq_options,
            project=self._project,
            location=self._location,
            # Instead of credentials, use _http so that users can override
            # requests options with transport adapters. See internal issue
            # b/419106112.
            _http=requests_session,
        )

        # If a new enough client library is available, we opt-in to the faster
        # backend behavior. This only affects code paths where query_and_wait is
        # used, which doesn't expose a query job directly. See internal issue
        # b/417985981.
        if hasattr(bq_client, "default_job_creation_mode"):
            bq_client.default_job_creation_mode = "JOB_CREATION_OPTIONAL"

        if self._bq_kms_key_name:
            # Note: Key configuration only applies automatically to load and query jobs, not copy jobs.
            encryption_config = bigquery.EncryptionConfiguration(
                kms_key_name=self._bq_kms_key_name
            )
            default_load_job_config = bigquery.LoadJobConfig()
            default_query_job_config = bigquery.QueryJobConfig()
            default_load_job_config.destination_encryption_configuration = (
                encryption_config
            )
            default_query_job_config.destination_encryption_configuration = (
                encryption_config
            )
            bq_client.default_load_job_config = default_load_job_config
            bq_client.default_query_job_config = default_query_job_config

        return bq_client

    @property
    def bqclient(self):
        with self._bqclient_lock:
            if not self._bqclient:
                self._bqclient = self._create_bigquery_client()

        return self._bqclient

    @property
    def bqconnectionclient(self):
        with self._bqconnectionclient_lock:
            if not self._bqconnectionclient:
                bqconnection_options = None
                if "bqconnectionclient" in self._client_endpoints_override:
                    bqconnection_options = google.api_core.client_options.ClientOptions(
                        api_endpoint=self._client_endpoints_override[
                            "bqconnectionclient"
                        ]
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
        with self._bqstoragereadclient_lock:
            if not self._bqstoragereadclient:
                bqstorage_options = None
                if "bqstoragereadclient" in self._client_endpoints_override:
                    bqstorage_options = google.api_core.client_options.ClientOptions(
                        api_endpoint=self._client_endpoints_override[
                            "bqstoragereadclient"
                        ]
                    )
                elif self._use_regional_endpoints:
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
    def bqstoragewriteclient(self):
        with self._bqstoragewriteclient_lock:
            if not self._bqstoragewriteclient:
                bqstorage_options = None
                if "bqstoragewriteclient" in self._client_endpoints_override:
                    bqstorage_options = google.api_core.client_options.ClientOptions(
                        api_endpoint=self._client_endpoints_override[
                            "bqstoragewriteclient"
                        ]
                    )
                elif self._use_regional_endpoints:
                    bqstorage_options = google.api_core.client_options.ClientOptions(
                        api_endpoint=_BIGQUERYSTORAGE_REGIONAL_ENDPOINT.format(
                            location=self._location
                        )
                    )

                bqstorage_info = google.api_core.gapic_v1.client_info.ClientInfo(
                    user_agent=self._application_name
                )
                self._bqstoragewriteclient = (
                    google.cloud.bigquery_storage_v1.BigQueryWriteClient(
                        client_info=bqstorage_info,
                        client_options=bqstorage_options,
                        credentials=self._credentials,
                    )
                )

        return self._bqstoragewriteclient

    @property
    def cloudfunctionsclient(self):
        with self._cloudfunctionsclient_lock:
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
        with self._resourcemanagerclient_lock:
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
