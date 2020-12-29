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

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dataproc_v1beta2.services.cluster_controller import pagers
from google.cloud.dataproc_v1beta2.types import clusters
from google.cloud.dataproc_v1beta2.types import operations
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore

from .transports.base import ClusterControllerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import ClusterControllerGrpcTransport
from .transports.grpc_asyncio import ClusterControllerGrpcAsyncIOTransport


class ClusterControllerClientMeta(type):
    """Metaclass for the ClusterController client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ClusterControllerTransport]]
    _transport_registry["grpc"] = ClusterControllerGrpcTransport
    _transport_registry["grpc_asyncio"] = ClusterControllerGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[ClusterControllerTransport]:
        """Return an appropriate transport class.

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


class ClusterControllerClient(metaclass=ClusterControllerClientMeta):
    """The ClusterControllerService provides methods to manage
    clusters of Compute Engine instances.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
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

    DEFAULT_ENDPOINT = "dataproc.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ClusterControllerTransport:
        """Return the transport used by the client instance.

        Returns:
            ClusterControllerTransport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def cluster_path(project: str, location: str, cluster: str,) -> str:
        """Return a fully-qualified cluster string."""
        return "projects/{project}/locations/{location}/clusters/{cluster}".format(
            project=project, location=location, cluster=cluster,
        )

    @staticmethod
    def parse_cluster_path(path: str) -> Dict[str, str]:
        """Parse a cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/clusters/(?P<cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
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
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
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
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, ClusterControllerTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
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
            client_options (client_options_lib.ClientOptions): Custom options for the
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

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

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
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ClusterControllerTransport):
            # transport is a ClusterControllerTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_cluster(
        self,
        request: clusters.CreateClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster: clusters.Cluster = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1beta2#clusteroperationmetadata>`__.

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
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.clusters.Cluster``: Describes the identifying
                information, config, and status of a cluster of Compute
                Engine instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, region, cluster])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.CreateClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.CreateClusterRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.create_cluster]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clusters.Cluster,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_cluster(
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
    ) -> operation.Operation:
        r"""Updates a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1beta2#clusteroperationmetadata>`__.

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

                Note: currently only the following fields can be
                updated:

                .. raw:: html

                    <table>
                    <tr>
                    <td><strong>Mask</strong></td><td><strong>Purpose</strong></td>
                    </tr>
                    <tr>
                    <td>labels</td><td>Updates labels</td>
                    </tr>
                    <tr>
                    <td>config.worker_config.num_instances</td><td>Resize primary worker
                    group</td>
                    </tr>
                    <tr>
                    <td>config.secondary_worker_config.num_instances</td><td>Resize secondary
                    worker group</td>
                    </tr>
                    <tr>
                    <td>config.lifecycle_config.auto_delete_ttl</td><td>Reset MAX TTL
                    duration</td>
                    </tr>
                    <tr>
                    <td>config.lifecycle_config.auto_delete_time</td><td>Update MAX TTL
                    deletion timestamp</td>
                    </tr>
                    <tr>
                    <td>config.lifecycle_config.idle_delete_ttl</td><td>Update Idle TTL
                    duration</td>
                    </tr>
                    <tr>
                    <td>config.autoscaling_config.policy_uri</td><td>Use, stop using, or change
                    autoscaling policies</td>
                    </tr>
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
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.clusters.Cluster``: Describes the identifying
                information, config, and status of a cluster of Compute
                Engine instances.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project_id, region, cluster_name, cluster, update_mask]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.UpdateClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.UpdateClusterRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.update_cluster]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clusters.Cluster,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_cluster(
        self,
        request: clusters.DeleteClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1beta2#clusteroperationmetadata>`__.

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
            ~.operation.Operation:
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
        has_flattened_params = any([project_id, region, cluster_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.DeleteClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.DeleteClusterRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.delete_cluster]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_cluster(
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
        has_flattened_params = any([project_id, region, cluster_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.GetClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.GetClusterRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.get_cluster]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_clusters(
        self,
        request: clusters.ListClustersRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListClustersPager:
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
            ~.pagers.ListClustersPager:
                The list of all clusters in a
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, region, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.ListClustersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.ListClustersRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.list_clusters]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListClustersPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def diagnose_cluster(
        self,
        request: clusters.DiagnoseClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Gets cluster diagnostic information. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1beta2#clusteroperationmetadata>`__.
        After the operation completes,
        [Operation.response][google.longrunning.Operation.response]
        contains [Empty][google.protobuf.Empty].

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
            ~.operation.Operation:
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
        has_flattened_params = any([project_id, region, cluster_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.DiagnoseClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.DiagnoseClusterRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.diagnose_cluster]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataproc",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ClusterControllerClient",)
