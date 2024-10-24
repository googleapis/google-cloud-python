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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.rapidmigrationassessment_v1.types import (
    api_entities,
    rapidmigrationassessment,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRapidMigrationAssessmentRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RapidMigrationAssessmentRestInterceptor:
    """Interceptor for RapidMigrationAssessment.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RapidMigrationAssessmentRestTransport.

    .. code-block:: python
        class MyCustomRapidMigrationAssessmentInterceptor(RapidMigrationAssessmentRestInterceptor):
            def pre_create_annotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_annotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_annotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_annotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_collectors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_collectors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_pause_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_pause_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_register_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_register_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resume_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resume_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_collector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_collector(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RapidMigrationAssessmentRestTransport(interceptor=MyCustomRapidMigrationAssessmentInterceptor())
        client = RapidMigrationAssessmentClient(transport=transport)


    """

    def pre_create_annotation(
        self,
        request: rapidmigrationassessment.CreateAnnotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.CreateAnnotationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_annotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_create_annotation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_annotation

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_create_collector(
        self,
        request: rapidmigrationassessment.CreateCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.CreateCollectorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_create_collector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_delete_collector(
        self,
        request: rapidmigrationassessment.DeleteCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.DeleteCollectorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_delete_collector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_get_annotation(
        self,
        request: rapidmigrationassessment.GetAnnotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.GetAnnotationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_annotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_get_annotation(
        self, response: api_entities.Annotation
    ) -> api_entities.Annotation:
        """Post-rpc interceptor for get_annotation

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_get_collector(
        self,
        request: rapidmigrationassessment.GetCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[rapidmigrationassessment.GetCollectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_get_collector(
        self, response: api_entities.Collector
    ) -> api_entities.Collector:
        """Post-rpc interceptor for get_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_list_collectors(
        self,
        request: rapidmigrationassessment.ListCollectorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.ListCollectorsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_collectors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_list_collectors(
        self, response: rapidmigrationassessment.ListCollectorsResponse
    ) -> rapidmigrationassessment.ListCollectorsResponse:
        """Post-rpc interceptor for list_collectors

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_pause_collector(
        self,
        request: rapidmigrationassessment.PauseCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.PauseCollectorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for pause_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_pause_collector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for pause_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_register_collector(
        self,
        request: rapidmigrationassessment.RegisterCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.RegisterCollectorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for register_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_register_collector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for register_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_resume_collector(
        self,
        request: rapidmigrationassessment.ResumeCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.ResumeCollectorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for resume_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_resume_collector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for resume_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response

    def pre_update_collector(
        self,
        request: rapidmigrationassessment.UpdateCollectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        rapidmigrationassessment.UpdateCollectorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_collector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_update_collector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_collector

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
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
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
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
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
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
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
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
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
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
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
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
        before they are sent to the RapidMigrationAssessment server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the RapidMigrationAssessment server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RapidMigrationAssessmentRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RapidMigrationAssessmentRestInterceptor


class RapidMigrationAssessmentRestTransport(_BaseRapidMigrationAssessmentRestTransport):
    """REST backend synchronous transport for RapidMigrationAssessment.

    Service describing handlers for resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "rapidmigrationassessment.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RapidMigrationAssessmentRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'rapidmigrationassessment.googleapis.com').
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
        self._interceptor = interceptor or RapidMigrationAssessmentRestInterceptor()
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

    class _CreateAnnotation(
        _BaseRapidMigrationAssessmentRestTransport._BaseCreateAnnotation,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.CreateAnnotation")

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
            request: rapidmigrationassessment.CreateAnnotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create annotation method over HTTP.

            Args:
                request (~.rapidmigrationassessment.CreateAnnotationRequest):
                    The request object. Message for creating an AnnotationS.
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
                _BaseRapidMigrationAssessmentRestTransport._BaseCreateAnnotation._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_annotation(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseCreateAnnotation._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BaseCreateAnnotation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseCreateAnnotation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._CreateAnnotation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_annotation(resp)
            return resp

    class _CreateCollector(
        _BaseRapidMigrationAssessmentRestTransport._BaseCreateCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.CreateCollector")

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
            request: rapidmigrationassessment.CreateCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.CreateCollectorRequest):
                    The request object. Message for creating a Collector.
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
                _BaseRapidMigrationAssessmentRestTransport._BaseCreateCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_collector(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseCreateCollector._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BaseCreateCollector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseCreateCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._CreateCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_collector(resp)
            return resp

    class _DeleteCollector(
        _BaseRapidMigrationAssessmentRestTransport._BaseDeleteCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.DeleteCollector")

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
            request: rapidmigrationassessment.DeleteCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.DeleteCollectorRequest):
                    The request object. Message for deleting a Collector.
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
                _BaseRapidMigrationAssessmentRestTransport._BaseDeleteCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_collector(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseDeleteCollector._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseDeleteCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._DeleteCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_collector(resp)
            return resp

    class _GetAnnotation(
        _BaseRapidMigrationAssessmentRestTransport._BaseGetAnnotation,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.GetAnnotation")

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
            request: rapidmigrationassessment.GetAnnotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> api_entities.Annotation:
            r"""Call the get annotation method over HTTP.

            Args:
                request (~.rapidmigrationassessment.GetAnnotationRequest):
                    The request object. Message for getting a specific
                Annotation
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.api_entities.Annotation:
                    Message describing an Annotation
            """

            http_options = (
                _BaseRapidMigrationAssessmentRestTransport._BaseGetAnnotation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_annotation(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseGetAnnotation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseGetAnnotation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._GetAnnotation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = api_entities.Annotation()
            pb_resp = api_entities.Annotation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_annotation(resp)
            return resp

    class _GetCollector(
        _BaseRapidMigrationAssessmentRestTransport._BaseGetCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.GetCollector")

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
            request: rapidmigrationassessment.GetCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> api_entities.Collector:
            r"""Call the get collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.GetCollectorRequest):
                    The request object. Message for getting a specific
                Collector.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.api_entities.Collector:
                    Message describing Collector object.
            """

            http_options = (
                _BaseRapidMigrationAssessmentRestTransport._BaseGetCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_collector(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseGetCollector._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseGetCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._GetCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = api_entities.Collector()
            pb_resp = api_entities.Collector.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_collector(resp)
            return resp

    class _ListCollectors(
        _BaseRapidMigrationAssessmentRestTransport._BaseListCollectors,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.ListCollectors")

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
            request: rapidmigrationassessment.ListCollectorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rapidmigrationassessment.ListCollectorsResponse:
            r"""Call the list collectors method over HTTP.

            Args:
                request (~.rapidmigrationassessment.ListCollectorsRequest):
                    The request object. Message for requesting list of
                Collectors.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.rapidmigrationassessment.ListCollectorsResponse:
                    Message for response to listing
                Collectors.

            """

            http_options = (
                _BaseRapidMigrationAssessmentRestTransport._BaseListCollectors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_collectors(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseListCollectors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseListCollectors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._ListCollectors._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = rapidmigrationassessment.ListCollectorsResponse()
            pb_resp = rapidmigrationassessment.ListCollectorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_collectors(resp)
            return resp

    class _PauseCollector(
        _BaseRapidMigrationAssessmentRestTransport._BasePauseCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.PauseCollector")

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
            request: rapidmigrationassessment.PauseCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the pause collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.PauseCollectorRequest):
                    The request object. Message for pausing a Collector.
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
                _BaseRapidMigrationAssessmentRestTransport._BasePauseCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_pause_collector(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BasePauseCollector._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BasePauseCollector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BasePauseCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._PauseCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_pause_collector(resp)
            return resp

    class _RegisterCollector(
        _BaseRapidMigrationAssessmentRestTransport._BaseRegisterCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.RegisterCollector")

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
            request: rapidmigrationassessment.RegisterCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the register collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.RegisterCollectorRequest):
                    The request object. Message for registering a Collector.
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
                _BaseRapidMigrationAssessmentRestTransport._BaseRegisterCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_register_collector(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseRegisterCollector._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BaseRegisterCollector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseRegisterCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._RegisterCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_register_collector(resp)
            return resp

    class _ResumeCollector(
        _BaseRapidMigrationAssessmentRestTransport._BaseResumeCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.ResumeCollector")

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
            request: rapidmigrationassessment.ResumeCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the resume collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.ResumeCollectorRequest):
                    The request object. Message for resuming a Collector.
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
                _BaseRapidMigrationAssessmentRestTransport._BaseResumeCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_resume_collector(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseResumeCollector._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BaseResumeCollector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseResumeCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._ResumeCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resume_collector(resp)
            return resp

    class _UpdateCollector(
        _BaseRapidMigrationAssessmentRestTransport._BaseUpdateCollector,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.UpdateCollector")

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
            request: rapidmigrationassessment.UpdateCollectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update collector method over HTTP.

            Args:
                request (~.rapidmigrationassessment.UpdateCollectorRequest):
                    The request object. Message for updating a Collector.
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
                _BaseRapidMigrationAssessmentRestTransport._BaseUpdateCollector._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_collector(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseUpdateCollector._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BaseUpdateCollector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseUpdateCollector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._UpdateCollector._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_collector(resp)
            return resp

    @property
    def create_annotation(
        self,
    ) -> Callable[
        [rapidmigrationassessment.CreateAnnotationRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAnnotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.CreateCollectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.DeleteCollectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_annotation(
        self,
    ) -> Callable[
        [rapidmigrationassessment.GetAnnotationRequest], api_entities.Annotation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAnnotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.GetCollectorRequest], api_entities.Collector
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_collectors(
        self,
    ) -> Callable[
        [rapidmigrationassessment.ListCollectorsRequest],
        rapidmigrationassessment.ListCollectorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCollectors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def pause_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.PauseCollectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PauseCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def register_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.RegisterCollectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RegisterCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resume_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.ResumeCollectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResumeCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_collector(
        self,
    ) -> Callable[
        [rapidmigrationassessment.UpdateCollectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCollector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseRapidMigrationAssessmentRestTransport._BaseGetLocation,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.GetLocation")

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
                _BaseRapidMigrationAssessmentRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RapidMigrationAssessmentRestTransport._GetLocation._get_response(
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
        _BaseRapidMigrationAssessmentRestTransport._BaseListLocations,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.ListLocations")

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
                _BaseRapidMigrationAssessmentRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._ListLocations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
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
        _BaseRapidMigrationAssessmentRestTransport._BaseCancelOperation,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.CancelOperation")

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
                _BaseRapidMigrationAssessmentRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseRapidMigrationAssessmentRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._CancelOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
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
        _BaseRapidMigrationAssessmentRestTransport._BaseDeleteOperation,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.DeleteOperation")

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
                _BaseRapidMigrationAssessmentRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._DeleteOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
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
        _BaseRapidMigrationAssessmentRestTransport._BaseGetOperation,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.GetOperation")

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
                _BaseRapidMigrationAssessmentRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._GetOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
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
        _BaseRapidMigrationAssessmentRestTransport._BaseListOperations,
        RapidMigrationAssessmentRestStub,
    ):
        def __hash__(self):
            return hash("RapidMigrationAssessmentRestTransport.ListOperations")

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
                _BaseRapidMigrationAssessmentRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseRapidMigrationAssessmentRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRapidMigrationAssessmentRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RapidMigrationAssessmentRestTransport._ListOperations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
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


__all__ = ("RapidMigrationAssessmentRestTransport",)
