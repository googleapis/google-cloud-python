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
from typing import (
    Dict,
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

from google.cloud.dataproc_v1 import gapic_version as package_version

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dataproc_v1.services.cluster_controller import pagers
from google.cloud.dataproc_v1.types import clusters
from google.cloud.dataproc_v1.types import operations
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
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
        cls,
        label: Optional[str] = None,
    ) -> Type[ClusterControllerTransport]:
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


class ClusterControllerClient(metaclass=ClusterControllerClientMeta):
    """The ClusterControllerService provides methods to manage
    clusters of Compute Engine instances.
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

    DEFAULT_ENDPOINT = "dataproc.googleapis.com"
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
            ClusterControllerClient: The constructed client.
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
            ClusterControllerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ClusterControllerTransport:
        """Returns the transport used by the client instance.

        Returns:
            ClusterControllerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def node_group_path(
        project: str,
        region: str,
        cluster: str,
        node_group: str,
    ) -> str:
        """Returns a fully-qualified node_group string."""
        return "projects/{project}/regions/{region}/clusters/{cluster}/nodeGroups/{node_group}".format(
            project=project,
            region=region,
            cluster=cluster,
            node_group=node_group,
        )

    @staticmethod
    def parse_node_group_path(path: str) -> Dict[str, str]:
        """Parses a node_group path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/regions/(?P<region>.+?)/clusters/(?P<cluster>.+?)/nodeGroups/(?P<node_group>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def service_path(
        project: str,
        location: str,
        service: str,
    ) -> str:
        """Returns a fully-qualified service string."""
        return "projects/{project}/locations/{location}/services/{service}".format(
            project=project,
            location=location,
            service=service,
        )

    @staticmethod
    def parse_service_path(path: str) -> Dict[str, str]:
        """Parses a service path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/services/(?P<service>.+?)$",
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
        transport: Optional[Union[str, ClusterControllerTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cluster controller client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ClusterControllerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
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
        client_options = cast(client_options_lib.ClientOptions, client_options)

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
        if isinstance(transport, ClusterControllerTransport):
            # transport is a ClusterControllerTransport instance.
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

    def create_cluster(
        self,
        request: Optional[Union[clusters.CreateClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        cluster: Optional[clusters.Cluster] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_create_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                cluster = dataproc_v1.Cluster()
                cluster.project_id = "project_id_value"
                cluster.cluster_name = "cluster_name_value"

                request = dataproc_v1.CreateClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster=cluster,
                )

                # Make the request
                operation = client.create_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.CreateClusterRequest, dict]):
                The request object. A request to create a cluster.
            project_id (str):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Required. The Dataproc region in
                which to handle the request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (google.cloud.dataproc_v1.types.Cluster):
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.dataproc_v1.types.Cluster` Describes the identifying information, config, and status of
                   a Dataproc cluster

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

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
        request: Optional[Union[clusters.UpdateClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        cluster_name: Optional[str] = None,
        cluster: Optional[clusters.Cluster] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.
        The cluster must be in a
        [``RUNNING``][google.cloud.dataproc.v1.ClusterStatus.State]
        state or an error is returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_update_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                cluster = dataproc_v1.Cluster()
                cluster.project_id = "project_id_value"
                cluster.cluster_name = "cluster_name_value"

                request = dataproc_v1.UpdateClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster_name="cluster_name_value",
                    cluster=cluster,
                )

                # Make the request
                operation = client.update_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.UpdateClusterRequest, dict]):
                The request object. A request to update a cluster.
            project_id (str):
                Required. The ID of the Google Cloud
                Platform project the cluster belongs to.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Required. The Dataproc region in
                which to handle the request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (str):
                Required. The cluster name.
                This corresponds to the ``cluster_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (google.cloud.dataproc_v1.types.Cluster):
                Required. The changes to the cluster.
                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.dataproc_v1.types.Cluster` Describes the identifying information, config, and status of
                   a Dataproc cluster

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                    ("cluster_name", request.cluster_name),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clusters.Cluster,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def stop_cluster(
        self,
        request: Optional[Union[clusters.StopClusterRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Stops a cluster in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_stop_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                request = dataproc_v1.StopClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster_name="cluster_name_value",
                )

                # Make the request
                operation = client.stop_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.StopClusterRequest, dict]):
                The request object. A request to stop a cluster.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.dataproc_v1.types.Cluster` Describes the identifying information, config, and status of
                   a Dataproc cluster

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.StopClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.StopClusterRequest):
            request = clusters.StopClusterRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                    ("cluster_name", request.cluster_name),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clusters.Cluster,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def start_cluster(
        self,
        request: Optional[Union[clusters.StartClusterRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a cluster in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_start_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                request = dataproc_v1.StartClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster_name="cluster_name_value",
                )

                # Make the request
                operation = client.start_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.StartClusterRequest, dict]):
                The request object. A request to start a cluster.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.dataproc_v1.types.Cluster` Describes the identifying information, config, and status of
                   a Dataproc cluster

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clusters.StartClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clusters.StartClusterRequest):
            request = clusters.StartClusterRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                    ("cluster_name", request.cluster_name),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

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
        request: Optional[Union[clusters.DeleteClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        cluster_name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a cluster in a project. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_delete_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                request = dataproc_v1.DeleteClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster_name="cluster_name_value",
                )

                # Make the request
                operation = client.delete_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.DeleteClusterRequest, dict]):
                The request object. A request to delete a cluster.
            project_id (str):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Required. The Dataproc region in
                which to handle the request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (str):
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                    ("cluster_name", request.cluster_name),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_cluster(
        self,
        request: Optional[Union[clusters.GetClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        cluster_name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clusters.Cluster:
        r"""Gets the resource representation for a cluster in a
        project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_get_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                request = dataproc_v1.GetClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster_name="cluster_name_value",
                )

                # Make the request
                response = client.get_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.GetClusterRequest, dict]):
                The request object. Request to get the resource
                representation for a cluster in a project.
            project_id (str):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Required. The Dataproc region in
                which to handle the request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (str):
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
            google.cloud.dataproc_v1.types.Cluster:
                Describes the identifying
                information, config, and status of a
                Dataproc cluster

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                    ("cluster_name", request.cluster_name),
                )
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

    def list_clusters(
        self,
        request: Optional[Union[clusters.ListClustersRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        filter: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListClustersPager:
        r"""Lists all regions/{region}/clusters in a project
        alphabetically.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_list_clusters():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                request = dataproc_v1.ListClustersRequest(
                    project_id="project_id_value",
                    region="region_value",
                )

                # Make the request
                page_result = client.list_clusters(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.ListClustersRequest, dict]):
                The request object. A request to list the clusters in a
                project.
            project_id (str):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Required. The Dataproc region in
                which to handle the request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
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
            google.cloud.dataproc_v1.services.cluster_controller.pagers.ListClustersPager:
                The list of all clusters in a
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                )
            ),
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
        response = pagers.ListClustersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def diagnose_cluster(
        self,
        request: Optional[Union[clusters.DiagnoseClusterRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        cluster_name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Gets cluster diagnostic information. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] will
        be
        `ClusterOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#clusteroperationmetadata>`__.
        After the operation completes,
        [Operation.response][google.longrunning.Operation.response]
        contains
        `DiagnoseClusterResults <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#diagnoseclusterresults>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            def sample_diagnose_cluster():
                # Create a client
                client = dataproc_v1.ClusterControllerClient()

                # Initialize request argument(s)
                request = dataproc_v1.DiagnoseClusterRequest(
                    project_id="project_id_value",
                    region="region_value",
                    cluster_name="cluster_name_value",
                )

                # Make the request
                operation = client.diagnose_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataproc_v1.types.DiagnoseClusterRequest, dict]):
                The request object. A request to collect cluster
                diagnostic information.
            project_id (str):
                Required. The ID of the Google Cloud
                Platform project that the cluster
                belongs to.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Required. The Dataproc region in
                which to handle the request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_name (str):
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dataproc_v1.types.DiagnoseClusterResults`
                The location of diagnostic output.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project_id", request.project_id),
                    ("region", request.region),
                    ("cluster_name", request.cluster_name),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clusters.DiagnoseClusterResults,
            metadata_type=operations.ClusterOperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ClusterControllerClient":
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


__all__ = ("ClusterControllerClient",)
