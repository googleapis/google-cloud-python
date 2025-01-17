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
import logging as std_logging
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

from google.cloud.accesscontextmanager_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.accesscontextmanager_v1.services.access_context_manager import pagers
from google.cloud.accesscontextmanager_v1.types import access_level as gia_access_level
from google.cloud.accesscontextmanager_v1.types import (
    gcp_user_access_binding as gia_gcp_user_access_binding,
)
from google.cloud.accesscontextmanager_v1.types import (
    service_perimeter as gia_service_perimeter,
)
from google.cloud.accesscontextmanager_v1.types import access_context_manager
from google.cloud.accesscontextmanager_v1.types import access_level
from google.cloud.accesscontextmanager_v1.types import access_policy
from google.cloud.accesscontextmanager_v1.types import gcp_user_access_binding
from google.cloud.accesscontextmanager_v1.types import service_perimeter

from .transports.base import DEFAULT_CLIENT_INFO, AccessContextManagerTransport
from .transports.grpc import AccessContextManagerGrpcTransport
from .transports.grpc_asyncio import AccessContextManagerGrpcAsyncIOTransport
from .transports.rest import AccessContextManagerRestTransport


class AccessContextManagerClientMeta(type):
    """Metaclass for the AccessContextManager client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[AccessContextManagerTransport]]
    _transport_registry["grpc"] = AccessContextManagerGrpcTransport
    _transport_registry["grpc_asyncio"] = AccessContextManagerGrpcAsyncIOTransport
    _transport_registry["rest"] = AccessContextManagerRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[AccessContextManagerTransport]:
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


class AccessContextManagerClient(metaclass=AccessContextManagerClientMeta):
    """API for setting [access levels]
    [google.identity.accesscontextmanager.v1.AccessLevel] and [service
    perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter] for
    Google Cloud projects. Each organization has one [access policy]
    [google.identity.accesscontextmanager.v1.AccessPolicy] that contains
    the [access levels]
    [google.identity.accesscontextmanager.v1.AccessLevel] and [service
    perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter]. This
    [access policy]
    [google.identity.accesscontextmanager.v1.AccessPolicy] is applicable
    to all resources in the organization. AccessPolicies
    """

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
    DEFAULT_ENDPOINT = "accesscontextmanager.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "accesscontextmanager.{UNIVERSE_DOMAIN}"
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
            AccessContextManagerClient: The constructed client.
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
            AccessContextManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AccessContextManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            AccessContextManagerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def access_level_path(
        access_policy: str,
        access_level: str,
    ) -> str:
        """Returns a fully-qualified access_level string."""
        return "accessPolicies/{access_policy}/accessLevels/{access_level}".format(
            access_policy=access_policy,
            access_level=access_level,
        )

    @staticmethod
    def parse_access_level_path(path: str) -> Dict[str, str]:
        """Parses a access_level path into its component segments."""
        m = re.match(
            r"^accessPolicies/(?P<access_policy>.+?)/accessLevels/(?P<access_level>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def access_policy_path(
        access_policy: str,
    ) -> str:
        """Returns a fully-qualified access_policy string."""
        return "accessPolicies/{access_policy}".format(
            access_policy=access_policy,
        )

    @staticmethod
    def parse_access_policy_path(path: str) -> Dict[str, str]:
        """Parses a access_policy path into its component segments."""
        m = re.match(r"^accessPolicies/(?P<access_policy>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def gcp_user_access_binding_path(
        organization: str,
        gcp_user_access_binding: str,
    ) -> str:
        """Returns a fully-qualified gcp_user_access_binding string."""
        return "organizations/{organization}/gcpUserAccessBindings/{gcp_user_access_binding}".format(
            organization=organization,
            gcp_user_access_binding=gcp_user_access_binding,
        )

    @staticmethod
    def parse_gcp_user_access_binding_path(path: str) -> Dict[str, str]:
        """Parses a gcp_user_access_binding path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/gcpUserAccessBindings/(?P<gcp_user_access_binding>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def service_perimeter_path(
        access_policy: str,
        service_perimeter: str,
    ) -> str:
        """Returns a fully-qualified service_perimeter string."""
        return "accessPolicies/{access_policy}/servicePerimeters/{service_perimeter}".format(
            access_policy=access_policy,
            service_perimeter=service_perimeter,
        )

    @staticmethod
    def parse_service_perimeter_path(path: str) -> Dict[str, str]:
        """Parses a service_perimeter path into its component segments."""
        m = re.match(
            r"^accessPolicies/(?P<access_policy>.+?)/servicePerimeters/(?P<service_perimeter>.+?)$",
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
            _default_universe = AccessContextManagerClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = AccessContextManagerClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = AccessContextManagerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=universe_domain
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
        universe_domain = AccessContextManagerClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """

        # NOTE (b/349488459): universe validation is disabled until further notice.
        return True

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
                AccessContextManagerTransport,
                Callable[..., AccessContextManagerTransport],
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the access context manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,AccessContextManagerTransport,Callable[..., AccessContextManagerTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the AccessContextManagerTransport constructor.
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
        ) = AccessContextManagerClient._read_environment_variables()
        self._client_cert_source = AccessContextManagerClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = AccessContextManagerClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        if CLIENT_LOGGING_SUPPORTED:  # pragma: NO COVER
            # Setup logging.
            client_logging.initialize_logging()

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, AccessContextManagerTransport)
        if transport_provided:
            # transport is a AccessContextManagerTransport instance.
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
            self._transport = cast(AccessContextManagerTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or AccessContextManagerClient._get_api_endpoint(
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
                Type[AccessContextManagerTransport],
                Callable[..., AccessContextManagerTransport],
            ] = (
                AccessContextManagerClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., AccessContextManagerTransport], transport)
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

        if "async" not in str(self._transport):
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                std_logging.DEBUG
            ):  # pragma: NO COVER
                _LOGGER.debug(
                    "Created client `google.identity.accesscontextmanager_v1.AccessContextManagerClient`.",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "universeDomain": getattr(
                            self._transport._credentials, "universe_domain", ""
                        ),
                        "credentialsType": f"{type(self._transport._credentials).__module__}.{type(self._transport._credentials).__qualname__}",
                        "credentialsInfo": getattr(
                            self.transport._credentials, "get_cred_info", lambda: None
                        )(),
                    }
                    if hasattr(self._transport, "_credentials")
                    else {
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "credentialsType": None,
                    },
                )

    def list_access_policies(
        self,
        request: Optional[
            Union[access_context_manager.ListAccessPoliciesRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAccessPoliciesPager:
        r"""Lists all [access policies]
        [google.identity.accesscontextmanager.v1.AccessPolicy] in an
        organization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_list_access_policies():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.ListAccessPoliciesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_access_policies(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.ListAccessPoliciesRequest, dict]):
                The request object. A request to list all ``AccessPolicies`` for a
                container.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.services.access_context_manager.pagers.ListAccessPoliciesPager:
                A response to ListAccessPoliciesRequest.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, access_context_manager.ListAccessPoliciesRequest):
            request = access_context_manager.ListAccessPoliciesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_access_policies]

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
        response = pagers.ListAccessPoliciesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_access_policy(
        self,
        request: Optional[
            Union[access_context_manager.GetAccessPolicyRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> access_policy.AccessPolicy:
        r"""Returns an [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] based on
        the name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_get_access_policy():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.GetAccessPolicyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_access_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.GetAccessPolicyRequest, dict]):
                The request object. A request to get a particular ``AccessPolicy``.
            name (str):
                Required. Resource name for the access policy to get.

                Format ``accessPolicies/{policy_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.types.AccessPolicy:
                AccessPolicy is a container for AccessLevels (which define the necessary
                   attributes to use Google Cloud services) and
                   ServicePerimeters (which define regions of services
                   able to freely pass data within a perimeter). An
                   access policy is globally visible within an
                   organization, and the restrictions it specifies apply
                   to all projects within an organization.

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
        if not isinstance(request, access_context_manager.GetAccessPolicyRequest):
            request = access_context_manager.GetAccessPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_access_policy]

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

    def create_access_policy(
        self,
        request: Optional[Union[access_policy.AccessPolicy, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates an access policy. This method fails if the organization
        already has an access policy. The long-running operation has a
        successful status after the access policy propagates to
        long-lasting storage. Syntactic and basic semantic errors are
        returned in ``metadata`` as a BadRequest proto.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_create_access_policy():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.AccessPolicy(
                )

                # Make the request
                operation = client.create_access_policy(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.AccessPolicy, dict]):
                The request object. ``AccessPolicy`` is a container for ``AccessLevels``
                (which define the necessary attributes to use Google
                Cloud services) and ``ServicePerimeters`` (which define
                regions of services able to freely pass data within a
                perimeter). An access policy is globally visible within
                an organization, and the restrictions it specifies apply
                to all projects within an organization.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.AccessPolicy` AccessPolicy is a container for AccessLevels (which define the necessary
                   attributes to use Google Cloud services) and
                   ServicePerimeters (which define regions of services
                   able to freely pass data within a perimeter). An
                   access policy is globally visible within an
                   organization, and the restrictions it specifies apply
                   to all projects within an organization.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, access_policy.AccessPolicy):
            request = access_policy.AccessPolicy(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_access_policy]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            access_policy.AccessPolicy,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_access_policy(
        self,
        request: Optional[
            Union[access_context_manager.UpdateAccessPolicyRequest, dict]
        ] = None,
        *,
        policy: Optional[access_policy.AccessPolicy] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Updates an [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy]. The
        long-running operation from this RPC has a successful status
        after the changes to the [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] propagate
        to long-lasting storage.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_update_access_policy():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.UpdateAccessPolicyRequest(
                )

                # Make the request
                operation = client.update_access_policy(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.UpdateAccessPolicyRequest, dict]):
                The request object. A request to update an ``AccessPolicy``.
            policy (google.cloud.accesscontextmanager_v1.types.AccessPolicy):
                Required. The updated AccessPolicy.
                This corresponds to the ``policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask to control which
                fields get updated. Must be non-empty.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.AccessPolicy` AccessPolicy is a container for AccessLevels (which define the necessary
                   attributes to use Google Cloud services) and
                   ServicePerimeters (which define regions of services
                   able to freely pass data within a perimeter). An
                   access policy is globally visible within an
                   organization, and the restrictions it specifies apply
                   to all projects within an organization.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([policy, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, access_context_manager.UpdateAccessPolicyRequest):
            request = access_context_manager.UpdateAccessPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if policy is not None:
                request.policy = policy
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_access_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("policy.name", request.policy.name),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            access_policy.AccessPolicy,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_access_policy(
        self,
        request: Optional[
            Union[access_context_manager.DeleteAccessPolicyRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes an [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] based on
        the resource name. The long-running operation has a successful
        status after the [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] is
        removed from long-lasting storage.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_delete_access_policy():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.DeleteAccessPolicyRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_access_policy(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.DeleteAccessPolicyRequest, dict]):
                The request object. A request to delete an ``AccessPolicy``.
            name (str):
                Required. Resource name for the access policy to delete.

                Format ``accessPolicies/{policy_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, access_context_manager.DeleteAccessPolicyRequest):
            request = access_context_manager.DeleteAccessPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_access_policy]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_access_levels(
        self,
        request: Optional[
            Union[access_context_manager.ListAccessLevelsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAccessLevelsPager:
        r"""Lists all [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] for an
        access policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_list_access_levels():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.ListAccessLevelsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_access_levels(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.ListAccessLevelsRequest, dict]):
                The request object. A request to list all ``AccessLevels`` in an
                ``AccessPolicy``.
            parent (str):
                Required. Resource name for the access policy to list
                [Access Levels]
                [google.identity.accesscontextmanager.v1.AccessLevel]
                from.

                Format: ``accessPolicies/{policy_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.services.access_context_manager.pagers.ListAccessLevelsPager:
                A response to ListAccessLevelsRequest.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        if not isinstance(request, access_context_manager.ListAccessLevelsRequest):
            request = access_context_manager.ListAccessLevelsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_access_levels]

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
        response = pagers.ListAccessLevelsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_access_level(
        self,
        request: Optional[
            Union[access_context_manager.GetAccessLevelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> access_level.AccessLevel:
        r"""Gets an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] based on
        the resource name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_get_access_level():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.GetAccessLevelRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_access_level(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.GetAccessLevelRequest, dict]):
                The request object. A request to get a particular ``AccessLevel``.
            name (str):
                Required. Resource name for the [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel].

                Format:
                ``accessPolicies/{policy_id}/accessLevels/{access_level_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.types.AccessLevel:
                An AccessLevel is a label that can be applied to requests to Google Cloud
                   services, along with a list of requirements necessary
                   for the label to be applied.

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
        if not isinstance(request, access_context_manager.GetAccessLevelRequest):
            request = access_context_manager.GetAccessLevelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_access_level]

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

    def create_access_level(
        self,
        request: Optional[
            Union[access_context_manager.CreateAccessLevelRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        access_level: Optional[gia_access_level.AccessLevel] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel]. The
        long-running operation from this RPC has a successful status
        after the [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] propagates
        to long-lasting storage. If [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] contain
        errors, an error response is returned for the first error
        encountered.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_create_access_level():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.CreateAccessLevelRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_access_level(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.CreateAccessLevelRequest, dict]):
                The request object. A request to create an ``AccessLevel``.
            parent (str):
                Required. Resource name for the access policy which owns
                this [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel].

                Format: ``accessPolicies/{policy_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_level (google.cloud.accesscontextmanager_v1.types.AccessLevel):
                Required. The [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel] to
                create. Syntactic correctness of the [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel] is
                a precondition for creation.

                This corresponds to the ``access_level`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.AccessLevel` An AccessLevel is a label that can be applied to requests to Google Cloud
                   services, along with a list of requirements necessary
                   for the label to be applied.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, access_level])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, access_context_manager.CreateAccessLevelRequest):
            request = access_context_manager.CreateAccessLevelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if access_level is not None:
                request.access_level = access_level

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_access_level]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gia_access_level.AccessLevel,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_access_level(
        self,
        request: Optional[
            Union[access_context_manager.UpdateAccessLevelRequest, dict]
        ] = None,
        *,
        access_level: Optional[gia_access_level.AccessLevel] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Updates an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel]. The
        long-running operation from this RPC has a successful status
        after the changes to the [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] propagate
        to long-lasting storage. If [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] contain
        errors, an error response is returned for the first error
        encountered.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_update_access_level():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.UpdateAccessLevelRequest(
                )

                # Make the request
                operation = client.update_access_level(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.UpdateAccessLevelRequest, dict]):
                The request object. A request to update an ``AccessLevel``.
            access_level (google.cloud.accesscontextmanager_v1.types.AccessLevel):
                Required. The updated [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel].
                Syntactic correctness of the [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel] is
                a precondition for creation.

                This corresponds to the ``access_level`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask to control which
                fields get updated. Must be non-empty.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.AccessLevel` An AccessLevel is a label that can be applied to requests to Google Cloud
                   services, along with a list of requirements necessary
                   for the label to be applied.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([access_level, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, access_context_manager.UpdateAccessLevelRequest):
            request = access_context_manager.UpdateAccessLevelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if access_level is not None:
                request.access_level = access_level
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_access_level]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("access_level.name", request.access_level.name),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gia_access_level.AccessLevel,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_access_level(
        self,
        request: Optional[
            Union[access_context_manager.DeleteAccessLevelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] based on
        the resource name. The long-running operation from this RPC has
        a successful status after the [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] has been
        removed from long-lasting storage.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_delete_access_level():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.DeleteAccessLevelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_access_level(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.DeleteAccessLevelRequest, dict]):
                The request object. A request to delete an ``AccessLevel``.
            name (str):
                Required. Resource name for the [Access Level]
                [google.identity.accesscontextmanager.v1.AccessLevel].

                Format:
                ``accessPolicies/{policy_id}/accessLevels/{access_level_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, access_context_manager.DeleteAccessLevelRequest):
            request = access_context_manager.DeleteAccessLevelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_access_level]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def replace_access_levels(
        self,
        request: Optional[
            Union[access_context_manager.ReplaceAccessLevelsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Replaces all existing [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] in an
        [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] with the
        [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] provided.
        This is done atomically. The long-running operation from this
        RPC has a successful status after all replacements propagate to
        long-lasting storage. If the replacement contains errors, an
        error response is returned for the first error encountered. Upon
        error, the replacement is cancelled, and existing [access
        levels] [google.identity.accesscontextmanager.v1.AccessLevel]
        are not affected. The Operation.response field contains
        ReplaceAccessLevelsResponse. Removing [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] contained
        in existing [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        result in an error.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_replace_access_levels():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.ReplaceAccessLevelsRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.replace_access_levels(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.ReplaceAccessLevelsRequest, dict]):
                The request object. A request to replace all existing
                Access Levels in an Access Policy with
                the Access Levels provided. This is done
                atomically.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.ReplaceAccessLevelsResponse` A response to ReplaceAccessLevelsRequest. This will be put inside of
                   Operation.response field.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, access_context_manager.ReplaceAccessLevelsRequest):
            request = access_context_manager.ReplaceAccessLevelsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.replace_access_levels]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            access_context_manager.ReplaceAccessLevelsResponse,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_service_perimeters(
        self,
        request: Optional[
            Union[access_context_manager.ListServicePerimetersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListServicePerimetersPager:
        r"""Lists all [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] for
        an access policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_list_service_perimeters():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.ListServicePerimetersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_service_perimeters(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.ListServicePerimetersRequest, dict]):
                The request object. A request to list all ``ServicePerimeters`` in an
                ``AccessPolicy``.
            parent (str):
                Required. Resource name for the access policy to list
                [Service Perimeters]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                from.

                Format: ``accessPolicies/{policy_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.services.access_context_manager.pagers.ListServicePerimetersPager:
                A response to ListServicePerimetersRequest.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        if not isinstance(request, access_context_manager.ListServicePerimetersRequest):
            request = access_context_manager.ListServicePerimetersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_service_perimeters]

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
        response = pagers.ListServicePerimetersPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_service_perimeter(
        self,
        request: Optional[
            Union[access_context_manager.GetServicePerimeterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> service_perimeter.ServicePerimeter:
        r"""Gets a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] based
        on the resource name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_get_service_perimeter():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.GetServicePerimeterRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_service_perimeter(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.GetServicePerimeterRequest, dict]):
                The request object. A request to get a particular ``ServicePerimeter``.
            name (str):
                Required. Resource name for the [Service Perimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter].

                Format:
                ``accessPolicies/{policy_id}/servicePerimeters/{service_perimeters_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.types.ServicePerimeter:
                ServicePerimeter describes a set of Google Cloud resources which can freely
                   import and export data amongst themselves, but not
                   export outside of the ServicePerimeter. If a request
                   with a source within this ServicePerimeter has a
                   target outside of the ServicePerimeter, the request
                   will be blocked. Otherwise the request is allowed.
                   There are two types of Service Perimeter -Regular and
                   Bridge. Regular Service Perimeters cannot overlap, a
                   single Google Cloud project can only belong to a
                   single regular Service Perimeter. Service Perimeter
                   Bridges can contain only Google Cloud projects as
                   members, a single Google Cloud project may belong to
                   multiple Service Perimeter Bridges.

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
        if not isinstance(request, access_context_manager.GetServicePerimeterRequest):
            request = access_context_manager.GetServicePerimeterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_service_perimeter]

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

    def create_service_perimeter(
        self,
        request: Optional[
            Union[access_context_manager.CreateServicePerimeterRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        service_perimeter: Optional[gia_service_perimeter.ServicePerimeter] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]. The
        long-running operation from this RPC has a successful status
        after the [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        propagates to long-lasting storage. If a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        contains errors, an error response is returned for the first
        error encountered.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_create_service_perimeter():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.CreateServicePerimeterRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_service_perimeter(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.CreateServicePerimeterRequest, dict]):
                The request object. A request to create a ``ServicePerimeter``.
            parent (str):
                Required. Resource name for the access policy which owns
                this [Service Perimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter].

                Format: ``accessPolicies/{policy_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_perimeter (google.cloud.accesscontextmanager_v1.types.ServicePerimeter):
                Required. The [Service Perimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                to create. Syntactic correctness of the [Service
                Perimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                is a precondition for creation.

                This corresponds to the ``service_perimeter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.ServicePerimeter` ServicePerimeter describes a set of Google Cloud resources which can freely
                   import and export data amongst themselves, but not
                   export outside of the ServicePerimeter. If a request
                   with a source within this ServicePerimeter has a
                   target outside of the ServicePerimeter, the request
                   will be blocked. Otherwise the request is allowed.
                   There are two types of Service Perimeter -Regular and
                   Bridge. Regular Service Perimeters cannot overlap, a
                   single Google Cloud project can only belong to a
                   single regular Service Perimeter. Service Perimeter
                   Bridges can contain only Google Cloud projects as
                   members, a single Google Cloud project may belong to
                   multiple Service Perimeter Bridges.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, service_perimeter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, access_context_manager.CreateServicePerimeterRequest
        ):
            request = access_context_manager.CreateServicePerimeterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if service_perimeter is not None:
                request.service_perimeter = service_perimeter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_service_perimeter]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gia_service_perimeter.ServicePerimeter,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_service_perimeter(
        self,
        request: Optional[
            Union[access_context_manager.UpdateServicePerimeterRequest, dict]
        ] = None,
        *,
        service_perimeter: Optional[gia_service_perimeter.ServicePerimeter] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Updates a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]. The
        long-running operation from this RPC has a successful status
        after the [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        propagates to long-lasting storage. If a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        contains errors, an error response is returned for the first
        error encountered.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_update_service_perimeter():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.UpdateServicePerimeterRequest(
                )

                # Make the request
                operation = client.update_service_perimeter(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.UpdateServicePerimeterRequest, dict]):
                The request object. A request to update a ``ServicePerimeter``.
            service_perimeter (google.cloud.accesscontextmanager_v1.types.ServicePerimeter):
                Required. The updated ``ServicePerimeter``. Syntactic
                correctness of the ``ServicePerimeter`` is a
                precondition for creation.

                This corresponds to the ``service_perimeter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask to control which
                fields get updated. Must be non-empty.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.ServicePerimeter` ServicePerimeter describes a set of Google Cloud resources which can freely
                   import and export data amongst themselves, but not
                   export outside of the ServicePerimeter. If a request
                   with a source within this ServicePerimeter has a
                   target outside of the ServicePerimeter, the request
                   will be blocked. Otherwise the request is allowed.
                   There are two types of Service Perimeter -Regular and
                   Bridge. Regular Service Perimeters cannot overlap, a
                   single Google Cloud project can only belong to a
                   single regular Service Perimeter. Service Perimeter
                   Bridges can contain only Google Cloud projects as
                   members, a single Google Cloud project may belong to
                   multiple Service Perimeter Bridges.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_perimeter, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, access_context_manager.UpdateServicePerimeterRequest
        ):
            request = access_context_manager.UpdateServicePerimeterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_perimeter is not None:
                request.service_perimeter = service_perimeter
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_service_perimeter]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("service_perimeter.name", request.service_perimeter.name),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gia_service_perimeter.ServicePerimeter,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_service_perimeter(
        self,
        request: Optional[
            Union[access_context_manager.DeleteServicePerimeterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] based
        on the resource name. The long-running operation from this RPC
        has a successful status after the [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] is
        removed from long-lasting storage.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_delete_service_perimeter():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.DeleteServicePerimeterRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_service_perimeter(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.DeleteServicePerimeterRequest, dict]):
                The request object. A request to delete a ``ServicePerimeter``.
            name (str):
                Required. Resource name for the [Service Perimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter].

                Format:
                ``accessPolicies/{policy_id}/servicePerimeters/{service_perimeter_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
            request, access_context_manager.DeleteServicePerimeterRequest
        ):
            request = access_context_manager.DeleteServicePerimeterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_service_perimeter]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def replace_service_perimeters(
        self,
        request: Optional[
            Union[access_context_manager.ReplaceServicePerimetersRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Replace all existing [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] in an
        [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] with the
        [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        provided. This is done atomically. The long-running operation
        from this RPC has a successful status after all replacements
        propagate to long-lasting storage. Replacements containing
        errors result in an error response for the first error
        encountered. Upon an error, replacement are cancelled and
        existing [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] are
        not affected. The Operation.response field contains
        ReplaceServicePerimetersResponse.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_replace_service_perimeters():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.ReplaceServicePerimetersRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.replace_service_perimeters(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.ReplaceServicePerimetersRequest, dict]):
                The request object. A request to replace all existing
                Service Perimeters in an Access Policy
                with the Service Perimeters provided.
                This is done atomically.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.ReplaceServicePerimetersResponse` A response to ReplaceServicePerimetersRequest. This will be put inside of
                   Operation.response field.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, access_context_manager.ReplaceServicePerimetersRequest
        ):
            request = access_context_manager.ReplaceServicePerimetersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.replace_service_perimeters
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            access_context_manager.ReplaceServicePerimetersResponse,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def commit_service_perimeters(
        self,
        request: Optional[
            Union[access_context_manager.CommitServicePerimetersRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Commits the dry-run specification for all the [service
        perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] in an
        [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy]. A
        commit operation on a service perimeter involves copying its
        ``spec`` field to the ``status`` field of the service perimeter.
        Only [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] with
        ``use_explicit_dry_run_spec`` field set to true are affected by
        a commit operation. The long-running operation from this RPC has
        a successful status after the dry-run specifications for all the
        [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] have
        been committed. If a commit fails, it causes the long-running
        operation to return an error response and the entire commit
        operation is cancelled. When successful, the Operation.response
        field contains CommitServicePerimetersResponse. The ``dry_run``
        and the ``spec`` fields are cleared after a successful commit
        operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_commit_service_perimeters():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.CommitServicePerimetersRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.commit_service_perimeters(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.CommitServicePerimetersRequest, dict]):
                The request object. A request to commit dry-run specs in all [Service
                Perimeters]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                belonging to an [Access
                Policy][google.identity.accesscontextmanager.v1.AccessPolicy].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.CommitServicePerimetersResponse` A response to CommitServicePerimetersRequest. This will be put inside of
                   Operation.response field.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, access_context_manager.CommitServicePerimetersRequest
        ):
            request = access_context_manager.CommitServicePerimetersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.commit_service_perimeters
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            access_context_manager.CommitServicePerimetersResponse,
            metadata_type=access_context_manager.AccessContextManagerOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_gcp_user_access_bindings(
        self,
        request: Optional[
            Union[access_context_manager.ListGcpUserAccessBindingsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListGcpUserAccessBindingsPager:
        r"""Lists all [GcpUserAccessBindings]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
        for a Google Cloud organization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_list_gcp_user_access_bindings():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.ListGcpUserAccessBindingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_gcp_user_access_bindings(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.ListGcpUserAccessBindingsRequest, dict]):
                The request object. Request of [ListGcpUserAccessBindings]
                [google.identity.accesscontextmanager.v1.AccessContextManager.ListGcpUserAccessBindings].
            parent (str):
                Required. Example:
                "organizations/256"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.services.access_context_manager.pagers.ListGcpUserAccessBindingsPager:
                Response of [ListGcpUserAccessBindings]
                   [google.identity.accesscontextmanager.v1.AccessContextManager.ListGcpUserAccessBindings].

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
            request, access_context_manager.ListGcpUserAccessBindingsRequest
        ):
            request = access_context_manager.ListGcpUserAccessBindingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_gcp_user_access_bindings
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
        response = pagers.ListGcpUserAccessBindingsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_gcp_user_access_binding(
        self,
        request: Optional[
            Union[access_context_manager.GetGcpUserAccessBindingRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcp_user_access_binding.GcpUserAccessBinding:
        r"""Gets the [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
        with the given name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_get_gcp_user_access_binding():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.GetGcpUserAccessBindingRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_gcp_user_access_binding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.GetGcpUserAccessBindingRequest, dict]):
                The request object. Request of [GetGcpUserAccessBinding]
                [google.identity.accesscontextmanager.v1.AccessContextManager.GetGcpUserAccessBinding].
            name (str):
                Required. Example:
                "organizations/256/gcpUserAccessBindings/b3-BhcX_Ud5N"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding:
                Restricts access to Cloud Console and
                Google Cloud APIs for a set of users
                using Context-Aware Access.

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
            request, access_context_manager.GetGcpUserAccessBindingRequest
        ):
            request = access_context_manager.GetGcpUserAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_gcp_user_access_binding
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

    def create_gcp_user_access_binding(
        self,
        request: Optional[
            Union[access_context_manager.CreateGcpUserAccessBindingRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        gcp_user_access_binding: Optional[
            gia_gcp_user_access_binding.GcpUserAccessBinding
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates a [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding].
        If the client specifies a [name]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding.name],
        the server ignores it. Fails if a resource already exists with
        the same [group_key]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding.group_key].
        Completion of this long-running operation does not necessarily
        signify that the new binding is deployed onto all affected
        users, which may take more time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_create_gcp_user_access_binding():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                gcp_user_access_binding = accesscontextmanager_v1.GcpUserAccessBinding()
                gcp_user_access_binding.group_key = "group_key_value"
                gcp_user_access_binding.access_levels = ['access_levels_value1', 'access_levels_value2']

                request = accesscontextmanager_v1.CreateGcpUserAccessBindingRequest(
                    parent="parent_value",
                    gcp_user_access_binding=gcp_user_access_binding,
                )

                # Make the request
                operation = client.create_gcp_user_access_binding(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.CreateGcpUserAccessBindingRequest, dict]):
                The request object. Request of [CreateGcpUserAccessBinding]
                [google.identity.accesscontextmanager.v1.AccessContextManager.CreateGcpUserAccessBinding].
            parent (str):
                Required. Example:
                "organizations/256"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            gcp_user_access_binding (google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding):
                Required. [GcpUserAccessBinding]
                [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]

                This corresponds to the ``gcp_user_access_binding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding` Restricts access to Cloud Console and Google Cloud APIs for a set of users
                   using Context-Aware Access.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, gcp_user_access_binding])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, access_context_manager.CreateGcpUserAccessBindingRequest
        ):
            request = access_context_manager.CreateGcpUserAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if gcp_user_access_binding is not None:
                request.gcp_user_access_binding = gcp_user_access_binding

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_gcp_user_access_binding
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gia_gcp_user_access_binding.GcpUserAccessBinding,
            metadata_type=access_context_manager.GcpUserAccessBindingOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_gcp_user_access_binding(
        self,
        request: Optional[
            Union[access_context_manager.UpdateGcpUserAccessBindingRequest, dict]
        ] = None,
        *,
        gcp_user_access_binding: Optional[
            gia_gcp_user_access_binding.GcpUserAccessBinding
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Updates a [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding].
        Completion of this long-running operation does not necessarily
        signify that the changed binding is deployed onto all affected
        users, which may take more time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_update_gcp_user_access_binding():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                gcp_user_access_binding = accesscontextmanager_v1.GcpUserAccessBinding()
                gcp_user_access_binding.group_key = "group_key_value"
                gcp_user_access_binding.access_levels = ['access_levels_value1', 'access_levels_value2']

                request = accesscontextmanager_v1.UpdateGcpUserAccessBindingRequest(
                    gcp_user_access_binding=gcp_user_access_binding,
                )

                # Make the request
                operation = client.update_gcp_user_access_binding(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.UpdateGcpUserAccessBindingRequest, dict]):
                The request object. Request of [UpdateGcpUserAccessBinding]
                [google.identity.accesscontextmanager.v1.AccessContextManager.UpdateGcpUserAccessBinding].
            gcp_user_access_binding (google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding):
                Required. [GcpUserAccessBinding]
                [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]

                This corresponds to the ``gcp_user_access_binding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Only the fields specified in this mask are
                updated. Because name and group_key cannot be changed,
                update_mask is required and must always be:

                update_mask { paths: "access_levels" }

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding` Restricts access to Cloud Console and Google Cloud APIs for a set of users
                   using Context-Aware Access.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([gcp_user_access_binding, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, access_context_manager.UpdateGcpUserAccessBindingRequest
        ):
            request = access_context_manager.UpdateGcpUserAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if gcp_user_access_binding is not None:
                request.gcp_user_access_binding = gcp_user_access_binding
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_gcp_user_access_binding
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "gcp_user_access_binding.name",
                        request.gcp_user_access_binding.name,
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gia_gcp_user_access_binding.GcpUserAccessBinding,
            metadata_type=access_context_manager.GcpUserAccessBindingOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_gcp_user_access_binding(
        self,
        request: Optional[
            Union[access_context_manager.DeleteGcpUserAccessBindingRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes a [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding].
        Completion of this long-running operation does not necessarily
        signify that the binding deletion is deployed onto all affected
        users, which may take more time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1

            def sample_delete_gcp_user_access_binding():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = accesscontextmanager_v1.DeleteGcpUserAccessBindingRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_gcp_user_access_binding(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.accesscontextmanager_v1.types.DeleteGcpUserAccessBindingRequest, dict]):
                The request object. Request of [DeleteGcpUserAccessBinding]
                [google.identity.accesscontextmanager.v1.AccessContextManager.DeleteGcpUserAccessBinding].
            name (str):
                Required. Example:
                "organizations/256/gcpUserAccessBindings/b3-BhcX_Ud5N"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
            request, access_context_manager.DeleteGcpUserAccessBindingRequest
        ):
            request = access_context_manager.DeleteGcpUserAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_gcp_user_access_binding
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=access_context_manager.GcpUserAccessBindingOperationMetadata,
        )

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM policy for the specified Access Context Manager
        [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy].
        This method replaces the existing IAM policy on the access
        policy. The IAM policy controls the set of users who can perform
        specific operations on the Access Context Manager [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for ``SetIamPolicy`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   :literal:`\`     {       "bindings": [         {           "role": "roles/resourcemanager.organizationAdmin",           "members": [             "user:mike@example.com",             "group:admins@example.com",             "domain:google.com",             "serviceAccount:my-project-id@appspot.gserviceaccount.com"           ]         },         {           "role": "roles/resourcemanager.organizationViewer",           "members": [             "user:eve@example.com"           ],           "condition": {             "title": "expirable access",             "description": "Does not grant access after Sep 2020",             "expression": "request.time <             timestamp('2020-10-01T00:00:00.000Z')",           }         }       ],       "etag": "BwWWja0YfJA=",       "version": 3     }`\ \`

                   **YAML example:**

                   :literal:`\`     bindings:     - members:       - user:mike@example.com       - group:admins@example.com       - domain:google.com       - serviceAccount:my-project-id@appspot.gserviceaccount.com       role: roles/resourcemanager.organizationAdmin     - members:       - user:eve@example.com       role: roles/resourcemanager.organizationViewer       condition:         title: expirable access         description: Does not grant access after Sep 2020         expression: request.time < timestamp('2020-10-01T00:00:00.000Z')     etag: BwWWja0YfJA=     version: 3`\ \`

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        if isinstance(request, dict):
            # - The request isn't a proto-plus wrapped type,
            #   so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    def get_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.GetIamPolicyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM policy for the specified Access Context Manager
        [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for ``GetIamPolicy`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   :literal:`\`     {       "bindings": [         {           "role": "roles/resourcemanager.organizationAdmin",           "members": [             "user:mike@example.com",             "group:admins@example.com",             "domain:google.com",             "serviceAccount:my-project-id@appspot.gserviceaccount.com"           ]         },         {           "role": "roles/resourcemanager.organizationViewer",           "members": [             "user:eve@example.com"           ],           "condition": {             "title": "expirable access",             "description": "Does not grant access after Sep 2020",             "expression": "request.time <             timestamp('2020-10-01T00:00:00.000Z')",           }         }       ],       "etag": "BwWWja0YfJA=",       "version": 3     }`\ \`

                   **YAML example:**

                   :literal:`\`     bindings:     - members:       - user:mike@example.com       - group:admins@example.com       - domain:google.com       - serviceAccount:my-project-id@appspot.gserviceaccount.com       role: roles/resourcemanager.organizationAdmin     - members:       - user:eve@example.com       role: roles/resourcemanager.organizationViewer       condition:         title: expirable access         description: Does not grant access after Sep 2020         expression: request.time < timestamp('2020-10-01T00:00:00.000Z')     etag: BwWWja0YfJA=     version: 3`\ \`

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        if isinstance(request, dict):
            # - The request isn't a proto-plus wrapped type,
            #   so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    def test_iam_permissions(
        self,
        request: Optional[Union[iam_policy_pb2.TestIamPermissionsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns the IAM permissions that the caller has on the specified
        Access Context Manager resource. The resource can be an
        [AccessPolicy][google.identity.accesscontextmanager.v1.AccessPolicy],
        [AccessLevel][google.identity.accesscontextmanager.v1.AccessLevel],
        or
        [ServicePerimeter][google.identity.accesscontextmanager.v1.ServicePerimeter
        ]. This method does not support other resources.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import accesscontextmanager_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = accesscontextmanager_v1.AccessContextManagerClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for ``TestIamPermissions`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        if isinstance(request, dict):
            # - The request isn't a proto-plus wrapped type,
            #   so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    def __enter__(self) -> "AccessContextManagerClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_operation]

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


__all__ = ("AccessContextManagerClient",)
