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

"""Options for BigQuery DataFrames."""

from __future__ import annotations

from typing import Optional

import google.api_core.exceptions
import google.auth.credentials

SESSION_STARTED_MESSAGE = (
    "Cannot change '{attribute}' once a session has started. "
    "Call bigframes.pandas.close_session() first, if you are using the bigframes.pandas API."
)


class BigQueryOptions:
    """Encapsulates configuration for working with a session."""

    def __init__(
        self,
        credentials: Optional[google.auth.credentials.Credentials] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        bq_connection: Optional[str] = None,
        use_regional_endpoints: bool = False,
        application_name: Optional[str] = None,
    ):
        self._credentials = credentials
        self._project = project
        self._location = location
        self._bq_connection = bq_connection
        self._use_regional_endpoints = use_regional_endpoints
        self._application_name = application_name
        self._session_started = False

    @property
    def application_name(self) -> Optional[str]:
        """The application name to amend to the user-agent sent to Google APIs.

        Recommended format is ``"appplication-name/major.minor.patch_version"``
        or ``"(gpn:PartnerName;)"`` for official Google partners.
        """
        return self._application_name

    @application_name.setter
    def application_name(self, value: Optional[str]):
        if self._session_started and self._application_name != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="application_name")
            )
        self._application_name = value

    @property
    def credentials(self) -> Optional[google.auth.credentials.Credentials]:
        """The OAuth2 Credentials to use for this client."""
        return self._credentials

    @credentials.setter
    def credentials(self, value: Optional[google.auth.credentials.Credentials]):
        if self._session_started and self._credentials is not value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="credentials"))
        self._credentials = value

    @property
    def location(self) -> Optional[str]:
        """Default location for job, datasets, and tables.

        See: https://cloud.google.com/bigquery/docs/locations
        """
        return self._location

    @location.setter
    def location(self, value: Optional[str]):
        if self._session_started and self._location != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="location"))
        self._location = value

    @property
    def project(self) -> Optional[str]:
        """Google Cloud project ID to use for billing and as the default project."""
        return self._project

    @project.setter
    def project(self, value: Optional[str]):
        if self._session_started and self._project != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="project"))
        self._project = value

    @property
    def bq_connection(self) -> Optional[str]:
        """Name of the BigQuery connection to use. Should be of the form <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.

        You should either have the connection already created in the
        <code>location</code> you have chosen, or you should have the Project IAM
        Admin role to enable the service to create the connection for you if you
        need it.

        If this option isn't provided, or project or location aren't provided, session will use its default project/location/connection_id as default connection.
        """
        return self._bq_connection

    @bq_connection.setter
    def bq_connection(self, value: Optional[str]):
        if self._session_started and self._bq_connection != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="bq_connection"))
        self._bq_connection = value

    @property
    def use_regional_endpoints(self) -> bool:
        """Flag to connect to regional API endpoints.

        Requires ``location`` to also be set. For example, set
        ``location='asia-northeast1'`` and ``use_regional_endpoints=True`` to
        connect to asia-northeast1-bigquery.googleapis.com.
        """
        return self._use_regional_endpoints

    @use_regional_endpoints.setter
    def use_regional_endpoints(self, value: bool):
        if self._session_started and self._use_regional_endpoints != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="use_regional_endpoints")
            )
        self._use_regional_endpoints = value
