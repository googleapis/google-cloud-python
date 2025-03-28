# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.gkehub_v1.types import feature, membership, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseGkeHubRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class GkeHubRestInterceptor:
    """Interceptor for GkeHub.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the GkeHubRestTransport.

    .. code-block:: python
        class MyCustomGkeHubInterceptor(GkeHubRestInterceptor):
            def pre_create_feature(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_feature(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_feature(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_feature(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_connect_manifest(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_connect_manifest(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_feature(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_feature(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_features(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_features(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_memberships(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_memberships(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_feature(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_feature(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = GkeHubRestTransport(interceptor=MyCustomGkeHubInterceptor())
        client = GkeHubClient(transport=transport)


    """

    def pre_create_feature(
        self,
        request: service.CreateFeatureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateFeatureRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_feature

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_create_feature(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_feature

        DEPRECATED. Please use the `post_create_feature_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_create_feature` interceptor runs
        before the `post_create_feature_with_metadata` interceptor.
        """
        return response

    def post_create_feature_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_feature

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_create_feature_with_metadata`
        interceptor in new development instead of the `post_create_feature` interceptor.
        When both interceptors are used, this `post_create_feature_with_metadata` interceptor runs after the
        `post_create_feature` interceptor. The (possibly modified) response returned by
        `post_create_feature` will be passed to
        `post_create_feature_with_metadata`.
        """
        return response, metadata

    def pre_create_membership(
        self,
        request: service.CreateMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.CreateMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_create_membership(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_membership

        DEPRECATED. Please use the `post_create_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_create_membership` interceptor runs
        before the `post_create_membership_with_metadata` interceptor.
        """
        return response

    def post_create_membership_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_create_membership_with_metadata`
        interceptor in new development instead of the `post_create_membership` interceptor.
        When both interceptors are used, this `post_create_membership_with_metadata` interceptor runs after the
        `post_create_membership` interceptor. The (possibly modified) response returned by
        `post_create_membership` will be passed to
        `post_create_membership_with_metadata`.
        """
        return response, metadata

    def pre_delete_feature(
        self,
        request: service.DeleteFeatureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteFeatureRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_feature

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_delete_feature(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_feature

        DEPRECATED. Please use the `post_delete_feature_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_delete_feature` interceptor runs
        before the `post_delete_feature_with_metadata` interceptor.
        """
        return response

    def post_delete_feature_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_feature

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_delete_feature_with_metadata`
        interceptor in new development instead of the `post_delete_feature` interceptor.
        When both interceptors are used, this `post_delete_feature_with_metadata` interceptor runs after the
        `post_delete_feature` interceptor. The (possibly modified) response returned by
        `post_delete_feature` will be passed to
        `post_delete_feature_with_metadata`.
        """
        return response, metadata

    def pre_delete_membership(
        self,
        request: service.DeleteMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.DeleteMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_delete_membership(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_membership

        DEPRECATED. Please use the `post_delete_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_delete_membership` interceptor runs
        before the `post_delete_membership_with_metadata` interceptor.
        """
        return response

    def post_delete_membership_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_delete_membership_with_metadata`
        interceptor in new development instead of the `post_delete_membership` interceptor.
        When both interceptors are used, this `post_delete_membership_with_metadata` interceptor runs after the
        `post_delete_membership` interceptor. The (possibly modified) response returned by
        `post_delete_membership` will be passed to
        `post_delete_membership_with_metadata`.
        """
        return response, metadata

    def pre_generate_connect_manifest(
        self,
        request: service.GenerateConnectManifestRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.GenerateConnectManifestRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for generate_connect_manifest

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_generate_connect_manifest(
        self, response: service.GenerateConnectManifestResponse
    ) -> service.GenerateConnectManifestResponse:
        """Post-rpc interceptor for generate_connect_manifest

        DEPRECATED. Please use the `post_generate_connect_manifest_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_generate_connect_manifest` interceptor runs
        before the `post_generate_connect_manifest_with_metadata` interceptor.
        """
        return response

    def post_generate_connect_manifest_with_metadata(
        self,
        response: service.GenerateConnectManifestResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.GenerateConnectManifestResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for generate_connect_manifest

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_generate_connect_manifest_with_metadata`
        interceptor in new development instead of the `post_generate_connect_manifest` interceptor.
        When both interceptors are used, this `post_generate_connect_manifest_with_metadata` interceptor runs after the
        `post_generate_connect_manifest` interceptor. The (possibly modified) response returned by
        `post_generate_connect_manifest` will be passed to
        `post_generate_connect_manifest_with_metadata`.
        """
        return response, metadata

    def pre_get_feature(
        self,
        request: service.GetFeatureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetFeatureRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_feature

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_get_feature(self, response: feature.Feature) -> feature.Feature:
        """Post-rpc interceptor for get_feature

        DEPRECATED. Please use the `post_get_feature_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_get_feature` interceptor runs
        before the `post_get_feature_with_metadata` interceptor.
        """
        return response

    def post_get_feature_with_metadata(
        self,
        response: feature.Feature,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[feature.Feature, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_feature

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_get_feature_with_metadata`
        interceptor in new development instead of the `post_get_feature` interceptor.
        When both interceptors are used, this `post_get_feature_with_metadata` interceptor runs after the
        `post_get_feature` interceptor. The (possibly modified) response returned by
        `post_get_feature` will be passed to
        `post_get_feature_with_metadata`.
        """
        return response, metadata

    def pre_get_membership(
        self,
        request: service.GetMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_get_membership(
        self, response: membership.Membership
    ) -> membership.Membership:
        """Post-rpc interceptor for get_membership

        DEPRECATED. Please use the `post_get_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_get_membership` interceptor runs
        before the `post_get_membership_with_metadata` interceptor.
        """
        return response

    def post_get_membership_with_metadata(
        self,
        response: membership.Membership,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[membership.Membership, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_get_membership_with_metadata`
        interceptor in new development instead of the `post_get_membership` interceptor.
        When both interceptors are used, this `post_get_membership_with_metadata` interceptor runs after the
        `post_get_membership` interceptor. The (possibly modified) response returned by
        `post_get_membership` will be passed to
        `post_get_membership_with_metadata`.
        """
        return response, metadata

    def pre_list_features(
        self,
        request: service.ListFeaturesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListFeaturesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_features

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_list_features(
        self, response: service.ListFeaturesResponse
    ) -> service.ListFeaturesResponse:
        """Post-rpc interceptor for list_features

        DEPRECATED. Please use the `post_list_features_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_list_features` interceptor runs
        before the `post_list_features_with_metadata` interceptor.
        """
        return response

    def post_list_features_with_metadata(
        self,
        response: service.ListFeaturesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListFeaturesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_features

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_list_features_with_metadata`
        interceptor in new development instead of the `post_list_features` interceptor.
        When both interceptors are used, this `post_list_features_with_metadata` interceptor runs after the
        `post_list_features` interceptor. The (possibly modified) response returned by
        `post_list_features` will be passed to
        `post_list_features_with_metadata`.
        """
        return response, metadata

    def pre_list_memberships(
        self,
        request: service.ListMembershipsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListMembershipsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_memberships

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_list_memberships(
        self, response: service.ListMembershipsResponse
    ) -> service.ListMembershipsResponse:
        """Post-rpc interceptor for list_memberships

        DEPRECATED. Please use the `post_list_memberships_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_list_memberships` interceptor runs
        before the `post_list_memberships_with_metadata` interceptor.
        """
        return response

    def post_list_memberships_with_metadata(
        self,
        response: service.ListMembershipsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListMembershipsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_memberships

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_list_memberships_with_metadata`
        interceptor in new development instead of the `post_list_memberships` interceptor.
        When both interceptors are used, this `post_list_memberships_with_metadata` interceptor runs after the
        `post_list_memberships` interceptor. The (possibly modified) response returned by
        `post_list_memberships` will be passed to
        `post_list_memberships_with_metadata`.
        """
        return response, metadata

    def pre_update_feature(
        self,
        request: service.UpdateFeatureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateFeatureRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_feature

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_update_feature(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_feature

        DEPRECATED. Please use the `post_update_feature_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_update_feature` interceptor runs
        before the `post_update_feature_with_metadata` interceptor.
        """
        return response

    def post_update_feature_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_feature

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_update_feature_with_metadata`
        interceptor in new development instead of the `post_update_feature` interceptor.
        When both interceptors are used, this `post_update_feature_with_metadata` interceptor runs after the
        `post_update_feature` interceptor. The (possibly modified) response returned by
        `post_update_feature` will be passed to
        `post_update_feature_with_metadata`.
        """
        return response, metadata

    def pre_update_membership(
        self,
        request: service.UpdateMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.UpdateMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GkeHub server.
        """
        return request, metadata

    def post_update_membership(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_membership

        DEPRECATED. Please use the `post_update_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GkeHub server but before
        it is returned to user code. This `post_update_membership` interceptor runs
        before the `post_update_membership_with_metadata` interceptor.
        """
        return response

    def post_update_membership_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GkeHub server but before it is returned to user code.

        We recommend only using this `post_update_membership_with_metadata`
        interceptor in new development instead of the `post_update_membership` interceptor.
        When both interceptors are used, this `post_update_membership_with_metadata` interceptor runs after the
        `post_update_membership` interceptor. The (possibly modified) response returned by
        `post_update_membership` will be passed to
        `post_update_membership_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class GkeHubRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: GkeHubRestInterceptor


class GkeHubRestTransport(_BaseGkeHubRestTransport):
    """REST backend synchronous transport for GkeHub.

    The GKE Hub service handles the registration of many Kubernetes
    clusters to Google Cloud, and the management of multi-cluster
    features over those clusters.

    The GKE Hub service operates on the following resources:

    -  [Membership][google.cloud.gkehub.v1.Membership]
    -  [Feature][google.cloud.gkehub.v1.Feature]

    GKE Hub is currently available in the global region and all regions
    in https://cloud.google.com/compute/docs/regions-zones. Feature is
    only available in global region while membership is global region
    and all the regions.

    **Membership management may be non-trivial:** it is recommended to
    use one of the Google-provided client libraries or tools where
    possible when working with Membership resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "gkehub.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[GkeHubRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'gkehub.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or GkeHubRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateFeature(_BaseGkeHubRestTransport._BaseCreateFeature, GkeHubRestStub):
        def __hash__(self):
            return hash("GkeHubRestTransport.CreateFeature")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateFeatureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create feature method over HTTP.

            Args:
                request (~.service.CreateFeatureRequest):
                    The request object. Request message for the ``GkeHub.CreateFeature`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseCreateFeature._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_feature(request, metadata)
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseCreateFeature._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseGkeHubRestTransport._BaseCreateFeature._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseCreateFeature._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.CreateFeature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "CreateFeature",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._CreateFeature._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_feature(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_feature_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.create_feature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "CreateFeature",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateMembership(
        _BaseGkeHubRestTransport._BaseCreateMembership, GkeHubRestStub
    ):
        def __hash__(self):
            return hash("GkeHubRestTransport.CreateMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create membership method over HTTP.

            Args:
                request (~.service.CreateMembershipRequest):
                    The request object. Request message for the ``GkeHub.CreateMembership``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseCreateMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_membership(
                request, metadata
            )
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseCreateMembership._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseGkeHubRestTransport._BaseCreateMembership._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseCreateMembership._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.CreateMembership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "CreateMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._CreateMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.create_membership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "CreateMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteFeature(_BaseGkeHubRestTransport._BaseDeleteFeature, GkeHubRestStub):
        def __hash__(self):
            return hash("GkeHubRestTransport.DeleteFeature")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteFeatureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete feature method over HTTP.

            Args:
                request (~.service.DeleteFeatureRequest):
                    The request object. Request message for ``GkeHub.DeleteFeature`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseDeleteFeature._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_feature(request, metadata)
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseDeleteFeature._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseDeleteFeature._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.DeleteFeature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "DeleteFeature",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._DeleteFeature._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_feature(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_feature_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.delete_feature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "DeleteFeature",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteMembership(
        _BaseGkeHubRestTransport._BaseDeleteMembership, GkeHubRestStub
    ):
        def __hash__(self):
            return hash("GkeHubRestTransport.DeleteMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete membership method over HTTP.

            Args:
                request (~.service.DeleteMembershipRequest):
                    The request object. Request message for ``GkeHub.DeleteMembership`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseDeleteMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_membership(
                request, metadata
            )
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseDeleteMembership._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseDeleteMembership._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.DeleteMembership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "DeleteMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._DeleteMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.delete_membership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "DeleteMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GenerateConnectManifest(
        _BaseGkeHubRestTransport._BaseGenerateConnectManifest, GkeHubRestStub
    ):
        def __hash__(self):
            return hash("GkeHubRestTransport.GenerateConnectManifest")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GenerateConnectManifestRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.GenerateConnectManifestResponse:
            r"""Call the generate connect manifest method over HTTP.

            Args:
                request (~.service.GenerateConnectManifestRequest):
                    The request object. Request message for ``GkeHub.GenerateConnectManifest``
                method. .
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.GenerateConnectManifestResponse:
                    GenerateConnectManifestResponse
                contains manifest information for
                installing/upgrading a Connect agent.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseGenerateConnectManifest._get_http_options()
            )

            request, metadata = self._interceptor.pre_generate_connect_manifest(
                request, metadata
            )
            transcoded_request = _BaseGkeHubRestTransport._BaseGenerateConnectManifest._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGkeHubRestTransport._BaseGenerateConnectManifest._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.GenerateConnectManifest",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "GenerateConnectManifest",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._GenerateConnectManifest._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.GenerateConnectManifestResponse()
            pb_resp = service.GenerateConnectManifestResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_generate_connect_manifest(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_generate_connect_manifest_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.GenerateConnectManifestResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.generate_connect_manifest",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "GenerateConnectManifest",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetFeature(_BaseGkeHubRestTransport._BaseGetFeature, GkeHubRestStub):
        def __hash__(self):
            return hash("GkeHubRestTransport.GetFeature")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetFeatureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> feature.Feature:
            r"""Call the get feature method over HTTP.

            Args:
                request (~.service.GetFeatureRequest):
                    The request object. Request message for ``GkeHub.GetFeature`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.feature.Feature:
                    Feature represents the settings and
                status of any Hub Feature.

            """

            http_options = _BaseGkeHubRestTransport._BaseGetFeature._get_http_options()

            request, metadata = self._interceptor.pre_get_feature(request, metadata)
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseGetFeature._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseGetFeature._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.GetFeature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "GetFeature",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._GetFeature._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = feature.Feature()
            pb_resp = feature.Feature.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_feature(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_feature_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = feature.Feature.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.get_feature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "GetFeature",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetMembership(_BaseGkeHubRestTransport._BaseGetMembership, GkeHubRestStub):
        def __hash__(self):
            return hash("GkeHubRestTransport.GetMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> membership.Membership:
            r"""Call the get membership method over HTTP.

            Args:
                request (~.service.GetMembershipRequest):
                    The request object. Request message for ``GkeHub.GetMembership`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.membership.Membership:
                    Membership contains information about
                a member cluster.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseGetMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_membership(request, metadata)
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseGetMembership._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseGetMembership._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.GetMembership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "GetMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._GetMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = membership.Membership()
            pb_resp = membership.Membership.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = membership.Membership.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.get_membership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "GetMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListFeatures(_BaseGkeHubRestTransport._BaseListFeatures, GkeHubRestStub):
        def __hash__(self):
            return hash("GkeHubRestTransport.ListFeatures")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListFeaturesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListFeaturesResponse:
            r"""Call the list features method over HTTP.

            Args:
                request (~.service.ListFeaturesRequest):
                    The request object. Request message for ``GkeHub.ListFeatures`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListFeaturesResponse:
                    Response message for the ``GkeHub.ListFeatures`` method.
            """

            http_options = (
                _BaseGkeHubRestTransport._BaseListFeatures._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_features(request, metadata)
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseListFeatures._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseListFeatures._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.ListFeatures",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "ListFeatures",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._ListFeatures._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListFeaturesResponse()
            pb_resp = service.ListFeaturesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_features(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_features_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListFeaturesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.list_features",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "ListFeatures",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListMemberships(
        _BaseGkeHubRestTransport._BaseListMemberships, GkeHubRestStub
    ):
        def __hash__(self):
            return hash("GkeHubRestTransport.ListMemberships")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListMembershipsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListMembershipsResponse:
            r"""Call the list memberships method over HTTP.

            Args:
                request (~.service.ListMembershipsRequest):
                    The request object. Request message for ``GkeHub.ListMemberships`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListMembershipsResponse:
                    Response message for the ``GkeHub.ListMemberships``
                method.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseListMemberships._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_memberships(
                request, metadata
            )
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseListMemberships._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseListMemberships._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.ListMemberships",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "ListMemberships",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._ListMemberships._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListMembershipsResponse()
            pb_resp = service.ListMembershipsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_memberships(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_memberships_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListMembershipsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.list_memberships",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "ListMemberships",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateFeature(_BaseGkeHubRestTransport._BaseUpdateFeature, GkeHubRestStub):
        def __hash__(self):
            return hash("GkeHubRestTransport.UpdateFeature")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateFeatureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update feature method over HTTP.

            Args:
                request (~.service.UpdateFeatureRequest):
                    The request object. Request message for ``GkeHub.UpdateFeature`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseUpdateFeature._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_feature(request, metadata)
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseUpdateFeature._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseGkeHubRestTransport._BaseUpdateFeature._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseUpdateFeature._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.UpdateFeature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "UpdateFeature",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._UpdateFeature._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_feature(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_feature_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.update_feature",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "UpdateFeature",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateMembership(
        _BaseGkeHubRestTransport._BaseUpdateMembership, GkeHubRestStub
    ):
        def __hash__(self):
            return hash("GkeHubRestTransport.UpdateMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update membership method over HTTP.

            Args:
                request (~.service.UpdateMembershipRequest):
                    The request object. Request message for ``GkeHub.UpdateMembership`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseGkeHubRestTransport._BaseUpdateMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_membership(
                request, metadata
            )
            transcoded_request = (
                _BaseGkeHubRestTransport._BaseUpdateMembership._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseGkeHubRestTransport._BaseUpdateMembership._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseGkeHubRestTransport._BaseUpdateMembership._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.gkehub_v1.GkeHubClient.UpdateMembership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "UpdateMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GkeHubRestTransport._UpdateMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gkehub_v1.GkeHubClient.update_membership",
                    extra={
                        "serviceName": "google.cloud.gkehub.v1.GkeHub",
                        "rpcName": "UpdateMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_feature(
        self,
    ) -> Callable[[service.CreateFeatureRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFeature(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_membership(
        self,
    ) -> Callable[[service.CreateMembershipRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_feature(
        self,
    ) -> Callable[[service.DeleteFeatureRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteFeature(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_membership(
        self,
    ) -> Callable[[service.DeleteMembershipRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_connect_manifest(
        self,
    ) -> Callable[
        [service.GenerateConnectManifestRequest],
        service.GenerateConnectManifestResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateConnectManifest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_feature(self) -> Callable[[service.GetFeatureRequest], feature.Feature]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFeature(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_membership(
        self,
    ) -> Callable[[service.GetMembershipRequest], membership.Membership]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_features(
        self,
    ) -> Callable[[service.ListFeaturesRequest], service.ListFeaturesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFeatures(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_memberships(
        self,
    ) -> Callable[[service.ListMembershipsRequest], service.ListMembershipsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMemberships(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_feature(
        self,
    ) -> Callable[[service.UpdateFeatureRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateFeature(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_membership(
        self,
    ) -> Callable[[service.UpdateMembershipRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("GkeHubRestTransport",)
