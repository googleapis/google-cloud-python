# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.managedkafka_v1.types import managed_kafka, resources

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseManagedKafkaRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ManagedKafkaRestInterceptor:
    """Interceptor for ManagedKafka.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ManagedKafkaRestTransport.

    .. code-block:: python
        class MyCustomManagedKafkaInterceptor(ManagedKafkaRestInterceptor):
            def pre_create_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_topic(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_topic(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_consumer_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_topic(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_consumer_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_consumer_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_topic(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_topic(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_consumer_groups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_consumer_groups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_topics(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_topics(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_consumer_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_consumer_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_topic(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_topic(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ManagedKafkaRestTransport(interceptor=MyCustomManagedKafkaInterceptor())
        client = ManagedKafkaClient(transport=transport)


    """

    def pre_create_cluster(
        self,
        request: managed_kafka.CreateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.CreateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_create_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_create_topic(
        self,
        request: managed_kafka.CreateTopicRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.CreateTopicRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_topic

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_create_topic(self, response: resources.Topic) -> resources.Topic:
        """Post-rpc interceptor for create_topic

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cluster(
        self,
        request: managed_kafka.DeleteClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.DeleteClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_delete_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_delete_consumer_group(
        self,
        request: managed_kafka.DeleteConsumerGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.DeleteConsumerGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_consumer_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def pre_delete_topic(
        self,
        request: managed_kafka.DeleteTopicRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.DeleteTopicRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_topic

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def pre_get_cluster(
        self,
        request: managed_kafka.GetClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.GetClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_get_cluster(self, response: resources.Cluster) -> resources.Cluster:
        """Post-rpc interceptor for get_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_get_consumer_group(
        self,
        request: managed_kafka.GetConsumerGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.GetConsumerGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_consumer_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_get_consumer_group(
        self, response: resources.ConsumerGroup
    ) -> resources.ConsumerGroup:
        """Post-rpc interceptor for get_consumer_group

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_get_topic(
        self,
        request: managed_kafka.GetTopicRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.GetTopicRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_topic

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_get_topic(self, response: resources.Topic) -> resources.Topic:
        """Post-rpc interceptor for get_topic

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_list_clusters(
        self,
        request: managed_kafka.ListClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.ListClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_list_clusters(
        self, response: managed_kafka.ListClustersResponse
    ) -> managed_kafka.ListClustersResponse:
        """Post-rpc interceptor for list_clusters

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_list_consumer_groups(
        self,
        request: managed_kafka.ListConsumerGroupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.ListConsumerGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_consumer_groups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_list_consumer_groups(
        self, response: managed_kafka.ListConsumerGroupsResponse
    ) -> managed_kafka.ListConsumerGroupsResponse:
        """Post-rpc interceptor for list_consumer_groups

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_list_topics(
        self,
        request: managed_kafka.ListTopicsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.ListTopicsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_topics

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_list_topics(
        self, response: managed_kafka.ListTopicsResponse
    ) -> managed_kafka.ListTopicsResponse:
        """Post-rpc interceptor for list_topics

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_update_cluster(
        self,
        request: managed_kafka.UpdateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.UpdateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_update_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_update_consumer_group(
        self,
        request: managed_kafka.UpdateConsumerGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.UpdateConsumerGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_consumer_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_update_consumer_group(
        self, response: resources.ConsumerGroup
    ) -> resources.ConsumerGroup:
        """Post-rpc interceptor for update_consumer_group

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_update_topic(
        self,
        request: managed_kafka.UpdateTopicRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[managed_kafka.UpdateTopicRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_topic

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_update_topic(self, response: resources.Topic) -> resources.Topic:
        """Post-rpc interceptor for update_topic

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ManagedKafka server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ManagedKafka server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ManagedKafkaRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ManagedKafkaRestInterceptor


class ManagedKafkaRestTransport(_BaseManagedKafkaRestTransport):
    """REST backend synchronous transport for ManagedKafka.

    The service that a client application uses to manage Apache
    Kafka clusters, topics and consumer groups.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "managedkafka.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ManagedKafkaRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'managedkafka.googleapis.com').
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
        self._interceptor = interceptor or ManagedKafkaRestInterceptor()
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

    class _CreateCluster(
        _BaseManagedKafkaRestTransport._BaseCreateCluster, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.CreateCluster")

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
            request: managed_kafka.CreateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cluster method over HTTP.

            Args:
                request (~.managed_kafka.CreateClusterRequest):
                    The request object. Request for CreateCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseCreateCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_cluster(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseCreateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseManagedKafkaRestTransport._BaseCreateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseCreateCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._CreateCluster._get_response(
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
            resp = self._interceptor.post_create_cluster(resp)
            return resp

    class _CreateTopic(
        _BaseManagedKafkaRestTransport._BaseCreateTopic, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.CreateTopic")

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
            request: managed_kafka.CreateTopicRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Topic:
            r"""Call the create topic method over HTTP.

            Args:
                request (~.managed_kafka.CreateTopicRequest):
                    The request object. Request for CreateTopic.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Topic:
                    A Kafka topic in a given cluster.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseCreateTopic._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_topic(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseCreateTopic._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseManagedKafkaRestTransport._BaseCreateTopic._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseCreateTopic._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._CreateTopic._get_response(
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
            resp = resources.Topic()
            pb_resp = resources.Topic.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_topic(resp)
            return resp

    class _DeleteCluster(
        _BaseManagedKafkaRestTransport._BaseDeleteCluster, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.DeleteCluster")

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
            request: managed_kafka.DeleteClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cluster method over HTTP.

            Args:
                request (~.managed_kafka.DeleteClusterRequest):
                    The request object. Request for DeleteCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseDeleteCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_cluster(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseDeleteCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseDeleteCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._DeleteCluster._get_response(
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
            resp = self._interceptor.post_delete_cluster(resp)
            return resp

    class _DeleteConsumerGroup(
        _BaseManagedKafkaRestTransport._BaseDeleteConsumerGroup, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.DeleteConsumerGroup")

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
            request: managed_kafka.DeleteConsumerGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete consumer group method over HTTP.

            Args:
                request (~.managed_kafka.DeleteConsumerGroupRequest):
                    The request object. Request for DeleteConsumerGroup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseDeleteConsumerGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_consumer_group(
                request, metadata
            )
            transcoded_request = _BaseManagedKafkaRestTransport._BaseDeleteConsumerGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseDeleteConsumerGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._DeleteConsumerGroup._get_response(
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

    class _DeleteTopic(
        _BaseManagedKafkaRestTransport._BaseDeleteTopic, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.DeleteTopic")

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
            request: managed_kafka.DeleteTopicRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete topic method over HTTP.

            Args:
                request (~.managed_kafka.DeleteTopicRequest):
                    The request object. Request for DeleteTopic.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseDeleteTopic._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_topic(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseDeleteTopic._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseDeleteTopic._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._DeleteTopic._get_response(
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

    class _GetCluster(
        _BaseManagedKafkaRestTransport._BaseGetCluster, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.GetCluster")

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
            request: managed_kafka.GetClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Cluster:
            r"""Call the get cluster method over HTTP.

            Args:
                request (~.managed_kafka.GetClusterRequest):
                    The request object. Request for GetCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Cluster:
                    An Apache Kafka cluster deployed in a
                location.

            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseGetCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_cluster(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseGetCluster._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseGetCluster._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._GetCluster._get_response(
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
            resp = resources.Cluster()
            pb_resp = resources.Cluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cluster(resp)
            return resp

    class _GetConsumerGroup(
        _BaseManagedKafkaRestTransport._BaseGetConsumerGroup, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.GetConsumerGroup")

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
            request: managed_kafka.GetConsumerGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ConsumerGroup:
            r"""Call the get consumer group method over HTTP.

            Args:
                request (~.managed_kafka.GetConsumerGroupRequest):
                    The request object. Request for GetConsumerGroup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ConsumerGroup:
                    A Kafka consumer group in a given
                cluster.

            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseGetConsumerGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_consumer_group(
                request, metadata
            )
            transcoded_request = _BaseManagedKafkaRestTransport._BaseGetConsumerGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseGetConsumerGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._GetConsumerGroup._get_response(
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
            resp = resources.ConsumerGroup()
            pb_resp = resources.ConsumerGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_consumer_group(resp)
            return resp

    class _GetTopic(_BaseManagedKafkaRestTransport._BaseGetTopic, ManagedKafkaRestStub):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.GetTopic")

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
            request: managed_kafka.GetTopicRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Topic:
            r"""Call the get topic method over HTTP.

            Args:
                request (~.managed_kafka.GetTopicRequest):
                    The request object. Request for GetTopic.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Topic:
                    A Kafka topic in a given cluster.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseGetTopic._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_topic(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseGetTopic._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseGetTopic._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._GetTopic._get_response(
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
            resp = resources.Topic()
            pb_resp = resources.Topic.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_topic(resp)
            return resp

    class _ListClusters(
        _BaseManagedKafkaRestTransport._BaseListClusters, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.ListClusters")

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
            request: managed_kafka.ListClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> managed_kafka.ListClustersResponse:
            r"""Call the list clusters method over HTTP.

            Args:
                request (~.managed_kafka.ListClustersRequest):
                    The request object. Request for ListClusters.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.managed_kafka.ListClustersResponse:
                    Response for ListClusters.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseListClusters._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_clusters(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseListClusters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseListClusters._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._ListClusters._get_response(
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
            resp = managed_kafka.ListClustersResponse()
            pb_resp = managed_kafka.ListClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clusters(resp)
            return resp

    class _ListConsumerGroups(
        _BaseManagedKafkaRestTransport._BaseListConsumerGroups, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.ListConsumerGroups")

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
            request: managed_kafka.ListConsumerGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> managed_kafka.ListConsumerGroupsResponse:
            r"""Call the list consumer groups method over HTTP.

            Args:
                request (~.managed_kafka.ListConsumerGroupsRequest):
                    The request object. Request for ListConsumerGroups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.managed_kafka.ListConsumerGroupsResponse:
                    Response for ListConsumerGroups.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseListConsumerGroups._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_consumer_groups(
                request, metadata
            )
            transcoded_request = _BaseManagedKafkaRestTransport._BaseListConsumerGroups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseListConsumerGroups._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._ListConsumerGroups._get_response(
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
            resp = managed_kafka.ListConsumerGroupsResponse()
            pb_resp = managed_kafka.ListConsumerGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_consumer_groups(resp)
            return resp

    class _ListTopics(
        _BaseManagedKafkaRestTransport._BaseListTopics, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.ListTopics")

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
            request: managed_kafka.ListTopicsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> managed_kafka.ListTopicsResponse:
            r"""Call the list topics method over HTTP.

            Args:
                request (~.managed_kafka.ListTopicsRequest):
                    The request object. Request for ListTopics.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.managed_kafka.ListTopicsResponse:
                    Response for ListTopics.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseListTopics._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_topics(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseListTopics._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseListTopics._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._ListTopics._get_response(
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
            resp = managed_kafka.ListTopicsResponse()
            pb_resp = managed_kafka.ListTopicsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_topics(resp)
            return resp

    class _UpdateCluster(
        _BaseManagedKafkaRestTransport._BaseUpdateCluster, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.UpdateCluster")

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
            request: managed_kafka.UpdateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update cluster method over HTTP.

            Args:
                request (~.managed_kafka.UpdateClusterRequest):
                    The request object. Request for UpdateCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseUpdateCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_cluster(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseUpdateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseManagedKafkaRestTransport._BaseUpdateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseUpdateCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._UpdateCluster._get_response(
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
            resp = self._interceptor.post_update_cluster(resp)
            return resp

    class _UpdateConsumerGroup(
        _BaseManagedKafkaRestTransport._BaseUpdateConsumerGroup, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.UpdateConsumerGroup")

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
            request: managed_kafka.UpdateConsumerGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ConsumerGroup:
            r"""Call the update consumer group method over HTTP.

            Args:
                request (~.managed_kafka.UpdateConsumerGroupRequest):
                    The request object. Request for UpdateConsumerGroup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ConsumerGroup:
                    A Kafka consumer group in a given
                cluster.

            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseUpdateConsumerGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_consumer_group(
                request, metadata
            )
            transcoded_request = _BaseManagedKafkaRestTransport._BaseUpdateConsumerGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseManagedKafkaRestTransport._BaseUpdateConsumerGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseUpdateConsumerGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._UpdateConsumerGroup._get_response(
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
            resp = resources.ConsumerGroup()
            pb_resp = resources.ConsumerGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_consumer_group(resp)
            return resp

    class _UpdateTopic(
        _BaseManagedKafkaRestTransport._BaseUpdateTopic, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.UpdateTopic")

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
            request: managed_kafka.UpdateTopicRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Topic:
            r"""Call the update topic method over HTTP.

            Args:
                request (~.managed_kafka.UpdateTopicRequest):
                    The request object. Request for UpdateTopic.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Topic:
                    A Kafka topic in a given cluster.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseUpdateTopic._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_topic(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseUpdateTopic._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseManagedKafkaRestTransport._BaseUpdateTopic._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseUpdateTopic._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._UpdateTopic._get_response(
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
            resp = resources.Topic()
            pb_resp = resources.Topic.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_topic(resp)
            return resp

    @property
    def create_cluster(
        self,
    ) -> Callable[[managed_kafka.CreateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_topic(
        self,
    ) -> Callable[[managed_kafka.CreateTopicRequest], resources.Topic]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTopic(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cluster(
        self,
    ) -> Callable[[managed_kafka.DeleteClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_consumer_group(
        self,
    ) -> Callable[[managed_kafka.DeleteConsumerGroupRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConsumerGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_topic(
        self,
    ) -> Callable[[managed_kafka.DeleteTopicRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTopic(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster(
        self,
    ) -> Callable[[managed_kafka.GetClusterRequest], resources.Cluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_consumer_group(
        self,
    ) -> Callable[[managed_kafka.GetConsumerGroupRequest], resources.ConsumerGroup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConsumerGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_topic(self) -> Callable[[managed_kafka.GetTopicRequest], resources.Topic]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTopic(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [managed_kafka.ListClustersRequest], managed_kafka.ListClustersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_consumer_groups(
        self,
    ) -> Callable[
        [managed_kafka.ListConsumerGroupsRequest],
        managed_kafka.ListConsumerGroupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConsumerGroups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_topics(
        self,
    ) -> Callable[[managed_kafka.ListTopicsRequest], managed_kafka.ListTopicsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTopics(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cluster(
        self,
    ) -> Callable[[managed_kafka.UpdateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_consumer_group(
        self,
    ) -> Callable[[managed_kafka.UpdateConsumerGroupRequest], resources.ConsumerGroup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConsumerGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_topic(
        self,
    ) -> Callable[[managed_kafka.UpdateTopicRequest], resources.Topic]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTopic(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseManagedKafkaRestTransport._BaseGetLocation, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseManagedKafkaRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._GetLocation._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseManagedKafkaRestTransport._BaseListLocations, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.ListLocations")

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
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._ListLocations._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseManagedKafkaRestTransport._BaseCancelOperation, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseManagedKafkaRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseManagedKafkaRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseManagedKafkaRestTransport._BaseDeleteOperation, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.DeleteOperation")

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
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseManagedKafkaRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseManagedKafkaRestTransport._BaseGetOperation, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.GetOperation")

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
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseManagedKafkaRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ManagedKafkaRestTransport._GetOperation._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseManagedKafkaRestTransport._BaseListOperations, ManagedKafkaRestStub
    ):
        def __hash__(self):
            return hash("ManagedKafkaRestTransport.ListOperations")

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
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseManagedKafkaRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseManagedKafkaRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseManagedKafkaRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ManagedKafkaRestTransport._ListOperations._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ManagedKafkaRestTransport",)
