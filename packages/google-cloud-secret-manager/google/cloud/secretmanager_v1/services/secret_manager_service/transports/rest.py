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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.secretmanager_v1.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSecretManagerServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SecretManagerServiceRestInterceptor:
    """Interceptor for SecretManagerService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SecretManagerServiceRestTransport.

    .. code-block:: python
        class MyCustomSecretManagerServiceInterceptor(SecretManagerServiceRestInterceptor):
            def pre_access_secret_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_access_secret_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_add_secret_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_secret_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_destroy_secret_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_destroy_secret_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_secret_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_secret_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_secret_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_secret_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_secret_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_secret_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_secrets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_secrets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_secret_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_secret_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SecretManagerServiceRestTransport(interceptor=MyCustomSecretManagerServiceInterceptor())
        client = SecretManagerServiceClient(transport=transport)


    """

    def pre_access_secret_version(
        self,
        request: service.AccessSecretVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.AccessSecretVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for access_secret_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_access_secret_version(
        self, response: service.AccessSecretVersionResponse
    ) -> service.AccessSecretVersionResponse:
        """Post-rpc interceptor for access_secret_version

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_add_secret_version(
        self,
        request: service.AddSecretVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.AddSecretVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_secret_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_add_secret_version(
        self, response: resources.SecretVersion
    ) -> resources.SecretVersion:
        """Post-rpc interceptor for add_secret_version

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_create_secret(
        self, request: service.CreateSecretRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateSecretRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_create_secret(self, response: resources.Secret) -> resources.Secret:
        """Post-rpc interceptor for create_secret

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_secret(
        self, request: service.DeleteSecretRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteSecretRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def pre_destroy_secret_version(
        self,
        request: service.DestroySecretVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DestroySecretVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for destroy_secret_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_destroy_secret_version(
        self, response: resources.SecretVersion
    ) -> resources.SecretVersion:
        """Post-rpc interceptor for destroy_secret_version

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_disable_secret_version(
        self,
        request: service.DisableSecretVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DisableSecretVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for disable_secret_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_disable_secret_version(
        self, response: resources.SecretVersion
    ) -> resources.SecretVersion:
        """Post-rpc interceptor for disable_secret_version

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_enable_secret_version(
        self,
        request: service.EnableSecretVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.EnableSecretVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enable_secret_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_enable_secret_version(
        self, response: resources.SecretVersion
    ) -> resources.SecretVersion:
        """Post-rpc interceptor for enable_secret_version

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
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
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_get_secret(
        self, request: service.GetSecretRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetSecretRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_get_secret(self, response: resources.Secret) -> resources.Secret:
        """Post-rpc interceptor for get_secret

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_get_secret_version(
        self,
        request: service.GetSecretVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetSecretVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_secret_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_get_secret_version(
        self, response: resources.SecretVersion
    ) -> resources.SecretVersion:
        """Post-rpc interceptor for get_secret_version

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_list_secrets(
        self, request: service.ListSecretsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListSecretsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_secrets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_list_secrets(
        self, response: service.ListSecretsResponse
    ) -> service.ListSecretsResponse:
        """Post-rpc interceptor for list_secrets

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_list_secret_versions(
        self,
        request: service.ListSecretVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListSecretVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_secret_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_list_secret_versions(
        self, response: service.ListSecretVersionsResponse
    ) -> service.ListSecretVersionsResponse:
        """Post-rpc interceptor for list_secret_versions

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
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
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
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
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response

    def pre_update_secret(
        self, request: service.UpdateSecretRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateSecretRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_update_secret(self, response: resources.Secret) -> resources.Secret:
        """Post-rpc interceptor for update_secret

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
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
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
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
        before they are sent to the SecretManagerService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the SecretManagerService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SecretManagerServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SecretManagerServiceRestInterceptor


class SecretManagerServiceRestTransport(_BaseSecretManagerServiceRestTransport):
    """REST backend synchronous transport for SecretManagerService.

    Secret Manager Service

    Manages secrets and operations using those secrets. Implements a
    REST model with the following objects:

    -  [Secret][google.cloud.secretmanager.v1.Secret]
    -  [SecretVersion][google.cloud.secretmanager.v1.SecretVersion]

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "secretmanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SecretManagerServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'secretmanager.googleapis.com').
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
        self._interceptor = interceptor or SecretManagerServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AccessSecretVersion(
        _BaseSecretManagerServiceRestTransport._BaseAccessSecretVersion,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.AccessSecretVersion")

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
            request: service.AccessSecretVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.AccessSecretVersionResponse:
            r"""Call the access secret version method over HTTP.

            Args:
                request (~.service.AccessSecretVersionRequest):
                    The request object. Request message for
                [SecretManagerService.AccessSecretVersion][google.cloud.secretmanager.v1.SecretManagerService.AccessSecretVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.AccessSecretVersionResponse:
                    Response message for
                [SecretManagerService.AccessSecretVersion][google.cloud.secretmanager.v1.SecretManagerService.AccessSecretVersion].

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseAccessSecretVersion._get_http_options()
            )
            request, metadata = self._interceptor.pre_access_secret_version(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseAccessSecretVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseAccessSecretVersion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._AccessSecretVersion._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.AccessSecretVersionResponse()
            pb_resp = service.AccessSecretVersionResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_access_secret_version(resp)
            return resp

    class _AddSecretVersion(
        _BaseSecretManagerServiceRestTransport._BaseAddSecretVersion,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.AddSecretVersion")

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
            request: service.AddSecretVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SecretVersion:
            r"""Call the add secret version method over HTTP.

            Args:
                request (~.service.AddSecretVersionRequest):
                    The request object. Request message for
                [SecretManagerService.AddSecretVersion][google.cloud.secretmanager.v1.SecretManagerService.AddSecretVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SecretVersion:
                    A secret version resource in the
                Secret Manager API.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseAddSecretVersion._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_secret_version(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseAddSecretVersion._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseAddSecretVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseAddSecretVersion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._AddSecretVersion._get_response(
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
            resp = resources.SecretVersion()
            pb_resp = resources.SecretVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_secret_version(resp)
            return resp

    class _CreateSecret(
        _BaseSecretManagerServiceRestTransport._BaseCreateSecret,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.CreateSecret")

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
            request: service.CreateSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Secret:
            r"""Call the create secret method over HTTP.

            Args:
                request (~.service.CreateSecretRequest):
                    The request object. Request message for
                [SecretManagerService.CreateSecret][google.cloud.secretmanager.v1.SecretManagerService.CreateSecret].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Secret:
                    A [Secret][google.cloud.secretmanager.v1.Secret] is a
                logical secret whose value and versions can be accessed.

                A [Secret][google.cloud.secretmanager.v1.Secret] is made
                up of zero or more
                [SecretVersions][google.cloud.secretmanager.v1.SecretVersion]
                that represent the secret data.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseCreateSecret._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_secret(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseCreateSecret._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseCreateSecret._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseCreateSecret._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._CreateSecret._get_response(
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
            resp = resources.Secret()
            pb_resp = resources.Secret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_secret(resp)
            return resp

    class _DeleteSecret(
        _BaseSecretManagerServiceRestTransport._BaseDeleteSecret,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.DeleteSecret")

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
            request: service.DeleteSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete secret method over HTTP.

            Args:
                request (~.service.DeleteSecretRequest):
                    The request object. Request message for
                [SecretManagerService.DeleteSecret][google.cloud.secretmanager.v1.SecretManagerService.DeleteSecret].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseDeleteSecret._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_secret(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseDeleteSecret._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseDeleteSecret._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._DeleteSecret._get_response(
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

    class _DestroySecretVersion(
        _BaseSecretManagerServiceRestTransport._BaseDestroySecretVersion,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.DestroySecretVersion")

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
            request: service.DestroySecretVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SecretVersion:
            r"""Call the destroy secret version method over HTTP.

            Args:
                request (~.service.DestroySecretVersionRequest):
                    The request object. Request message for
                [SecretManagerService.DestroySecretVersion][google.cloud.secretmanager.v1.SecretManagerService.DestroySecretVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SecretVersion:
                    A secret version resource in the
                Secret Manager API.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseDestroySecretVersion._get_http_options()
            )
            request, metadata = self._interceptor.pre_destroy_secret_version(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseDestroySecretVersion._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseDestroySecretVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseDestroySecretVersion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._DestroySecretVersion._get_response(
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
            resp = resources.SecretVersion()
            pb_resp = resources.SecretVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_destroy_secret_version(resp)
            return resp

    class _DisableSecretVersion(
        _BaseSecretManagerServiceRestTransport._BaseDisableSecretVersion,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.DisableSecretVersion")

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
            request: service.DisableSecretVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SecretVersion:
            r"""Call the disable secret version method over HTTP.

            Args:
                request (~.service.DisableSecretVersionRequest):
                    The request object. Request message for
                [SecretManagerService.DisableSecretVersion][google.cloud.secretmanager.v1.SecretManagerService.DisableSecretVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SecretVersion:
                    A secret version resource in the
                Secret Manager API.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseDisableSecretVersion._get_http_options()
            )
            request, metadata = self._interceptor.pre_disable_secret_version(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseDisableSecretVersion._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseDisableSecretVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseDisableSecretVersion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._DisableSecretVersion._get_response(
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
            resp = resources.SecretVersion()
            pb_resp = resources.SecretVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_disable_secret_version(resp)
            return resp

    class _EnableSecretVersion(
        _BaseSecretManagerServiceRestTransport._BaseEnableSecretVersion,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.EnableSecretVersion")

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
            request: service.EnableSecretVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SecretVersion:
            r"""Call the enable secret version method over HTTP.

            Args:
                request (~.service.EnableSecretVersionRequest):
                    The request object. Request message for
                [SecretManagerService.EnableSecretVersion][google.cloud.secretmanager.v1.SecretManagerService.EnableSecretVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SecretVersion:
                    A secret version resource in the
                Secret Manager API.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseEnableSecretVersion._get_http_options()
            )
            request, metadata = self._interceptor.pre_enable_secret_version(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseEnableSecretVersion._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseEnableSecretVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseEnableSecretVersion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._EnableSecretVersion._get_response(
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
            resp = resources.SecretVersion()
            pb_resp = resources.SecretVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_enable_secret_version(resp)
            return resp

    class _GetIamPolicy(
        _BaseSecretManagerServiceRestTransport._BaseGetIamPolicy,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetSecret(
        _BaseSecretManagerServiceRestTransport._BaseGetSecret,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.GetSecret")

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
            request: service.GetSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Secret:
            r"""Call the get secret method over HTTP.

            Args:
                request (~.service.GetSecretRequest):
                    The request object. Request message for
                [SecretManagerService.GetSecret][google.cloud.secretmanager.v1.SecretManagerService.GetSecret].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Secret:
                    A [Secret][google.cloud.secretmanager.v1.Secret] is a
                logical secret whose value and versions can be accessed.

                A [Secret][google.cloud.secretmanager.v1.Secret] is made
                up of zero or more
                [SecretVersions][google.cloud.secretmanager.v1.SecretVersion]
                that represent the secret data.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseGetSecret._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_secret(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseGetSecret._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseGetSecret._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._GetSecret._get_response(
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
            resp = resources.Secret()
            pb_resp = resources.Secret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_secret(resp)
            return resp

    class _GetSecretVersion(
        _BaseSecretManagerServiceRestTransport._BaseGetSecretVersion,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.GetSecretVersion")

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
            request: service.GetSecretVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SecretVersion:
            r"""Call the get secret version method over HTTP.

            Args:
                request (~.service.GetSecretVersionRequest):
                    The request object. Request message for
                [SecretManagerService.GetSecretVersion][google.cloud.secretmanager.v1.SecretManagerService.GetSecretVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SecretVersion:
                    A secret version resource in the
                Secret Manager API.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseGetSecretVersion._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_secret_version(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseGetSecretVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseGetSecretVersion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._GetSecretVersion._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.SecretVersion()
            pb_resp = resources.SecretVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_secret_version(resp)
            return resp

    class _ListSecrets(
        _BaseSecretManagerServiceRestTransport._BaseListSecrets,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.ListSecrets")

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
            request: service.ListSecretsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListSecretsResponse:
            r"""Call the list secrets method over HTTP.

            Args:
                request (~.service.ListSecretsRequest):
                    The request object. Request message for
                [SecretManagerService.ListSecrets][google.cloud.secretmanager.v1.SecretManagerService.ListSecrets].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListSecretsResponse:
                    Response message for
                [SecretManagerService.ListSecrets][google.cloud.secretmanager.v1.SecretManagerService.ListSecrets].

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseListSecrets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_secrets(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseListSecrets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseListSecrets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._ListSecrets._get_response(
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
            resp = service.ListSecretsResponse()
            pb_resp = service.ListSecretsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_secrets(resp)
            return resp

    class _ListSecretVersions(
        _BaseSecretManagerServiceRestTransport._BaseListSecretVersions,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.ListSecretVersions")

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
            request: service.ListSecretVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListSecretVersionsResponse:
            r"""Call the list secret versions method over HTTP.

            Args:
                request (~.service.ListSecretVersionsRequest):
                    The request object. Request message for
                [SecretManagerService.ListSecretVersions][google.cloud.secretmanager.v1.SecretManagerService.ListSecretVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListSecretVersionsResponse:
                    Response message for
                [SecretManagerService.ListSecretVersions][google.cloud.secretmanager.v1.SecretManagerService.ListSecretVersions].

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseListSecretVersions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_secret_versions(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseListSecretVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseListSecretVersions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._ListSecretVersions._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListSecretVersionsResponse()
            pb_resp = service.ListSecretVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_secret_versions(resp)
            return resp

    class _SetIamPolicy(
        _BaseSecretManagerServiceRestTransport._BaseSetIamPolicy,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._SetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(
        _BaseSecretManagerServiceRestTransport._BaseTestIamPermissions,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecretManagerServiceRestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UpdateSecret(
        _BaseSecretManagerServiceRestTransport._BaseUpdateSecret,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.UpdateSecret")

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
            request: service.UpdateSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Secret:
            r"""Call the update secret method over HTTP.

            Args:
                request (~.service.UpdateSecretRequest):
                    The request object. Request message for
                [SecretManagerService.UpdateSecret][google.cloud.secretmanager.v1.SecretManagerService.UpdateSecret].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Secret:
                    A [Secret][google.cloud.secretmanager.v1.Secret] is a
                logical secret whose value and versions can be accessed.

                A [Secret][google.cloud.secretmanager.v1.Secret] is made
                up of zero or more
                [SecretVersions][google.cloud.secretmanager.v1.SecretVersion]
                that represent the secret data.

            """

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseUpdateSecret._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_secret(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseUpdateSecret._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecretManagerServiceRestTransport._BaseUpdateSecret._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseUpdateSecret._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._UpdateSecret._get_response(
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
            resp = resources.Secret()
            pb_resp = resources.Secret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_secret(resp)
            return resp

    @property
    def access_secret_version(
        self,
    ) -> Callable[
        [service.AccessSecretVersionRequest], service.AccessSecretVersionResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AccessSecretVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def add_secret_version(
        self,
    ) -> Callable[[service.AddSecretVersionRequest], resources.SecretVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddSecretVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_secret(
        self,
    ) -> Callable[[service.CreateSecretRequest], resources.Secret]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_secret(self) -> Callable[[service.DeleteSecretRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def destroy_secret_version(
        self,
    ) -> Callable[[service.DestroySecretVersionRequest], resources.SecretVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DestroySecretVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_secret_version(
        self,
    ) -> Callable[[service.DisableSecretVersionRequest], resources.SecretVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableSecretVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_secret_version(
        self,
    ) -> Callable[[service.EnableSecretVersionRequest], resources.SecretVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableSecretVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_secret(self) -> Callable[[service.GetSecretRequest], resources.Secret]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_secret_version(
        self,
    ) -> Callable[[service.GetSecretVersionRequest], resources.SecretVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSecretVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_secrets(
        self,
    ) -> Callable[[service.ListSecretsRequest], service.ListSecretsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSecrets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_secret_versions(
        self,
    ) -> Callable[
        [service.ListSecretVersionsRequest], service.ListSecretVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSecretVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_secret(
        self,
    ) -> Callable[[service.UpdateSecretRequest], resources.Secret]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseSecretManagerServiceRestTransport._BaseGetLocation,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.GetLocation")

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

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._GetLocation._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseSecretManagerServiceRestTransport._BaseListLocations,
        SecretManagerServiceRestStub,
    ):
        def __hash__(self):
            return hash("SecretManagerServiceRestTransport.ListLocations")

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

            http_options = (
                _BaseSecretManagerServiceRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseSecretManagerServiceRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecretManagerServiceRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecretManagerServiceRestTransport._ListLocations._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SecretManagerServiceRestTransport",)
