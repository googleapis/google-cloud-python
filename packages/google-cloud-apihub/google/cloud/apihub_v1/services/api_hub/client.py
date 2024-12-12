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

from google.cloud.apihub_v1 import gapic_version as package_version

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

from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.apihub_v1.services.api_hub import pagers
from google.cloud.apihub_v1.types import apihub_service, common_fields

from .transports.base import DEFAULT_CLIENT_INFO, ApiHubTransport
from .transports.rest import ApiHubRestTransport


class ApiHubClientMeta(type):
    """Metaclass for the ApiHub client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[ApiHubTransport]]
    _transport_registry["rest"] = ApiHubRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ApiHubTransport]:
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


class ApiHubClient(metaclass=ApiHubClientMeta):
    """This service provides all methods related to the API hub."""

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
    DEFAULT_ENDPOINT = "apihub.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "apihub.{UNIVERSE_DOMAIN}"
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
            ApiHubClient: The constructed client.
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
            ApiHubClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ApiHubTransport:
        """Returns the transport used by the client instance.

        Returns:
            ApiHubTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def api_path(
        project: str,
        location: str,
        api: str,
    ) -> str:
        """Returns a fully-qualified api string."""
        return "projects/{project}/locations/{location}/apis/{api}".format(
            project=project,
            location=location,
            api=api,
        )

    @staticmethod
    def parse_api_path(path: str) -> Dict[str, str]:
        """Parses a api path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/apis/(?P<api>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def api_operation_path(
        project: str,
        location: str,
        api: str,
        version: str,
        operation: str,
    ) -> str:
        """Returns a fully-qualified api_operation string."""
        return "projects/{project}/locations/{location}/apis/{api}/versions/{version}/operations/{operation}".format(
            project=project,
            location=location,
            api=api,
            version=version,
            operation=operation,
        )

    @staticmethod
    def parse_api_operation_path(path: str) -> Dict[str, str]:
        """Parses a api_operation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/apis/(?P<api>.+?)/versions/(?P<version>.+?)/operations/(?P<operation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def attribute_path(
        project: str,
        location: str,
        attribute: str,
    ) -> str:
        """Returns a fully-qualified attribute string."""
        return "projects/{project}/locations/{location}/attributes/{attribute}".format(
            project=project,
            location=location,
            attribute=attribute,
        )

    @staticmethod
    def parse_attribute_path(path: str) -> Dict[str, str]:
        """Parses a attribute path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/attributes/(?P<attribute>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def definition_path(
        project: str,
        location: str,
        api: str,
        version: str,
        definition: str,
    ) -> str:
        """Returns a fully-qualified definition string."""
        return "projects/{project}/locations/{location}/apis/{api}/versions/{version}/definitions/{definition}".format(
            project=project,
            location=location,
            api=api,
            version=version,
            definition=definition,
        )

    @staticmethod
    def parse_definition_path(path: str) -> Dict[str, str]:
        """Parses a definition path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/apis/(?P<api>.+?)/versions/(?P<version>.+?)/definitions/(?P<definition>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def deployment_path(
        project: str,
        location: str,
        deployment: str,
    ) -> str:
        """Returns a fully-qualified deployment string."""
        return (
            "projects/{project}/locations/{location}/deployments/{deployment}".format(
                project=project,
                location=location,
                deployment=deployment,
            )
        )

    @staticmethod
    def parse_deployment_path(path: str) -> Dict[str, str]:
        """Parses a deployment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/deployments/(?P<deployment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def external_api_path(
        project: str,
        location: str,
        external_api: str,
    ) -> str:
        """Returns a fully-qualified external_api string."""
        return "projects/{project}/locations/{location}/externalApis/{external_api}".format(
            project=project,
            location=location,
            external_api=external_api,
        )

    @staticmethod
    def parse_external_api_path(path: str) -> Dict[str, str]:
        """Parses a external_api path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/externalApis/(?P<external_api>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def spec_path(
        project: str,
        location: str,
        api: str,
        version: str,
        spec: str,
    ) -> str:
        """Returns a fully-qualified spec string."""
        return "projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}".format(
            project=project,
            location=location,
            api=api,
            version=version,
            spec=spec,
        )

    @staticmethod
    def parse_spec_path(path: str) -> Dict[str, str]:
        """Parses a spec path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/apis/(?P<api>.+?)/versions/(?P<version>.+?)/specs/(?P<spec>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def version_path(
        project: str,
        location: str,
        api: str,
        version: str,
    ) -> str:
        """Returns a fully-qualified version string."""
        return "projects/{project}/locations/{location}/apis/{api}/versions/{version}".format(
            project=project,
            location=location,
            api=api,
            version=version,
        )

    @staticmethod
    def parse_version_path(path: str) -> Dict[str, str]:
        """Parses a version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/apis/(?P<api>.+?)/versions/(?P<version>.+?)$",
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
            _default_universe = ApiHubClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = ApiHubClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = ApiHubClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = ApiHubClient._DEFAULT_UNIVERSE
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
            Union[str, ApiHubTransport, Callable[..., ApiHubTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the api hub client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ApiHubTransport,Callable[..., ApiHubTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ApiHubTransport constructor.
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
        ) = ApiHubClient._read_environment_variables()
        self._client_cert_source = ApiHubClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = ApiHubClient._get_universe_domain(
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
        transport_provided = isinstance(transport, ApiHubTransport)
        if transport_provided:
            # transport is a ApiHubTransport instance.
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
            self._transport = cast(ApiHubTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or ApiHubClient._get_api_endpoint(
            self._client_options.api_endpoint,
            self._client_cert_source,
            self._universe_domain,
            self._use_mtls_endpoint,
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
                Type[ApiHubTransport], Callable[..., ApiHubTransport]
            ] = (
                ApiHubClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., ApiHubTransport], transport)
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
                    "Created client `google.cloud.apihub_v1.ApiHubClient`.",
                    extra={
                        "serviceName": "google.cloud.apihub.v1.ApiHub",
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
                        "serviceName": "google.cloud.apihub.v1.ApiHub",
                        "credentialsType": None,
                    },
                )

    def create_api(
        self,
        request: Optional[Union[apihub_service.CreateApiRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        api: Optional[common_fields.Api] = None,
        api_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Api:
        r"""Create an API resource in the API hub.
        Once an API resource is created, versions can be added
        to it.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_create_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                api = apihub_v1.Api()
                api.display_name = "display_name_value"

                request = apihub_v1.CreateApiRequest(
                    parent="parent_value",
                    api=api,
                )

                # Make the request
                response = client.create_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.CreateApiRequest, dict]):
                The request object. The [CreateApi][google.cloud.apihub.v1.ApiHub.CreateApi]
                method's request.
            parent (str):
                Required. The parent resource for the API resource.
                Format: ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api (google.cloud.apihub_v1.types.Api):
                Required. The API resource to create.
                This corresponds to the ``api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_id (str):
                Optional. The ID to use for the API resource, which will
                become the final component of the API's resource name.
                This field is optional.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another API resource in the API hub.
                -  If not provided, a system generated id will be used.

                This value should be 4-500 characters, and valid
                characters are /[a-z][A-Z][0-9]-_/.

                This corresponds to the ``api_id`` field
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
            google.cloud.apihub_v1.types.Api:
                An API resource in the API Hub.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api, api_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.CreateApiRequest):
            request = apihub_service.CreateApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if api is not None:
                request.api = api
            if api_id is not None:
                request.api_id = api_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_api]

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

    def get_api(
        self,
        request: Optional[Union[apihub_service.GetApiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Api:
        r"""Get API resource details including the API versions
        contained in it.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetApiRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetApiRequest, dict]):
                The request object. The [GetApi][google.cloud.apihub.v1.ApiHub.GetApi]
                method's request.
            name (str):
                Required. The name of the API resource to retrieve.
                Format:
                ``projects/{project}/locations/{location}/apis/{api}``

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
            google.cloud.apihub_v1.types.Api:
                An API resource in the API Hub.
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
        if not isinstance(request, apihub_service.GetApiRequest):
            request = apihub_service.GetApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_api]

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

    def list_apis(
        self,
        request: Optional[Union[apihub_service.ListApisRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListApisPager:
        r"""List API resources in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_apis():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListApisRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_apis(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListApisRequest, dict]):
                The request object. The [ListApis][google.cloud.apihub.v1.ApiHub.ListApis]
                method's request.
            parent (str):
                Required. The parent, which owns this collection of API
                resources. Format:
                ``projects/{project}/locations/{location}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListApisPager:
                The [ListApis][google.cloud.apihub.v1.ApiHub.ListApis]
                method's response.

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
        if not isinstance(request, apihub_service.ListApisRequest):
            request = apihub_service.ListApisRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_apis]

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
        response = pagers.ListApisPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_api(
        self,
        request: Optional[Union[apihub_service.UpdateApiRequest, dict]] = None,
        *,
        api: Optional[common_fields.Api] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Api:
        r"""Update an API resource in the API hub. The following fields in
        the [API][] can be updated:

        -  [display_name][google.cloud.apihub.v1.Api.display_name]
        -  [description][google.cloud.apihub.v1.Api.description]
        -  [owner][google.cloud.apihub.v1.Api.owner]
        -  [documentation][google.cloud.apihub.v1.Api.documentation]
        -  [target_user][google.cloud.apihub.v1.Api.target_user]
        -  [team][google.cloud.apihub.v1.Api.team]
        -  [business_unit][google.cloud.apihub.v1.Api.business_unit]
        -  [maturity_level][google.cloud.apihub.v1.Api.maturity_level]
        -  [attributes][google.cloud.apihub.v1.Api.attributes]

        The
        [update_mask][google.cloud.apihub.v1.UpdateApiRequest.update_mask]
        should be used to specify the fields being updated.

        Updating the owner field requires complete owner message and
        updates both owner and email fields.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_update_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                api = apihub_v1.Api()
                api.display_name = "display_name_value"

                request = apihub_v1.UpdateApiRequest(
                    api=api,
                )

                # Make the request
                response = client.update_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.UpdateApiRequest, dict]):
                The request object. The [UpdateApi][google.cloud.apihub.v1.ApiHub.UpdateApi]
                method's request.
            api (google.cloud.apihub_v1.types.Api):
                Required. The API resource to update.

                The API resource's ``name`` field is used to identify
                the API resource to update. Format:
                ``projects/{project}/locations/{location}/apis/{api}``

                This corresponds to the ``api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

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
            google.cloud.apihub_v1.types.Api:
                An API resource in the API Hub.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([api, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.UpdateApiRequest):
            request = apihub_service.UpdateApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if api is not None:
                request.api = api
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_api]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("api.name", request.api.name),)),
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

    def delete_api(
        self,
        request: Optional[Union[apihub_service.DeleteApiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete an API resource in the API hub. API can only
        be deleted if all underlying versions are deleted.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_delete_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.DeleteApiRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_api(request=request)

        Args:
            request (Union[google.cloud.apihub_v1.types.DeleteApiRequest, dict]):
                The request object. The [DeleteApi][google.cloud.apihub.v1.ApiHub.DeleteApi]
                method's request.
            name (str):
                Required. The name of the API resource to delete.
                Format:
                ``projects/{project}/locations/{location}/apis/{api}``

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
        if not isinstance(request, apihub_service.DeleteApiRequest):
            request = apihub_service.DeleteApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_api]

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

    def create_version(
        self,
        request: Optional[Union[apihub_service.CreateVersionRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        version: Optional[common_fields.Version] = None,
        version_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Version:
        r"""Create an API version for an API resource in the API
        hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_create_version():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                version = apihub_v1.Version()
                version.display_name = "display_name_value"

                request = apihub_v1.CreateVersionRequest(
                    parent="parent_value",
                    version=version,
                )

                # Make the request
                response = client.create_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.CreateVersionRequest, dict]):
                The request object. The
                [CreateVersion][google.cloud.apihub.v1.ApiHub.CreateVersion]
                method's request.
            parent (str):
                Required. The parent resource for API version. Format:
                ``projects/{project}/locations/{location}/apis/{api}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            version (google.cloud.apihub_v1.types.Version):
                Required. The version to create.
                This corresponds to the ``version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            version_id (str):
                Optional. The ID to use for the API version, which will
                become the final component of the version's resource
                name. This field is optional.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another version in the API resource.
                -  If not provided, a system generated id will be used.

                This value should be 4-500 characters, and valid
                characters are /[a-z][A-Z][0-9]-_/.

                This corresponds to the ``version_id`` field
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
            google.cloud.apihub_v1.types.Version:
                Represents a version of the API
                resource in API hub. This is also
                referred to as the API version.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, version, version_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.CreateVersionRequest):
            request = apihub_service.CreateVersionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if version is not None:
                request.version = version
            if version_id is not None:
                request.version_id = version_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_version]

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

    def get_version(
        self,
        request: Optional[Union[apihub_service.GetVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Version:
        r"""Get details about the API version of an API resource.
        This will include information about the specs and
        operations present in the API version as well as the
        deployments linked to it.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_version():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetVersionRequest, dict]):
                The request object. The
                [GetVersion][google.cloud.apihub.v1.ApiHub.GetVersion]
                method's request.
            name (str):
                Required. The name of the API version to retrieve.
                Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``

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
            google.cloud.apihub_v1.types.Version:
                Represents a version of the API
                resource in API hub. This is also
                referred to as the API version.

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
        if not isinstance(request, apihub_service.GetVersionRequest):
            request = apihub_service.GetVersionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_version]

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

    def list_versions(
        self,
        request: Optional[Union[apihub_service.ListVersionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListVersionsPager:
        r"""List API versions of an API resource in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_versions():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListVersionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_versions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListVersionsRequest, dict]):
                The request object. The
                [ListVersions][google.cloud.apihub.v1.ApiHub.ListVersions]
                method's request.
            parent (str):
                Required. The parent which owns this collection of API
                versions i.e., the API resource Format:
                ``projects/{project}/locations/{location}/apis/{api}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListVersionsPager:
                The [ListVersions][google.cloud.apihub.v1.ApiHub.ListVersions] method's
                   response.

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
        if not isinstance(request, apihub_service.ListVersionsRequest):
            request = apihub_service.ListVersionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_versions]

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
        response = pagers.ListVersionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_version(
        self,
        request: Optional[Union[apihub_service.UpdateVersionRequest, dict]] = None,
        *,
        version: Optional[common_fields.Version] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Version:
        r"""Update API version. The following fields in the
        [version][google.cloud.apihub.v1.Version] can be updated
        currently:

        -  [display_name][google.cloud.apihub.v1.Version.display_name]
        -  [description][google.cloud.apihub.v1.Version.description]
        -  [documentation][google.cloud.apihub.v1.Version.documentation]
        -  [deployments][google.cloud.apihub.v1.Version.deployments]
        -  [lifecycle][google.cloud.apihub.v1.Version.lifecycle]
        -  [compliance][google.cloud.apihub.v1.Version.compliance]
        -  [accreditation][google.cloud.apihub.v1.Version.accreditation]
        -  [attributes][google.cloud.apihub.v1.Version.attributes]

        The
        [update_mask][google.cloud.apihub.v1.UpdateVersionRequest.update_mask]
        should be used to specify the fields being updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_update_version():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                version = apihub_v1.Version()
                version.display_name = "display_name_value"

                request = apihub_v1.UpdateVersionRequest(
                    version=version,
                )

                # Make the request
                response = client.update_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.UpdateVersionRequest, dict]):
                The request object. The
                [UpdateVersion][google.cloud.apihub.v1.ApiHub.UpdateVersion]
                method's request.
            version (google.cloud.apihub_v1.types.Version):
                Required. The API version to update.

                The version's ``name`` field is used to identify the API
                version to update. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``

                This corresponds to the ``version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

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
            google.cloud.apihub_v1.types.Version:
                Represents a version of the API
                resource in API hub. This is also
                referred to as the API version.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([version, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.UpdateVersionRequest):
            request = apihub_service.UpdateVersionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if version is not None:
                request.version = version
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_version]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("version.name", request.version.name),)
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

    def delete_version(
        self,
        request: Optional[Union[apihub_service.DeleteVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete an API version. Version can only be deleted if
        all underlying specs, operations, definitions and linked
        deployments are deleted.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_delete_version():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.DeleteVersionRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_version(request=request)

        Args:
            request (Union[google.cloud.apihub_v1.types.DeleteVersionRequest, dict]):
                The request object. The
                [DeleteVersion][google.cloud.apihub.v1.ApiHub.DeleteVersion]
                method's request.
            name (str):
                Required. The name of the version to delete. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``

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
        if not isinstance(request, apihub_service.DeleteVersionRequest):
            request = apihub_service.DeleteVersionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_version]

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

    def create_spec(
        self,
        request: Optional[Union[apihub_service.CreateSpecRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        spec: Optional[common_fields.Spec] = None,
        spec_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Spec:
        r"""Add a spec to an API version in the API hub. Multiple specs can
        be added to an API version. Note, while adding a spec, at least
        one of ``contents`` or ``source_uri`` must be provided. If
        ``contents`` is provided, then ``spec_type`` must also be
        provided.

        On adding a spec with contents to the version, the operations
        present in it will be added to the version.Note that the file
        contents in the spec should be of the same type as defined in
        the
        ``projects/{project}/locations/{location}/attributes/system-spec-type``
        attribute associated with spec resource. Note that specs of
        various types can be uploaded, however parsing of details is
        supported for OpenAPI spec currently.

        In order to access the information parsed from the spec, use the
        [GetSpec][google.cloud.apihub.v1.ApiHub.GetSpec] method. In
        order to access the raw contents for a particular spec, use the
        [GetSpecContents][google.cloud.apihub.v1.ApiHub.GetSpecContents]
        method. In order to access the operations parsed from the spec,
        use the
        [ListAPIOperations][google.cloud.apihub.v1.ApiHub.ListApiOperations]
        method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_create_spec():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                spec = apihub_v1.Spec()
                spec.display_name = "display_name_value"
                spec.spec_type.enum_values.values.id = "id_value"
                spec.spec_type.enum_values.values.display_name = "display_name_value"

                request = apihub_v1.CreateSpecRequest(
                    parent="parent_value",
                    spec=spec,
                )

                # Make the request
                response = client.create_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.CreateSpecRequest, dict]):
                The request object. The
                [CreateSpec][google.cloud.apihub.v1.ApiHub.CreateSpec]
                method's request.
            parent (str):
                Required. The parent resource for Spec. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            spec (google.cloud.apihub_v1.types.Spec):
                Required. The spec to create.
                This corresponds to the ``spec`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            spec_id (str):
                Optional. The ID to use for the spec, which will become
                the final component of the spec's resource name. This
                field is optional.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another spec in the API resource.
                -  If not provided, a system generated id will be used.

                This value should be 4-500 characters, and valid
                characters are /[a-z][A-Z][0-9]-_/.

                This corresponds to the ``spec_id`` field
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
            google.cloud.apihub_v1.types.Spec:
                Represents a spec associated with an
                API version in the API Hub. Note that
                specs of various types can be uploaded,
                however parsing of details is supported
                for OpenAPI spec currently.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, spec, spec_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.CreateSpecRequest):
            request = apihub_service.CreateSpecRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if spec is not None:
                request.spec = spec
            if spec_id is not None:
                request.spec_id = spec_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_spec]

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

    def get_spec(
        self,
        request: Optional[Union[apihub_service.GetSpecRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Spec:
        r"""Get details about the information parsed from a spec. Note that
        this method does not return the raw spec contents. Use
        [GetSpecContents][google.cloud.apihub.v1.ApiHub.GetSpecContents]
        method to retrieve the same.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_spec():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetSpecRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetSpecRequest, dict]):
                The request object. The [GetSpec][google.cloud.apihub.v1.ApiHub.GetSpec]
                method's request.
            name (str):
                Required. The name of the spec to retrieve. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``

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
            google.cloud.apihub_v1.types.Spec:
                Represents a spec associated with an
                API version in the API Hub. Note that
                specs of various types can be uploaded,
                however parsing of details is supported
                for OpenAPI spec currently.

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
        if not isinstance(request, apihub_service.GetSpecRequest):
            request = apihub_service.GetSpecRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_spec]

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

    def get_spec_contents(
        self,
        request: Optional[Union[apihub_service.GetSpecContentsRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.SpecContents:
        r"""Get spec contents.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_spec_contents():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetSpecContentsRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_spec_contents(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetSpecContentsRequest, dict]):
                The request object. The
                [GetSpecContents][google.cloud.apihub.v1.ApiHub.GetSpecContents]
                method's request.
            name (str):
                Required. The name of the spec whose contents need to be
                retrieved. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``

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
            google.cloud.apihub_v1.types.SpecContents:
                The spec contents.
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
        if not isinstance(request, apihub_service.GetSpecContentsRequest):
            request = apihub_service.GetSpecContentsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_spec_contents]

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

    def list_specs(
        self,
        request: Optional[Union[apihub_service.ListSpecsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListSpecsPager:
        r"""List specs corresponding to a particular API
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_specs():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListSpecsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_specs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListSpecsRequest, dict]):
                The request object. The [ListSpecs][ListSpecs] method's request.
            parent (str):
                Required. The parent, which owns this collection of
                specs. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListSpecsPager:
                The [ListSpecs][google.cloud.apihub.v1.ApiHub.ListSpecs]
                method's response.

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
        if not isinstance(request, apihub_service.ListSpecsRequest):
            request = apihub_service.ListSpecsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_specs]

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
        response = pagers.ListSpecsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_spec(
        self,
        request: Optional[Union[apihub_service.UpdateSpecRequest, dict]] = None,
        *,
        spec: Optional[common_fields.Spec] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Spec:
        r"""Update spec. The following fields in the
        [spec][google.cloud.apihub.v1.Spec] can be updated:

        -  [display_name][google.cloud.apihub.v1.Spec.display_name]
        -  [source_uri][google.cloud.apihub.v1.Spec.source_uri]
        -  [lint_response][google.cloud.apihub.v1.Spec.lint_response]
        -  [attributes][google.cloud.apihub.v1.Spec.attributes]
        -  [contents][google.cloud.apihub.v1.Spec.contents]
        -  [spec_type][google.cloud.apihub.v1.Spec.spec_type]

        In case of an OAS spec, updating spec contents can lead to:

        1. Creation, deletion and update of operations.
        2. Creation, deletion and update of definitions.
        3. Update of other info parsed out from the new spec.

        In case of contents or source_uri being present in update mask,
        spec_type must also be present. Also, spec_type can not be
        present in update mask if contents or source_uri is not present.

        The
        [update_mask][google.cloud.apihub.v1.UpdateSpecRequest.update_mask]
        should be used to specify the fields being updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_update_spec():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                spec = apihub_v1.Spec()
                spec.display_name = "display_name_value"
                spec.spec_type.enum_values.values.id = "id_value"
                spec.spec_type.enum_values.values.display_name = "display_name_value"

                request = apihub_v1.UpdateSpecRequest(
                    spec=spec,
                )

                # Make the request
                response = client.update_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.UpdateSpecRequest, dict]):
                The request object. The
                [UpdateSpec][google.cloud.apihub.v1.ApiHub.UpdateSpec]
                method's request.
            spec (google.cloud.apihub_v1.types.Spec):
                Required. The spec to update.

                The spec's ``name`` field is used to identify the spec
                to update. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``

                This corresponds to the ``spec`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

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
            google.cloud.apihub_v1.types.Spec:
                Represents a spec associated with an
                API version in the API Hub. Note that
                specs of various types can be uploaded,
                however parsing of details is supported
                for OpenAPI spec currently.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([spec, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.UpdateSpecRequest):
            request = apihub_service.UpdateSpecRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if spec is not None:
                request.spec = spec
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_spec]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("spec.name", request.spec.name),)
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

    def delete_spec(
        self,
        request: Optional[Union[apihub_service.DeleteSpecRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a spec.
        Deleting a spec will also delete the associated
        operations from the version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_delete_spec():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.DeleteSpecRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_spec(request=request)

        Args:
            request (Union[google.cloud.apihub_v1.types.DeleteSpecRequest, dict]):
                The request object. The
                [DeleteSpec][google.cloud.apihub.v1.ApiHub.DeleteSpec]
                method's request.
            name (str):
                Required. The name of the spec to delete. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``

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
        if not isinstance(request, apihub_service.DeleteSpecRequest):
            request = apihub_service.DeleteSpecRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_spec]

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

    def get_api_operation(
        self,
        request: Optional[Union[apihub_service.GetApiOperationRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.ApiOperation:
        r"""Get details about a particular operation in API
        version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_api_operation():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetApiOperationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_api_operation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetApiOperationRequest, dict]):
                The request object. The
                [GetApiOperation][google.cloud.apihub.v1.ApiHub.GetApiOperation]
                method's request.
            name (str):
                Required. The name of the operation to retrieve. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/operations/{operation}``

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
            google.cloud.apihub_v1.types.ApiOperation:
                Represents an operation contained in
                an API version in the API Hub. An
                operation is added/updated/deleted in an
                API version when a new spec is added or
                an existing spec is updated/deleted in a
                version. Currently, an operation will be
                created only corresponding to OpenAPI
                spec as parsing is supported for OpenAPI
                spec.

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
        if not isinstance(request, apihub_service.GetApiOperationRequest):
            request = apihub_service.GetApiOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_api_operation]

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

    def list_api_operations(
        self,
        request: Optional[Union[apihub_service.ListApiOperationsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListApiOperationsPager:
        r"""List operations in an API version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_api_operations():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListApiOperationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_api_operations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListApiOperationsRequest, dict]):
                The request object. The
                [ListApiOperations][google.cloud.apihub.v1.ApiHub.ListApiOperations]
                method's request.
            parent (str):
                Required. The parent which owns this collection of
                operations i.e., the API version. Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListApiOperationsPager:
                The [ListApiOperations][google.cloud.apihub.v1.ApiHub.ListApiOperations]
                   method's response.

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
        if not isinstance(request, apihub_service.ListApiOperationsRequest):
            request = apihub_service.ListApiOperationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_api_operations]

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
        response = pagers.ListApiOperationsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_definition(
        self,
        request: Optional[Union[apihub_service.GetDefinitionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Definition:
        r"""Get details about a definition in an API version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_definition():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetDefinitionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_definition(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetDefinitionRequest, dict]):
                The request object. The
                [GetDefinition][google.cloud.apihub.v1.ApiHub.GetDefinition]
                method's request.
            name (str):
                Required. The name of the definition to retrieve.
                Format:
                ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/definitions/{definition}``

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
            google.cloud.apihub_v1.types.Definition:
                Represents a definition for example schema, request, response definitions
                   contained in an API version. A definition is
                   added/updated/deleted in an API version when a new
                   spec is added or an existing spec is updated/deleted
                   in a version. Currently, definition will be created
                   only corresponding to OpenAPI spec as parsing is
                   supported for OpenAPI spec. Also, within OpenAPI
                   spec, only schema object is supported.

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
        if not isinstance(request, apihub_service.GetDefinitionRequest):
            request = apihub_service.GetDefinitionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_definition]

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

    def create_deployment(
        self,
        request: Optional[Union[apihub_service.CreateDeploymentRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        deployment: Optional[common_fields.Deployment] = None,
        deployment_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Deployment:
        r"""Create a deployment resource in the API hub.
        Once a deployment resource is created, it can be
        associated with API versions.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_create_deployment():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                deployment = apihub_v1.Deployment()
                deployment.display_name = "display_name_value"
                deployment.deployment_type.enum_values.values.id = "id_value"
                deployment.deployment_type.enum_values.values.display_name = "display_name_value"
                deployment.resource_uri = "resource_uri_value"
                deployment.endpoints = ['endpoints_value1', 'endpoints_value2']

                request = apihub_v1.CreateDeploymentRequest(
                    parent="parent_value",
                    deployment=deployment,
                )

                # Make the request
                response = client.create_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.CreateDeploymentRequest, dict]):
                The request object. The
                [CreateDeployment][google.cloud.apihub.v1.ApiHub.CreateDeployment]
                method's request.
            parent (str):
                Required. The parent resource for the deployment
                resource. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            deployment (google.cloud.apihub_v1.types.Deployment):
                Required. The deployment resource to
                create.

                This corresponds to the ``deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            deployment_id (str):
                Optional. The ID to use for the deployment resource,
                which will become the final component of the
                deployment's resource name. This field is optional.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another deployment resource in the API hub.
                -  If not provided, a system generated id will be used.

                This value should be 4-500 characters, and valid
                characters are /[a-z][A-Z][0-9]-_/.

                This corresponds to the ``deployment_id`` field
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
            google.cloud.apihub_v1.types.Deployment:
                Details of the deployment where APIs
                are hosted. A deployment could represent
                an Apigee proxy, API gateway, other
                Google Cloud services or non-Google
                Cloud services as well. A deployment
                entity is a root level entity in the API
                hub and exists independent of any API.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, deployment, deployment_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.CreateDeploymentRequest):
            request = apihub_service.CreateDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if deployment is not None:
                request.deployment = deployment
            if deployment_id is not None:
                request.deployment_id = deployment_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_deployment]

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

    def get_deployment(
        self,
        request: Optional[Union[apihub_service.GetDeploymentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Deployment:
        r"""Get details about a deployment and the API versions
        linked to it.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_deployment():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetDeploymentRequest, dict]):
                The request object. The
                [GetDeployment][google.cloud.apihub.v1.ApiHub.GetDeployment]
                method's request.
            name (str):
                Required. The name of the deployment resource to
                retrieve. Format:
                ``projects/{project}/locations/{location}/deployments/{deployment}``

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
            google.cloud.apihub_v1.types.Deployment:
                Details of the deployment where APIs
                are hosted. A deployment could represent
                an Apigee proxy, API gateway, other
                Google Cloud services or non-Google
                Cloud services as well. A deployment
                entity is a root level entity in the API
                hub and exists independent of any API.

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
        if not isinstance(request, apihub_service.GetDeploymentRequest):
            request = apihub_service.GetDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_deployment]

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

    def list_deployments(
        self,
        request: Optional[Union[apihub_service.ListDeploymentsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListDeploymentsPager:
        r"""List deployment resources in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_deployments():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListDeploymentsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_deployments(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListDeploymentsRequest, dict]):
                The request object. The
                [ListDeployments][google.cloud.apihub.v1.ApiHub.ListDeployments]
                method's request.
            parent (str):
                Required. The parent, which owns this collection of
                deployment resources. Format:
                ``projects/{project}/locations/{location}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListDeploymentsPager:
                The [ListDeployments][google.cloud.apihub.v1.ApiHub.ListDeployments] method's
                   response.

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
        if not isinstance(request, apihub_service.ListDeploymentsRequest):
            request = apihub_service.ListDeploymentsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_deployments]

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
        response = pagers.ListDeploymentsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_deployment(
        self,
        request: Optional[Union[apihub_service.UpdateDeploymentRequest, dict]] = None,
        *,
        deployment: Optional[common_fields.Deployment] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Deployment:
        r"""Update a deployment resource in the API hub. The following
        fields in the [deployment
        resource][google.cloud.apihub.v1.Deployment] can be updated:

        -  [display_name][google.cloud.apihub.v1.Deployment.display_name]
        -  [description][google.cloud.apihub.v1.Deployment.description]
        -  [documentation][google.cloud.apihub.v1.Deployment.documentation]
        -  [deployment_type][google.cloud.apihub.v1.Deployment.deployment_type]
        -  [resource_uri][google.cloud.apihub.v1.Deployment.resource_uri]
        -  [endpoints][google.cloud.apihub.v1.Deployment.endpoints]
        -  [slo][google.cloud.apihub.v1.Deployment.slo]
        -  [environment][google.cloud.apihub.v1.Deployment.environment]
        -  [attributes][google.cloud.apihub.v1.Deployment.attributes]

        The
        [update_mask][google.cloud.apihub.v1.UpdateDeploymentRequest.update_mask]
        should be used to specify the fields being updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_update_deployment():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                deployment = apihub_v1.Deployment()
                deployment.display_name = "display_name_value"
                deployment.deployment_type.enum_values.values.id = "id_value"
                deployment.deployment_type.enum_values.values.display_name = "display_name_value"
                deployment.resource_uri = "resource_uri_value"
                deployment.endpoints = ['endpoints_value1', 'endpoints_value2']

                request = apihub_v1.UpdateDeploymentRequest(
                    deployment=deployment,
                )

                # Make the request
                response = client.update_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.UpdateDeploymentRequest, dict]):
                The request object. The
                [UpdateDeployment][google.cloud.apihub.v1.ApiHub.UpdateDeployment]
                method's request.
            deployment (google.cloud.apihub_v1.types.Deployment):
                Required. The deployment resource to update.

                The deployment resource's ``name`` field is used to
                identify the deployment resource to update. Format:
                ``projects/{project}/locations/{location}/deployments/{deployment}``

                This corresponds to the ``deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

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
            google.cloud.apihub_v1.types.Deployment:
                Details of the deployment where APIs
                are hosted. A deployment could represent
                an Apigee proxy, API gateway, other
                Google Cloud services or non-Google
                Cloud services as well. A deployment
                entity is a root level entity in the API
                hub and exists independent of any API.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([deployment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.UpdateDeploymentRequest):
            request = apihub_service.UpdateDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if deployment is not None:
                request.deployment = deployment
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_deployment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("deployment.name", request.deployment.name),)
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

    def delete_deployment(
        self,
        request: Optional[Union[apihub_service.DeleteDeploymentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a deployment resource in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_delete_deployment():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.DeleteDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_deployment(request=request)

        Args:
            request (Union[google.cloud.apihub_v1.types.DeleteDeploymentRequest, dict]):
                The request object. The
                [DeleteDeployment][google.cloud.apihub.v1.ApiHub.DeleteDeployment]
                method's request.
            name (str):
                Required. The name of the deployment resource to delete.
                Format:
                ``projects/{project}/locations/{location}/deployments/{deployment}``

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
        if not isinstance(request, apihub_service.DeleteDeploymentRequest):
            request = apihub_service.DeleteDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_deployment]

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

    def create_attribute(
        self,
        request: Optional[Union[apihub_service.CreateAttributeRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        attribute: Optional[common_fields.Attribute] = None,
        attribute_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Attribute:
        r"""Create a user defined attribute.

        Certain pre defined attributes are already created by the API
        hub. These attributes will have type as ``SYSTEM_DEFINED`` and
        can be listed via
        [ListAttributes][google.cloud.apihub.v1.ApiHub.ListAttributes]
        method. Allowed values for the same can be updated via
        [UpdateAttribute][google.cloud.apihub.v1.ApiHub.UpdateAttribute]
        method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_create_attribute():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                attribute = apihub_v1.Attribute()
                attribute.display_name = "display_name_value"
                attribute.scope = "PLUGIN"
                attribute.data_type = "STRING"

                request = apihub_v1.CreateAttributeRequest(
                    parent="parent_value",
                    attribute=attribute,
                )

                # Make the request
                response = client.create_attribute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.CreateAttributeRequest, dict]):
                The request object. The
                [CreateAttribute][google.cloud.apihub.v1.ApiHub.CreateAttribute]
                method's request.
            parent (str):
                Required. The parent resource for Attribute. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attribute (google.cloud.apihub_v1.types.Attribute):
                Required. The attribute to create.
                This corresponds to the ``attribute`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attribute_id (str):
                Optional. The ID to use for the attribute, which will
                become the final component of the attribute's resource
                name. This field is optional.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another attribute resource in the API hub.
                -  If not provided, a system generated id will be used.

                This value should be 4-500 characters, and valid
                characters are /[a-z][A-Z][0-9]-_/.

                This corresponds to the ``attribute_id`` field
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
            google.cloud.apihub_v1.types.Attribute:
                An attribute in the API Hub.
                An attribute is a name value pair which
                can be attached to different resources
                in the API hub based on the scope of the
                attribute. Attributes can either be
                pre-defined by the API Hub or created by
                users.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, attribute, attribute_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.CreateAttributeRequest):
            request = apihub_service.CreateAttributeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if attribute is not None:
                request.attribute = attribute
            if attribute_id is not None:
                request.attribute_id = attribute_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_attribute]

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

    def get_attribute(
        self,
        request: Optional[Union[apihub_service.GetAttributeRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Attribute:
        r"""Get details about the attribute.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_attribute():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetAttributeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_attribute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetAttributeRequest, dict]):
                The request object. The
                [GetAttribute][google.cloud.apihub.v1.ApiHub.GetAttribute]
                method's request.
            name (str):
                Required. The name of the attribute to retrieve. Format:
                ``projects/{project}/locations/{location}/attributes/{attribute}``

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
            google.cloud.apihub_v1.types.Attribute:
                An attribute in the API Hub.
                An attribute is a name value pair which
                can be attached to different resources
                in the API hub based on the scope of the
                attribute. Attributes can either be
                pre-defined by the API Hub or created by
                users.

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
        if not isinstance(request, apihub_service.GetAttributeRequest):
            request = apihub_service.GetAttributeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_attribute]

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

    def update_attribute(
        self,
        request: Optional[Union[apihub_service.UpdateAttributeRequest, dict]] = None,
        *,
        attribute: Optional[common_fields.Attribute] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.Attribute:
        r"""Update the attribute. The following fields in the [Attribute
        resource][google.cloud.apihub.v1.Attribute] can be updated:

        -  [display_name][google.cloud.apihub.v1.Attribute.display_name]
           The display name can be updated for user defined attributes
           only.
        -  [description][google.cloud.apihub.v1.Attribute.description]
           The description can be updated for user defined attributes
           only.
        -  [allowed_values][google.cloud.apihub.v1.Attribute.allowed_values]
           To update the list of allowed values, clients need to use the
           fetched list of allowed values and add or remove values to or
           from the same list. The mutable allowed values can be updated
           for both user defined and System defined attributes. The
           immutable allowed values cannot be updated or deleted. The
           updated list of allowed values cannot be empty. If an allowed
           value that is already used by some resource's attribute is
           deleted, then the association between the resource and the
           attribute value will also be deleted.
        -  [cardinality][google.cloud.apihub.v1.Attribute.cardinality]
           The cardinality can be updated for user defined attributes
           only. Cardinality can only be increased during an update.

        The
        [update_mask][google.cloud.apihub.v1.UpdateAttributeRequest.update_mask]
        should be used to specify the fields being updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_update_attribute():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                attribute = apihub_v1.Attribute()
                attribute.display_name = "display_name_value"
                attribute.scope = "PLUGIN"
                attribute.data_type = "STRING"

                request = apihub_v1.UpdateAttributeRequest(
                    attribute=attribute,
                )

                # Make the request
                response = client.update_attribute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.UpdateAttributeRequest, dict]):
                The request object. The
                [UpdateAttribute][google.cloud.apihub.v1.ApiHub.UpdateAttribute]
                method's request.
            attribute (google.cloud.apihub_v1.types.Attribute):
                Required. The attribute to update.

                The attribute's ``name`` field is used to identify the
                attribute to update. Format:
                ``projects/{project}/locations/{location}/attributes/{attribute}``

                This corresponds to the ``attribute`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

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
            google.cloud.apihub_v1.types.Attribute:
                An attribute in the API Hub.
                An attribute is a name value pair which
                can be attached to different resources
                in the API hub based on the scope of the
                attribute. Attributes can either be
                pre-defined by the API Hub or created by
                users.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([attribute, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.UpdateAttributeRequest):
            request = apihub_service.UpdateAttributeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if attribute is not None:
                request.attribute = attribute
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_attribute]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attribute.name", request.attribute.name),)
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

    def delete_attribute(
        self,
        request: Optional[Union[apihub_service.DeleteAttributeRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete an attribute.

        Note: System defined attributes cannot be deleted. All
        associations of the attribute being deleted with any API
        hub resource will also get deleted.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_delete_attribute():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.DeleteAttributeRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_attribute(request=request)

        Args:
            request (Union[google.cloud.apihub_v1.types.DeleteAttributeRequest, dict]):
                The request object. The
                [DeleteAttribute][google.cloud.apihub.v1.ApiHub.DeleteAttribute]
                method's request.
            name (str):
                Required. The name of the attribute to delete. Format:
                ``projects/{project}/locations/{location}/attributes/{attribute}``

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
        if not isinstance(request, apihub_service.DeleteAttributeRequest):
            request = apihub_service.DeleteAttributeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_attribute]

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

    def list_attributes(
        self,
        request: Optional[Union[apihub_service.ListAttributesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAttributesPager:
        r"""List all attributes.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_attributes():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListAttributesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_attributes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListAttributesRequest, dict]):
                The request object. The
                [ListAttributes][google.cloud.apihub.v1.ApiHub.ListAttributes]
                method's request.
            parent (str):
                Required. The parent resource for Attribute. Format:
                ``projects/{project}/locations/{location}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListAttributesPager:
                The [ListAttributes][google.cloud.apihub.v1.ApiHub.ListAttributes] method's
                   response.

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
        if not isinstance(request, apihub_service.ListAttributesRequest):
            request = apihub_service.ListAttributesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_attributes]

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
        response = pagers.ListAttributesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_resources(
        self,
        request: Optional[Union[apihub_service.SearchResourcesRequest, dict]] = None,
        *,
        location: Optional[str] = None,
        query: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.SearchResourcesPager:
        r"""Search across API-Hub resources.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_search_resources():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.SearchResourcesRequest(
                    location="location_value",
                    query="query_value",
                )

                # Make the request
                page_result = client.search_resources(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.SearchResourcesRequest, dict]):
                The request object. The
                [SearchResources][google.cloud.apihub.v1.ApiHub.SearchResources]
                method's request.
            location (str):
                Required. The resource name of the location which will
                be of the type
                ``projects/{project_id}/locations/{location_id}``. This
                field is used to identify the instance of API-Hub in
                which resources should be searched.

                This corresponds to the ``location`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (str):
                Required. The free text search query.
                This query can contain keywords which
                could be related to any detail of the
                API-Hub resources such display names,
                descriptions, attributes etc.

                This corresponds to the ``query`` field
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
            google.cloud.apihub_v1.services.api_hub.pagers.SearchResourcesPager:
                Response for the
                   [SearchResources][google.cloud.apihub.v1.ApiHub.SearchResources]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([location, query])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.SearchResourcesRequest):
            request = apihub_service.SearchResourcesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if location is not None:
                request.location = location
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_resources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("location", request.location),)),
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
        response = pagers.SearchResourcesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_external_api(
        self,
        request: Optional[Union[apihub_service.CreateExternalApiRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        external_api: Optional[common_fields.ExternalApi] = None,
        external_api_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.ExternalApi:
        r"""Create an External API resource in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_create_external_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                external_api = apihub_v1.ExternalApi()
                external_api.display_name = "display_name_value"

                request = apihub_v1.CreateExternalApiRequest(
                    parent="parent_value",
                    external_api=external_api,
                )

                # Make the request
                response = client.create_external_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.CreateExternalApiRequest, dict]):
                The request object. The
                [CreateExternalApi][google.cloud.apihub.v1.ApiHub.CreateExternalApi]
                method's request.
            parent (str):
                Required. The parent resource for the External API
                resource. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            external_api (google.cloud.apihub_v1.types.ExternalApi):
                Required. The External API resource
                to create.

                This corresponds to the ``external_api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            external_api_id (str):
                Optional. The ID to use for the External API resource,
                which will become the final component of the External
                API's resource name. This field is optional.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another External API resource in the API hub.
                -  If not provided, a system generated id will be used.

                This value should be 4-500 characters, and valid
                characters are /[a-z][A-Z][0-9]-_/.

                This corresponds to the ``external_api_id`` field
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
            google.cloud.apihub_v1.types.ExternalApi:
                An external API represents an API
                being provided by external sources. This
                can be used to model third-party APIs
                and can be used to define dependencies.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, external_api, external_api_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.CreateExternalApiRequest):
            request = apihub_service.CreateExternalApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if external_api is not None:
                request.external_api = external_api
            if external_api_id is not None:
                request.external_api_id = external_api_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_external_api]

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

    def get_external_api(
        self,
        request: Optional[Union[apihub_service.GetExternalApiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.ExternalApi:
        r"""Get details about an External API resource in the API
        hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_get_external_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.GetExternalApiRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_external_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.GetExternalApiRequest, dict]):
                The request object. The
                [GetExternalApi][google.cloud.apihub.v1.ApiHub.GetExternalApi]
                method's request.
            name (str):
                Required. The name of the External API resource to
                retrieve. Format:
                ``projects/{project}/locations/{location}/externalApis/{externalApi}``

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
            google.cloud.apihub_v1.types.ExternalApi:
                An external API represents an API
                being provided by external sources. This
                can be used to model third-party APIs
                and can be used to define dependencies.

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
        if not isinstance(request, apihub_service.GetExternalApiRequest):
            request = apihub_service.GetExternalApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_external_api]

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

    def update_external_api(
        self,
        request: Optional[Union[apihub_service.UpdateExternalApiRequest, dict]] = None,
        *,
        external_api: Optional[common_fields.ExternalApi] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> common_fields.ExternalApi:
        r"""Update an External API resource in the API hub. The following
        fields can be updated:

        -  [display_name][google.cloud.apihub.v1.ExternalApi.display_name]
        -  [description][google.cloud.apihub.v1.ExternalApi.description]
        -  [documentation][google.cloud.apihub.v1.ExternalApi.documentation]
        -  [endpoints][google.cloud.apihub.v1.ExternalApi.endpoints]
        -  [paths][google.cloud.apihub.v1.ExternalApi.paths]

        The
        [update_mask][google.cloud.apihub.v1.UpdateExternalApiRequest.update_mask]
        should be used to specify the fields being updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_update_external_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                external_api = apihub_v1.ExternalApi()
                external_api.display_name = "display_name_value"

                request = apihub_v1.UpdateExternalApiRequest(
                    external_api=external_api,
                )

                # Make the request
                response = client.update_external_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.UpdateExternalApiRequest, dict]):
                The request object. The
                [UpdateExternalApi][google.cloud.apihub.v1.ApiHub.UpdateExternalApi]
                method's request.
            external_api (google.cloud.apihub_v1.types.ExternalApi):
                Required. The External API resource to update.

                The External API resource's ``name`` field is used to
                identify the External API resource to update. Format:
                ``projects/{project}/locations/{location}/externalApis/{externalApi}``

                This corresponds to the ``external_api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

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
            google.cloud.apihub_v1.types.ExternalApi:
                An external API represents an API
                being provided by external sources. This
                can be used to model third-party APIs
                and can be used to define dependencies.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([external_api, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, apihub_service.UpdateExternalApiRequest):
            request = apihub_service.UpdateExternalApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if external_api is not None:
                request.external_api = external_api
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_external_api]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("external_api.name", request.external_api.name),)
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

    def delete_external_api(
        self,
        request: Optional[Union[apihub_service.DeleteExternalApiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete an External API resource in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_delete_external_api():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.DeleteExternalApiRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_external_api(request=request)

        Args:
            request (Union[google.cloud.apihub_v1.types.DeleteExternalApiRequest, dict]):
                The request object. The
                [DeleteExternalApi][google.cloud.apihub.v1.ApiHub.DeleteExternalApi]
                method's request.
            name (str):
                Required. The name of the External API resource to
                delete. Format:
                ``projects/{project}/locations/{location}/externalApis/{externalApi}``

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
        if not isinstance(request, apihub_service.DeleteExternalApiRequest):
            request = apihub_service.DeleteExternalApiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_external_api]

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

    def list_external_apis(
        self,
        request: Optional[Union[apihub_service.ListExternalApisRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListExternalApisPager:
        r"""List External API resources in the API hub.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apihub_v1

            def sample_list_external_apis():
                # Create a client
                client = apihub_v1.ApiHubClient()

                # Initialize request argument(s)
                request = apihub_v1.ListExternalApisRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_external_apis(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.apihub_v1.types.ListExternalApisRequest, dict]):
                The request object. The
                [ListExternalApis][google.cloud.apihub.v1.ApiHub.ListExternalApis]
                method's request.
            parent (str):
                Required. The parent, which owns this collection of
                External API resources. Format:
                ``projects/{project}/locations/{location}``

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
            google.cloud.apihub_v1.services.api_hub.pagers.ListExternalApisPager:
                The [ListExternalApis][google.cloud.apihub.v1.ApiHub.ListExternalApis]
                   method's response.

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
        if not isinstance(request, apihub_service.ListExternalApisRequest):
            request = apihub_service.ListExternalApisRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_external_apis]

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
        response = pagers.ListExternalApisPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ApiHubClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_operations]

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

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_operation]

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

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_operation]

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

    def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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
        rpc = self._transport._wrapped_methods[self._transport.get_location]

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
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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
        rpc = self._transport._wrapped_methods[self._transport.list_locations]

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


__all__ = ("ApiHubClient",)
