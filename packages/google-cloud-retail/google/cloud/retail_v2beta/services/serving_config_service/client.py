# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore

from google.cloud.retail_v2beta.services.serving_config_service import pagers
from google.cloud.retail_v2beta.types import serving_config as gcr_serving_config
from google.cloud.retail_v2beta.types import common, search_service
from google.cloud.retail_v2beta.types import serving_config
from google.cloud.retail_v2beta.types import serving_config_service

from .transports.base import DEFAULT_CLIENT_INFO, ServingConfigServiceTransport
from .transports.grpc import ServingConfigServiceGrpcTransport
from .transports.grpc_asyncio import ServingConfigServiceGrpcAsyncIOTransport


class ServingConfigServiceClientMeta(type):
    """Metaclass for the ServingConfigService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ServingConfigServiceTransport]]
    _transport_registry["grpc"] = ServingConfigServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ServingConfigServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[ServingConfigServiceTransport]:
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


class ServingConfigServiceClient(metaclass=ServingConfigServiceClientMeta):
    """Service for modifying ServingConfig."""

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

    DEFAULT_ENDPOINT = "retail.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ServingConfigServiceClient: The constructed client.
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
            ServingConfigServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ServingConfigServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ServingConfigServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def catalog_path(
        project: str,
        location: str,
        catalog: str,
    ) -> str:
        """Returns a fully-qualified catalog string."""
        return "projects/{project}/locations/{location}/catalogs/{catalog}".format(
            project=project,
            location=location,
            catalog=catalog,
        )

    @staticmethod
    def parse_catalog_path(path: str) -> Dict[str, str]:
        """Parses a catalog path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/catalogs/(?P<catalog>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def serving_config_path(
        project: str,
        location: str,
        catalog: str,
        serving_config: str,
    ) -> str:
        """Returns a fully-qualified serving_config string."""
        return "projects/{project}/locations/{location}/catalogs/{catalog}/servingConfigs/{serving_config}".format(
            project=project,
            location=location,
            catalog=catalog,
            serving_config=serving_config,
        )

    @staticmethod
    def parse_serving_config_path(path: str) -> Dict[str, str]:
        """Parses a serving_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/catalogs/(?P<catalog>.+?)/servingConfigs/(?P<serving_config>.+?)$",
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
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
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

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, ServingConfigServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the serving config service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ServingConfigServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ServingConfigServiceTransport):
            # transport is a ServingConfigServiceTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def create_serving_config(
        self,
        request: Union[serving_config_service.CreateServingConfigRequest, dict] = None,
        *,
        parent: str = None,
        serving_config: gcr_serving_config.ServingConfig = None,
        serving_config_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_serving_config.ServingConfig:
        r"""Creates a ServingConfig.

        A maximum of 100
        [ServingConfig][google.cloud.retail.v2beta.ServingConfig]s are
        allowed in a [Catalog][google.cloud.retail.v2beta.Catalog],
        otherwise a FAILED_PRECONDITION error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_create_serving_config():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                serving_config = retail_v2beta.ServingConfig()
                serving_config.display_name = "display_name_value"
                serving_config.solution_types = "SOLUTION_TYPE_SEARCH"

                request = retail_v2beta.CreateServingConfigRequest(
                    parent="parent_value",
                    serving_config=serving_config,
                    serving_config_id="serving_config_id_value",
                )

                # Make the request
                response = client.create_serving_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.CreateServingConfigRequest, dict]):
                The request object. Request for CreateServingConfig
                method.
            parent (str):
                Required. Full resource name of parent. Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            serving_config (google.cloud.retail_v2beta.types.ServingConfig):
                Required. The ServingConfig to
                create.

                This corresponds to the ``serving_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            serving_config_id (str):
                Required. The ID to use for the ServingConfig, which
                will become the final component of the ServingConfig's
                resource name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-_/.

                This corresponds to the ``serving_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.ServingConfig:
                Configures metadata that is used to generate serving time results (e.g.
                   search results or recommendation predictions). The
                   ServingConfig is passed in the search and predict
                   request and together with the Catalog.default_branch,
                   generates results.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, serving_config, serving_config_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a serving_config_service.CreateServingConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.CreateServingConfigRequest):
            request = serving_config_service.CreateServingConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if serving_config is not None:
                request.serving_config = serving_config
            if serving_config_id is not None:
                request.serving_config_id = serving_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_serving_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_serving_config(
        self,
        request: Union[serving_config_service.DeleteServingConfigRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ServingConfig.
        Returns a NotFound error if the ServingConfig does not
        exist.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_delete_serving_config():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                request = retail_v2beta.DeleteServingConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_serving_config(request=request)

        Args:
            request (Union[google.cloud.retail_v2beta.types.DeleteServingConfigRequest, dict]):
                The request object. Request for DeleteServingConfig
                method.
            name (str):
                Required. The resource name of the ServingConfig to
                delete. Format:
                projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/servingConfigs/{serving_config_id}

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
        # in a serving_config_service.DeleteServingConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.DeleteServingConfigRequest):
            request = serving_config_service.DeleteServingConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_serving_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_serving_config(
        self,
        request: Union[serving_config_service.UpdateServingConfigRequest, dict] = None,
        *,
        serving_config: gcr_serving_config.ServingConfig = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_serving_config.ServingConfig:
        r"""Updates a ServingConfig.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_update_serving_config():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                serving_config = retail_v2beta.ServingConfig()
                serving_config.display_name = "display_name_value"
                serving_config.solution_types = "SOLUTION_TYPE_SEARCH"

                request = retail_v2beta.UpdateServingConfigRequest(
                    serving_config=serving_config,
                )

                # Make the request
                response = client.update_serving_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.UpdateServingConfigRequest, dict]):
                The request object. Request for UpdateServingConfig
                method.
            serving_config (google.cloud.retail_v2beta.types.ServingConfig):
                Required. The ServingConfig to
                update.

                This corresponds to the ``serving_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Indicates which fields in the provided
                [ServingConfig][google.cloud.retail.v2beta.ServingConfig]
                to update. The following are NOT supported:

                -  [ServingConfig.name][google.cloud.retail.v2beta.ServingConfig.name]

                If not set, all supported fields are updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.ServingConfig:
                Configures metadata that is used to generate serving time results (e.g.
                   search results or recommendation predictions). The
                   ServingConfig is passed in the search and predict
                   request and together with the Catalog.default_branch,
                   generates results.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([serving_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a serving_config_service.UpdateServingConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.UpdateServingConfigRequest):
            request = serving_config_service.UpdateServingConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if serving_config is not None:
                request.serving_config = serving_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_serving_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("serving_config.name", request.serving_config.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_serving_config(
        self,
        request: Union[serving_config_service.GetServingConfigRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> serving_config.ServingConfig:
        r"""Gets a ServingConfig.
        Returns a NotFound error if the ServingConfig does not
        exist.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_get_serving_config():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                request = retail_v2beta.GetServingConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_serving_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.GetServingConfigRequest, dict]):
                The request object. Request for GetServingConfig method.
            name (str):
                Required. The resource name of the ServingConfig to get.
                Format:
                projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/servingConfigs/{serving_config_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.ServingConfig:
                Configures metadata that is used to generate serving time results (e.g.
                   search results or recommendation predictions). The
                   ServingConfig is passed in the search and predict
                   request and together with the Catalog.default_branch,
                   generates results.

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
        # in a serving_config_service.GetServingConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.GetServingConfigRequest):
            request = serving_config_service.GetServingConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_serving_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_serving_configs(
        self,
        request: Union[serving_config_service.ListServingConfigsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServingConfigsPager:
        r"""Lists all ServingConfigs linked to this catalog.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_list_serving_configs():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                request = retail_v2beta.ListServingConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_serving_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.ListServingConfigsRequest, dict]):
                The request object. Request for ListServingConfigs
                method.
            parent (str):
                Required. The catalog resource name. Format:
                projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.services.serving_config_service.pagers.ListServingConfigsPager:
                Response for ListServingConfigs
                method.
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
        # in a serving_config_service.ListServingConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.ListServingConfigsRequest):
            request = serving_config_service.ListServingConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_serving_configs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServingConfigsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def add_control(
        self,
        request: Union[serving_config_service.AddControlRequest, dict] = None,
        *,
        serving_config: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_serving_config.ServingConfig:
        r"""Enables a Control on the specified ServingConfig. The control is
        added in the last position of the list of controls it belongs to
        (e.g. if it's a facet spec control it will be applied in the
        last position of servingConfig.facetSpecIds) Returns a
        ALREADY_EXISTS error if the control has already been applied.
        Returns a FAILED_PRECONDITION error if the addition could exceed
        maximum number of control allowed for that type of control.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_add_control():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                request = retail_v2beta.AddControlRequest(
                    serving_config="serving_config_value",
                    control_id="control_id_value",
                )

                # Make the request
                response = client.add_control(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.AddControlRequest, dict]):
                The request object. Request for AddControl method.
            serving_config (str):
                Required. The source ServingConfig resource name .
                Format:
                projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/servingConfigs/{serving_config_id}

                This corresponds to the ``serving_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.ServingConfig:
                Configures metadata that is used to generate serving time results (e.g.
                   search results or recommendation predictions). The
                   ServingConfig is passed in the search and predict
                   request and together with the Catalog.default_branch,
                   generates results.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([serving_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a serving_config_service.AddControlRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.AddControlRequest):
            request = serving_config_service.AddControlRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if serving_config is not None:
                request.serving_config = serving_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_control]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("serving_config", request.serving_config),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_control(
        self,
        request: Union[serving_config_service.RemoveControlRequest, dict] = None,
        *,
        serving_config: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_serving_config.ServingConfig:
        r"""Disables a Control on the specified ServingConfig. The control
        is removed from the ServingConfig. Returns a NOT_FOUND error if
        the Control is not enabled for the ServingConfig.

        .. code-block:: python

            from google.cloud import retail_v2beta

            def sample_remove_control():
                # Create a client
                client = retail_v2beta.ServingConfigServiceClient()

                # Initialize request argument(s)
                request = retail_v2beta.RemoveControlRequest(
                    serving_config="serving_config_value",
                    control_id="control_id_value",
                )

                # Make the request
                response = client.remove_control(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.RemoveControlRequest, dict]):
                The request object. Request for RemoveControl method.
            serving_config (str):
                Required. The source ServingConfig resource name .
                Format:
                projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/servingConfigs/{serving_config_id}

                This corresponds to the ``serving_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.ServingConfig:
                Configures metadata that is used to generate serving time results (e.g.
                   search results or recommendation predictions). The
                   ServingConfig is passed in the search and predict
                   request and together with the Catalog.default_branch,
                   generates results.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([serving_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a serving_config_service.RemoveControlRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, serving_config_service.RemoveControlRequest):
            request = serving_config_service.RemoveControlRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if serving_config is not None:
                request.serving_config = serving_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_control]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("serving_config", request.serving_config),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-retail",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ServingConfigServiceClient",)
