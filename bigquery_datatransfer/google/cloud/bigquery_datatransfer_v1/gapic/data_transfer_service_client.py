# Copyright 2017, Google LLC All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/cloud/bigquery/datatransfer/v1/datatransfer.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.bigquery.datatransfer.v1 DataTransferService API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from google.cloud.bigquery_datatransfer_v1.gapic import data_transfer_service_client_config
from google.cloud.bigquery_datatransfer_v1.gapic import enums
from google.cloud.bigquery_datatransfer_v1.proto import datatransfer_pb2
from google.cloud.bigquery_datatransfer_v1.proto import transfer_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-bigquery-datatransfer',
).version


class DataTransferServiceClient(object):
    """
    The Google BigQuery Data Transfer Service API enables BigQuery users to
    configure the transfer of their data from other Google Products into BigQuery.
    This service contains methods that are end user exposed. It backs up the
    frontend.
    """

    SERVICE_ADDRESS = 'bigquerydatatransfer.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloud-platform.read-only',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = (
        'google.cloud.bigquery.datatransfer.v1.DataTransferService')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def location_path(cls, project, location):
        """Returns a fully-qualified location resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/locations/{location}',
            project=project,
            location=location,
        )

    @classmethod
    def location_data_source_path(cls, project, location, data_source):
        """Returns a fully-qualified location_data_source resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/locations/{location}/dataSources/{data_source}',
            project=project,
            location=location,
            data_source=data_source,
        )

    @classmethod
    def location_transfer_config_path(cls, project, location, transfer_config):
        """Returns a fully-qualified location_transfer_config resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/locations/{location}/transferConfigs/{transfer_config}',
            project=project,
            location=location,
            transfer_config=transfer_config,
        )

    @classmethod
    def location_run_path(cls, project, location, transfer_config, run):
        """Returns a fully-qualified location_run resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/locations/{location}/transferConfigs/{transfer_config}/runs/{run}',
            project=project,
            location=location,
            transfer_config=transfer_config,
            run=run,
        )

    @classmethod
    def data_source_path(cls, project, data_source):
        """Returns a fully-qualified data_source resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/dataSources/{data_source}',
            project=project,
            data_source=data_source,
        )

    @classmethod
    def transfer_config_path(cls, project, transfer_config):
        """Returns a fully-qualified transfer_config resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/transferConfigs/{transfer_config}',
            project=project,
            transfer_config=transfer_config,
        )

    @classmethod
    def run_path(cls, project, transfer_config, run):
        """Returns a fully-qualified run resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/transferConfigs/{transfer_config}/runs/{run}',
            project=project,
            transfer_config=transfer_config,
            run=run,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=data_transfer_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

        self.data_transfer_service_stub = (
            datatransfer_pb2.DataTransferServiceStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._get_data_source = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.GetDataSource,
            default_retry=method_configs['GetDataSource'].retry,
            default_timeout=method_configs['GetDataSource'].timeout,
            client_info=client_info)
        self._list_data_sources = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.ListDataSources,
            default_retry=method_configs['ListDataSources'].retry,
            default_timeout=method_configs['ListDataSources'].timeout,
            client_info=client_info)
        self._create_transfer_config = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.CreateTransferConfig,
            default_retry=method_configs['CreateTransferConfig'].retry,
            default_timeout=method_configs['CreateTransferConfig'].timeout,
            client_info=client_info)
        self._update_transfer_config = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.UpdateTransferConfig,
            default_retry=method_configs['UpdateTransferConfig'].retry,
            default_timeout=method_configs['UpdateTransferConfig'].timeout,
            client_info=client_info)
        self._delete_transfer_config = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.DeleteTransferConfig,
            default_retry=method_configs['DeleteTransferConfig'].retry,
            default_timeout=method_configs['DeleteTransferConfig'].timeout,
            client_info=client_info)
        self._get_transfer_config = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.GetTransferConfig,
            default_retry=method_configs['GetTransferConfig'].retry,
            default_timeout=method_configs['GetTransferConfig'].timeout,
            client_info=client_info)
        self._list_transfer_configs = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.ListTransferConfigs,
            default_retry=method_configs['ListTransferConfigs'].retry,
            default_timeout=method_configs['ListTransferConfigs'].timeout,
            client_info=client_info)
        self._schedule_transfer_runs = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.ScheduleTransferRuns,
            default_retry=method_configs['ScheduleTransferRuns'].retry,
            default_timeout=method_configs['ScheduleTransferRuns'].timeout,
            client_info=client_info)
        self._get_transfer_run = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.GetTransferRun,
            default_retry=method_configs['GetTransferRun'].retry,
            default_timeout=method_configs['GetTransferRun'].timeout,
            client_info=client_info)
        self._delete_transfer_run = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.DeleteTransferRun,
            default_retry=method_configs['DeleteTransferRun'].retry,
            default_timeout=method_configs['DeleteTransferRun'].timeout,
            client_info=client_info)
        self._list_transfer_runs = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.ListTransferRuns,
            default_retry=method_configs['ListTransferRuns'].retry,
            default_timeout=method_configs['ListTransferRuns'].timeout,
            client_info=client_info)
        self._list_transfer_logs = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.ListTransferLogs,
            default_retry=method_configs['ListTransferLogs'].retry,
            default_timeout=method_configs['ListTransferLogs'].timeout,
            client_info=client_info)
        self._check_valid_creds = google.api_core.gapic_v1.method.wrap_method(
            self.data_transfer_service_stub.CheckValidCreds,
            default_retry=method_configs['CheckValidCreds'].retry,
            default_timeout=method_configs['CheckValidCreds'].timeout,
            client_info=client_info)

    # Service calls
    def get_data_source(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Retrieves a supported data source and returns its settings,
        which can be used for UI rendering.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.location_data_source_path('[PROJECT]', '[LOCATION]', '[DATA_SOURCE]')
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

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.DataSource` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.GetDataSourceRequest(name=name)
        return self._get_data_source(request, retry=retry, timeout=timeout)

    def list_data_sources(self,
                          parent,
                          page_size=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists supported data sources and returns their settings,
        which can be used for UI rendering.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_data_sources(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_data_sources(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The BigQuery project id for which data sources should be returned.
                Must be in the form: ``projects/{project_id}``
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
        request = datatransfer_pb2.ListDataSourcesRequest(
            parent=parent, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_data_sources, retry=retry, timeout=timeout),
            request=request,
            items_field='data_sources',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def create_transfer_config(
            self,
            parent,
            transfer_config,
            authorization_code=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a new data transfer configuration.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>> transfer_config = {}
            >>>
            >>> response = client.create_transfer_config(parent, transfer_config)

        Args:
            parent (str): The BigQuery project id where the transfer configuration should be created.
                Must be in the format /projects/{project_id}/locations/{location_id}
                or
                /projects/{project_id}/locations/-
                In case when '-' is specified as location_id, location is infered from
                the destination dataset region.
            transfer_config (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.TransferConfig]): Data transfer configuration to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig`
            authorization_code (str): Optional OAuth2 authorization code to use with this transfer configuration.
                This is required if new credentials are needed, as indicated by
                ``CheckValidCreds``.
                In order to obtain authorization_code, please make a
                request to
                https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client_id=<datatransferapiclientid>&scope=<data_source_scopes>&redirect_uri=<redirect_uri>

                * client_id should be OAuth client_id of BigQuery DTS API for the given
                  data source returned by ListDataSources method.
                * data_source_scopes are the scopes returned by ListDataSources method.
                * redirect_uri is an optional parameter. If not specified, then
                  authorization code is posted to the opener of authorization flow window.
                  Otherwise it will be sent to the redirect uri. A special value of
                  urn:ietf:wg:oauth:2.0:oob means that authorization code should be
                  returned in the title bar of the browser, with the page text prompting
                  the user to copy the code and paste it in the application.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.CreateTransferConfigRequest(
            parent=parent,
            transfer_config=transfer_config,
            authorization_code=authorization_code)
        return self._create_transfer_config(
            request, retry=retry, timeout=timeout)

    def update_transfer_config(
            self,
            transfer_config,
            update_mask,
            authorization_code=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates a data transfer configuration.
        All fields must be set, even if they are not updated.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> transfer_config = {}
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
            authorization_code (str): Optional OAuth2 authorization code to use with this transfer configuration.
                If it is provided, the transfer configuration will be associated with the
                authorizing user.
                In order to obtain authorization_code, please make a
                request to
                https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client_id=<datatransferapiclientid>&scope=<data_source_scopes>&redirect_uri=<redirect_uri>

                * client_id should be OAuth client_id of BigQuery DTS API for the given
                  data source returned by ListDataSources method.
                * data_source_scopes are the scopes returned by ListDataSources method.
                * redirect_uri is an optional parameter. If not specified, then
                  authorization code is posted to the opener of authorization flow window.
                  Otherwise it will be sent to the redirect uri. A special value of
                  urn:ietf:wg:oauth:2.0:oob means that authorization code should be
                  returned in the title bar of the browser, with the page text prompting
                  the user to copy the code and paste it in the application.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.UpdateTransferConfigRequest(
            transfer_config=transfer_config,
            update_mask=update_mask,
            authorization_code=authorization_code)
        return self._update_transfer_config(
            request, retry=retry, timeout=timeout)

    def delete_transfer_config(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Deletes a data transfer configuration,
        including any associated transfer runs and logs.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.location_transfer_config_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]')
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

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.DeleteTransferConfigRequest(name=name)
        self._delete_transfer_config(request, retry=retry, timeout=timeout)

    def get_transfer_config(self,
                            name,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns information about a data transfer config.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.location_transfer_config_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]')
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

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.GetTransferConfigRequest(name=name)
        return self._get_transfer_config(request, retry=retry, timeout=timeout)

    def list_transfer_configs(self,
                              parent,
                              data_source_ids=None,
                              page_size=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns information about all data transfers in the project.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_transfer_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_transfer_configs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The BigQuery project id for which data sources
                should be returned: ``projects/{project_id}``.
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
        request = datatransfer_pb2.ListTransferConfigsRequest(
            parent=parent,
            data_source_ids=data_source_ids,
            page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_transfer_configs, retry=retry, timeout=timeout),
            request=request,
            items_field='transfer_configs',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def schedule_transfer_runs(
            self,
            parent,
            start_time,
            end_time,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates transfer runs for a time range [range_start_time, range_end_time].
        For each date - or whatever granularity the data source supports - in the
        range, one transfer run is created.
        Note that runs are created per UTC time in the time range.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.location_transfer_config_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]')
            >>> start_time = {}
            >>> end_time = {}
            >>>
            >>> response = client.schedule_transfer_runs(parent, start_time, end_time)

        Args:
            parent (str): Transfer configuration name in the form:
                ``projects/{project_id}/transferConfigs/{config_id}``.
            start_time (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.Timestamp]): Start time of the range of transfer runs. For example,
                ``\"2017-05-25T00:00:00+00:00\"``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.Timestamp`
            end_time (Union[dict, ~google.cloud.bigquery_datatransfer_v1.types.Timestamp]): End time of the range of transfer runs. For example,
                ``\"2017-05-30T00:00:00+00:00\"``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_datatransfer_v1.types.Timestamp`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.ScheduleTransferRunsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.ScheduleTransferRunsRequest(
            parent=parent, start_time=start_time, end_time=end_time)
        return self._schedule_transfer_runs(
            request, retry=retry, timeout=timeout)

    def get_transfer_run(self,
                         name,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns information about the particular transfer run.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.location_run_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]', '[RUN]')
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

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.TransferRun` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.GetTransferRunRequest(name=name)
        return self._get_transfer_run(request, retry=retry, timeout=timeout)

    def delete_transfer_run(self,
                            name,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Deletes the specified transfer run.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> name = client.location_run_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]', '[RUN]')
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

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.DeleteTransferRunRequest(name=name)
        self._delete_transfer_run(request, retry=retry, timeout=timeout)

    def list_transfer_runs(self,
                           parent,
                           states=None,
                           page_size=None,
                           run_attempt=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns information about running and completed jobs.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.location_transfer_config_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_transfer_runs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_transfer_runs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Name of transfer configuration for which transfer runs should be retrieved.
                Format of transfer configuration resource name is:
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
        request = datatransfer_pb2.ListTransferRunsRequest(
            parent=parent,
            states=states,
            page_size=page_size,
            run_attempt=run_attempt)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_transfer_runs, retry=retry, timeout=timeout),
            request=request,
            items_field='transfer_runs',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def list_transfer_logs(self,
                           parent,
                           page_size=None,
                           message_types=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns user facing log messages for the data transfer run.

        Example:
            >>> from google.cloud import bigquery_datatransfer_v1
            >>>
            >>> client = bigquery_datatransfer_v1.DataTransferServiceClient()
            >>>
            >>> parent = client.location_run_path('[PROJECT]', '[LOCATION]', '[TRANSFER_CONFIG]', '[RUN]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_transfer_logs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_transfer_logs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
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
        request = datatransfer_pb2.ListTransferLogsRequest(
            parent=parent, page_size=page_size, message_types=message_types)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_transfer_logs, retry=retry, timeout=timeout),
            request=request,
            items_field='transfer_messages',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def check_valid_creds(self,
                          name,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT):
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
            >>> name = client.location_data_source_path('[PROJECT]', '[LOCATION]', '[DATA_SOURCE]')
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

        Returns:
            A :class:`~google.cloud.bigquery_datatransfer_v1.types.CheckValidCredsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = datatransfer_pb2.CheckValidCredsRequest(name=name)
        return self._check_valid_creds(request, retry=retry, timeout=timeout)
