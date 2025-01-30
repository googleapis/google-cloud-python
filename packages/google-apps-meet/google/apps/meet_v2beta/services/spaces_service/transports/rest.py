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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.apps.meet_v2beta.types import resource, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSpacesServiceRestTransport

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


class SpacesServiceRestInterceptor:
    """Interceptor for SpacesService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SpacesServiceRestTransport.

    .. code-block:: python
        class MyCustomSpacesServiceInterceptor(SpacesServiceRestInterceptor):
            def pre_create_member(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_member(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_member(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_end_active_conference(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_member(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_member(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_members(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_members(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_space(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SpacesServiceRestTransport(interceptor=MyCustomSpacesServiceInterceptor())
        client = SpacesServiceClient(transport=transport)


    """

    def pre_create_member(
        self,
        request: service.CreateMemberRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateMemberRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_member

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def post_create_member(self, response: resource.Member) -> resource.Member:
        """Post-rpc interceptor for create_member

        Override in a subclass to manipulate the response
        after it is returned by the SpacesService server but before
        it is returned to user code.
        """
        return response

    def pre_create_space(
        self,
        request: service.CreateSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def post_create_space(self, response: resource.Space) -> resource.Space:
        """Post-rpc interceptor for create_space

        Override in a subclass to manipulate the response
        after it is returned by the SpacesService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_member(
        self,
        request: service.DeleteMemberRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteMemberRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_member

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def pre_end_active_conference(
        self,
        request: service.EndActiveConferenceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.EndActiveConferenceRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for end_active_conference

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def pre_get_member(
        self,
        request: service.GetMemberRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetMemberRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_member

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def post_get_member(self, response: resource.Member) -> resource.Member:
        """Post-rpc interceptor for get_member

        Override in a subclass to manipulate the response
        after it is returned by the SpacesService server but before
        it is returned to user code.
        """
        return response

    def pre_get_space(
        self,
        request: service.GetSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def post_get_space(self, response: resource.Space) -> resource.Space:
        """Post-rpc interceptor for get_space

        Override in a subclass to manipulate the response
        after it is returned by the SpacesService server but before
        it is returned to user code.
        """
        return response

    def pre_list_members(
        self,
        request: service.ListMembersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListMembersRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_members

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def post_list_members(
        self, response: service.ListMembersResponse
    ) -> service.ListMembersResponse:
        """Post-rpc interceptor for list_members

        Override in a subclass to manipulate the response
        after it is returned by the SpacesService server but before
        it is returned to user code.
        """
        return response

    def pre_update_space(
        self,
        request: service.UpdateSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SpacesService server.
        """
        return request, metadata

    def post_update_space(self, response: resource.Space) -> resource.Space:
        """Post-rpc interceptor for update_space

        Override in a subclass to manipulate the response
        after it is returned by the SpacesService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SpacesServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SpacesServiceRestInterceptor


class SpacesServiceRestTransport(_BaseSpacesServiceRestTransport):
    """REST backend synchronous transport for SpacesService.

    REST API for services dealing with spaces.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "meet.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SpacesServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'meet.googleapis.com').
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
        self._interceptor = interceptor or SpacesServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateMember(
        _BaseSpacesServiceRestTransport._BaseCreateMember, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.CreateMember")

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
            request: service.CreateMemberRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resource.Member:
            r"""Call the create member method over HTTP.

            Args:
                request (~.service.CreateMemberRequest):
                    The request object. Request to create a member for a
                space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resource.Member:
                    Users who are configured to have a
                role in the space. These users can join
                the space without knocking.

            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseCreateMember._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_member(request, metadata)
            transcoded_request = _BaseSpacesServiceRestTransport._BaseCreateMember._get_transcoded_request(
                http_options, request
            )

            body = _BaseSpacesServiceRestTransport._BaseCreateMember._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSpacesServiceRestTransport._BaseCreateMember._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.CreateMember",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "CreateMember",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._CreateMember._get_response(
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
            resp = resource.Member()
            pb_resp = resource.Member.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_member(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resource.Member.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.apps.meet_v2beta.SpacesServiceClient.create_member",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "CreateMember",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateSpace(
        _BaseSpacesServiceRestTransport._BaseCreateSpace, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.CreateSpace")

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
            request: service.CreateSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resource.Space:
            r"""Call the create space method over HTTP.

            Args:
                request (~.service.CreateSpaceRequest):
                    The request object. Request to create a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resource.Space:
                    Virtual place where conferences are
                held. Only one active conference can be
                held in one space at any given time.

            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseCreateSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_space(request, metadata)
            transcoded_request = _BaseSpacesServiceRestTransport._BaseCreateSpace._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseSpacesServiceRestTransport._BaseCreateSpace._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSpacesServiceRestTransport._BaseCreateSpace._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.CreateSpace",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "CreateSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._CreateSpace._get_response(
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
            resp = resource.Space()
            pb_resp = resource.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_space(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resource.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.apps.meet_v2beta.SpacesServiceClient.create_space",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "CreateSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteMember(
        _BaseSpacesServiceRestTransport._BaseDeleteMember, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.DeleteMember")

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
            request: service.DeleteMemberRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete member method over HTTP.

            Args:
                request (~.service.DeleteMemberRequest):
                    The request object. Request to delete a member from a
                space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseDeleteMember._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_member(request, metadata)
            transcoded_request = _BaseSpacesServiceRestTransport._BaseDeleteMember._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSpacesServiceRestTransport._BaseDeleteMember._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.DeleteMember",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "DeleteMember",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._DeleteMember._get_response(
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

    class _EndActiveConference(
        _BaseSpacesServiceRestTransport._BaseEndActiveConference, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.EndActiveConference")

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
            request: service.EndActiveConferenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the end active conference method over HTTP.

            Args:
                request (~.service.EndActiveConferenceRequest):
                    The request object. Request to end an ongoing conference
                of a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseEndActiveConference._get_http_options()
            )

            request, metadata = self._interceptor.pre_end_active_conference(
                request, metadata
            )
            transcoded_request = _BaseSpacesServiceRestTransport._BaseEndActiveConference._get_transcoded_request(
                http_options, request
            )

            body = _BaseSpacesServiceRestTransport._BaseEndActiveConference._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSpacesServiceRestTransport._BaseEndActiveConference._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.EndActiveConference",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "EndActiveConference",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._EndActiveConference._get_response(
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

    class _GetMember(
        _BaseSpacesServiceRestTransport._BaseGetMember, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.GetMember")

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
            request: service.GetMemberRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resource.Member:
            r"""Call the get member method over HTTP.

            Args:
                request (~.service.GetMemberRequest):
                    The request object. Request to get a member from a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resource.Member:
                    Users who are configured to have a
                role in the space. These users can join
                the space without knocking.

            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseGetMember._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_member(request, metadata)
            transcoded_request = (
                _BaseSpacesServiceRestTransport._BaseGetMember._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSpacesServiceRestTransport._BaseGetMember._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.GetMember",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "GetMember",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._GetMember._get_response(
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
            resp = resource.Member()
            pb_resp = resource.Member.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_member(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resource.Member.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.apps.meet_v2beta.SpacesServiceClient.get_member",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "GetMember",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSpace(
        _BaseSpacesServiceRestTransport._BaseGetSpace, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.GetSpace")

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
            request: service.GetSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resource.Space:
            r"""Call the get space method over HTTP.

            Args:
                request (~.service.GetSpaceRequest):
                    The request object. Request to get a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resource.Space:
                    Virtual place where conferences are
                held. Only one active conference can be
                held in one space at any given time.

            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseGetSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_space(request, metadata)
            transcoded_request = (
                _BaseSpacesServiceRestTransport._BaseGetSpace._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSpacesServiceRestTransport._BaseGetSpace._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.GetSpace",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "GetSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._GetSpace._get_response(
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
            resp = resource.Space()
            pb_resp = resource.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_space(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resource.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.apps.meet_v2beta.SpacesServiceClient.get_space",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "GetSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListMembers(
        _BaseSpacesServiceRestTransport._BaseListMembers, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.ListMembers")

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
            request: service.ListMembersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListMembersResponse:
            r"""Call the list members method over HTTP.

            Args:
                request (~.service.ListMembersRequest):
                    The request object. Request to list all members of a
                space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListMembersResponse:
                    Response of list members.
            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseListMembers._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_members(request, metadata)
            transcoded_request = _BaseSpacesServiceRestTransport._BaseListMembers._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseSpacesServiceRestTransport._BaseListMembers._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.ListMembers",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "ListMembers",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._ListMembers._get_response(
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
            resp = service.ListMembersResponse()
            pb_resp = service.ListMembersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_members(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListMembersResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.apps.meet_v2beta.SpacesServiceClient.list_members",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "ListMembers",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateSpace(
        _BaseSpacesServiceRestTransport._BaseUpdateSpace, SpacesServiceRestStub
    ):
        def __hash__(self):
            return hash("SpacesServiceRestTransport.UpdateSpace")

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
            request: service.UpdateSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resource.Space:
            r"""Call the update space method over HTTP.

            Args:
                request (~.service.UpdateSpaceRequest):
                    The request object. Request to update a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resource.Space:
                    Virtual place where conferences are
                held. Only one active conference can be
                held in one space at any given time.

            """

            http_options = (
                _BaseSpacesServiceRestTransport._BaseUpdateSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_space(request, metadata)
            transcoded_request = _BaseSpacesServiceRestTransport._BaseUpdateSpace._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseSpacesServiceRestTransport._BaseUpdateSpace._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSpacesServiceRestTransport._BaseUpdateSpace._get_query_params_json(
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
                    f"Sending request for google.apps.meet_v2beta.SpacesServiceClient.UpdateSpace",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "UpdateSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = SpacesServiceRestTransport._UpdateSpace._get_response(
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
            resp = resource.Space()
            pb_resp = resource.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_space(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resource.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.apps.meet_v2beta.SpacesServiceClient.update_space",
                    extra={
                        "serviceName": "google.apps.meet.v2beta.SpacesService",
                        "rpcName": "UpdateSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_member(self) -> Callable[[service.CreateMemberRequest], resource.Member]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMember(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_space(self) -> Callable[[service.CreateSpaceRequest], resource.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_member(self) -> Callable[[service.DeleteMemberRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMember(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def end_active_conference(
        self,
    ) -> Callable[[service.EndActiveConferenceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EndActiveConference(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_member(self) -> Callable[[service.GetMemberRequest], resource.Member]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMember(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_space(self) -> Callable[[service.GetSpaceRequest], resource.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_members(
        self,
    ) -> Callable[[service.ListMembersRequest], service.ListMembersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMembers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_space(self) -> Callable[[service.UpdateSpaceRequest], resource.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SpacesServiceRestTransport",)
