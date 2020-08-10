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
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.dataproc_v1.services.cluster_controller import pagers
from google.cloud.dataproc_v1.types import clusters
from google.cloud.dataproc_v1.types import operations
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore

from .transports.base import ClusterControllerTransport
from .transports.grpc_asyncio import ClusterControllerGrpcAsyncIOTransport
from .client import ClusterControllerClient


class ClusterControllerAsyncClient:
    """The ClusterControllerService provides methods to manage
    clusters of Compute Engine instances.
    """

    _client: ClusterControllerClient

    DEFAULT_ENDPOINT = ClusterControllerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ClusterControllerClient.DEFAULT_MTLS_ENDPOINT

    from_service_account_file = ClusterControllerClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(ClusterControllerClient).get_transport_class, type(ClusterControllerClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, ClusterControllerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the cluster controller client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ClusterControllerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = ClusterControllerClient(
            credentials=credentials, transport=transport, client_options=client_options,
        )

    async def create_cluster(
        self,
        request: clusters.CreateClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster: clusters.Cluster = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.

        Args:
            request (:class:`~.clusters.CreateClusterRequest`):
                The request object. A request to create a cluster.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (:class:`~.clusters.Cluster`):
                Required. The cluster to create.
                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.clusters.Cluster``: Describes the identifying
                information, config, and status of a cluster of Compute
                Engine instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, cluster]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = clusters.CreateClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if cluster is not None:
            request.cluster = cluster

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_cluster,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=300.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            clusters.Cluster,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_cluster(
        self,
        request: clusters.UpdateClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        cluster: clusters.Cluster = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.

        Args:
            request (:class:`~.clusters.UpdateClusterRequest`):
                The request object. A request to update a cluster.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project the cluster belongs to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (:class:`str`):
                Required. The cluster name.
                This corresponds to the ``cluster_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (:class:`~.clusters.Cluster`):
                Required. The changes to the cluster.
                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. Specifies the path, relative to ``Cluster``,
                of the field to update. For example, to change the
                number of workers in a cluster to 5, the ``update_mask``
                parameter would be specified as
                ``config.worker_config.num_instances``, and the
                ``PATCH`` request body would specify the new value, as
                follows:

                ::

                    {
                      "config":{
                        "workerConfig":{
                          "numInstances":"5"
                        }
                      }
                    }

                Similarly, to change the number of preemptible workers
                in a cluster to 5, the ``update_mask`` parameter would
                be ``config.secondary_worker_config.num_instances``, and
                the ``PATCH`` request body would be set as follows:

                ::

                    {
                      "config":{
                        "secondaryWorkerConfig":{
                          "numInstances":"5"
                        }
                      }
                    }

                Note: Currently, only the following fields can be
                updated:

                .. raw:: html

                     <table>
                     <tbody>
                     <tr>
                     <td><strong>Mask</strong></td>
                     <td><strong>Purpose</strong></td>
                     </tr>
                     <tr>
                     <td><strong><em>labels</em></strong></td>
                     <td>Update labels</td>
                     </tr>
                     <tr>
                     <td><strong><em>config.worker_config.num_instances</em></strong></td>
                     <td>Resize primary worker group</td>
                     </tr>
                     <tr>
                     <td><strong><em>config.secondary_worker_config.num_instances</em></strong></td>
                     <td>Resize secondary worker group</td>
                     </tr>
                     <tr>
                     <td>config.autoscaling_config.policy_uri</td><td>Use, stop using, or
                     change autoscaling policies</td>
                     </tr>
                     </tbody>
                     </table>
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.clusters.Cluster``: Describes the identifying
                information, config, and status of a cluster of Compute
                Engine instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any(
            [project_id, region, cluster_name, cluster, update_mask]
        ):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = clusters.UpdateClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if cluster_name is not None:
            request.cluster_name = cluster_name
        if cluster is not None:
            request.cluster = cluster
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_cluster,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=300.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            clusters.Cluster,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_cluster(
        self,
        request: clusters.DeleteClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.

        Args:
            request (:class:`~.clusters.DeleteClusterRequest`):
                The request object. A request to delete a cluster.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (:class:`str`):
                Required. The cluster name.
                This corresponds to the ``cluster_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, cluster_name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = clusters.DeleteClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if cluster_name is not None:
            request.cluster_name = cluster_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_cluster,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=300.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty.Empty,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_cluster(
        self,
        request: clusters.GetClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clusters.Cluster:
        r"""Gets the resource representation for a cluster in a
        project.

        Args:
            request (:class:`~.clusters.GetClusterRequest`):
                The request object. Request to get the resource
                representation for a cluster in a project.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (:class:`str`):
                Required. The cluster name.
                This corresponds to the ``cluster_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.clusters.Cluster:
                Describes the identifying
                information, config, and status of a
                cluster of Compute Engine instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, cluster_name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = clusters.GetClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if cluster_name is not None:
            request.cluster_name = cluster_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_cluster,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.InternalServerError,
                    exceptions.ServiceUnavailable,
                    exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=300.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_clusters(
        self,
        request: clusters.ListClustersRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListClustersAsyncPager:
        r"""Lists all regions/{region}/clusters in a project
        alphabetically.

        Args:
            request (:class:`~.clusters.ListClustersRequest`):
                The request object. A request to list the clusters in a
                project.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Optional. A filter constraining the clusters to list.
                Filters are case-sensitive and have the following
                syntax:

                field = value [AND [field = value]] ...

                where **field** is one of ``status.state``,
                ``clusterName``, or ``labels.[KEY]``, and ``[KEY]`` is a
                label key. **value** can be ``*`` to match all values.
                ``status.state`` can be one of the following:
                ``ACTIVE``, ``INACTIVE``, ``CREATING``, ``RUNNING``,
                ``ERROR``, ``DELETING``, or ``UPDATING``. ``ACTIVE``
                contains the ``CREATING``, ``UPDATING``, and ``RUNNING``
                states. ``INACTIVE`` contains the ``DELETING`` and
                ``ERROR`` states. ``clusterName`` is the name of the
                cluster provided at creation time. Only the logical
                ``AND`` operator is supported; space-separated items are
                treated as having an implicit ``AND`` operator.

                Example filter:

                status.state = ACTIVE AND clusterName = mycluster AND
                labels.env = staging AND labels.starred = \*
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListClustersAsyncPager:
                The list of all clusters in a
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, filter]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = clusters.ListClustersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if filter is not None:
            request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_clusters,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.InternalServerError,
                    exceptions.ServiceUnavailable,
                    exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=300.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListClustersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def diagnose_cluster(
        self,
        request: clusters.DiagnoseClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Gets cluster diagnostic information. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.
        After the operation completes,
        [Operation.response][google.longrunning.Operation.response]
        contains
        `DiagnoseClusterResults <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#diagnoseclusterresults>`__.

        Args:
            request (:class:`~.clusters.DiagnoseClusterRequest`):
                The request object. A request to collect cluster
                diagnostic information.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (:class:`str`):
                Required. The cluster name.
                This corresponds to the ``cluster_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.clusters.DiagnoseClusterResults``: The
                location of diagnostic output.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, cluster_name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = clusters.DiagnoseClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if cluster_name is not None:
            request.cluster_name = cluster_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.diagnose_cluster,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=300.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            clusters.DiagnoseClusterResults,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataproc",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("ClusterControllerAsyncClient",)
