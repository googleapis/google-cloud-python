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
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.shopping.merchant_accounts_v1beta.types import user
from google.shopping.merchant_accounts_v1beta.types import user as gsma_user

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import UserServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class UserServiceRestInterceptor:
    """Interceptor for UserService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the UserServiceRestTransport.

    .. code-block:: python
        class MyCustomUserServiceInterceptor(UserServiceRestInterceptor):
            def pre_create_user(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_user(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_user(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_user(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_user(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_users(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_users(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_user(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_user(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = UserServiceRestTransport(interceptor=MyCustomUserServiceInterceptor())
        client = UserServiceClient(transport=transport)


    """

    def pre_create_user(
        self, request: gsma_user.CreateUserRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gsma_user.CreateUserRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_user

        Override in a subclass to manipulate the request or metadata
        before they are sent to the UserService server.
        """
        return request, metadata

    def post_create_user(self, response: gsma_user.User) -> gsma_user.User:
        """Post-rpc interceptor for create_user

        Override in a subclass to manipulate the response
        after it is returned by the UserService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_user(
        self, request: user.DeleteUserRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[user.DeleteUserRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_user

        Override in a subclass to manipulate the request or metadata
        before they are sent to the UserService server.
        """
        return request, metadata

    def pre_get_user(
        self, request: user.GetUserRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[user.GetUserRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_user

        Override in a subclass to manipulate the request or metadata
        before they are sent to the UserService server.
        """
        return request, metadata

    def post_get_user(self, response: user.User) -> user.User:
        """Post-rpc interceptor for get_user

        Override in a subclass to manipulate the response
        after it is returned by the UserService server but before
        it is returned to user code.
        """
        return response

    def pre_list_users(
        self, request: user.ListUsersRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[user.ListUsersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_users

        Override in a subclass to manipulate the request or metadata
        before they are sent to the UserService server.
        """
        return request, metadata

    def post_list_users(
        self, response: user.ListUsersResponse
    ) -> user.ListUsersResponse:
        """Post-rpc interceptor for list_users

        Override in a subclass to manipulate the response
        after it is returned by the UserService server but before
        it is returned to user code.
        """
        return response

    def pre_update_user(
        self, request: gsma_user.UpdateUserRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gsma_user.UpdateUserRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_user

        Override in a subclass to manipulate the request or metadata
        before they are sent to the UserService server.
        """
        return request, metadata

    def post_update_user(self, response: gsma_user.User) -> gsma_user.User:
        """Post-rpc interceptor for update_user

        Override in a subclass to manipulate the response
        after it is returned by the UserService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class UserServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: UserServiceRestInterceptor


class UserServiceRestTransport(UserServiceTransport):
    """REST backend transport for UserService.

    Service to support user API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[UserServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        self._interceptor = interceptor or UserServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateUser(UserServiceRestStub):
        def __hash__(self):
            return hash("CreateUser")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "userId": "",
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
            request: gsma_user.CreateUserRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsma_user.User:
            r"""Call the create user method over HTTP.

            Args:
                request (~.gsma_user.CreateUserRequest):
                    The request object. Request message for the ``CreateUser`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsma_user.User:
                    A
                `user <https://support.google.com/merchants/answer/12160472>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/accounts/v1beta/{parent=accounts/*}/users",
                    "body": "user",
                },
            ]
            request, metadata = self._interceptor.pre_create_user(request, metadata)
            pb_request = gsma_user.CreateUserRequest.pb(request)
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
            resp = gsma_user.User()
            pb_resp = gsma_user.User.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_user(resp)
            return resp

    class _DeleteUser(UserServiceRestStub):
        def __hash__(self):
            return hash("DeleteUser")

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
            request: user.DeleteUserRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete user method over HTTP.

            Args:
                request (~.user.DeleteUserRequest):
                    The request object. Request message for the ``DeleteUser`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/accounts/v1beta/{name=accounts/*/users/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_user(request, metadata)
            pb_request = user.DeleteUserRequest.pb(request)
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

    class _GetUser(UserServiceRestStub):
        def __hash__(self):
            return hash("GetUser")

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
            request: user.GetUserRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> user.User:
            r"""Call the get user method over HTTP.

            Args:
                request (~.user.GetUserRequest):
                    The request object. Request message for the ``GetUser`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.user.User:
                    A
                `user <https://support.google.com/merchants/answer/12160472>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/accounts/v1beta/{name=accounts/*/users/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_user(request, metadata)
            pb_request = user.GetUserRequest.pb(request)
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
            resp = user.User()
            pb_resp = user.User.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_user(resp)
            return resp

    class _ListUsers(UserServiceRestStub):
        def __hash__(self):
            return hash("ListUsers")

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
            request: user.ListUsersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> user.ListUsersResponse:
            r"""Call the list users method over HTTP.

            Args:
                request (~.user.ListUsersRequest):
                    The request object. Request message for the ``ListUsers`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.user.ListUsersResponse:
                    Response message for the ``ListUsers`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/accounts/v1beta/{parent=accounts/*}/users",
                },
            ]
            request, metadata = self._interceptor.pre_list_users(request, metadata)
            pb_request = user.ListUsersRequest.pb(request)
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
            resp = user.ListUsersResponse()
            pb_resp = user.ListUsersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_users(resp)
            return resp

    class _UpdateUser(UserServiceRestStub):
        def __hash__(self):
            return hash("UpdateUser")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: gsma_user.UpdateUserRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsma_user.User:
            r"""Call the update user method over HTTP.

            Args:
                request (~.gsma_user.UpdateUserRequest):
                    The request object. Request message for the ``UpdateUser`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsma_user.User:
                    A
                `user <https://support.google.com/merchants/answer/12160472>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/accounts/v1beta/{user.name=accounts/*/users/*}",
                    "body": "user",
                },
            ]
            request, metadata = self._interceptor.pre_update_user(request, metadata)
            pb_request = gsma_user.UpdateUserRequest.pb(request)
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
            resp = gsma_user.User()
            pb_resp = gsma_user.User.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_user(resp)
            return resp

    @property
    def create_user(self) -> Callable[[gsma_user.CreateUserRequest], gsma_user.User]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateUser(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_user(self) -> Callable[[user.DeleteUserRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteUser(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_user(self) -> Callable[[user.GetUserRequest], user.User]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetUser(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_users(self) -> Callable[[user.ListUsersRequest], user.ListUsersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUsers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_user(self) -> Callable[[gsma_user.UpdateUserRequest], gsma_user.User]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateUser(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("UserServiceRestTransport",)
