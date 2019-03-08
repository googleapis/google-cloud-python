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
"""Accesses the google.cloud.dataproc.v1 ClusterController API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import grpc

from google.cloud.dataproc_v1.gapic import cluster_controller_client_config
from google.cloud.dataproc_v1.gapic import enums
from google.cloud.dataproc_v1.gapic.transports import cluster_controller_grpc_transport
from google.cloud.dataproc_v1.proto import clusters_pb2
from google.cloud.dataproc_v1.proto import clusters_pb2_grpc
from google.cloud.dataproc_v1.proto import operations_pb2 as proto_operations_pb2
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-dataproc").version


class ClusterControllerClient(object):
    """
    The ClusterControllerService provides methods to manage clusters
    of Compute Engine instances.
    """

    SERVICE_ADDRESS = "dataproc.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.dataproc.v1.ClusterController"

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
            ClusterControllerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

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
            transport (Union[~.ClusterControllerGrpcTransport,
                    Callable[[~.Credentials, type], ~.ClusterControllerGrpcTransport]): A transport
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
            client_config = cluster_controller_client_config.config

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
                    default_class=cluster_controller_grpc_transport.ClusterControllerGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cluster_controller_grpc_transport.ClusterControllerGrpcTransport(
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
    def create_cluster(
        self,
        project_id,
        region,
        cluster,
        request_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a cluster in a project.

        Example:
            >>> from google.cloud import dataproc_v1
            >>>
            >>> client = dataproc_v1.ClusterControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `cluster`:
            >>> cluster = {}
            >>>
            >>> response = client.create_cluster(project_id, region, cluster)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the cluster
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            cluster (Union[dict, ~google.cloud.dataproc_v1.types.Cluster]): Required. The cluster to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1.types.Cluster`
            request_id (str): Optional. A unique id used to identify the request. If the server
                receives two ``CreateClusterRequest`` requests with the same id, then
                the second request will be ignored and the first
                ``google.longrunning.Operation`` created and stored in the backend is
                returned.

                It is recommended to always set this value to a
                `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__.

                The id must contain only letters (a-z, A-Z), numbers (0-9), underscores
                (\_), and hyphens (-). The maximum length is 40 characters.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_cluster,
                default_retry=self._method_configs["CreateCluster"].retry,
                default_timeout=self._method_configs["CreateCluster"].timeout,
                client_info=self._client_info,
            )

        request = clusters_pb2.CreateClusterRequest(
            project_id=project_id, region=region, cluster=cluster, request_id=request_id
        )
        operation = self._inner_api_calls["create_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            clusters_pb2.Cluster,
            metadata_type=proto_operations_pb2.ClusterOperationMetadata,
        )

    def update_cluster(
        self,
        project_id,
        region,
        cluster_name,
        cluster,
        update_mask,
        graceful_decommission_timeout=None,
        request_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a cluster in a project.

        Example:
            >>> from google.cloud import dataproc_v1
            >>>
            >>> client = dataproc_v1.ClusterControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `cluster_name`:
            >>> cluster_name = ''
            >>>
            >>> # TODO: Initialize `cluster`:
            >>> cluster = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_cluster(project_id, region, cluster_name, cluster, update_mask)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project the
                cluster belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            cluster_name (str): Required. The cluster name.
            cluster (Union[dict, ~google.cloud.dataproc_v1.types.Cluster]): Required. The changes to the cluster.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1.types.Cluster`
            update_mask (Union[dict, ~google.cloud.dataproc_v1.types.FieldMask]): Required. Specifies the path, relative to ``Cluster``, of the field to
                update. For example, to change the number of workers in a cluster to 5,
                the ``update_mask`` parameter would be specified as
                ``config.worker_config.num_instances``, and the ``PATCH`` request body
                would specify the new value, as follows:

                ::

                     {
                       "config":{
                         "workerConfig":{
                           "numInstances":"5"
                         }
                       }
                     }

                Similarly, to change the number of preemptible workers in a cluster to
                5, the ``update_mask`` parameter would be
                ``config.secondary_worker_config.num_instances``, and the ``PATCH``
                request body would be set as follows:

                ::

                     {
                       "config":{
                         "secondaryWorkerConfig":{
                           "numInstances":"5"
                         }
                       }
                     }

                Note: Currently, only the following fields can be updated:

                .. raw:: html

                   <table>

                .. raw:: html

                   <tbody>

                .. raw:: html

                   <tr>

                .. raw:: html

                   <td>

                Mask

                .. raw:: html

                   </td>

                .. raw:: html

                   <td>

                Purpose

                .. raw:: html

                   </td>

                .. raw:: html

                   </tr>

                .. raw:: html

                   <tr>

                .. raw:: html

                   <td>

                labels

                .. raw:: html

                   </td>

                .. raw:: html

                   <td>

                Update labels

                .. raw:: html

                   </td>

                .. raw:: html

                   </tr>

                .. raw:: html

                   <tr>

                .. raw:: html

                   <td>

                config.worker\_config.num\_instances

                .. raw:: html

                   </td>

                .. raw:: html

                   <td>

                Resize primary worker group

                .. raw:: html

                   </td>

                .. raw:: html

                   </tr>

                .. raw:: html

                   <tr>

                .. raw:: html

                   <td>

                config.secondary\_worker\_config.num\_instances

                .. raw:: html

                   </td>

                .. raw:: html

                   <td>

                Resize secondary worker group

                .. raw:: html

                   </td>

                .. raw:: html

                   </tr>

                .. raw:: html

                   </tbody>

                .. raw:: html

                   </table>

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1.types.FieldMask`
            graceful_decommission_timeout (Union[dict, ~google.cloud.dataproc_v1.types.Duration]): Optional. Timeout for graceful YARN decomissioning. Graceful
                decommissioning allows removing nodes from the cluster without
                interrupting jobs in progress. Timeout specifies how long to wait for jobs
                in progress to finish before forcefully removing nodes (and potentially
                interrupting jobs). Default timeout is 0 (for forceful decommission), and
                the maximum allowed timeout is 1 day.

                Only supported on Dataproc image versions 1.2 and higher.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1.types.Duration`
            request_id (str): Optional. A unique id used to identify the request. If the server
                receives two ``UpdateClusterRequest`` requests with the same id, then
                the second request will be ignored and the first
                ``google.longrunning.Operation`` created and stored in the backend is
                returned.

                It is recommended to always set this value to a
                `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__.

                The id must contain only letters (a-z, A-Z), numbers (0-9), underscores
                (\_), and hyphens (-). The maximum length is 40 characters.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_cluster,
                default_retry=self._method_configs["UpdateCluster"].retry,
                default_timeout=self._method_configs["UpdateCluster"].timeout,
                client_info=self._client_info,
            )

        request = clusters_pb2.UpdateClusterRequest(
            project_id=project_id,
            region=region,
            cluster_name=cluster_name,
            cluster=cluster,
            update_mask=update_mask,
            graceful_decommission_timeout=graceful_decommission_timeout,
            request_id=request_id,
        )
        operation = self._inner_api_calls["update_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            clusters_pb2.Cluster,
            metadata_type=proto_operations_pb2.ClusterOperationMetadata,
        )

    def delete_cluster(
        self,
        project_id,
        region,
        cluster_name,
        cluster_uuid=None,
        request_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a cluster in a project.

        Example:
            >>> from google.cloud import dataproc_v1
            >>>
            >>> client = dataproc_v1.ClusterControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `cluster_name`:
            >>> cluster_name = ''
            >>>
            >>> response = client.delete_cluster(project_id, region, cluster_name)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the cluster
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            cluster_name (str): Required. The cluster name.
            cluster_uuid (str): Optional. Specifying the ``cluster_uuid`` means the RPC should fail
                (with error NOT\_FOUND) if cluster with specified UUID does not exist.
            request_id (str): Optional. A unique id used to identify the request. If the server
                receives two ``DeleteClusterRequest`` requests with the same id, then
                the second request will be ignored and the first
                ``google.longrunning.Operation`` created and stored in the backend is
                returned.

                It is recommended to always set this value to a
                `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__.

                The id must contain only letters (a-z, A-Z), numbers (0-9), underscores
                (\_), and hyphens (-). The maximum length is 40 characters.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_cluster,
                default_retry=self._method_configs["DeleteCluster"].retry,
                default_timeout=self._method_configs["DeleteCluster"].timeout,
                client_info=self._client_info,
            )

        request = clusters_pb2.DeleteClusterRequest(
            project_id=project_id,
            region=region,
            cluster_name=cluster_name,
            cluster_uuid=cluster_uuid,
            request_id=request_id,
        )
        operation = self._inner_api_calls["delete_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.ClusterOperationMetadata,
        )

    def get_cluster(
        self,
        project_id,
        region,
        cluster_name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the resource representation for a cluster in a project.

        Example:
            >>> from google.cloud import dataproc_v1
            >>>
            >>> client = dataproc_v1.ClusterControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `cluster_name`:
            >>> cluster_name = ''
            >>>
            >>> response = client.get_cluster(project_id, region, cluster_name)

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the cluster
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            cluster_name (str): Required. The cluster name.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1.types.Cluster` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_cluster,
                default_retry=self._method_configs["GetCluster"].retry,
                default_timeout=self._method_configs["GetCluster"].timeout,
                client_info=self._client_info,
            )

        request = clusters_pb2.GetClusterRequest(
            project_id=project_id, region=region, cluster_name=cluster_name
        )
        return self._inner_api_calls["get_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_clusters(
        self,
        project_id,
        region,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all regions/{region}/clusters in a project.

        Example:
            >>> from google.cloud import dataproc_v1
            >>>
            >>> client = dataproc_v1.ClusterControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_clusters(project_id, region):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_clusters(project_id, region).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the cluster
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            filter_ (str): Optional. A filter constraining the clusters to list. Filters are
                case-sensitive and have the following syntax:

                field = value [AND [field = value]] ...

                where **field** is one of ``status.state``, ``clusterName``, or
                ``labels.[KEY]``, and ``[KEY]`` is a label key. **value** can be ``*``
                to match all values. ``status.state`` can be one of the following:
                ``ACTIVE``, ``INACTIVE``, ``CREATING``, ``RUNNING``, ``ERROR``,
                ``DELETING``, or ``UPDATING``. ``ACTIVE`` contains the ``CREATING``,
                ``UPDATING``, and ``RUNNING`` states. ``INACTIVE`` contains the
                ``DELETING`` and ``ERROR`` states. ``clusterName`` is the name of the
                cluster provided at creation time. Only the logical ``AND`` operator is
                supported; space-separated items are treated as having an implicit
                ``AND`` operator.

                Example filter:

                status.state = ACTIVE AND clusterName = mycluster AND labels.env =
                staging AND labels.starred = \*
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
            is an iterable of :class:`~google.cloud.dataproc_v1.types.Cluster` instances.
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
        if "list_clusters" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_clusters"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_clusters,
                default_retry=self._method_configs["ListClusters"].retry,
                default_timeout=self._method_configs["ListClusters"].timeout,
                client_info=self._client_info,
            )

        request = clusters_pb2.ListClustersRequest(
            project_id=project_id, region=region, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_clusters"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="clusters",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def diagnose_cluster(
        self,
        project_id,
        region,
        cluster_name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets cluster diagnostic information. After the operation completes, the
        Operation.response field contains ``DiagnoseClusterOutputLocation``.

        Example:
            >>> from google.cloud import dataproc_v1
            >>>
            >>> client = dataproc_v1.ClusterControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `cluster_name`:
            >>> cluster_name = ''
            >>>
            >>> response = client.diagnose_cluster(project_id, region, cluster_name)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the cluster
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            cluster_name (str): Required. The cluster name.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "diagnose_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "diagnose_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.diagnose_cluster,
                default_retry=self._method_configs["DiagnoseCluster"].retry,
                default_timeout=self._method_configs["DiagnoseCluster"].timeout,
                client_info=self._client_info,
            )

        request = clusters_pb2.DiagnoseClusterRequest(
            project_id=project_id, region=region, cluster_name=cluster_name
        )
        operation = self._inner_api_calls["diagnose_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=clusters_pb2.DiagnoseClusterResults,
        )
