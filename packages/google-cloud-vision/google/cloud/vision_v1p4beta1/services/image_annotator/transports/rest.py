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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.vision_v1p4beta1.types import image_annotator

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseImageAnnotatorRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ImageAnnotatorRestInterceptor:
    """Interceptor for ImageAnnotator.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ImageAnnotatorRestTransport.

    .. code-block:: python
        class MyCustomImageAnnotatorInterceptor(ImageAnnotatorRestInterceptor):
            def pre_async_batch_annotate_files(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_async_batch_annotate_files(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_async_batch_annotate_images(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_async_batch_annotate_images(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_annotate_files(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_annotate_files(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_annotate_images(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_annotate_images(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ImageAnnotatorRestTransport(interceptor=MyCustomImageAnnotatorInterceptor())
        client = ImageAnnotatorClient(transport=transport)


    """

    def pre_async_batch_annotate_files(
        self,
        request: image_annotator.AsyncBatchAnnotateFilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        image_annotator.AsyncBatchAnnotateFilesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for async_batch_annotate_files

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageAnnotator server.
        """
        return request, metadata

    def post_async_batch_annotate_files(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for async_batch_annotate_files

        Override in a subclass to manipulate the response
        after it is returned by the ImageAnnotator server but before
        it is returned to user code.
        """
        return response

    def pre_async_batch_annotate_images(
        self,
        request: image_annotator.AsyncBatchAnnotateImagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        image_annotator.AsyncBatchAnnotateImagesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for async_batch_annotate_images

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageAnnotator server.
        """
        return request, metadata

    def post_async_batch_annotate_images(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for async_batch_annotate_images

        Override in a subclass to manipulate the response
        after it is returned by the ImageAnnotator server but before
        it is returned to user code.
        """
        return response

    def pre_batch_annotate_files(
        self,
        request: image_annotator.BatchAnnotateFilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[image_annotator.BatchAnnotateFilesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_annotate_files

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageAnnotator server.
        """
        return request, metadata

    def post_batch_annotate_files(
        self, response: image_annotator.BatchAnnotateFilesResponse
    ) -> image_annotator.BatchAnnotateFilesResponse:
        """Post-rpc interceptor for batch_annotate_files

        Override in a subclass to manipulate the response
        after it is returned by the ImageAnnotator server but before
        it is returned to user code.
        """
        return response

    def pre_batch_annotate_images(
        self,
        request: image_annotator.BatchAnnotateImagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[image_annotator.BatchAnnotateImagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_annotate_images

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ImageAnnotator server.
        """
        return request, metadata

    def post_batch_annotate_images(
        self, response: image_annotator.BatchAnnotateImagesResponse
    ) -> image_annotator.BatchAnnotateImagesResponse:
        """Post-rpc interceptor for batch_annotate_images

        Override in a subclass to manipulate the response
        after it is returned by the ImageAnnotator server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ImageAnnotatorRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ImageAnnotatorRestInterceptor


class ImageAnnotatorRestTransport(_BaseImageAnnotatorRestTransport):
    """REST backend synchronous transport for ImageAnnotator.

    Service that performs Google Cloud Vision API detection tasks
    over client images, such as face, landmark, logo, label, and
    text detection. The ImageAnnotator service returns detected
    entities from the images.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ImageAnnotatorRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'vision.googleapis.com').
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
        self._interceptor = interceptor or ImageAnnotatorRestInterceptor()
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
                path_prefix="v1p4beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _AsyncBatchAnnotateFiles(
        _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateFiles,
        ImageAnnotatorRestStub,
    ):
        def __hash__(self):
            return hash("ImageAnnotatorRestTransport.AsyncBatchAnnotateFiles")

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
            request: image_annotator.AsyncBatchAnnotateFilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the async batch annotate
            files method over HTTP.

                Args:
                    request (~.image_annotator.AsyncBatchAnnotateFilesRequest):
                        The request object. Multiple async file annotation
                    requests are batched into a single
                    service call.
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

            http_options = (
                _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateFiles._get_http_options()
            )
            request, metadata = self._interceptor.pre_async_batch_annotate_files(
                request, metadata
            )
            transcoded_request = _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateFiles._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateFiles._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateFiles._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ImageAnnotatorRestTransport._AsyncBatchAnnotateFiles._get_response(
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
            resp = self._interceptor.post_async_batch_annotate_files(resp)
            return resp

    class _AsyncBatchAnnotateImages(
        _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateImages,
        ImageAnnotatorRestStub,
    ):
        def __hash__(self):
            return hash("ImageAnnotatorRestTransport.AsyncBatchAnnotateImages")

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
            request: image_annotator.AsyncBatchAnnotateImagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the async batch annotate
            images method over HTTP.

                Args:
                    request (~.image_annotator.AsyncBatchAnnotateImagesRequest):
                        The request object. Request for async image annotation
                    for a list of images.
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

            http_options = (
                _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateImages._get_http_options()
            )
            request, metadata = self._interceptor.pre_async_batch_annotate_images(
                request, metadata
            )
            transcoded_request = _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateImages._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateImages._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageAnnotatorRestTransport._BaseAsyncBatchAnnotateImages._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ImageAnnotatorRestTransport._AsyncBatchAnnotateImages._get_response(
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
            resp = self._interceptor.post_async_batch_annotate_images(resp)
            return resp

    class _BatchAnnotateFiles(
        _BaseImageAnnotatorRestTransport._BaseBatchAnnotateFiles, ImageAnnotatorRestStub
    ):
        def __hash__(self):
            return hash("ImageAnnotatorRestTransport.BatchAnnotateFiles")

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
            request: image_annotator.BatchAnnotateFilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> image_annotator.BatchAnnotateFilesResponse:
            r"""Call the batch annotate files method over HTTP.

            Args:
                request (~.image_annotator.BatchAnnotateFilesRequest):
                    The request object. A list of requests to annotate files
                using the BatchAnnotateFiles API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.image_annotator.BatchAnnotateFilesResponse:
                    A list of file annotation responses.
            """

            http_options = (
                _BaseImageAnnotatorRestTransport._BaseBatchAnnotateFiles._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_annotate_files(
                request, metadata
            )
            transcoded_request = _BaseImageAnnotatorRestTransport._BaseBatchAnnotateFiles._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageAnnotatorRestTransport._BaseBatchAnnotateFiles._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageAnnotatorRestTransport._BaseBatchAnnotateFiles._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ImageAnnotatorRestTransport._BatchAnnotateFiles._get_response(
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
            resp = image_annotator.BatchAnnotateFilesResponse()
            pb_resp = image_annotator.BatchAnnotateFilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_annotate_files(resp)
            return resp

    class _BatchAnnotateImages(
        _BaseImageAnnotatorRestTransport._BaseBatchAnnotateImages,
        ImageAnnotatorRestStub,
    ):
        def __hash__(self):
            return hash("ImageAnnotatorRestTransport.BatchAnnotateImages")

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
            request: image_annotator.BatchAnnotateImagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> image_annotator.BatchAnnotateImagesResponse:
            r"""Call the batch annotate images method over HTTP.

            Args:
                request (~.image_annotator.BatchAnnotateImagesRequest):
                    The request object. Multiple image annotation requests
                are batched into a single service call.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.image_annotator.BatchAnnotateImagesResponse:
                    Response to a batch image annotation
                request.

            """

            http_options = (
                _BaseImageAnnotatorRestTransport._BaseBatchAnnotateImages._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_annotate_images(
                request, metadata
            )
            transcoded_request = _BaseImageAnnotatorRestTransport._BaseBatchAnnotateImages._get_transcoded_request(
                http_options, request
            )

            body = _BaseImageAnnotatorRestTransport._BaseBatchAnnotateImages._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseImageAnnotatorRestTransport._BaseBatchAnnotateImages._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ImageAnnotatorRestTransport._BatchAnnotateImages._get_response(
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
            resp = image_annotator.BatchAnnotateImagesResponse()
            pb_resp = image_annotator.BatchAnnotateImagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_annotate_images(resp)
            return resp

    @property
    def async_batch_annotate_files(
        self,
    ) -> Callable[
        [image_annotator.AsyncBatchAnnotateFilesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AsyncBatchAnnotateFiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def async_batch_annotate_images(
        self,
    ) -> Callable[
        [image_annotator.AsyncBatchAnnotateImagesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AsyncBatchAnnotateImages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_annotate_files(
        self,
    ) -> Callable[
        [image_annotator.BatchAnnotateFilesRequest],
        image_annotator.BatchAnnotateFilesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchAnnotateFiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_annotate_images(
        self,
    ) -> Callable[
        [image_annotator.BatchAnnotateImagesRequest],
        image_annotator.BatchAnnotateImagesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchAnnotateImages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ImageAnnotatorRestTransport",)
