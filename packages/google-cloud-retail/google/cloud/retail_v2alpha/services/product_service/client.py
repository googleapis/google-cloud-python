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

from google.cloud.retail_v2alpha import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

from google.cloud.retail_v2alpha.services.product_service import pagers
from google.cloud.retail_v2alpha.types import common, export_config, import_config
from google.cloud.retail_v2alpha.types import product_service, promotion, purge_config
from google.cloud.retail_v2alpha.types import product
from google.cloud.retail_v2alpha.types import product as gcr_product

from .transports.base import DEFAULT_CLIENT_INFO, ProductServiceTransport
from .transports.grpc import ProductServiceGrpcTransport
from .transports.grpc_asyncio import ProductServiceGrpcAsyncIOTransport
from .transports.rest import ProductServiceRestTransport


class ProductServiceClientMeta(type):
    """Metaclass for the ProductService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ProductServiceTransport]]
    _transport_registry["grpc"] = ProductServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ProductServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = ProductServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ProductServiceTransport]:
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


class ProductServiceClient(metaclass=ProductServiceClientMeta):
    """Service for ingesting [Product][google.cloud.retail.v2alpha.Product]
    information of the customer's website.
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
    DEFAULT_ENDPOINT = "retail.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "retail.{UNIVERSE_DOMAIN}"
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
            ProductServiceClient: The constructed client.
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
            ProductServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ProductServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ProductServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def branch_path(
        project: str,
        location: str,
        catalog: str,
        branch: str,
    ) -> str:
        """Returns a fully-qualified branch string."""
        return "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}".format(
            project=project,
            location=location,
            catalog=catalog,
            branch=branch,
        )

    @staticmethod
    def parse_branch_path(path: str) -> Dict[str, str]:
        """Parses a branch path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/catalogs/(?P<catalog>.+?)/branches/(?P<branch>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def product_path(
        project: str,
        location: str,
        catalog: str,
        branch: str,
        product: str,
    ) -> str:
        """Returns a fully-qualified product string."""
        return "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}/products/{product}".format(
            project=project,
            location=location,
            catalog=catalog,
            branch=branch,
            product=product,
        )

    @staticmethod
    def parse_product_path(path: str) -> Dict[str, str]:
        """Parses a product path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/catalogs/(?P<catalog>.+?)/branches/(?P<branch>.+?)/products/(?P<product>.+?)$",
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
            _default_universe = ProductServiceClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = ProductServiceClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = ProductServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = ProductServiceClient._DEFAULT_UNIVERSE
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

        default_universe = ProductServiceClient._DEFAULT_UNIVERSE
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
            or ProductServiceClient._compare_universes(
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
            Union[str, ProductServiceTransport, Callable[..., ProductServiceTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the product service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ProductServiceTransport,Callable[..., ProductServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ProductServiceTransport constructor.
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
        ) = ProductServiceClient._read_environment_variables()
        self._client_cert_source = ProductServiceClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = ProductServiceClient._get_universe_domain(
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
        transport_provided = isinstance(transport, ProductServiceTransport)
        if transport_provided:
            # transport is a ProductServiceTransport instance.
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
            self._transport = cast(ProductServiceTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or ProductServiceClient._get_api_endpoint(
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
                Type[ProductServiceTransport], Callable[..., ProductServiceTransport]
            ] = (
                ProductServiceClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., ProductServiceTransport], transport)
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

    def create_product(
        self,
        request: Optional[Union[product_service.CreateProductRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        product: Optional[gcr_product.Product] = None,
        product_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_product.Product:
        r"""Creates a [Product][google.cloud.retail.v2alpha.Product].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_create_product():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                product = retail_v2alpha.Product()
                product.title = "title_value"

                request = retail_v2alpha.CreateProductRequest(
                    parent="parent_value",
                    product=product,
                    product_id="product_id_value",
                )

                # Make the request
                response = client.create_product(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.CreateProductRequest, dict]):
                The request object. Request message for
                [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
                method.
            parent (str):
                Required. The parent catalog resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product (google.cloud.retail_v2alpha.types.Product):
                Required. The
                [Product][google.cloud.retail.v2alpha.Product] to
                create.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product_id (str):
                Required. The ID to use for the
                [Product][google.cloud.retail.v2alpha.Product], which
                will become the final component of the
                [Product.name][google.cloud.retail.v2alpha.Product.name].

                If the caller does not have permission to create the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                This field must be unique among all
                [Product][google.cloud.retail.v2alpha.Product]s with the
                same
                [parent][google.cloud.retail.v2alpha.CreateProductRequest.parent].
                Otherwise, an ALREADY_EXISTS error is returned.

                This field must be a UTF-8 encoded string with a length
                limit of 128 characters. Otherwise, an INVALID_ARGUMENT
                error is returned.

                This corresponds to the ``product_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2alpha.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, product, product_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.CreateProductRequest):
            request = product_service.CreateProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if product is not None:
                request.product = product
            if product_id is not None:
                request.product_id = product_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_product]

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

    def get_product(
        self,
        request: Optional[Union[product_service.GetProductRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product.Product:
        r"""Gets a [Product][google.cloud.retail.v2alpha.Product].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_get_product():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.GetProductRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_product(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.GetProductRequest, dict]):
                The request object. Request message for
                [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
                method.
            name (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2alpha.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                If the requested
                [Product][google.cloud.retail.v2alpha.Product] does not
                exist, a NOT_FOUND error is returned.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2alpha.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

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
        if not isinstance(request, product_service.GetProductRequest):
            request = product_service.GetProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_product]

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

    def list_products(
        self,
        request: Optional[Union[product_service.ListProductsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProductsPager:
        r"""Gets a list of [Product][google.cloud.retail.v2alpha.Product]s.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_list_products():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.ListProductsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_products(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.ListProductsRequest, dict]):
                The request object. Request message for
                [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts]
                method.
            parent (str):
                Required. The parent branch resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/0``.
                Use ``default_branch`` as the branch ID, to list
                products under the default branch.

                If the caller does not have permission to list
                [Product][google.cloud.retail.v2alpha.Product]s under
                this branch, regardless of whether or not this branch
                exists, a PERMISSION_DENIED error is returned.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2alpha.services.product_service.pagers.ListProductsPager:
                Response message for
                   [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts]
                   method.

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
        if not isinstance(request, product_service.ListProductsRequest):
            request = product_service.ListProductsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_products]

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
        response = pagers.ListProductsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_product(
        self,
        request: Optional[Union[product_service.UpdateProductRequest, dict]] = None,
        *,
        product: Optional[gcr_product.Product] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_product.Product:
        r"""Updates a [Product][google.cloud.retail.v2alpha.Product].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_update_product():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                product = retail_v2alpha.Product()
                product.title = "title_value"

                request = retail_v2alpha.UpdateProductRequest(
                    product=product,
                )

                # Make the request
                response = client.update_product(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.UpdateProductRequest, dict]):
                The request object. Request message for
                [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
                method.
            product (google.cloud.retail_v2alpha.types.Product):
                Required. The product to update/create.

                If the caller does not have permission to update the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                If the [Product][google.cloud.retail.v2alpha.Product] to
                update does not exist and
                [allow_missing][google.cloud.retail.v2alpha.UpdateProductRequest.allow_missing]
                is not set, a NOT_FOUND error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Indicates which fields in the provided
                [Product][google.cloud.retail.v2alpha.Product] to
                update. The immutable and output only fields are NOT
                supported. If not set, all supported fields (the fields
                that are neither immutable nor output only) are updated.

                If an unsupported or unknown field is provided, an
                INVALID_ARGUMENT error is returned.

                The attribute key can be updated by setting the mask
                path as "attributes.${key_name}". If a key name is
                present in the mask but not in the patching product from
                the request, this key will be deleted after the update.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2alpha.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([product, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.UpdateProductRequest):
            request = product_service.UpdateProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_product]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("product.name", request.product.name),)
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

    def delete_product(
        self,
        request: Optional[Union[product_service.DeleteProductRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a [Product][google.cloud.retail.v2alpha.Product].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_delete_product():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.DeleteProductRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_product(request=request)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.DeleteProductRequest, dict]):
                The request object. Request message for
                [ProductService.DeleteProduct][google.cloud.retail.v2alpha.ProductService.DeleteProduct]
                method.
            name (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2alpha.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to delete the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                If the [Product][google.cloud.retail.v2alpha.Product] to
                delete does not exist, a NOT_FOUND error is returned.

                The [Product][google.cloud.retail.v2alpha.Product] to
                delete can neither be a
                [Product.Type.COLLECTION][google.cloud.retail.v2alpha.Product.Type.COLLECTION]
                [Product][google.cloud.retail.v2alpha.Product] member
                nor a
                [Product.Type.PRIMARY][google.cloud.retail.v2alpha.Product.Type.PRIMARY]
                [Product][google.cloud.retail.v2alpha.Product] with more
                than one
                [variants][google.cloud.retail.v2alpha.Product.Type.VARIANT].
                Otherwise, an INVALID_ARGUMENT error is returned.

                All inventory information for the named
                [Product][google.cloud.retail.v2alpha.Product] will be
                deleted.

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
        if not isinstance(request, product_service.DeleteProductRequest):
            request = product_service.DeleteProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_product]

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

    def purge_products(
        self,
        request: Optional[Union[purge_config.PurgeProductsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Permanently deletes all selected
        [Product][google.cloud.retail.v2alpha.Product]s under a branch.

        This process is asynchronous. If the request is valid, the
        removal will be enqueued and processed offline. Depending on the
        number of [Product][google.cloud.retail.v2alpha.Product]s, this
        operation could take hours to complete. Before the operation
        completes, some [Product][google.cloud.retail.v2alpha.Product]s
        may still be returned by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        Depending on the number of
        [Product][google.cloud.retail.v2alpha.Product]s, this operation
        could take hours to complete. To get a sample of
        [Product][google.cloud.retail.v2alpha.Product]s that would be
        deleted, set
        [PurgeProductsRequest.force][google.cloud.retail.v2alpha.PurgeProductsRequest.force]
        to false.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_purge_products():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.PurgeProductsRequest(
                    parent="parent_value",
                    filter="filter_value",
                )

                # Make the request
                operation = client.purge_products(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.PurgeProductsRequest, dict]):
                The request object. Request message for PurgeProducts
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.PurgeProductsResponse` Response of the PurgeProductsRequest. If the long running operation is
                   successfully done, then this message is returned by
                   the google.longrunning.Operations.response field.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, purge_config.PurgeProductsRequest):
            request = purge_config.PurgeProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.purge_products]

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
            purge_config.PurgeProductsResponse,
            metadata_type=purge_config.PurgeProductsMetadata,
        )

        # Done; return the response.
        return response

    def import_products(
        self,
        request: Optional[Union[import_config.ImportProductsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Bulk import of multiple
        [Product][google.cloud.retail.v2alpha.Product]s.

        Request processing may be synchronous. Non-existing items are
        created.

        Note that it is possible for a subset of the
        [Product][google.cloud.retail.v2alpha.Product]s to be
        successfully updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_import_products():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                input_config = retail_v2alpha.ProductInputConfig()
                input_config.product_inline_source.products.title = "title_value"

                request = retail_v2alpha.ImportProductsRequest(
                    parent="parent_value",
                    input_config=input_config,
                )

                # Make the request
                operation = client.import_products(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.ImportProductsRequest, dict]):
                The request object. Request message for Import methods.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.ImportProductsResponse` Response of the
                   [ImportProductsRequest][google.cloud.retail.v2alpha.ImportProductsRequest].
                   If the long running operation is done, then this
                   message is returned by the
                   google.longrunning.Operations.response field if the
                   operation was successful.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, import_config.ImportProductsRequest):
            request = import_config.ImportProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_products]

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
            import_config.ImportProductsResponse,
            metadata_type=import_config.ImportMetadata,
        )

        # Done; return the response.
        return response

    def export_products(
        self,
        request: Optional[Union[export_config.ExportProductsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Exports multiple
        [Product][google.cloud.retail.v2alpha.Product]s.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_export_products():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                output_config = retail_v2alpha.OutputConfig()
                output_config.gcs_destination.output_uri_prefix = "output_uri_prefix_value"

                request = retail_v2alpha.ExportProductsRequest(
                    parent="parent_value",
                    output_config=output_config,
                )

                # Make the request
                operation = client.export_products(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.ExportProductsRequest, dict]):
                The request object. Request message for ExportProducts
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.ExportProductsResponse` Response of the ExportProductsRequest. If the long running
                   operation is done, then this message is returned by
                   the google.longrunning.Operations.response field if
                   the operation was successful.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, export_config.ExportProductsRequest):
            request = export_config.ExportProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_products]

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
            export_config.ExportProductsResponse,
            metadata_type=export_config.ExportMetadata,
        )

        # Done; return the response.
        return response

    def set_inventory(
        self,
        request: Optional[Union[product_service.SetInventoryRequest, dict]] = None,
        *,
        inventory: Optional[product.Product] = None,
        set_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates inventory information for a
        [Product][google.cloud.retail.v2alpha.Product] while respecting
        the last update timestamps of each inventory field.

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update is enqueued and processed downstream. As a consequence,
        when a response is returned, updates are not immediately
        manifested in the [Product][google.cloud.retail.v2alpha.Product]
        queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        When inventory is updated with
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        and
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct],
        the specified inventory field value(s) overwrite any existing
        value(s) while ignoring the last update time for this field.
        Furthermore, the last update times for the specified inventory
        fields are overwritten by the times of the
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        or
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
        request.

        If no inventory fields are set in
        [CreateProductRequest.product][google.cloud.retail.v2alpha.CreateProductRequest.product],
        then any pre-existing inventory information for this product is
        used.

        If no inventory fields are set in
        [SetInventoryRequest.set_mask][google.cloud.retail.v2alpha.SetInventoryRequest.set_mask],
        then any existing inventory information is preserved.

        Pre-existing inventory information can only be updated with
        [ProductService.SetInventory][google.cloud.retail.v2alpha.ProductService.SetInventory],
        [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces],
        and
        [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces].

        The returned [Operation][google.longrunning.Operation]s is
        obsolete after one day, and the
        [GetOperation][google.longrunning.Operations.GetOperation] API
        returns ``NOT_FOUND`` afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates are not marked as
        [done][google.longrunning.Operation.done] until they are
        obsolete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_set_inventory():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                inventory = retail_v2alpha.Product()
                inventory.title = "title_value"

                request = retail_v2alpha.SetInventoryRequest(
                    inventory=inventory,
                )

                # Make the request
                operation = client.set_inventory(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.SetInventoryRequest, dict]):
                The request object. Request message for
                [ProductService.SetInventory][google.cloud.retail.v2alpha.ProductService.SetInventory]
                method.
            inventory (google.cloud.retail_v2alpha.types.Product):
                Required. The inventory information to update. The
                allowable fields to update are:

                -  [Product.price_info][google.cloud.retail.v2alpha.Product.price_info]
                -  [Product.availability][google.cloud.retail.v2alpha.Product.availability]
                -  [Product.available_quantity][google.cloud.retail.v2alpha.Product.available_quantity]
                -  [Product.fulfillment_info][google.cloud.retail.v2alpha.Product.fulfillment_info]
                   The updated inventory fields must be specified in
                   [SetInventoryRequest.set_mask][google.cloud.retail.v2alpha.SetInventoryRequest.set_mask].

                If
                [SetInventoryRequest.inventory.name][google.cloud.retail.v2alpha.Product.name]
                is empty or invalid, an INVALID_ARGUMENT error is
                returned.

                If the caller does not have permission to update the
                [Product][google.cloud.retail.v2alpha.Product] named in
                [Product.name][google.cloud.retail.v2alpha.Product.name],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                If the [Product][google.cloud.retail.v2alpha.Product] to
                update does not have existing inventory information, the
                provided inventory information will be inserted.

                If the [Product][google.cloud.retail.v2alpha.Product] to
                update has existing inventory information, the provided
                inventory information will be merged while respecting
                the last update time for each inventory field, using the
                provided or default value for
                [SetInventoryRequest.set_time][google.cloud.retail.v2alpha.SetInventoryRequest.set_time].

                The caller can replace place IDs for a subset of
                fulfillment types in the following ways:

                -  Adds "fulfillment_info" in
                   [SetInventoryRequest.set_mask][google.cloud.retail.v2alpha.SetInventoryRequest.set_mask]
                -  Specifies only the desired fulfillment types and
                   corresponding place IDs to update in
                   [SetInventoryRequest.inventory.fulfillment_info][google.cloud.retail.v2alpha.Product.fulfillment_info]

                The caller can clear all place IDs from a subset of
                fulfillment types in the following ways:

                -  Adds "fulfillment_info" in
                   [SetInventoryRequest.set_mask][google.cloud.retail.v2alpha.SetInventoryRequest.set_mask]
                -  Specifies only the desired fulfillment types to clear
                   in
                   [SetInventoryRequest.inventory.fulfillment_info][google.cloud.retail.v2alpha.Product.fulfillment_info]
                -  Checks that only the desired fulfillment info types
                   have empty
                   [SetInventoryRequest.inventory.fulfillment_info.place_ids][google.cloud.retail.v2alpha.FulfillmentInfo.place_ids]

                The last update time is recorded for the following
                inventory fields:

                -  [Product.price_info][google.cloud.retail.v2alpha.Product.price_info]
                -  [Product.availability][google.cloud.retail.v2alpha.Product.availability]
                -  [Product.available_quantity][google.cloud.retail.v2alpha.Product.available_quantity]
                -  [Product.fulfillment_info][google.cloud.retail.v2alpha.Product.fulfillment_info]

                If a full overwrite of inventory information while
                ignoring timestamps is needed,
                [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
                should be invoked instead.

                This corresponds to the ``inventory`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            set_mask (google.protobuf.field_mask_pb2.FieldMask):
                Indicates which inventory fields in the provided
                [Product][google.cloud.retail.v2alpha.Product] to
                update.

                At least one field must be provided.

                If an unsupported or unknown field is provided, an
                INVALID_ARGUMENT error is returned and the entire update
                will be ignored.

                This corresponds to the ``set_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.SetInventoryResponse` Response of the SetInventoryRequest. Currently empty because
                   there is no meaningful response populated from the
                   [ProductService.SetInventory][google.cloud.retail.v2alpha.ProductService.SetInventory]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([inventory, set_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.SetInventoryRequest):
            request = product_service.SetInventoryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if inventory is not None:
                request.inventory = inventory
            if set_mask is not None:
                request.set_mask = set_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_inventory]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("inventory.name", request.inventory.name),)
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
            product_service.SetInventoryResponse,
            metadata_type=product_service.SetInventoryMetadata,
        )

        # Done; return the response.
        return response

    def add_fulfillment_places(
        self,
        request: Optional[
            Union[product_service.AddFulfillmentPlacesRequest, dict]
        ] = None,
        *,
        product: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""We recommend that you use the
        [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
        method instead of the
        [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces]
        method.
        [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
        achieves the same results but provides more fine-grained control
        over ingesting local inventory data.

        Incrementally adds place IDs to
        [Product.fulfillment_info.place_ids][google.cloud.retail.v2alpha.FulfillmentInfo.place_ids].

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, the added place IDs
        are not immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_add_fulfillment_places():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.AddFulfillmentPlacesRequest(
                    product="product_value",
                    type_="type__value",
                    place_ids=['place_ids_value1', 'place_ids_value2'],
                )

                # Make the request
                operation = client.add_fulfillment_places(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.AddFulfillmentPlacesRequest, dict]):
                The request object. Request message for
                [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces]
                method.
            product (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2alpha.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.AddFulfillmentPlacesResponse` Response of the AddFulfillmentPlacesRequest. Currently empty because
                   there is no meaningful response populated from the
                   [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([product])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.AddFulfillmentPlacesRequest):
            request = product_service.AddFulfillmentPlacesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_fulfillment_places]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("product", request.product),)),
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
            product_service.AddFulfillmentPlacesResponse,
            metadata_type=product_service.AddFulfillmentPlacesMetadata,
        )

        # Done; return the response.
        return response

    def remove_fulfillment_places(
        self,
        request: Optional[
            Union[product_service.RemoveFulfillmentPlacesRequest, dict]
        ] = None,
        *,
        product: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""We recommend that you use the
        [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
        method instead of the
        [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces]
        method.
        [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
        achieves the same results but provides more fine-grained control
        over ingesting local inventory data.

        Incrementally removes place IDs from a
        [Product.fulfillment_info.place_ids][google.cloud.retail.v2alpha.FulfillmentInfo.place_ids].

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, the removed place IDs
        are not immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_remove_fulfillment_places():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.RemoveFulfillmentPlacesRequest(
                    product="product_value",
                    type_="type__value",
                    place_ids=['place_ids_value1', 'place_ids_value2'],
                )

                # Make the request
                operation = client.remove_fulfillment_places(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.RemoveFulfillmentPlacesRequest, dict]):
                The request object. Request message for
                [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces]
                method.
            product (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2alpha.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.RemoveFulfillmentPlacesResponse` Response of the RemoveFulfillmentPlacesRequest. Currently empty because there
                   is no meaningful response populated from the
                   [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([product])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.RemoveFulfillmentPlacesRequest):
            request = product_service.RemoveFulfillmentPlacesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.remove_fulfillment_places
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("product", request.product),)),
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
            product_service.RemoveFulfillmentPlacesResponse,
            metadata_type=product_service.RemoveFulfillmentPlacesMetadata,
        )

        # Done; return the response.
        return response

    def add_local_inventories(
        self,
        request: Optional[
            Union[product_service.AddLocalInventoriesRequest, dict]
        ] = None,
        *,
        product: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates local inventory information for a
        [Product][google.cloud.retail.v2alpha.Product] at a list of
        places, while respecting the last update timestamps of each
        inventory field.

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating inventory information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, updates are not
        immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        Local inventory information can only be modified using this
        method.
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        and
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
        has no effect on local inventories.

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_add_local_inventories():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.AddLocalInventoriesRequest(
                    product="product_value",
                )

                # Make the request
                operation = client.add_local_inventories(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.AddLocalInventoriesRequest, dict]):
                The request object. Request message for
                [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
                method.
            product (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2alpha.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.AddLocalInventoriesResponse` Response of the
                   [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
                   API. Currently empty because there is no meaningful
                   response populated from the
                   [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([product])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.AddLocalInventoriesRequest):
            request = product_service.AddLocalInventoriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_local_inventories]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("product", request.product),)),
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
            product_service.AddLocalInventoriesResponse,
            metadata_type=product_service.AddLocalInventoriesMetadata,
        )

        # Done; return the response.
        return response

    def remove_local_inventories(
        self,
        request: Optional[
            Union[product_service.RemoveLocalInventoriesRequest, dict]
        ] = None,
        *,
        product: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Remove local inventory information for a
        [Product][google.cloud.retail.v2alpha.Product] at a list of
        places at a removal timestamp.

        This process is asynchronous. If the request is valid, the
        removal will be enqueued and processed downstream. As a
        consequence, when a response is returned, removals are not
        immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        Local inventory information can only be removed using this
        method.
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        and
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
        has no effect on local inventories.

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            def sample_remove_local_inventories():
                # Create a client
                client = retail_v2alpha.ProductServiceClient()

                # Initialize request argument(s)
                request = retail_v2alpha.RemoveLocalInventoriesRequest(
                    product="product_value",
                    place_ids=['place_ids_value1', 'place_ids_value2'],
                )

                # Make the request
                operation = client.remove_local_inventories(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2alpha.types.RemoveLocalInventoriesRequest, dict]):
                The request object. Request message for
                [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
                method.
            product (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2alpha.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2alpha.Product],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.RemoveLocalInventoriesResponse` Response of the
                   [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
                   API. Currently empty because there is no meaningful
                   response populated from the
                   [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([product])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, product_service.RemoveLocalInventoriesRequest):
            request = product_service.RemoveLocalInventoriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_local_inventories]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("product", request.product),)),
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
            product_service.RemoveLocalInventoriesResponse,
            metadata_type=product_service.RemoveLocalInventoriesMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ProductServiceClient":
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
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
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

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
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


__all__ = ("ProductServiceClient",)
