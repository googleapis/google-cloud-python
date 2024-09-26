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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore
from google.shopping.merchant_accounts_v1beta.types import accounts

from .base import AccountsServiceTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AccountsServiceRestInterceptor:
    """Interceptor for AccountsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AccountsServiceRestTransport.

    .. code-block:: python
        class MyCustomAccountsServiceInterceptor(AccountsServiceRestInterceptor):
            def pre_create_and_configure_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_and_configure_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_accounts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_accounts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sub_accounts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sub_accounts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_account(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AccountsServiceRestTransport(interceptor=MyCustomAccountsServiceInterceptor())
        client = AccountsServiceClient(transport=transport)


    """
    def pre_create_and_configure_account(self, request: accounts.CreateAndConfigureAccountRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[accounts.CreateAndConfigureAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_and_configure_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccountsService server.
        """
        return request, metadata

    def post_create_and_configure_account(self, response: accounts.Account) -> accounts.Account:
        """Post-rpc interceptor for create_and_configure_account

        Override in a subclass to manipulate the response
        after it is returned by the AccountsService server but before
        it is returned to user code.
        """
        return response
    def pre_delete_account(self, request: accounts.DeleteAccountRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[accounts.DeleteAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccountsService server.
        """
        return request, metadata

    def pre_get_account(self, request: accounts.GetAccountRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[accounts.GetAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccountsService server.
        """
        return request, metadata

    def post_get_account(self, response: accounts.Account) -> accounts.Account:
        """Post-rpc interceptor for get_account

        Override in a subclass to manipulate the response
        after it is returned by the AccountsService server but before
        it is returned to user code.
        """
        return response
    def pre_list_accounts(self, request: accounts.ListAccountsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[accounts.ListAccountsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_accounts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccountsService server.
        """
        return request, metadata

    def post_list_accounts(self, response: accounts.ListAccountsResponse) -> accounts.ListAccountsResponse:
        """Post-rpc interceptor for list_accounts

        Override in a subclass to manipulate the response
        after it is returned by the AccountsService server but before
        it is returned to user code.
        """
        return response
    def pre_list_sub_accounts(self, request: accounts.ListSubAccountsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[accounts.ListSubAccountsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sub_accounts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccountsService server.
        """
        return request, metadata

    def post_list_sub_accounts(self, response: accounts.ListSubAccountsResponse) -> accounts.ListSubAccountsResponse:
        """Post-rpc interceptor for list_sub_accounts

        Override in a subclass to manipulate the response
        after it is returned by the AccountsService server but before
        it is returned to user code.
        """
        return response
    def pre_update_account(self, request: accounts.UpdateAccountRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[accounts.UpdateAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccountsService server.
        """
        return request, metadata

    def post_update_account(self, response: accounts.Account) -> accounts.Account:
        """Post-rpc interceptor for update_account

        Override in a subclass to manipulate the response
        after it is returned by the AccountsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AccountsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AccountsServiceRestInterceptor


class AccountsServiceRestTransport(AccountsServiceTransport):
    """REST backend transport for AccountsService.

    Service to support Accounts API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(self, *,
            host: str = 'merchantapi.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[AccountsServiceRestInterceptor] = None,
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
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or AccountsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateAndConfigureAccount(AccountsServiceRestStub):
        def __hash__(self):
            return hash("CreateAndConfigureAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: accounts.CreateAndConfigureAccountRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> accounts.Account:
            r"""Call the create and configure
        account method over HTTP.

            Args:
                request (~.accounts.CreateAndConfigureAccountRequest):
                    The request object. Request message for the ``CreateAndConfigureAccount``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accounts.Account:
                    An account.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/accounts/v1beta/accounts:createAndConfigure',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_create_and_configure_account(request, metadata)
            pb_request = accounts.CreateAndConfigureAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = accounts.Account()
            pb_resp = accounts.Account.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_and_configure_account(resp)
            return resp

    class _DeleteAccount(AccountsServiceRestStub):
        def __hash__(self):
            return hash("DeleteAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: accounts.DeleteAccountRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the delete account method over HTTP.

            Args:
                request (~.accounts.DeleteAccountRequest):
                    The request object. Request message for the ``DeleteAccount`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/accounts/v1beta/{name=accounts/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_account(request, metadata)
            pb_request = accounts.DeleteAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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

    class _GetAccount(AccountsServiceRestStub):
        def __hash__(self):
            return hash("GetAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: accounts.GetAccountRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> accounts.Account:
            r"""Call the get account method over HTTP.

            Args:
                request (~.accounts.GetAccountRequest):
                    The request object. Request message for the ``GetAccount`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accounts.Account:
                    An account.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/accounts/v1beta/{name=accounts/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_account(request, metadata)
            pb_request = accounts.GetAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = accounts.Account()
            pb_resp = accounts.Account.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_account(resp)
            return resp

    class _ListAccounts(AccountsServiceRestStub):
        def __hash__(self):
            return hash("ListAccounts")

        def __call__(self,
                request: accounts.ListAccountsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> accounts.ListAccountsResponse:
            r"""Call the list accounts method over HTTP.

            Args:
                request (~.accounts.ListAccountsRequest):
                    The request object. Request message for the ``ListAccounts`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accounts.ListAccountsResponse:
                    Response message for the ``ListAccounts`` method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/accounts/v1beta/accounts',
            },
            ]
            request, metadata = self._interceptor.pre_list_accounts(request, metadata)
            pb_request = accounts.ListAccountsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = accounts.ListAccountsResponse()
            pb_resp = accounts.ListAccountsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_accounts(resp)
            return resp

    class _ListSubAccounts(AccountsServiceRestStub):
        def __hash__(self):
            return hash("ListSubAccounts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: accounts.ListSubAccountsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> accounts.ListSubAccountsResponse:
            r"""Call the list sub accounts method over HTTP.

            Args:
                request (~.accounts.ListSubAccountsRequest):
                    The request object. Request message for the ``ListSubAccounts`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accounts.ListSubAccountsResponse:
                    Response message for the ``ListSubAccounts`` method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/accounts/v1beta/{provider=accounts/*}:listSubaccounts',
            },
            ]
            request, metadata = self._interceptor.pre_list_sub_accounts(request, metadata)
            pb_request = accounts.ListSubAccountsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = accounts.ListSubAccountsResponse()
            pb_resp = accounts.ListSubAccountsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sub_accounts(resp)
            return resp

    class _UpdateAccount(AccountsServiceRestStub):
        def __hash__(self):
            return hash("UpdateAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "updateMask" : {},        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: accounts.UpdateAccountRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> accounts.Account:
            r"""Call the update account method over HTTP.

            Args:
                request (~.accounts.UpdateAccountRequest):
                    The request object. Request message for the ``UpdateAccount`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accounts.Account:
                    An account.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/accounts/v1beta/{account.name=accounts/*}',
                'body': 'account',
            },
            ]
            request, metadata = self._interceptor.pre_update_account(request, metadata)
            pb_request = accounts.UpdateAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = accounts.Account()
            pb_resp = accounts.Account.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_account(resp)
            return resp

    @property
    def create_and_configure_account(self) -> Callable[
            [accounts.CreateAndConfigureAccountRequest],
            accounts.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAndConfigureAccount(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_account(self) -> Callable[
            [accounts.DeleteAccountRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccount(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_account(self) -> Callable[
            [accounts.GetAccountRequest],
            accounts.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccount(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_accounts(self) -> Callable[
            [accounts.ListAccountsRequest],
            accounts.ListAccountsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccounts(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_sub_accounts(self) -> Callable[
            [accounts.ListSubAccountsRequest],
            accounts.ListSubAccountsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSubAccounts(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_account(self) -> Callable[
            [accounts.UpdateAccountRequest],
            accounts.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccount(self._session, self._host, self._interceptor) # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'AccountsServiceRestTransport',
)
