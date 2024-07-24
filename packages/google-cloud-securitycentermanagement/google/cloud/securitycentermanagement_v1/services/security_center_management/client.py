# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
from collections import OrderedDict
import os
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.securitycentermanagement_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.securitycentermanagement_v1.services.security_center_management import (
    pagers,
)
from google.cloud.securitycentermanagement_v1.types import security_center_management

from .transports.base import DEFAULT_CLIENT_INFO, SecurityCenterManagementTransport
from .transports.grpc import SecurityCenterManagementGrpcTransport
from .transports.grpc_asyncio import SecurityCenterManagementGrpcAsyncIOTransport
from .transports.rest import SecurityCenterManagementRestTransport


class SecurityCenterManagementClientMeta(type):
    """Metaclass for the SecurityCenterManagement client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[SecurityCenterManagementTransport]]
    _transport_registry["grpc"] = SecurityCenterManagementGrpcTransport
    _transport_registry["grpc_asyncio"] = SecurityCenterManagementGrpcAsyncIOTransport
    _transport_registry["rest"] = SecurityCenterManagementRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[SecurityCenterManagementTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class SecurityCenterManagementClient(metaclass=SecurityCenterManagementClientMeta):
    """Service describing handlers for resources"""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "securitycentermanagement.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "securitycentermanagement.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SecurityCenterManagementClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SecurityCenterManagementClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SecurityCenterManagementTransport:
        """Returns the transport used by the client instance.

        Returns:
            SecurityCenterManagementTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def effective_event_threat_detection_custom_module_path(
        organization: str,
        location: str,
        effective_event_threat_detection_custom_module: str,
    ) -> str:
        """Returns a fully-qualified effective_event_threat_detection_custom_module string."""
        return "organizations/{organization}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}".format(
            organization=organization,
            location=location,
            effective_event_threat_detection_custom_module=effective_event_threat_detection_custom_module,
        )

    @staticmethod
    def parse_effective_event_threat_detection_custom_module_path(
        path: str,
    ) -> Dict[str, str]:
        """Parses a effective_event_threat_detection_custom_module path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/locations/(?P<location>.+?)/effectiveEventThreatDetectionCustomModules/(?P<effective_event_threat_detection_custom_module>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def effective_security_health_analytics_custom_module_path(
        organization: str,
        location: str,
        effective_security_health_analytics_custom_module: str,
    ) -> str:
        """Returns a fully-qualified effective_security_health_analytics_custom_module string."""
        return "organizations/{organization}/locations/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}".format(
            organization=organization,
            location=location,
            effective_security_health_analytics_custom_module=effective_security_health_analytics_custom_module,
        )

    @staticmethod
    def parse_effective_security_health_analytics_custom_module_path(
        path: str,
    ) -> Dict[str, str]:
        """Parses a effective_security_health_analytics_custom_module path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/locations/(?P<location>.+?)/effectiveSecurityHealthAnalyticsCustomModules/(?P<effective_security_health_analytics_custom_module>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def event_threat_detection_custom_module_path(
        organization: str,
        location: str,
        event_threat_detection_custom_module: str,
    ) -> str:
        """Returns a fully-qualified event_threat_detection_custom_module string."""
        return "organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}".format(
            organization=organization,
            location=location,
            event_threat_detection_custom_module=event_threat_detection_custom_module,
        )

    @staticmethod
    def parse_event_threat_detection_custom_module_path(path: str) -> Dict[str, str]:
        """Parses a event_threat_detection_custom_module path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/locations/(?P<location>.+?)/eventThreatDetectionCustomModules/(?P<event_threat_detection_custom_module>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def finding_path(
        organization: str,
        source: str,
        finding: str,
    ) -> str:
        """Returns a fully-qualified finding string."""
        return (
            "organizations/{organization}/sources/{source}/findings/{finding}".format(
                organization=organization,
                source=source,
                finding=finding,
            )
        )

    @staticmethod
    def parse_finding_path(path: str) -> Dict[str, str]:
        """Parses a finding path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/sources/(?P<source>.+?)/findings/(?P<finding>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def security_center_service_path(
        project: str,
        location: str,
        service: str,
    ) -> str:
        """Returns a fully-qualified security_center_service string."""
        return "projects/{project}/locations/{location}/securityCenterServices/{service}".format(
            project=project,
            location=location,
            service=service,
        )

    @staticmethod
    def parse_security_center_service_path(path: str) -> Dict[str, str]:
        """Parses a security_center_service path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/securityCenterServices/(?P<service>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def security_health_analytics_custom_module_path(
        organization: str,
        location: str,
        security_health_analytics_custom_module: str,
    ) -> str:
        """Returns a fully-qualified security_health_analytics_custom_module string."""
        return "organizations/{organization}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}".format(
            organization=organization,
            location=location,
            security_health_analytics_custom_module=security_health_analytics_custom_module,
        )

    @staticmethod
    def parse_security_health_analytics_custom_module_path(path: str) -> Dict[str, str]:
        """Parses a security_health_analytics_custom_module path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/locations/(?P<location>.+?)/securityHealthAnalyticsCustomModules/(?P<security_health_analytics_custom_module>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = SecurityCenterManagementClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = SecurityCenterManagementClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = (
                SecurityCenterManagementClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=universe_domain
                )
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = SecurityCenterManagementClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    @staticmethod
    def _compare_universes(
        client_universe: str, credentials: ga_credentials.Credentials
    ) -> bool:
        """Returns True iff the universe domains used by the client and credentials match.

        Args:
            client_universe (str): The universe domain configured via the client options.
            credentials (ga_credentials.Credentials): The credentials being used in the client.

        Returns:
            bool: True iff client_universe matches the universe in credentials.

        Raises:
            ValueError: when client_universe does not match the universe in credentials.
        """

        default_universe = SecurityCenterManagementClient._DEFAULT_UNIVERSE
        credentials_universe = getattr(credentials, "universe_domain", default_universe)

        if client_universe != credentials_universe:
            raise ValueError(
                "The configured universe domain "
                f"({client_universe}) does not match the universe domain "
                f"found in the credentials ({credentials_universe}). "
                "If you haven't configured the universe domain explicitly, "
                f"`{default_universe}` is the default."
            )
        return True

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """
        self._is_universe_domain_valid = (
            self._is_universe_domain_valid
            or SecurityCenterManagementClient._compare_universes(
                self.universe_domain, self.transport._credentials
            )
        )
        return self._is_universe_domain_valid

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                SecurityCenterManagementTransport,
                Callable[..., SecurityCenterManagementTransport],
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the security center management client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,SecurityCenterManagementTransport,Callable[..., SecurityCenterManagementTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the SecurityCenterManagementTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = SecurityCenterManagementClient._read_environment_variables()
        self._client_cert_source = (
            SecurityCenterManagementClient._get_client_cert_source(
                self._client_options.client_cert_source, self._use_client_cert
            )
        )
        self._universe_domain = SecurityCenterManagementClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, SecurityCenterManagementTransport)
        if transport_provided:
            # transport is a SecurityCenterManagementTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(SecurityCenterManagementTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or SecurityCenterManagementClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint,
            )
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            transport_init: Union[
                Type[SecurityCenterManagementTransport],
                Callable[..., SecurityCenterManagementTransport],
            ] = (
                type(self).get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., SecurityCenterManagementTransport], transport)
            )
            # initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

    def list_effective_security_health_analytics_custom_modules(
        self,
        request: Optional[
            Union[
                security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEffectiveSecurityHealthAnalyticsCustomModulesPager:
        r"""Returns a list of all
        EffectiveSecurityHealthAnalyticsCustomModules for the
        given parent. This includes resident modules defined at
        the scope of the parent, and inherited modules,
        inherited from CRM ancestors (no descendants).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_effective_security_health_analytics_custom_modules():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_effective_security_health_analytics_custom_modules(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest, dict]):
                The request object. Request message for listing effective
                Security Health Analytics custom
                modules.
            parent (str):
                Required. Name of parent to list effective custom
                modules. specified in one of the following formats:

                -  ``organizations/{organization}/locations/{location}``
                -  ``folders/{folder}/locations/{location}`` or
                   ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListEffectiveSecurityHealthAnalyticsCustomModulesPager:
                Response message for listing
                effective Security Health Analytics
                custom modules.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        ):
            request = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_effective_security_health_analytics_custom_modules
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEffectiveSecurityHealthAnalyticsCustomModulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_effective_security_health_analytics_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.EffectiveSecurityHealthAnalyticsCustomModule:
        r"""Gets details of a single
        EffectiveSecurityHealthAnalyticsCustomModule.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_get_effective_security_health_analytics_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_effective_security_health_analytics_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest, dict]):
                The request object. Message for getting a
                EffectiveSecurityHealthAnalyticsCustomModule
            name (str):
                Required. The full resource name of the custom module,
                specified in one of the following formats:

                -  ``organizations/organization/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
                -  ``folders/folder/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
                -  ``projects/project/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.EffectiveSecurityHealthAnalyticsCustomModule:
                An EffectiveSecurityHealthAnalyticsCustomModule is the representation of
                   a Security Health Analytics custom module at a
                   specified level of the resource hierarchy:
                   organization, folder, or project. If a custom module
                   is inherited from a parent organization or folder,
                   the value of the enablementState property in
                   EffectiveSecurityHealthAnalyticsCustomModule is set
                   to the value that is effective in the parent, instead
                   of INHERITED. For example, if the module is enabled
                   in a parent organization or folder, the effective
                   enablement_state for the module in all child folders
                   or projects is also enabled.
                   EffectiveSecurityHealthAnalyticsCustomModule is
                   read-only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
        ):
            request = security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_effective_security_health_analytics_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_security_health_analytics_custom_modules(
        self,
        request: Optional[
            Union[
                security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSecurityHealthAnalyticsCustomModulesPager:
        r"""Returns a list of all
        SecurityHealthAnalyticsCustomModules for the given
        parent. This includes resident modules defined at the
        scope of the parent, and inherited modules, inherited
        from CRM ancestors (no descendants).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_security_health_analytics_custom_modules():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListSecurityHealthAnalyticsCustomModulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_security_health_analytics_custom_modules(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListSecurityHealthAnalyticsCustomModulesRequest, dict]):
                The request object. Request message for listing Security
                Health Analytics custom modules.
            parent (str):
                Required. Name of parent organization, folder, or
                project in which to list custom modules, specified in
                one of the following formats:

                -  ``organizations/{organization}/locations/{location}``
                -  ``folders/{folder}/locations/{location}``
                -  ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListSecurityHealthAnalyticsCustomModulesPager:
                Response message for listing Security
                Health Analytics custom modules.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
        ):
            request = security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_security_health_analytics_custom_modules
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSecurityHealthAnalyticsCustomModulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_descendant_security_health_analytics_custom_modules(
        self,
        request: Optional[
            Union[
                security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDescendantSecurityHealthAnalyticsCustomModulesPager:
        r"""Returns a list of all resident
        SecurityHealthAnalyticsCustomModules under the given CRM
        parent and all of the parent's CRM descendants.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_descendant_security_health_analytics_custom_modules():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_descendant_security_health_analytics_custom_modules(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesRequest, dict]):
                The request object. Request message for listing
                descendant Security Health Analytics
                custom modules.
            parent (str):
                Required. Name of the parent organization, folder, or
                project in which to list custom modules, specified in
                one of the following formats:

                -  ``organizations/{organization}/locations/{location}``
                -  ``folders/{folder}/locations/{location}``
                -  ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListDescendantSecurityHealthAnalyticsCustomModulesPager:
                Response message for listing
                descendant Security Health Analytics
                custom modules.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        ):
            request = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_descendant_security_health_analytics_custom_modules
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDescendantSecurityHealthAnalyticsCustomModulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_security_health_analytics_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
        r"""Retrieves a SecurityHealthAnalyticsCustomModule.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_get_security_health_analytics_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.GetSecurityHealthAnalyticsCustomModuleRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_security_health_analytics_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.GetSecurityHealthAnalyticsCustomModuleRequest, dict]):
                The request object. Message for getting a
                SecurityHealthAnalyticsCustomModule
            name (str):
                Required. Name of the resource
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule:
                Represents an instance of a Security
                Health Analytics custom module,
                including its full module name, display
                name, enablement state, and last updated
                time. You can create a custom module at
                the organization, folder, or project
                level. Custom modules that you create at
                the organization or folder level are
                inherited by the child folders and
                projects.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
        ):
            request = security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_security_health_analytics_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_security_health_analytics_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        security_health_analytics_custom_module: Optional[
            security_center_management.SecurityHealthAnalyticsCustomModule
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
        r"""Creates a resident
        SecurityHealthAnalyticsCustomModule at the scope of the
        given CRM parent, and also creates inherited
        SecurityHealthAnalyticsCustomModules for all CRM
        descendants of the given parent. These modules are
        enabled by default.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_create_security_health_analytics_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.CreateSecurityHealthAnalyticsCustomModuleRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_security_health_analytics_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.CreateSecurityHealthAnalyticsCustomModuleRequest, dict]):
                The request object. Message for creating a
                SecurityHealthAnalyticsCustomModule
            parent (str):
                Required. Name of the parent organization, folder, or
                project of the module, specified in one of the following
                formats:

                -  ``organizations/{organization}/locations/{location}``
                -  ``folders/{folder}/locations/{location}``
                -  ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_health_analytics_custom_module (google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule):
                Required. The resource being created
                This corresponds to the ``security_health_analytics_custom_module`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule:
                Represents an instance of a Security
                Health Analytics custom module,
                including its full module name, display
                name, enablement state, and last updated
                time. You can create a custom module at
                the organization, folder, or project
                level. Custom modules that you create at
                the organization or folder level are
                inherited by the child folders and
                projects.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, security_health_analytics_custom_module])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
        ):
            request = security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if security_health_analytics_custom_module is not None:
                request.security_health_analytics_custom_module = (
                    security_health_analytics_custom_module
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_security_health_analytics_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_security_health_analytics_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        security_health_analytics_custom_module: Optional[
            security_center_management.SecurityHealthAnalyticsCustomModule
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
        r"""Updates the SecurityHealthAnalyticsCustomModule under
        the given name based on the given update mask. Updating
        the enablement state is supported on both resident and
        inherited modules (though resident modules cannot have
        an enablement state of "inherited"). Updating the
        display name and custom config of a module is supported
        on resident modules only.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_update_security_health_analytics_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.UpdateSecurityHealthAnalyticsCustomModuleRequest(
                )

                # Make the request
                response = client.update_security_health_analytics_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.UpdateSecurityHealthAnalyticsCustomModuleRequest, dict]):
                The request object. Message for updating a
                SecurityHealthAnalyticsCustomModule
            security_health_analytics_custom_module (google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule):
                Required. The resource being updated
                This corresponds to the ``security_health_analytics_custom_module`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to be updated. The only
                fields that can be updated are ``enablement_state`` and
                ``custom_config``. If empty or set to the wildcard value
                ``*``, both ``enablement_state`` and ``custom_config``
                are updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule:
                Represents an instance of a Security
                Health Analytics custom module,
                including its full module name, display
                name, enablement state, and last updated
                time. You can create a custom module at
                the organization, folder, or project
                level. Custom modules that you create at
                the organization or folder level are
                inherited by the child folders and
                projects.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [security_health_analytics_custom_module, update_mask]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
        ):
            request = security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if security_health_analytics_custom_module is not None:
                request.security_health_analytics_custom_module = (
                    security_health_analytics_custom_module
                )
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_security_health_analytics_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "security_health_analytics_custom_module.name",
                        request.security_health_analytics_custom_module.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_security_health_analytics_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified
        SecurityHealthAnalyticsCustomModule and all of its
        descendants in the CRM hierarchy. This method is only
        supported for resident custom modules.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_delete_security_health_analytics_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.DeleteSecurityHealthAnalyticsCustomModuleRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_security_health_analytics_custom_module(request=request)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.DeleteSecurityHealthAnalyticsCustomModuleRequest, dict]):
                The request object. Message for deleting a
                SecurityHealthAnalyticsCustomModule
            name (str):
                Required. The resource name of the SHA custom module.

                Its format is:

                -  ``organizations/{organization}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``.
                -  ``folders/{folder}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``.
                -  ``projects/{project}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
        ):
            request = security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_security_health_analytics_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def simulate_security_health_analytics_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        custom_config: Optional[security_center_management.CustomConfig] = None,
        resource: Optional[
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse:
        r"""Simulates a given SecurityHealthAnalyticsCustomModule
        and Resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_simulate_security_health_analytics_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                resource = securitycentermanagement_v1.SimulatedResource()
                resource.resource_type = "resource_type_value"

                request = securitycentermanagement_v1.SimulateSecurityHealthAnalyticsCustomModuleRequest(
                    parent="parent_value",
                    resource=resource,
                )

                # Make the request
                response = client.simulate_security_health_analytics_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.SimulateSecurityHealthAnalyticsCustomModuleRequest, dict]):
                The request object. Request message to simulate a
                CustomConfig against a given test
                resource. Maximum size of the request is
                4 MB by default.
            parent (str):
                Required. The relative resource name of the
                organization, project, or folder. For more information
                about relative resource names, see `Relative Resource
                Name <https://cloud.google.com/apis/design/resource_names#relative_resource_name>`__
                Example: ``organizations/{organization_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_config (google.cloud.securitycentermanagement_v1.types.CustomConfig):
                Required. The custom configuration
                that you need to test.

                This corresponds to the ``custom_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (google.cloud.securitycentermanagement_v1.types.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource):
                Required. Resource data to simulate
                custom module against.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.SimulateSecurityHealthAnalyticsCustomModuleResponse:
                Response message for simulating a SecurityHealthAnalyticsCustomModule
                   against a given resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_config, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
        ):
            request = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if custom_config is not None:
                request.custom_config = custom_config
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.simulate_security_health_analytics_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_effective_event_threat_detection_custom_modules(
        self,
        request: Optional[
            Union[
                security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEffectiveEventThreatDetectionCustomModulesPager:
        r"""Lists all effective Event Threat Detection custom
        modules for the given parent. This includes resident
        modules defined at the scope of the parent along with
        modules inherited from its ancestors.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_effective_event_threat_detection_custom_modules():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListEffectiveEventThreatDetectionCustomModulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_effective_event_threat_detection_custom_modules(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListEffectiveEventThreatDetectionCustomModulesRequest, dict]):
                The request object. Request message for listing effective
                Event Threat Detection custom modules.
            parent (str):
                Required. Name of parent to list effective custom
                modules. Its format is
                ``organizations/{organization}/locations/{location}``,
                ``folders/{folder}/locations/{location}``, or
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListEffectiveEventThreatDetectionCustomModulesPager:
                Response message for listing
                effective Event Threat Detection custom
                modules.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
        ):
            request = security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_effective_event_threat_detection_custom_modules
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEffectiveEventThreatDetectionCustomModulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_effective_event_threat_detection_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.EffectiveEventThreatDetectionCustomModule:
        r"""Gets an effective ETD custom module. Retrieves the effective
        module at the given level. The difference between an
        EffectiveCustomModule and a CustomModule is that the fields for
        an EffectiveCustomModule are computed from ancestors if needed.
        For example, the enablement_state for a CustomModule can be
        either ENABLED, DISABLED, or INHERITED. Where as the
        enablement_state for an EffectiveCustomModule is always computed
        to ENABLED or DISABLED (the effective enablement_state).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_get_effective_event_threat_detection_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.GetEffectiveEventThreatDetectionCustomModuleRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_effective_event_threat_detection_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.GetEffectiveEventThreatDetectionCustomModuleRequest, dict]):
                The request object. Message for getting a
                EffectiveEventThreatDetectionCustomModule
            name (str):
                Required. The resource name of the ETD custom module.

                Its format is:

                -  ``organizations/{organization}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
                -  ``folders/{folder}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
                -  ``projects/{project}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.EffectiveEventThreatDetectionCustomModule:
                An EffectiveEventThreatDetectionCustomModule is the representation of
                   EventThreatDetectionCustomModule at a given level
                   taking hierarchy into account and resolving various
                   fields accordingly. e.g. if the module is enabled at
                   the ancestor level, effective modules at all
                   descendant levels will have enablement_state set to
                   ENABLED. Similarly, if module.inherited is set, then
                   effective module's config will contain the ancestor's
                   config details.
                   EffectiveEventThreatDetectionCustomModule is
                   read-only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
        ):
            request = security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_effective_event_threat_detection_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_event_threat_detection_custom_modules(
        self,
        request: Optional[
            Union[
                security_center_management.ListEventThreatDetectionCustomModulesRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEventThreatDetectionCustomModulesPager:
        r"""Lists all Event Threat Detection custom modules for
        the given Resource Manager parent. This includes
        resident modules defined at the scope of the parent
        along with modules inherited from ancestors.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_event_threat_detection_custom_modules():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListEventThreatDetectionCustomModulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_event_threat_detection_custom_modules(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListEventThreatDetectionCustomModulesRequest, dict]):
                The request object. Request message for listing Event
                Threat Detection custom modules.
            parent (str):
                Required. Name of parent to list custom modules. Its
                format is
                ``organizations/{organization}/locations/{location}``,
                ``folders/{folder}/locations/{location}``, or
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListEventThreatDetectionCustomModulesPager:
                Response message for listing Event
                Threat Detection custom modules.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ListEventThreatDetectionCustomModulesRequest,
        ):
            request = (
                security_center_management.ListEventThreatDetectionCustomModulesRequest(
                    request
                )
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_event_threat_detection_custom_modules
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEventThreatDetectionCustomModulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_descendant_event_threat_detection_custom_modules(
        self,
        request: Optional[
            Union[
                security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDescendantEventThreatDetectionCustomModulesPager:
        r"""Lists all resident Event Threat Detection custom
        modules under the given Resource Manager parent and its
        descendants.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_descendant_event_threat_detection_custom_modules():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListDescendantEventThreatDetectionCustomModulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_descendant_event_threat_detection_custom_modules(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListDescendantEventThreatDetectionCustomModulesRequest, dict]):
                The request object. Request message for listing
                descendant Event Threat Detection custom
                modules.
            parent (str):
                Required. Name of parent to list custom modules. Its
                format is
                ``organizations/{organization}/locations/{location}``,
                ``folders/{folder}/locations/{location}``, or
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListDescendantEventThreatDetectionCustomModulesPager:
                Response message for listing
                descendant Event Threat Detection custom
                modules.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
        ):
            request = security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_descendant_event_threat_detection_custom_modules
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDescendantEventThreatDetectionCustomModulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_event_threat_detection_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.GetEventThreatDetectionCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.EventThreatDetectionCustomModule:
        r"""Gets an Event Threat Detection custom module.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_get_event_threat_detection_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.GetEventThreatDetectionCustomModuleRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_event_threat_detection_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.GetEventThreatDetectionCustomModuleRequest, dict]):
                The request object. Message for getting a
                EventThreatDetectionCustomModule
            name (str):
                Required. The resource name of the ETD custom module.

                Its format is:

                -  ``organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
                -  ``folders/{folder}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
                -  ``projects/{project}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule:
                An event threat detection custom
                module is a Cloud SCC resource that
                contains the configuration and
                enablement state of a custom module,
                which enables ETD to write certain
                findings to Cloud SCC.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.GetEventThreatDetectionCustomModuleRequest,
        ):
            request = (
                security_center_management.GetEventThreatDetectionCustomModuleRequest(
                    request
                )
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_event_threat_detection_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_event_threat_detection_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.CreateEventThreatDetectionCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        event_threat_detection_custom_module: Optional[
            security_center_management.EventThreatDetectionCustomModule
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.EventThreatDetectionCustomModule:
        r"""Creates a resident Event Threat Detection custom
        module at the scope of the given Resource Manager
        parent, and also creates inherited custom modules for
        all descendants of the given parent. These modules are
        enabled by default.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_create_event_threat_detection_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.CreateEventThreatDetectionCustomModuleRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_event_threat_detection_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.CreateEventThreatDetectionCustomModuleRequest, dict]):
                The request object. Message for creating a
                EventThreatDetectionCustomModule
            parent (str):
                Required. Name of parent for the module. Its format is
                ``organizations/{organization}/locations/{location}``,
                ``folders/{folder}/locations/{location}``, or
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_threat_detection_custom_module (google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule):
                Required. The module to create. The
                event_threat_detection_custom_module.name will be
                ignored and server generated.

                This corresponds to the ``event_threat_detection_custom_module`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule:
                An event threat detection custom
                module is a Cloud SCC resource that
                contains the configuration and
                enablement state of a custom module,
                which enables ETD to write certain
                findings to Cloud SCC.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, event_threat_detection_custom_module])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.CreateEventThreatDetectionCustomModuleRequest,
        ):
            request = security_center_management.CreateEventThreatDetectionCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if event_threat_detection_custom_module is not None:
                request.event_threat_detection_custom_module = (
                    event_threat_detection_custom_module
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_event_threat_detection_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_event_threat_detection_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        event_threat_detection_custom_module: Optional[
            security_center_management.EventThreatDetectionCustomModule
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.EventThreatDetectionCustomModule:
        r"""Updates the Event Threat Detection custom module with
        the given name based on the given update mask. Updating
        the enablement state is supported for both resident and
        inherited modules (though resident modules cannot have
        an enablement state of "inherited"). Updating the
        display name or configuration of a module is supported
        for resident modules only. The type of a module cannot
        be changed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_update_event_threat_detection_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.UpdateEventThreatDetectionCustomModuleRequest(
                )

                # Make the request
                response = client.update_event_threat_detection_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.UpdateEventThreatDetectionCustomModuleRequest, dict]):
                The request object. Message for updating a
                EventThreatDetectionCustomModule
            event_threat_detection_custom_module (google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule):
                Required. The module being updated
                This corresponds to the ``event_threat_detection_custom_module`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the EventThreatDetectionCustomModule
                resource by the update. The fields specified in the
                update_mask are relative to the resource, not the full
                request. A field will be overwritten if it is in the
                mask. If the user does not provide a mask then all
                fields will be overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule:
                An event threat detection custom
                module is a Cloud SCC resource that
                contains the configuration and
                enablement state of a custom module,
                which enables ETD to write certain
                findings to Cloud SCC.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([event_threat_detection_custom_module, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
        ):
            request = security_center_management.UpdateEventThreatDetectionCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if event_threat_detection_custom_module is not None:
                request.event_threat_detection_custom_module = (
                    event_threat_detection_custom_module
                )
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_event_threat_detection_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "event_threat_detection_custom_module.name",
                        request.event_threat_detection_custom_module.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_event_threat_detection_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified Event Threat Detection custom
        module and all of its descendants in the Resource
        Manager hierarchy. This method is only supported for
        resident custom modules.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_delete_event_threat_detection_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.DeleteEventThreatDetectionCustomModuleRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_event_threat_detection_custom_module(request=request)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.DeleteEventThreatDetectionCustomModuleRequest, dict]):
                The request object. Message for deleting a
                EventThreatDetectionCustomModule
            name (str):
                Required. The resource name of the ETD custom module.

                Its format is:

                -  ``organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
                -  ``folders/{folder}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
                -  ``projects/{project}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
        ):
            request = security_center_management.DeleteEventThreatDetectionCustomModuleRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_event_threat_detection_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def validate_event_threat_detection_custom_module(
        self,
        request: Optional[
            Union[
                security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
                dict,
            ]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.ValidateEventThreatDetectionCustomModuleResponse:
        r"""Validates the given Event Threat Detection custom
        module.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_validate_event_threat_detection_custom_module():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ValidateEventThreatDetectionCustomModuleRequest(
                    parent="parent_value",
                    raw_text="raw_text_value",
                    type_="type__value",
                )

                # Make the request
                response = client.validate_event_threat_detection_custom_module(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ValidateEventThreatDetectionCustomModuleRequest, dict]):
                The request object. Request to validate an Event Threat
                Detection custom module.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.ValidateEventThreatDetectionCustomModuleResponse:
                Response to validating an Event
                Threat Detection custom module.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
        ):
            request = security_center_management.ValidateEventThreatDetectionCustomModuleRequest(
                request
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.validate_event_threat_detection_custom_module
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_security_center_service(
        self,
        request: Optional[
            Union[security_center_management.GetSecurityCenterServiceRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.SecurityCenterService:
        r"""Gets service settings for the specified Security
        Command Center service.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_get_security_center_service():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.GetSecurityCenterServiceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_security_center_service(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.GetSecurityCenterServiceRequest, dict]):
                The request object. Request message for getting a
                Security Command Center service.
            name (str):
                Required. The Security Command Center service to
                retrieve.

                Formats:

                -  organizations/{organization}/locations/{location}/securityCenterServices/{service}
                -  folders/{folder}/locations/{location}/securityCenterServices/{service}
                -  projects/{project}/locations/{location}/securityCenterServices/{service}

                The possible values for id {service} are:

                -  container-threat-detection
                -  event-threat-detection
                -  security-health-analytics
                -  vm-threat-detection
                -  web-security-scanner

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.SecurityCenterService:
                Represents a particular Security
                Command Center service. This includes
                settings information such as top-level
                enablement in addition to individual
                module settings. Service settings can be
                configured at the organization, folder,
                or project level. Service settings at
                the organization or folder level are
                inherited by those in child folders and
                projects.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, security_center_management.GetSecurityCenterServiceRequest
        ):
            request = security_center_management.GetSecurityCenterServiceRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_security_center_service
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_security_center_services(
        self,
        request: Optional[
            Union[security_center_management.ListSecurityCenterServicesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSecurityCenterServicesPager:
        r"""Returns a list of all Security Command Center
        services for the given parent.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_list_security_center_services():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.ListSecurityCenterServicesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_security_center_services(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.ListSecurityCenterServicesRequest, dict]):
                The request object. Request message for listing Security
                Command Center services.
            parent (str):
                Required. The name of the parent to list Security
                Command Center services.

                Formats:

                -  organizations/{organization}/locations/{location}
                -  folders/{folder}/locations/{location}
                -  projects/{project}/locations/{location}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.services.security_center_management.pagers.ListSecurityCenterServicesPager:
                Response message for listing Security
                Command Center services.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, security_center_management.ListSecurityCenterServicesRequest
        ):
            request = security_center_management.ListSecurityCenterServicesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_security_center_services
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSecurityCenterServicesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_security_center_service(
        self,
        request: Optional[
            Union[security_center_management.UpdateSecurityCenterServiceRequest, dict]
        ] = None,
        *,
        security_center_service: Optional[
            security_center_management.SecurityCenterService
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_center_management.SecurityCenterService:
        r"""Updates a Security Command Center service using the
        given update mask.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycentermanagement_v1

            def sample_update_security_center_service():
                # Create a client
                client = securitycentermanagement_v1.SecurityCenterManagementClient()

                # Initialize request argument(s)
                request = securitycentermanagement_v1.UpdateSecurityCenterServiceRequest(
                )

                # Make the request
                response = client.update_security_center_service(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycentermanagement_v1.types.UpdateSecurityCenterServiceRequest, dict]):
                The request object. Request message for updating a
                Security Command Center service.
            security_center_service (google.cloud.securitycentermanagement_v1.types.SecurityCenterService):
                Required. The updated service.
                This corresponds to the ``security_center_service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to be updated. Possible
                values:

                -  "intended_enablement_state"
                -  "modules"

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.securitycentermanagement_v1.types.SecurityCenterService:
                Represents a particular Security
                Command Center service. This includes
                settings information such as top-level
                enablement in addition to individual
                module settings. Service settings can be
                configured at the organization, folder,
                or project level. Service settings at
                the organization or folder level are
                inherited by those in child folders and
                projects.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([security_center_service, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, security_center_management.UpdateSecurityCenterServiceRequest
        ):
            request = security_center_management.UpdateSecurityCenterServiceRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if security_center_service is not None:
                request.security_center_service = security_center_service
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_security_center_service
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "security_center_service.name",
                        request.security_center_service.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "SecurityCenterManagementClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_location,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_locations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("SecurityCenterManagementClient",)
