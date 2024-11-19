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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.ai.generativelanguage_v1beta.types import file, file_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseFileServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class FileServiceRestInterceptor:
    """Interceptor for FileService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the FileServiceRestTransport.

    .. code-block:: python
        class MyCustomFileServiceInterceptor(FileServiceRestInterceptor):
            def pre_create_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_files(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_files(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = FileServiceRestTransport(interceptor=MyCustomFileServiceInterceptor())
        client = FileServiceClient(transport=transport)


    """

    def pre_create_file(
        self,
        request: file_service.CreateFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[file_service.CreateFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FileService server.
        """
        return request, metadata

    def post_create_file(
        self, response: file_service.CreateFileResponse
    ) -> file_service.CreateFileResponse:
        """Post-rpc interceptor for create_file

        Override in a subclass to manipulate the response
        after it is returned by the FileService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_file(
        self,
        request: file_service.DeleteFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[file_service.DeleteFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FileService server.
        """
        return request, metadata

    def pre_get_file(
        self, request: file_service.GetFileRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[file_service.GetFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FileService server.
        """
        return request, metadata

    def post_get_file(self, response: file.File) -> file.File:
        """Post-rpc interceptor for get_file

        Override in a subclass to manipulate the response
        after it is returned by the FileService server but before
        it is returned to user code.
        """
        return response

    def pre_list_files(
        self,
        request: file_service.ListFilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[file_service.ListFilesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_files

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FileService server.
        """
        return request, metadata

    def post_list_files(
        self, response: file_service.ListFilesResponse
    ) -> file_service.ListFilesResponse:
        """Post-rpc interceptor for list_files

        Override in a subclass to manipulate the response
        after it is returned by the FileService server but before
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
        before they are sent to the FileService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the FileService server but before
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
        before they are sent to the FileService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the FileService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class FileServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: FileServiceRestInterceptor


class FileServiceRestTransport(_BaseFileServiceRestTransport):
    """REST backend synchronous transport for FileService.

    An API for uploading and managing files.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "generativelanguage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[FileServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'generativelanguage.googleapis.com').
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
        self._interceptor = interceptor or FileServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateFile(
        _BaseFileServiceRestTransport._BaseCreateFile, FileServiceRestStub
    ):
        def __hash__(self):
            return hash("FileServiceRestTransport.CreateFile")

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
            request: file_service.CreateFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> file_service.CreateFileResponse:
            r"""Call the create file method over HTTP.

            Args:
                request (~.file_service.CreateFileRequest):
                    The request object. Request for ``CreateFile``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.file_service.CreateFileResponse:
                    Response for ``CreateFile``.
            """

            http_options = (
                _BaseFileServiceRestTransport._BaseCreateFile._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_file(request, metadata)
            transcoded_request = (
                _BaseFileServiceRestTransport._BaseCreateFile._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseFileServiceRestTransport._BaseCreateFile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseFileServiceRestTransport._BaseCreateFile._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FileServiceRestTransport._CreateFile._get_response(
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
            resp = file_service.CreateFileResponse()
            pb_resp = file_service.CreateFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_file(resp)
            return resp

    class _DeleteFile(
        _BaseFileServiceRestTransport._BaseDeleteFile, FileServiceRestStub
    ):
        def __hash__(self):
            return hash("FileServiceRestTransport.DeleteFile")

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
            request: file_service.DeleteFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete file method over HTTP.

            Args:
                request (~.file_service.DeleteFileRequest):
                    The request object. Request for ``DeleteFile``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseFileServiceRestTransport._BaseDeleteFile._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_file(request, metadata)
            transcoded_request = (
                _BaseFileServiceRestTransport._BaseDeleteFile._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFileServiceRestTransport._BaseDeleteFile._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FileServiceRestTransport._DeleteFile._get_response(
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

    class _GetFile(_BaseFileServiceRestTransport._BaseGetFile, FileServiceRestStub):
        def __hash__(self):
            return hash("FileServiceRestTransport.GetFile")

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
            request: file_service.GetFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> file.File:
            r"""Call the get file method over HTTP.

            Args:
                request (~.file_service.GetFileRequest):
                    The request object. Request for ``GetFile``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.file.File:
                    A file uploaded to the API.
            """

            http_options = (
                _BaseFileServiceRestTransport._BaseGetFile._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_file(request, metadata)
            transcoded_request = (
                _BaseFileServiceRestTransport._BaseGetFile._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFileServiceRestTransport._BaseGetFile._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FileServiceRestTransport._GetFile._get_response(
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
            resp = file.File()
            pb_resp = file.File.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_file(resp)
            return resp

    class _ListFiles(_BaseFileServiceRestTransport._BaseListFiles, FileServiceRestStub):
        def __hash__(self):
            return hash("FileServiceRestTransport.ListFiles")

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
            request: file_service.ListFilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> file_service.ListFilesResponse:
            r"""Call the list files method over HTTP.

            Args:
                request (~.file_service.ListFilesRequest):
                    The request object. Request for ``ListFiles``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.file_service.ListFilesResponse:
                    Response for ``ListFiles``.
            """

            http_options = (
                _BaseFileServiceRestTransport._BaseListFiles._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_files(request, metadata)
            transcoded_request = (
                _BaseFileServiceRestTransport._BaseListFiles._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFileServiceRestTransport._BaseListFiles._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FileServiceRestTransport._ListFiles._get_response(
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
            resp = file_service.ListFilesResponse()
            pb_resp = file_service.ListFilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_files(resp)
            return resp

    @property
    def create_file(
        self,
    ) -> Callable[[file_service.CreateFileRequest], file_service.CreateFileResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_file(
        self,
    ) -> Callable[[file_service.DeleteFileRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_file(self) -> Callable[[file_service.GetFileRequest], file.File]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_files(
        self,
    ) -> Callable[[file_service.ListFilesRequest], file_service.ListFilesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseFileServiceRestTransport._BaseGetOperation, FileServiceRestStub
    ):
        def __hash__(self):
            return hash("FileServiceRestTransport.GetOperation")

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

            http_options = (
                _BaseFileServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseFileServiceRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFileServiceRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FileServiceRestTransport._GetOperation._get_response(
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
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseFileServiceRestTransport._BaseListOperations, FileServiceRestStub
    ):
        def __hash__(self):
            return hash("FileServiceRestTransport.ListOperations")

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

            http_options = (
                _BaseFileServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseFileServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFileServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FileServiceRestTransport._ListOperations._get_response(
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
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("FileServiceRestTransport",)
