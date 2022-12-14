# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.network_security_v1.types import (
    authorization_policy as gcn_authorization_policy,
)
from google.cloud.network_security_v1.types import (
    client_tls_policy as gcn_client_tls_policy,
)
from google.cloud.network_security_v1.types import (
    server_tls_policy as gcn_server_tls_policy,
)
from google.cloud.network_security_v1.types import authorization_policy
from google.cloud.network_security_v1.types import client_tls_policy
from google.cloud.network_security_v1.types import server_tls_policy

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import NetworkSecurityTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class NetworkSecurityRestInterceptor:
    """Interceptor for NetworkSecurity.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the NetworkSecurityRestTransport.

    .. code-block:: python
        class MyCustomNetworkSecurityInterceptor(NetworkSecurityRestInterceptor):
            def pre_create_authorization_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_authorization_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_client_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_client_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_server_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_server_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_authorization_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_authorization_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_client_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_client_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_server_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_server_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_authorization_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_authorization_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_client_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_client_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_server_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_server_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_authorization_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_authorization_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_client_tls_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_client_tls_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_server_tls_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_server_tls_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_authorization_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_authorization_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_client_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_client_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_server_tls_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_server_tls_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = NetworkSecurityRestTransport(interceptor=MyCustomNetworkSecurityInterceptor())
        client = NetworkSecurityClient(transport=transport)


    """

    def pre_create_authorization_policy(
        self,
        request: gcn_authorization_policy.CreateAuthorizationPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_authorization_policy.CreateAuthorizationPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_authorization_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_create_authorization_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_authorization_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_create_client_tls_policy(
        self,
        request: gcn_client_tls_policy.CreateClientTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_client_tls_policy.CreateClientTlsPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_client_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_create_client_tls_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_client_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_create_server_tls_policy(
        self,
        request: gcn_server_tls_policy.CreateServerTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_server_tls_policy.CreateServerTlsPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_server_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_create_server_tls_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_server_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_delete_authorization_policy(
        self,
        request: authorization_policy.DeleteAuthorizationPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        authorization_policy.DeleteAuthorizationPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_authorization_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_delete_authorization_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_authorization_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_delete_client_tls_policy(
        self,
        request: client_tls_policy.DeleteClientTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        client_tls_policy.DeleteClientTlsPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_client_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_delete_client_tls_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_client_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_delete_server_tls_policy(
        self,
        request: server_tls_policy.DeleteServerTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        server_tls_policy.DeleteServerTlsPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_server_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_delete_server_tls_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_server_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_get_authorization_policy(
        self,
        request: authorization_policy.GetAuthorizationPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        authorization_policy.GetAuthorizationPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_authorization_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_get_authorization_policy(
        self, response: authorization_policy.AuthorizationPolicy
    ) -> authorization_policy.AuthorizationPolicy:
        """Post-rpc interceptor for get_authorization_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_get_client_tls_policy(
        self,
        request: client_tls_policy.GetClientTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[client_tls_policy.GetClientTlsPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_client_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_get_client_tls_policy(
        self, response: client_tls_policy.ClientTlsPolicy
    ) -> client_tls_policy.ClientTlsPolicy:
        """Post-rpc interceptor for get_client_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_get_server_tls_policy(
        self,
        request: server_tls_policy.GetServerTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[server_tls_policy.GetServerTlsPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_server_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_get_server_tls_policy(
        self, response: server_tls_policy.ServerTlsPolicy
    ) -> server_tls_policy.ServerTlsPolicy:
        """Post-rpc interceptor for get_server_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_list_authorization_policies(
        self,
        request: authorization_policy.ListAuthorizationPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        authorization_policy.ListAuthorizationPoliciesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_authorization_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_list_authorization_policies(
        self, response: authorization_policy.ListAuthorizationPoliciesResponse
    ) -> authorization_policy.ListAuthorizationPoliciesResponse:
        """Post-rpc interceptor for list_authorization_policies

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_list_client_tls_policies(
        self,
        request: client_tls_policy.ListClientTlsPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        client_tls_policy.ListClientTlsPoliciesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_client_tls_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_list_client_tls_policies(
        self, response: client_tls_policy.ListClientTlsPoliciesResponse
    ) -> client_tls_policy.ListClientTlsPoliciesResponse:
        """Post-rpc interceptor for list_client_tls_policies

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_list_server_tls_policies(
        self,
        request: server_tls_policy.ListServerTlsPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        server_tls_policy.ListServerTlsPoliciesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_server_tls_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_list_server_tls_policies(
        self, response: server_tls_policy.ListServerTlsPoliciesResponse
    ) -> server_tls_policy.ListServerTlsPoliciesResponse:
        """Post-rpc interceptor for list_server_tls_policies

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_update_authorization_policy(
        self,
        request: gcn_authorization_policy.UpdateAuthorizationPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_authorization_policy.UpdateAuthorizationPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_authorization_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_update_authorization_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_authorization_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_update_client_tls_policy(
        self,
        request: gcn_client_tls_policy.UpdateClientTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_client_tls_policy.UpdateClientTlsPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_client_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_update_client_tls_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_client_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response

    def pre_update_server_tls_policy(
        self,
        request: gcn_server_tls_policy.UpdateServerTlsPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_server_tls_policy.UpdateServerTlsPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_server_tls_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkSecurity server.
        """
        return request, metadata

    def post_update_server_tls_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_server_tls_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkSecurity server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class NetworkSecurityRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: NetworkSecurityRestInterceptor


class NetworkSecurityRestTransport(NetworkSecurityTransport):
    """REST backend transport for NetworkSecurity.

    Network Security API provides resources to configure
    authentication and authorization policies. Refer to per API
    resource documentation for more information.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "networksecurity.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[NetworkSecurityRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or NetworkSecurityRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {}

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

    class _CreateAuthorizationPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("CreateAuthorizationPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "authorizationPolicyId": "",
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
            request: gcn_authorization_policy.CreateAuthorizationPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create authorization
            policy method over HTTP.

                Args:
                    request (~.gcn_authorization_policy.CreateAuthorizationPolicyRequest):
                        The request object. Request used by the
                    CreateAuthorizationPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/authorizationPolicies",
                    "body": "authorization_policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_authorization_policy(
                request, metadata
            )
            pb_request = gcn_authorization_policy.CreateAuthorizationPolicyRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_authorization_policy(resp)
            return resp

    class _CreateClientTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("CreateClientTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "clientTlsPolicyId": "",
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
            request: gcn_client_tls_policy.CreateClientTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create client tls policy method over HTTP.

            Args:
                request (~.gcn_client_tls_policy.CreateClientTlsPolicyRequest):
                    The request object. Request used by the
                CreateClientTlsPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/clientTlsPolicies",
                    "body": "client_tls_policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_client_tls_policy(
                request, metadata
            )
            pb_request = gcn_client_tls_policy.CreateClientTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_client_tls_policy(resp)
            return resp

    class _CreateServerTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("CreateServerTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "serverTlsPolicyId": "",
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
            request: gcn_server_tls_policy.CreateServerTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create server tls policy method over HTTP.

            Args:
                request (~.gcn_server_tls_policy.CreateServerTlsPolicyRequest):
                    The request object. Request used by the
                CreateServerTlsPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/serverTlsPolicies",
                    "body": "server_tls_policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_server_tls_policy(
                request, metadata
            )
            pb_request = gcn_server_tls_policy.CreateServerTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_server_tls_policy(resp)
            return resp

    class _DeleteAuthorizationPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("DeleteAuthorizationPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: authorization_policy.DeleteAuthorizationPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete authorization
            policy method over HTTP.

                Args:
                    request (~.authorization_policy.DeleteAuthorizationPolicyRequest):
                        The request object. Request used by the
                    DeleteAuthorizationPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/authorizationPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_authorization_policy(
                request, metadata
            )
            pb_request = authorization_policy.DeleteAuthorizationPolicyRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_authorization_policy(resp)
            return resp

    class _DeleteClientTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("DeleteClientTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: client_tls_policy.DeleteClientTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete client tls policy method over HTTP.

            Args:
                request (~.client_tls_policy.DeleteClientTlsPolicyRequest):
                    The request object. Request used by the
                DeleteClientTlsPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/clientTlsPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_client_tls_policy(
                request, metadata
            )
            pb_request = client_tls_policy.DeleteClientTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_client_tls_policy(resp)
            return resp

    class _DeleteServerTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("DeleteServerTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: server_tls_policy.DeleteServerTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete server tls policy method over HTTP.

            Args:
                request (~.server_tls_policy.DeleteServerTlsPolicyRequest):
                    The request object. Request used by the
                DeleteServerTlsPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/serverTlsPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_server_tls_policy(
                request, metadata
            )
            pb_request = server_tls_policy.DeleteServerTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_server_tls_policy(resp)
            return resp

    class _GetAuthorizationPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("GetAuthorizationPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: authorization_policy.GetAuthorizationPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> authorization_policy.AuthorizationPolicy:
            r"""Call the get authorization policy method over HTTP.

            Args:
                request (~.authorization_policy.GetAuthorizationPolicyRequest):
                    The request object. Request used by the
                GetAuthorizationPolicy method.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.authorization_policy.AuthorizationPolicy:
                    AuthorizationPolicy is a resource
                that specifies how a server should
                authorize incoming connections. This
                resource in itself does not change the
                configuration unless it's attached to a
                target https proxy or endpoint config
                selector resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/authorizationPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_authorization_policy(
                request, metadata
            )
            pb_request = authorization_policy.GetAuthorizationPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = authorization_policy.AuthorizationPolicy()
            pb_resp = authorization_policy.AuthorizationPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_authorization_policy(resp)
            return resp

    class _GetClientTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("GetClientTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: client_tls_policy.GetClientTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> client_tls_policy.ClientTlsPolicy:
            r"""Call the get client tls policy method over HTTP.

            Args:
                request (~.client_tls_policy.GetClientTlsPolicyRequest):
                    The request object. Request used by the
                GetClientTlsPolicy method.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.client_tls_policy.ClientTlsPolicy:
                    ClientTlsPolicy is a resource that
                specifies how a client should
                authenticate connections to backends of
                a service. This resource itself does not
                affect configuration unless it is
                attached to a backend service resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/clientTlsPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_client_tls_policy(
                request, metadata
            )
            pb_request = client_tls_policy.GetClientTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = client_tls_policy.ClientTlsPolicy()
            pb_resp = client_tls_policy.ClientTlsPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_client_tls_policy(resp)
            return resp

    class _GetServerTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("GetServerTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: server_tls_policy.GetServerTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> server_tls_policy.ServerTlsPolicy:
            r"""Call the get server tls policy method over HTTP.

            Args:
                request (~.server_tls_policy.GetServerTlsPolicyRequest):
                    The request object. Request used by the
                GetServerTlsPolicy method.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.server_tls_policy.ServerTlsPolicy:
                    ServerTlsPolicy is a resource that
                specifies how a server should
                authenticate incoming requests. This
                resource itself does not affect
                configuration unless it is attached to a
                target https proxy or endpoint config
                selector resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/serverTlsPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_server_tls_policy(
                request, metadata
            )
            pb_request = server_tls_policy.GetServerTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = server_tls_policy.ServerTlsPolicy()
            pb_resp = server_tls_policy.ServerTlsPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_server_tls_policy(resp)
            return resp

    class _ListAuthorizationPolicies(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("ListAuthorizationPolicies")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: authorization_policy.ListAuthorizationPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> authorization_policy.ListAuthorizationPoliciesResponse:
            r"""Call the list authorization
            policies method over HTTP.

                Args:
                    request (~.authorization_policy.ListAuthorizationPoliciesRequest):
                        The request object. Request used with the
                    ListAuthorizationPolicies method.

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.authorization_policy.ListAuthorizationPoliciesResponse:
                        Response returned by the
                    ListAuthorizationPolicies method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/authorizationPolicies",
                },
            ]
            request, metadata = self._interceptor.pre_list_authorization_policies(
                request, metadata
            )
            pb_request = authorization_policy.ListAuthorizationPoliciesRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = authorization_policy.ListAuthorizationPoliciesResponse()
            pb_resp = authorization_policy.ListAuthorizationPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_authorization_policies(resp)
            return resp

    class _ListClientTlsPolicies(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("ListClientTlsPolicies")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: client_tls_policy.ListClientTlsPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> client_tls_policy.ListClientTlsPoliciesResponse:
            r"""Call the list client tls policies method over HTTP.

            Args:
                request (~.client_tls_policy.ListClientTlsPoliciesRequest):
                    The request object. Request used by the
                ListClientTlsPolicies method.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.client_tls_policy.ListClientTlsPoliciesResponse:
                    Response returned by the
                ListClientTlsPolicies method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/clientTlsPolicies",
                },
            ]
            request, metadata = self._interceptor.pre_list_client_tls_policies(
                request, metadata
            )
            pb_request = client_tls_policy.ListClientTlsPoliciesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = client_tls_policy.ListClientTlsPoliciesResponse()
            pb_resp = client_tls_policy.ListClientTlsPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_client_tls_policies(resp)
            return resp

    class _ListServerTlsPolicies(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("ListServerTlsPolicies")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: server_tls_policy.ListServerTlsPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> server_tls_policy.ListServerTlsPoliciesResponse:
            r"""Call the list server tls policies method over HTTP.

            Args:
                request (~.server_tls_policy.ListServerTlsPoliciesRequest):
                    The request object. Request used by the
                ListServerTlsPolicies method.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.server_tls_policy.ListServerTlsPoliciesResponse:
                    Response returned by the
                ListServerTlsPolicies method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/serverTlsPolicies",
                },
            ]
            request, metadata = self._interceptor.pre_list_server_tls_policies(
                request, metadata
            )
            pb_request = server_tls_policy.ListServerTlsPoliciesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = server_tls_policy.ListServerTlsPoliciesResponse()
            pb_resp = server_tls_policy.ListServerTlsPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_server_tls_policies(resp)
            return resp

    class _UpdateAuthorizationPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("UpdateAuthorizationPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_authorization_policy.UpdateAuthorizationPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update authorization
            policy method over HTTP.

                Args:
                    request (~.gcn_authorization_policy.UpdateAuthorizationPolicyRequest):
                        The request object. Request used by the
                    UpdateAuthorizationPolicy method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{authorization_policy.name=projects/*/locations/*/authorizationPolicies/*}",
                    "body": "authorization_policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_authorization_policy(
                request, metadata
            )
            pb_request = gcn_authorization_policy.UpdateAuthorizationPolicyRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_authorization_policy(resp)
            return resp

    class _UpdateClientTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("UpdateClientTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_client_tls_policy.UpdateClientTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update client tls policy method over HTTP.

            Args:
                request (~.gcn_client_tls_policy.UpdateClientTlsPolicyRequest):
                    The request object. Request used by UpdateClientTlsPolicy
                method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{client_tls_policy.name=projects/*/locations/*/clientTlsPolicies/*}",
                    "body": "client_tls_policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_client_tls_policy(
                request, metadata
            )
            pb_request = gcn_client_tls_policy.UpdateClientTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_client_tls_policy(resp)
            return resp

    class _UpdateServerTlsPolicy(NetworkSecurityRestStub):
        def __hash__(self):
            return hash("UpdateServerTlsPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_server_tls_policy.UpdateServerTlsPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update server tls policy method over HTTP.

            Args:
                request (~.gcn_server_tls_policy.UpdateServerTlsPolicyRequest):
                    The request object. Request used by UpdateServerTlsPolicy
                method.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{server_tls_policy.name=projects/*/locations/*/serverTlsPolicies/*}",
                    "body": "server_tls_policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_server_tls_policy(
                request, metadata
            )
            pb_request = gcn_server_tls_policy.UpdateServerTlsPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_server_tls_policy(resp)
            return resp

    @property
    def create_authorization_policy(
        self,
    ) -> Callable[
        [gcn_authorization_policy.CreateAuthorizationPolicyRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAuthorizationPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_client_tls_policy(
        self,
    ) -> Callable[
        [gcn_client_tls_policy.CreateClientTlsPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateClientTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_server_tls_policy(
        self,
    ) -> Callable[
        [gcn_server_tls_policy.CreateServerTlsPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateServerTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_authorization_policy(
        self,
    ) -> Callable[
        [authorization_policy.DeleteAuthorizationPolicyRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAuthorizationPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_client_tls_policy(
        self,
    ) -> Callable[
        [client_tls_policy.DeleteClientTlsPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteClientTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_server_tls_policy(
        self,
    ) -> Callable[
        [server_tls_policy.DeleteServerTlsPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteServerTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_authorization_policy(
        self,
    ) -> Callable[
        [authorization_policy.GetAuthorizationPolicyRequest],
        authorization_policy.AuthorizationPolicy,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAuthorizationPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_client_tls_policy(
        self,
    ) -> Callable[
        [client_tls_policy.GetClientTlsPolicyRequest], client_tls_policy.ClientTlsPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetClientTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_server_tls_policy(
        self,
    ) -> Callable[
        [server_tls_policy.GetServerTlsPolicyRequest], server_tls_policy.ServerTlsPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServerTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_authorization_policies(
        self,
    ) -> Callable[
        [authorization_policy.ListAuthorizationPoliciesRequest],
        authorization_policy.ListAuthorizationPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAuthorizationPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_client_tls_policies(
        self,
    ) -> Callable[
        [client_tls_policy.ListClientTlsPoliciesRequest],
        client_tls_policy.ListClientTlsPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClientTlsPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_server_tls_policies(
        self,
    ) -> Callable[
        [server_tls_policy.ListServerTlsPoliciesRequest],
        server_tls_policy.ListServerTlsPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServerTlsPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_authorization_policy(
        self,
    ) -> Callable[
        [gcn_authorization_policy.UpdateAuthorizationPolicyRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAuthorizationPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_client_tls_policy(
        self,
    ) -> Callable[
        [gcn_client_tls_policy.UpdateClientTlsPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateClientTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_server_tls_policy(
        self,
    ) -> Callable[
        [gcn_server_tls_policy.UpdateServerTlsPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateServerTlsPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("NetworkSecurityRestTransport",)
