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
    Dict,
    Iterable,
    Iterator,
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

from google.cloud.storage_client_v2 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.storage_client_v2.services.storage import pagers
from google.cloud.storage_client_v2.types import storage

from .transports.base import DEFAULT_CLIENT_INFO, StorageTransport
from .transports.grpc import StorageGrpcTransport
from .transports.grpc_asyncio import StorageGrpcAsyncIOTransport


class StorageClientMeta(type):
    """Metaclass for the Storage client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[StorageTransport]]
    _transport_registry["grpc"] = StorageGrpcTransport
    _transport_registry["grpc_asyncio"] = StorageGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[StorageTransport]:
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


class StorageClient(metaclass=StorageClientMeta):
    """API Overview and Naming Syntax
    ------------------------------

    The Cloud Storage gRPC API allows applications to read and write
    data through the abstractions of buckets and objects. For a
    description of these abstractions please see
    https://cloud.google.com/storage/docs.

    Resources are named as follows:

    -  Projects are referred to as they are defined by the Resource
       Manager API, using strings like ``projects/123456`` or
       ``projects/my-string-id``.

    -  Buckets are named using string names of the form:
       ``projects/{project}/buckets/{bucket}`` For globally unique
       buckets, ``_`` may be substituted for the project.

    -  Objects are uniquely identified by their name along with the name
       of the bucket they belong to, as separate strings in this API.
       For example:

       ReadObjectRequest { bucket: 'projects/_/buckets/my-bucket'
       object: 'my-object' } Note that object names can contain ``/``
       characters, which are treated as any other character (no special
       directory semantics).
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
    DEFAULT_ENDPOINT = "storage.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "storage.{UNIVERSE_DOMAIN}"
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
            StorageClient: The constructed client.
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
            StorageClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> StorageTransport:
        """Returns the transport used by the client instance.

        Returns:
            StorageTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def bucket_path(
        project: str,
        bucket: str,
    ) -> str:
        """Returns a fully-qualified bucket string."""
        return "projects/{project}/buckets/{bucket}".format(
            project=project,
            bucket=bucket,
        )

    @staticmethod
    def parse_bucket_path(path: str) -> Dict[str, str]:
        """Parses a bucket path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/buckets/(?P<bucket>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
    ) -> str:
        """Returns a fully-qualified crypto_key string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
        )

    @staticmethod
    def parse_crypto_key_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def notification_config_path(
        project: str,
        bucket: str,
        notification_config: str,
    ) -> str:
        """Returns a fully-qualified notification_config string."""
        return "projects/{project}/buckets/{bucket}/notificationConfigs/{notification_config}".format(
            project=project,
            bucket=bucket,
            notification_config=notification_config,
        )

    @staticmethod
    def parse_notification_config_path(path: str) -> Dict[str, str]:
        """Parses a notification_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/buckets/(?P<bucket>.+?)/notificationConfigs/(?P<notification_config>.+?)$",
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
            _default_universe = StorageClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = StorageClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = StorageClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = StorageClient._DEFAULT_UNIVERSE
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

        default_universe = StorageClient._DEFAULT_UNIVERSE
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
            or StorageClient._compare_universes(
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
        transport: Optional[Union[str, StorageTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the storage client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, StorageTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
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
        ) = StorageClient._read_environment_variables()
        self._client_cert_source = StorageClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = StorageClient._get_universe_domain(
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
        transport_provided = isinstance(transport, StorageTransport)
        if transport_provided:
            # transport is a StorageTransport instance.
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
            self._transport = cast(StorageTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or StorageClient._get_api_endpoint(
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

            Transport = type(self).get_transport_class(cast(str, transport))
            self._transport = Transport(
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

    def delete_bucket(
        self,
        request: Optional[Union[storage.DeleteBucketRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes an empty bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_delete_bucket():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.DeleteBucketRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_bucket(request=request)

        Args:
            request (Union[google.cloud.storage_client_v2.types.DeleteBucketRequest, dict]):
                The request object. Request message for DeleteBucket.
            name (str):
                Required. Name of a bucket to delete.
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.DeleteBucketRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.DeleteBucketRequest):
            request = storage.DeleteBucketRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_bucket]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def get_bucket(
        self,
        request: Optional[Union[storage.GetBucketRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Bucket:
        r"""Returns metadata for the specified bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_get_bucket():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.GetBucketRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_bucket(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.GetBucketRequest, dict]):
                The request object. Request message for GetBucket.
            name (str):
                Required. Name of a bucket.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Bucket:
                A bucket.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.GetBucketRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.GetBucketRequest):
            request = storage.GetBucketRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_bucket]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def create_bucket(
        self,
        request: Optional[Union[storage.CreateBucketRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        bucket: Optional[storage.Bucket] = None,
        bucket_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Bucket:
        r"""Creates a new bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_create_bucket():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.CreateBucketRequest(
                    parent="parent_value",
                    bucket_id="bucket_id_value",
                )

                # Make the request
                response = client.create_bucket(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.CreateBucketRequest, dict]):
                The request object. Request message for CreateBucket.
            parent (str):
                Required. The project to which this
                bucket will belong.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bucket (google.cloud.storage_client_v2.types.Bucket):
                Properties of the new bucket being inserted. The name of
                the bucket is specified in the ``bucket_id`` field.
                Populating ``bucket.name`` field will result in an
                error. The project of the bucket must be specified in
                the ``bucket.project`` field. This field must be in
                ``projects/{projectIdentifier}`` format,
                {projectIdentifier} can be the project ID or project
                number. The ``parent`` field must be either empty or
                ``projects/_``.

                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bucket_id (str):
                Required. The ID to use for this bucket, which will
                become the final component of the bucket's resource
                name. For example, the value ``foo`` might result in a
                bucket with the name ``projects/123456/buckets/foo``.

                This corresponds to the ``bucket_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Bucket:
                A bucket.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, bucket, bucket_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.CreateBucketRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.CreateBucketRequest):
            request = storage.CreateBucketRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if bucket is not None:
                request.bucket = bucket
            if bucket_id is not None:
                request.bucket_id = bucket_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_bucket]

        header_params = {}

        routing_param_regex = re.compile("^(?P<project>.*)$")
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("project"):
            header_params["project"] = regex_match.group("project")

        routing_param_regex = re.compile("^(?P<project>.*)$")
        regex_match = routing_param_regex.match(request.bucket.project)
        if regex_match and regex_match.group("project"):
            header_params["project"] = regex_match.group("project")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def list_buckets(
        self,
        request: Optional[Union[storage.ListBucketsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBucketsPager:
        r"""Retrieves a list of buckets for a given project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_list_buckets():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.ListBucketsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_buckets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.ListBucketsRequest, dict]):
                The request object. Request message for ListBuckets.
            parent (str):
                Required. The project whose buckets
                we are listing.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.services.storage.pagers.ListBucketsPager:
                The result of a call to
                Buckets.ListBuckets
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ListBucketsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ListBucketsRequest):
            request = storage.ListBucketsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_buckets]

        header_params = {}

        routing_param_regex = re.compile("^(?P<project>.*)$")
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("project"):
            header_params["project"] = regex_match.group("project")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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
        response = pagers.ListBucketsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def lock_bucket_retention_policy(
        self,
        request: Optional[Union[storage.LockBucketRetentionPolicyRequest, dict]] = None,
        *,
        bucket: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Bucket:
        r"""Locks retention policy on a bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_lock_bucket_retention_policy():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.LockBucketRetentionPolicyRequest(
                    bucket="bucket_value",
                    if_metageneration_match=2413,
                )

                # Make the request
                response = client.lock_bucket_retention_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.LockBucketRetentionPolicyRequest, dict]):
                The request object. Request message for
                LockBucketRetentionPolicyRequest.
            bucket (str):
                Required. Name of a bucket.
                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Bucket:
                A bucket.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bucket])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.LockBucketRetentionPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.LockBucketRetentionPolicyRequest):
            request = storage.LockBucketRetentionPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bucket is not None:
                request.bucket = bucket

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.lock_bucket_retention_policy
        ]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM policy for a specified bucket. The ``resource``
        field in the request should be ``projects/_/buckets/{bucket}``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = storage_client_v2.StorageClient()

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
            resource (str):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.resource)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Updates an IAM policy for the specified bucket. The ``resource``
        field in the request should be ``projects/_/buckets/{bucket}``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = storage_client_v2.StorageClient()

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
            resource (str):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.resource)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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
        resource: Optional[str] = None,
        permissions: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests a set of permissions on the given bucket or object to see
        which, if any, are held by the caller. The ``resource`` field in
        the request should be ``projects/_/buckets/{bucket}`` for a
        bucket or ``projects/_/buckets/{bucket}/objects/{object}`` for
        an object.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = storage_client_v2.StorageClient()

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
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (MutableSequence[str]):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.resource)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        routing_param_regex = re.compile(
            "^(?P<bucket>projects/[^/]+/buckets/[^/]+)/objects(?:/.*)?$"
        )
        regex_match = routing_param_regex.match(request.resource)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def update_bucket(
        self,
        request: Optional[Union[storage.UpdateBucketRequest, dict]] = None,
        *,
        bucket: Optional[storage.Bucket] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Bucket:
        r"""Updates a bucket. Equivalent to JSON API's
        storage.buckets.patch method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_update_bucket():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.UpdateBucketRequest(
                )

                # Make the request
                response = client.update_bucket(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.UpdateBucketRequest, dict]):
                The request object. Request for UpdateBucket method.
            bucket (google.cloud.storage_client_v2.types.Bucket):
                Required. The bucket to update. The bucket's ``name``
                field will be used to identify the bucket.

                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. List of fields to be updated.

                To specify ALL fields, equivalent to the JSON API's
                "update" function, specify a single field with the value
                ``*``. Note: not recommended. If a new field is
                introduced at a later time, an older client updating
                with the ``*`` may accidentally reset the new field's
                value.

                Not specifying any fields is an error.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Bucket:
                A bucket.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bucket, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.UpdateBucketRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.UpdateBucketRequest):
            request = storage.UpdateBucketRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bucket is not None:
                request.bucket = bucket
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_bucket]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.bucket.name)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def delete_notification_config(
        self,
        request: Optional[Union[storage.DeleteNotificationConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes a NotificationConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_delete_notification_config():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.DeleteNotificationConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_notification_config(request=request)

        Args:
            request (Union[google.cloud.storage_client_v2.types.DeleteNotificationConfigRequest, dict]):
                The request object. Request message for
                DeleteNotificationConfig.
            name (str):
                Required. The parent bucket of the
                NotificationConfig.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.DeleteNotificationConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.DeleteNotificationConfigRequest):
            request = storage.DeleteNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_notification_config
        ]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<bucket>projects/[^/]+/buckets/[^/]+)(?:/.*)?$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def get_notification_config(
        self,
        request: Optional[Union[storage.GetNotificationConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.NotificationConfig:
        r"""View a NotificationConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_get_notification_config():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.GetNotificationConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_notification_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.GetNotificationConfigRequest, dict]):
                The request object. Request message for
                GetNotificationConfig.
            name (str):
                Required. The parent bucket of the NotificationConfig.
                Format:
                ``projects/{project}/buckets/{bucket}/notificationConfigs/{notificationConfig}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.NotificationConfig:
                A directive to publish Pub/Sub
                notifications upon changes to a bucket.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.GetNotificationConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.GetNotificationConfigRequest):
            request = storage.GetNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_notification_config]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<bucket>projects/[^/]+/buckets/[^/]+)(?:/.*)?$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def create_notification_config(
        self,
        request: Optional[Union[storage.CreateNotificationConfigRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        notification_config: Optional[storage.NotificationConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.NotificationConfig:
        r"""Creates a NotificationConfig for a given bucket.
        These NotificationConfigs, when triggered, publish
        messages to the specified Pub/Sub topics. See
        https://cloud.google.com/storage/docs/pubsub-notifications.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_create_notification_config():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                notification_config = storage_client_v2.NotificationConfig()
                notification_config.name = "name_value"
                notification_config.topic = "topic_value"
                notification_config.payload_format = "payload_format_value"

                request = storage_client_v2.CreateNotificationConfigRequest(
                    parent="parent_value",
                    notification_config=notification_config,
                )

                # Make the request
                response = client.create_notification_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.CreateNotificationConfigRequest, dict]):
                The request object. Request message for
                CreateNotificationConfig.
            parent (str):
                Required. The bucket to which this
                NotificationConfig belongs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notification_config (google.cloud.storage_client_v2.types.NotificationConfig):
                Required. Properties of the
                NotificationConfig to be inserted.

                This corresponds to the ``notification_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.NotificationConfig:
                A directive to publish Pub/Sub
                notifications upon changes to a bucket.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, notification_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.CreateNotificationConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.CreateNotificationConfigRequest):
            request = storage.CreateNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if notification_config is not None:
                request.notification_config = notification_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_notification_config
        ]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def list_notification_configs(
        self,
        request: Optional[Union[storage.ListNotificationConfigsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotificationConfigsPager:
        r"""Retrieves a list of NotificationConfigs for a given
        bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_list_notification_configs():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.ListNotificationConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_notification_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.ListNotificationConfigsRequest, dict]):
                The request object. Request message for
                ListNotifications.
            parent (str):
                Required. Name of a Google Cloud
                Storage bucket.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.services.storage.pagers.ListNotificationConfigsPager:
                The result of a call to
                ListNotificationConfigs
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ListNotificationConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ListNotificationConfigsRequest):
            request = storage.ListNotificationConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_notification_configs
        ]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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
        response = pagers.ListNotificationConfigsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def compose_object(
        self,
        request: Optional[Union[storage.ComposeObjectRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Object:
        r"""Concatenates a list of existing objects into a new
        object in the same bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_compose_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.ComposeObjectRequest(
                )

                # Make the request
                response = client.compose_object(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.ComposeObjectRequest, dict]):
                The request object. Request message for ComposeObject.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Object:
                An object.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ComposeObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ComposeObjectRequest):
            request = storage.ComposeObjectRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.compose_object]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.destination.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def delete_object(
        self,
        request: Optional[Union[storage.DeleteObjectRequest, dict]] = None,
        *,
        bucket: Optional[str] = None,
        object_: Optional[str] = None,
        generation: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an object and its metadata.

        Deletions are normally permanent when versioning is
        disabled or whenever the generation parameter is used.
        However, if soft delete is enabled for the bucket,
        deleted objects can be restored using RestoreObject
        until the soft delete retention period has passed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_delete_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.DeleteObjectRequest(
                    bucket="bucket_value",
                    object_="object__value",
                )

                # Make the request
                client.delete_object(request=request)

        Args:
            request (Union[google.cloud.storage_client_v2.types.DeleteObjectRequest, dict]):
                The request object. Message for deleting an object. ``bucket`` and
                ``object`` **must** be set.
            bucket (str):
                Required. Name of the bucket in which
                the object resides.

                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            object_ (str):
                Required. The name of the finalized object to delete.
                Note: If you want to delete an unfinalized resumable
                upload please use ``CancelResumableWrite``.

                This corresponds to the ``object_`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            generation (int):
                If present, permanently deletes a
                specific revision of this object (as
                opposed to the latest version, the
                default).

                This corresponds to the ``generation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bucket, object_, generation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.DeleteObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.DeleteObjectRequest):
            request = storage.DeleteObjectRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bucket is not None:
                request.bucket = bucket
            if object_ is not None:
                request.object_ = object_
            if generation is not None:
                request.generation = generation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_object]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def restore_object(
        self,
        request: Optional[Union[storage.RestoreObjectRequest, dict]] = None,
        *,
        bucket: Optional[str] = None,
        object_: Optional[str] = None,
        generation: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Object:
        r"""Restores a soft-deleted object.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_restore_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.RestoreObjectRequest(
                    bucket="bucket_value",
                    object_="object__value",
                    generation=1068,
                )

                # Make the request
                response = client.restore_object(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.RestoreObjectRequest, dict]):
                The request object. Message for restoring an object. ``bucket``, ``object``,
                and ``generation`` **must** be set.
            bucket (str):
                Required. Name of the bucket in which
                the object resides.

                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            object_ (str):
                Required. The name of the object to
                restore.

                This corresponds to the ``object_`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            generation (int):
                Required. The specific revision of
                the object to restore.

                This corresponds to the ``generation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Object:
                An object.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bucket, object_, generation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.RestoreObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.RestoreObjectRequest):
            request = storage.RestoreObjectRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bucket is not None:
                request.bucket = bucket
            if object_ is not None:
                request.object_ = object_
            if generation is not None:
                request.generation = generation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restore_object]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def cancel_resumable_write(
        self,
        request: Optional[Union[storage.CancelResumableWriteRequest, dict]] = None,
        *,
        upload_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.CancelResumableWriteResponse:
        r"""Cancels an in-progress resumable upload.

        Any attempts to write to the resumable upload after
        cancelling the upload will fail.

        The behavior for currently in progress write operations
        is not guaranteed - they could either complete before
        the cancellation or fail if the cancellation completes
        first.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_cancel_resumable_write():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.CancelResumableWriteRequest(
                    upload_id="upload_id_value",
                )

                # Make the request
                response = client.cancel_resumable_write(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.CancelResumableWriteRequest, dict]):
                The request object. Message for canceling an in-progress resumable upload.
                ``upload_id`` **must** be set.
            upload_id (str):
                Required. The upload_id of the resumable upload to
                cancel. This should be copied from the ``upload_id``
                field of ``StartResumableWriteResponse``.

                This corresponds to the ``upload_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.CancelResumableWriteResponse:
                Empty response message for canceling
                an in-progress resumable upload, will be
                extended as needed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([upload_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.CancelResumableWriteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.CancelResumableWriteRequest):
            request = storage.CancelResumableWriteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if upload_id is not None:
                request.upload_id = upload_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_resumable_write]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<bucket>projects/[^/]+/buckets/[^/]+)(?:/.*)?$"
        )
        regex_match = routing_param_regex.match(request.upload_id)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def get_object(
        self,
        request: Optional[Union[storage.GetObjectRequest, dict]] = None,
        *,
        bucket: Optional[str] = None,
        object_: Optional[str] = None,
        generation: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Object:
        r"""Retrieves an object's metadata.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_get_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.GetObjectRequest(
                    bucket="bucket_value",
                    object_="object__value",
                )

                # Make the request
                response = client.get_object(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.GetObjectRequest, dict]):
                The request object. Request message for GetObject.
            bucket (str):
                Required. Name of the bucket in which
                the object resides.

                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            object_ (str):
                Required. Name of the object.
                This corresponds to the ``object_`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            generation (int):
                If present, selects a specific
                revision of this object (as opposed to
                the latest version, the default).

                This corresponds to the ``generation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Object:
                An object.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bucket, object_, generation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.GetObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.GetObjectRequest):
            request = storage.GetObjectRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bucket is not None:
                request.bucket = bucket
            if object_ is not None:
                request.object_ = object_
            if generation is not None:
                request.generation = generation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_object]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def read_object(
        self,
        request: Optional[Union[storage.ReadObjectRequest, dict]] = None,
        *,
        bucket: Optional[str] = None,
        object_: Optional[str] = None,
        generation: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[storage.ReadObjectResponse]:
        r"""Reads an object's data.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_read_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.ReadObjectRequest(
                    bucket="bucket_value",
                    object_="object__value",
                )

                # Make the request
                stream = client.read_object(request=request)

                # Handle the response
                for response in stream:
                    print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.ReadObjectRequest, dict]):
                The request object. Request message for ReadObject.
            bucket (str):
                Required. The name of the bucket
                containing the object to read.

                This corresponds to the ``bucket`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            object_ (str):
                Required. The name of the object to
                read.

                This corresponds to the ``object_`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            generation (int):
                If present, selects a specific
                revision of this object (as opposed to
                the latest version, the default).

                This corresponds to the ``generation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.storage_client_v2.types.ReadObjectResponse]:
                Response message for ReadObject.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bucket, object_, generation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ReadObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ReadObjectRequest):
            request = storage.ReadObjectRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bucket is not None:
                request.bucket = bucket
            if object_ is not None:
                request.object_ = object_
            if generation is not None:
                request.generation = generation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_object]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def update_object(
        self,
        request: Optional[Union[storage.UpdateObjectRequest, dict]] = None,
        *,
        object_: Optional[storage.Object] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.Object:
        r"""Updates an object's metadata.
        Equivalent to JSON API's storage.objects.patch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_update_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.UpdateObjectRequest(
                )

                # Make the request
                response = client.update_object(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.UpdateObjectRequest, dict]):
                The request object. Request message for UpdateObject.
            object_ (google.cloud.storage_client_v2.types.Object):
                Required. The object to update.
                The object's bucket and name fields are
                used to identify the object to update.
                If present, the object's generation
                field selects a specific revision of
                this object whose metadata should be
                updated. Otherwise, assumes the live
                version of the object.

                This corresponds to the ``object_`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. List of fields to be updated.

                To specify ALL fields, equivalent to the JSON API's
                "update" function, specify a single field with the value
                ``*``. Note: not recommended. If a new field is
                introduced at a later time, an older client updating
                with the ``*`` may accidentally reset the new field's
                value.

                Not specifying any fields is an error.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.Object:
                An object.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([object_, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.UpdateObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.UpdateObjectRequest):
            request = storage.UpdateObjectRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if object_ is not None:
                request.object_ = object_
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_object]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.object.bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def write_object(
        self,
        requests: Optional[Iterator[storage.WriteObjectRequest]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.WriteObjectResponse:
        r"""Stores a new object and metadata.

        An object can be written either in a single message stream or in
        a resumable sequence of message streams. To write using a single
        stream, the client should include in the first message of the
        stream an ``WriteObjectSpec`` describing the destination bucket,
        object, and any preconditions. Additionally, the final message
        must set 'finish_write' to true, or else it is an error.

        For a resumable write, the client should instead call
        ``StartResumableWrite()``, populating a ``WriteObjectSpec`` into
        that request. They should then attach the returned ``upload_id``
        to the first message of each following call to ``WriteObject``.
        If the stream is closed before finishing the upload (either
        explicitly by the client or due to a network error or an error
        response from the server), the client should do as follows:

        -  Check the result Status of the stream, to determine if
           writing can be resumed on this stream or must be restarted
           from scratch (by calling ``StartResumableWrite()``). The
           resumable errors are DEADLINE_EXCEEDED, INTERNAL, and
           UNAVAILABLE. For each case, the client should use binary
           exponential backoff before retrying. Additionally, writes can
           be resumed after RESOURCE_EXHAUSTED errors, but only after
           taking appropriate measures, which may include reducing
           aggregate send rate across clients and/or requesting a quota
           increase for your project.
        -  If the call to ``WriteObject`` returns ``ABORTED``, that
           indicates concurrent attempts to update the resumable write,
           caused either by multiple racing clients or by a single
           client where the previous request was timed out on the client
           side but nonetheless reached the server. In this case the
           client should take steps to prevent further concurrent writes
           (e.g., increase the timeouts, stop using more than one
           process to perform the upload, etc.), and then should follow
           the steps below for resuming the upload.
        -  For resumable errors, the client should call
           ``QueryWriteStatus()`` and then continue writing from the
           returned ``persisted_size``. This may be less than the amount
           of data the client previously sent. Note also that it is
           acceptable to send data starting at an offset earlier than
           the returned ``persisted_size``; in this case, the service
           will skip data at offsets that were already persisted
           (without checking that it matches the previously written
           data), and write only the data starting from the persisted
           offset. Even though the data isn't written, it may still
           incur a performance cost over resuming at the correct write
           offset. This behavior can make client-side handling simpler
           in some cases.
        -  Clients must only send data that is a multiple of 256 KiB per
           message, unless the object is being finished with
           ``finish_write`` set to ``true``.

        The service will not view the object as complete until the
        client has sent a ``WriteObjectRequest`` with ``finish_write``
        set to ``true``. Sending any requests on a stream after sending
        a request with ``finish_write`` set to ``true`` will cause an
        error. The client **should** check the response it receives to
        determine how much data the service was able to commit and
        whether the service views the object as complete.

        Attempting to resume an already finalized object will result in
        an OK status, with a WriteObjectResponse containing the
        finalized object's metadata.

        Alternatively, the BidiWriteObject operation may be used to
        write an object with controls over flushing and the ability to
        fetch the ability to determine the current persisted size.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_write_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.WriteObjectRequest(
                    upload_id="upload_id_value",
                    write_offset=1297,
                )

                # This method expects an iterator which contains
                # 'storage_client_v2.WriteObjectRequest' objects
                # Here we create a generator that yields a single `request` for
                # demonstrative purposes.
                requests = [request]

                def request_generator():
                    for request in requests:
                        yield request

                # Make the request
                response = client.write_object(requests=request_generator())

                # Handle the response
                print(response)

        Args:
            requests (Iterator[google.cloud.storage_client_v2.types.WriteObjectRequest]):
                The request object iterator. Request message for WriteObject.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.WriteObjectResponse:
                Response message for WriteObject.
        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.write_object]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            requests,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def bidi_write_object(
        self,
        requests: Optional[Iterator[storage.BidiWriteObjectRequest]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[storage.BidiWriteObjectResponse]:
        r"""Stores a new object and metadata.

        This is similar to the WriteObject call with the added support
        for manual flushing of persisted state, and the ability to
        determine current persisted size without closing the stream.

        The client may specify one or both of the ``state_lookup`` and
        ``flush`` fields in each BidiWriteObjectRequest. If ``flush`` is
        specified, the data written so far will be persisted to storage.
        If ``state_lookup`` is specified, the service will respond with
        a BidiWriteObjectResponse that contains the persisted size. If
        both ``flush`` and ``state_lookup`` are specified, the flush
        will always occur before a ``state_lookup``, so that both may be
        set in the same request and the returned state will be the state
        of the object post-flush. When the stream is closed, a
        BidiWriteObjectResponse will always be sent to the client,
        regardless of the value of ``state_lookup``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_bidi_write_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.BidiWriteObjectRequest(
                    upload_id="upload_id_value",
                    write_offset=1297,
                )

                # This method expects an iterator which contains
                # 'storage_client_v2.BidiWriteObjectRequest' objects
                # Here we create a generator that yields a single `request` for
                # demonstrative purposes.
                requests = [request]

                def request_generator():
                    for request in requests:
                        yield request

                # Make the request
                stream = client.bidi_write_object(requests=request_generator())

                # Handle the response
                for response in stream:
                    print(response)

        Args:
            requests (Iterator[google.cloud.storage_client_v2.types.BidiWriteObjectRequest]):
                The request object iterator. Request message for BidiWriteObject.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.storage_client_v2.types.BidiWriteObjectResponse]:
                Response message for BidiWriteObject.
        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bidi_write_object]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            requests,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_objects(
        self,
        request: Optional[Union[storage.ListObjectsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListObjectsPager:
        r"""Retrieves a list of objects matching the criteria.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_list_objects():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.ListObjectsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_objects(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.ListObjectsRequest, dict]):
                The request object. Request message for ListObjects.
            parent (str):
                Required. Name of the bucket in which
                to look for objects.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.services.storage.pagers.ListObjectsPager:
                The result of a call to
                Objects.ListObjects
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ListObjectsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ListObjectsRequest):
            request = storage.ListObjectsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_objects]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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
        response = pagers.ListObjectsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def rewrite_object(
        self,
        request: Optional[Union[storage.RewriteObjectRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.RewriteResponse:
        r"""Rewrites a source object to a destination object.
        Optionally overrides metadata.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_rewrite_object():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.RewriteObjectRequest(
                    destination_name="destination_name_value",
                    destination_bucket="destination_bucket_value",
                    source_bucket="source_bucket_value",
                    source_object="source_object_value",
                )

                # Make the request
                response = client.rewrite_object(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.RewriteObjectRequest, dict]):
                The request object. Request message for RewriteObject. If the source object
                is encrypted using a Customer-Supplied Encryption Key
                the key information must be provided in the
                copy_source_encryption_algorithm,
                copy_source_encryption_key_bytes, and
                copy_source_encryption_key_sha256_bytes fields. If the
                destination object should be encrypted the keying
                information should be provided in the
                encryption_algorithm, encryption_key_bytes, and
                encryption_key_sha256_bytes fields of the
                common_object_request_params.customer_encryption field.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.RewriteResponse:
                A rewrite response.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a storage.RewriteObjectRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.RewriteObjectRequest):
            request = storage.RewriteObjectRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.rewrite_object]

        header_params = {}

        if request.source_bucket:
            header_params["source_bucket"] = request.source_bucket

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(request.destination_bucket)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def start_resumable_write(
        self,
        request: Optional[Union[storage.StartResumableWriteRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.StartResumableWriteResponse:
        r"""Starts a resumable write. How long the write
        operation remains valid, and what happens when the write
        operation becomes invalid, are service-dependent.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_start_resumable_write():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.StartResumableWriteRequest(
                )

                # Make the request
                response = client.start_resumable_write(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.StartResumableWriteRequest, dict]):
                The request object. Request message StartResumableWrite.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.StartResumableWriteResponse:
                Response object for StartResumableWrite.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a storage.StartResumableWriteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.StartResumableWriteRequest):
            request = storage.StartResumableWriteRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_resumable_write]

        header_params = {}

        routing_param_regex = re.compile("^(?P<bucket>.*)$")
        regex_match = routing_param_regex.match(
            request.write_object_spec.resource.bucket
        )
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def query_write_status(
        self,
        request: Optional[Union[storage.QueryWriteStatusRequest, dict]] = None,
        *,
        upload_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.QueryWriteStatusResponse:
        r"""Determines the ``persisted_size`` for an object that is being
        written, which can then be used as the ``write_offset`` for the
        next ``Write()`` call.

        If the object does not exist (i.e., the object has been deleted,
        or the first ``Write()`` has not yet reached the service), this
        method returns the error ``NOT_FOUND``.

        The client **may** call ``QueryWriteStatus()`` at any time to
        determine how much data has been processed for this object. This
        is useful if the client is buffering data and needs to know
        which data can be safely evicted. For any sequence of
        ``QueryWriteStatus()`` calls for a given object name, the
        sequence of returned ``persisted_size`` values will be
        non-decreasing.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_query_write_status():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.QueryWriteStatusRequest(
                    upload_id="upload_id_value",
                )

                # Make the request
                response = client.query_write_status(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.QueryWriteStatusRequest, dict]):
                The request object. Request object for ``QueryWriteStatus``.
            upload_id (str):
                Required. The name of the resume
                token for the object whose write status
                is being requested.

                This corresponds to the ``upload_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.QueryWriteStatusResponse:
                Response object for QueryWriteStatus.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([upload_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.QueryWriteStatusRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.QueryWriteStatusRequest):
            request = storage.QueryWriteStatusRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if upload_id is not None:
                request.upload_id = upload_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.query_write_status]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<bucket>projects/[^/]+/buckets/[^/]+)(?:/.*)?$"
        )
        regex_match = routing_param_regex.match(request.upload_id)
        if regex_match and regex_match.group("bucket"):
            header_params["bucket"] = regex_match.group("bucket")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def get_service_account(
        self,
        request: Optional[Union[storage.GetServiceAccountRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.ServiceAccount:
        r"""Retrieves the name of a project's Google Cloud
        Storage service account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_get_service_account():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.GetServiceAccountRequest(
                    project="project_value",
                )

                # Make the request
                response = client.get_service_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.GetServiceAccountRequest, dict]):
                The request object. Request message for
                GetServiceAccount.
            project (str):
                Required. Project ID, in the format
                of "projects/{projectIdentifier}".
                {projectIdentifier} can be the project
                ID or project number.

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.ServiceAccount:
                A service account, owned by Cloud
                Storage, which may be used when taking
                action on behalf of a given project, for
                example to publish Pub/Sub notifications
                or to retrieve security keys.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.GetServiceAccountRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.GetServiceAccountRequest):
            request = storage.GetServiceAccountRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_service_account]

        header_params = {}

        if request.project:
            header_params["project"] = request.project

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def create_hmac_key(
        self,
        request: Optional[Union[storage.CreateHmacKeyRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        service_account_email: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.CreateHmacKeyResponse:
        r"""Creates a new HMAC key for the given service account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_create_hmac_key():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.CreateHmacKeyRequest(
                    project="project_value",
                    service_account_email="service_account_email_value",
                )

                # Make the request
                response = client.create_hmac_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.CreateHmacKeyRequest, dict]):
                The request object. Request message for CreateHmacKey.
            project (str):
                Required. The project that the
                HMAC-owning service account lives in, in
                the format of
                "projects/{projectIdentifier}".
                {projectIdentifier} can be the project
                ID or project number.

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_account_email (str):
                Required. The service account to
                create the HMAC for.

                This corresponds to the ``service_account_email`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.CreateHmacKeyResponse:
                Create hmac response.  The only time
                the secret for an HMAC will be returned.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, service_account_email])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.CreateHmacKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.CreateHmacKeyRequest):
            request = storage.CreateHmacKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if service_account_email is not None:
                request.service_account_email = service_account_email

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_hmac_key]

        header_params = {}

        if request.project:
            header_params["project"] = request.project

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def delete_hmac_key(
        self,
        request: Optional[Union[storage.DeleteHmacKeyRequest, dict]] = None,
        *,
        access_id: Optional[str] = None,
        project: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a given HMAC key.  Key must be in an INACTIVE
        state.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_delete_hmac_key():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.DeleteHmacKeyRequest(
                    access_id="access_id_value",
                    project="project_value",
                )

                # Make the request
                client.delete_hmac_key(request=request)

        Args:
            request (Union[google.cloud.storage_client_v2.types.DeleteHmacKeyRequest, dict]):
                The request object. Request object to delete a given HMAC
                key.
            access_id (str):
                Required. The identifying key for the
                HMAC to delete.

                This corresponds to the ``access_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            project (str):
                Required. The project that owns the
                HMAC key, in the format of
                "projects/{projectIdentifier}".
                {projectIdentifier} can be the project
                ID or project number.

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([access_id, project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.DeleteHmacKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.DeleteHmacKeyRequest):
            request = storage.DeleteHmacKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if access_id is not None:
                request.access_id = access_id
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_hmac_key]

        header_params = {}

        if request.project:
            header_params["project"] = request.project

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def get_hmac_key(
        self,
        request: Optional[Union[storage.GetHmacKeyRequest, dict]] = None,
        *,
        access_id: Optional[str] = None,
        project: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.HmacKeyMetadata:
        r"""Gets an existing HMAC key metadata for the given id.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_get_hmac_key():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.GetHmacKeyRequest(
                    access_id="access_id_value",
                    project="project_value",
                )

                # Make the request
                response = client.get_hmac_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.GetHmacKeyRequest, dict]):
                The request object. Request object to get metadata on a
                given HMAC key.
            access_id (str):
                Required. The identifying key for the
                HMAC to delete.

                This corresponds to the ``access_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            project (str):
                Required. The project the HMAC key
                lies in, in the format of
                "projects/{projectIdentifier}".
                {projectIdentifier} can be the project
                ID or project number.

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.HmacKeyMetadata:
                Hmac Key Metadata, which includes all
                information other than the secret.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([access_id, project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.GetHmacKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.GetHmacKeyRequest):
            request = storage.GetHmacKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if access_id is not None:
                request.access_id = access_id
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_hmac_key]

        header_params = {}

        if request.project:
            header_params["project"] = request.project

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def list_hmac_keys(
        self,
        request: Optional[Union[storage.ListHmacKeysRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListHmacKeysPager:
        r"""Lists HMAC keys under a given project with the
        additional filters provided.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_list_hmac_keys():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.ListHmacKeysRequest(
                    project="project_value",
                )

                # Make the request
                page_result = client.list_hmac_keys(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.ListHmacKeysRequest, dict]):
                The request object. Request to fetch a list of HMAC keys
                under a given project.
            project (str):
                Required. The project to list HMAC
                keys for, in the format of
                "projects/{projectIdentifier}".
                {projectIdentifier} can be the project
                ID or project number.

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.services.storage.pagers.ListHmacKeysPager:
                Hmac key list response with next page
                information.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ListHmacKeysRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ListHmacKeysRequest):
            request = storage.ListHmacKeysRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_hmac_keys]

        header_params = {}

        if request.project:
            header_params["project"] = request.project

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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
        response = pagers.ListHmacKeysPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_hmac_key(
        self,
        request: Optional[Union[storage.UpdateHmacKeyRequest, dict]] = None,
        *,
        hmac_key: Optional[storage.HmacKeyMetadata] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.HmacKeyMetadata:
        r"""Updates a given HMAC key state between ACTIVE and
        INACTIVE.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_client_v2

            def sample_update_hmac_key():
                # Create a client
                client = storage_client_v2.StorageClient()

                # Initialize request argument(s)
                request = storage_client_v2.UpdateHmacKeyRequest(
                )

                # Make the request
                response = client.update_hmac_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_client_v2.types.UpdateHmacKeyRequest, dict]):
                The request object. Request object to update an HMAC key
                state. HmacKeyMetadata.state is required
                and the only writable field in
                UpdateHmacKey operation. Specifying
                fields other than state will result in
                an error.
            hmac_key (google.cloud.storage_client_v2.types.HmacKeyMetadata):
                Required. The HMAC key to update. If present, the
                hmac_key's ``id`` field will be used to identify the
                key. Otherwise, the hmac_key's access_id and project
                fields will be used to identify the key.

                This corresponds to the ``hmac_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Update mask for hmac_key. Not specifying any fields will
                mean only the ``state`` field is updated to the value
                specified in ``hmac_key``.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_client_v2.types.HmacKeyMetadata:
                Hmac Key Metadata, which includes all
                information other than the secret.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([hmac_key, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.UpdateHmacKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.UpdateHmacKeyRequest):
            request = storage.UpdateHmacKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if hmac_key is not None:
                request.hmac_key = hmac_key
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_hmac_key]

        header_params = {}

        routing_param_regex = re.compile("^(?P<project>.*)$")
        regex_match = routing_param_regex.match(request.hmac_key.project)
        if regex_match and regex_match.group("project"):
            header_params["project"] = regex_match.group("project")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
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

    def __enter__(self) -> "StorageClient":
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


__all__ = ("StorageClient",)
