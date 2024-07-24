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

from google.cloud.dataform_v1beta1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore

from google.cloud.dataform_v1beta1.services.dataform import pagers
from google.cloud.dataform_v1beta1.types import dataform

from .transports.base import DEFAULT_CLIENT_INFO, DataformTransport
from .transports.grpc import DataformGrpcTransport
from .transports.grpc_asyncio import DataformGrpcAsyncIOTransport
from .transports.rest import DataformRestTransport


class DataformClientMeta(type):
    """Metaclass for the Dataform client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DataformTransport]]
    _transport_registry["grpc"] = DataformGrpcTransport
    _transport_registry["grpc_asyncio"] = DataformGrpcAsyncIOTransport
    _transport_registry["rest"] = DataformRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[DataformTransport]:
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


class DataformClient(metaclass=DataformClientMeta):
    """Dataform is a service to develop, create, document, test, and
    update curated tables in BigQuery.
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
    DEFAULT_ENDPOINT = "dataform.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "dataform.{UNIVERSE_DOMAIN}"
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
            DataformClient: The constructed client.
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
            DataformClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataformTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataformTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def compilation_result_path(
        project: str,
        location: str,
        repository: str,
        compilation_result: str,
    ) -> str:
        """Returns a fully-qualified compilation_result string."""
        return "projects/{project}/locations/{location}/repositories/{repository}/compilationResults/{compilation_result}".format(
            project=project,
            location=location,
            repository=repository,
            compilation_result=compilation_result,
        )

    @staticmethod
    def parse_compilation_result_path(path: str) -> Dict[str, str]:
        """Parses a compilation_result path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/repositories/(?P<repository>.+?)/compilationResults/(?P<compilation_result>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def release_config_path(
        project: str,
        location: str,
        repository: str,
        release_config: str,
    ) -> str:
        """Returns a fully-qualified release_config string."""
        return "projects/{project}/locations/{location}/repositories/{repository}/releaseConfigs/{release_config}".format(
            project=project,
            location=location,
            repository=repository,
            release_config=release_config,
        )

    @staticmethod
    def parse_release_config_path(path: str) -> Dict[str, str]:
        """Parses a release_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/repositories/(?P<repository>.+?)/releaseConfigs/(?P<release_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def repository_path(
        project: str,
        location: str,
        repository: str,
    ) -> str:
        """Returns a fully-qualified repository string."""
        return (
            "projects/{project}/locations/{location}/repositories/{repository}".format(
                project=project,
                location=location,
                repository=repository,
            )
        )

    @staticmethod
    def parse_repository_path(path: str) -> Dict[str, str]:
        """Parses a repository path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/repositories/(?P<repository>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def secret_version_path(
        project: str,
        secret: str,
        version: str,
    ) -> str:
        """Returns a fully-qualified secret_version string."""
        return "projects/{project}/secrets/{secret}/versions/{version}".format(
            project=project,
            secret=secret,
            version=version,
        )

    @staticmethod
    def parse_secret_version_path(path: str) -> Dict[str, str]:
        """Parses a secret_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/secrets/(?P<secret>.+?)/versions/(?P<version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def workflow_config_path(
        project: str,
        location: str,
        repository: str,
        workflow_config: str,
    ) -> str:
        """Returns a fully-qualified workflow_config string."""
        return "projects/{project}/locations/{location}/repositories/{repository}/workflowConfigs/{workflow_config}".format(
            project=project,
            location=location,
            repository=repository,
            workflow_config=workflow_config,
        )

    @staticmethod
    def parse_workflow_config_path(path: str) -> Dict[str, str]:
        """Parses a workflow_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/repositories/(?P<repository>.+?)/workflowConfigs/(?P<workflow_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def workflow_invocation_path(
        project: str,
        location: str,
        repository: str,
        workflow_invocation: str,
    ) -> str:
        """Returns a fully-qualified workflow_invocation string."""
        return "projects/{project}/locations/{location}/repositories/{repository}/workflowInvocations/{workflow_invocation}".format(
            project=project,
            location=location,
            repository=repository,
            workflow_invocation=workflow_invocation,
        )

    @staticmethod
    def parse_workflow_invocation_path(path: str) -> Dict[str, str]:
        """Parses a workflow_invocation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/repositories/(?P<repository>.+?)/workflowInvocations/(?P<workflow_invocation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def workspace_path(
        project: str,
        location: str,
        repository: str,
        workspace: str,
    ) -> str:
        """Returns a fully-qualified workspace string."""
        return "projects/{project}/locations/{location}/repositories/{repository}/workspaces/{workspace}".format(
            project=project,
            location=location,
            repository=repository,
            workspace=workspace,
        )

    @staticmethod
    def parse_workspace_path(path: str) -> Dict[str, str]:
        """Parses a workspace path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/repositories/(?P<repository>.+?)/workspaces/(?P<workspace>.+?)$",
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
            _default_universe = DataformClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = DataformClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = DataformClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = DataformClient._DEFAULT_UNIVERSE
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

        default_universe = DataformClient._DEFAULT_UNIVERSE
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
            or DataformClient._compare_universes(
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
            Union[str, DataformTransport, Callable[..., DataformTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the dataform client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,DataformTransport,Callable[..., DataformTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the DataformTransport constructor.
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
        ) = DataformClient._read_environment_variables()
        self._client_cert_source = DataformClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = DataformClient._get_universe_domain(
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
        transport_provided = isinstance(transport, DataformTransport)
        if transport_provided:
            # transport is a DataformTransport instance.
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
            self._transport = cast(DataformTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or DataformClient._get_api_endpoint(
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
                Type[DataformTransport], Callable[..., DataformTransport]
            ] = (
                type(self).get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., DataformTransport], transport)
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

    def list_repositories(
        self,
        request: Optional[Union[dataform.ListRepositoriesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRepositoriesPager:
        r"""Lists Repositories in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_list_repositories():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ListRepositoriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_repositories(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ListRepositoriesRequest, dict]):
                The request object. ``ListRepositories`` request message.
            parent (str):
                Required. The location in which to list repositories.
                Must be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.ListRepositoriesPager:
                ListRepositories response message.

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
        if not isinstance(request, dataform.ListRepositoriesRequest):
            request = dataform.ListRepositoriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_repositories]

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
        response = pagers.ListRepositoriesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_repository(
        self,
        request: Optional[Union[dataform.GetRepositoryRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Repository:
        r"""Fetches a single Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_get_repository():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.GetRepositoryRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_repository(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.GetRepositoryRequest, dict]):
                The request object. ``GetRepository`` request message.
            name (str):
                Required. The repository's name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.Repository:
                Represents a Dataform Git repository.
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
        if not isinstance(request, dataform.GetRepositoryRequest):
            request = dataform.GetRepositoryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_repository]

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

    def create_repository(
        self,
        request: Optional[Union[dataform.CreateRepositoryRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        repository: Optional[dataform.Repository] = None,
        repository_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Repository:
        r"""Creates a new Repository in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_create_repository():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.CreateRepositoryRequest(
                    parent="parent_value",
                    repository_id="repository_id_value",
                )

                # Make the request
                response = client.create_repository(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CreateRepositoryRequest, dict]):
                The request object. ``CreateRepository`` request message.
            parent (str):
                Required. The location in which to create the
                repository. Must be in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            repository (google.cloud.dataform_v1beta1.types.Repository):
                Required. The repository to create.
                This corresponds to the ``repository`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            repository_id (str):
                Required. The ID to use for the
                repository, which will become the final
                component of the repository's resource
                name.

                This corresponds to the ``repository_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.Repository:
                Represents a Dataform Git repository.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, repository, repository_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CreateRepositoryRequest):
            request = dataform.CreateRepositoryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if repository is not None:
                request.repository = repository
            if repository_id is not None:
                request.repository_id = repository_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_repository]

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

    def update_repository(
        self,
        request: Optional[Union[dataform.UpdateRepositoryRequest, dict]] = None,
        *,
        repository: Optional[dataform.Repository] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Repository:
        r"""Updates a single Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_update_repository():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.UpdateRepositoryRequest(
                )

                # Make the request
                response = client.update_repository(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.UpdateRepositoryRequest, dict]):
                The request object. ``UpdateRepository`` request message.
            repository (google.cloud.dataform_v1beta1.types.Repository):
                Required. The repository to update.
                This corresponds to the ``repository`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Specifies the fields to be
                updated in the repository. If left
                unset, all fields will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.Repository:
                Represents a Dataform Git repository.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([repository, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.UpdateRepositoryRequest):
            request = dataform.UpdateRepositoryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if repository is not None:
                request.repository = repository
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_repository]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("repository.name", request.repository.name),)
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

    def delete_repository(
        self,
        request: Optional[Union[dataform.DeleteRepositoryRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_delete_repository():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.DeleteRepositoryRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_repository(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.DeleteRepositoryRequest, dict]):
                The request object. ``DeleteRepository`` request message.
            name (str):
                Required. The repository's name.
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
        if not isinstance(request, dataform.DeleteRepositoryRequest):
            request = dataform.DeleteRepositoryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_repository]

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

    def commit_repository_changes(
        self,
        request: Optional[Union[dataform.CommitRepositoryChangesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Applies a Git commit to a Repository. The Repository must not
        have a value for ``git_remote_settings.url``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_commit_repository_changes():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                commit_metadata = dataform_v1beta1.CommitMetadata()
                commit_metadata.author.name = "name_value"
                commit_metadata.author.email_address = "email_address_value"

                request = dataform_v1beta1.CommitRepositoryChangesRequest(
                    name="name_value",
                    commit_metadata=commit_metadata,
                )

                # Make the request
                client.commit_repository_changes(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CommitRepositoryChangesRequest, dict]):
                The request object. ``CommitRepositoryChanges`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CommitRepositoryChangesRequest):
            request = dataform.CommitRepositoryChangesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.commit_repository_changes
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

    def read_repository_file(
        self,
        request: Optional[Union[dataform.ReadRepositoryFileRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ReadRepositoryFileResponse:
        r"""Returns the contents of a file (inside a Repository). The
        Repository must not have a value for
        ``git_remote_settings.url``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_read_repository_file():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ReadRepositoryFileRequest(
                    name="name_value",
                    path="path_value",
                )

                # Make the request
                response = client.read_repository_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ReadRepositoryFileRequest, dict]):
                The request object. ``ReadRepositoryFile`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.ReadRepositoryFileResponse:
                ReadRepositoryFile response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.ReadRepositoryFileRequest):
            request = dataform.ReadRepositoryFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_repository_file]

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

    def query_repository_directory_contents(
        self,
        request: Optional[
            Union[dataform.QueryRepositoryDirectoryContentsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryRepositoryDirectoryContentsPager:
        r"""Returns the contents of a given Repository directory. The
        Repository must not have a value for
        ``git_remote_settings.url``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_query_repository_directory_contents():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.QueryRepositoryDirectoryContentsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.query_repository_directory_contents(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.QueryRepositoryDirectoryContentsRequest, dict]):
                The request object. ``QueryRepositoryDirectoryContents`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.QueryRepositoryDirectoryContentsPager:
                QueryRepositoryDirectoryContents response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.QueryRepositoryDirectoryContentsRequest):
            request = dataform.QueryRepositoryDirectoryContentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.query_repository_directory_contents
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.QueryRepositoryDirectoryContentsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def fetch_repository_history(
        self,
        request: Optional[Union[dataform.FetchRepositoryHistoryRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.FetchRepositoryHistoryPager:
        r"""Fetches a Repository's history of commits. The Repository must
        not have a value for ``git_remote_settings.url``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_fetch_repository_history():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.FetchRepositoryHistoryRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.fetch_repository_history(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.FetchRepositoryHistoryRequest, dict]):
                The request object. ``FetchRepositoryHistory`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.FetchRepositoryHistoryPager:
                FetchRepositoryHistory response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.FetchRepositoryHistoryRequest):
            request = dataform.FetchRepositoryHistoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.fetch_repository_history]

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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.FetchRepositoryHistoryPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def compute_repository_access_token_status(
        self,
        request: Optional[
            Union[dataform.ComputeRepositoryAccessTokenStatusRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ComputeRepositoryAccessTokenStatusResponse:
        r"""Computes a Repository's Git access token status.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_compute_repository_access_token_status():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ComputeRepositoryAccessTokenStatusRequest(
                    name="name_value",
                )

                # Make the request
                response = client.compute_repository_access_token_status(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ComputeRepositoryAccessTokenStatusRequest, dict]):
                The request object. ``ComputeRepositoryAccessTokenStatus`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.ComputeRepositoryAccessTokenStatusResponse:
                ComputeRepositoryAccessTokenStatus response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.ComputeRepositoryAccessTokenStatusRequest):
            request = dataform.ComputeRepositoryAccessTokenStatusRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.compute_repository_access_token_status
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

    def fetch_remote_branches(
        self,
        request: Optional[Union[dataform.FetchRemoteBranchesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchRemoteBranchesResponse:
        r"""Fetches a Repository's remote branches.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_fetch_remote_branches():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.FetchRemoteBranchesRequest(
                    name="name_value",
                )

                # Make the request
                response = client.fetch_remote_branches(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.FetchRemoteBranchesRequest, dict]):
                The request object. ``FetchRemoteBranches`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.FetchRemoteBranchesResponse:
                FetchRemoteBranches response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.FetchRemoteBranchesRequest):
            request = dataform.FetchRemoteBranchesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.fetch_remote_branches]

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

    def list_workspaces(
        self,
        request: Optional[Union[dataform.ListWorkspacesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkspacesPager:
        r"""Lists Workspaces in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_list_workspaces():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ListWorkspacesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workspaces(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ListWorkspacesRequest, dict]):
                The request object. ``ListWorkspaces`` request message.
            parent (str):
                Required. The repository in which to list workspaces.
                Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.ListWorkspacesPager:
                ListWorkspaces response message.

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
        if not isinstance(request, dataform.ListWorkspacesRequest):
            request = dataform.ListWorkspacesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_workspaces]

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
        response = pagers.ListWorkspacesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_workspace(
        self,
        request: Optional[Union[dataform.GetWorkspaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Workspace:
        r"""Fetches a single Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_get_workspace():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.GetWorkspaceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_workspace(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.GetWorkspaceRequest, dict]):
                The request object. ``GetWorkspace`` request message.
            name (str):
                Required. The workspace's name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.Workspace:
                Represents a Dataform Git workspace.
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
        if not isinstance(request, dataform.GetWorkspaceRequest):
            request = dataform.GetWorkspaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_workspace]

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

    def create_workspace(
        self,
        request: Optional[Union[dataform.CreateWorkspaceRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        workspace: Optional[dataform.Workspace] = None,
        workspace_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Workspace:
        r"""Creates a new Workspace in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_create_workspace():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.CreateWorkspaceRequest(
                    parent="parent_value",
                    workspace_id="workspace_id_value",
                )

                # Make the request
                response = client.create_workspace(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CreateWorkspaceRequest, dict]):
                The request object. ``CreateWorkspace`` request message.
            parent (str):
                Required. The repository in which to create the
                workspace. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workspace (google.cloud.dataform_v1beta1.types.Workspace):
                Required. The workspace to create.
                This corresponds to the ``workspace`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workspace_id (str):
                Required. The ID to use for the
                workspace, which will become the final
                component of the workspace's resource
                name.

                This corresponds to the ``workspace_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.Workspace:
                Represents a Dataform Git workspace.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workspace, workspace_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CreateWorkspaceRequest):
            request = dataform.CreateWorkspaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if workspace is not None:
                request.workspace = workspace
            if workspace_id is not None:
                request.workspace_id = workspace_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_workspace]

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

    def delete_workspace(
        self,
        request: Optional[Union[dataform.DeleteWorkspaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_delete_workspace():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.DeleteWorkspaceRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_workspace(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.DeleteWorkspaceRequest, dict]):
                The request object. ``DeleteWorkspace`` request message.
            name (str):
                Required. The workspace resource's
                name.

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
        if not isinstance(request, dataform.DeleteWorkspaceRequest):
            request = dataform.DeleteWorkspaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_workspace]

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

    def install_npm_packages(
        self,
        request: Optional[Union[dataform.InstallNpmPackagesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.InstallNpmPackagesResponse:
        r"""Installs dependency NPM packages (inside a
        Workspace).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_install_npm_packages():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.InstallNpmPackagesRequest(
                    workspace="workspace_value",
                )

                # Make the request
                response = client.install_npm_packages(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.InstallNpmPackagesRequest, dict]):
                The request object. ``InstallNpmPackages`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.InstallNpmPackagesResponse:
                InstallNpmPackages response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.InstallNpmPackagesRequest):
            request = dataform.InstallNpmPackagesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.install_npm_packages]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def pull_git_commits(
        self,
        request: Optional[Union[dataform.PullGitCommitsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pulls Git commits from the Repository's remote into a
        Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_pull_git_commits():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                author = dataform_v1beta1.CommitAuthor()
                author.name = "name_value"
                author.email_address = "email_address_value"

                request = dataform_v1beta1.PullGitCommitsRequest(
                    name="name_value",
                    author=author,
                )

                # Make the request
                client.pull_git_commits(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.PullGitCommitsRequest, dict]):
                The request object. ``PullGitCommits`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.PullGitCommitsRequest):
            request = dataform.PullGitCommitsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.pull_git_commits]

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

    def push_git_commits(
        self,
        request: Optional[Union[dataform.PushGitCommitsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pushes Git commits from a Workspace to the
        Repository's remote.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_push_git_commits():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.PushGitCommitsRequest(
                    name="name_value",
                )

                # Make the request
                client.push_git_commits(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.PushGitCommitsRequest, dict]):
                The request object. ``PushGitCommits`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.PushGitCommitsRequest):
            request = dataform.PushGitCommitsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.push_git_commits]

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

    def fetch_file_git_statuses(
        self,
        request: Optional[Union[dataform.FetchFileGitStatusesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchFileGitStatusesResponse:
        r"""Fetches Git statuses for the files in a Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_fetch_file_git_statuses():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.FetchFileGitStatusesRequest(
                    name="name_value",
                )

                # Make the request
                response = client.fetch_file_git_statuses(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.FetchFileGitStatusesRequest, dict]):
                The request object. ``FetchFileGitStatuses`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.FetchFileGitStatusesResponse:
                FetchFileGitStatuses response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.FetchFileGitStatusesRequest):
            request = dataform.FetchFileGitStatusesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.fetch_file_git_statuses]

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

    def fetch_git_ahead_behind(
        self,
        request: Optional[Union[dataform.FetchGitAheadBehindRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchGitAheadBehindResponse:
        r"""Fetches Git ahead/behind against a remote branch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_fetch_git_ahead_behind():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.FetchGitAheadBehindRequest(
                    name="name_value",
                )

                # Make the request
                response = client.fetch_git_ahead_behind(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.FetchGitAheadBehindRequest, dict]):
                The request object. ``FetchGitAheadBehind`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.FetchGitAheadBehindResponse:
                FetchGitAheadBehind response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.FetchGitAheadBehindRequest):
            request = dataform.FetchGitAheadBehindRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.fetch_git_ahead_behind]

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

    def commit_workspace_changes(
        self,
        request: Optional[Union[dataform.CommitWorkspaceChangesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Applies a Git commit for uncommitted files in a
        Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_commit_workspace_changes():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                author = dataform_v1beta1.CommitAuthor()
                author.name = "name_value"
                author.email_address = "email_address_value"

                request = dataform_v1beta1.CommitWorkspaceChangesRequest(
                    name="name_value",
                    author=author,
                )

                # Make the request
                client.commit_workspace_changes(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CommitWorkspaceChangesRequest, dict]):
                The request object. ``CommitWorkspaceChanges`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CommitWorkspaceChangesRequest):
            request = dataform.CommitWorkspaceChangesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.commit_workspace_changes]

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

    def reset_workspace_changes(
        self,
        request: Optional[Union[dataform.ResetWorkspaceChangesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Performs a Git reset for uncommitted files in a
        Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_reset_workspace_changes():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ResetWorkspaceChangesRequest(
                    name="name_value",
                )

                # Make the request
                client.reset_workspace_changes(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ResetWorkspaceChangesRequest, dict]):
                The request object. ``ResetWorkspaceChanges`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.ResetWorkspaceChangesRequest):
            request = dataform.ResetWorkspaceChangesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reset_workspace_changes]

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

    def fetch_file_diff(
        self,
        request: Optional[Union[dataform.FetchFileDiffRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchFileDiffResponse:
        r"""Fetches Git diff for an uncommitted file in a
        Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_fetch_file_diff():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.FetchFileDiffRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                response = client.fetch_file_diff(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.FetchFileDiffRequest, dict]):
                The request object. ``FetchFileDiff`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.FetchFileDiffResponse:
                FetchFileDiff response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.FetchFileDiffRequest):
            request = dataform.FetchFileDiffRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.fetch_file_diff]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def query_directory_contents(
        self,
        request: Optional[Union[dataform.QueryDirectoryContentsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryDirectoryContentsPager:
        r"""Returns the contents of a given Workspace directory.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_query_directory_contents():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.QueryDirectoryContentsRequest(
                    workspace="workspace_value",
                )

                # Make the request
                page_result = client.query_directory_contents(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.QueryDirectoryContentsRequest, dict]):
                The request object. ``QueryDirectoryContents`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.QueryDirectoryContentsPager:
                QueryDirectoryContents response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.QueryDirectoryContentsRequest):
            request = dataform.QueryDirectoryContentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.query_directory_contents]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.QueryDirectoryContentsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def make_directory(
        self,
        request: Optional[Union[dataform.MakeDirectoryRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.MakeDirectoryResponse:
        r"""Creates a directory inside a Workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_make_directory():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.MakeDirectoryRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                response = client.make_directory(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.MakeDirectoryRequest, dict]):
                The request object. ``MakeDirectory`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.MakeDirectoryResponse:
                MakeDirectory response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.MakeDirectoryRequest):
            request = dataform.MakeDirectoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.make_directory]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def remove_directory(
        self,
        request: Optional[Union[dataform.RemoveDirectoryRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a directory (inside a Workspace) and all of
        its contents.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_remove_directory():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.RemoveDirectoryRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                client.remove_directory(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.RemoveDirectoryRequest, dict]):
                The request object. ``RemoveDirectory`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.RemoveDirectoryRequest):
            request = dataform.RemoveDirectoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_directory]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
            ),
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

    def move_directory(
        self,
        request: Optional[Union[dataform.MoveDirectoryRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.MoveDirectoryResponse:
        r"""Moves a directory (inside a Workspace), and all of
        its contents, to a new location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_move_directory():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.MoveDirectoryRequest(
                    workspace="workspace_value",
                    path="path_value",
                    new_path="new_path_value",
                )

                # Make the request
                response = client.move_directory(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.MoveDirectoryRequest, dict]):
                The request object. ``MoveDirectory`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.MoveDirectoryResponse:
                MoveDirectory response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.MoveDirectoryRequest):
            request = dataform.MoveDirectoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.move_directory]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def read_file(
        self,
        request: Optional[Union[dataform.ReadFileRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ReadFileResponse:
        r"""Returns the contents of a file (inside a Workspace).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_read_file():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ReadFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                response = client.read_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ReadFileRequest, dict]):
                The request object. ``ReadFile`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.ReadFileResponse:
                ReadFile response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.ReadFileRequest):
            request = dataform.ReadFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def remove_file(
        self,
        request: Optional[Union[dataform.RemoveFileRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a file (inside a Workspace).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_remove_file():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.RemoveFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                client.remove_file(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.RemoveFileRequest, dict]):
                The request object. ``RemoveFile`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.RemoveFileRequest):
            request = dataform.RemoveFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
            ),
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

    def move_file(
        self,
        request: Optional[Union[dataform.MoveFileRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.MoveFileResponse:
        r"""Moves a file (inside a Workspace) to a new location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_move_file():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.MoveFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                    new_path="new_path_value",
                )

                # Make the request
                response = client.move_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.MoveFileRequest, dict]):
                The request object. ``MoveFile`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.MoveFileResponse:
                MoveFile response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.MoveFileRequest):
            request = dataform.MoveFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.move_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def write_file(
        self,
        request: Optional[Union[dataform.WriteFileRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WriteFileResponse:
        r"""Writes to a file (inside a Workspace).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_write_file():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.WriteFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                    contents=b'contents_blob',
                )

                # Make the request
                response = client.write_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.WriteFileRequest, dict]):
                The request object. ``WriteFile`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.WriteFileResponse:
                WriteFile response message.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.WriteFileRequest):
            request = dataform.WriteFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.write_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    def list_release_configs(
        self,
        request: Optional[Union[dataform.ListReleaseConfigsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReleaseConfigsPager:
        r"""Lists ReleaseConfigs in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_list_release_configs():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ListReleaseConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_release_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ListReleaseConfigsRequest, dict]):
                The request object. ``ListReleaseConfigs`` request message.
            parent (str):
                Required. The repository in which to list release
                configs. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.ListReleaseConfigsPager:
                ListReleaseConfigs response message.

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
        if not isinstance(request, dataform.ListReleaseConfigsRequest):
            request = dataform.ListReleaseConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_release_configs]

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
        response = pagers.ListReleaseConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_release_config(
        self,
        request: Optional[Union[dataform.GetReleaseConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ReleaseConfig:
        r"""Fetches a single ReleaseConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_get_release_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.GetReleaseConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_release_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.GetReleaseConfigRequest, dict]):
                The request object. ``GetReleaseConfig`` request message.
            name (str):
                Required. The release config's name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.ReleaseConfig:
                Represents a Dataform release
                configuration.

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
        if not isinstance(request, dataform.GetReleaseConfigRequest):
            request = dataform.GetReleaseConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_release_config]

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

    def create_release_config(
        self,
        request: Optional[Union[dataform.CreateReleaseConfigRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        release_config: Optional[dataform.ReleaseConfig] = None,
        release_config_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ReleaseConfig:
        r"""Creates a new ReleaseConfig in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_create_release_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                release_config = dataform_v1beta1.ReleaseConfig()
                release_config.git_commitish = "git_commitish_value"

                request = dataform_v1beta1.CreateReleaseConfigRequest(
                    parent="parent_value",
                    release_config=release_config,
                    release_config_id="release_config_id_value",
                )

                # Make the request
                response = client.create_release_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CreateReleaseConfigRequest, dict]):
                The request object. ``CreateReleaseConfig`` request message.
            parent (str):
                Required. The repository in which to create the release
                config. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release_config (google.cloud.dataform_v1beta1.types.ReleaseConfig):
                Required. The release config to
                create.

                This corresponds to the ``release_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release_config_id (str):
                Required. The ID to use for the
                release config, which will become the
                final component of the release config's
                resource name.

                This corresponds to the ``release_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.ReleaseConfig:
                Represents a Dataform release
                configuration.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, release_config, release_config_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CreateReleaseConfigRequest):
            request = dataform.CreateReleaseConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if release_config is not None:
                request.release_config = release_config
            if release_config_id is not None:
                request.release_config_id = release_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_release_config]

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

    def update_release_config(
        self,
        request: Optional[Union[dataform.UpdateReleaseConfigRequest, dict]] = None,
        *,
        release_config: Optional[dataform.ReleaseConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ReleaseConfig:
        r"""Updates a single ReleaseConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_update_release_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                release_config = dataform_v1beta1.ReleaseConfig()
                release_config.git_commitish = "git_commitish_value"

                request = dataform_v1beta1.UpdateReleaseConfigRequest(
                    release_config=release_config,
                )

                # Make the request
                response = client.update_release_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.UpdateReleaseConfigRequest, dict]):
                The request object. ``UpdateReleaseConfig`` request message.
            release_config (google.cloud.dataform_v1beta1.types.ReleaseConfig):
                Required. The release config to
                update.

                This corresponds to the ``release_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Specifies the fields to be
                updated in the release config. If left
                unset, all fields will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.ReleaseConfig:
                Represents a Dataform release
                configuration.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([release_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.UpdateReleaseConfigRequest):
            request = dataform.UpdateReleaseConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if release_config is not None:
                request.release_config = release_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_release_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("release_config.name", request.release_config.name),)
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

    def delete_release_config(
        self,
        request: Optional[Union[dataform.DeleteReleaseConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single ReleaseConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_delete_release_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.DeleteReleaseConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_release_config(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.DeleteReleaseConfigRequest, dict]):
                The request object. ``DeleteReleaseConfig`` request message.
            name (str):
                Required. The release config's name.
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
        if not isinstance(request, dataform.DeleteReleaseConfigRequest):
            request = dataform.DeleteReleaseConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_release_config]

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

    def list_compilation_results(
        self,
        request: Optional[Union[dataform.ListCompilationResultsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCompilationResultsPager:
        r"""Lists CompilationResults in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_list_compilation_results():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ListCompilationResultsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_compilation_results(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ListCompilationResultsRequest, dict]):
                The request object. ``ListCompilationResults`` request message.
            parent (str):
                Required. The repository in which to list compilation
                results. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.ListCompilationResultsPager:
                ListCompilationResults response message.

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
        if not isinstance(request, dataform.ListCompilationResultsRequest):
            request = dataform.ListCompilationResultsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_compilation_results]

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
        response = pagers.ListCompilationResultsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_compilation_result(
        self,
        request: Optional[Union[dataform.GetCompilationResultRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.CompilationResult:
        r"""Fetches a single CompilationResult.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_get_compilation_result():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.GetCompilationResultRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_compilation_result(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.GetCompilationResultRequest, dict]):
                The request object. ``GetCompilationResult`` request message.
            name (str):
                Required. The compilation result's
                name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.CompilationResult:
                Represents the result of compiling a
                Dataform project.

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
        if not isinstance(request, dataform.GetCompilationResultRequest):
            request = dataform.GetCompilationResultRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_compilation_result]

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

    def create_compilation_result(
        self,
        request: Optional[Union[dataform.CreateCompilationResultRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        compilation_result: Optional[dataform.CompilationResult] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.CompilationResult:
        r"""Creates a new CompilationResult in a given project
        and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_create_compilation_result():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                compilation_result = dataform_v1beta1.CompilationResult()
                compilation_result.git_commitish = "git_commitish_value"

                request = dataform_v1beta1.CreateCompilationResultRequest(
                    parent="parent_value",
                    compilation_result=compilation_result,
                )

                # Make the request
                response = client.create_compilation_result(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CreateCompilationResultRequest, dict]):
                The request object. ``CreateCompilationResult`` request message.
            parent (str):
                Required. The repository in which to create the
                compilation result. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            compilation_result (google.cloud.dataform_v1beta1.types.CompilationResult):
                Required. The compilation result to
                create.

                This corresponds to the ``compilation_result`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.CompilationResult:
                Represents the result of compiling a
                Dataform project.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, compilation_result])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CreateCompilationResultRequest):
            request = dataform.CreateCompilationResultRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if compilation_result is not None:
                request.compilation_result = compilation_result

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_compilation_result
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

    def query_compilation_result_actions(
        self,
        request: Optional[
            Union[dataform.QueryCompilationResultActionsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryCompilationResultActionsPager:
        r"""Returns CompilationResultActions in a given
        CompilationResult.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_query_compilation_result_actions():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.QueryCompilationResultActionsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.query_compilation_result_actions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.QueryCompilationResultActionsRequest, dict]):
                The request object. ``QueryCompilationResultActions`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.QueryCompilationResultActionsPager:
                QueryCompilationResultActions response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.QueryCompilationResultActionsRequest):
            request = dataform.QueryCompilationResultActionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.query_compilation_result_actions
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.QueryCompilationResultActionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_workflow_configs(
        self,
        request: Optional[Union[dataform.ListWorkflowConfigsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkflowConfigsPager:
        r"""Lists WorkflowConfigs in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_list_workflow_configs():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ListWorkflowConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workflow_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ListWorkflowConfigsRequest, dict]):
                The request object. ``ListWorkflowConfigs`` request message.
            parent (str):
                Required. The repository in which to list workflow
                configs. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.ListWorkflowConfigsPager:
                ListWorkflowConfigs response message.

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
        if not isinstance(request, dataform.ListWorkflowConfigsRequest):
            request = dataform.ListWorkflowConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_workflow_configs]

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
        response = pagers.ListWorkflowConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_workflow_config(
        self,
        request: Optional[Union[dataform.GetWorkflowConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowConfig:
        r"""Fetches a single WorkflowConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_get_workflow_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.GetWorkflowConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_workflow_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.GetWorkflowConfigRequest, dict]):
                The request object. ``GetWorkflowConfig`` request message.
            name (str):
                Required. The workflow config's name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.WorkflowConfig:
                Represents a Dataform workflow
                configuration.

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
        if not isinstance(request, dataform.GetWorkflowConfigRequest):
            request = dataform.GetWorkflowConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_workflow_config]

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

    def create_workflow_config(
        self,
        request: Optional[Union[dataform.CreateWorkflowConfigRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        workflow_config: Optional[dataform.WorkflowConfig] = None,
        workflow_config_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowConfig:
        r"""Creates a new WorkflowConfig in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_create_workflow_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                workflow_config = dataform_v1beta1.WorkflowConfig()
                workflow_config.release_config = "release_config_value"

                request = dataform_v1beta1.CreateWorkflowConfigRequest(
                    parent="parent_value",
                    workflow_config=workflow_config,
                    workflow_config_id="workflow_config_id_value",
                )

                # Make the request
                response = client.create_workflow_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CreateWorkflowConfigRequest, dict]):
                The request object. ``CreateWorkflowConfig`` request message.
            parent (str):
                Required. The repository in which to create the workflow
                config. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workflow_config (google.cloud.dataform_v1beta1.types.WorkflowConfig):
                Required. The workflow config to
                create.

                This corresponds to the ``workflow_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workflow_config_id (str):
                Required. The ID to use for the
                workflow config, which will become the
                final component of the workflow config's
                resource name.

                This corresponds to the ``workflow_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.WorkflowConfig:
                Represents a Dataform workflow
                configuration.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workflow_config, workflow_config_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CreateWorkflowConfigRequest):
            request = dataform.CreateWorkflowConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if workflow_config is not None:
                request.workflow_config = workflow_config
            if workflow_config_id is not None:
                request.workflow_config_id = workflow_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_workflow_config]

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

    def update_workflow_config(
        self,
        request: Optional[Union[dataform.UpdateWorkflowConfigRequest, dict]] = None,
        *,
        workflow_config: Optional[dataform.WorkflowConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowConfig:
        r"""Updates a single WorkflowConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_update_workflow_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                workflow_config = dataform_v1beta1.WorkflowConfig()
                workflow_config.release_config = "release_config_value"

                request = dataform_v1beta1.UpdateWorkflowConfigRequest(
                    workflow_config=workflow_config,
                )

                # Make the request
                response = client.update_workflow_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.UpdateWorkflowConfigRequest, dict]):
                The request object. ``UpdateWorkflowConfig`` request message.
            workflow_config (google.cloud.dataform_v1beta1.types.WorkflowConfig):
                Required. The workflow config to
                update.

                This corresponds to the ``workflow_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Specifies the fields to be
                updated in the workflow config. If left
                unset, all fields will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.WorkflowConfig:
                Represents a Dataform workflow
                configuration.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([workflow_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.UpdateWorkflowConfigRequest):
            request = dataform.UpdateWorkflowConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if workflow_config is not None:
                request.workflow_config = workflow_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_workflow_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workflow_config.name", request.workflow_config.name),)
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

    def delete_workflow_config(
        self,
        request: Optional[Union[dataform.DeleteWorkflowConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single WorkflowConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_delete_workflow_config():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.DeleteWorkflowConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_workflow_config(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.DeleteWorkflowConfigRequest, dict]):
                The request object. ``DeleteWorkflowConfig`` request message.
            name (str):
                Required. The workflow config's name.
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
        if not isinstance(request, dataform.DeleteWorkflowConfigRequest):
            request = dataform.DeleteWorkflowConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_workflow_config]

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

    def list_workflow_invocations(
        self,
        request: Optional[Union[dataform.ListWorkflowInvocationsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkflowInvocationsPager:
        r"""Lists WorkflowInvocations in a given Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_list_workflow_invocations():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.ListWorkflowInvocationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workflow_invocations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.ListWorkflowInvocationsRequest, dict]):
                The request object. ``ListWorkflowInvocations`` request message.
            parent (str):
                Required. The parent resource of the WorkflowInvocation
                type. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.ListWorkflowInvocationsPager:
                ListWorkflowInvocations response message.

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
        if not isinstance(request, dataform.ListWorkflowInvocationsRequest):
            request = dataform.ListWorkflowInvocationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_workflow_invocations
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
        response = pagers.ListWorkflowInvocationsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_workflow_invocation(
        self,
        request: Optional[Union[dataform.GetWorkflowInvocationRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowInvocation:
        r"""Fetches a single WorkflowInvocation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_get_workflow_invocation():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.GetWorkflowInvocationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_workflow_invocation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.GetWorkflowInvocationRequest, dict]):
                The request object. ``GetWorkflowInvocation`` request message.
            name (str):
                Required. The workflow invocation
                resource's name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.WorkflowInvocation:
                Represents a single invocation of a
                compilation result.

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
        if not isinstance(request, dataform.GetWorkflowInvocationRequest):
            request = dataform.GetWorkflowInvocationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_workflow_invocation]

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

    def create_workflow_invocation(
        self,
        request: Optional[Union[dataform.CreateWorkflowInvocationRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        workflow_invocation: Optional[dataform.WorkflowInvocation] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowInvocation:
        r"""Creates a new WorkflowInvocation in a given
        Repository.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_create_workflow_invocation():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                workflow_invocation = dataform_v1beta1.WorkflowInvocation()
                workflow_invocation.compilation_result = "compilation_result_value"

                request = dataform_v1beta1.CreateWorkflowInvocationRequest(
                    parent="parent_value",
                    workflow_invocation=workflow_invocation,
                )

                # Make the request
                response = client.create_workflow_invocation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CreateWorkflowInvocationRequest, dict]):
                The request object. ``CreateWorkflowInvocation`` request message.
            parent (str):
                Required. The repository in which to create the workflow
                invocation. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workflow_invocation (google.cloud.dataform_v1beta1.types.WorkflowInvocation):
                Required. The workflow invocation
                resource to create.

                This corresponds to the ``workflow_invocation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.types.WorkflowInvocation:
                Represents a single invocation of a
                compilation result.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workflow_invocation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CreateWorkflowInvocationRequest):
            request = dataform.CreateWorkflowInvocationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if workflow_invocation is not None:
                request.workflow_invocation = workflow_invocation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_workflow_invocation
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

    def delete_workflow_invocation(
        self,
        request: Optional[Union[dataform.DeleteWorkflowInvocationRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single WorkflowInvocation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_delete_workflow_invocation():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.DeleteWorkflowInvocationRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_workflow_invocation(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.DeleteWorkflowInvocationRequest, dict]):
                The request object. ``DeleteWorkflowInvocation`` request message.
            name (str):
                Required. The workflow invocation
                resource's name.

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
        if not isinstance(request, dataform.DeleteWorkflowInvocationRequest):
            request = dataform.DeleteWorkflowInvocationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_workflow_invocation
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

    def cancel_workflow_invocation(
        self,
        request: Optional[Union[dataform.CancelWorkflowInvocationRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Requests cancellation of a running
        WorkflowInvocation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_cancel_workflow_invocation():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.CancelWorkflowInvocationRequest(
                    name="name_value",
                )

                # Make the request
                client.cancel_workflow_invocation(request=request)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.CancelWorkflowInvocationRequest, dict]):
                The request object. ``CancelWorkflowInvocation`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.CancelWorkflowInvocationRequest):
            request = dataform.CancelWorkflowInvocationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.cancel_workflow_invocation
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

    def query_workflow_invocation_actions(
        self,
        request: Optional[
            Union[dataform.QueryWorkflowInvocationActionsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryWorkflowInvocationActionsPager:
        r"""Returns WorkflowInvocationActions in a given
        WorkflowInvocation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataform_v1beta1

            def sample_query_workflow_invocation_actions():
                # Create a client
                client = dataform_v1beta1.DataformClient()

                # Initialize request argument(s)
                request = dataform_v1beta1.QueryWorkflowInvocationActionsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.query_workflow_invocation_actions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1beta1.types.QueryWorkflowInvocationActionsRequest, dict]):
                The request object. ``QueryWorkflowInvocationActions`` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1beta1.services.dataform.pagers.QueryWorkflowInvocationActionsPager:
                QueryWorkflowInvocationActions response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, dataform.QueryWorkflowInvocationActionsRequest):
            request = dataform.QueryWorkflowInvocationActionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.query_workflow_invocation_actions
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.QueryWorkflowInvocationActionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "DataformClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def set_iam_policy(
        self,
        request: Optional[iam_policy_pb2.SetIamPolicyRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM access control policy on the specified function.

        Replaces any existing policy.

        Args:
            request (:class:`~.iam_policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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
        request: Optional[iam_policy_pb2.GetIamPolicyRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM access control policy for a function.

        Returns an empty policy if the function exists and does not have a
        policy set.

        Args:
            request (:class:`~.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if
                any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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
        request: Optional[iam_policy_pb2.TestIamPermissionsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the specified IAM permissions against the IAM access control
            policy for a function.

        If the function does not exist, this will return an empty set
        of permissions, not a NOT_FOUND error.

        Args:
            request (:class:`~.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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


__all__ = ("DataformClient",)
