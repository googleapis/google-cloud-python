# Copyright 2018 Google LLC
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
"""Accesses the google.cloud.websecurityscanner.v1alpha WebSecurityScanner API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from google.cloud.websecurityscanner_v1alpha.gapic import enums
from google.cloud.websecurityscanner_v1alpha.gapic import web_security_scanner_client_config
from google.cloud.websecurityscanner_v1alpha.proto import finding_pb2
from google.cloud.websecurityscanner_v1alpha.proto import scan_config_pb2
from google.cloud.websecurityscanner_v1alpha.proto import scan_run_pb2
from google.cloud.websecurityscanner_v1alpha.proto import web_security_scanner_pb2
from google.cloud.websecurityscanner_v1alpha.proto import web_security_scanner_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-websecurityscanner', ).version


class WebSecurityScannerClient(object):
    """
    Cloud Web Security Scanner Service identifies security vulnerabilities in web
    applications hosted on Google Cloud Platform. It crawls your application, and
    attempts to exercise as many user inputs and event handlers as possible.
    """

    SERVICE_ADDRESS = 'websecurityscanner.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.websecurityscanner.v1alpha.WebSecurityScanner'

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def scan_config_path(cls, project, scan_config):
        """Return a fully-qualified scan_config string."""
        return google.api_core.path_template.expand(
            'projects/{project}/scanConfigs/{scan_config}',
            project=project,
            scan_config=scan_config,
        )

    @classmethod
    def scan_run_path(cls, project, scan_config, scan_run):
        """Return a fully-qualified scan_run string."""
        return google.api_core.path_template.expand(
            'projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}',
            project=project,
            scan_config=scan_config,
            scan_run=scan_run,
        )

    @classmethod
    def finding_path(cls, project, scan_config, scan_run, finding):
        """Return a fully-qualified finding string."""
        return google.api_core.path_template.expand(
            'projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}/findings/{finding}',
            project=project,
            scan_config=scan_config,
            scan_run=scan_run,
            finding=finding,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=web_security_scanner_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.web_security_scanner_stub = (
            web_security_scanner_pb2_grpc.WebSecurityScannerStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._create_scan_config = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.CreateScanConfig,
            default_retry=method_configs['CreateScanConfig'].retry,
            default_timeout=method_configs['CreateScanConfig'].timeout,
            client_info=client_info,
        )
        self._delete_scan_config = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.DeleteScanConfig,
            default_retry=method_configs['DeleteScanConfig'].retry,
            default_timeout=method_configs['DeleteScanConfig'].timeout,
            client_info=client_info,
        )
        self._get_scan_config = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.GetScanConfig,
            default_retry=method_configs['GetScanConfig'].retry,
            default_timeout=method_configs['GetScanConfig'].timeout,
            client_info=client_info,
        )
        self._list_scan_configs = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.ListScanConfigs,
            default_retry=method_configs['ListScanConfigs'].retry,
            default_timeout=method_configs['ListScanConfigs'].timeout,
            client_info=client_info,
        )
        self._update_scan_config = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.UpdateScanConfig,
            default_retry=method_configs['UpdateScanConfig'].retry,
            default_timeout=method_configs['UpdateScanConfig'].timeout,
            client_info=client_info,
        )
        self._start_scan_run = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.StartScanRun,
            default_retry=method_configs['StartScanRun'].retry,
            default_timeout=method_configs['StartScanRun'].timeout,
            client_info=client_info,
        )
        self._get_scan_run = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.GetScanRun,
            default_retry=method_configs['GetScanRun'].retry,
            default_timeout=method_configs['GetScanRun'].timeout,
            client_info=client_info,
        )
        self._list_scan_runs = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.ListScanRuns,
            default_retry=method_configs['ListScanRuns'].retry,
            default_timeout=method_configs['ListScanRuns'].timeout,
            client_info=client_info,
        )
        self._stop_scan_run = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.StopScanRun,
            default_retry=method_configs['StopScanRun'].retry,
            default_timeout=method_configs['StopScanRun'].timeout,
            client_info=client_info,
        )
        self._list_crawled_urls = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.ListCrawledUrls,
            default_retry=method_configs['ListCrawledUrls'].retry,
            default_timeout=method_configs['ListCrawledUrls'].timeout,
            client_info=client_info,
        )
        self._get_finding = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.GetFinding,
            default_retry=method_configs['GetFinding'].retry,
            default_timeout=method_configs['GetFinding'].timeout,
            client_info=client_info,
        )
        self._list_findings = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.ListFindings,
            default_retry=method_configs['ListFindings'].retry,
            default_timeout=method_configs['ListFindings'].timeout,
            client_info=client_info,
        )
        self._list_finding_type_stats = google.api_core.gapic_v1.method.wrap_method(
            self.web_security_scanner_stub.ListFindingTypeStats,
            default_retry=method_configs['ListFindingTypeStats'].retry,
            default_timeout=method_configs['ListFindingTypeStats'].timeout,
            client_info=client_info,
        )

    # Service calls
    def create_scan_config(self,
                           parent,
                           scan_config,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Creates a new ScanConfig.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize ``scan_config``:
            >>> scan_config = {}
            >>>
            >>> response = client.create_scan_config(parent, scan_config)

        Args:
            parent (str): Required.
                The parent resource name where the scan is created, which should be a
                project resource name in the format 'projects/{projectId}'.
            scan_config (Union[dict, ~google.cloud.websecurityscanner_v1alpha.types.ScanConfig]): Required.
                The ScanConfig to be created.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.CreateScanConfigRequest(
            parent=parent,
            scan_config=scan_config,
        )
        return self._create_scan_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_scan_config(self,
                           name,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Deletes an existing ScanConfig and its child resources.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> name = client.scan_config_path('[PROJECT]', '[SCAN_CONFIG]')
            >>>
            >>> client.delete_scan_config(name)

        Args:
            name (str): Required.
                The resource name of the ScanConfig to be deleted. The name follows the
                format of 'projects/{projectId}/scanConfigs/{scanConfigId}'.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.DeleteScanConfigRequest(name=name, )
        self._delete_scan_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_scan_config(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Gets a ScanConfig.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> name = client.scan_config_path('[PROJECT]', '[SCAN_CONFIG]')
            >>>
            >>> response = client.get_scan_config(name)

        Args:
            name (str): Required.
                The resource name of the ScanConfig to be returned. The name follows the
                format of 'projects/{projectId}/scanConfigs/{scanConfigId}'.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.GetScanConfigRequest(name=name, )
        return self._get_scan_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_scan_configs(self,
                          parent,
                          page_size=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Lists ScanConfigs under a given project.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_scan_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_scan_configs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.
                The parent resource name, which should be a project resource name in the
                format 'projects/{projectId}'.
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
            is an iterable of :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanConfig` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.ListScanConfigsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_scan_configs,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='scan_configs',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def update_scan_config(self,
                           scan_config,
                           update_mask,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Updates a ScanConfig. This method support partial update of a ScanConfig.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> # TODO: Initialize ``scan_config``:
            >>> scan_config = {}
            >>>
            >>> # TODO: Initialize ``update_mask``:
            >>> update_mask = {}
            >>>
            >>> response = client.update_scan_config(scan_config, update_mask)

        Args:
            scan_config (Union[dict, ~google.cloud.websecurityscanner_v1alpha.types.ScanConfig]): Required.
                The ScanConfig to be updated. The name field must be set to identify the
                resource to be updated. The values of fields not covered by the mask
                will be ignored.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanConfig`
            update_mask (Union[dict, ~google.cloud.websecurityscanner_v1alpha.types.FieldMask]): Required.
                The update mask applies to the resource. For the ``FieldMask`` definition,
                see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.websecurityscanner_v1alpha.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.UpdateScanConfigRequest(
            scan_config=scan_config,
            update_mask=update_mask,
        )
        return self._update_scan_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def start_scan_run(self,
                       name,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Start a ScanRun according to the given ScanConfig.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> name = client.scan_config_path('[PROJECT]', '[SCAN_CONFIG]')
            >>>
            >>> response = client.start_scan_run(name)

        Args:
            name (str): Required.
                The resource name of the ScanConfig to be used. The name follows the
                format of 'projects/{projectId}/scanConfigs/{scanConfigId}'.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanRun` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.StartScanRunRequest(name=name, )
        return self._start_scan_run(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_scan_run(self,
                     name,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Gets a ScanRun.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> name = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>> response = client.get_scan_run(name)

        Args:
            name (str): Required.
                The resource name of the ScanRun to be returned. The name follows the
                format of
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanRun` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.GetScanRunRequest(name=name, )
        return self._get_scan_run(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_scan_runs(self,
                       parent,
                       page_size=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Lists ScanRuns under a given ScanConfig, in descending order of ScanRun
        stop time.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.scan_config_path('[PROJECT]', '[SCAN_CONFIG]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_scan_runs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_scan_runs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.
                The parent resource name, which should be a scan resource name in the
                format 'projects/{projectId}/scanConfigs/{scanConfigId}'.
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
            is an iterable of :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanRun` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.ListScanRunsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_scan_runs,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='scan_runs',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def stop_scan_run(self,
                      name,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Stops a ScanRun. The stopped ScanRun is returned.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> name = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>> response = client.stop_scan_run(name)

        Args:
            name (str): Required.
                The resource name of the ScanRun to be stopped. The name follows the
                format of
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ScanRun` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.StopScanRunRequest(name=name, )
        return self._stop_scan_run(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_crawled_urls(self,
                          parent,
                          page_size=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        List CrawledUrls under a given ScanRun.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_crawled_urls(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_crawled_urls(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.
                The parent resource name, which should be a scan run resource name in the
                format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.
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
            is an iterable of :class:`~google.cloud.websecurityscanner_v1alpha.types.CrawledUrl` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.ListCrawledUrlsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_crawled_urls,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='crawled_urls',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_finding(self,
                    name,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT,
                    metadata=None):
        """
        Gets a Finding.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> name = client.finding_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]', '[FINDING]')
            >>>
            >>> response = client.get_finding(name)

        Args:
            name (str): Required.
                The resource name of the Finding to be returned. The name follows the
                format of
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}/findings/{findingId}'.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.Finding` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.GetFindingRequest(name=name, )
        return self._get_finding(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_findings(self,
                      parent,
                      filter_,
                      page_size=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        List Findings under a given ScanRun.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>> # TODO: Initialize ``filter_``:
            >>> filter_ = ''
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_findings(parent, filter_):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_findings(parent, filter_, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.
                The parent resource name, which should be a scan run resource name in the
                format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.
            filter_ (str): The filter expression. The expression must be in the format: <field>
                <operator> <value>.
                Supported field: 'finding_type'.
                Supported operator: '='.
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
            is an iterable of :class:`~google.cloud.websecurityscanner_v1alpha.types.Finding` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.ListFindingsRequest(
            parent=parent,
            filter=filter_,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_findings,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='findings',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def list_finding_type_stats(
            self,
            parent,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        List all FindingTypeStats under a given ScanRun.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>> response = client.list_finding_type_stats(parent)

        Args:
            parent (str): Required.
                The parent resource name, which should be a scan run resource name in the
                format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.websecurityscanner_v1alpha.types.ListFindingTypeStatsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = web_security_scanner_pb2.ListFindingTypeStatsRequest(
            parent=parent, )
        return self._list_finding_type_stats(
            request, retry=retry, timeout=timeout, metadata=metadata)
