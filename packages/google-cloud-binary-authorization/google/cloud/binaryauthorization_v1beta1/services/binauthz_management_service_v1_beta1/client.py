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

from google.cloud.binaryauthorization_v1beta1 import gapic_version as package_version

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

from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.binaryauthorization_v1beta1.services.binauthz_management_service_v1_beta1 import (
    pagers,
)
from google.cloud.binaryauthorization_v1beta1.types import resources, service

from .transports.base import (
    DEFAULT_CLIENT_INFO,
    BinauthzManagementServiceV1Beta1Transport,
)
from .transports.grpc import BinauthzManagementServiceV1Beta1GrpcTransport
from .transports.grpc_asyncio import (
    BinauthzManagementServiceV1Beta1GrpcAsyncIOTransport,
)
from .transports.rest import BinauthzManagementServiceV1Beta1RestTransport


class BinauthzManagementServiceV1Beta1ClientMeta(type):
    """Metaclass for the BinauthzManagementServiceV1Beta1 client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[BinauthzManagementServiceV1Beta1Transport]]
    _transport_registry["grpc"] = BinauthzManagementServiceV1Beta1GrpcTransport
    _transport_registry[
        "grpc_asyncio"
    ] = BinauthzManagementServiceV1Beta1GrpcAsyncIOTransport
    _transport_registry["rest"] = BinauthzManagementServiceV1Beta1RestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[BinauthzManagementServiceV1Beta1Transport]:
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


class BinauthzManagementServiceV1Beta1Client(
    metaclass=BinauthzManagementServiceV1Beta1ClientMeta
):
    """Google Cloud Management Service for Binary Authorization admission
    policies and attestation authorities.

    This API implements a REST model with the following objects:

    -  [Policy][google.cloud.binaryauthorization.v1beta1.Policy]
    -  [Attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
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
    DEFAULT_ENDPOINT = "binaryauthorization.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "binaryauthorization.{UNIVERSE_DOMAIN}"
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
            BinauthzManagementServiceV1Beta1Client: The constructed client.
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
            BinauthzManagementServiceV1Beta1Client: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BinauthzManagementServiceV1Beta1Transport:
        """Returns the transport used by the client instance.

        Returns:
            BinauthzManagementServiceV1Beta1Transport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def attestor_path(
        project: str,
        attestor: str,
    ) -> str:
        """Returns a fully-qualified attestor string."""
        return "projects/{project}/attestors/{attestor}".format(
            project=project,
            attestor=attestor,
        )

    @staticmethod
    def parse_attestor_path(path: str) -> Dict[str, str]:
        """Parses a attestor path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/attestors/(?P<attestor>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def policy_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified policy string."""
        return "projects/{project}/policy".format(
            project=project,
        )

    @staticmethod
    def parse_policy_path(path: str) -> Dict[str, str]:
        """Parses a policy path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/policy$", path)
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
            _default_universe = BinauthzManagementServiceV1Beta1Client._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = BinauthzManagementServiceV1Beta1Client.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = BinauthzManagementServiceV1Beta1Client._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = BinauthzManagementServiceV1Beta1Client._DEFAULT_UNIVERSE
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
                BinauthzManagementServiceV1Beta1Transport,
                Callable[..., BinauthzManagementServiceV1Beta1Transport],
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the binauthz management service v1 beta1 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,BinauthzManagementServiceV1Beta1Transport,Callable[..., BinauthzManagementServiceV1Beta1Transport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the BinauthzManagementServiceV1Beta1Transport constructor.
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
        ) = BinauthzManagementServiceV1Beta1Client._read_environment_variables()
        self._client_cert_source = (
            BinauthzManagementServiceV1Beta1Client._get_client_cert_source(
                self._client_options.client_cert_source, self._use_client_cert
            )
        )
        self._universe_domain = (
            BinauthzManagementServiceV1Beta1Client._get_universe_domain(
                universe_domain_opt, self._universe_domain_env
            )
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
        transport_provided = isinstance(
            transport, BinauthzManagementServiceV1Beta1Transport
        )
        if transport_provided:
            # transport is a BinauthzManagementServiceV1Beta1Transport instance.
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
            self._transport = cast(BinauthzManagementServiceV1Beta1Transport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or BinauthzManagementServiceV1Beta1Client._get_api_endpoint(
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
                Type[BinauthzManagementServiceV1Beta1Transport],
                Callable[..., BinauthzManagementServiceV1Beta1Transport],
            ] = (
                BinauthzManagementServiceV1Beta1Client.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(
                    Callable[..., BinauthzManagementServiceV1Beta1Transport], transport
                )
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
                    "Created client `google.cloud.binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client`.",
                    extra={
                        "serviceName": "google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1",
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
                        "serviceName": "google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1",
                        "credentialsType": None,
                    },
                )

    def get_policy(
        self,
        request: Optional[Union[service.GetPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> resources.Policy:
        r"""A [policy][google.cloud.binaryauthorization.v1beta1.Policy]
        specifies the
        [attestors][google.cloud.binaryauthorization.v1beta1.Attestor]
        that must attest to a container image, before the project is
        allowed to deploy that image. There is at most one policy per
        project. All image admission requests are permitted if a project
        has no policy.

        Gets the
        [policy][google.cloud.binaryauthorization.v1beta1.Policy] for
        this project. Returns a default
        [policy][google.cloud.binaryauthorization.v1beta1.Policy] if the
        project does not have one.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_get_policy():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                request = binaryauthorization_v1beta1.GetPolicyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.GetPolicyRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.GetPolicy][].
            name (str):
                Required. The resource name of the
                [policy][google.cloud.binaryauthorization.v1beta1.Policy]
                to retrieve, in the format ``projects/*/policy``.

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
            google.cloud.binaryauthorization_v1beta1.types.Policy:
                A
                [policy][google.cloud.binaryauthorization.v1beta1.Policy]
                for Binary Authorization.

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
        if not isinstance(request, service.GetPolicyRequest):
            request = service.GetPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_policy]

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

    def update_policy(
        self,
        request: Optional[Union[service.UpdatePolicyRequest, dict]] = None,
        *,
        policy: Optional[resources.Policy] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> resources.Policy:
        r"""Creates or updates a project's
        [policy][google.cloud.binaryauthorization.v1beta1.Policy], and
        returns a copy of the new
        [policy][google.cloud.binaryauthorization.v1beta1.Policy]. A
        policy is always updated as a whole, to avoid race conditions
        with concurrent policy enforcement (or management!) requests.
        Returns NOT_FOUND if the project does not exist,
        INVALID_ARGUMENT if the request is malformed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_update_policy():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                policy = binaryauthorization_v1beta1.Policy()
                policy.default_admission_rule.evaluation_mode = "ALWAYS_DENY"
                policy.default_admission_rule.enforcement_mode = "DRYRUN_AUDIT_LOG_ONLY"

                request = binaryauthorization_v1beta1.UpdatePolicyRequest(
                    policy=policy,
                )

                # Make the request
                response = client.update_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.UpdatePolicyRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.UpdatePolicy][].
            policy (google.cloud.binaryauthorization_v1beta1.types.Policy):
                Required. A new or updated
                [policy][google.cloud.binaryauthorization.v1beta1.Policy]
                value. The service will overwrite the [policy
                name][google.cloud.binaryauthorization.v1beta1.Policy.name]
                field with the resource name in the request URL, in the
                format ``projects/*/policy``.

                This corresponds to the ``policy`` field
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
            google.cloud.binaryauthorization_v1beta1.types.Policy:
                A
                [policy][google.cloud.binaryauthorization.v1beta1.Policy]
                for Binary Authorization.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, service.UpdatePolicyRequest):
            request = service.UpdatePolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if policy is not None:
                request.policy = policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_policy]

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

        # Done; return the response.
        return response

    def create_attestor(
        self,
        request: Optional[Union[service.CreateAttestorRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        attestor_id: Optional[str] = None,
        attestor: Optional[resources.Attestor] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> resources.Attestor:
        r"""Creates an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor],
        and returns a copy of the new
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the project does not exist,
        INVALID_ARGUMENT if the request is malformed, ALREADY_EXISTS if
        the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        already exists.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_create_attestor():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                attestor = binaryauthorization_v1beta1.Attestor()
                attestor.user_owned_drydock_note.note_reference = "note_reference_value"
                attestor.name = "name_value"

                request = binaryauthorization_v1beta1.CreateAttestorRequest(
                    parent="parent_value",
                    attestor_id="attestor_id_value",
                    attestor=attestor,
                )

                # Make the request
                response = client.create_attestor(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.CreateAttestorRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.CreateAttestor][].
            parent (str):
                Required. The parent of this
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attestor_id (str):
                Required. The
                [attestors][google.cloud.binaryauthorization.v1beta1.Attestor]
                ID.

                This corresponds to the ``attestor_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attestor (google.cloud.binaryauthorization_v1beta1.types.Attestor):
                Required. The initial
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
                value. The service will overwrite the [attestor
                name][google.cloud.binaryauthorization.v1beta1.Attestor.name]
                field with the resource name, in the format
                ``projects/*/attestors/*``.

                This corresponds to the ``attestor`` field
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
            google.cloud.binaryauthorization_v1beta1.types.Attestor:
                An [attestor][google.cloud.binaryauthorization.v1beta1.Attestor] that attests to container image
                   artifacts. An existing attestor cannot be modified
                   except where indicated.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, attestor_id, attestor])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, service.CreateAttestorRequest):
            request = service.CreateAttestorRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if attestor_id is not None:
                request.attestor_id = attestor_id
            if attestor is not None:
                request.attestor = attestor

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_attestor]

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

    def get_attestor(
        self,
        request: Optional[Union[service.GetAttestorRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> resources.Attestor:
        r"""Gets an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        does not exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_get_attestor():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                request = binaryauthorization_v1beta1.GetAttestorRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_attestor(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.GetAttestorRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.GetAttestor][].
            name (str):
                Required. The name of the
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
                to retrieve, in the format ``projects/*/attestors/*``.

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
            google.cloud.binaryauthorization_v1beta1.types.Attestor:
                An [attestor][google.cloud.binaryauthorization.v1beta1.Attestor] that attests to container image
                   artifacts. An existing attestor cannot be modified
                   except where indicated.

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
        if not isinstance(request, service.GetAttestorRequest):
            request = service.GetAttestorRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_attestor]

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

    def update_attestor(
        self,
        request: Optional[Union[service.UpdateAttestorRequest, dict]] = None,
        *,
        attestor: Optional[resources.Attestor] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> resources.Attestor:
        r"""Updates an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        does not exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_update_attestor():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                attestor = binaryauthorization_v1beta1.Attestor()
                attestor.user_owned_drydock_note.note_reference = "note_reference_value"
                attestor.name = "name_value"

                request = binaryauthorization_v1beta1.UpdateAttestorRequest(
                    attestor=attestor,
                )

                # Make the request
                response = client.update_attestor(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.UpdateAttestorRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.UpdateAttestor][].
            attestor (google.cloud.binaryauthorization_v1beta1.types.Attestor):
                Required. The updated
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
                value. The service will overwrite the [attestor
                name][google.cloud.binaryauthorization.v1beta1.Attestor.name]
                field with the resource name in the request URL, in the
                format ``projects/*/attestors/*``.

                This corresponds to the ``attestor`` field
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
            google.cloud.binaryauthorization_v1beta1.types.Attestor:
                An [attestor][google.cloud.binaryauthorization.v1beta1.Attestor] that attests to container image
                   artifacts. An existing attestor cannot be modified
                   except where indicated.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([attestor])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, service.UpdateAttestorRequest):
            request = service.UpdateAttestorRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if attestor is not None:
                request.attestor = attestor

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_attestor]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attestor.name", request.attestor.name),)
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

    def list_attestors(
        self,
        request: Optional[Union[service.ListAttestorsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAttestorsPager:
        r"""Lists
        [attestors][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns INVALID_ARGUMENT if the project does not exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_list_attestors():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                request = binaryauthorization_v1beta1.ListAttestorsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_attestors(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.ListAttestorsRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.ListAttestors][].
            parent (str):
                Required. The resource name of the project associated
                with the
                [attestors][google.cloud.binaryauthorization.v1beta1.Attestor],
                in the format ``projects/*``.

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
            google.cloud.binaryauthorization_v1beta1.services.binauthz_management_service_v1_beta1.pagers.ListAttestorsPager:
                Response message for
                [BinauthzManagementService.ListAttestors][].

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
        if not isinstance(request, service.ListAttestorsRequest):
            request = service.ListAttestorsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_attestors]

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
        response = pagers.ListAttestorsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_attestor(
        self,
        request: Optional[Union[service.DeleteAttestorRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        does not exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1beta1

            def sample_delete_attestor():
                # Create a client
                client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

                # Initialize request argument(s)
                request = binaryauthorization_v1beta1.DeleteAttestorRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_attestor(request=request)

        Args:
            request (Union[google.cloud.binaryauthorization_v1beta1.types.DeleteAttestorRequest, dict]):
                The request object. Request message for
                [BinauthzManagementService.DeleteAttestor][].
            name (str):
                Required. The name of the
                [attestors][google.cloud.binaryauthorization.v1beta1.Attestor]
                to delete, in the format ``projects/*/attestors/*``.

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
        if not isinstance(request, service.DeleteAttestorRequest):
            request = service.DeleteAttestorRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_attestor]

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

    def __enter__(self) -> "BinauthzManagementServiceV1Beta1Client":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("BinauthzManagementServiceV1Beta1Client",)
