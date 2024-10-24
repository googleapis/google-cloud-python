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

from google.cloud.dialogflowcx_v3beta1.types import playbook
from google.cloud.dialogflowcx_v3beta1.types import playbook as gcdc_playbook

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import PlaybooksTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class PlaybooksRestInterceptor:
    """Interceptor for Playbooks.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PlaybooksRestTransport.

    .. code-block:: python
        class MyCustomPlaybooksInterceptor(PlaybooksRestInterceptor):
            def pre_create_playbook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_playbook(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_playbook_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_playbook_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_playbook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_playbook_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_playbook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_playbook(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_playbook_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_playbook_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_playbooks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_playbooks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_playbook_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_playbook_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_playbook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_playbook(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PlaybooksRestTransport(interceptor=MyCustomPlaybooksInterceptor())
        client = PlaybooksClient(transport=transport)


    """

    def pre_create_playbook(
        self,
        request: gcdc_playbook.CreatePlaybookRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcdc_playbook.CreatePlaybookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_playbook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_create_playbook(
        self, response: gcdc_playbook.Playbook
    ) -> gcdc_playbook.Playbook:
        """Post-rpc interceptor for create_playbook

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response

    def pre_create_playbook_version(
        self,
        request: playbook.CreatePlaybookVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[playbook.CreatePlaybookVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_playbook_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_create_playbook_version(
        self, response: playbook.PlaybookVersion
    ) -> playbook.PlaybookVersion:
        """Post-rpc interceptor for create_playbook_version

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response

    def pre_delete_playbook(
        self,
        request: playbook.DeletePlaybookRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[playbook.DeletePlaybookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_playbook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def pre_delete_playbook_version(
        self,
        request: playbook.DeletePlaybookVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[playbook.DeletePlaybookVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_playbook_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def pre_get_playbook(
        self, request: playbook.GetPlaybookRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[playbook.GetPlaybookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_playbook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_get_playbook(self, response: playbook.Playbook) -> playbook.Playbook:
        """Post-rpc interceptor for get_playbook

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response

    def pre_get_playbook_version(
        self,
        request: playbook.GetPlaybookVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[playbook.GetPlaybookVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_playbook_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_get_playbook_version(
        self, response: playbook.PlaybookVersion
    ) -> playbook.PlaybookVersion:
        """Post-rpc interceptor for get_playbook_version

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response

    def pre_list_playbooks(
        self,
        request: playbook.ListPlaybooksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[playbook.ListPlaybooksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_playbooks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_list_playbooks(
        self, response: playbook.ListPlaybooksResponse
    ) -> playbook.ListPlaybooksResponse:
        """Post-rpc interceptor for list_playbooks

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response

    def pre_list_playbook_versions(
        self,
        request: playbook.ListPlaybookVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[playbook.ListPlaybookVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_playbook_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_list_playbook_versions(
        self, response: playbook.ListPlaybookVersionsResponse
    ) -> playbook.ListPlaybookVersionsResponse:
        """Post-rpc interceptor for list_playbook_versions

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response

    def pre_update_playbook(
        self,
        request: gcdc_playbook.UpdatePlaybookRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcdc_playbook.UpdatePlaybookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_playbook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_update_playbook(
        self, response: gcdc_playbook.Playbook
    ) -> gcdc_playbook.Playbook:
        """Post-rpc interceptor for update_playbook

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
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
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
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
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
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
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
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
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
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
        before they are sent to the Playbooks server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Playbooks server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PlaybooksRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PlaybooksRestInterceptor


class PlaybooksRestTransport(PlaybooksTransport):
    """REST backend transport for Playbooks.

    Service for managing
    [Playbooks][google.cloud.dialogflow.cx.v3beta1.Playbook].

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
        interceptor: Optional[PlaybooksRestInterceptor] = None,
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
        self._interceptor = interceptor or PlaybooksRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreatePlaybook(PlaybooksRestStub):
        def __hash__(self):
            return hash("CreatePlaybook")

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
            request: gcdc_playbook.CreatePlaybookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcdc_playbook.Playbook:
            r"""Call the create playbook method over HTTP.

            Args:
                request (~.gcdc_playbook.CreatePlaybookRequest):
                    The request object. The request message for
                [Playbooks.CreatePlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.CreatePlaybook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcdc_playbook.Playbook:
                    Playbook is the basic building block
                to instruct the LLM how to execute a
                certain task.

                A playbook consists of a goal to
                accomplish, an optional list of step by
                step instructions (the step instruction
                may refers to name of the custom or
                default plugin tools to use) to perform
                the task, a list of contextual input
                data to be passed in at the beginning of
                the invoked, and a list of output
                parameters to store the playbook result.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*/agents/*}/playbooks",
                    "body": "playbook",
                },
            ]
            request, metadata = self._interceptor.pre_create_playbook(request, metadata)
            pb_request = gcdc_playbook.CreatePlaybookRequest.pb(request)
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
            resp = gcdc_playbook.Playbook()
            pb_resp = gcdc_playbook.Playbook.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_playbook(resp)
            return resp

    class _CreatePlaybookVersion(PlaybooksRestStub):
        def __hash__(self):
            return hash("CreatePlaybookVersion")

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
            request: playbook.CreatePlaybookVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> playbook.PlaybookVersion:
            r"""Call the create playbook version method over HTTP.

            Args:
                request (~.playbook.CreatePlaybookVersionRequest):
                    The request object. The request message for
                [Playbooks.CreatePlaybookVersion][google.cloud.dialogflow.cx.v3beta1.Playbooks.CreatePlaybookVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.playbook.PlaybookVersion:
                    Playbook version is a snapshot of the
                playbook at certain timestamp.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*/agents/*/playbooks/*}/versions",
                    "body": "playbook_version",
                },
            ]
            request, metadata = self._interceptor.pre_create_playbook_version(
                request, metadata
            )
            pb_request = playbook.CreatePlaybookVersionRequest.pb(request)
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
            resp = playbook.PlaybookVersion()
            pb_resp = playbook.PlaybookVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_playbook_version(resp)
            return resp

    class _DeletePlaybook(PlaybooksRestStub):
        def __hash__(self):
            return hash("DeletePlaybook")

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
            request: playbook.DeletePlaybookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete playbook method over HTTP.

            Args:
                request (~.playbook.DeletePlaybookRequest):
                    The request object. The request message for
                [Playbooks.DeletePlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.DeletePlaybook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_playbook(request, metadata)
            pb_request = playbook.DeletePlaybookRequest.pb(request)
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

    class _DeletePlaybookVersion(PlaybooksRestStub):
        def __hash__(self):
            return hash("DeletePlaybookVersion")

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
            request: playbook.DeletePlaybookVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete playbook version method over HTTP.

            Args:
                request (~.playbook.DeletePlaybookVersionRequest):
                    The request object. The request message for
                [Playbooks.DeletePlaybookVersion][google.cloud.dialogflow.cx.v3beta1.Playbooks.DeletePlaybookVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_playbook_version(
                request, metadata
            )
            pb_request = playbook.DeletePlaybookVersionRequest.pb(request)
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

    class _GetPlaybook(PlaybooksRestStub):
        def __hash__(self):
            return hash("GetPlaybook")

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
            request: playbook.GetPlaybookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> playbook.Playbook:
            r"""Call the get playbook method over HTTP.

            Args:
                request (~.playbook.GetPlaybookRequest):
                    The request object. The request message for
                [Playbooks.GetPlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.GetPlaybook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.playbook.Playbook:
                    Playbook is the basic building block
                to instruct the LLM how to execute a
                certain task.

                A playbook consists of a goal to
                accomplish, an optional list of step by
                step instructions (the step instruction
                may refers to name of the custom or
                default plugin tools to use) to perform
                the task, a list of contextual input
                data to be passed in at the beginning of
                the invoked, and a list of output
                parameters to store the playbook result.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_playbook(request, metadata)
            pb_request = playbook.GetPlaybookRequest.pb(request)
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
            resp = playbook.Playbook()
            pb_resp = playbook.Playbook.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_playbook(resp)
            return resp

    class _GetPlaybookVersion(PlaybooksRestStub):
        def __hash__(self):
            return hash("GetPlaybookVersion")

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
            request: playbook.GetPlaybookVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> playbook.PlaybookVersion:
            r"""Call the get playbook version method over HTTP.

            Args:
                request (~.playbook.GetPlaybookVersionRequest):
                    The request object. The request message for
                [Playbooks.GetPlaybookVersion][google.cloud.dialogflow.cx.v3beta1.Playbooks.GetPlaybookVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.playbook.PlaybookVersion:
                    Playbook version is a snapshot of the
                playbook at certain timestamp.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_playbook_version(
                request, metadata
            )
            pb_request = playbook.GetPlaybookVersionRequest.pb(request)
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
            resp = playbook.PlaybookVersion()
            pb_resp = playbook.PlaybookVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_playbook_version(resp)
            return resp

    class _ListPlaybooks(PlaybooksRestStub):
        def __hash__(self):
            return hash("ListPlaybooks")

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
            request: playbook.ListPlaybooksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> playbook.ListPlaybooksResponse:
            r"""Call the list playbooks method over HTTP.

            Args:
                request (~.playbook.ListPlaybooksRequest):
                    The request object. The request message for
                [Playbooks.ListPlaybooks][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybooks].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.playbook.ListPlaybooksResponse:
                    The response message for
                [Playbooks.ListPlaybooks][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybooks].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{parent=projects/*/locations/*/agents/*}/playbooks",
                },
            ]
            request, metadata = self._interceptor.pre_list_playbooks(request, metadata)
            pb_request = playbook.ListPlaybooksRequest.pb(request)
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
            resp = playbook.ListPlaybooksResponse()
            pb_resp = playbook.ListPlaybooksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_playbooks(resp)
            return resp

    class _ListPlaybookVersions(PlaybooksRestStub):
        def __hash__(self):
            return hash("ListPlaybookVersions")

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
            request: playbook.ListPlaybookVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> playbook.ListPlaybookVersionsResponse:
            r"""Call the list playbook versions method over HTTP.

            Args:
                request (~.playbook.ListPlaybookVersionsRequest):
                    The request object. The request message for
                [Playbooks.ListPlaybookVersions][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybookVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.playbook.ListPlaybookVersionsResponse:
                    The response message for
                [Playbooks.ListPlaybookVersions][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybookVersions].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{parent=projects/*/locations/*/agents/*/playbooks/*}/versions",
                },
            ]
            request, metadata = self._interceptor.pre_list_playbook_versions(
                request, metadata
            )
            pb_request = playbook.ListPlaybookVersionsRequest.pb(request)
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
            resp = playbook.ListPlaybookVersionsResponse()
            pb_resp = playbook.ListPlaybookVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_playbook_versions(resp)
            return resp

    class _UpdatePlaybook(PlaybooksRestStub):
        def __hash__(self):
            return hash("UpdatePlaybook")

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
            request: gcdc_playbook.UpdatePlaybookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcdc_playbook.Playbook:
            r"""Call the update playbook method over HTTP.

            Args:
                request (~.gcdc_playbook.UpdatePlaybookRequest):
                    The request object. The request message for
                [Playbooks.UpdatePlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.UpdatePlaybook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcdc_playbook.Playbook:
                    Playbook is the basic building block
                to instruct the LLM how to execute a
                certain task.

                A playbook consists of a goal to
                accomplish, an optional list of step by
                step instructions (the step instruction
                may refers to name of the custom or
                default plugin tools to use) to perform
                the task, a list of contextual input
                data to be passed in at the beginning of
                the invoked, and a list of output
                parameters to store the playbook result.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v3beta1/{playbook.name=projects/*/locations/*/agents/*/playbooks/*}",
                    "body": "playbook",
                },
            ]
            request, metadata = self._interceptor.pre_update_playbook(request, metadata)
            pb_request = gcdc_playbook.UpdatePlaybookRequest.pb(request)
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
            resp = gcdc_playbook.Playbook()
            pb_resp = gcdc_playbook.Playbook.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_playbook(resp)
            return resp

    @property
    def create_playbook(
        self,
    ) -> Callable[[gcdc_playbook.CreatePlaybookRequest], gcdc_playbook.Playbook]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePlaybook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_playbook_version(
        self,
    ) -> Callable[[playbook.CreatePlaybookVersionRequest], playbook.PlaybookVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePlaybookVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_playbook(
        self,
    ) -> Callable[[playbook.DeletePlaybookRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePlaybook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_playbook_version(
        self,
    ) -> Callable[[playbook.DeletePlaybookVersionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePlaybookVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_playbook(
        self,
    ) -> Callable[[playbook.GetPlaybookRequest], playbook.Playbook]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPlaybook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_playbook_version(
        self,
    ) -> Callable[[playbook.GetPlaybookVersionRequest], playbook.PlaybookVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPlaybookVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_playbooks(
        self,
    ) -> Callable[[playbook.ListPlaybooksRequest], playbook.ListPlaybooksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPlaybooks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_playbook_versions(
        self,
    ) -> Callable[
        [playbook.ListPlaybookVersionsRequest], playbook.ListPlaybookVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPlaybookVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_playbook(
        self,
    ) -> Callable[[gcdc_playbook.UpdatePlaybookRequest], gcdc_playbook.Playbook]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePlaybook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(PlaybooksRestStub):
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
                    "uri": "/v3beta1/{name=projects/*/locations/*}",
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

    class _ListLocations(PlaybooksRestStub):
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
                    "uri": "/v3beta1/{name=projects/*}/locations",
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

    class _CancelOperation(PlaybooksRestStub):
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
                    "uri": "/v3beta1/{name=projects/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}:cancel",
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

    class _GetOperation(PlaybooksRestStub):
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
                    "uri": "/v3beta1/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(PlaybooksRestStub):
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
                    "uri": "/v3beta1/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v3beta1/{name=projects/*/locations/*}/operations",
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


__all__ = ("PlaybooksRestTransport",)
