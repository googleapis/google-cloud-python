# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.gke_multicloud_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.gke_multicloud_v1.services.aws_clusters import pagers
from google.cloud.gke_multicloud_v1.types import (
    aws_resources,
    aws_service,
    common_resources,
)

from .transports.base import DEFAULT_CLIENT_INFO, AwsClustersTransport
from .transports.grpc import AwsClustersGrpcTransport
from .transports.grpc_asyncio import AwsClustersGrpcAsyncIOTransport
from .transports.rest import AwsClustersRestTransport


class AwsClustersClientMeta(type):
    """Metaclass for the AwsClusters client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[AwsClustersTransport]]
    _transport_registry["grpc"] = AwsClustersGrpcTransport
    _transport_registry["grpc_asyncio"] = AwsClustersGrpcAsyncIOTransport
    _transport_registry["rest"] = AwsClustersRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[AwsClustersTransport]:
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


class AwsClustersClient(metaclass=AwsClustersClientMeta):
    """The AwsClusters API provides a single centrally managed
    service to create and manage Anthos clusters that run on AWS
    infrastructure.
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

    DEFAULT_ENDPOINT = "gkemulticloud.googleapis.com"
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
            AwsClustersClient: The constructed client.
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
            AwsClustersClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AwsClustersTransport:
        """Returns the transport used by the client instance.

        Returns:
            AwsClustersTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def aws_cluster_path(
        project: str,
        location: str,
        aws_cluster: str,
    ) -> str:
        """Returns a fully-qualified aws_cluster string."""
        return (
            "projects/{project}/locations/{location}/awsClusters/{aws_cluster}".format(
                project=project,
                location=location,
                aws_cluster=aws_cluster,
            )
        )

    @staticmethod
    def parse_aws_cluster_path(path: str) -> Dict[str, str]:
        """Parses a aws_cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/awsClusters/(?P<aws_cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def aws_node_pool_path(
        project: str,
        location: str,
        aws_cluster: str,
        aws_node_pool: str,
    ) -> str:
        """Returns a fully-qualified aws_node_pool string."""
        return "projects/{project}/locations/{location}/awsClusters/{aws_cluster}/awsNodePools/{aws_node_pool}".format(
            project=project,
            location=location,
            aws_cluster=aws_cluster,
            aws_node_pool=aws_node_pool,
        )

    @staticmethod
    def parse_aws_node_pool_path(path: str) -> Dict[str, str]:
        """Parses a aws_node_pool path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/awsClusters/(?P<aws_cluster>.+?)/awsNodePools/(?P<aws_node_pool>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def aws_server_config_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified aws_server_config string."""
        return "projects/{project}/locations/{location}/awsServerConfig".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_aws_server_config_path(path: str) -> Dict[str, str]:
        """Parses a aws_server_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/awsServerConfig$",
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
        transport: Optional[Union[str, AwsClustersTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the aws clusters client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, AwsClustersTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
                NOTE: "rest" transport functionality is currently in a
                beta state (preview). We welcome your feedback via an
                issue in this library's source repository.
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
        if isinstance(transport, AwsClustersTransport):
            # transport is a AwsClustersTransport instance.
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

    def create_aws_cluster(
        self,
        request: Optional[Union[aws_service.CreateAwsClusterRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        aws_cluster: Optional[aws_resources.AwsCluster] = None,
        aws_cluster_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster] resource
        on a given Google Cloud Platform project and region.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_create_aws_cluster():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                aws_cluster = gke_multicloud_v1.AwsCluster()
                aws_cluster.networking.vpc_id = "vpc_id_value"
                aws_cluster.networking.pod_address_cidr_blocks = ['pod_address_cidr_blocks_value1', 'pod_address_cidr_blocks_value2']
                aws_cluster.networking.service_address_cidr_blocks = ['service_address_cidr_blocks_value1', 'service_address_cidr_blocks_value2']
                aws_cluster.aws_region = "aws_region_value"
                aws_cluster.control_plane.version = "version_value"
                aws_cluster.control_plane.subnet_ids = ['subnet_ids_value1', 'subnet_ids_value2']
                aws_cluster.control_plane.iam_instance_profile = "iam_instance_profile_value"
                aws_cluster.control_plane.database_encryption.kms_key_arn = "kms_key_arn_value"
                aws_cluster.control_plane.aws_services_authentication.role_arn = "role_arn_value"
                aws_cluster.control_plane.config_encryption.kms_key_arn = "kms_key_arn_value"
                aws_cluster.authorization.admin_users.username = "username_value"
                aws_cluster.fleet.project = "project_value"

                request = gke_multicloud_v1.CreateAwsClusterRequest(
                    parent="parent_value",
                    aws_cluster=aws_cluster,
                    aws_cluster_id="aws_cluster_id_value",
                )

                # Make the request
                operation = client.create_aws_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.CreateAwsClusterRequest, dict]):
                The request object. Request message for ``AwsClusters.CreateAwsCluster``
                method.
            parent (str):
                Required. The parent location where this
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                resource will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            aws_cluster (google.cloud.gke_multicloud_v1.types.AwsCluster):
                Required. The specification of the
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                to create.

                This corresponds to the ``aws_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            aws_cluster_id (str):
                Required. A client provided ID the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                This corresponds to the ``aws_cluster_id`` field
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
                :class:`google.cloud.gke_multicloud_v1.types.AwsCluster`
                An Anthos cluster running on AWS.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, aws_cluster, aws_cluster_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.CreateAwsClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.CreateAwsClusterRequest):
            request = aws_service.CreateAwsClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if aws_cluster is not None:
                request.aws_cluster = aws_cluster
            if aws_cluster_id is not None:
                request.aws_cluster_id = aws_cluster_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_aws_cluster]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            aws_resources.AwsCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_aws_cluster(
        self,
        request: Optional[Union[aws_service.UpdateAwsClusterRequest, dict]] = None,
        *,
        aws_cluster: Optional[aws_resources.AwsCluster] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates an
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_update_aws_cluster():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                aws_cluster = gke_multicloud_v1.AwsCluster()
                aws_cluster.networking.vpc_id = "vpc_id_value"
                aws_cluster.networking.pod_address_cidr_blocks = ['pod_address_cidr_blocks_value1', 'pod_address_cidr_blocks_value2']
                aws_cluster.networking.service_address_cidr_blocks = ['service_address_cidr_blocks_value1', 'service_address_cidr_blocks_value2']
                aws_cluster.aws_region = "aws_region_value"
                aws_cluster.control_plane.version = "version_value"
                aws_cluster.control_plane.subnet_ids = ['subnet_ids_value1', 'subnet_ids_value2']
                aws_cluster.control_plane.iam_instance_profile = "iam_instance_profile_value"
                aws_cluster.control_plane.database_encryption.kms_key_arn = "kms_key_arn_value"
                aws_cluster.control_plane.aws_services_authentication.role_arn = "role_arn_value"
                aws_cluster.control_plane.config_encryption.kms_key_arn = "kms_key_arn_value"
                aws_cluster.authorization.admin_users.username = "username_value"
                aws_cluster.fleet.project = "project_value"

                request = gke_multicloud_v1.UpdateAwsClusterRequest(
                    aws_cluster=aws_cluster,
                )

                # Make the request
                operation = client.update_aws_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.UpdateAwsClusterRequest, dict]):
                The request object. Request message for ``AwsClusters.UpdateAwsCluster``
                method.
            aws_cluster (google.cloud.gke_multicloud_v1.types.AwsCluster):
                Required. The
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                resource to update.

                This corresponds to the ``aws_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask of fields to update. At least one path
                must be supplied in this field. The elements of the
                repeated paths field can only include these fields from
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]:

                -  ``description``.
                -  ``annotations``.
                -  ``control_plane.version``.
                -  ``authorization.admin_users``.
                -  ``control_plane.aws_services_authentication.role_arn``.
                -  ``control_plane.aws_services_authentication.role_session_name``.
                -  ``control_plane.config_encryption.kms_key_arn``.
                -  ``control_plane.instance_type``.
                -  ``control_plane.security_group_ids``.
                -  ``control_plane.proxy_config``.
                -  ``control_plane.proxy_config.secret_arn``.
                -  ``control_plane.proxy_config.secret_version``.
                -  ``control_plane.root_volume.size_gib``.
                -  ``control_plane.root_volume.volume_type``.
                -  ``control_plane.root_volume.iops``.
                -  ``control_plane.root_volume.kms_key_arn``.
                -  ``control_plane.ssh_config``.
                -  ``control_plane.ssh_config.ec2_key_pair``.
                -  ``control_plane.instance_placement.tenancy``.
                -  ``control_plane.iam_instance_profile``.
                -  ``logging_config.component_config.enable_components``.
                -  ``control_plane.tags``.
                -  ``monitoring_config.managed_prometheus_config.enabled``.

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

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AwsCluster`
                An Anthos cluster running on AWS.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([aws_cluster, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.UpdateAwsClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.UpdateAwsClusterRequest):
            request = aws_service.UpdateAwsClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if aws_cluster is not None:
                request.aws_cluster = aws_cluster
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_aws_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("aws_cluster.name", request.aws_cluster.name),)
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
            aws_resources.AwsCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_aws_cluster(
        self,
        request: Optional[Union[aws_service.GetAwsClusterRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> aws_resources.AwsCluster:
        r"""Describes a specific
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster] resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_aws_cluster():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAwsClusterRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_aws_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAwsClusterRequest, dict]):
                The request object. Request message for ``AwsClusters.GetAwsCluster``
                method.
            name (str):
                Required. The name of the
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                resource to describe.

                ``AwsCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AwsCluster:
                An Anthos cluster running on AWS.
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
        # in a aws_service.GetAwsClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.GetAwsClusterRequest):
            request = aws_service.GetAwsClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_aws_cluster]

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

    def list_aws_clusters(
        self,
        request: Optional[Union[aws_service.ListAwsClustersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAwsClustersPager:
        r"""Lists all [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
        resources on a given Google Cloud project and region.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_list_aws_clusters():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ListAwsClustersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_aws_clusters(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.ListAwsClustersRequest, dict]):
                The request object. Request message for ``AwsClusters.ListAwsClusters``
                method.
            parent (str):
                Required. The parent location which owns this collection
                of
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                resources.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.services.aws_clusters.pagers.ListAwsClustersPager:
                Response message for AwsClusters.ListAwsClusters method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        # in a aws_service.ListAwsClustersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.ListAwsClustersRequest):
            request = aws_service.ListAwsClustersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_aws_clusters]

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
        response = pagers.ListAwsClustersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_aws_cluster(
        self,
        request: Optional[Union[aws_service.DeleteAwsClusterRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a specific
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster] resource.

        Fails if the cluster has one or more associated
        [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
        resources.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_delete_aws_cluster():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.DeleteAwsClusterRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_aws_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.DeleteAwsClusterRequest, dict]):
                The request object. Request message for ``AwsClusters.DeleteAwsCluster``
                method.
            name (str):
                Required. The resource name the
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                to delete.

                ``AwsCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``name`` field
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.DeleteAwsClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.DeleteAwsClusterRequest):
            request = aws_service.DeleteAwsClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_aws_cluster]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def generate_aws_access_token(
        self,
        request: Optional[
            Union[aws_service.GenerateAwsAccessTokenRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> aws_service.GenerateAwsAccessTokenResponse:
        r"""Generates a short-lived access token to authenticate to a given
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster] resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_generate_aws_access_token():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GenerateAwsAccessTokenRequest(
                    aws_cluster="aws_cluster_value",
                )

                # Make the request
                response = client.generate_aws_access_token(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GenerateAwsAccessTokenRequest, dict]):
                The request object. Request message for
                ``AwsClusters.GenerateAwsAccessToken`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.GenerateAwsAccessTokenResponse:
                Response message for AwsClusters.GenerateAwsAccessToken
                method.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.GenerateAwsAccessTokenRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.GenerateAwsAccessTokenRequest):
            request = aws_service.GenerateAwsAccessTokenRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_aws_access_token
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("aws_cluster", request.aws_cluster),)
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

    def create_aws_node_pool(
        self,
        request: Optional[Union[aws_service.CreateAwsNodePoolRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        aws_node_pool: Optional[aws_resources.AwsNodePool] = None,
        aws_node_pool_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new
        [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool],
        attached to a given
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster].

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_create_aws_node_pool():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                aws_node_pool = gke_multicloud_v1.AwsNodePool()
                aws_node_pool.version = "version_value"
                aws_node_pool.config.iam_instance_profile = "iam_instance_profile_value"
                aws_node_pool.config.config_encryption.kms_key_arn = "kms_key_arn_value"
                aws_node_pool.autoscaling.min_node_count = 1489
                aws_node_pool.autoscaling.max_node_count = 1491
                aws_node_pool.subnet_id = "subnet_id_value"
                aws_node_pool.max_pods_constraint.max_pods_per_node = 1798

                request = gke_multicloud_v1.CreateAwsNodePoolRequest(
                    parent="parent_value",
                    aws_node_pool=aws_node_pool,
                    aws_node_pool_id="aws_node_pool_id_value",
                )

                # Make the request
                operation = client.create_aws_node_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.CreateAwsNodePoolRequest, dict]):
                The request object. Response message for ``AwsClusters.CreateAwsNodePool``
                method.
            parent (str):
                Required. The
                [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
                resource where this node pool will be created.

                ``AwsCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            aws_node_pool (google.cloud.gke_multicloud_v1.types.AwsNodePool):
                Required. The specification of the
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
                to create.

                This corresponds to the ``aws_node_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            aws_node_pool_id (str):
                Required. A client provided ID the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>/awsNodePools/<node-pool-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                This corresponds to the ``aws_node_pool_id`` field
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
                :class:`google.cloud.gke_multicloud_v1.types.AwsNodePool`
                An Anthos node pool running on AWS.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, aws_node_pool, aws_node_pool_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.CreateAwsNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.CreateAwsNodePoolRequest):
            request = aws_service.CreateAwsNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if aws_node_pool is not None:
                request.aws_node_pool = aws_node_pool
            if aws_node_pool_id is not None:
                request.aws_node_pool_id = aws_node_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_aws_node_pool]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            aws_resources.AwsNodePool,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_aws_node_pool(
        self,
        request: Optional[Union[aws_service.UpdateAwsNodePoolRequest, dict]] = None,
        *,
        aws_node_pool: Optional[aws_resources.AwsNodePool] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates an
        [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_update_aws_node_pool():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                aws_node_pool = gke_multicloud_v1.AwsNodePool()
                aws_node_pool.version = "version_value"
                aws_node_pool.config.iam_instance_profile = "iam_instance_profile_value"
                aws_node_pool.config.config_encryption.kms_key_arn = "kms_key_arn_value"
                aws_node_pool.autoscaling.min_node_count = 1489
                aws_node_pool.autoscaling.max_node_count = 1491
                aws_node_pool.subnet_id = "subnet_id_value"
                aws_node_pool.max_pods_constraint.max_pods_per_node = 1798

                request = gke_multicloud_v1.UpdateAwsNodePoolRequest(
                    aws_node_pool=aws_node_pool,
                )

                # Make the request
                operation = client.update_aws_node_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.UpdateAwsNodePoolRequest, dict]):
                The request object. Request message for ``AwsClusters.UpdateAwsNodePool``
                method.
            aws_node_pool (google.cloud.gke_multicloud_v1.types.AwsNodePool):
                Required. The
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
                resource to update.

                This corresponds to the ``aws_node_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask of fields to update. At least one path
                must be supplied in this field. The elements of the
                repeated paths field can only include these fields from
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]:

                -  ``annotations``.
                -  ``version``.
                -  ``autoscaling.min_node_count``.
                -  ``autoscaling.max_node_count``.
                -  ``config.config_encryption.kms_key_arn``.
                -  ``config.security_group_ids``.
                -  ``config.root_volume.iops``.
                -  ``config.root_volume.kms_key_arn``.
                -  ``config.root_volume.volume_type``.
                -  ``config.root_volume.size_gib``.
                -  ``config.proxy_config``.
                -  ``config.proxy_config.secret_arn``.
                -  ``config.proxy_config.secret_version``.
                -  ``config.ssh_config``.
                -  ``config.ssh_config.ec2_key_pair``.
                -  ``config.instance_placement.tenancy``.
                -  ``config.iam_instance_profile``.
                -  ``config.labels``.
                -  ``config.tags``.
                -  ``config.autoscaling_metrics_collection``.
                -  ``config.autoscaling_metrics_collection.granularity``.
                -  ``config.autoscaling_metrics_collection.metrics``.

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

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AwsNodePool`
                An Anthos node pool running on AWS.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([aws_node_pool, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.UpdateAwsNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.UpdateAwsNodePoolRequest):
            request = aws_service.UpdateAwsNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if aws_node_pool is not None:
                request.aws_node_pool = aws_node_pool
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_aws_node_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("aws_node_pool.name", request.aws_node_pool.name),)
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
            aws_resources.AwsNodePool,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_aws_node_pool(
        self,
        request: Optional[Union[aws_service.GetAwsNodePoolRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> aws_resources.AwsNodePool:
        r"""Describes a specific
        [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_aws_node_pool():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAwsNodePoolRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_aws_node_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAwsNodePoolRequest, dict]):
                The request object. Request message for ``AwsClusters.GetAwsNodePool``
                method.
            name (str):
                Required. The name of the
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
                resource to describe.

                ``AwsNodePool`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>/awsNodePools/<node-pool-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AwsNodePool:
                An Anthos node pool running on AWS.
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
        # in a aws_service.GetAwsNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.GetAwsNodePoolRequest):
            request = aws_service.GetAwsNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_aws_node_pool]

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

    def list_aws_node_pools(
        self,
        request: Optional[Union[aws_service.ListAwsNodePoolsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAwsNodePoolsPager:
        r"""Lists all
        [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
        resources on a given
        [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_list_aws_node_pools():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ListAwsNodePoolsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_aws_node_pools(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.ListAwsNodePoolsRequest, dict]):
                The request object. Request message for ``AwsClusters.ListAwsNodePools``
                method.
            parent (str):
                Required. The parent ``AwsCluster`` which owns this
                collection of
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
                resources.

                ``AwsCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.services.aws_clusters.pagers.ListAwsNodePoolsPager:
                Response message for AwsClusters.ListAwsNodePools
                method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        # in a aws_service.ListAwsNodePoolsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.ListAwsNodePoolsRequest):
            request = aws_service.ListAwsNodePoolsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_aws_node_pools]

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
        response = pagers.ListAwsNodePoolsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_aws_node_pool(
        self,
        request: Optional[Union[aws_service.DeleteAwsNodePoolRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a specific
        [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
        resource.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_delete_aws_node_pool():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.DeleteAwsNodePoolRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_aws_node_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.DeleteAwsNodePoolRequest, dict]):
                The request object. Request message for ``AwsClusters.DeleteAwsNodePool``
                method.
            name (str):
                Required. The resource name the
                [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
                to delete.

                ``AwsNodePool`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>/awsNodePools/<node-pool-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a aws_service.DeleteAwsNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.DeleteAwsNodePoolRequest):
            request = aws_service.DeleteAwsNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_aws_node_pool]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_aws_server_config(
        self,
        request: Optional[Union[aws_service.GetAwsServerConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> aws_resources.AwsServerConfig:
        r"""Returns information, such as supported AWS regions
        and Kubernetes versions, on a given Google Cloud
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_aws_server_config():
                # Create a client
                client = gke_multicloud_v1.AwsClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAwsServerConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_aws_server_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAwsServerConfigRequest, dict]):
                The request object. GetAwsServerConfigRequest gets the
                server config of GKE cluster on AWS.
            name (str):
                Required. The name of the
                [AwsServerConfig][google.cloud.gkemulticloud.v1.AwsServerConfig]
                resource to describe.

                ``AwsServerConfig`` names are formatted as
                ``projects/<project-id>/locations/<region>/awsServerConfig``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AwsServerConfig:
                AwsServerConfig is the configuration
                of GKE cluster on AWS.

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
        # in a aws_service.GetAwsServerConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, aws_service.GetAwsServerConfigRequest):
            request = aws_service.GetAwsServerConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_aws_server_config]

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

    def __enter__(self) -> "AwsClustersClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AwsClustersClient",)
