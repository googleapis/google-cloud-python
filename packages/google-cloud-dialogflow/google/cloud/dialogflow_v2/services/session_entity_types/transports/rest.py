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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflow_v2.types import (
    session_entity_type as gcd_session_entity_type,
)
from google.cloud.dialogflow_v2.types import session_entity_type

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSessionEntityTypesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SessionEntityTypesRestInterceptor:
    """Interceptor for SessionEntityTypes.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SessionEntityTypesRestTransport.

    .. code-block:: python
        class MyCustomSessionEntityTypesInterceptor(SessionEntityTypesRestInterceptor):
            def pre_create_session_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_session_entity_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_session_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_session_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_session_entity_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_session_entity_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_session_entity_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_session_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_session_entity_type(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SessionEntityTypesRestTransport(interceptor=MyCustomSessionEntityTypesInterceptor())
        client = SessionEntityTypesClient(transport=transport)


    """

    def pre_create_session_entity_type(
        self,
        request: gcd_session_entity_type.CreateSessionEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_session_entity_type.CreateSessionEntityTypeRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_session_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_create_session_entity_type(
        self, response: gcd_session_entity_type.SessionEntityType
    ) -> gcd_session_entity_type.SessionEntityType:
        """Post-rpc interceptor for create_session_entity_type

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_delete_session_entity_type(
        self,
        request: session_entity_type.DeleteSessionEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        session_entity_type.DeleteSessionEntityTypeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_session_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def pre_get_session_entity_type(
        self,
        request: session_entity_type.GetSessionEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        session_entity_type.GetSessionEntityTypeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_session_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_get_session_entity_type(
        self, response: session_entity_type.SessionEntityType
    ) -> session_entity_type.SessionEntityType:
        """Post-rpc interceptor for get_session_entity_type

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_list_session_entity_types(
        self,
        request: session_entity_type.ListSessionEntityTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        session_entity_type.ListSessionEntityTypesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_session_entity_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_list_session_entity_types(
        self, response: session_entity_type.ListSessionEntityTypesResponse
    ) -> session_entity_type.ListSessionEntityTypesResponse:
        """Post-rpc interceptor for list_session_entity_types

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_update_session_entity_type(
        self,
        request: gcd_session_entity_type.UpdateSessionEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_session_entity_type.UpdateSessionEntityTypeRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_session_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_update_session_entity_type(
        self, response: gcd_session_entity_type.SessionEntityType
    ) -> gcd_session_entity_type.SessionEntityType:
        """Post-rpc interceptor for update_session_entity_type

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
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
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
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
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
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
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
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
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
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
        before they are sent to the SessionEntityTypes server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the SessionEntityTypes server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SessionEntityTypesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SessionEntityTypesRestInterceptor


class SessionEntityTypesRestTransport(_BaseSessionEntityTypesRestTransport):
    """REST backend synchronous transport for SessionEntityTypes.

    Service for managing
    [SessionEntityTypes][google.cloud.dialogflow.v2.SessionEntityType].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SessionEntityTypesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or SessionEntityTypesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateSessionEntityType(
        _BaseSessionEntityTypesRestTransport._BaseCreateSessionEntityType,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.CreateSessionEntityType")

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
            request: gcd_session_entity_type.CreateSessionEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_session_entity_type.SessionEntityType:
            r"""Call the create session entity
            type method over HTTP.

                Args:
                    request (~.gcd_session_entity_type.CreateSessionEntityTypeRequest):
                        The request object. The request message for
                    [SessionEntityTypes.CreateSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.CreateSessionEntityType].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcd_session_entity_type.SessionEntityType:
                        A session represents a conversation between a Dialogflow
                    agent and an end-user. You can create special entities,
                    called session entities, during a session. Session
                    entities can extend or replace custom entity types and
                    only exist during the session that they were created
                    for. All session data, including session entities, is
                    stored by Dialogflow for 20 minutes.

                    For more information, see the `session entity
                    guide <https://cloud.google.com/dialogflow/docs/entities-session>`__.

            """

            http_options = (
                _BaseSessionEntityTypesRestTransport._BaseCreateSessionEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_session_entity_type(
                request, metadata
            )
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseCreateSessionEntityType._get_transcoded_request(
                http_options, request
            )

            body = _BaseSessionEntityTypesRestTransport._BaseCreateSessionEntityType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseCreateSessionEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SessionEntityTypesRestTransport._CreateSessionEntityType._get_response(
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
            resp = gcd_session_entity_type.SessionEntityType()
            pb_resp = gcd_session_entity_type.SessionEntityType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_session_entity_type(resp)
            return resp

    class _DeleteSessionEntityType(
        _BaseSessionEntityTypesRestTransport._BaseDeleteSessionEntityType,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.DeleteSessionEntityType")

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
            request: session_entity_type.DeleteSessionEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete session entity
            type method over HTTP.

                Args:
                    request (~.session_entity_type.DeleteSessionEntityTypeRequest):
                        The request object. The request message for
                    [SessionEntityTypes.DeleteSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.DeleteSessionEntityType].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options = (
                _BaseSessionEntityTypesRestTransport._BaseDeleteSessionEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_session_entity_type(
                request, metadata
            )
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseDeleteSessionEntityType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseDeleteSessionEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SessionEntityTypesRestTransport._DeleteSessionEntityType._get_response(
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

    class _GetSessionEntityType(
        _BaseSessionEntityTypesRestTransport._BaseGetSessionEntityType,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.GetSessionEntityType")

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
            request: session_entity_type.GetSessionEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> session_entity_type.SessionEntityType:
            r"""Call the get session entity type method over HTTP.

            Args:
                request (~.session_entity_type.GetSessionEntityTypeRequest):
                    The request object. The request message for
                [SessionEntityTypes.GetSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.GetSessionEntityType].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.session_entity_type.SessionEntityType:
                    A session represents a conversation between a Dialogflow
                agent and an end-user. You can create special entities,
                called session entities, during a session. Session
                entities can extend or replace custom entity types and
                only exist during the session that they were created
                for. All session data, including session entities, is
                stored by Dialogflow for 20 minutes.

                For more information, see the `session entity
                guide <https://cloud.google.com/dialogflow/docs/entities-session>`__.

            """

            http_options = (
                _BaseSessionEntityTypesRestTransport._BaseGetSessionEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_session_entity_type(
                request, metadata
            )
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseGetSessionEntityType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseGetSessionEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SessionEntityTypesRestTransport._GetSessionEntityType._get_response(
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
            resp = session_entity_type.SessionEntityType()
            pb_resp = session_entity_type.SessionEntityType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_session_entity_type(resp)
            return resp

    class _ListSessionEntityTypes(
        _BaseSessionEntityTypesRestTransport._BaseListSessionEntityTypes,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.ListSessionEntityTypes")

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
            request: session_entity_type.ListSessionEntityTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> session_entity_type.ListSessionEntityTypesResponse:
            r"""Call the list session entity types method over HTTP.

            Args:
                request (~.session_entity_type.ListSessionEntityTypesRequest):
                    The request object. The request message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.v2.SessionEntityTypes.ListSessionEntityTypes].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.session_entity_type.ListSessionEntityTypesResponse:
                    The response message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.v2.SessionEntityTypes.ListSessionEntityTypes].

            """

            http_options = (
                _BaseSessionEntityTypesRestTransport._BaseListSessionEntityTypes._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_session_entity_types(
                request, metadata
            )
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseListSessionEntityTypes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseListSessionEntityTypes._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SessionEntityTypesRestTransport._ListSessionEntityTypes._get_response(
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
            resp = session_entity_type.ListSessionEntityTypesResponse()
            pb_resp = session_entity_type.ListSessionEntityTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_session_entity_types(resp)
            return resp

    class _UpdateSessionEntityType(
        _BaseSessionEntityTypesRestTransport._BaseUpdateSessionEntityType,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.UpdateSessionEntityType")

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
            request: gcd_session_entity_type.UpdateSessionEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_session_entity_type.SessionEntityType:
            r"""Call the update session entity
            type method over HTTP.

                Args:
                    request (~.gcd_session_entity_type.UpdateSessionEntityTypeRequest):
                        The request object. The request message for
                    [SessionEntityTypes.UpdateSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.UpdateSessionEntityType].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcd_session_entity_type.SessionEntityType:
                        A session represents a conversation between a Dialogflow
                    agent and an end-user. You can create special entities,
                    called session entities, during a session. Session
                    entities can extend or replace custom entity types and
                    only exist during the session that they were created
                    for. All session data, including session entities, is
                    stored by Dialogflow for 20 minutes.

                    For more information, see the `session entity
                    guide <https://cloud.google.com/dialogflow/docs/entities-session>`__.

            """

            http_options = (
                _BaseSessionEntityTypesRestTransport._BaseUpdateSessionEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_session_entity_type(
                request, metadata
            )
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseUpdateSessionEntityType._get_transcoded_request(
                http_options, request
            )

            body = _BaseSessionEntityTypesRestTransport._BaseUpdateSessionEntityType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseUpdateSessionEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SessionEntityTypesRestTransport._UpdateSessionEntityType._get_response(
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
            resp = gcd_session_entity_type.SessionEntityType()
            pb_resp = gcd_session_entity_type.SessionEntityType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_session_entity_type(resp)
            return resp

    @property
    def create_session_entity_type(
        self,
    ) -> Callable[
        [gcd_session_entity_type.CreateSessionEntityTypeRequest],
        gcd_session_entity_type.SessionEntityType,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSessionEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_session_entity_type(
        self,
    ) -> Callable[
        [session_entity_type.DeleteSessionEntityTypeRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSessionEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_session_entity_type(
        self,
    ) -> Callable[
        [session_entity_type.GetSessionEntityTypeRequest],
        session_entity_type.SessionEntityType,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSessionEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_session_entity_types(
        self,
    ) -> Callable[
        [session_entity_type.ListSessionEntityTypesRequest],
        session_entity_type.ListSessionEntityTypesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSessionEntityTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_session_entity_type(
        self,
    ) -> Callable[
        [gcd_session_entity_type.UpdateSessionEntityTypeRequest],
        gcd_session_entity_type.SessionEntityType,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSessionEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseSessionEntityTypesRestTransport._BaseGetLocation,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.GetLocation")

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
                _BaseSessionEntityTypesRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SessionEntityTypesRestTransport._GetLocation._get_response(
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
        _BaseSessionEntityTypesRestTransport._BaseListLocations,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.ListLocations")

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
                _BaseSessionEntityTypesRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SessionEntityTypesRestTransport._ListLocations._get_response(
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
        _BaseSessionEntityTypesRestTransport._BaseCancelOperation,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.CancelOperation")

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
                _BaseSessionEntityTypesRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SessionEntityTypesRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseSessionEntityTypesRestTransport._BaseGetOperation,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.GetOperation")

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
                _BaseSessionEntityTypesRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SessionEntityTypesRestTransport._GetOperation._get_response(
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
        _BaseSessionEntityTypesRestTransport._BaseListOperations,
        SessionEntityTypesRestStub,
    ):
        def __hash__(self):
            return hash("SessionEntityTypesRestTransport.ListOperations")

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
                _BaseSessionEntityTypesRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseSessionEntityTypesRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSessionEntityTypesRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SessionEntityTypesRestTransport._ListOperations._get_response(
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


__all__ = ("SessionEntityTypesRestTransport",)
