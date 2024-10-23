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

from google.cloud.dialogflow_v2beta1.types import intent
from google.cloud.dialogflow_v2beta1.types import intent as gcd_intent

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseIntentsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class IntentsRestInterceptor:
    """Interceptor for Intents.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the IntentsRestTransport.

    .. code-block:: python
        class MyCustomIntentsInterceptor(IntentsRestInterceptor):
            def pre_batch_delete_intents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_delete_intents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_update_intents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_intents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_intent(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_intent(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_intent(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_intent(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_intent(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_intents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_intents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_intent(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_intent(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = IntentsRestTransport(interceptor=MyCustomIntentsInterceptor())
        client = IntentsClient(transport=transport)


    """

    def pre_batch_delete_intents(
        self,
        request: intent.BatchDeleteIntentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[intent.BatchDeleteIntentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_delete_intents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_batch_delete_intents(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_delete_intents

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
        it is returned to user code.
        """
        return response

    def pre_batch_update_intents(
        self,
        request: intent.BatchUpdateIntentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[intent.BatchUpdateIntentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_intents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_batch_update_intents(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_update_intents

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
        it is returned to user code.
        """
        return response

    def pre_create_intent(
        self,
        request: gcd_intent.CreateIntentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_intent.CreateIntentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_intent

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_create_intent(self, response: gcd_intent.Intent) -> gcd_intent.Intent:
        """Post-rpc interceptor for create_intent

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
        it is returned to user code.
        """
        return response

    def pre_delete_intent(
        self, request: intent.DeleteIntentRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[intent.DeleteIntentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_intent

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def pre_get_intent(
        self, request: intent.GetIntentRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[intent.GetIntentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_intent

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_get_intent(self, response: intent.Intent) -> intent.Intent:
        """Post-rpc interceptor for get_intent

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
        it is returned to user code.
        """
        return response

    def pre_list_intents(
        self, request: intent.ListIntentsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[intent.ListIntentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_intents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_list_intents(
        self, response: intent.ListIntentsResponse
    ) -> intent.ListIntentsResponse:
        """Post-rpc interceptor for list_intents

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
        it is returned to user code.
        """
        return response

    def pre_update_intent(
        self,
        request: gcd_intent.UpdateIntentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_intent.UpdateIntentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_intent

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_update_intent(self, response: gcd_intent.Intent) -> gcd_intent.Intent:
        """Post-rpc interceptor for update_intent

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
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
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
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
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
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
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
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
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
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
        before they are sent to the Intents server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Intents server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class IntentsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: IntentsRestInterceptor


class IntentsRestTransport(_BaseIntentsRestTransport):
    """REST backend synchronous transport for Intents.

    Service for managing
    [Intents][google.cloud.dialogflow.v2beta1.Intent].

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
        interceptor: Optional[IntentsRestInterceptor] = None,
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or IntentsRestInterceptor()
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
                        "uri": "/v2beta1/{name=projects/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchDeleteIntents(
        _BaseIntentsRestTransport._BaseBatchDeleteIntents, IntentsRestStub
    ):
        def __hash__(self):
            return hash("IntentsRestTransport.BatchDeleteIntents")

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
            request: intent.BatchDeleteIntentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch delete intents method over HTTP.

            Args:
                request (~.intent.BatchDeleteIntentsRequest):
                    The request object. The request message for
                [Intents.BatchDeleteIntents][google.cloud.dialogflow.v2beta1.Intents.BatchDeleteIntents].
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
                _BaseIntentsRestTransport._BaseBatchDeleteIntents._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_delete_intents(
                request, metadata
            )
            transcoded_request = _BaseIntentsRestTransport._BaseBatchDeleteIntents._get_transcoded_request(
                http_options, request
            )

            body = _BaseIntentsRestTransport._BaseBatchDeleteIntents._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseIntentsRestTransport._BaseBatchDeleteIntents._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = IntentsRestTransport._BatchDeleteIntents._get_response(
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
            resp = self._interceptor.post_batch_delete_intents(resp)
            return resp

    class _BatchUpdateIntents(
        _BaseIntentsRestTransport._BaseBatchUpdateIntents, IntentsRestStub
    ):
        def __hash__(self):
            return hash("IntentsRestTransport.BatchUpdateIntents")

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
            request: intent.BatchUpdateIntentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch update intents method over HTTP.

            Args:
                request (~.intent.BatchUpdateIntentsRequest):
                    The request object. The request message for
                [Intents.BatchUpdateIntents][google.cloud.dialogflow.v2beta1.Intents.BatchUpdateIntents].
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
                _BaseIntentsRestTransport._BaseBatchUpdateIntents._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_update_intents(
                request, metadata
            )
            transcoded_request = _BaseIntentsRestTransport._BaseBatchUpdateIntents._get_transcoded_request(
                http_options, request
            )

            body = _BaseIntentsRestTransport._BaseBatchUpdateIntents._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseIntentsRestTransport._BaseBatchUpdateIntents._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = IntentsRestTransport._BatchUpdateIntents._get_response(
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
            resp = self._interceptor.post_batch_update_intents(resp)
            return resp

    class _CreateIntent(_BaseIntentsRestTransport._BaseCreateIntent, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.CreateIntent")

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
            request: gcd_intent.CreateIntentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_intent.Intent:
            r"""Call the create intent method over HTTP.

            Args:
                request (~.gcd_intent.CreateIntentRequest):
                    The request object. The request message for
                [Intents.CreateIntent][google.cloud.dialogflow.v2beta1.Intents.CreateIntent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_intent.Intent:
                    An intent categorizes an end-user's intention for one
                conversation turn. For each agent, you define many
                intents, where your combined intents can handle a
                complete conversation. When an end-user writes or says
                something, referred to as an end-user expression or
                end-user input, Dialogflow matches the end-user input to
                the best intent in your agent. Matching an intent is
                also known as intent classification.

                For more information, see the `intent
                guide <https://cloud.google.com/dialogflow/docs/intents-overview>`__.

            """

            http_options = (
                _BaseIntentsRestTransport._BaseCreateIntent._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_intent(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseCreateIntent._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseIntentsRestTransport._BaseCreateIntent._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseCreateIntent._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._CreateIntent._get_response(
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
            resp = gcd_intent.Intent()
            pb_resp = gcd_intent.Intent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_intent(resp)
            return resp

    class _DeleteIntent(_BaseIntentsRestTransport._BaseDeleteIntent, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.DeleteIntent")

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
            request: intent.DeleteIntentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete intent method over HTTP.

            Args:
                request (~.intent.DeleteIntentRequest):
                    The request object. The request message for
                [Intents.DeleteIntent][google.cloud.dialogflow.v2beta1.Intents.DeleteIntent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseIntentsRestTransport._BaseDeleteIntent._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_intent(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseDeleteIntent._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseDeleteIntent._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._DeleteIntent._get_response(
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

    class _GetIntent(_BaseIntentsRestTransport._BaseGetIntent, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.GetIntent")

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
            request: intent.GetIntentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> intent.Intent:
            r"""Call the get intent method over HTTP.

            Args:
                request (~.intent.GetIntentRequest):
                    The request object. The request message for
                [Intents.GetIntent][google.cloud.dialogflow.v2beta1.Intents.GetIntent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.intent.Intent:
                    An intent categorizes an end-user's intention for one
                conversation turn. For each agent, you define many
                intents, where your combined intents can handle a
                complete conversation. When an end-user writes or says
                something, referred to as an end-user expression or
                end-user input, Dialogflow matches the end-user input to
                the best intent in your agent. Matching an intent is
                also known as intent classification.

                For more information, see the `intent
                guide <https://cloud.google.com/dialogflow/docs/intents-overview>`__.

            """

            http_options = _BaseIntentsRestTransport._BaseGetIntent._get_http_options()
            request, metadata = self._interceptor.pre_get_intent(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseGetIntent._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseGetIntent._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._GetIntent._get_response(
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
            resp = intent.Intent()
            pb_resp = intent.Intent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_intent(resp)
            return resp

    class _ListIntents(_BaseIntentsRestTransport._BaseListIntents, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.ListIntents")

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
            request: intent.ListIntentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> intent.ListIntentsResponse:
            r"""Call the list intents method over HTTP.

            Args:
                request (~.intent.ListIntentsRequest):
                    The request object. The request message for
                [Intents.ListIntents][google.cloud.dialogflow.v2beta1.Intents.ListIntents].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.intent.ListIntentsResponse:
                    The response message for
                [Intents.ListIntents][google.cloud.dialogflow.v2beta1.Intents.ListIntents].

            """

            http_options = (
                _BaseIntentsRestTransport._BaseListIntents._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_intents(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseListIntents._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseListIntents._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._ListIntents._get_response(
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
            resp = intent.ListIntentsResponse()
            pb_resp = intent.ListIntentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_intents(resp)
            return resp

    class _UpdateIntent(_BaseIntentsRestTransport._BaseUpdateIntent, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.UpdateIntent")

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
            request: gcd_intent.UpdateIntentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_intent.Intent:
            r"""Call the update intent method over HTTP.

            Args:
                request (~.gcd_intent.UpdateIntentRequest):
                    The request object. The request message for
                [Intents.UpdateIntent][google.cloud.dialogflow.v2beta1.Intents.UpdateIntent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_intent.Intent:
                    An intent categorizes an end-user's intention for one
                conversation turn. For each agent, you define many
                intents, where your combined intents can handle a
                complete conversation. When an end-user writes or says
                something, referred to as an end-user expression or
                end-user input, Dialogflow matches the end-user input to
                the best intent in your agent. Matching an intent is
                also known as intent classification.

                For more information, see the `intent
                guide <https://cloud.google.com/dialogflow/docs/intents-overview>`__.

            """

            http_options = (
                _BaseIntentsRestTransport._BaseUpdateIntent._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_intent(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseUpdateIntent._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseIntentsRestTransport._BaseUpdateIntent._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseUpdateIntent._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._UpdateIntent._get_response(
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
            resp = gcd_intent.Intent()
            pb_resp = gcd_intent.Intent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_intent(resp)
            return resp

    @property
    def batch_delete_intents(
        self,
    ) -> Callable[[intent.BatchDeleteIntentsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteIntents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_intents(
        self,
    ) -> Callable[[intent.BatchUpdateIntentsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateIntents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_intent(
        self,
    ) -> Callable[[gcd_intent.CreateIntentRequest], gcd_intent.Intent]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateIntent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_intent(self) -> Callable[[intent.DeleteIntentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIntent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_intent(self) -> Callable[[intent.GetIntentRequest], intent.Intent]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIntent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_intents(
        self,
    ) -> Callable[[intent.ListIntentsRequest], intent.ListIntentsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIntents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_intent(
        self,
    ) -> Callable[[gcd_intent.UpdateIntentRequest], gcd_intent.Intent]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateIntent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseIntentsRestTransport._BaseGetLocation, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.GetLocation")

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
                _BaseIntentsRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._GetLocation._get_response(
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

    class _ListLocations(_BaseIntentsRestTransport._BaseListLocations, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.ListLocations")

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
                _BaseIntentsRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._ListLocations._get_response(
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
        _BaseIntentsRestTransport._BaseCancelOperation, IntentsRestStub
    ):
        def __hash__(self):
            return hash("IntentsRestTransport.CancelOperation")

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
                _BaseIntentsRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseIntentsRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._CancelOperation._get_response(
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

    class _GetOperation(_BaseIntentsRestTransport._BaseGetOperation, IntentsRestStub):
        def __hash__(self):
            return hash("IntentsRestTransport.GetOperation")

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
                _BaseIntentsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._GetOperation._get_response(
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
        _BaseIntentsRestTransport._BaseListOperations, IntentsRestStub
    ):
        def __hash__(self):
            return hash("IntentsRestTransport.ListOperations")

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
                _BaseIntentsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseIntentsRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseIntentsRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = IntentsRestTransport._ListOperations._get_response(
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


__all__ = ("IntentsRestTransport",)
