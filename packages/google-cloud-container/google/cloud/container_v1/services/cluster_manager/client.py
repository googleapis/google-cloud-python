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

from google.cloud.container_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.rpc import status_pb2  # type: ignore

from google.cloud.container_v1.services.cluster_manager import pagers
from google.cloud.container_v1.types import cluster_service

from .transports.base import DEFAULT_CLIENT_INFO, ClusterManagerTransport
from .transports.grpc import ClusterManagerGrpcTransport
from .transports.grpc_asyncio import ClusterManagerGrpcAsyncIOTransport
from .transports.rest import ClusterManagerRestTransport


class ClusterManagerClientMeta(type):
    """Metaclass for the ClusterManager client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ClusterManagerTransport]]
    _transport_registry["grpc"] = ClusterManagerGrpcTransport
    _transport_registry["grpc_asyncio"] = ClusterManagerGrpcAsyncIOTransport
    _transport_registry["rest"] = ClusterManagerRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ClusterManagerTransport]:
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


class ClusterManagerClient(metaclass=ClusterManagerClientMeta):
    """Google Kubernetes Engine Cluster Manager v1"""

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
    DEFAULT_ENDPOINT = "container.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "container.{UNIVERSE_DOMAIN}"
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
            ClusterManagerClient: The constructed client.
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
            ClusterManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ClusterManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            ClusterManagerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def ca_pool_path(
        project: str,
        location: str,
        ca_pool: str,
    ) -> str:
        """Returns a fully-qualified ca_pool string."""
        return "projects/{project}/locations/{location}/caPools/{ca_pool}".format(
            project=project,
            location=location,
            ca_pool=ca_pool,
        )

    @staticmethod
    def parse_ca_pool_path(path: str) -> Dict[str, str]:
        """Parses a ca_pool path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/caPools/(?P<ca_pool>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_version_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
        crypto_key_version: str,
    ) -> str:
        """Returns a fully-qualified crypto_key_version string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
            crypto_key_version=crypto_key_version,
        )

    @staticmethod
    def parse_crypto_key_version_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)/cryptoKeyVersions/(?P<crypto_key_version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def topic_path(
        project: str,
        topic: str,
    ) -> str:
        """Returns a fully-qualified topic string."""
        return "projects/{project}/topics/{topic}".format(
            project=project,
            topic=topic,
        )

    @staticmethod
    def parse_topic_path(path: str) -> Dict[str, str]:
        """Parses a topic path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/topics/(?P<topic>.+?)$", path)
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
            _default_universe = ClusterManagerClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = ClusterManagerClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = ClusterManagerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = ClusterManagerClient._DEFAULT_UNIVERSE
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
            Union[str, ClusterManagerTransport, Callable[..., ClusterManagerTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cluster manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ClusterManagerTransport,Callable[..., ClusterManagerTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ClusterManagerTransport constructor.
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
        ) = ClusterManagerClient._read_environment_variables()
        self._client_cert_source = ClusterManagerClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = ClusterManagerClient._get_universe_domain(
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
        transport_provided = isinstance(transport, ClusterManagerTransport)
        if transport_provided:
            # transport is a ClusterManagerTransport instance.
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
            self._transport = cast(ClusterManagerTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or ClusterManagerClient._get_api_endpoint(
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
                Type[ClusterManagerTransport], Callable[..., ClusterManagerTransport]
            ] = (
                ClusterManagerClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., ClusterManagerTransport], transport)
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

    def list_clusters(
        self,
        request: Optional[Union[cluster_service.ListClustersRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.ListClustersResponse:
        r"""Lists all clusters owned by a project in either the
        specified zone or all zones.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_list_clusters():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.ListClustersRequest(
                )

                # Make the request
                response = client.list_clusters(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.ListClustersRequest, dict]):
                The request object. ListClustersRequest lists clusters.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the
                parent field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides, or "-" for all zones. This
                field has been deprecated and replaced by the parent
                field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (str):
                The parent (project and location) where the clusters
                will be listed. Specified in the format
                ``projects/*/locations/*``. Location "-" matches all
                zones and all regions.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.ListClustersResponse:
                ListClustersResponse is the result of
                ListClustersRequest.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.ListClustersRequest):
            request = cluster_service.ListClustersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_clusters]

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

    def get_cluster(
        self,
        request: Optional[Union[cluster_service.GetClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Cluster:
        r"""Gets the details of a specific cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_get_cluster():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.GetClusterRequest(
                )

                # Make the request
                response = client.get_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.GetClusterRequest, dict]):
                The request object. GetClusterRequest gets the settings
                of a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to retrieve. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                retrieve. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Cluster:
                A Google Kubernetes Engine cluster.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.GetClusterRequest):
            request = cluster_service.GetClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_cluster]

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

    def create_cluster(
        self,
        request: Optional[Union[cluster_service.CreateClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster: Optional[cluster_service.Cluster] = None,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Creates a cluster, consisting of the specified number and type
        of Google Compute Engine instances.

        By default, the cluster is created in the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        One firewall is added for the cluster. After cluster creation,
        the Kubelet creates routes for each node to allow the containers
        on that node to communicate with all other instances in the
        cluster.

        Finally, an entry is added to the project's global metadata
        indicating which CIDR range the cluster is using.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_create_cluster():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.CreateClusterRequest(
                )

                # Make the request
                response = client.create_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.CreateClusterRequest, dict]):
                The request object. CreateClusterRequest creates a
                cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the
                parent field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the parent field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (google.cloud.container_v1.types.Cluster):
                Required. A `cluster
                resource <https://cloud.google.com/container-engine/reference/rest/v1/projects.locations.clusters>`__

                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (str):
                The parent (project and location) where the cluster will
                be created. Specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster, parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.CreateClusterRequest):
            request = cluster_service.CreateClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster is not None:
                request.cluster = cluster
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_cluster]

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

    def update_cluster(
        self,
        request: Optional[Union[cluster_service.UpdateClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        update: Optional[cluster_service.ClusterUpdate] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Updates the settings of a specific cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_update_cluster():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.UpdateClusterRequest(
                )

                # Make the request
                response = client.update_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.UpdateClusterRequest, dict]):
                The request object. UpdateClusterRequest updates the
                settings of a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update (google.cloud.container_v1.types.ClusterUpdate):
                Required. A description of the
                update.

                This corresponds to the ``update`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                update. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, update, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.UpdateClusterRequest):
            request = cluster_service.UpdateClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if update is not None:
                request.update = update
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_cluster]

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

    def update_node_pool(
        self,
        request: Optional[Union[cluster_service.UpdateNodePoolRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Updates the version and/or image type for the
        specified node pool.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_update_node_pool():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.UpdateNodePoolRequest(
                    node_version="node_version_value",
                    image_type="image_type_value",
                )

                # Make the request
                response = client.update_node_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.UpdateNodePoolRequest, dict]):
                The request object. UpdateNodePoolRequests update a node
                pool's image and/or version.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.UpdateNodePoolRequest):
            request = cluster_service.UpdateNodePoolRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_node_pool]

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

    def set_node_pool_autoscaling(
        self,
        request: Optional[
            Union[cluster_service.SetNodePoolAutoscalingRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the autoscaling settings for the specified node
        pool.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_node_pool_autoscaling():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetNodePoolAutoscalingRequest(
                )

                # Make the request
                response = client.set_node_pool_autoscaling(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetNodePoolAutoscalingRequest, dict]):
                The request object. SetNodePoolAutoscalingRequest sets
                the autoscaler settings of a node pool.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetNodePoolAutoscalingRequest):
            request = cluster_service.SetNodePoolAutoscalingRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.set_node_pool_autoscaling
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

    def set_logging_service(
        self,
        request: Optional[Union[cluster_service.SetLoggingServiceRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        logging_service: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the logging service for a specific cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_logging_service():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetLoggingServiceRequest(
                    logging_service="logging_service_value",
                )

                # Make the request
                response = client.set_logging_service(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetLoggingServiceRequest, dict]):
                The request object. SetLoggingServiceRequest sets the
                logging service of a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            logging_service (str):
                Required. The logging service the cluster should use to
                write logs. Currently available options:

                -  ``logging.googleapis.com/kubernetes`` - The Cloud
                   Logging service with a Kubernetes-native resource
                   model
                -  ``logging.googleapis.com`` - The legacy Cloud Logging
                   service (no longer available as of GKE 1.15).
                -  ``none`` - no logs will be exported from the cluster.

                If left as an empty
                string,\ ``logging.googleapis.com/kubernetes`` will be
                used for GKE 1.14+ or ``logging.googleapis.com`` for
                earlier versions.

                This corresponds to the ``logging_service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                set logging. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project_id, zone, cluster_id, logging_service, name]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetLoggingServiceRequest):
            request = cluster_service.SetLoggingServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if logging_service is not None:
                request.logging_service = logging_service
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_logging_service]

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

    def set_monitoring_service(
        self,
        request: Optional[
            Union[cluster_service.SetMonitoringServiceRequest, dict]
        ] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        monitoring_service: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the monitoring service for a specific cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_monitoring_service():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetMonitoringServiceRequest(
                    monitoring_service="monitoring_service_value",
                )

                # Make the request
                response = client.set_monitoring_service(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetMonitoringServiceRequest, dict]):
                The request object. SetMonitoringServiceRequest sets the
                monitoring service of a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            monitoring_service (str):
                Required. The monitoring service the cluster should use
                to write metrics. Currently available options:

                -  "monitoring.googleapis.com/kubernetes" - The Cloud
                   Monitoring service with a Kubernetes-native resource
                   model
                -  ``monitoring.googleapis.com`` - The legacy Cloud
                   Monitoring service (no longer available as of GKE
                   1.15).
                -  ``none`` - No metrics will be exported from the
                   cluster.

                If left as an empty
                string,\ ``monitoring.googleapis.com/kubernetes`` will
                be used for GKE 1.14+ or ``monitoring.googleapis.com``
                for earlier versions.

                This corresponds to the ``monitoring_service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                set monitoring. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project_id, zone, cluster_id, monitoring_service, name]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetMonitoringServiceRequest):
            request = cluster_service.SetMonitoringServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if monitoring_service is not None:
                request.monitoring_service = monitoring_service
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_monitoring_service]

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

    def set_addons_config(
        self,
        request: Optional[Union[cluster_service.SetAddonsConfigRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        addons_config: Optional[cluster_service.AddonsConfig] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the addons for a specific cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_addons_config():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetAddonsConfigRequest(
                )

                # Make the request
                response = client.set_addons_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetAddonsConfigRequest, dict]):
                The request object. SetAddonsConfigRequest sets the
                addons associated with the cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            addons_config (google.cloud.container_v1.types.AddonsConfig):
                Required. The desired configurations
                for the various addons available to run
                in the cluster.

                This corresponds to the ``addons_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                set addons. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, addons_config, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetAddonsConfigRequest):
            request = cluster_service.SetAddonsConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if addons_config is not None:
                request.addons_config = addons_config
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_addons_config]

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

    def set_locations(
        self,
        request: Optional[Union[cluster_service.SetLocationsRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        locations: Optional[MutableSequence[str]] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the locations for a specific cluster. Deprecated. Use
        `projects.locations.clusters.update <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters/update>`__
        instead.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_locations():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetLocationsRequest(
                    locations=['locations_value1', 'locations_value2'],
                )

                # Make the request
                response = client.set_locations(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetLocationsRequest, dict]):
                The request object. SetLocationsRequest sets the
                locations of the cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            locations (MutableSequence[str]):
                Required. The desired list of Google Compute Engine
                `zones <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster's nodes should be located. Changing
                the locations a cluster is in will result in nodes being
                either created or removed from the cluster, depending on
                whether locations are being added or removed.

                This list must always include the cluster's primary
                zone.

                This corresponds to the ``locations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                set locations. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        warnings.warn(
            "ClusterManagerClient.set_locations is deprecated", DeprecationWarning
        )

        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, locations, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetLocationsRequest):
            request = cluster_service.SetLocationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if locations is not None:
                request.locations = locations
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_locations]

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

    def update_master(
        self,
        request: Optional[Union[cluster_service.UpdateMasterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        master_version: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Updates the master for a specific cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_update_master():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.UpdateMasterRequest(
                    master_version="master_version_value",
                )

                # Make the request
                response = client.update_master(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.UpdateMasterRequest, dict]):
                The request object. UpdateMasterRequest updates the
                master of the cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            master_version (str):
                Required. The Kubernetes version to
                change the master to.
                Users may specify either explicit
                versions offered by Kubernetes Engine or
                version aliases, which have the
                following behavior:

                - "latest": picks the highest valid
                  Kubernetes version
                - "1.X": picks the highest valid
                  patch+gke.N patch in the 1.X version
                - "1.X.Y": picks the highest valid gke.N
                  patch in the 1.X.Y version
                - "1.X.Y-gke.N": picks an explicit
                  Kubernetes version
                - "-": picks the default Kubernetes
                  version

                This corresponds to the ``master_version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                update. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, master_version, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.UpdateMasterRequest):
            request = cluster_service.UpdateMasterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if master_version is not None:
                request.master_version = master_version
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_master]

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

    def set_master_auth(
        self,
        request: Optional[Union[cluster_service.SetMasterAuthRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets master auth materials. Currently supports
        changing the admin password or a specific cluster,
        either via password generation or explicitly setting the
        password.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_master_auth():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetMasterAuthRequest(
                    action="SET_USERNAME",
                )

                # Make the request
                response = client.set_master_auth(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetMasterAuthRequest, dict]):
                The request object. SetMasterAuthRequest updates the
                admin password of a cluster.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetMasterAuthRequest):
            request = cluster_service.SetMasterAuthRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_master_auth]

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

    def delete_cluster(
        self,
        request: Optional[Union[cluster_service.DeleteClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Deletes the cluster, including the Kubernetes
        endpoint and all worker nodes.

        Firewalls and routes that were configured during cluster
        creation are also deleted.

        Other Google Compute Engine resources that might be in
        use by the cluster, such as load balancer resources, are
        not deleted if they weren't present when the cluster was
        initially created.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_delete_cluster():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.DeleteClusterRequest(
                )

                # Make the request
                response = client.delete_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.DeleteClusterRequest, dict]):
                The request object. DeleteClusterRequest deletes a
                cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to delete. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster) of the cluster to
                delete. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.DeleteClusterRequest):
            request = cluster_service.DeleteClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_cluster]

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

    def list_operations(
        self,
        request: Optional[Union[cluster_service.ListOperationsRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.ListOperationsResponse:
        r"""Lists all operations in a project in a specific zone
        or all zones.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_list_operations():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.ListOperationsRequest(
                )

                # Make the request
                response = client.list_operations(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.ListOperationsRequest, dict]):
                The request object. ListOperationsRequest lists
                operations.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the
                parent field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                to return operations for, or ``-`` for all zones. This
                field has been deprecated and replaced by the parent
                field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (str):
                The parent (project and location) where the operations
                will be listed. Specified in the format
                ``projects/*/locations/*``. Location "-" matches all
                zones and all regions.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.ListOperationsResponse:
                ListOperationsResponse is the result
                of ListOperationsRequest.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.ListOperationsRequest):
            request = cluster_service.ListOperationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_operations]

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

    def get_operation(
        self,
        request: Optional[Union[cluster_service.GetOperationRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        operation_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Gets the specified operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_get_operation():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.GetOperationRequest(
                )

                # Make the request
                response = client.get_operation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.GetOperationRequest, dict]):
                The request object. GetOperationRequest gets a single
                operation.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operation_id (str):
                Deprecated. The server-assigned ``name`` of the
                operation. This field has been deprecated and replaced
                by the name field.

                This corresponds to the ``operation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, operation id) of the
                operation to get. Specified in the format
                ``projects/*/locations/*/operations/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, operation_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.GetOperationRequest):
            request = cluster_service.GetOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if operation_id is not None:
                request.operation_id = operation_id
            if name is not None:
                request.name = name

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

    def cancel_operation(
        self,
        request: Optional[Union[cluster_service.CancelOperationRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        operation_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Cancels the specified operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_cancel_operation():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.CancelOperationRequest(
                )

                # Make the request
                client.cancel_operation(request=request)

        Args:
            request (Union[google.cloud.container_v1.types.CancelOperationRequest, dict]):
                The request object. CancelOperationRequest cancels a
                single operation.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the operation resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operation_id (str):
                Deprecated. The server-assigned ``name`` of the
                operation. This field has been deprecated and replaced
                by the name field.

                This corresponds to the ``operation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, operation id) of the
                operation to cancel. Specified in the format
                ``projects/*/locations/*/operations/*``.

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
        has_flattened_params = any([project_id, zone, operation_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.CancelOperationRequest):
            request = cluster_service.CancelOperationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if operation_id is not None:
                request.operation_id = operation_id
            if name is not None:
                request.name = name

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

    def get_server_config(
        self,
        request: Optional[Union[cluster_service.GetServerConfigRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.ServerConfig:
        r"""Returns configuration info about the Google
        Kubernetes Engine service.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_get_server_config():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.GetServerConfigRequest(
                )

                # Make the request
                response = client.get_server_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.GetServerConfigRequest, dict]):
                The request object. Gets the current Kubernetes Engine
                service configuration.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                to return operations for. This field has been deprecated
                and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project and location) of the server config to
                get, specified in the format ``projects/*/locations/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.ServerConfig:
                Kubernetes Engine service
                configuration.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.GetServerConfigRequest):
            request = cluster_service.GetServerConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_server_config]

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

    def get_json_web_keys(
        self,
        request: Optional[Union[cluster_service.GetJSONWebKeysRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.GetJSONWebKeysResponse:
        r"""Gets the public component of the cluster signing keys
        in JSON Web Key format.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_get_json_web_keys():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.GetJSONWebKeysRequest(
                )

                # Make the request
                response = client.get_json_web_keys(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.GetJSONWebKeysRequest, dict]):
                The request object. GetJSONWebKeysRequest gets the public component of the
                keys used by the cluster to sign token requests. This
                will be the jwks_uri for the discover document returned
                by getOpenIDConfig. See the OpenID Connect Discovery 1.0
                specification for details.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.GetJSONWebKeysResponse:
                GetJSONWebKeysResponse is a valid
                JSON Web Key Set as specififed in rfc
                7517

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.GetJSONWebKeysRequest):
            request = cluster_service.GetJSONWebKeysRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_json_web_keys]

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

    def list_node_pools(
        self,
        request: Optional[Union[cluster_service.ListNodePoolsRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.ListNodePoolsResponse:
        r"""Lists the node pools for a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_list_node_pools():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.ListNodePoolsRequest(
                )

                # Make the request
                response = client.list_node_pools(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.ListNodePoolsRequest, dict]):
                The request object. ListNodePoolsRequest lists the node
                pool(s) for a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the
                parent field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the parent field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the parent field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (str):
                The parent (project, location, cluster name) where the
                node pools will be listed. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.ListNodePoolsResponse:
                ListNodePoolsResponse is the result
                of ListNodePoolsRequest.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.ListNodePoolsRequest):
            request = cluster_service.ListNodePoolsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_node_pools]

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

    def get_node_pool(
        self,
        request: Optional[Union[cluster_service.GetNodePoolRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        node_pool_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.NodePool:
        r"""Retrieves the requested node pool.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_get_node_pool():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.GetNodePoolRequest(
                )

                # Make the request
                response = client.get_node_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.GetNodePoolRequest, dict]):
                The request object. GetNodePoolRequest retrieves a node
                pool for a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool_id (str):
                Deprecated. The name of the node
                pool. This field has been deprecated and
                replaced by the name field.

                This corresponds to the ``node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster, node pool id) of
                the node pool to get. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.NodePool:
                NodePool contains the name and
                configuration for a cluster's node pool.
                Node pools are a set of nodes (i.e.
                VM's), with a common configuration and
                specification, under the control of the
                cluster master. They may have a set of
                Kubernetes labels applied to them, which
                may be used to reference them during pod
                scheduling. They may also be resized up
                or down, to accommodate the workload.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, node_pool_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.GetNodePoolRequest):
            request = cluster_service.GetNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if node_pool_id is not None:
                request.node_pool_id = node_pool_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_node_pool]

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

    def create_node_pool(
        self,
        request: Optional[Union[cluster_service.CreateNodePoolRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        node_pool: Optional[cluster_service.NodePool] = None,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Creates a node pool for a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_create_node_pool():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.CreateNodePoolRequest(
                )

                # Make the request
                response = client.create_node_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.CreateNodePoolRequest, dict]):
                The request object. CreateNodePoolRequest creates a node
                pool for a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the
                parent field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the parent field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the parent field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool (google.cloud.container_v1.types.NodePool):
                Required. The node pool to create.
                This corresponds to the ``node_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (str):
                The parent (project, location, cluster name) where the
                node pool will be created. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, node_pool, parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.CreateNodePoolRequest):
            request = cluster_service.CreateNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if node_pool is not None:
                request.node_pool = node_pool
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_node_pool]

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

    def delete_node_pool(
        self,
        request: Optional[Union[cluster_service.DeleteNodePoolRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        node_pool_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Deletes a node pool from a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_delete_node_pool():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.DeleteNodePoolRequest(
                )

                # Make the request
                response = client.delete_node_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.DeleteNodePoolRequest, dict]):
                The request object. DeleteNodePoolRequest deletes a node
                pool for a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool_id (str):
                Deprecated. The name of the node pool
                to delete. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster, node pool id) of
                the node pool to delete. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, node_pool_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.DeleteNodePoolRequest):
            request = cluster_service.DeleteNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if node_pool_id is not None:
                request.node_pool_id = node_pool_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_node_pool]

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

    def complete_node_pool_upgrade(
        self,
        request: Optional[
            Union[cluster_service.CompleteNodePoolUpgradeRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""CompleteNodePoolUpgrade will signal an on-going node
        pool upgrade to complete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_complete_node_pool_upgrade():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.CompleteNodePoolUpgradeRequest(
                )

                # Make the request
                client.complete_node_pool_upgrade(request=request)

        Args:
            request (Union[google.cloud.container_v1.types.CompleteNodePoolUpgradeRequest, dict]):
                The request object. CompleteNodePoolUpgradeRequest sets
                the name of target node pool to complete
                upgrade.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.CompleteNodePoolUpgradeRequest):
            request = cluster_service.CompleteNodePoolUpgradeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.complete_node_pool_upgrade
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

    def rollback_node_pool_upgrade(
        self,
        request: Optional[
            Union[cluster_service.RollbackNodePoolUpgradeRequest, dict]
        ] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        node_pool_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Rolls back a previously Aborted or Failed NodePool
        upgrade. This makes no changes if the last upgrade
        successfully completed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_rollback_node_pool_upgrade():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.RollbackNodePoolUpgradeRequest(
                )

                # Make the request
                response = client.rollback_node_pool_upgrade(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.RollbackNodePoolUpgradeRequest, dict]):
                The request object. RollbackNodePoolUpgradeRequest
                rollbacks the previously Aborted or
                Failed NodePool upgrade. This will be an
                no-op if the last upgrade successfully
                completed.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to rollback. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool_id (str):
                Deprecated. The name of the node pool
                to rollback. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster, node pool id) of
                the node poll to rollback upgrade. Specified in the
                format
                ``projects/*/locations/*/clusters/*/nodePools/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, node_pool_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.RollbackNodePoolUpgradeRequest):
            request = cluster_service.RollbackNodePoolUpgradeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if node_pool_id is not None:
                request.node_pool_id = node_pool_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.rollback_node_pool_upgrade
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

    def set_node_pool_management(
        self,
        request: Optional[
            Union[cluster_service.SetNodePoolManagementRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the NodeManagement options for a node pool.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_node_pool_management():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetNodePoolManagementRequest(
                )

                # Make the request
                response = client.set_node_pool_management(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetNodePoolManagementRequest, dict]):
                The request object. SetNodePoolManagementRequest sets the
                node management properties of a node
                pool.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetNodePoolManagementRequest):
            request = cluster_service.SetNodePoolManagementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_node_pool_management]

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

    def set_labels(
        self,
        request: Optional[Union[cluster_service.SetLabelsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets labels on a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_labels():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetLabelsRequest(
                    label_fingerprint="label_fingerprint_value",
                )

                # Make the request
                response = client.set_labels(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetLabelsRequest, dict]):
                The request object. SetLabelsRequest sets the Google
                Cloud Platform labels on a Google
                Container Engine cluster, which will in
                turn set them for Google Compute Engine
                resources used by that cluster
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetLabelsRequest):
            request = cluster_service.SetLabelsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_labels]

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

    def set_legacy_abac(
        self,
        request: Optional[Union[cluster_service.SetLegacyAbacRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        enabled: Optional[bool] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Enables or disables the ABAC authorization mechanism
        on a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_legacy_abac():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetLegacyAbacRequest(
                    enabled=True,
                )

                # Make the request
                response = client.set_legacy_abac(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetLegacyAbacRequest, dict]):
                The request object. SetLegacyAbacRequest enables or
                disables the ABAC authorization
                mechanism for a cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster
                to update. This field has been
                deprecated and replaced by the name
                field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            enabled (bool):
                Required. Whether ABAC authorization
                will be enabled in the cluster.

                This corresponds to the ``enabled`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster name) of the
                cluster to set legacy abac. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, enabled, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetLegacyAbacRequest):
            request = cluster_service.SetLegacyAbacRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if enabled is not None:
                request.enabled = enabled
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_legacy_abac]

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

    def start_ip_rotation(
        self,
        request: Optional[Union[cluster_service.StartIPRotationRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Starts master IP rotation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_start_ip_rotation():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.StartIPRotationRequest(
                )

                # Make the request
                response = client.start_ip_rotation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.StartIPRotationRequest, dict]):
                The request object. StartIPRotationRequest creates a new
                IP for the cluster and then performs a
                node upgrade on each node pool to point
                to the new IP.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster name) of the
                cluster to start IP rotation. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.StartIPRotationRequest):
            request = cluster_service.StartIPRotationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_ip_rotation]

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

    def complete_ip_rotation(
        self,
        request: Optional[
            Union[cluster_service.CompleteIPRotationRequest, dict]
        ] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Completes master IP rotation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_complete_ip_rotation():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.CompleteIPRotationRequest(
                )

                # Make the request
                response = client.complete_ip_rotation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.CompleteIPRotationRequest, dict]):
                The request object. CompleteIPRotationRequest moves the
                cluster master back into single-IP mode.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster name) of the
                cluster to complete IP rotation. Specified in the format
                ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.CompleteIPRotationRequest):
            request = cluster_service.CompleteIPRotationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.complete_ip_rotation]

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

    def set_node_pool_size(
        self,
        request: Optional[Union[cluster_service.SetNodePoolSizeRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the size for a specific node pool. The new size will be
        used for all replicas, including future replicas created by
        modifying
        [NodePool.locations][google.container.v1.NodePool.locations].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_node_pool_size():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetNodePoolSizeRequest(
                    node_count=1070,
                )

                # Make the request
                response = client.set_node_pool_size(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetNodePoolSizeRequest, dict]):
                The request object. SetNodePoolSizeRequest sets the size
                of a node pool.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetNodePoolSizeRequest):
            request = cluster_service.SetNodePoolSizeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_node_pool_size]

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

    def set_network_policy(
        self,
        request: Optional[Union[cluster_service.SetNetworkPolicyRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        network_policy: Optional[cluster_service.NetworkPolicy] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Enables or disables Network Policy for a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_network_policy():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetNetworkPolicyRequest(
                )

                # Make the request
                response = client.set_network_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetNetworkPolicyRequest, dict]):
                The request object. SetNetworkPolicyRequest
                enables/disables network policy for a
                cluster.
            project_id (str):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
                This field has been deprecated and replaced by the name
                field.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_policy (google.cloud.container_v1.types.NetworkPolicy):
                Required. Configuration options for
                the NetworkPolicy feature.

                This corresponds to the ``network_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster name) of the
                cluster to set networking policy. Specified in the
                format ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, zone, cluster_id, network_policy, name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetNetworkPolicyRequest):
            request = cluster_service.SetNetworkPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if network_policy is not None:
                request.network_policy = network_policy
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_network_policy]

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

    def set_maintenance_policy(
        self,
        request: Optional[
            Union[cluster_service.SetMaintenancePolicyRequest, dict]
        ] = None,
        *,
        project_id: Optional[str] = None,
        zone: Optional[str] = None,
        cluster_id: Optional[str] = None,
        maintenance_policy: Optional[cluster_service.MaintenancePolicy] = None,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.Operation:
        r"""Sets the maintenance policy for a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_set_maintenance_policy():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.SetMaintenancePolicyRequest(
                    project_id="project_id_value",
                    zone="zone_value",
                    cluster_id="cluster_id_value",
                )

                # Make the request
                response = client.set_maintenance_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.SetMaintenancePolicyRequest, dict]):
                The request object. SetMaintenancePolicyRequest sets the
                maintenance policy for a cluster.
            project_id (str):
                Required. The Google Developers Console `project ID or
                project
                number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                Required. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (str):
                Required. The name of the cluster to
                update.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            maintenance_policy (google.cloud.container_v1.types.MaintenancePolicy):
                Required. The maintenance policy to
                be set for the cluster. An empty field
                clears the existing maintenance policy.

                This corresponds to the ``maintenance_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (str):
                The name (project, location, cluster name) of the
                cluster to set maintenance policy. Specified in the
                format ``projects/*/locations/*/clusters/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project_id, zone, cluster_id, maintenance_policy, name]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.SetMaintenancePolicyRequest):
            request = cluster_service.SetMaintenancePolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if zone is not None:
                request.zone = zone
            if cluster_id is not None:
                request.cluster_id = cluster_id
            if maintenance_policy is not None:
                request.maintenance_policy = maintenance_policy
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_maintenance_policy]

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

    def list_usable_subnetworks(
        self,
        request: Optional[
            Union[cluster_service.ListUsableSubnetworksRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListUsableSubnetworksPager:
        r"""Lists subnetworks that are usable for creating
        clusters in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_list_usable_subnetworks():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.ListUsableSubnetworksRequest(
                )

                # Make the request
                page_result = client.list_usable_subnetworks(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.container_v1.types.ListUsableSubnetworksRequest, dict]):
                The request object. ListUsableSubnetworksRequest requests
                the list of usable subnetworks available
                to a user for creating clusters.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.services.cluster_manager.pagers.ListUsableSubnetworksPager:
                ListUsableSubnetworksResponse is the
                response of
                ListUsableSubnetworksRequest.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.ListUsableSubnetworksRequest):
            request = cluster_service.ListUsableSubnetworksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_usable_subnetworks]

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
        response = pagers.ListUsableSubnetworksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def check_autopilot_compatibility(
        self,
        request: Optional[
            Union[cluster_service.CheckAutopilotCompatibilityRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.CheckAutopilotCompatibilityResponse:
        r"""Checks the cluster compatibility with Autopilot mode,
        and returns a list of compatibility issues.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import container_v1

            def sample_check_autopilot_compatibility():
                # Create a client
                client = container_v1.ClusterManagerClient()

                # Initialize request argument(s)
                request = container_v1.CheckAutopilotCompatibilityRequest(
                )

                # Make the request
                response = client.check_autopilot_compatibility(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.container_v1.types.CheckAutopilotCompatibilityRequest, dict]):
                The request object. CheckAutopilotCompatibilityRequest
                requests getting the blockers for the
                given operation in the cluster.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.container_v1.types.CheckAutopilotCompatibilityResponse:
                CheckAutopilotCompatibilityResponse
                has a list of compatibility issues.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cluster_service.CheckAutopilotCompatibilityRequest):
            request = cluster_service.CheckAutopilotCompatibilityRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.check_autopilot_compatibility
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

    def __enter__(self) -> "ClusterManagerClient":
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


__all__ = ("ClusterManagerClient",)
