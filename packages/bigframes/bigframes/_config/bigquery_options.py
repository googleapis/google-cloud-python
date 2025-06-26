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

from typing import Literal, Optional, Sequence, Tuple
import warnings

import google.auth.credentials
import requests.adapters

import bigframes._importing
import bigframes.enums
import bigframes.exceptions as bfe

SESSION_STARTED_MESSAGE = (
    "Cannot change '{attribute}' once a session has started. "
    "Call bigframes.pandas.close_session() first, if you are using the bigframes.pandas API."
)


UNKNOWN_LOCATION_MESSAGE = "The location '{location}' is set to an unknown value. Did you mean '{possibility}'?"


def _get_validated_location(value: Optional[str]) -> Optional[str]:
    import bigframes._tools.strings

    if value is None or value in bigframes.constants.ALL_BIGQUERY_LOCATIONS:
        return value

    location = str(value)

    location_lowercase = location.lower()
    if location_lowercase in bigframes.constants.BIGQUERY_REGIONS:
        return location_lowercase

    location_uppercase = location.upper()
    if location_uppercase in bigframes.constants.BIGQUERY_MULTIREGIONS:
        return location_uppercase

    possibility = min(
        bigframes.constants.ALL_BIGQUERY_LOCATIONS,
        key=lambda item: bigframes._tools.strings.levenshtein_distance(location, item),
    )
    # There are many layers before we get to (possibly) the user's code:
    # -> bpd.options.bigquery.location = "us-central-1"
    # -> location.setter
    # -> _get_validated_location
    msg = bfe.format_message(
        UNKNOWN_LOCATION_MESSAGE.format(location=location, possibility=possibility)
    )
    warnings.warn(msg, stacklevel=3, category=bfe.UnknownLocationWarning)

    return value


