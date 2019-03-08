# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.cloud.bigquery.datatransfer.v1 DataTransferService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.path_template
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.bigquery_datatransfer_v1.gapic import (
    data_transfer_service_client_config,
)
from google.cloud.bigquery_datatransfer_v1.gapic import enums
from google.cloud.bigquery_datatransfer_v1.gapic.transports import (
    data_transfer_service_grpc_transport,
)
from google.cloud.bigquery_datatransfer_v1.proto import datatransfer_pb2
from google.cloud.bigquery_datatransfer_v1.proto import datatransfer_pb2_grpc
from google.cloud.bigquery_datatransfer_v1.proto import transfer_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-bigquery-datatransfer"
).version


class DataTransferServiceClient(object):
    """
    The Google BigQuery Data Transfer Service API enables BigQuery users to
    configure the transfer of their data from other Google Products into BigQuery.
    This service contains methods that are end user exposed. It backs up the
    frontend.
    """

    SERVICE_ADDRESS = "bigquerydatatransfer.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.bigquery.datatransfer.v1.DataTransferService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
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

    @classmethod
    def project_data_source_path(cls, project, data_source):
        """Return a fully-qualified project_data_source string."""
        return google.api_core.path_template.expand(
            "projects/{project}/dataSources/{data_source}",
            project=project,
            data_source=data_source,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def project_transfer_config_path(cls, project, transfer_config):
        """Return a fully-qualified project_transfer_config string."""
        return google.api_core.path_template.expand(
            "projects/{project}/transferConfigs/{transfer_config}",
            project=project,
            transfer_config=transfer_config,
        )

    @classmethod
    def project_run_path(cls, project, transfer_config, run):
        """Return a fully-qualified project_run string."""
        return google.api_core.path_template.expand(
            "projects/{project}/transferConfigs/{transfer_config}/runs/{run}",
            project=project,
            transfer_config=transfer_config,
            run=run,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.DataTransferServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.DataTransferServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = data_transfer_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=data_transfer_service_grpc_transport.DataTransferServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = data_transfer_service_grpc_transport.DataTransferServiceGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def get_data_source(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves a supported data source and returns its settings,
        which can be used for UI rendering.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.project_data_source_path('[PROJECT]', '[DATA_SOURCE]')
            >>>
            >>> response = client.get_data_source(name)

        Args:
            name (str): The field will contain name of the resource requested, for example:
                ``projects/{project_id}/dataSources/{data_source_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.DataSource` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_data_source" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_data_source"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_data_source,
                default_retry=self._method_configs["GetDataSource"].retry,
                default_timeout=self._method_configs["GetDataSource"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.GetDataSourceRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_data_source"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_data_sources(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists supported data sources and returns their settings,
        which can be used for UI rendering.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_data_sources(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_data_sources(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The BigQuery project id for which data sources should be returned. Must
                be in the form: ``projects/{project_id}``
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.bigquery_datatransfer_v1.types.DataSource` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_data_sources" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_data_sources"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_data_sources,
                default_retry=self._method_configs["ListDataSources"].retry,
                default_timeout=self._method_configs["ListDataSources"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.ListDataSourcesRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_data_sources"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="data_sources",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_transfer_config(
        self,
        parent,
        transfer_config,
        authorization_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new data transfer configuration.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `transfer_config`:
            >>> transfer_config = {}
            >>>
            >>> response = client.create_transfer_config(parent, transfer_config)

        Args:
            parent (str): The BigQuery project id where the transfer configuration should be
                created. Must be in the format
                /projects/{project\_id}/locations/{location\_id} If specified location
                and location of the destination bigquery dataset do not match - the
                request will fail.
            transfer_config (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.TransferConfig]): Data transfer configuration to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig`
            authorization_code (str): Optional OAuth2 authorization code to use with this transfer
                configuration. This is required if new credentials are needed, as
                indicated by ``CheckValidCreds``. In order to obtain
                authorization\_code, please make a request to
                https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client\_id=&scope=&redirect\_uri=

                -  client\_id should be OAuth client\_id of BigQuery DTS API for the
                   given data source returned by ListDataSources method.
                -  data\_source\_scopes are the scopes returned by ListDataSources
                   method.
                -  redirect\_uri is an optional parameter. If not specified, then
                   authorization code is posted to the opener of authorization flow
                   window. Otherwise it will be sent to the redirect uri. A special
                   value of urn:ietf:wg:oauth:2.0:oob means that authorization code
                   should be returned in the title bar of the browser, with the page
                   text prompting the user to copy the code and paste it in the
                   application.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_transfer_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_transfer_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_transfer_config,
                default_retry=self._method_configs["CreateTransferConfig"].retry,
                default_timeout=self._method_configs["CreateTransferConfig"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.CreateTransferConfigRequest(
            parent=parent,
            transfer_config=transfer_config,
            authorization_code=authorization_code,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_transfer_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_transfer_config(
        self,
        transfer_config,
        update_mask,
        authorization_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a data transfer configuration.
        All fields must be set, even if they are not updated.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> # TODO: Initialize `transfer_config`:
            >>> transfer_config = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_transfer_config(transfer_config, update_mask)

        Args:
            transfer_config (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.TransferConfig]): Data transfer configuration to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig`
            update_mask (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.FieldMask]): Required list of fields to be updated in this request.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.FieldMask`
            authorization_code (str): Optional OAuth2 authorization code to use with this transfer
                configuration. If it is provided, the transfer configuration will be
                associated with the authorizing user. In order to obtain
                authorization\_code, please make a request to
                https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client\_id=&scope=&redirect\_uri=

                -  client\_id should be OAuth client\_id of BigQuery DTS API for the
                   given data source returned by ListDataSources method.
                -  data\_source\_scopes are the scopes returned by ListDataSources
                   method.
                -  redirect\_uri is an optional parameter. If not specified, then
                   authorization code is posted to the opener of authorization flow
                   window. Otherwise it will be sent to the redirect uri. A special
                   value of urn:ietf:wg:oauth:2.0:oob means that authorization code
                   should be returned in the title bar of the browser, with the page
                   text prompting the user to copy the code and paste it in the
                   application.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_transfer_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_transfer_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_transfer_config,
                default_retry=self._method_configs["UpdateTransferConfig"].retry,
                default_timeout=self._method_configs["UpdateTransferConfig"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.UpdateTransferConfigRequest(
            transfer_config=transfer_config,
            update_mask=update_mask,
            authorization_code=authorization_code,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("transfer_config.name", transfer_config.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_transfer_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_transfer_config(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a data transfer configuration,
        including any associated transfer runs and logs.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.project_transfer_config_path('[PROJECT]', '[TRANSFER_CONFIG]')
            >>>
            >>> client.delete_transfer_config(name)

        Args:
            name (str): The field will contain name of the resource requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_transfer_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_transfer_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_transfer_config,
                default_retry=self._method_configs["DeleteTransferConfig"].retry,
                default_timeout=self._method_configs["DeleteTransferConfig"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.DeleteTransferConfigRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_transfer_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_transfer_config(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns information about a data transfer config.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.project_transfer_config_path('[PROJECT]', '[TRANSFER_CONFIG]')
            >>>
            >>> response = client.get_transfer_config(name)

        Args:
            name (str): The field will contain name of the resource requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_transfer_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_transfer_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_transfer_config,
                default_retry=self._method_configs["GetTransferConfig"].retry,
                default_timeout=self._method_configs["GetTransferConfig"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.GetTransferConfigRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_transfer_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_transfer_configs(
        self,
        parent,
        data_source_ids=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns information about all data transfers in the project.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_transfer_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_transfer_configs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The BigQuery project id for which data sources should be returned:
                ``projects/{project_id}``.
            data_source_ids (list[str]): When specified, only configurations of requested data sources are returned.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_transfer_configs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_transfer_configs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_transfer_configs,
                default_retry=self._method_configs["ListTransferConfigs"].retry,
                default_timeout=self._method_configs["ListTransferConfigs"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.ListTransferConfigsRequest(
            parent=parent, data_source_ids=data_source_ids, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_transfer_configs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="transfer_configs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def schedule_transfer_runs(
        self,
        parent,
        start_time,
        end_time,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates transfer runs for a time range [start\_time, end\_time]. For
        each date - or whatever granularity the data source supports - in the
        range, one transfer run is created. Note that runs are created per UTC
        time in the time range.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.project_transfer_config_path('[PROJECT]', '[TRANSFER_CONFIG]')
            >>>
            >>> # TODO: Initialize `start_time`:
            >>> start_time = {}
            >>>
            >>> # TODO: Initialize `end_time`:
            >>> end_time = {}
            >>>
            >>> response = client.schedule_transfer_runs(parent, start_time, end_time)

        Args:
            parent (str): Transfer configuration name in the form:
                ``projects/{project_id}/transferConfigs/{config_id}``.
            start_time (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.Timestamp]): Start time of the range of transfer runs. For example,
                ``"2017-05-25T00:00:00+00:00"``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.Timestamp`
            end_time (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.Timestamp]): End time of the range of transfer runs. For example,
                ``"2017-05-30T00:00:00+00:00"``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.Timestamp`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.ScheduleTransferRunsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "schedule_transfer_runs" not in self._inner_api_calls:
            self._inner_api_calls[
                "schedule_transfer_runs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.schedule_transfer_runs,
                default_retry=self._method_configs["ScheduleTransferRuns"].retry,
                default_timeout=self._method_configs["ScheduleTransferRuns"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.ScheduleTransferRunsRequest(
            parent=parent, start_time=start_time, end_time=end_time
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["schedule_transfer_runs"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_transfer_run(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns information about the particular transfer run.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.project_run_path('[PROJECT]', '[TRANSFER_CONFIG]', '[RUN]')
            >>>
            >>> response = client.get_transfer_run(name)

        Args:
            name (str): The field will contain name of the resource requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferRun` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_transfer_run" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_transfer_run"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_transfer_run,
                default_retry=self._method_configs["GetTransferRun"].retry,
                default_timeout=self._method_configs["GetTransferRun"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.GetTransferRunRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_transfer_run"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_transfer_run(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified transfer run.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.project_run_path('[PROJECT]', '[TRANSFER_CONFIG]', '[RUN]')
            >>>
            >>> client.delete_transfer_run(name)

        Args:
            name (str): The field will contain name of the resource requested, for example:
                ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_transfer_run" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_transfer_run"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_transfer_run,
                default_retry=self._method_configs["DeleteTransferRun"].retry,
                default_timeout=self._method_configs["DeleteTransferRun"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.DeleteTransferRunRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_transfer_run"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_transfer_runs(
        self,
        parent,
        states=None,
        page_size=None,
        run_attempt=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns information about running and completed jobs.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.project_transfer_config_path('[PROJECT]', '[TRANSFER_CONFIG]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_transfer_runs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_transfer_runs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Name of transfer configuration for which transfer runs should be
                retrieved. Format of transfer configuration resource name is:
                ``projects/{project_id}/transferConfigs/{config_id}``.
            states (list[~google.cloud.bigquery_datatransfer_v1.types.TransferState]): When specified, only transfer runs with requested states are returned.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            run_attempt (~google.cloud.bigquery_datatransfer_v1.types.RunAttempt): Indicates how run attempts are to be pulled.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferRun` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_transfer_runs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_transfer_runs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_transfer_runs,
                default_retry=self._method_configs["ListTransferRuns"].retry,
                default_timeout=self._method_configs["ListTransferRuns"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.ListTransferRunsRequest(
            parent=parent, states=states, page_size=page_size, run_attempt=run_attempt
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_transfer_runs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="transfer_runs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_transfer_logs(
        self,
        parent,
        page_size=None,
        message_types=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns user facing log messages for the data transfer run.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.project_run_path('[PROJECT]', '[TRANSFER_CONFIG]', '[RUN]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_transfer_logs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_transfer_logs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Transfer run name in the form:
                ``projects/{project_id}/transferConfigs/{config_Id}/runs/{run_id}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            message_types (list[~google.cloud.bigquery_datatransfer_v1.types.MessageSeverity]): Message types to return. If not populated - INFO, WARNING and ERROR
                messages are returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferMessage` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_transfer_logs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_transfer_logs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_transfer_logs,
                default_retry=self._method_configs["ListTransferLogs"].retry,
                default_timeout=self._method_configs["ListTransferLogs"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.ListTransferLogsRequest(
            parent=parent, page_size=page_size, message_types=message_types
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_transfer_logs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="transfer_messages",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def check_valid_creds(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns true if valid credentials exist for the given data source and
        requesting user.
        Some data sources doesn't support service account, so we need to talk to
        them on behalf of the end user. This API just checks whether we have OAuth
        token for the particular user, which is a pre-requisite before user can
        create a transfer config.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.project_data_source_path('[PROJECT]', '[DATA_SOURCE]')
            >>>
            >>> response = client.check_valid_creds(name)

        Args:
            name (str): The data source in the form:
                ``projects/{project_id}/dataSources/{data_source_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.CheckValidCredsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "check_valid_creds" not in self._inner_api_calls:
            self._inner_api_calls[
                "check_valid_creds"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.check_valid_creds,
                default_retry=self._method_configs["CheckValidCreds"].retry,
                default_timeout=self._method_configs["CheckValidCreds"].timeout,
                client_info=self._client_info,
            )

        request = datatransfer_pb2.CheckValidCredsRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["check_valid_creds"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
