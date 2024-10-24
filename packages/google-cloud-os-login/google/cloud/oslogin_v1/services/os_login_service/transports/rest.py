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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.oslogin_v1.common.types import common
from google.cloud.oslogin_v1.types import oslogin

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseOsLoginServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class OsLoginServiceRestInterceptor:
    """Interceptor for OsLoginService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the OsLoginServiceRestTransport.

    .. code-block:: python
        class MyCustomOsLoginServiceInterceptor(OsLoginServiceRestInterceptor):
            def pre_create_ssh_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_ssh_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_posix_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_ssh_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_login_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_login_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_ssh_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ssh_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_ssh_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_ssh_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_ssh_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_ssh_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = OsLoginServiceRestTransport(interceptor=MyCustomOsLoginServiceInterceptor())
        client = OsLoginServiceClient(transport=transport)


    """

    def pre_create_ssh_public_key(
        self,
        request: oslogin.CreateSshPublicKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.CreateSshPublicKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_ssh_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def post_create_ssh_public_key(
        self, response: common.SshPublicKey
    ) -> common.SshPublicKey:
        """Post-rpc interceptor for create_ssh_public_key

        Override in a subclass to manipulate the response
        after it is returned by the OsLoginService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_posix_account(
        self,
        request: oslogin.DeletePosixAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.DeletePosixAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_posix_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def pre_delete_ssh_public_key(
        self,
        request: oslogin.DeleteSshPublicKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.DeleteSshPublicKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_ssh_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def pre_get_login_profile(
        self,
        request: oslogin.GetLoginProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.GetLoginProfileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_login_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def post_get_login_profile(
        self, response: oslogin.LoginProfile
    ) -> oslogin.LoginProfile:
        """Post-rpc interceptor for get_login_profile

        Override in a subclass to manipulate the response
        after it is returned by the OsLoginService server but before
        it is returned to user code.
        """
        return response

    def pre_get_ssh_public_key(
        self,
        request: oslogin.GetSshPublicKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.GetSshPublicKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ssh_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def post_get_ssh_public_key(
        self, response: common.SshPublicKey
    ) -> common.SshPublicKey:
        """Post-rpc interceptor for get_ssh_public_key

        Override in a subclass to manipulate the response
        after it is returned by the OsLoginService server but before
        it is returned to user code.
        """
        return response

    def pre_import_ssh_public_key(
        self,
        request: oslogin.ImportSshPublicKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.ImportSshPublicKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_ssh_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def post_import_ssh_public_key(
        self, response: oslogin.ImportSshPublicKeyResponse
    ) -> oslogin.ImportSshPublicKeyResponse:
        """Post-rpc interceptor for import_ssh_public_key

        Override in a subclass to manipulate the response
        after it is returned by the OsLoginService server but before
        it is returned to user code.
        """
        return response

    def pre_update_ssh_public_key(
        self,
        request: oslogin.UpdateSshPublicKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oslogin.UpdateSshPublicKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_ssh_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsLoginService server.
        """
        return request, metadata

    def post_update_ssh_public_key(
        self, response: common.SshPublicKey
    ) -> common.SshPublicKey:
        """Post-rpc interceptor for update_ssh_public_key

        Override in a subclass to manipulate the response
        after it is returned by the OsLoginService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class OsLoginServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: OsLoginServiceRestInterceptor


class OsLoginServiceRestTransport(_BaseOsLoginServiceRestTransport):
    """REST backend synchronous transport for OsLoginService.

    Cloud OS Login API

    The Cloud OS Login API allows you to manage users and their
    associated SSH public keys for logging into virtual machines on
    Google Cloud Platform.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "oslogin.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[OsLoginServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'oslogin.googleapis.com').
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
        self._interceptor = interceptor or OsLoginServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateSshPublicKey(
        _BaseOsLoginServiceRestTransport._BaseCreateSshPublicKey, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.CreateSshPublicKey")

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
            request: oslogin.CreateSshPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.SshPublicKey:
            r"""Call the create ssh public key method over HTTP.

            Args:
                request (~.oslogin.CreateSshPublicKeyRequest):
                    The request object. A request message for creating an SSH
                public key.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.SshPublicKey:
                    The SSH public key information
                associated with a Google account.

            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseCreateSshPublicKey._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_ssh_public_key(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseCreateSshPublicKey._get_transcoded_request(
                http_options, request
            )

            body = _BaseOsLoginServiceRestTransport._BaseCreateSshPublicKey._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseCreateSshPublicKey._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._CreateSshPublicKey._get_response(
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
            resp = common.SshPublicKey()
            pb_resp = common.SshPublicKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_ssh_public_key(resp)
            return resp

    class _DeletePosixAccount(
        _BaseOsLoginServiceRestTransport._BaseDeletePosixAccount, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.DeletePosixAccount")

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
            request: oslogin.DeletePosixAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete posix account method over HTTP.

            Args:
                request (~.oslogin.DeletePosixAccountRequest):
                    The request object. A request message for deleting a
                POSIX account entry.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseDeletePosixAccount._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_posix_account(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseDeletePosixAccount._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseDeletePosixAccount._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._DeletePosixAccount._get_response(
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

    class _DeleteSshPublicKey(
        _BaseOsLoginServiceRestTransport._BaseDeleteSshPublicKey, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.DeleteSshPublicKey")

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
            request: oslogin.DeleteSshPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete ssh public key method over HTTP.

            Args:
                request (~.oslogin.DeleteSshPublicKeyRequest):
                    The request object. A request message for deleting an SSH
                public key.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseDeleteSshPublicKey._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_ssh_public_key(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseDeleteSshPublicKey._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseDeleteSshPublicKey._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._DeleteSshPublicKey._get_response(
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

    class _GetLoginProfile(
        _BaseOsLoginServiceRestTransport._BaseGetLoginProfile, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.GetLoginProfile")

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
            request: oslogin.GetLoginProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oslogin.LoginProfile:
            r"""Call the get login profile method over HTTP.

            Args:
                request (~.oslogin.GetLoginProfileRequest):
                    The request object. A request message for retrieving the
                login profile information for a user.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oslogin.LoginProfile:
                    The user profile information used for
                logging in to a virtual machine on
                Google Compute Engine.

            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseGetLoginProfile._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_login_profile(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseGetLoginProfile._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseGetLoginProfile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._GetLoginProfile._get_response(
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
            resp = oslogin.LoginProfile()
            pb_resp = oslogin.LoginProfile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_login_profile(resp)
            return resp

    class _GetSshPublicKey(
        _BaseOsLoginServiceRestTransport._BaseGetSshPublicKey, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.GetSshPublicKey")

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
            request: oslogin.GetSshPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.SshPublicKey:
            r"""Call the get ssh public key method over HTTP.

            Args:
                request (~.oslogin.GetSshPublicKeyRequest):
                    The request object. A request message for retrieving an
                SSH public key.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.SshPublicKey:
                    The SSH public key information
                associated with a Google account.

            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseGetSshPublicKey._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_ssh_public_key(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseGetSshPublicKey._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseGetSshPublicKey._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._GetSshPublicKey._get_response(
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
            resp = common.SshPublicKey()
            pb_resp = common.SshPublicKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ssh_public_key(resp)
            return resp

    class _ImportSshPublicKey(
        _BaseOsLoginServiceRestTransport._BaseImportSshPublicKey, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.ImportSshPublicKey")

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
            request: oslogin.ImportSshPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oslogin.ImportSshPublicKeyResponse:
            r"""Call the import ssh public key method over HTTP.

            Args:
                request (~.oslogin.ImportSshPublicKeyRequest):
                    The request object. A request message for importing an
                SSH public key.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oslogin.ImportSshPublicKeyResponse:
                    A response message for importing an
                SSH public key.

            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseImportSshPublicKey._get_http_options()
            )
            request, metadata = self._interceptor.pre_import_ssh_public_key(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseImportSshPublicKey._get_transcoded_request(
                http_options, request
            )

            body = _BaseOsLoginServiceRestTransport._BaseImportSshPublicKey._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseImportSshPublicKey._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._ImportSshPublicKey._get_response(
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
            resp = oslogin.ImportSshPublicKeyResponse()
            pb_resp = oslogin.ImportSshPublicKeyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_ssh_public_key(resp)
            return resp

    class _UpdateSshPublicKey(
        _BaseOsLoginServiceRestTransport._BaseUpdateSshPublicKey, OsLoginServiceRestStub
    ):
        def __hash__(self):
            return hash("OsLoginServiceRestTransport.UpdateSshPublicKey")

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
            request: oslogin.UpdateSshPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.SshPublicKey:
            r"""Call the update ssh public key method over HTTP.

            Args:
                request (~.oslogin.UpdateSshPublicKeyRequest):
                    The request object. A request message for updating an SSH
                public key.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.SshPublicKey:
                    The SSH public key information
                associated with a Google account.

            """

            http_options = (
                _BaseOsLoginServiceRestTransport._BaseUpdateSshPublicKey._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_ssh_public_key(
                request, metadata
            )
            transcoded_request = _BaseOsLoginServiceRestTransport._BaseUpdateSshPublicKey._get_transcoded_request(
                http_options, request
            )

            body = _BaseOsLoginServiceRestTransport._BaseUpdateSshPublicKey._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOsLoginServiceRestTransport._BaseUpdateSshPublicKey._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = OsLoginServiceRestTransport._UpdateSshPublicKey._get_response(
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
            resp = common.SshPublicKey()
            pb_resp = common.SshPublicKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_ssh_public_key(resp)
            return resp

    @property
    def create_ssh_public_key(
        self,
    ) -> Callable[[oslogin.CreateSshPublicKeyRequest], common.SshPublicKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSshPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_posix_account(
        self,
    ) -> Callable[[oslogin.DeletePosixAccountRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePosixAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_ssh_public_key(
        self,
    ) -> Callable[[oslogin.DeleteSshPublicKeyRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSshPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_login_profile(
        self,
    ) -> Callable[[oslogin.GetLoginProfileRequest], oslogin.LoginProfile]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLoginProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ssh_public_key(
        self,
    ) -> Callable[[oslogin.GetSshPublicKeyRequest], common.SshPublicKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSshPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_ssh_public_key(
        self,
    ) -> Callable[
        [oslogin.ImportSshPublicKeyRequest], oslogin.ImportSshPublicKeyResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportSshPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_ssh_public_key(
        self,
    ) -> Callable[[oslogin.UpdateSshPublicKeyRequest], common.SshPublicKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSshPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("OsLoginServiceRestTransport",)
