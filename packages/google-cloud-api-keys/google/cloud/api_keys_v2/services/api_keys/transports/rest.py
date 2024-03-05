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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.api_keys_v2.types import apikeys, resources

from .base import ApiKeysTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ApiKeysRestInterceptor:
    """Interceptor for ApiKeys.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ApiKeysRestTransport.

    .. code-block:: python
        class MyCustomApiKeysInterceptor(ApiKeysRestInterceptor):
            def pre_create_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_key_string(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_key_string(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_key(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ApiKeysRestTransport(interceptor=MyCustomApiKeysInterceptor())
        client = ApiKeysClient(transport=transport)


    """

    def pre_create_key(
        self, request: apikeys.CreateKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.CreateKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_create_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_key

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_delete_key(
        self, request: apikeys.DeleteKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.DeleteKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_delete_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_key

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_get_key(
        self, request: apikeys.GetKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.GetKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_get_key(self, response: resources.Key) -> resources.Key:
        """Post-rpc interceptor for get_key

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_get_key_string(
        self, request: apikeys.GetKeyStringRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.GetKeyStringRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_key_string

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_get_key_string(
        self, response: apikeys.GetKeyStringResponse
    ) -> apikeys.GetKeyStringResponse:
        """Post-rpc interceptor for get_key_string

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_list_keys(
        self, request: apikeys.ListKeysRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.ListKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_list_keys(
        self, response: apikeys.ListKeysResponse
    ) -> apikeys.ListKeysResponse:
        """Post-rpc interceptor for list_keys

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_lookup_key(
        self, request: apikeys.LookupKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.LookupKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for lookup_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_lookup_key(
        self, response: apikeys.LookupKeyResponse
    ) -> apikeys.LookupKeyResponse:
        """Post-rpc interceptor for lookup_key

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_key(
        self, request: apikeys.UndeleteKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.UndeleteKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_undelete_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_key

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response

    def pre_update_key(
        self, request: apikeys.UpdateKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apikeys.UpdateKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_update_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_key

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
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
        before they are sent to the ApiKeys server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ApiKeys server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ApiKeysRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ApiKeysRestInterceptor


class ApiKeysRestTransport(ApiKeysTransport):
    """REST backend transport for ApiKeys.

    Manages the API keys associated with projects.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "apikeys.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ApiKeysRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'apikeys.googleapis.com').
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
        self._interceptor = interceptor or ApiKeysRestInterceptor()
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
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateKey(ApiKeysRestStub):
        def __hash__(self):
            return hash("CreateKey")

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
            request: apikeys.CreateKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create key method over HTTP.

            Args:
                request (~.apikeys.CreateKeyRequest):
                    The request object. Request message for ``CreateKey`` method.
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
                    "uri": "/v2/{parent=projects/*/locations/*}/keys",
                    "body": "key",
                },
            ]
            request, metadata = self._interceptor.pre_create_key(request, metadata)
            pb_request = apikeys.CreateKeyRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_key(resp)
            return resp

    class _DeleteKey(ApiKeysRestStub):
        def __hash__(self):
            return hash("DeleteKey")

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
            request: apikeys.DeleteKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete key method over HTTP.

            Args:
                request (~.apikeys.DeleteKeyRequest):
                    The request object. Request message for ``DeleteKey`` method.
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
                    "uri": "/v2/{name=projects/*/locations/*/keys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_key(request, metadata)
            pb_request = apikeys.DeleteKeyRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_key(resp)
            return resp

    class _GetKey(ApiKeysRestStub):
        def __hash__(self):
            return hash("GetKey")

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
            request: apikeys.GetKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Key:
            r"""Call the get key method over HTTP.

            Args:
                request (~.apikeys.GetKeyRequest):
                    The request object. Request message for ``GetKey`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Key:
                    The representation of a key managed
                by the API Keys API.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/keys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_key(request, metadata)
            pb_request = apikeys.GetKeyRequest.pb(request)
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
            resp = resources.Key()
            pb_resp = resources.Key.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_key(resp)
            return resp

    class _GetKeyString(ApiKeysRestStub):
        def __hash__(self):
            return hash("GetKeyString")

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
            request: apikeys.GetKeyStringRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apikeys.GetKeyStringResponse:
            r"""Call the get key string method over HTTP.

            Args:
                request (~.apikeys.GetKeyStringRequest):
                    The request object. Request message for ``GetKeyString`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apikeys.GetKeyStringResponse:
                    Response message for ``GetKeyString`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/keys/*}/keyString",
                },
            ]
            request, metadata = self._interceptor.pre_get_key_string(request, metadata)
            pb_request = apikeys.GetKeyStringRequest.pb(request)
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
            resp = apikeys.GetKeyStringResponse()
            pb_resp = apikeys.GetKeyStringResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_key_string(resp)
            return resp

    class _ListKeys(ApiKeysRestStub):
        def __hash__(self):
            return hash("ListKeys")

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
            request: apikeys.ListKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apikeys.ListKeysResponse:
            r"""Call the list keys method over HTTP.

            Args:
                request (~.apikeys.ListKeysRequest):
                    The request object. Request message for ``ListKeys`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apikeys.ListKeysResponse:
                    Response message for ``ListKeys`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/keys",
                },
            ]
            request, metadata = self._interceptor.pre_list_keys(request, metadata)
            pb_request = apikeys.ListKeysRequest.pb(request)
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
            resp = apikeys.ListKeysResponse()
            pb_resp = apikeys.ListKeysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_keys(resp)
            return resp

    class _LookupKey(ApiKeysRestStub):
        def __hash__(self):
            return hash("LookupKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "keyString": "",
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
            request: apikeys.LookupKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apikeys.LookupKeyResponse:
            r"""Call the lookup key method over HTTP.

            Args:
                request (~.apikeys.LookupKeyRequest):
                    The request object. Request message for ``LookupKey`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apikeys.LookupKeyResponse:
                    Response message for ``LookupKey`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/keys:lookupKey",
                },
            ]
            request, metadata = self._interceptor.pre_lookup_key(request, metadata)
            pb_request = apikeys.LookupKeyRequest.pb(request)
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
            resp = apikeys.LookupKeyResponse()
            pb_resp = apikeys.LookupKeyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lookup_key(resp)
            return resp

    class _UndeleteKey(ApiKeysRestStub):
        def __hash__(self):
            return hash("UndeleteKey")

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
            request: apikeys.UndeleteKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete key method over HTTP.

            Args:
                request (~.apikeys.UndeleteKeyRequest):
                    The request object. Request message for ``UndeleteKey`` method.
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
                    "uri": "/v2/{name=projects/*/locations/*/keys/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_key(request, metadata)
            pb_request = apikeys.UndeleteKeyRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_undelete_key(resp)
            return resp

    class _UpdateKey(ApiKeysRestStub):
        def __hash__(self):
            return hash("UpdateKey")

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
            request: apikeys.UpdateKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update key method over HTTP.

            Args:
                request (~.apikeys.UpdateKeyRequest):
                    The request object. Request message for ``UpdateKey`` method.
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
                    "uri": "/v2/{key.name=projects/*/locations/*/keys/*}",
                    "body": "key",
                },
            ]
            request, metadata = self._interceptor.pre_update_key(request, metadata)
            pb_request = apikeys.UpdateKeyRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_key(resp)
            return resp

    @property
    def create_key(
        self,
    ) -> Callable[[apikeys.CreateKeyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_key(
        self,
    ) -> Callable[[apikeys.DeleteKeyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_key(self) -> Callable[[apikeys.GetKeyRequest], resources.Key]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_key_string(
        self,
    ) -> Callable[[apikeys.GetKeyStringRequest], apikeys.GetKeyStringResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetKeyString(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_keys(
        self,
    ) -> Callable[[apikeys.ListKeysRequest], apikeys.ListKeysResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_key(
        self,
    ) -> Callable[[apikeys.LookupKeyRequest], apikeys.LookupKeyResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_key(
        self,
    ) -> Callable[[apikeys.UndeleteKeyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_key(
        self,
    ) -> Callable[[apikeys.UpdateKeyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(ApiKeysRestStub):
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
                    "uri": "/v2/{name=operations/*}",
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


__all__ = ("ApiKeysRestTransport",)
