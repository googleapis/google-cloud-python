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
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.dialogflow_v2.types import context
from google.cloud.dialogflow_v2.types import context as gcd_context

from .base import ContextsTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ContextsRestInterceptor:
    """Interceptor for Contexts.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ContextsRestTransport.

    .. code-block:: python
        class MyCustomContextsInterceptor(ContextsRestInterceptor):
            def pre_create_context(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_context(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_all_contexts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_context(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_context(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_context(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_contexts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_contexts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_context(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_context(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ContextsRestTransport(interceptor=MyCustomContextsInterceptor())
        client = ContextsClient(transport=transport)


    """

    def pre_create_context(
        self,
        request: gcd_context.CreateContextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_context.CreateContextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_context

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_create_context(self, response: gcd_context.Context) -> gcd_context.Context:
        """Post-rpc interceptor for create_context

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
        it is returned to user code.
        """
        return response

    def pre_delete_all_contexts(
        self,
        request: context.DeleteAllContextsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[context.DeleteAllContextsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_all_contexts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Contexts server.
        """
        return request, metadata

    def pre_delete_context(
        self, request: context.DeleteContextRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[context.DeleteContextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_context

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Contexts server.
        """
        return request, metadata

    def pre_get_context(
        self, request: context.GetContextRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[context.GetContextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_context

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_get_context(self, response: context.Context) -> context.Context:
        """Post-rpc interceptor for get_context

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
        it is returned to user code.
        """
        return response

    def pre_list_contexts(
        self, request: context.ListContextsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[context.ListContextsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_contexts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_list_contexts(
        self, response: context.ListContextsResponse
    ) -> context.ListContextsResponse:
        """Post-rpc interceptor for list_contexts

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
        it is returned to user code.
        """
        return response

    def pre_update_context(
        self,
        request: gcd_context.UpdateContextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_context.UpdateContextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_context

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_update_context(self, response: gcd_context.Context) -> gcd_context.Context:
        """Post-rpc interceptor for update_context

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
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
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
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
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
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
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
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
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
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
        before they are sent to the Contexts server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Contexts server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ContextsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ContextsRestInterceptor


class ContextsRestTransport(ContextsTransport):
    """REST backend transport for Contexts.

    Service for managing [Contexts][google.cloud.dialogflow.v2.Context].

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
        interceptor: Optional[ContextsRestInterceptor] = None,
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ContextsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateContext(ContextsRestStub):
        def __hash__(self):
            return hash("CreateContext")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_context.CreateContextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_context.Context:
            r"""Call the create context method over HTTP.

            Args:
                request (~.gcd_context.CreateContextRequest):
                    The request object. The request message for
                [Contexts.CreateContext][google.cloud.dialogflow.v2.Contexts.CreateContext].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_context.Context:
                    Dialogflow contexts are similar to natural language
                context. If a person says to you "they are orange", you
                need context in order to understand what "they" is
                referring to. Similarly, for Dialogflow to handle an
                end-user expression like that, it needs to be provided
                with context in order to correctly match an intent.

                Using contexts, you can control the flow of a
                conversation. You can configure contexts for an intent
                by setting input and output contexts, which are
                identified by string names. When an intent is matched,
                any configured output contexts for that intent become
                active. While any contexts are active, Dialogflow is
                more likely to match intents that are configured with
                input contexts that correspond to the currently active
                contexts.

                For more information about context, see the `Contexts
                guide <https://cloud.google.com/dialogflow/docs/contexts-overview>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/agent/sessions/*}/contexts",
                    "body": "context",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/agent/environments/*/users/*/sessions/*}/contexts",
                    "body": "context",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*/agent/sessions/*}/contexts",
                    "body": "context",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*/agent/environments/*/users/*/sessions/*}/contexts",
                    "body": "context",
                },
            ]
            request, metadata = self._interceptor.pre_create_context(request, metadata)
            pb_request = gcd_context.CreateContextRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_context.Context()
            pb_resp = gcd_context.Context.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_context(resp)
            return resp

    class _DeleteAllContexts(ContextsRestStub):
        def __hash__(self):
            return hash("DeleteAllContexts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: context.DeleteAllContextsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete all contexts method over HTTP.

            Args:
                request (~.context.DeleteAllContextsRequest):
                    The request object. The request message for
                [Contexts.DeleteAllContexts][google.cloud.dialogflow.v2.Contexts.DeleteAllContexts].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{parent=projects/*/agent/sessions/*}/contexts",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{parent=projects/*/agent/environments/*/users/*/sessions/*}/contexts",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{parent=projects/*/locations/*/agent/sessions/*}/contexts",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{parent=projects/*/locations/*/agent/environments/*/users/*/sessions/*}/contexts",
                },
            ]
            request, metadata = self._interceptor.pre_delete_all_contexts(
                request, metadata
            )
            pb_request = context.DeleteAllContextsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteContext(ContextsRestStub):
        def __hash__(self):
            return hash("DeleteContext")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: context.DeleteContextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete context method over HTTP.

            Args:
                request (~.context.DeleteContextRequest):
                    The request object. The request message for
                [Contexts.DeleteContext][google.cloud.dialogflow.v2.Contexts.DeleteContext].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/agent/sessions/*/contexts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/agent/environments/*/users/*/sessions/*/contexts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/agent/sessions/*/contexts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/agent/environments/*/users/*/sessions/*/contexts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_context(request, metadata)
            pb_request = context.DeleteContextRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetContext(ContextsRestStub):
        def __hash__(self):
            return hash("GetContext")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: context.GetContextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> context.Context:
            r"""Call the get context method over HTTP.

            Args:
                request (~.context.GetContextRequest):
                    The request object. The request message for
                [Contexts.GetContext][google.cloud.dialogflow.v2.Contexts.GetContext].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.context.Context:
                    Dialogflow contexts are similar to natural language
                context. If a person says to you "they are orange", you
                need context in order to understand what "they" is
                referring to. Similarly, for Dialogflow to handle an
                end-user expression like that, it needs to be provided
                with context in order to correctly match an intent.

                Using contexts, you can control the flow of a
                conversation. You can configure contexts for an intent
                by setting input and output contexts, which are
                identified by string names. When an intent is matched,
                any configured output contexts for that intent become
                active. While any contexts are active, Dialogflow is
                more likely to match intents that are configured with
                input contexts that correspond to the currently active
                contexts.

                For more information about context, see the `Contexts
                guide <https://cloud.google.com/dialogflow/docs/contexts-overview>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/agent/sessions/*/contexts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/agent/environments/*/users/*/sessions/*/contexts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/agent/sessions/*/contexts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/agent/environments/*/users/*/sessions/*/contexts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_context(request, metadata)
            pb_request = context.GetContextRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = context.Context()
            pb_resp = context.Context.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_context(resp)
            return resp

    class _ListContexts(ContextsRestStub):
        def __hash__(self):
            return hash("ListContexts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: context.ListContextsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> context.ListContextsResponse:
            r"""Call the list contexts method over HTTP.

            Args:
                request (~.context.ListContextsRequest):
                    The request object. The request message for
                [Contexts.ListContexts][google.cloud.dialogflow.v2.Contexts.ListContexts].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.context.ListContextsResponse:
                    The response message for
                [Contexts.ListContexts][google.cloud.dialogflow.v2.Contexts.ListContexts].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/agent/sessions/*}/contexts",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/agent/environments/*/users/*/sessions/*}/contexts",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*/agent/sessions/*}/contexts",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*/agent/environments/*/users/*/sessions/*}/contexts",
                },
            ]
            request, metadata = self._interceptor.pre_list_contexts(request, metadata)
            pb_request = context.ListContextsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = context.ListContextsResponse()
            pb_resp = context.ListContextsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_contexts(resp)
            return resp

    class _UpdateContext(ContextsRestStub):
        def __hash__(self):
            return hash("UpdateContext")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_context.UpdateContextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_context.Context:
            r"""Call the update context method over HTTP.

            Args:
                request (~.gcd_context.UpdateContextRequest):
                    The request object. The request message for
                [Contexts.UpdateContext][google.cloud.dialogflow.v2.Contexts.UpdateContext].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_context.Context:
                    Dialogflow contexts are similar to natural language
                context. If a person says to you "they are orange", you
                need context in order to understand what "they" is
                referring to. Similarly, for Dialogflow to handle an
                end-user expression like that, it needs to be provided
                with context in order to correctly match an intent.

                Using contexts, you can control the flow of a
                conversation. You can configure contexts for an intent
                by setting input and output contexts, which are
                identified by string names. When an intent is matched,
                any configured output contexts for that intent become
                active. While any contexts are active, Dialogflow is
                more likely to match intents that are configured with
                input contexts that correspond to the currently active
                contexts.

                For more information about context, see the `Contexts
                guide <https://cloud.google.com/dialogflow/docs/contexts-overview>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{context.name=projects/*/agent/sessions/*/contexts/*}",
                    "body": "context",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{context.name=projects/*/agent/environments/*/users/*/sessions/*/contexts/*}",
                    "body": "context",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{context.name=projects/*/locations/*/agent/sessions/*/contexts/*}",
                    "body": "context",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{context.name=projects/*/locations/*/agent/environments/*/users/*/sessions/*/contexts/*}",
                    "body": "context",
                },
            ]
            request, metadata = self._interceptor.pre_update_context(request, metadata)
            pb_request = gcd_context.UpdateContextRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_context.Context()
            pb_resp = gcd_context.Context.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_context(resp)
            return resp

    @property
    def create_context(
        self,
    ) -> Callable[[gcd_context.CreateContextRequest], gcd_context.Context]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateContext(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_all_contexts(
        self,
    ) -> Callable[[context.DeleteAllContextsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAllContexts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_context(
        self,
    ) -> Callable[[context.DeleteContextRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteContext(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_context(self) -> Callable[[context.GetContextRequest], context.Context]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetContext(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_contexts(
        self,
    ) -> Callable[[context.ListContextsRequest], context.ListContextsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListContexts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_context(
        self,
    ) -> Callable[[gcd_context.UpdateContextRequest], gcd_context.Context]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateContext(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(ContextsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(ContextsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(ContextsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}:cancel",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(ContextsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(ContextsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ContextsRestTransport",)
