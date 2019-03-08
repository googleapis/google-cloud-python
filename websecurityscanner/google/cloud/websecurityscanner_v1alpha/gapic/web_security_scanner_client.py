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
"""Accesses the google.cloud.websecurityscanner.v1alpha WebSecurityScanner API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.websecurityscanner_v1alpha.gapic import enums
from google.cloud.websecurityscanner_v1alpha.gapic import (
    web_security_scanner_client_config,
)
from google.cloud.websecurityscanner_v1alpha.gapic.transports import (
    web_security_scanner_grpc_transport,
)
from google.cloud.websecurityscanner_v1alpha.proto import finding_pb2
from google.cloud.websecurityscanner_v1alpha.proto import scan_config_pb2
from google.cloud.websecurityscanner_v1alpha.proto import scan_run_pb2
from google.cloud.websecurityscanner_v1alpha.proto import web_security_scanner_pb2
from google.cloud.websecurityscanner_v1alpha.proto import web_security_scanner_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-websecurityscanner"
).version


class WebSecurityScannerClient(object):
    """
    Cloud Web Security Scanner Service identifies security vulnerabilities in web
    applications hosted on Google Cloud Platform. It crawls your application, and
    attempts to exercise as many user inputs and event handlers as possible.
    """

    SERVICE_ADDRESS = "websecurityscanner.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.websecurityscanner.v1alpha.WebSecurityScanner"

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
            WebSecurityScannerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def scan_config_path(cls, project, scan_config):
        """Return a fully-qualified scan_config string."""
        return google.api_core.path_template.expand(
            "projects/{project}/scanConfigs/{scan_config}",
            project=project,
            scan_config=scan_config,
        )

    @classmethod
    def scan_run_path(cls, project, scan_config, scan_run):
        """Return a fully-qualified scan_run string."""
        return google.api_core.path_template.expand(
            "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}",
            project=project,
            scan_config=scan_config,
            scan_run=scan_run,
        )

    @classmethod
    def finding_path(cls, project, scan_config, scan_run, finding):
        """Return a fully-qualified finding string."""
        return google.api_core.path_template.expand(
            "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}/findings/{finding}",
            project=project,
            scan_config=scan_config,
            scan_run=scan_run,
            finding=finding,
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
            transport (Union[~.WebSecurityScannerGrpcTransport,
                    Callable[[~.Credentials, type], ~.WebSecurityScannerGrpcTransport]): A transport
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
            client_config = web_security_scanner_client_config.config

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
                    default_class=web_security_scanner_grpc_transport.WebSecurityScannerGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = web_security_scanner_grpc_transport.WebSecurityScannerGrpcTransport(
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
    def create_scan_config(
        self,
        parent,
        scan_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new ScanConfig.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `scan_config`:
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
        # Wrap the transport method to add retry and timeout logic.
        if "create_scan_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_scan_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_scan_config,
                default_retry=self._method_configs["CreateScanConfig"].retry,
                default_timeout=self._method_configs["CreateScanConfig"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.CreateScanConfigRequest(
            parent=parent, scan_config=scan_config
        )
        return self._inner_api_calls["create_scan_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_scan_config(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "delete_scan_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_scan_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_scan_config,
                default_retry=self._method_configs["DeleteScanConfig"].retry,
                default_timeout=self._method_configs["DeleteScanConfig"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.DeleteScanConfigRequest(name=name)
        self._inner_api_calls["delete_scan_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_scan_config(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "get_scan_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_scan_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_scan_config,
                default_retry=self._method_configs["GetScanConfig"].retry,
                default_timeout=self._method_configs["GetScanConfig"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.GetScanConfigRequest(name=name)
        return self._inner_api_calls["get_scan_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_scan_configs(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ScanConfigs under a given project.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_scan_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_scan_configs(parent).pages:
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_scan_configs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_scan_configs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_scan_configs,
                default_retry=self._method_configs["ListScanConfigs"].retry,
                default_timeout=self._method_configs["ListScanConfigs"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.ListScanConfigsRequest(
            parent=parent, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_scan_configs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="scan_configs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_scan_config(
        self,
        scan_config,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a ScanConfig. This method support partial update of a ScanConfig.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> # TODO: Initialize `scan_config`:
            >>> scan_config = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
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
            update_mask (Union[dict, ~google.cloud.websecurityscanner_v1alpha.types.FieldMask]): Required. The update mask applies to the resource. For the ``FieldMask``
                definition, see
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
        # Wrap the transport method to add retry and timeout logic.
        if "update_scan_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_scan_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_scan_config,
                default_retry=self._method_configs["UpdateScanConfig"].retry,
                default_timeout=self._method_configs["UpdateScanConfig"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.UpdateScanConfigRequest(
            scan_config=scan_config, update_mask=update_mask
        )
        return self._inner_api_calls["update_scan_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def start_scan_run(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "start_scan_run" not in self._inner_api_calls:
            self._inner_api_calls[
                "start_scan_run"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.start_scan_run,
                default_retry=self._method_configs["StartScanRun"].retry,
                default_timeout=self._method_configs["StartScanRun"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.StartScanRunRequest(name=name)
        return self._inner_api_calls["start_scan_run"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_scan_run(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "get_scan_run" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_scan_run"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_scan_run,
                default_retry=self._method_configs["GetScanRun"].retry,
                default_timeout=self._method_configs["GetScanRun"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.GetScanRunRequest(name=name)
        return self._inner_api_calls["get_scan_run"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_scan_runs(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            >>> # Iterate over all results
            >>> for element in client.list_scan_runs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_scan_runs(parent).pages:
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_scan_runs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_scan_runs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_scan_runs,
                default_retry=self._method_configs["ListScanRuns"].retry,
                default_timeout=self._method_configs["ListScanRuns"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.ListScanRunsRequest(
            parent=parent, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_scan_runs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="scan_runs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def stop_scan_run(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "stop_scan_run" not in self._inner_api_calls:
            self._inner_api_calls[
                "stop_scan_run"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.stop_scan_run,
                default_retry=self._method_configs["StopScanRun"].retry,
                default_timeout=self._method_configs["StopScanRun"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.StopScanRunRequest(name=name)
        return self._inner_api_calls["stop_scan_run"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_crawled_urls(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        List CrawledUrls under a given ScanRun.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_crawled_urls(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_crawled_urls(parent).pages:
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_crawled_urls" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_crawled_urls"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_crawled_urls,
                default_retry=self._method_configs["ListCrawledUrls"].retry,
                default_timeout=self._method_configs["ListCrawledUrls"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.ListCrawledUrlsRequest(
            parent=parent, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_crawled_urls"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="crawled_urls",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_finding(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "get_finding" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_finding"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_finding,
                default_retry=self._method_configs["GetFinding"].retry,
                default_timeout=self._method_configs["GetFinding"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.GetFindingRequest(name=name)
        return self._inner_api_calls["get_finding"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_findings(
        self,
        parent,
        filter_,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        List Findings under a given ScanRun.

        Example:
            >>> from google.cloud import websecurityscanner_v1alpha
            >>>
            >>> client = websecurityscanner_v1alpha.WebSecurityScannerClient()
            >>>
            >>> parent = client.scan_run_path('[PROJECT]', '[SCAN_CONFIG]', '[SCAN_RUN]')
            >>>
            >>> # TODO: Initialize `filter_`:
            >>> filter_ = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_findings(parent, filter_):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_findings(parent, filter_).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.
                The parent resource name, which should be a scan run resource name in the
                format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.
            filter_ (str): The filter expression. The expression must be in the format: . Supported
                field: 'finding\_type'. Supported operator: '='.
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_findings" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_findings"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_findings,
                default_retry=self._method_configs["ListFindings"].retry,
                default_timeout=self._method_configs["ListFindings"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.ListFindingsRequest(
            parent=parent, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_findings"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="findings",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_finding_type_stats(
        self,
        parent,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_finding_type_stats" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_finding_type_stats"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_finding_type_stats,
                default_retry=self._method_configs["ListFindingTypeStats"].retry,
                default_timeout=self._method_configs["ListFindingTypeStats"].timeout,
                client_info=self._client_info,
            )

        request = web_security_scanner_pb2.ListFindingTypeStatsRequest(parent=parent)
        return self._inner_api_calls["list_finding_type_stats"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