def _validate_ordering_mode(value: str) -> bigframes.enums.OrderingMode:
    if value.casefold() == bigframes.enums.OrderingMode.STRICT.value.casefold():
        return bigframes.enums.OrderingMode.STRICT
    if value.casefold() == bigframes.enums.OrderingMode.PARTIAL.value.casefold():
        return bigframes.enums.OrderingMode.PARTIAL
    raise ValueError("Ordering mode must be one of 'strict' or 'partial'.")


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
        kms_key_name: Optional[str] = None,
        skip_bq_connection_check: bool = False,
        *,
        allow_large_results: bool = False,
        ordering_mode: Literal["strict", "partial"] = "strict",
        client_endpoints_override: Optional[dict] = None,
        requests_transport_adapters: Sequence[
            Tuple[str, requests.adapters.BaseAdapter]
        ] = (),
        enable_polars_execution: bool = False,
    ):
        self._credentials = credentials
        self._project = project
        self._location = _get_validated_location(location)
        self._bq_connection = bq_connection
        self._use_regional_endpoints = use_regional_endpoints
        self._application_name = application_name
        self._kms_key_name = kms_key_name
        self._skip_bq_connection_check = skip_bq_connection_check
        self._allow_large_results = allow_large_results
        self._requests_transport_adapters = requests_transport_adapters
        self._session_started = False
        # Determines the ordering strictness for the session.
        self._ordering_mode = _validate_ordering_mode(ordering_mode)

        if client_endpoints_override is None:
            client_endpoints_override = {}

        self._client_endpoints_override = client_endpoints_override
        if enable_polars_execution:
            bigframes._importing.import_polars()
        self._enable_polars_execution = enable_polars_execution

    @property
    def application_name(self) -> Optional[str]:
        """The application name to amend to the user-agent sent to Google APIs.

        The application name to amend to the user agent sent to Google APIs.
        The recommended format is  ``"application-name/major.minor.patch_version"``
        or ``"(gpn:PartnerName;)"`` for official Google partners.

        Returns:
            None or str:
                Application name as a string if exists; otherwise None.
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
        """The OAuth2 credentials to use for this client.

        Returns:
            None or google.auth.credentials.Credentials:
                google.auth.credentials.Credentials if exists; otherwise None.
        """
        return self._credentials

    @credentials.setter
    def credentials(self, value: Optional[google.auth.credentials.Credentials]):
        if self._session_started and self._credentials is not value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="credentials"))
        self._credentials = value

    @property
    def location(self) -> Optional[str]:
        """Default location for job, datasets, and tables.

        For more information, see https://cloud.google.com/bigquery/docs/locations BigQuery locations.

        Returns:
            None or str:
                Default location as a string; otherwise None.
        """
        return self._location

    @location.setter
    def location(self, value: Optional[str]):
        if self._session_started and self._location != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="location"))
        self._location = _get_validated_location(value)

    @property
    def project(self) -> Optional[str]:
        """Google Cloud project ID to use for billing and as the default project.

        Returns:
            None or str:
                Google Cloud project ID as a string; otherwise None.
        """
        return self._project

    @project.setter
    def project(self, value: Optional[str]):
        if self._session_started and self._project != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="project"))
        self._project = value

    @property
    def bq_connection(self) -> Optional[str]:
        """Name of the BigQuery connection to use in the form
        <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.

        You either need to create the connection in a location of your choice, or
        you need the Project Admin IAM role to enable the service to create the
        connection for you.

        If this option isn't available, or the project or location isn't provided,
        then the default connection project/location/connection_id is used in the session.

        If this option isn't provided, or project or location aren't provided,
        session will use its default project/location/connection_id as default connection.

        Returns:
            None or str:
                Name of the BigQuery connection as a string; otherwise None.
        """
        return self._bq_connection

    @bq_connection.setter
    def bq_connection(self, value: Optional[str]):
        if self._session_started and self._bq_connection != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="bq_connection"))
        self._bq_connection = value

    @property
    def skip_bq_connection_check(self) -> bool:
        """Forcibly use the BigQuery connection.

        Setting this flag to True would avoid creating the BigQuery connection
        and checking or setting IAM permissions on it. So if the BigQuery
        connection (default or user-provided) does not exist, or it does not have
        necessary permissions set up to support BigQuery DataFrames operations,
        then a runtime error will be reported.

        Returns:
            bool:
                A boolean value, where True indicates a BigQuery connection is
                not created or the connection does not have necessary
                permissions set up; otherwise False.
        """
        return self._skip_bq_connection_check

    @skip_bq_connection_check.setter
    def skip_bq_connection_check(self, value: bool):
        if self._session_started and self._skip_bq_connection_check != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="skip_bq_connection_check")
            )
        self._skip_bq_connection_check = value

    @property
    def allow_large_results(self) -> bool:
        """
        DEPRECATED: Checks the legacy global setting for allowing large results.
        Use ``bpd.options.compute.allow_large_results`` instead.

        Warning: Accessing ``bpd.options.bigquery.allow_large_results`` is deprecated
        and this property will be removed in a future version. The configuration for
        handling large results has moved.

        Returns:
            bool: The value of the deprecated setting.
        """
        return self._allow_large_results

    @allow_large_results.setter
    def allow_large_results(self, value: bool):
        warnings.warn(
            "Setting `bpd.options.bigquery.allow_large_results` is deprecated, "
            "and will be removed in the future. "
            "Please use `bpd.options.compute.allow_large_results = <value>` instead. "
            "The `bpd.options.bigquery.allow_large_results` option is ignored if "
            "`bpd.options.compute.allow_large_results` is set.",
            FutureWarning,
            stacklevel=2,
        )
        if self._session_started and self._allow_large_results != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="allow_large_results")
            )

        self._allow_large_results = value

    @property
    def use_regional_endpoints(self) -> bool:
        """Flag to connect to regional API endpoints for BigQuery API and
        BigQuery Storage API.

        .. note::
            Use of regional endpoints is a feature in Preview and available only
            in regions "europe-west3", "europe-west8", "europe-west9",
            "me-central2", "us-central1", "us-central2", "us-east1", "us-east4",
            "us-east5", "us-east7", "us-south1", "us-west1", "us-west2", "us-west3"
            and "us-west4".

        Requires that ``location`` is set. For [supported regions](https://cloud.google.com/bigquery/docs/regional-endpoints),
        for example ``europe-west3``, you need to specify
        ``location='europe-west3'`` and ``use_regional_endpoints=True``, and
        then BigQuery DataFrames would connect to the BigQuery endpoint
        ``bigquery.europe-west3.rep.googleapis.com``. For not supported regions,
        for example ``asia-northeast1``, when you specify
        ``location='asia-northeast1'`` and ``use_regional_endpoints=True``,
        the global endpoint ``bigquery.googleapis.com`` would be used, which
        does not promise any guarantee on the request remaining within the
        location during transit.

        Returns:
            bool:
              A boolean value, where True indicates that regional endpoints
              would be used for BigQuery and BigQuery storage APIs; otherwise
              global endpoints would be used.
        """
        return self._use_regional_endpoints

    @use_regional_endpoints.setter
    def use_regional_endpoints(self, value: bool):
        if self._session_started and self._use_regional_endpoints != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="use_regional_endpoints")
            )

        if value:
            msg = bfe.format_message(
                "Use of regional endpoints is a feature in preview and "
                "available only in selected regions and projects. "
            )
            warnings.warn(msg, category=bfe.PreviewWarning, stacklevel=2)

        self._use_regional_endpoints = value

    @property
    def kms_key_name(self) -> Optional[str]:
        """
        Customer managed encryption key used to control encryption of the
        data-at-rest in BigQuery. This is of the format
        projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY.

        For more information, see https://cloud.google.com/bigquery/docs/customer-managed-encryption
        Customer-managed Cloud KMS keys

        Make sure the project used for Bigquery DataFrames has the
        Cloud KMS CryptoKey Encrypter/Decrypter IAM role in the key's project.
        For more information, see https://cloud.google.com/bigquery/docs/customer-managed-encryption#assign_role
        Assign the Encrypter/Decrypter.

        Returns:
            None or str:
                Name of the customer managed encryption key as a string; otherwise None.
        """
        return self._kms_key_name

    @kms_key_name.setter
    def kms_key_name(self, value: str):
        if self._session_started and self._kms_key_name != value:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="kms_key_name"))

        self._kms_key_name = value

    @property
    def ordering_mode(self) -> Literal["strict", "partial"]:
        """Controls whether total row order is always maintained for DataFrame/Series.

        Returns:
            Literal:
                A literal string value of either strict or partial ordering mode.
        """
        return self._ordering_mode.value

    @ordering_mode.setter
    def ordering_mode(self, value: Literal["strict", "partial"]) -> None:
        ordering_mode = _validate_ordering_mode(value)
        if self._session_started and self._ordering_mode != ordering_mode:
            raise ValueError(SESSION_STARTED_MESSAGE.format(attribute="ordering_mode"))
        self._ordering_mode = ordering_mode

    @property
    def client_endpoints_override(self) -> dict:
        """Option that sets the BQ client endpoints addresses directly as a dict. Possible keys are "bqclient", "bqconnectionclient", "bqstoragereadclient"."""
        return self._client_endpoints_override

    @client_endpoints_override.setter
    def client_endpoints_override(self, value: dict):
        msg = bfe.format_message(
            "This is an advanced configuration option for directly setting endpoints. "
            "Incorrect use may lead to unexpected behavior or system instability. "
            "Proceed only if you fully understand its implications."
        )
        warnings.warn(msg)

        if self._session_started and self._client_endpoints_override != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="client_endpoints_override")
            )

        self._client_endpoints_override = value

    @property
    def requests_transport_adapters(
        self,
    ) -> Sequence[Tuple[str, requests.adapters.BaseAdapter]]:
        """Transport adapters for requests-based REST clients such as the
        google-cloud-bigquery package.

        For more details, see the explanation in `requests guide to transport
        adapters
        <https://requests.readthedocs.io/en/latest/user/advanced/#transport-adapters>`_.

        **Examples:**

        Increase the connection pool size using the requests `HTTPAdapter
        <https://requests.readthedocs.io/en/latest/api/#requests.adapters.HTTPAdapter>`_.

            >>> import bigframes.pandas as bpd
            >>> bpd.options.bigquery.requests_transport_adapters = (
            ...     ("http://", requests.adapters.HTTPAdapter(pool_maxsize=100)),
            ...     ("https://", requests.adapters.HTTPAdapter(pool_maxsize=100)),
            ... )  # doctest: +SKIP

        Returns:
            Sequence[Tuple[str, requests.adapters.BaseAdapter]]:
                Prefixes and corresponding transport adapters to `mount
                <https://requests.readthedocs.io/en/latest/api/#requests.Session.mount>`_
                in requests-based REST clients.
        """
        return self._requests_transport_adapters

    @requests_transport_adapters.setter
    def requests_transport_adapters(
        self, value: Sequence[Tuple[str, requests.adapters.BaseAdapter]]
    ) -> None:
        if self._session_started and self._requests_transport_adapters != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="requests_transport_adapters")
            )
        self._requests_transport_adapters = value

    @property
    def enable_polars_execution(self) -> bool:
        """If True, will use polars to execute some simple query plans locally."""
        return self._enable_polars_execution

    @enable_polars_execution.setter
    def enable_polars_execution(self, value: bool):
        if self._session_started and self._enable_polars_execution != value:
            raise ValueError(
                SESSION_STARTED_MESSAGE.format(attribute="enable_polars_execution")
            )
        if value is True:
            msg = bfe.format_message(
                "Polars execution is an experimental feature, and may not be stable. Must have polars installed."
            )
            warnings.warn(msg, category=bfe.PreviewWarning)
            bigframes._importing.import_polars()
        self._enable_polars_execution = value
