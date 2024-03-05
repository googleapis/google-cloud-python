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

from google.cloud.dialogflow_v2beta1.types import knowledge_base as gcd_knowledge_base
from google.cloud.dialogflow_v2beta1.types import knowledge_base

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import KnowledgeBasesTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class KnowledgeBasesRestInterceptor:
    """Interceptor for KnowledgeBases.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the KnowledgeBasesRestTransport.

    .. code-block:: python
        class MyCustomKnowledgeBasesInterceptor(KnowledgeBasesRestInterceptor):
            def pre_create_knowledge_base(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_knowledge_base(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_knowledge_base(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_knowledge_base(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_knowledge_base(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_knowledge_bases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_knowledge_bases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_knowledge_base(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_knowledge_base(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = KnowledgeBasesRestTransport(interceptor=MyCustomKnowledgeBasesInterceptor())
        client = KnowledgeBasesClient(transport=transport)


    """

    def pre_create_knowledge_base(
        self,
        request: gcd_knowledge_base.CreateKnowledgeBaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_knowledge_base.CreateKnowledgeBaseRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_knowledge_base

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_create_knowledge_base(
        self, response: gcd_knowledge_base.KnowledgeBase
    ) -> gcd_knowledge_base.KnowledgeBase:
        """Post-rpc interceptor for create_knowledge_base

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
        it is returned to user code.
        """
        return response

    def pre_delete_knowledge_base(
        self,
        request: knowledge_base.DeleteKnowledgeBaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[knowledge_base.DeleteKnowledgeBaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_knowledge_base

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def pre_get_knowledge_base(
        self,
        request: knowledge_base.GetKnowledgeBaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[knowledge_base.GetKnowledgeBaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_knowledge_base

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_get_knowledge_base(
        self, response: knowledge_base.KnowledgeBase
    ) -> knowledge_base.KnowledgeBase:
        """Post-rpc interceptor for get_knowledge_base

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
        it is returned to user code.
        """
        return response

    def pre_list_knowledge_bases(
        self,
        request: knowledge_base.ListKnowledgeBasesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[knowledge_base.ListKnowledgeBasesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_knowledge_bases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_list_knowledge_bases(
        self, response: knowledge_base.ListKnowledgeBasesResponse
    ) -> knowledge_base.ListKnowledgeBasesResponse:
        """Post-rpc interceptor for list_knowledge_bases

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
        it is returned to user code.
        """
        return response

    def pre_update_knowledge_base(
        self,
        request: gcd_knowledge_base.UpdateKnowledgeBaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_knowledge_base.UpdateKnowledgeBaseRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_knowledge_base

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_update_knowledge_base(
        self, response: gcd_knowledge_base.KnowledgeBase
    ) -> gcd_knowledge_base.KnowledgeBase:
        """Post-rpc interceptor for update_knowledge_base

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
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
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
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
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
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
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
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
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
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
        before they are sent to the KnowledgeBases server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the KnowledgeBases server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class KnowledgeBasesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: KnowledgeBasesRestInterceptor


class KnowledgeBasesRestTransport(KnowledgeBasesTransport):
    """REST backend transport for KnowledgeBases.

    Service for managing
    [KnowledgeBases][google.cloud.dialogflow.v2beta1.KnowledgeBase].

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
        interceptor: Optional[KnowledgeBasesRestInterceptor] = None,
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
        self._interceptor = interceptor or KnowledgeBasesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateKnowledgeBase(KnowledgeBasesRestStub):
        def __hash__(self):
            return hash("CreateKnowledgeBase")

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
            request: gcd_knowledge_base.CreateKnowledgeBaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_knowledge_base.KnowledgeBase:
            r"""Call the create knowledge base method over HTTP.

            Args:
                request (~.gcd_knowledge_base.CreateKnowledgeBaseRequest):
                    The request object. Request message for
                [KnowledgeBases.CreateKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.CreateKnowledgeBase].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_knowledge_base.KnowledgeBase:
                    A knowledge base represents a collection of knowledge
                documents that you provide to Dialogflow. Your knowledge
                documents contain information that may be useful during
                conversations with end-users. Some Dialogflow features
                use knowledge bases when looking for a response to an
                end-user input.

                For more information, see the `knowledge base
                guide <https://cloud.google.com/dialogflow/docs/how/knowledge-bases>`__.

                Note: The ``projects.agent.knowledgeBases`` resource is
                deprecated; only use ``projects.knowledgeBases``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2beta1/{parent=projects/*}/knowledgeBases",
                    "body": "knowledge_base",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{parent=projects/*/locations/*}/knowledgeBases",
                    "body": "knowledge_base",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{parent=projects/*/agent}/knowledgeBases",
                    "body": "knowledge_base",
                },
            ]
            request, metadata = self._interceptor.pre_create_knowledge_base(
                request, metadata
            )
            pb_request = gcd_knowledge_base.CreateKnowledgeBaseRequest.pb(request)
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
            resp = gcd_knowledge_base.KnowledgeBase()
            pb_resp = gcd_knowledge_base.KnowledgeBase.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_knowledge_base(resp)
            return resp

    class _DeleteKnowledgeBase(KnowledgeBasesRestStub):
        def __hash__(self):
            return hash("DeleteKnowledgeBase")

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
            request: knowledge_base.DeleteKnowledgeBaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete knowledge base method over HTTP.

            Args:
                request (~.knowledge_base.DeleteKnowledgeBaseRequest):
                    The request object. Request message for
                [KnowledgeBases.DeleteKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.DeleteKnowledgeBase].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2beta1/{name=projects/*/knowledgeBases/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2beta1/{name=projects/*/locations/*/knowledgeBases/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2beta1/{name=projects/*/agent/knowledgeBases/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_knowledge_base(
                request, metadata
            )
            pb_request = knowledge_base.DeleteKnowledgeBaseRequest.pb(request)
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

    class _GetKnowledgeBase(KnowledgeBasesRestStub):
        def __hash__(self):
            return hash("GetKnowledgeBase")

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
            request: knowledge_base.GetKnowledgeBaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> knowledge_base.KnowledgeBase:
            r"""Call the get knowledge base method over HTTP.

            Args:
                request (~.knowledge_base.GetKnowledgeBaseRequest):
                    The request object. Request message for
                [KnowledgeBases.GetKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.GetKnowledgeBase].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.knowledge_base.KnowledgeBase:
                    A knowledge base represents a collection of knowledge
                documents that you provide to Dialogflow. Your knowledge
                documents contain information that may be useful during
                conversations with end-users. Some Dialogflow features
                use knowledge bases when looking for a response to an
                end-user input.

                For more information, see the `knowledge base
                guide <https://cloud.google.com/dialogflow/docs/how/knowledge-bases>`__.

                Note: The ``projects.agent.knowledgeBases`` resource is
                deprecated; only use ``projects.knowledgeBases``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/knowledgeBases/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*/knowledgeBases/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/agent/knowledgeBases/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_knowledge_base(
                request, metadata
            )
            pb_request = knowledge_base.GetKnowledgeBaseRequest.pb(request)
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
            resp = knowledge_base.KnowledgeBase()
            pb_resp = knowledge_base.KnowledgeBase.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_knowledge_base(resp)
            return resp

    class _ListKnowledgeBases(KnowledgeBasesRestStub):
        def __hash__(self):
            return hash("ListKnowledgeBases")

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
            request: knowledge_base.ListKnowledgeBasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> knowledge_base.ListKnowledgeBasesResponse:
            r"""Call the list knowledge bases method over HTTP.

            Args:
                request (~.knowledge_base.ListKnowledgeBasesRequest):
                    The request object. Request message for
                [KnowledgeBases.ListKnowledgeBases][google.cloud.dialogflow.v2beta1.KnowledgeBases.ListKnowledgeBases].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.knowledge_base.ListKnowledgeBasesResponse:
                    Response message for
                [KnowledgeBases.ListKnowledgeBases][google.cloud.dialogflow.v2beta1.KnowledgeBases.ListKnowledgeBases].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{parent=projects/*}/knowledgeBases",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{parent=projects/*/locations/*}/knowledgeBases",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{parent=projects/*/agent}/knowledgeBases",
                },
            ]
            request, metadata = self._interceptor.pre_list_knowledge_bases(
                request, metadata
            )
            pb_request = knowledge_base.ListKnowledgeBasesRequest.pb(request)
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
            resp = knowledge_base.ListKnowledgeBasesResponse()
            pb_resp = knowledge_base.ListKnowledgeBasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_knowledge_bases(resp)
            return resp

    class _UpdateKnowledgeBase(KnowledgeBasesRestStub):
        def __hash__(self):
            return hash("UpdateKnowledgeBase")

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
            request: gcd_knowledge_base.UpdateKnowledgeBaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_knowledge_base.KnowledgeBase:
            r"""Call the update knowledge base method over HTTP.

            Args:
                request (~.gcd_knowledge_base.UpdateKnowledgeBaseRequest):
                    The request object. Request message for
                [KnowledgeBases.UpdateKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.UpdateKnowledgeBase].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_knowledge_base.KnowledgeBase:
                    A knowledge base represents a collection of knowledge
                documents that you provide to Dialogflow. Your knowledge
                documents contain information that may be useful during
                conversations with end-users. Some Dialogflow features
                use knowledge bases when looking for a response to an
                end-user input.

                For more information, see the `knowledge base
                guide <https://cloud.google.com/dialogflow/docs/how/knowledge-bases>`__.

                Note: The ``projects.agent.knowledgeBases`` resource is
                deprecated; only use ``projects.knowledgeBases``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2beta1/{knowledge_base.name=projects/*/knowledgeBases/*}",
                    "body": "knowledge_base",
                },
                {
                    "method": "patch",
                    "uri": "/v2beta1/{knowledge_base.name=projects/*/locations/*/knowledgeBases/*}",
                    "body": "knowledge_base",
                },
                {
                    "method": "patch",
                    "uri": "/v2beta1/{knowledge_base.name=projects/*/agent/knowledgeBases/*}",
                    "body": "knowledge_base",
                },
            ]
            request, metadata = self._interceptor.pre_update_knowledge_base(
                request, metadata
            )
            pb_request = gcd_knowledge_base.UpdateKnowledgeBaseRequest.pb(request)
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
            resp = gcd_knowledge_base.KnowledgeBase()
            pb_resp = gcd_knowledge_base.KnowledgeBase.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_knowledge_base(resp)
            return resp

    @property
    def create_knowledge_base(
        self,
    ) -> Callable[
        [gcd_knowledge_base.CreateKnowledgeBaseRequest],
        gcd_knowledge_base.KnowledgeBase,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateKnowledgeBase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_knowledge_base(
        self,
    ) -> Callable[[knowledge_base.DeleteKnowledgeBaseRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteKnowledgeBase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_knowledge_base(
        self,
    ) -> Callable[
        [knowledge_base.GetKnowledgeBaseRequest], knowledge_base.KnowledgeBase
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetKnowledgeBase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_knowledge_bases(
        self,
    ) -> Callable[
        [knowledge_base.ListKnowledgeBasesRequest],
        knowledge_base.ListKnowledgeBasesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListKnowledgeBases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_knowledge_base(
        self,
    ) -> Callable[
        [gcd_knowledge_base.UpdateKnowledgeBaseRequest],
        gcd_knowledge_base.KnowledgeBase,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateKnowledgeBase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(KnowledgeBasesRestStub):
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
                    "uri": "/v2beta1/{name=projects/*/locations/*}",
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

    class _ListLocations(KnowledgeBasesRestStub):
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
                    "uri": "/v2beta1/{name=projects/*}/locations",
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

    class _CancelOperation(KnowledgeBasesRestStub):
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
                    "uri": "/v2beta1/{name=projects/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}:cancel",
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

    class _GetOperation(KnowledgeBasesRestStub):
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
                    "uri": "/v2beta1/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(KnowledgeBasesRestStub):
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
                    "uri": "/v2beta1/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*}/operations",
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


__all__ = ("KnowledgeBasesRestTransport",)
