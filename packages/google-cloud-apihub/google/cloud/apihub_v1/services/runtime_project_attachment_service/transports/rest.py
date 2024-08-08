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

from google.cloud.apihub_v1.types import runtime_project_attachment_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import RuntimeProjectAttachmentServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RuntimeProjectAttachmentServiceRestInterceptor:
    """Interceptor for RuntimeProjectAttachmentService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RuntimeProjectAttachmentServiceRestTransport.

    .. code-block:: python
        class MyCustomRuntimeProjectAttachmentServiceInterceptor(RuntimeProjectAttachmentServiceRestInterceptor):
            def pre_create_runtime_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_runtime_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_runtime_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_runtime_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_runtime_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_runtime_project_attachments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_runtime_project_attachments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_runtime_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_runtime_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RuntimeProjectAttachmentServiceRestTransport(interceptor=MyCustomRuntimeProjectAttachmentServiceInterceptor())
        client = RuntimeProjectAttachmentServiceClient(transport=transport)


    """

    def pre_create_runtime_project_attachment(
        self,
        request: runtime_project_attachment_service.CreateRuntimeProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        runtime_project_attachment_service.CreateRuntimeProjectAttachmentRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_runtime_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_create_runtime_project_attachment(
        self, response: runtime_project_attachment_service.RuntimeProjectAttachment
    ) -> runtime_project_attachment_service.RuntimeProjectAttachment:
        """Post-rpc interceptor for create_runtime_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_runtime_project_attachment(
        self,
        request: runtime_project_attachment_service.DeleteRuntimeProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        runtime_project_attachment_service.DeleteRuntimeProjectAttachmentRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_runtime_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def pre_get_runtime_project_attachment(
        self,
        request: runtime_project_attachment_service.GetRuntimeProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        runtime_project_attachment_service.GetRuntimeProjectAttachmentRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_runtime_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_get_runtime_project_attachment(
        self, response: runtime_project_attachment_service.RuntimeProjectAttachment
    ) -> runtime_project_attachment_service.RuntimeProjectAttachment:
        """Post-rpc interceptor for get_runtime_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
        it is returned to user code.
        """
        return response

    def pre_list_runtime_project_attachments(
        self,
        request: runtime_project_attachment_service.ListRuntimeProjectAttachmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        runtime_project_attachment_service.ListRuntimeProjectAttachmentsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_runtime_project_attachments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_list_runtime_project_attachments(
        self,
        response: runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse,
    ) -> runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse:
        """Post-rpc interceptor for list_runtime_project_attachments

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
        it is returned to user code.
        """
        return response

    def pre_lookup_runtime_project_attachment(
        self,
        request: runtime_project_attachment_service.LookupRuntimeProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        runtime_project_attachment_service.LookupRuntimeProjectAttachmentRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for lookup_runtime_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_lookup_runtime_project_attachment(
        self,
        response: runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse,
    ) -> runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse:
        """Post-rpc interceptor for lookup_runtime_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
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
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
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
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
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
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
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
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
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
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
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
        before they are sent to the RuntimeProjectAttachmentService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the RuntimeProjectAttachmentService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RuntimeProjectAttachmentServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RuntimeProjectAttachmentServiceRestInterceptor


class RuntimeProjectAttachmentServiceRestTransport(
    RuntimeProjectAttachmentServiceTransport
):
    """REST backend transport for RuntimeProjectAttachmentService.

    This service is used for managing the runtime project
    attachments.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "apihub.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RuntimeProjectAttachmentServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'apihub.googleapis.com').
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
        self._interceptor = (
            interceptor or RuntimeProjectAttachmentServiceRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _CreateRuntimeProjectAttachment(RuntimeProjectAttachmentServiceRestStub):
        def __hash__(self):
            return hash("CreateRuntimeProjectAttachment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "runtimeProjectAttachmentId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: runtime_project_attachment_service.CreateRuntimeProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> runtime_project_attachment_service.RuntimeProjectAttachment:
            r"""Call the create runtime project
            attachment method over HTTP.

                Args:
                    request (~.runtime_project_attachment_service.CreateRuntimeProjectAttachmentRequest):
                        The request object. The
                    [CreateRuntimeProjectAttachment][google.cloud.apihub.v1.RuntimeProjectAttachmentService.CreateRuntimeProjectAttachment]
                    method's request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.runtime_project_attachment_service.RuntimeProjectAttachment:
                        Runtime project attachment represents
                    an attachment from the runtime project
                    to the host project. Api Hub looks for
                    deployments in the attached runtime
                    projects and creates corresponding
                    resources in Api Hub for the discovered
                    deployments.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/runtimeProjectAttachments",
                    "body": "runtime_project_attachment",
                },
            ]
            request, metadata = self._interceptor.pre_create_runtime_project_attachment(
                request, metadata
            )
            pb_request = runtime_project_attachment_service.CreateRuntimeProjectAttachmentRequest.pb(
                request
            )
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
            resp = runtime_project_attachment_service.RuntimeProjectAttachment()
            pb_resp = runtime_project_attachment_service.RuntimeProjectAttachment.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_runtime_project_attachment(resp)
            return resp

    class _DeleteRuntimeProjectAttachment(RuntimeProjectAttachmentServiceRestStub):
        def __hash__(self):
            return hash("DeleteRuntimeProjectAttachment")

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
            request: runtime_project_attachment_service.DeleteRuntimeProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete runtime project
            attachment method over HTTP.

                Args:
                    request (~.runtime_project_attachment_service.DeleteRuntimeProjectAttachmentRequest):
                        The request object. The
                    [DeleteRuntimeProjectAttachment][google.cloud.apihub.v1.RuntimeProjectAttachmentService.DeleteRuntimeProjectAttachment]
                    method's request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/runtimeProjectAttachments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_runtime_project_attachment(
                request, metadata
            )
            pb_request = runtime_project_attachment_service.DeleteRuntimeProjectAttachmentRequest.pb(
                request
            )
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

    class _GetRuntimeProjectAttachment(RuntimeProjectAttachmentServiceRestStub):
        def __hash__(self):
            return hash("GetRuntimeProjectAttachment")

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
            request: runtime_project_attachment_service.GetRuntimeProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> runtime_project_attachment_service.RuntimeProjectAttachment:
            r"""Call the get runtime project
            attachment method over HTTP.

                Args:
                    request (~.runtime_project_attachment_service.GetRuntimeProjectAttachmentRequest):
                        The request object. The
                    [GetRuntimeProjectAttachment][google.cloud.apihub.v1.RuntimeProjectAttachmentService.GetRuntimeProjectAttachment]
                    method's request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.runtime_project_attachment_service.RuntimeProjectAttachment:
                        Runtime project attachment represents
                    an attachment from the runtime project
                    to the host project. Api Hub looks for
                    deployments in the attached runtime
                    projects and creates corresponding
                    resources in Api Hub for the discovered
                    deployments.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/runtimeProjectAttachments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_runtime_project_attachment(
                request, metadata
            )
            pb_request = runtime_project_attachment_service.GetRuntimeProjectAttachmentRequest.pb(
                request
            )
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
            resp = runtime_project_attachment_service.RuntimeProjectAttachment()
            pb_resp = runtime_project_attachment_service.RuntimeProjectAttachment.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_runtime_project_attachment(resp)
            return resp

    class _ListRuntimeProjectAttachments(RuntimeProjectAttachmentServiceRestStub):
        def __hash__(self):
            return hash("ListRuntimeProjectAttachments")

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
            request: runtime_project_attachment_service.ListRuntimeProjectAttachmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse:
            r"""Call the list runtime project
            attachments method over HTTP.

                Args:
                    request (~.runtime_project_attachment_service.ListRuntimeProjectAttachmentsRequest):
                        The request object. The
                    [ListRuntimeProjectAttachments][google.cloud.apihub.v1.RuntimeProjectAttachmentService.ListRuntimeProjectAttachments]
                    method's request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse:
                        The
                    [ListRuntimeProjectAttachments][google.cloud.apihub.v1.RuntimeProjectAttachmentService.ListRuntimeProjectAttachments]
                    method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/runtimeProjectAttachments",
                },
            ]
            request, metadata = self._interceptor.pre_list_runtime_project_attachments(
                request, metadata
            )
            pb_request = runtime_project_attachment_service.ListRuntimeProjectAttachmentsRequest.pb(
                request
            )
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
            resp = (
                runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse()
            )
            pb_resp = runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_runtime_project_attachments(resp)
            return resp

    class _LookupRuntimeProjectAttachment(RuntimeProjectAttachmentServiceRestStub):
        def __hash__(self):
            return hash("LookupRuntimeProjectAttachment")

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
            request: runtime_project_attachment_service.LookupRuntimeProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse:
            r"""Call the lookup runtime project
            attachment method over HTTP.

                Args:
                    request (~.runtime_project_attachment_service.LookupRuntimeProjectAttachmentRequest):
                        The request object. The
                    [LookupRuntimeProjectAttachment][google.cloud.apihub.v1.RuntimeProjectAttachmentService.LookupRuntimeProjectAttachment]
                    method's request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse:
                        The
                    [ListRuntimeProjectAttachments][google.cloud.apihub.v1.RuntimeProjectAttachmentService.ListRuntimeProjectAttachments]
                    method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}:lookupRuntimeProjectAttachment",
                },
            ]
            request, metadata = self._interceptor.pre_lookup_runtime_project_attachment(
                request, metadata
            )
            pb_request = runtime_project_attachment_service.LookupRuntimeProjectAttachmentRequest.pb(
                request
            )
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
            resp = (
                runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse()
            )
            pb_resp = runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lookup_runtime_project_attachment(resp)
            return resp

    @property
    def create_runtime_project_attachment(
        self,
    ) -> Callable[
        [runtime_project_attachment_service.CreateRuntimeProjectAttachmentRequest],
        runtime_project_attachment_service.RuntimeProjectAttachment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRuntimeProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_runtime_project_attachment(
        self,
    ) -> Callable[
        [runtime_project_attachment_service.DeleteRuntimeProjectAttachmentRequest],
        empty_pb2.Empty,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRuntimeProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_runtime_project_attachment(
        self,
    ) -> Callable[
        [runtime_project_attachment_service.GetRuntimeProjectAttachmentRequest],
        runtime_project_attachment_service.RuntimeProjectAttachment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRuntimeProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_runtime_project_attachments(
        self,
    ) -> Callable[
        [runtime_project_attachment_service.ListRuntimeProjectAttachmentsRequest],
        runtime_project_attachment_service.ListRuntimeProjectAttachmentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRuntimeProjectAttachments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_runtime_project_attachment(
        self,
    ) -> Callable[
        [runtime_project_attachment_service.LookupRuntimeProjectAttachmentRequest],
        runtime_project_attachment_service.LookupRuntimeProjectAttachmentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupRuntimeProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(RuntimeProjectAttachmentServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}",
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

    class _ListLocations(RuntimeProjectAttachmentServiceRestStub):
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
                    "uri": "/v1/{name=projects/*}/locations",
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

    class _CancelOperation(RuntimeProjectAttachmentServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(RuntimeProjectAttachmentServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(RuntimeProjectAttachmentServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(RuntimeProjectAttachmentServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
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


__all__ = ("RuntimeProjectAttachmentServiceRestTransport",)
