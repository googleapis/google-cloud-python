# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from http import HTTPStatus
import json
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
import google.protobuf

from google.cloud.saasplatform_saasservicemgmt_v1beta1 import (
    gapic_version as package_version,
)

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

from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments import (
    pagers,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types import (
    common,
    deployments_resources,
    deployments_service,
)

from .transports.base import DEFAULT_CLIENT_INFO, SaasDeploymentsTransport
from .transports.grpc import SaasDeploymentsGrpcTransport
from .transports.grpc_asyncio import SaasDeploymentsGrpcAsyncIOTransport
from .transports.rest import SaasDeploymentsRestTransport


class SaasDeploymentsClientMeta(type):
    """Metaclass for the SaasDeployments client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[SaasDeploymentsTransport]]
    _transport_registry["grpc"] = SaasDeploymentsGrpcTransport
    _transport_registry["grpc_asyncio"] = SaasDeploymentsGrpcAsyncIOTransport
    _transport_registry["rest"] = SaasDeploymentsRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[SaasDeploymentsTransport]:
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


class SaasDeploymentsClient(metaclass=SaasDeploymentsClientMeta):
    """Manages the deployment of SaaS services."""

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
    DEFAULT_ENDPOINT = "saasservicemgmt.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "saasservicemgmt.{UNIVERSE_DOMAIN}"
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
            SaasDeploymentsClient: The constructed client.
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
            SaasDeploymentsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SaasDeploymentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            SaasDeploymentsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def release_path(
        project: str,
        location: str,
        release: str,
    ) -> str:
        """Returns a fully-qualified release string."""
        return "projects/{project}/locations/{location}/releases/{release}".format(
            project=project,
            location=location,
            release=release,
        )

    @staticmethod
    def parse_release_path(path: str) -> Dict[str, str]:
        """Parses a release path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/releases/(?P<release>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def rollout_path(
        project: str,
        location: str,
        rollout_id: str,
    ) -> str:
        """Returns a fully-qualified rollout string."""
        return "projects/{project}/locations/{location}/rollouts/{rollout_id}".format(
            project=project,
            location=location,
            rollout_id=rollout_id,
        )

    @staticmethod
    def parse_rollout_path(path: str) -> Dict[str, str]:
        """Parses a rollout path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/rollouts/(?P<rollout_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def saas_path(
        project: str,
        location: str,
        saas: str,
    ) -> str:
        """Returns a fully-qualified saas string."""
        return "projects/{project}/locations/{location}/saas/{saas}".format(
            project=project,
            location=location,
            saas=saas,
        )

    @staticmethod
    def parse_saas_path(path: str) -> Dict[str, str]:
        """Parses a saas path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/saas/(?P<saas>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def tenant_path(
        project: str,
        location: str,
        tenant: str,
    ) -> str:
        """Returns a fully-qualified tenant string."""
        return "projects/{project}/locations/{location}/tenants/{tenant}".format(
            project=project,
            location=location,
            tenant=tenant,
        )

    @staticmethod
    def parse_tenant_path(path: str) -> Dict[str, str]:
        """Parses a tenant path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/tenants/(?P<tenant>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def unit_path(
        project: str,
        location: str,
        unit: str,
    ) -> str:
        """Returns a fully-qualified unit string."""
        return "projects/{project}/locations/{location}/units/{unit}".format(
            project=project,
            location=location,
            unit=unit,
        )

    @staticmethod
    def parse_unit_path(path: str) -> Dict[str, str]:
        """Parses a unit path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/units/(?P<unit>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def unit_kind_path(
        project: str,
        location: str,
        unitKind: str,
    ) -> str:
        """Returns a fully-qualified unit_kind string."""
        return "projects/{project}/locations/{location}/unitKinds/{unitKind}".format(
            project=project,
            location=location,
            unitKind=unitKind,
        )

    @staticmethod
    def parse_unit_kind_path(path: str) -> Dict[str, str]:
        """Parses a unit_kind path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/unitKinds/(?P<unitKind>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def unit_operation_path(
        project: str,
        location: str,
        unitOperation: str,
    ) -> str:
        """Returns a fully-qualified unit_operation string."""
        return "projects/{project}/locations/{location}/unitOperations/{unitOperation}".format(
            project=project,
            location=location,
            unitOperation=unitOperation,
        )

    @staticmethod
    def parse_unit_operation_path(path: str) -> Dict[str, str]:
        """Parses a unit_operation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/unitOperations/(?P<unitOperation>.+?)$",
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
            _default_universe = SaasDeploymentsClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = SaasDeploymentsClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = SaasDeploymentsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = SaasDeploymentsClient._DEFAULT_UNIVERSE
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

    def _add_cred_info_for_auth_errors(
        self, error: core_exceptions.GoogleAPICallError
    ) -> None:
        """Adds credential info string to error details for 401/403/404 errors.

        Args:
            error (google.api_core.exceptions.GoogleAPICallError): The error to add the cred info.
        """
        if error.code not in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
        ]:
            return

        cred = self._transport._credentials

        # get_cred_info is only available in google-auth>=2.35.0
        if not hasattr(cred, "get_cred_info"):
            return

        # ignore the type check since pypy test fails when get_cred_info
        # is not available
        cred_info = cred.get_cred_info()  # type: ignore
        if cred_info and hasattr(error._details, "append"):
            error._details.append(json.dumps(cred_info))

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
                str, SaasDeploymentsTransport, Callable[..., SaasDeploymentsTransport]
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the saas deployments client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,SaasDeploymentsTransport,Callable[..., SaasDeploymentsTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the SaasDeploymentsTransport constructor.
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
        ) = SaasDeploymentsClient._read_environment_variables()
        self._client_cert_source = SaasDeploymentsClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = SaasDeploymentsClient._get_universe_domain(
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
        transport_provided = isinstance(transport, SaasDeploymentsTransport)
        if transport_provided:
            # transport is a SaasDeploymentsTransport instance.
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
            self._transport = cast(SaasDeploymentsTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or SaasDeploymentsClient._get_api_endpoint(
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
                Type[SaasDeploymentsTransport], Callable[..., SaasDeploymentsTransport]
            ] = (
                SaasDeploymentsClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., SaasDeploymentsTransport], transport)
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
                    "Created client `google.cloud.saasplatform.saasservicemgmt_v1beta1.SaasDeploymentsClient`.",
                    extra={
                        "serviceName": "google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments",
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
                        "serviceName": "google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments",
                        "credentialsType": None,
                    },
                )

    def list_saas(
        self,
        request: Optional[Union[deployments_service.ListSaasRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListSaasPager:
        r"""Retrieve a collection of saas.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_list_saas():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.ListSaasRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_saas(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.ListSaasRequest, dict]):
                The request object. The request structure for the
                ListSaas method.
            parent (str):
                Required. The parent of the saas.
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.pagers.ListSaasPager:
                The response structure for the
                ListSaas method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.ListSaasRequest):
            request = deployments_service.ListSaasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_saas]

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
        response = pagers.ListSaasPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_saas(
        self,
        request: Optional[Union[deployments_service.GetSaasRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Saas:
        r"""Retrieve a single saas.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_get_saas():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.GetSaasRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_saas(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.GetSaasRequest, dict]):
                The request object. The request structure for the GetSaas
                method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Saas:
                Saas is a representation of a SaaS
                service managed by the Producer.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.GetSaasRequest):
            request = deployments_service.GetSaasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_saas]

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

    def create_saas(
        self,
        request: Optional[Union[deployments_service.CreateSaasRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        saas: Optional[deployments_resources.Saas] = None,
        saas_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Saas:
        r"""Create a new saas.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_create_saas():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.CreateSaasRequest(
                    parent="parent_value",
                    saas_id="saas_id_value",
                )

                # Make the request
                response = client.create_saas(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.CreateSaasRequest, dict]):
                The request object. The request structure for the
                CreateSaas method.
            parent (str):
                Required. The parent of the saas.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            saas (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Saas):
                Required. The desired state for the
                saas.

                This corresponds to the ``saas`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            saas_id (str):
                Required. The ID value for the new
                saas.

                This corresponds to the ``saas_id`` field
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Saas:
                Saas is a representation of a SaaS
                service managed by the Producer.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, saas, saas_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.CreateSaasRequest):
            request = deployments_service.CreateSaasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if saas is not None:
                request.saas = saas
            if saas_id is not None:
                request.saas_id = saas_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_saas]

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

    def update_saas(
        self,
        request: Optional[Union[deployments_service.UpdateSaasRequest, dict]] = None,
        *,
        saas: Optional[deployments_resources.Saas] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Saas:
        r"""Update a single saas.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_update_saas():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.UpdateSaasRequest(
                )

                # Make the request
                response = client.update_saas(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UpdateSaasRequest, dict]):
                The request object. The request structure for the
                UpdateSaas method.
            saas (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Saas):
                Required. The desired state for the
                saas.

                This corresponds to the ``saas`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Field mask is used to specify the fields to be
                overwritten in the Saas resource by the update.

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                If the user does not provide a mask then all fields in
                the Saas will be overwritten.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Saas:
                Saas is a representation of a SaaS
                service managed by the Producer.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [saas, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.UpdateSaasRequest):
            request = deployments_service.UpdateSaasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if saas is not None:
                request.saas = saas
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_saas]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("saas.name", request.saas.name),)
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

    def delete_saas(
        self,
        request: Optional[Union[deployments_service.DeleteSaasRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a single saas.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_delete_saas():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.DeleteSaasRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_saas(request=request)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.DeleteSaasRequest, dict]):
                The request object. The request structure for the
                DeleteSaas method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.DeleteSaasRequest):
            request = deployments_service.DeleteSaasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_saas]

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

    def list_tenants(
        self,
        request: Optional[Union[deployments_service.ListTenantsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListTenantsPager:
        r"""Retrieve a collection of tenants.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_list_tenants():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.ListTenantsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tenants(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.ListTenantsRequest, dict]):
                The request object. The request structure for the
                ListTenants method.
            parent (str):
                Required. The parent of the tenant.
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.pagers.ListTenantsPager:
                The response structure for the
                ListTenants method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.ListTenantsRequest):
            request = deployments_service.ListTenantsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_tenants]

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
        response = pagers.ListTenantsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_tenant(
        self,
        request: Optional[Union[deployments_service.GetTenantRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Tenant:
        r"""Retrieve a single tenant.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_get_tenant():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.GetTenantRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_tenant(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.GetTenantRequest, dict]):
                The request object. The request structure for the
                GetTenant method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Tenant:
                Tenant represents the service producer side of an instance of the
                   service created based on a request from a consumer.
                   In a typical scenario a Tenant has a one-to-one
                   mapping with a resource given out to a service
                   consumer.

                   Example:

                      tenant:
                         name:
                         "projects/svc1/locations/loc/tenants/inst-068afff8"
                         consumer_resource:
                         "projects/gshoe/locations/loc/shoes/black-shoe"

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.GetTenantRequest):
            request = deployments_service.GetTenantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_tenant]

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

    def create_tenant(
        self,
        request: Optional[Union[deployments_service.CreateTenantRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        tenant: Optional[deployments_resources.Tenant] = None,
        tenant_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Tenant:
        r"""Create a new tenant.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_create_tenant():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                tenant = saasplatform_saasservicemgmt_v1beta1.Tenant()
                tenant.saas = "saas_value"

                request = saasplatform_saasservicemgmt_v1beta1.CreateTenantRequest(
                    parent="parent_value",
                    tenant_id="tenant_id_value",
                    tenant=tenant,
                )

                # Make the request
                response = client.create_tenant(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.CreateTenantRequest, dict]):
                The request object. The request structure for the
                CreateTenant method.
            parent (str):
                Required. The parent of the tenant.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tenant (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Tenant):
                Required. The desired state for the
                tenant.

                This corresponds to the ``tenant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tenant_id (str):
                Required. The ID value for the new
                tenant.

                This corresponds to the ``tenant_id`` field
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Tenant:
                Tenant represents the service producer side of an instance of the
                   service created based on a request from a consumer.
                   In a typical scenario a Tenant has a one-to-one
                   mapping with a resource given out to a service
                   consumer.

                   Example:

                      tenant:
                         name:
                         "projects/svc1/locations/loc/tenants/inst-068afff8"
                         consumer_resource:
                         "projects/gshoe/locations/loc/shoes/black-shoe"

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, tenant, tenant_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.CreateTenantRequest):
            request = deployments_service.CreateTenantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if tenant is not None:
                request.tenant = tenant
            if tenant_id is not None:
                request.tenant_id = tenant_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_tenant]

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

    def update_tenant(
        self,
        request: Optional[Union[deployments_service.UpdateTenantRequest, dict]] = None,
        *,
        tenant: Optional[deployments_resources.Tenant] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Tenant:
        r"""Update a single tenant.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_update_tenant():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                tenant = saasplatform_saasservicemgmt_v1beta1.Tenant()
                tenant.saas = "saas_value"

                request = saasplatform_saasservicemgmt_v1beta1.UpdateTenantRequest(
                    tenant=tenant,
                )

                # Make the request
                response = client.update_tenant(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UpdateTenantRequest, dict]):
                The request object. The request structure for the
                UpdateTenant method.
            tenant (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Tenant):
                Required. The desired state for the
                tenant.

                This corresponds to the ``tenant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Field mask is used to specify the fields to be
                overwritten in the Tenant resource by the update.

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                If the user does not provide a mask then all fields in
                the Tenant will be overwritten.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Tenant:
                Tenant represents the service producer side of an instance of the
                   service created based on a request from a consumer.
                   In a typical scenario a Tenant has a one-to-one
                   mapping with a resource given out to a service
                   consumer.

                   Example:

                      tenant:
                         name:
                         "projects/svc1/locations/loc/tenants/inst-068afff8"
                         consumer_resource:
                         "projects/gshoe/locations/loc/shoes/black-shoe"

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [tenant, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.UpdateTenantRequest):
            request = deployments_service.UpdateTenantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tenant is not None:
                request.tenant = tenant
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_tenant]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tenant.name", request.tenant.name),)
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

    def delete_tenant(
        self,
        request: Optional[Union[deployments_service.DeleteTenantRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a single tenant.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_delete_tenant():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.DeleteTenantRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_tenant(request=request)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.DeleteTenantRequest, dict]):
                The request object. The request structure for the
                DeleteTenant method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.DeleteTenantRequest):
            request = deployments_service.DeleteTenantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_tenant]

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

    def list_unit_kinds(
        self,
        request: Optional[Union[deployments_service.ListUnitKindsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListUnitKindsPager:
        r"""Retrieve a collection of unit kinds.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_list_unit_kinds():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.ListUnitKindsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_unit_kinds(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.ListUnitKindsRequest, dict]):
                The request object. The request structure for the
                ListUnitKinds method.
            parent (str):
                Required. The parent of the unit
                kind.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.pagers.ListUnitKindsPager:
                The response structure for the
                ListUnitKinds method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.ListUnitKindsRequest):
            request = deployments_service.ListUnitKindsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_unit_kinds]

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
        response = pagers.ListUnitKindsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_unit_kind(
        self,
        request: Optional[Union[deployments_service.GetUnitKindRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.UnitKind:
        r"""Retrieve a single unit kind.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_get_unit_kind():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.GetUnitKindRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_unit_kind(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.GetUnitKindRequest, dict]):
                The request object. The request structure for the
                GetUnitKind method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitKind:
                Definition of a Unit. Units belonging
                to the same UnitKind are managed
                together; for example they follow the
                same release model (blueprints, versions
                etc.) and are typically rolled out
                together.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.GetUnitKindRequest):
            request = deployments_service.GetUnitKindRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_unit_kind]

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

    def create_unit_kind(
        self,
        request: Optional[
            Union[deployments_service.CreateUnitKindRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        unit_kind: Optional[deployments_resources.UnitKind] = None,
        unit_kind_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.UnitKind:
        r"""Create a new unit kind.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_create_unit_kind():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                unit_kind = saasplatform_saasservicemgmt_v1beta1.UnitKind()
                unit_kind.saas = "saas_value"

                request = saasplatform_saasservicemgmt_v1beta1.CreateUnitKindRequest(
                    parent="parent_value",
                    unit_kind_id="unit_kind_id_value",
                    unit_kind=unit_kind,
                )

                # Make the request
                response = client.create_unit_kind(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.CreateUnitKindRequest, dict]):
                The request object. The request structure for the
                CreateUnitKind method.
            parent (str):
                Required. The parent of the unit
                kind.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            unit_kind (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitKind):
                Required. The desired state for the
                unit kind.

                This corresponds to the ``unit_kind`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            unit_kind_id (str):
                Required. The ID value for the new
                unit kind.

                This corresponds to the ``unit_kind_id`` field
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitKind:
                Definition of a Unit. Units belonging
                to the same UnitKind are managed
                together; for example they follow the
                same release model (blueprints, versions
                etc.) and are typically rolled out
                together.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, unit_kind, unit_kind_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.CreateUnitKindRequest):
            request = deployments_service.CreateUnitKindRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if unit_kind is not None:
                request.unit_kind = unit_kind
            if unit_kind_id is not None:
                request.unit_kind_id = unit_kind_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_unit_kind]

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

    def update_unit_kind(
        self,
        request: Optional[
            Union[deployments_service.UpdateUnitKindRequest, dict]
        ] = None,
        *,
        unit_kind: Optional[deployments_resources.UnitKind] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.UnitKind:
        r"""Update a single unit kind.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_update_unit_kind():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                unit_kind = saasplatform_saasservicemgmt_v1beta1.UnitKind()
                unit_kind.saas = "saas_value"

                request = saasplatform_saasservicemgmt_v1beta1.UpdateUnitKindRequest(
                    unit_kind=unit_kind,
                )

                # Make the request
                response = client.update_unit_kind(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UpdateUnitKindRequest, dict]):
                The request object. The request structure for the
                UpdateUnitKind method.
            unit_kind (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitKind):
                Required. The desired state for the
                unit kind.

                This corresponds to the ``unit_kind`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Field mask is used to specify the fields to be
                overwritten in the UnitKind resource by the update.

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                If the user does not provide a mask then all fields in
                the UnitKind will be overwritten.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitKind:
                Definition of a Unit. Units belonging
                to the same UnitKind are managed
                together; for example they follow the
                same release model (blueprints, versions
                etc.) and are typically rolled out
                together.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [unit_kind, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.UpdateUnitKindRequest):
            request = deployments_service.UpdateUnitKindRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if unit_kind is not None:
                request.unit_kind = unit_kind
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_unit_kind]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("unit_kind.name", request.unit_kind.name),)
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

    def delete_unit_kind(
        self,
        request: Optional[
            Union[deployments_service.DeleteUnitKindRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a single unit kind.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_delete_unit_kind():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.DeleteUnitKindRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_unit_kind(request=request)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.DeleteUnitKindRequest, dict]):
                The request object. The request structure for the
                DeleteUnitKind method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.DeleteUnitKindRequest):
            request = deployments_service.DeleteUnitKindRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_unit_kind]

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

    def list_units(
        self,
        request: Optional[Union[deployments_service.ListUnitsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListUnitsPager:
        r"""Retrieve a collection of units.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_list_units():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.ListUnitsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_units(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.ListUnitsRequest, dict]):
                The request object. The request structure for the
                ListUnits method.
            parent (str):
                Required. The parent of the unit.
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.pagers.ListUnitsPager:
                The response structure for the
                ListUnits method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.ListUnitsRequest):
            request = deployments_service.ListUnitsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_units]

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
        response = pagers.ListUnitsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_unit(
        self,
        request: Optional[Union[deployments_service.GetUnitRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Unit:
        r"""Retrieve a single unit.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_get_unit():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.GetUnitRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_unit(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.GetUnitRequest, dict]):
                The request object. The request structure for the GetUnit
                method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Unit:
                A unit of deployment that has its
                lifecycle via a CRUD API using an
                actuation engine under the hood (e.g.
                based on Terraform, Helm or a custom
                implementation provided by a service
                producer). A building block of a SaaS
                Tenant.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.GetUnitRequest):
            request = deployments_service.GetUnitRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_unit]

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

    def create_unit(
        self,
        request: Optional[Union[deployments_service.CreateUnitRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        unit: Optional[deployments_resources.Unit] = None,
        unit_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Unit:
        r"""Create a new unit.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_create_unit():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.CreateUnitRequest(
                    parent="parent_value",
                    unit_id="unit_id_value",
                )

                # Make the request
                response = client.create_unit(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.CreateUnitRequest, dict]):
                The request object. The request structure for the
                CreateUnit method.
            parent (str):
                Required. The parent of the unit.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            unit (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Unit):
                Required. The desired state for the
                unit.

                This corresponds to the ``unit`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            unit_id (str):
                Required. The ID value for the new
                unit.

                This corresponds to the ``unit_id`` field
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Unit:
                A unit of deployment that has its
                lifecycle via a CRUD API using an
                actuation engine under the hood (e.g.
                based on Terraform, Helm or a custom
                implementation provided by a service
                producer). A building block of a SaaS
                Tenant.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, unit, unit_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.CreateUnitRequest):
            request = deployments_service.CreateUnitRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if unit is not None:
                request.unit = unit
            if unit_id is not None:
                request.unit_id = unit_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_unit]

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

    def update_unit(
        self,
        request: Optional[Union[deployments_service.UpdateUnitRequest, dict]] = None,
        *,
        unit: Optional[deployments_resources.Unit] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Unit:
        r"""Update a single unit.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_update_unit():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.UpdateUnitRequest(
                )

                # Make the request
                response = client.update_unit(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UpdateUnitRequest, dict]):
                The request object. The request structure for the
                UpdateUnit method.
            unit (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Unit):
                Required. The desired state for the
                unit.

                This corresponds to the ``unit`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Field mask is used to specify the fields to be
                overwritten in the Unit resource by the update.

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                If the user does not provide a mask then all fields in
                the Unit will be overwritten.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Unit:
                A unit of deployment that has its
                lifecycle via a CRUD API using an
                actuation engine under the hood (e.g.
                based on Terraform, Helm or a custom
                implementation provided by a service
                producer). A building block of a SaaS
                Tenant.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [unit, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.UpdateUnitRequest):
            request = deployments_service.UpdateUnitRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if unit is not None:
                request.unit = unit
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_unit]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("unit.name", request.unit.name),)
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

    def delete_unit(
        self,
        request: Optional[Union[deployments_service.DeleteUnitRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a single unit.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_delete_unit():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.DeleteUnitRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_unit(request=request)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.DeleteUnitRequest, dict]):
                The request object. The request structure for the
                DeleteUnit method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.DeleteUnitRequest):
            request = deployments_service.DeleteUnitRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_unit]

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

    def list_unit_operations(
        self,
        request: Optional[
            Union[deployments_service.ListUnitOperationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListUnitOperationsPager:
        r"""Retrieve a collection of unit operations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_list_unit_operations():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.ListUnitOperationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_unit_operations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.ListUnitOperationsRequest, dict]):
                The request object. The request structure for the
                ListUnitOperations method.
            parent (str):
                Required. The parent of the unit
                operation.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.pagers.ListUnitOperationsPager:
                The response structure for the
                ListUnitOperations method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.ListUnitOperationsRequest):
            request = deployments_service.ListUnitOperationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_unit_operations]

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
        response = pagers.ListUnitOperationsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_unit_operation(
        self,
        request: Optional[
            Union[deployments_service.GetUnitOperationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.UnitOperation:
        r"""Retrieve a single unit operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_get_unit_operation():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.GetUnitOperationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_unit_operation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.GetUnitOperationRequest, dict]):
                The request object. The request structure for the
                GetUnitOperation method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitOperation:
                UnitOperation encapsulates the intent
                of changing/interacting with the service
                component represented by the specific
                Unit. Multiple UnitOperations can be
                created (requested) and scheduled in the
                future, however only one will be allowed
                to execute at a time (that can change in
                the future for non-mutating operations).

                UnitOperations allow different actors
                interacting with the same unit to focus
                only on the change they have requested.

                This is a base object that contains the
                common fields in all unit operations.
                Next: 19

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.GetUnitOperationRequest):
            request = deployments_service.GetUnitOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_unit_operation]

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

    def create_unit_operation(
        self,
        request: Optional[
            Union[deployments_service.CreateUnitOperationRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        unit_operation: Optional[deployments_resources.UnitOperation] = None,
        unit_operation_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.UnitOperation:
        r"""Create a new unit operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_create_unit_operation():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                unit_operation = saasplatform_saasservicemgmt_v1beta1.UnitOperation()
                unit_operation.unit = "unit_value"

                request = saasplatform_saasservicemgmt_v1beta1.CreateUnitOperationRequest(
                    parent="parent_value",
                    unit_operation_id="unit_operation_id_value",
                    unit_operation=unit_operation,
                )

                # Make the request
                response = client.create_unit_operation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.CreateUnitOperationRequest, dict]):
                The request object. The request structure for the
                CreateUnitOperation method.
            parent (str):
                Required. The parent of the unit
                operation.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            unit_operation (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitOperation):
                Required. The desired state for the
                unit operation.

                This corresponds to the ``unit_operation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            unit_operation_id (str):
                Required. The ID value for the new
                unit operation.

                This corresponds to the ``unit_operation_id`` field
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitOperation:
                UnitOperation encapsulates the intent
                of changing/interacting with the service
                component represented by the specific
                Unit. Multiple UnitOperations can be
                created (requested) and scheduled in the
                future, however only one will be allowed
                to execute at a time (that can change in
                the future for non-mutating operations).

                UnitOperations allow different actors
                interacting with the same unit to focus
                only on the change they have requested.

                This is a base object that contains the
                common fields in all unit operations.
                Next: 19

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, unit_operation, unit_operation_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.CreateUnitOperationRequest):
            request = deployments_service.CreateUnitOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if unit_operation is not None:
                request.unit_operation = unit_operation
            if unit_operation_id is not None:
                request.unit_operation_id = unit_operation_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_unit_operation]

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

    def update_unit_operation(
        self,
        request: Optional[
            Union[deployments_service.UpdateUnitOperationRequest, dict]
        ] = None,
        *,
        unit_operation: Optional[deployments_resources.UnitOperation] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.UnitOperation:
        r"""Update a single unit operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_update_unit_operation():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                unit_operation = saasplatform_saasservicemgmt_v1beta1.UnitOperation()
                unit_operation.unit = "unit_value"

                request = saasplatform_saasservicemgmt_v1beta1.UpdateUnitOperationRequest(
                    unit_operation=unit_operation,
                )

                # Make the request
                response = client.update_unit_operation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UpdateUnitOperationRequest, dict]):
                The request object. The request structure for the
                UpdateUnitOperation method.
            unit_operation (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitOperation):
                Required. The desired state for the
                unit operation.

                This corresponds to the ``unit_operation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Field mask is used to specify the fields to be
                overwritten in the UnitOperation resource by the update.

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                If the user does not provide a mask then all fields in
                the UnitOperation will be overwritten.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UnitOperation:
                UnitOperation encapsulates the intent
                of changing/interacting with the service
                component represented by the specific
                Unit. Multiple UnitOperations can be
                created (requested) and scheduled in the
                future, however only one will be allowed
                to execute at a time (that can change in
                the future for non-mutating operations).

                UnitOperations allow different actors
                interacting with the same unit to focus
                only on the change they have requested.

                This is a base object that contains the
                common fields in all unit operations.
                Next: 19

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [unit_operation, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.UpdateUnitOperationRequest):
            request = deployments_service.UpdateUnitOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if unit_operation is not None:
                request.unit_operation = unit_operation
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_unit_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("unit_operation.name", request.unit_operation.name),)
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

    def delete_unit_operation(
        self,
        request: Optional[
            Union[deployments_service.DeleteUnitOperationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a single unit operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_delete_unit_operation():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.DeleteUnitOperationRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_unit_operation(request=request)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.DeleteUnitOperationRequest, dict]):
                The request object. The request structure for the
                DeleteUnitOperation method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.DeleteUnitOperationRequest):
            request = deployments_service.DeleteUnitOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_unit_operation]

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

    def list_releases(
        self,
        request: Optional[Union[deployments_service.ListReleasesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListReleasesPager:
        r"""Retrieve a collection of releases.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_list_releases():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.ListReleasesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_releases(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.ListReleasesRequest, dict]):
                The request object. The request structure for the
                ListReleases method.
            parent (str):
                Required. The parent of the release.
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.pagers.ListReleasesPager:
                The response structure for the
                ListReleases method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.ListReleasesRequest):
            request = deployments_service.ListReleasesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_releases]

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
        response = pagers.ListReleasesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_release(
        self,
        request: Optional[Union[deployments_service.GetReleaseRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Release:
        r"""Retrieve a single release.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_get_release():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.GetReleaseRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_release(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.GetReleaseRequest, dict]):
                The request object. The request structure for the
                GetRelease method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Release:
                A new version to be propagated and
                deployed to units. This includes
                pointers to packaged blueprints for
                actuation (e.g Helm or Terraform
                configuration packages) via artifact
                registry.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.GetReleaseRequest):
            request = deployments_service.GetReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_release]

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

    def create_release(
        self,
        request: Optional[Union[deployments_service.CreateReleaseRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        release: Optional[deployments_resources.Release] = None,
        release_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Release:
        r"""Create a new release.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_create_release():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                release = saasplatform_saasservicemgmt_v1beta1.Release()
                release.unit_kind = "unit_kind_value"

                request = saasplatform_saasservicemgmt_v1beta1.CreateReleaseRequest(
                    parent="parent_value",
                    release_id="release_id_value",
                    release=release,
                )

                # Make the request
                response = client.create_release(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.CreateReleaseRequest, dict]):
                The request object. The request structure for the
                CreateRelease method.
            parent (str):
                Required. The parent of the release.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Release):
                Required. The desired state for the
                release.

                This corresponds to the ``release`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release_id (str):
                Required. The ID value for the new
                release.

                This corresponds to the ``release_id`` field
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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Release:
                A new version to be propagated and
                deployed to units. This includes
                pointers to packaged blueprints for
                actuation (e.g Helm or Terraform
                configuration packages) via artifact
                registry.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, release, release_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.CreateReleaseRequest):
            request = deployments_service.CreateReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if release is not None:
                request.release = release
            if release_id is not None:
                request.release_id = release_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_release]

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

    def update_release(
        self,
        request: Optional[Union[deployments_service.UpdateReleaseRequest, dict]] = None,
        *,
        release: Optional[deployments_resources.Release] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> deployments_resources.Release:
        r"""Update a single release.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_update_release():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                release = saasplatform_saasservicemgmt_v1beta1.Release()
                release.unit_kind = "unit_kind_value"

                request = saasplatform_saasservicemgmt_v1beta1.UpdateReleaseRequest(
                    release=release,
                )

                # Make the request
                response = client.update_release(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.UpdateReleaseRequest, dict]):
                The request object. The request structure for the
                UpdateRelease method.
            release (google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Release):
                Required. The desired state for the
                release.

                This corresponds to the ``release`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Field mask is used to specify the fields to be
                overwritten in the Release resource by the update.

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                If the user does not provide a mask then all fields in
                the Release will be overwritten.

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
            google.cloud.saasplatform_saasservicemgmt_v1beta1.types.Release:
                A new version to be propagated and
                deployed to units. This includes
                pointers to packaged blueprints for
                actuation (e.g Helm or Terraform
                configuration packages) via artifact
                registry.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [release, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.UpdateReleaseRequest):
            request = deployments_service.UpdateReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if release is not None:
                request.release = release
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_release]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("release.name", request.release.name),)
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

    def delete_release(
        self,
        request: Optional[Union[deployments_service.DeleteReleaseRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Delete a single release.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import saasplatform_saasservicemgmt_v1beta1

            def sample_delete_release():
                # Create a client
                client = saasplatform_saasservicemgmt_v1beta1.SaasDeploymentsClient()

                # Initialize request argument(s)
                request = saasplatform_saasservicemgmt_v1beta1.DeleteReleaseRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_release(request=request)

        Args:
            request (Union[google.cloud.saasplatform_saasservicemgmt_v1beta1.types.DeleteReleaseRequest, dict]):
                The request object. The request structure for the
                DeleteRelease method.
            name (str):
                Required. The resource name of the
                resource within a service.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, deployments_service.DeleteReleaseRequest):
            request = deployments_service.DeleteReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_release]

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

    def __enter__(self) -> "SaasDeploymentsClient":
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

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e

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

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__

__all__ = ("SaasDeploymentsClient",)
