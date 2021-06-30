# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources
import warnings

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.bigquery_datatransfer_v1.services.data_transfer_service import pagers
from google.cloud.bigquery_datatransfer_v1.types import datatransfer
from google.cloud.bigquery_datatransfer_v1.types import transfer
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import DataTransferServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DataTransferServiceGrpcTransport
from .transports.grpc_asyncio import DataTransferServiceGrpcAsyncIOTransport


class DataTransferServiceClientMeta(type):
    """Metaclass for the DataTransferService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[DataTransferServiceTransport]]
    _transport_registry["grpc"] = DataTransferServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = DataTransferServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[DataTransferServiceTransport]:
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


class DataTransferServiceClient(metaclass=DataTransferServiceClientMeta):
    """The Google BigQuery Data Transfer Service API enables
    BigQuery users to configure the transfer of their data from
    other Google Products into BigQuery. This service contains
    methods that are end user exposed. It backs up the frontend.
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

    DEFAULT_ENDPOINT = "bigquerydatatransfer.googleapis.com"
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
            DataTransferServiceClient: The constructed client.
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
            DataTransferServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataTransferServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataTransferServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def data_source_path(project: str, data_source: str,) -> str:
        """Returns a fully-qualified data_source string."""
        return "projects/{project}/dataSources/{data_source}".format(
            project=project, data_source=data_source,
        )

    @staticmethod
    def parse_data_source_path(path: str) -> Dict[str, str]:
        """Parses a data_source path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/dataSources/(?P<data_source>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def run_path(project: str, transfer_config: str, run: str,) -> str:
        """Returns a fully-qualified run string."""
        return "projects/{project}/transferConfigs/{transfer_config}/runs/{run}".format(
            project=project, transfer_config=transfer_config, run=run,
        )

    @staticmethod
    def parse_run_path(path: str) -> Dict[str, str]:
        """Parses a run path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/transferConfigs/(?P<transfer_config>.+?)/runs/(?P<run>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def transfer_config_path(project: str, transfer_config: str,) -> str:
        """Returns a fully-qualified transfer_config string."""
        return "projects/{project}/transferConfigs/{transfer_config}".format(
            project=project, transfer_config=transfer_config,
        )

    @staticmethod
    def parse_transfer_config_path(path: str) -> Dict[str, str]:
        """Parses a transfer_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/transferConfigs/(?P<transfer_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
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
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, DataTransferServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the data transfer service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DataTransferServiceTransport]): The
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

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, DataTransferServiceTransport):
            # transport is a DataTransferServiceTransport instance.
            if credentials or client_options.credentials_file:
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
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def get_data_source(
        self,
        request: datatransfer.GetDataSourceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datatransfer.DataSource:
        r"""Retrieves a supported data source and returns its
        settings, which can be used for UI rendering.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.GetDataSourceRequest):
                The request object. A request to get data source info.
            name (str):
                Required. The field will contain name of the resource
                requested, for example:
                ``projects/{project_id}/dataSources/{data_source_id}``
                or
                ``projects/{project_id}/locations/{location_id}/dataSources/{data_source_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.DataSource:
                Represents data source metadata.
                Metadata is sufficient to render UI and
                request proper OAuth tokens.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.GetDataSourceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.GetDataSourceRequest):
            request = datatransfer.GetDataSourceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_data_source]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_data_sources(
        self,
        request: datatransfer.ListDataSourcesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataSourcesPager:
        r"""Lists supported data sources and returns their
        settings, which can be used for UI rendering.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesRequest):
                The request object. Request to list supported data
                sources and their data transfer settings.
            parent (str):
                Required. The BigQuery project id for which data sources
                should be returned. Must be in the form:
                ``projects/{project_id}`` or
                \`projects/{project_id}/locations/{location_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.pagers.ListDataSourcesPager:
                Returns list of supported data
                sources and their metadata.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.ListDataSourcesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.ListDataSourcesRequest):
            request = datatransfer.ListDataSourcesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_data_sources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDataSourcesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_transfer_config(
        self,
        request: datatransfer.CreateTransferConfigRequest = None,
        *,
        parent: str = None,
        transfer_config: transfer.TransferConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer.TransferConfig:
        r"""Creates a new data transfer configuration.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.CreateTransferConfigRequest):
                The request object. A request to create a data transfer
                configuration. If new credentials are needed for this
                transfer configuration, an authorization code must be
                provided. If an authorization code is provided, the
                transfer configuration will be associated with the user
                id corresponding to the authorization code. Otherwise,
                the transfer configuration will be associated with the
                calling user.
            parent (str):
                Required. The BigQuery project id where the transfer
                configuration should be created. Must be in the format
                projects/{project_id}/locations/{location_id} or
                projects/{project_id}. If specified location and
                location of the destination bigquery dataset do not
                match - the request will fail.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transfer_config (google.cloud.bigquery_datatransfer_v1.types.TransferConfig):
                Required. Data transfer configuration
                to create.

                This corresponds to the ``transfer_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.TransferConfig:
                Represents a data transfer configuration. A transfer configuration
                   contains all metadata needed to perform a data
                   transfer. For example, destination_dataset_id
                   specifies where data should be stored. When a new
                   transfer configuration is created, the specified
                   destination_dataset_id is created when needed and
                   shared with the appropriate data source service
                   account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, transfer_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.CreateTransferConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.CreateTransferConfigRequest):
            request = datatransfer.CreateTransferConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if transfer_config is not None:
                request.transfer_config = transfer_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_transfer_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_transfer_config(
        self,
        request: datatransfer.UpdateTransferConfigRequest = None,
        *,
        transfer_config: transfer.TransferConfig = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer.TransferConfig:
        r"""Updates a data transfer configuration.
        All fields must be set, even if they are not updated.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.UpdateTransferConfigRequest):
                The request object. A request to update a transfer
                configuration. To update the user id of the transfer
                configuration, an authorization code needs to be
                provided.
            transfer_config (google.cloud.bigquery_datatransfer_v1.types.TransferConfig):
                Required. Data transfer configuration
                to create.

                This corresponds to the ``transfer_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Required list of fields to
                be updated in this request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.TransferConfig:
                Represents a data transfer configuration. A transfer configuration
                   contains all metadata needed to perform a data
                   transfer. For example, destination_dataset_id
                   specifies where data should be stored. When a new
                   transfer configuration is created, the specified
                   destination_dataset_id is created when needed and
                   shared with the appropriate data source service
                   account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([transfer_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.UpdateTransferConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.UpdateTransferConfigRequest):
            request = datatransfer.UpdateTransferConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if transfer_config is not None:
                request.transfer_config = transfer_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_transfer_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("transfer_config.name", request.transfer_config.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_transfer_config(
        self,
        request: datatransfer.DeleteTransferConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a data transfer configuration,
        including any associated transfer runs and logs.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.DeleteTransferConfigRequest):
                The request object. A request to delete data transfer
                information. All associated transfer runs and log
                messages will be deleted as well.
            name (str):
                Required. The field will contain name of the resource
                requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}`` or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.DeleteTransferConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.DeleteTransferConfigRequest):
            request = datatransfer.DeleteTransferConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_transfer_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def get_transfer_config(
        self,
        request: datatransfer.GetTransferConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer.TransferConfig:
        r"""Returns information about a data transfer config.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.GetTransferConfigRequest):
                The request object. A request to get data transfer
                information.
            name (str):
                Required. The field will contain name of the resource
                requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}`` or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.TransferConfig:
                Represents a data transfer configuration. A transfer configuration
                   contains all metadata needed to perform a data
                   transfer. For example, destination_dataset_id
                   specifies where data should be stored. When a new
                   transfer configuration is created, the specified
                   destination_dataset_id is created when needed and
                   shared with the appropriate data source service
                   account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.GetTransferConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.GetTransferConfigRequest):
            request = datatransfer.GetTransferConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_transfer_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_transfer_configs(
        self,
        request: datatransfer.ListTransferConfigsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferConfigsPager:
        r"""Returns information about all data transfers in the
        project.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsRequest):
                The request object. A request to list data transfers
                configured for a BigQuery project.
            parent (str):
                Required. The BigQuery project id for which data sources
                should be returned: ``projects/{project_id}`` or
                ``projects/{project_id}/locations/{location_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.pagers.ListTransferConfigsPager:
                The returned list of pipelines in the
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.ListTransferConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.ListTransferConfigsRequest):
            request = datatransfer.ListTransferConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_transfer_configs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTransferConfigsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def schedule_transfer_runs(
        self,
        request: datatransfer.ScheduleTransferRunsRequest = None,
        *,
        parent: str = None,
        start_time: timestamp_pb2.Timestamp = None,
        end_time: timestamp_pb2.Timestamp = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datatransfer.ScheduleTransferRunsResponse:
        r"""Creates transfer runs for a time range [start_time, end_time].
        For each date - or whatever granularity the data source supports
        - in the range, one transfer run is created. Note that runs are
        created per UTC time in the time range. DEPRECATED: use
        StartManualTransferRuns instead.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.ScheduleTransferRunsRequest):
                The request object. A request to schedule transfer runs
                for a time range.
            parent (str):
                Required. Transfer configuration name in the form:
                ``projects/{project_id}/transferConfigs/{config_id}`` or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            start_time (google.protobuf.timestamp_pb2.Timestamp):
                Required. Start time of the range of transfer runs. For
                example, ``"2017-05-25T00:00:00+00:00"``.

                This corresponds to the ``start_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            end_time (google.protobuf.timestamp_pb2.Timestamp):
                Required. End time of the range of transfer runs. For
                example, ``"2017-05-30T00:00:00+00:00"``.

                This corresponds to the ``end_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.ScheduleTransferRunsResponse:
                A response to schedule transfer runs
                for a time range.

        """
        warnings.warn(
            "DataTransferServiceClient.schedule_transfer_runs is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, start_time, end_time])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.ScheduleTransferRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.ScheduleTransferRunsRequest):
            request = datatransfer.ScheduleTransferRunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if start_time is not None:
                request.start_time = start_time
            if end_time is not None:
                request.end_time = end_time

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.schedule_transfer_runs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def start_manual_transfer_runs(
        self,
        request: datatransfer.StartManualTransferRunsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datatransfer.StartManualTransferRunsResponse:
        r"""Start manual transfer runs to be executed now with schedule_time
        equal to current time. The transfer runs can be created for a
        time range where the run_time is between start_time (inclusive)
        and end_time (exclusive), or for a specific run_time.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.StartManualTransferRunsRequest):
                The request object. A request to start manual transfer
                runs.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.StartManualTransferRunsResponse:
                A response to start manual transfer
                runs.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.StartManualTransferRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.StartManualTransferRunsRequest):
            request = datatransfer.StartManualTransferRunsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.start_manual_transfer_runs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_transfer_run(
        self,
        request: datatransfer.GetTransferRunRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer.TransferRun:
        r"""Returns information about the particular transfer
        run.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.GetTransferRunRequest):
                The request object. A request to get data transfer run
                information.
            name (str):
                Required. The field will contain name of the resource
                requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
                or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.TransferRun:
                Represents a data transfer run.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.GetTransferRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.GetTransferRunRequest):
            request = datatransfer.GetTransferRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_transfer_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_transfer_run(
        self,
        request: datatransfer.DeleteTransferRunRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified transfer run.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.DeleteTransferRunRequest):
                The request object. A request to delete data transfer
                run information.
            name (str):
                Required. The field will contain name of the resource
                requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
                or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}``

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.DeleteTransferRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.DeleteTransferRunRequest):
            request = datatransfer.DeleteTransferRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_transfer_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def list_transfer_runs(
        self,
        request: datatransfer.ListTransferRunsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferRunsPager:
        r"""Returns information about running and completed jobs.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsRequest):
                The request object. A request to list data transfer
                runs. UI can use this method to show/filter specific
                data transfer runs. The data source can use this method
                to request all scheduled transfer runs.
            parent (str):
                Required. Name of transfer configuration for which
                transfer runs should be retrieved. Format of transfer
                configuration resource name is:
                ``projects/{project_id}/transferConfigs/{config_id}`` or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.pagers.ListTransferRunsPager:
                The returned list of pipelines in the
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.ListTransferRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.ListTransferRunsRequest):
            request = datatransfer.ListTransferRunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_transfer_runs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTransferRunsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_transfer_logs(
        self,
        request: datatransfer.ListTransferLogsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferLogsPager:
        r"""Returns user facing log messages for the data
        transfer run.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsRequest):
                The request object. A request to get user facing log
                messages associated with data transfer run.
            parent (str):
                Required. Transfer run name in the form:
                ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
                or
                ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.pagers.ListTransferLogsPager:
                The returned list transfer run
                messages.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.ListTransferLogsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.ListTransferLogsRequest):
            request = datatransfer.ListTransferLogsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_transfer_logs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTransferLogsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def check_valid_creds(
        self,
        request: datatransfer.CheckValidCredsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datatransfer.CheckValidCredsResponse:
        r"""Returns true if valid credentials exist for the given
        data source and requesting user.
        Some data sources doesn't support service account, so we
        need to talk to them on behalf of the end user. This API
        just checks whether we have OAuth token for the
        particular user, which is a pre-requisite before user
        can create a transfer config.

        Args:
            request (google.cloud.bigquery_datatransfer_v1.types.CheckValidCredsRequest):
                The request object. A request to determine whether the
                user has valid credentials. This method is used to limit
                the number of OAuth popups in the user interface. The
                user id is inferred from the API call context.
                If the data source has the Google+ authorization type,
                this method returns false, as it cannot be determined
                whether the credentials are already valid merely based
                on the user id.
            name (str):
                Required. The data source in the form:
                ``projects/{project_id}/dataSources/{data_source_id}``
                or
                ``projects/{project_id}/locations/{location_id}/dataSources/{data_source_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datatransfer_v1.types.CheckValidCredsResponse:
                A response indicating whether the
                credentials exist and are valid.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datatransfer.CheckValidCredsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datatransfer.CheckValidCredsRequest):
            request = datatransfer.CheckValidCredsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.check_valid_creds]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-datatransfer",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataTransferServiceClient",)
