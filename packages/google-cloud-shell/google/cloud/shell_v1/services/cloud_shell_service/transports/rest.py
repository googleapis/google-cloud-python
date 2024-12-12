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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.shell_v1.types import cloudshell

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCloudShellServiceRestTransport

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


class CloudShellServiceRestInterceptor:
    """Interceptor for CloudShellService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudShellServiceRestTransport.

    .. code-block:: python
        class MyCustomCloudShellServiceInterceptor(CloudShellServiceRestInterceptor):
            def pre_add_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_authorize_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_authorize_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudShellServiceRestTransport(interceptor=MyCustomCloudShellServiceInterceptor())
        client = CloudShellServiceClient(transport=transport)


    """

    def pre_add_public_key(
        self,
        request: cloudshell.AddPublicKeyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[cloudshell.AddPublicKeyRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for add_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudShellService server.
        """
        return request, metadata

    def post_add_public_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for add_public_key

        Override in a subclass to manipulate the response
        after it is returned by the CloudShellService server but before
        it is returned to user code.
        """
        return response

    def pre_authorize_environment(
        self,
        request: cloudshell.AuthorizeEnvironmentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloudshell.AuthorizeEnvironmentRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for authorize_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudShellService server.
        """
        return request, metadata

    def post_authorize_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for authorize_environment

        Override in a subclass to manipulate the response
        after it is returned by the CloudShellService server but before
        it is returned to user code.
        """
        return response

    def pre_get_environment(
        self,
        request: cloudshell.GetEnvironmentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloudshell.GetEnvironmentRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudShellService server.
        """
        return request, metadata

    def post_get_environment(
        self, response: cloudshell.Environment
    ) -> cloudshell.Environment:
        """Post-rpc interceptor for get_environment

        Override in a subclass to manipulate the response
        after it is returned by the CloudShellService server but before
        it is returned to user code.
        """
        return response

    def pre_remove_public_key(
        self,
        request: cloudshell.RemovePublicKeyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloudshell.RemovePublicKeyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for remove_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudShellService server.
        """
        return request, metadata

    def post_remove_public_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_public_key

        Override in a subclass to manipulate the response
        after it is returned by the CloudShellService server but before
        it is returned to user code.
        """
        return response

    def pre_start_environment(
        self,
        request: cloudshell.StartEnvironmentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloudshell.StartEnvironmentRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for start_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudShellService server.
        """
        return request, metadata

    def post_start_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_environment

        Override in a subclass to manipulate the response
        after it is returned by the CloudShellService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudShellServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudShellServiceRestInterceptor


class CloudShellServiceRestTransport(_BaseCloudShellServiceRestTransport):
    """REST backend synchronous transport for CloudShellService.

    API for interacting with Google Cloud Shell. Each user of
    Cloud Shell has at least one environment, which has the ID
    "default". Environment consists of a Docker image defining what
    is installed on the environment and a home directory containing
    the user's data that will remain across sessions. Clients use
    this API to start and fetch information about their environment,
    which can then be used to connect to that environment via a
    separate SSH client.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudshell.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudShellServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudshell.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CloudShellServiceRestInterceptor()
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

    class _AddPublicKey(
        _BaseCloudShellServiceRestTransport._BaseAddPublicKey, CloudShellServiceRestStub
    ):
        def __hash__(self):
            return hash("CloudShellServiceRestTransport.AddPublicKey")

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
            request: cloudshell.AddPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the add public key method over HTTP.

            Args:
                request (~.cloudshell.AddPublicKeyRequest):
                    The request object. Request message for
                [AddPublicKey][google.cloud.shell.v1.CloudShellService.AddPublicKey].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudShellServiceRestTransport._BaseAddPublicKey._get_http_options()
            )

            request, metadata = self._interceptor.pre_add_public_key(request, metadata)
            transcoded_request = _BaseCloudShellServiceRestTransport._BaseAddPublicKey._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudShellServiceRestTransport._BaseAddPublicKey._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudShellServiceRestTransport._BaseAddPublicKey._get_query_params_json(
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
                    f"Sending request for google.cloud.shell_v1.CloudShellServiceClient.AddPublicKey",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "AddPublicKey",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudShellServiceRestTransport._AddPublicKey._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_add_public_key(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.shell_v1.CloudShellServiceClient.add_public_key",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "AddPublicKey",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _AuthorizeEnvironment(
        _BaseCloudShellServiceRestTransport._BaseAuthorizeEnvironment,
        CloudShellServiceRestStub,
    ):
        def __hash__(self):
            return hash("CloudShellServiceRestTransport.AuthorizeEnvironment")

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
            request: cloudshell.AuthorizeEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the authorize environment method over HTTP.

            Args:
                request (~.cloudshell.AuthorizeEnvironmentRequest):
                    The request object. Request message for
                [AuthorizeEnvironment][google.cloud.shell.v1.CloudShellService.AuthorizeEnvironment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudShellServiceRestTransport._BaseAuthorizeEnvironment._get_http_options()
            )

            request, metadata = self._interceptor.pre_authorize_environment(
                request, metadata
            )
            transcoded_request = _BaseCloudShellServiceRestTransport._BaseAuthorizeEnvironment._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudShellServiceRestTransport._BaseAuthorizeEnvironment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudShellServiceRestTransport._BaseAuthorizeEnvironment._get_query_params_json(
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
                    f"Sending request for google.cloud.shell_v1.CloudShellServiceClient.AuthorizeEnvironment",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "AuthorizeEnvironment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                CloudShellServiceRestTransport._AuthorizeEnvironment._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_authorize_environment(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.shell_v1.CloudShellServiceClient.authorize_environment",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "AuthorizeEnvironment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetEnvironment(
        _BaseCloudShellServiceRestTransport._BaseGetEnvironment,
        CloudShellServiceRestStub,
    ):
        def __hash__(self):
            return hash("CloudShellServiceRestTransport.GetEnvironment")

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
            request: cloudshell.GetEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloudshell.Environment:
            r"""Call the get environment method over HTTP.

            Args:
                request (~.cloudshell.GetEnvironmentRequest):
                    The request object. Request message for
                [GetEnvironment][google.cloud.shell.v1.CloudShellService.GetEnvironment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloudshell.Environment:
                    A Cloud Shell environment, which is
                defined as the combination of a Docker
                image specifying what is installed on
                the environment and a home directory
                containing the user's data that will
                remain across sessions. Each user has at
                least an environment with the ID
                "default".

            """

            http_options = (
                _BaseCloudShellServiceRestTransport._BaseGetEnvironment._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_environment(request, metadata)
            transcoded_request = _BaseCloudShellServiceRestTransport._BaseGetEnvironment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudShellServiceRestTransport._BaseGetEnvironment._get_query_params_json(
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
                    f"Sending request for google.cloud.shell_v1.CloudShellServiceClient.GetEnvironment",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "GetEnvironment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudShellServiceRestTransport._GetEnvironment._get_response(
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
            resp = cloudshell.Environment()
            pb_resp = cloudshell.Environment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_environment(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloudshell.Environment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.shell_v1.CloudShellServiceClient.get_environment",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "GetEnvironment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RemovePublicKey(
        _BaseCloudShellServiceRestTransport._BaseRemovePublicKey,
        CloudShellServiceRestStub,
    ):
        def __hash__(self):
            return hash("CloudShellServiceRestTransport.RemovePublicKey")

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
            request: cloudshell.RemovePublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove public key method over HTTP.

            Args:
                request (~.cloudshell.RemovePublicKeyRequest):
                    The request object. Request message for
                [RemovePublicKey][google.cloud.shell.v1.CloudShellService.RemovePublicKey].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudShellServiceRestTransport._BaseRemovePublicKey._get_http_options()
            )

            request, metadata = self._interceptor.pre_remove_public_key(
                request, metadata
            )
            transcoded_request = _BaseCloudShellServiceRestTransport._BaseRemovePublicKey._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudShellServiceRestTransport._BaseRemovePublicKey._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudShellServiceRestTransport._BaseRemovePublicKey._get_query_params_json(
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
                    f"Sending request for google.cloud.shell_v1.CloudShellServiceClient.RemovePublicKey",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "RemovePublicKey",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudShellServiceRestTransport._RemovePublicKey._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_remove_public_key(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.shell_v1.CloudShellServiceClient.remove_public_key",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "RemovePublicKey",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _StartEnvironment(
        _BaseCloudShellServiceRestTransport._BaseStartEnvironment,
        CloudShellServiceRestStub,
    ):
        def __hash__(self):
            return hash("CloudShellServiceRestTransport.StartEnvironment")

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
            request: cloudshell.StartEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start environment method over HTTP.

            Args:
                request (~.cloudshell.StartEnvironmentRequest):
                    The request object. Request message for
                [StartEnvironment][google.cloud.shell.v1.CloudShellService.StartEnvironment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudShellServiceRestTransport._BaseStartEnvironment._get_http_options()
            )

            request, metadata = self._interceptor.pre_start_environment(
                request, metadata
            )
            transcoded_request = _BaseCloudShellServiceRestTransport._BaseStartEnvironment._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudShellServiceRestTransport._BaseStartEnvironment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudShellServiceRestTransport._BaseStartEnvironment._get_query_params_json(
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
                    f"Sending request for google.cloud.shell_v1.CloudShellServiceClient.StartEnvironment",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "StartEnvironment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudShellServiceRestTransport._StartEnvironment._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_start_environment(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.shell_v1.CloudShellServiceClient.start_environment",
                    extra={
                        "serviceName": "google.cloud.shell.v1.CloudShellService",
                        "rpcName": "StartEnvironment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def add_public_key(
        self,
    ) -> Callable[[cloudshell.AddPublicKeyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def authorize_environment(
        self,
    ) -> Callable[[cloudshell.AuthorizeEnvironmentRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AuthorizeEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_environment(
        self,
    ) -> Callable[[cloudshell.GetEnvironmentRequest], cloudshell.Environment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_public_key(
        self,
    ) -> Callable[[cloudshell.RemovePublicKeyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemovePublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_environment(
        self,
    ) -> Callable[[cloudshell.StartEnvironmentRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudShellServiceRestTransport",)
