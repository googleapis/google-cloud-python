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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore

from google.cloud.kms_v1.types import ekm_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import EkmServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class EkmServiceRestInterceptor:
    """Interceptor for EkmService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EkmServiceRestTransport.

    .. code-block:: python
        class MyCustomEkmServiceInterceptor(EkmServiceRestInterceptor):
            def pre_create_ekm_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_ekm_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_ekm_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ekm_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_ekm_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ekm_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_ekm_connections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_ekm_connections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_ekm_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_ekm_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_ekm_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_ekm_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_verify_connectivity(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_verify_connectivity(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EkmServiceRestTransport(interceptor=MyCustomEkmServiceInterceptor())
        client = EkmServiceClient(transport=transport)


    """

    def pre_create_ekm_connection(
        self,
        request: ekm_service.CreateEkmConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.CreateEkmConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_ekm_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_create_ekm_connection(
        self, response: ekm_service.EkmConnection
    ) -> ekm_service.EkmConnection:
        """Post-rpc interceptor for create_ekm_connection

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_get_ekm_config(
        self,
        request: ekm_service.GetEkmConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.GetEkmConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ekm_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_get_ekm_config(
        self, response: ekm_service.EkmConfig
    ) -> ekm_service.EkmConfig:
        """Post-rpc interceptor for get_ekm_config

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_get_ekm_connection(
        self,
        request: ekm_service.GetEkmConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.GetEkmConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ekm_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_get_ekm_connection(
        self, response: ekm_service.EkmConnection
    ) -> ekm_service.EkmConnection:
        """Post-rpc interceptor for get_ekm_connection

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_list_ekm_connections(
        self,
        request: ekm_service.ListEkmConnectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.ListEkmConnectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_ekm_connections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_list_ekm_connections(
        self, response: ekm_service.ListEkmConnectionsResponse
    ) -> ekm_service.ListEkmConnectionsResponse:
        """Post-rpc interceptor for list_ekm_connections

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_update_ekm_config(
        self,
        request: ekm_service.UpdateEkmConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.UpdateEkmConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_ekm_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_update_ekm_config(
        self, response: ekm_service.EkmConfig
    ) -> ekm_service.EkmConfig:
        """Post-rpc interceptor for update_ekm_config

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_update_ekm_connection(
        self,
        request: ekm_service.UpdateEkmConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.UpdateEkmConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_ekm_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_update_ekm_connection(
        self, response: ekm_service.EkmConnection
    ) -> ekm_service.EkmConnection:
        """Post-rpc interceptor for update_ekm_connection

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_verify_connectivity(
        self,
        request: ekm_service.VerifyConnectivityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_service.VerifyConnectivityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for verify_connectivity

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_verify_connectivity(
        self, response: ekm_service.VerifyConnectivityResponse
    ) -> ekm_service.VerifyConnectivityResponse:
        """Post-rpc interceptor for verify_connectivity

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
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
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
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
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
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
        before they are sent to the EkmService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the EkmService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EkmServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EkmServiceRestInterceptor


class EkmServiceRestTransport(EkmServiceTransport):
    """REST backend transport for EkmService.

    Google Cloud Key Management EKM Service

    Manages external cryptographic keys and operations using those keys.
    Implements a REST model with the following objects:

    -  [EkmConnection][google.cloud.kms.v1.EkmConnection]

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudkms.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[EkmServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudkms.googleapis.com').
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
        self._interceptor = interceptor or EkmServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateEkmConnection(EkmServiceRestStub):
        def __hash__(self):
            return hash("CreateEkmConnection")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "ekmConnectionId": "",
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
            request: ekm_service.CreateEkmConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.EkmConnection:
            r"""Call the create ekm connection method over HTTP.

            Args:
                request (~.ekm_service.CreateEkmConnectionRequest):
                    The request object. Request message for
                [EkmService.CreateEkmConnection][google.cloud.kms.v1.EkmService.CreateEkmConnection].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.EkmConnection:
                    An [EkmConnection][google.cloud.kms.v1.EkmConnection]
                represents an individual EKM connection. It can be used
                for creating [CryptoKeys][google.cloud.kms.v1.CryptoKey]
                and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                with a
                [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                of
                [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
                as well as performing cryptographic operations using
                keys created within the
                [EkmConnection][google.cloud.kms.v1.EkmConnection].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/ekmConnections",
                    "body": "ekm_connection",
                },
            ]
            request, metadata = self._interceptor.pre_create_ekm_connection(
                request, metadata
            )
            pb_request = ekm_service.CreateEkmConnectionRequest.pb(request)
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
            resp = ekm_service.EkmConnection()
            pb_resp = ekm_service.EkmConnection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_ekm_connection(resp)
            return resp

    class _GetEkmConfig(EkmServiceRestStub):
        def __hash__(self):
            return hash("GetEkmConfig")

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
            request: ekm_service.GetEkmConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.EkmConfig:
            r"""Call the get ekm config method over HTTP.

            Args:
                request (~.ekm_service.GetEkmConfigRequest):
                    The request object. Request message for
                [EkmService.GetEkmConfig][google.cloud.kms.v1.EkmService.GetEkmConfig].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.EkmConfig:
                    An [EkmConfig][google.cloud.kms.v1.EkmConfig] is a
                singleton resource that represents configuration
                parameters that apply to all
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                with a
                [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                of
                [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC]
                in a given project and location.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/ekmConfig}",
                },
            ]
            request, metadata = self._interceptor.pre_get_ekm_config(request, metadata)
            pb_request = ekm_service.GetEkmConfigRequest.pb(request)
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
            resp = ekm_service.EkmConfig()
            pb_resp = ekm_service.EkmConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ekm_config(resp)
            return resp

    class _GetEkmConnection(EkmServiceRestStub):
        def __hash__(self):
            return hash("GetEkmConnection")

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
            request: ekm_service.GetEkmConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.EkmConnection:
            r"""Call the get ekm connection method over HTTP.

            Args:
                request (~.ekm_service.GetEkmConnectionRequest):
                    The request object. Request message for
                [EkmService.GetEkmConnection][google.cloud.kms.v1.EkmService.GetEkmConnection].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.EkmConnection:
                    An [EkmConnection][google.cloud.kms.v1.EkmConnection]
                represents an individual EKM connection. It can be used
                for creating [CryptoKeys][google.cloud.kms.v1.CryptoKey]
                and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                with a
                [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                of
                [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
                as well as performing cryptographic operations using
                keys created within the
                [EkmConnection][google.cloud.kms.v1.EkmConnection].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/ekmConnections/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_ekm_connection(
                request, metadata
            )
            pb_request = ekm_service.GetEkmConnectionRequest.pb(request)
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
            resp = ekm_service.EkmConnection()
            pb_resp = ekm_service.EkmConnection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ekm_connection(resp)
            return resp

    class _ListEkmConnections(EkmServiceRestStub):
        def __hash__(self):
            return hash("ListEkmConnections")

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
            request: ekm_service.ListEkmConnectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.ListEkmConnectionsResponse:
            r"""Call the list ekm connections method over HTTP.

            Args:
                request (~.ekm_service.ListEkmConnectionsRequest):
                    The request object. Request message for
                [EkmService.ListEkmConnections][google.cloud.kms.v1.EkmService.ListEkmConnections].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.ListEkmConnectionsResponse:
                    Response message for
                [EkmService.ListEkmConnections][google.cloud.kms.v1.EkmService.ListEkmConnections].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/ekmConnections",
                },
            ]
            request, metadata = self._interceptor.pre_list_ekm_connections(
                request, metadata
            )
            pb_request = ekm_service.ListEkmConnectionsRequest.pb(request)
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
            resp = ekm_service.ListEkmConnectionsResponse()
            pb_resp = ekm_service.ListEkmConnectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_ekm_connections(resp)
            return resp

    class _UpdateEkmConfig(EkmServiceRestStub):
        def __hash__(self):
            return hash("UpdateEkmConfig")

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
            request: ekm_service.UpdateEkmConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.EkmConfig:
            r"""Call the update ekm config method over HTTP.

            Args:
                request (~.ekm_service.UpdateEkmConfigRequest):
                    The request object. Request message for
                [EkmService.UpdateEkmConfig][google.cloud.kms.v1.EkmService.UpdateEkmConfig].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.EkmConfig:
                    An [EkmConfig][google.cloud.kms.v1.EkmConfig] is a
                singleton resource that represents configuration
                parameters that apply to all
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                with a
                [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                of
                [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC]
                in a given project and location.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{ekm_config.name=projects/*/locations/*/ekmConfig}",
                    "body": "ekm_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_ekm_config(
                request, metadata
            )
            pb_request = ekm_service.UpdateEkmConfigRequest.pb(request)
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
            resp = ekm_service.EkmConfig()
            pb_resp = ekm_service.EkmConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_ekm_config(resp)
            return resp

    class _UpdateEkmConnection(EkmServiceRestStub):
        def __hash__(self):
            return hash("UpdateEkmConnection")

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
            request: ekm_service.UpdateEkmConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.EkmConnection:
            r"""Call the update ekm connection method over HTTP.

            Args:
                request (~.ekm_service.UpdateEkmConnectionRequest):
                    The request object. Request message for
                [EkmService.UpdateEkmConnection][google.cloud.kms.v1.EkmService.UpdateEkmConnection].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.EkmConnection:
                    An [EkmConnection][google.cloud.kms.v1.EkmConnection]
                represents an individual EKM connection. It can be used
                for creating [CryptoKeys][google.cloud.kms.v1.CryptoKey]
                and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                with a
                [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                of
                [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
                as well as performing cryptographic operations using
                keys created within the
                [EkmConnection][google.cloud.kms.v1.EkmConnection].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{ekm_connection.name=projects/*/locations/*/ekmConnections/*}",
                    "body": "ekm_connection",
                },
            ]
            request, metadata = self._interceptor.pre_update_ekm_connection(
                request, metadata
            )
            pb_request = ekm_service.UpdateEkmConnectionRequest.pb(request)
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
            resp = ekm_service.EkmConnection()
            pb_resp = ekm_service.EkmConnection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_ekm_connection(resp)
            return resp

    class _VerifyConnectivity(EkmServiceRestStub):
        def __hash__(self):
            return hash("VerifyConnectivity")

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
            request: ekm_service.VerifyConnectivityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_service.VerifyConnectivityResponse:
            r"""Call the verify connectivity method over HTTP.

            Args:
                request (~.ekm_service.VerifyConnectivityRequest):
                    The request object. Request message for
                [EkmService.VerifyConnectivity][google.cloud.kms.v1.EkmService.VerifyConnectivity].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_service.VerifyConnectivityResponse:
                    Response message for
                [EkmService.VerifyConnectivity][google.cloud.kms.v1.EkmService.VerifyConnectivity].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/ekmConnections/*}:verifyConnectivity",
                },
            ]
            request, metadata = self._interceptor.pre_verify_connectivity(
                request, metadata
            )
            pb_request = ekm_service.VerifyConnectivityRequest.pb(request)
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
            resp = ekm_service.VerifyConnectivityResponse()
            pb_resp = ekm_service.VerifyConnectivityResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_verify_connectivity(resp)
            return resp

    @property
    def create_ekm_connection(
        self,
    ) -> Callable[[ekm_service.CreateEkmConnectionRequest], ekm_service.EkmConnection]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEkmConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ekm_config(
        self,
    ) -> Callable[[ekm_service.GetEkmConfigRequest], ekm_service.EkmConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEkmConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ekm_connection(
        self,
    ) -> Callable[[ekm_service.GetEkmConnectionRequest], ekm_service.EkmConnection]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEkmConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_ekm_connections(
        self,
    ) -> Callable[
        [ekm_service.ListEkmConnectionsRequest], ekm_service.ListEkmConnectionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEkmConnections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_ekm_config(
        self,
    ) -> Callable[[ekm_service.UpdateEkmConfigRequest], ekm_service.EkmConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEkmConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_ekm_connection(
        self,
    ) -> Callable[[ekm_service.UpdateEkmConnectionRequest], ekm_service.EkmConnection]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEkmConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def verify_connectivity(
        self,
    ) -> Callable[
        [ekm_service.VerifyConnectivityRequest], ekm_service.VerifyConnectivityResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._VerifyConnectivity(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(EkmServiceRestStub):
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

    class _ListLocations(EkmServiceRestStub):
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(EkmServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/cryptoKeys/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/importJobs/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConfig}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConnections/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(EkmServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/cryptoKeys/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/importJobs/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConfig}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConnections/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(EkmServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/cryptoKeys/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/importJobs/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConfig}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConnections/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
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

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(EkmServiceRestStub):
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("EkmServiceRestTransport",)
