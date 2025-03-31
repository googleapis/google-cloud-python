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
from typing import Dict, Callable, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Tuple, Type, Union, cast
import warnings

from google.iam_v1beta import gapic_version as package_version

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials             # type: ignore
from google.auth.transport import mtls                            # type: ignore
from google.auth.transport.grpc import SslCredentials             # type: ignore
from google.auth.exceptions import MutualTLSChannelError          # type: ignore
from google.oauth2 import service_account                         # type: ignore

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
from google.iam_v1beta.services.workload_identity_pools import pagers
from google.iam_v1beta.types import workload_identity_pool
from google.iam_v1beta.types import workload_identity_pool as gi_workload_identity_pool
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import WorkloadIdentityPoolsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import WorkloadIdentityPoolsGrpcTransport
from .transports.grpc_asyncio import WorkloadIdentityPoolsGrpcAsyncIOTransport


class WorkloadIdentityPoolsClientMeta(type):
    """Metaclass for the WorkloadIdentityPools client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[WorkloadIdentityPoolsTransport]]
    _transport_registry["grpc"] = WorkloadIdentityPoolsGrpcTransport
    _transport_registry["grpc_asyncio"] = WorkloadIdentityPoolsGrpcAsyncIOTransport

    def get_transport_class(cls,
            label: Optional[str] = None,
        ) -> Type[WorkloadIdentityPoolsTransport]:
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


class WorkloadIdentityPoolsClient(metaclass=WorkloadIdentityPoolsClientMeta):
    """Manages WorkloadIdentityPools."""

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
    DEFAULT_ENDPOINT = "iam.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "iam.{UNIVERSE_DOMAIN}"
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
            WorkloadIdentityPoolsClient: The constructed client.
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
            WorkloadIdentityPoolsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> WorkloadIdentityPoolsTransport:
        """Returns the transport used by the client instance.

        Returns:
            WorkloadIdentityPoolsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def workload_identity_pool_path(project: str,location: str,workload_identity_pool: str,) -> str:
        """Returns a fully-qualified workload_identity_pool string."""
        return "projects/{project}/locations/{location}/workloadIdentityPools/{workload_identity_pool}".format(project=project, location=location, workload_identity_pool=workload_identity_pool, )

    @staticmethod
    def parse_workload_identity_pool_path(path: str) -> Dict[str,str]:
        """Parses a workload_identity_pool path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/workloadIdentityPools/(?P<workload_identity_pool>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def workload_identity_pool_provider_path(project: str,location: str,workload_identity_pool: str,workload_identity_pool_provider: str,) -> str:
        """Returns a fully-qualified workload_identity_pool_provider string."""
        return "projects/{project}/locations/{location}/workloadIdentityPools/{workload_identity_pool}/providers/{workload_identity_pool_provider}".format(project=project, location=location, workload_identity_pool=workload_identity_pool, workload_identity_pool_provider=workload_identity_pool_provider, )

    @staticmethod
    def parse_workload_identity_pool_provider_path(path: str) -> Dict[str,str]:
        """Parses a workload_identity_pool_provider path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/workloadIdentityPools/(?P<workload_identity_pool>.+?)/providers/(?P<workload_identity_pool_provider>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str, ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(billing_account=billing_account, )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str,str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str, ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder, )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str,str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str, ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization, )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str,str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str, ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project, )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str,str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str, ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(project=project, location=location, )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str,str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[client_options_lib.ClientOptions] = None):
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

        warnings.warn("get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")

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
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
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
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false").lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")
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
    def _get_api_endpoint(api_override, client_cert_source, universe_domain, use_mtls_endpoint):
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
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
            _default_universe = WorkloadIdentityPoolsClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(f"mTLS is not supported in any universe other than {_default_universe}.")
            api_endpoint = WorkloadIdentityPoolsClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = WorkloadIdentityPoolsClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=universe_domain)
        return api_endpoint

    @staticmethod
    def _get_universe_domain(client_universe_domain: Optional[str], universe_domain_env: Optional[str]) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = WorkloadIdentityPoolsClient._DEFAULT_UNIVERSE
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
        self,
        error: core_exceptions.GoogleAPICallError
    ) -> None:
        """Adds credential info string to error details for 401/403/404 errors.

        Args:
            error (google.api_core.exceptions.GoogleAPICallError): The error to add the cred info.
        """
        if error.code not in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND]:
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

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Optional[Union[str, WorkloadIdentityPoolsTransport, Callable[..., WorkloadIdentityPoolsTransport]]] = None,
            client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the workload identity pools client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,WorkloadIdentityPoolsTransport,Callable[..., WorkloadIdentityPoolsTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the WorkloadIdentityPoolsTransport constructor.
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
        self._client_options = cast(client_options_lib.ClientOptions, self._client_options)

        universe_domain_opt = getattr(self._client_options, 'universe_domain', None)

        self._use_client_cert, self._use_mtls_endpoint, self._universe_domain_env = WorkloadIdentityPoolsClient._read_environment_variables()
        self._client_cert_source = WorkloadIdentityPoolsClient._get_client_cert_source(self._client_options.client_cert_source, self._use_client_cert)
        self._universe_domain = WorkloadIdentityPoolsClient._get_universe_domain(universe_domain_opt, self._universe_domain_env)
        self._api_endpoint = None # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        if CLIENT_LOGGING_SUPPORTED:  # pragma: NO COVER
            # Setup logging.
            client_logging.initialize_logging()

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError("client_options.api_key and credentials are mutually exclusive")

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, WorkloadIdentityPoolsTransport)
        if transport_provided:
            # transport is a WorkloadIdentityPoolsTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError("When providing a transport instance, "
                                 "provide its credentials directly.")
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(WorkloadIdentityPoolsTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (self._api_endpoint or
            WorkloadIdentityPoolsClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint))

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(google.auth._default, "get_api_key_credentials"):
                credentials = google.auth._default.get_api_key_credentials(api_key_value)

            transport_init: Union[Type[WorkloadIdentityPoolsTransport], Callable[..., WorkloadIdentityPoolsTransport]] = (
                WorkloadIdentityPoolsClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., WorkloadIdentityPoolsTransport], transport)
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(std_logging.DEBUG):  # pragma: NO COVER
                _LOGGER.debug(
                    "Created client `google.iam_v1beta.WorkloadIdentityPoolsClient`.",
                    extra = {
                        "serviceName": "google.iam.v1beta.WorkloadIdentityPools",
                        "universeDomain": getattr(self._transport._credentials, "universe_domain", ""),
                        "credentialsType": f"{type(self._transport._credentials).__module__}.{type(self._transport._credentials).__qualname__}",
                        "credentialsInfo": getattr(self.transport._credentials, "get_cred_info", lambda: None)(),
                    } if hasattr(self._transport, "_credentials") else {
                        "serviceName": "google.iam.v1beta.WorkloadIdentityPools",
                        "credentialsType": None,
                    }
                )

    def list_workload_identity_pools(self,
            request: Optional[Union[workload_identity_pool.ListWorkloadIdentityPoolsRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> pagers.ListWorkloadIdentityPoolsPager:
        r"""Lists all non-deleted
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool]s
        in a project. If ``show_deleted`` is set to ``true``, then
        deleted pools are also listed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_list_workload_identity_pools():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.ListWorkloadIdentityPoolsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workload_identity_pools(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.iam_v1beta.types.ListWorkloadIdentityPoolsRequest, dict]):
                The request object. Request message for
                ListWorkloadIdentityPools.
            parent (str):
                Required. The parent resource to list
                pools for.

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
            google.iam_v1beta.services.workload_identity_pools.pagers.ListWorkloadIdentityPoolsPager:
                Response message for
                ListWorkloadIdentityPools.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.ListWorkloadIdentityPoolsRequest):
            request = workload_identity_pool.ListWorkloadIdentityPoolsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_workload_identity_pools]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListWorkloadIdentityPoolsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_workload_identity_pool(self,
            request: Optional[Union[workload_identity_pool.GetWorkloadIdentityPoolRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> workload_identity_pool.WorkloadIdentityPool:
        r"""Gets an individual
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_get_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.GetWorkloadIdentityPoolRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_workload_identity_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.GetWorkloadIdentityPoolRequest, dict]):
                The request object. Request message for
                GetWorkloadIdentityPool.
            name (str):
                Required. The name of the pool to
                retrieve.

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
            google.iam_v1beta.types.WorkloadIdentityPool:
                Represents a collection of external
                workload identities. You can define IAM
                policies to grant these identities
                access to Google Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.GetWorkloadIdentityPoolRequest):
            request = workload_identity_pool.GetWorkloadIdentityPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_workload_identity_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def create_workload_identity_pool(self,
            request: Optional[Union[gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            workload_identity_pool: Optional[gi_workload_identity_pool.WorkloadIdentityPool] = None,
            workload_identity_pool_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Creates a new
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted pool until 30 days after
        deletion.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_create_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.CreateWorkloadIdentityPoolRequest(
                    parent="parent_value",
                    workload_identity_pool_id="workload_identity_pool_id_value",
                )

                # Make the request
                operation = client.create_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.CreateWorkloadIdentityPoolRequest, dict]):
                The request object. Request message for
                CreateWorkloadIdentityPool.
            parent (str):
                Required. The parent resource to create the pool in. The
                only supported location is ``global``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool (google.iam_v1beta.types.WorkloadIdentityPool):
                Required. The pool to create.
                This corresponds to the ``workload_identity_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool_id (str):
                Required. The ID to use for the pool, which becomes the
                final component of the resource name. This value should
                be 4-32 characters, and may contain the characters
                [a-z0-9-]. The prefix ``gcp-`` is reserved for use by
                Google, and may not be specified.

                This corresponds to the ``workload_identity_pool_id`` field
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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, workload_identity_pool, workload_identity_pool_id]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest):
            request = gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if workload_identity_pool is not None:
                request.workload_identity_pool = workload_identity_pool
            if workload_identity_pool_id is not None:
                request.workload_identity_pool_id = workload_identity_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_workload_identity_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
            gi_workload_identity_pool.WorkloadIdentityPool,
            metadata_type=gi_workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_workload_identity_pool(self,
            request: Optional[Union[gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest, dict]] = None,
            *,
            workload_identity_pool: Optional[gi_workload_identity_pool.WorkloadIdentityPool] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Updates an existing
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_update_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.UpdateWorkloadIdentityPoolRequest(
                )

                # Make the request
                operation = client.update_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.UpdateWorkloadIdentityPoolRequest, dict]):
                The request object. Request message for
                UpdateWorkloadIdentityPool.
            workload_identity_pool (google.iam_v1beta.types.WorkloadIdentityPool):
                Required. The pool to update. The ``name`` field is used
                to identify the pool.

                This corresponds to the ``workload_identity_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields update.
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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [workload_identity_pool, update_mask]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest):
            request = gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if workload_identity_pool is not None:
                request.workload_identity_pool = workload_identity_pool
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_workload_identity_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("workload_identity_pool.name", request.workload_identity_pool.name),
            )),
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
            gi_workload_identity_pool.WorkloadIdentityPool,
            metadata_type=gi_workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_workload_identity_pool(self,
            request: Optional[Union[workload_identity_pool.DeleteWorkloadIdentityPoolRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Deletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot use a deleted pool to exchange external credentials
        for Google Cloud credentials. However, deletion does not revoke
        credentials that have already been issued. Credentials issued
        for a deleted pool do not grant access to resources. If the pool
        is undeleted, and the credentials are not expired, they grant
        access again. You can undelete a pool for 30 days. After 30
        days, deletion is permanent. You cannot update deleted pools.
        However, you can view and list them.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_delete_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.DeleteWorkloadIdentityPoolRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.DeleteWorkloadIdentityPoolRequest, dict]):
                The request object. Request message for
                DeleteWorkloadIdentityPool.
            name (str):
                Required. The name of the pool to
                delete.

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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.DeleteWorkloadIdentityPoolRequest):
            request = workload_identity_pool.DeleteWorkloadIdentityPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_workload_identity_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPool,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def undelete_workload_identity_pool(self,
            request: Optional[Union[workload_identity_pool.UndeleteWorkloadIdentityPoolRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Undeletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool],
        as long as it was deleted fewer than 30 days ago.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_undelete_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.UndeleteWorkloadIdentityPoolRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.UndeleteWorkloadIdentityPoolRequest, dict]):
                The request object. Request message for
                UndeleteWorkloadIdentityPool.
            name (str):
                Required. The name of the pool to
                undelete.

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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.UndeleteWorkloadIdentityPoolRequest):
            request = workload_identity_pool.UndeleteWorkloadIdentityPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_workload_identity_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPool,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_workload_identity_pool_providers(self,
            request: Optional[Union[workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> pagers.ListWorkloadIdentityPoolProvidersPager:
        r"""Lists all non-deleted
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider]s
        in a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].
        If ``show_deleted`` is set to ``true``, then deleted providers
        are also listed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_list_workload_identity_pool_providers():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.ListWorkloadIdentityPoolProvidersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workload_identity_pool_providers(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersRequest, dict]):
                The request object. Request message for
                ListWorkloadIdentityPoolProviders.
            parent (str):
                Required. The pool to list providers
                for.

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
            google.iam_v1beta.services.workload_identity_pools.pagers.ListWorkloadIdentityPoolProvidersPager:
                Response message for
                ListWorkloadIdentityPoolProviders.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest):
            request = workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_workload_identity_pool_providers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListWorkloadIdentityPoolProvidersPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.GetWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> workload_identity_pool.WorkloadIdentityPoolProvider:
        r"""Gets an individual
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_get_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.GetWorkloadIdentityPoolProviderRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_workload_identity_pool_provider(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.GetWorkloadIdentityPoolProviderRequest, dict]):
                The request object. Request message for
                GetWorkloadIdentityPoolProvider.
            name (str):
                Required. The name of the provider to
                retrieve.

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
            google.iam_v1beta.types.WorkloadIdentityPoolProvider:
                A configuration for an external
                identity provider.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.GetWorkloadIdentityPoolProviderRequest):
            request = workload_identity_pool.GetWorkloadIdentityPoolProviderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_workload_identity_pool_provider]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def create_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            workload_identity_pool_provider: Optional[workload_identity_pool.WorkloadIdentityPoolProvider] = None,
            workload_identity_pool_provider_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Creates a new
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider]
        in a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted provider until 30 days
        after deletion.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_create_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                workload_identity_pool_provider = iam_v1beta.WorkloadIdentityPoolProvider()
                workload_identity_pool_provider.aws.account_id = "account_id_value"

                request = iam_v1beta.CreateWorkloadIdentityPoolProviderRequest(
                    parent="parent_value",
                    workload_identity_pool_provider=workload_identity_pool_provider,
                    workload_identity_pool_provider_id="workload_identity_pool_provider_id_value",
                )

                # Make the request
                operation = client.create_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.CreateWorkloadIdentityPoolProviderRequest, dict]):
                The request object. Request message for
                CreateWorkloadIdentityPoolProvider.
            parent (str):
                Required. The pool to create this
                provider in.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool_provider (google.iam_v1beta.types.WorkloadIdentityPoolProvider):
                Required. The provider to create.
                This corresponds to the ``workload_identity_pool_provider`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool_provider_id (str):
                Required. The ID for the provider, which becomes the
                final component of the resource name. This value must be
                4-32 characters, and may contain the characters
                [a-z0-9-]. The prefix ``gcp-`` is reserved for use by
                Google, and may not be specified.

                This corresponds to the ``workload_identity_pool_provider_id`` field
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

                The result type for the operation will be
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, workload_identity_pool_provider, workload_identity_pool_provider_id]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest):
            request = workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if workload_identity_pool_provider is not None:
                request.workload_identity_pool_provider = workload_identity_pool_provider
            if workload_identity_pool_provider_id is not None:
                request.workload_identity_pool_provider_id = workload_identity_pool_provider_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_workload_identity_pool_provider]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            workload_identity_pool_provider: Optional[workload_identity_pool.WorkloadIdentityPoolProvider] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Updates an existing
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_update_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                workload_identity_pool_provider = iam_v1beta.WorkloadIdentityPoolProvider()
                workload_identity_pool_provider.aws.account_id = "account_id_value"

                request = iam_v1beta.UpdateWorkloadIdentityPoolProviderRequest(
                    workload_identity_pool_provider=workload_identity_pool_provider,
                )

                # Make the request
                operation = client.update_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.UpdateWorkloadIdentityPoolProviderRequest, dict]):
                The request object. Request message for
                UpdateWorkloadIdentityPoolProvider.
            workload_identity_pool_provider (google.iam_v1beta.types.WorkloadIdentityPoolProvider):
                Required. The provider to update.
                This corresponds to the ``workload_identity_pool_provider`` field
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [workload_identity_pool_provider, update_mask]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest):
            request = workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if workload_identity_pool_provider is not None:
                request.workload_identity_pool_provider = workload_identity_pool_provider
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_workload_identity_pool_provider]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("workload_identity_pool_provider.name", request.workload_identity_pool_provider.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Deletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].
        Deleting a provider does not revoke credentials that have
        already been issued; they continue to grant access. You can
        undelete a provider for 30 days. After 30 days, deletion is
        permanent. You cannot update deleted providers. However, you can
        view and list them.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_delete_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.DeleteWorkloadIdentityPoolProviderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.DeleteWorkloadIdentityPoolProviderRequest, dict]):
                The request object. Request message for
                DeleteWorkloadIdentityPoolProvider.
            name (str):
                Required. The name of the provider to
                delete.

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

                The result type for the operation will be
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest):
            request = workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_workload_identity_pool_provider]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    def undelete_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
            ) -> operation.Operation:
        r"""Undeletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider],
        as long as it was deleted fewer than 30 days ago.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            def sample_undelete_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsClient()

                # Initialize request argument(s)
                request = iam_v1beta.UndeleteWorkloadIdentityPoolProviderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam_v1beta.types.UndeleteWorkloadIdentityPoolProviderRequest, dict]):
                The request object. Request message for
                UndeleteWorkloadIdentityPoolProvider.
            name (str):
                Required. The name of the provider to
                undelete.

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

                The result type for the operation will be
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = len([param for param in flattened_params if param is not None]) > 0
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest):
            request = workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_workload_identity_pool_provider]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "WorkloadIdentityPoolsClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()







DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "WorkloadIdentityPoolsClient",
)
