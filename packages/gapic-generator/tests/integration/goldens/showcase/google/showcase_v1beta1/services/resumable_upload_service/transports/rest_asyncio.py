# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

import google.auth
try:
    import aiohttp # type: ignore
    from google.auth.aio.transport.sessions import AsyncAuthorizedSession # type: ignore
    from google.api_core import rest_streaming_async # type: ignore
    from google.api_core.operations_v1 import AsyncOperationsRestClient # type: ignore
except ImportError as e:  # pragma: NO COVER
    raise ImportError("`rest_asyncio` transport requires the library to be installed with the `async_rest` extra. Install the library with the `async_rest` extra using `pip install google-showcase[async_rest]`") from e

from google.auth.aio import credentials as ga_credentials_async  # type: ignore

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.cloud.location import locations_pb2 # type: ignore
from google.api_core import retry_async as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming_async  # type: ignore
from google.showcase_v1beta1._compat import transcode_request

import google.protobuf

from google.protobuf import json_format
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.cloud.location import locations_pb2 # type: ignore

import json  # type: ignore
import dataclasses
from typing import Any, Dict, List, Callable, Tuple, Optional, Sequence, Union


from google.showcase_v1beta1.types import resumable_upload
from google.longrunning import operations_pb2  # type: ignore


from .rest_base import _BaseResumableUploadServiceRestTransport

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


import logging

try:
    from google.api_core import client_logging  # type: ignore
    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"google-auth@{google.auth.__version__}",
)

DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class AsyncResumableUploadServiceRestInterceptor:
    """Asynchronous Interceptor for ResumableUploadService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AsyncResumableUploadServiceRestTransport.

    .. code-block:: python
        class MyCustomResumableUploadServiceInterceptor(ResumableUploadServiceRestInterceptor):
            async def pre_upload_media(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            async def post_upload_media(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AsyncResumableUploadServiceRestTransport(interceptor=MyCustomResumableUploadServiceInterceptor())
        client = async ResumableUploadServiceClient(transport=transport)


    """
    async def pre_upload_media(self, request: resumable_upload.UploadMediaRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[resumable_upload.UploadMediaRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for upload_media

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ResumableUploadService server.
        """
        return request, metadata

    async def post_upload_media(self, response: resumable_upload.UploadMediaResponse) -> resumable_upload.UploadMediaResponse:
        """Post-rpc interceptor for upload_media

        DEPRECATED. Please use the `post_upload_media_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ResumableUploadService server but before
        it is returned to user code. This `post_upload_media` interceptor runs
        before the `post_upload_media_with_metadata` interceptor.
        """
        return response

    async def post_upload_media_with_metadata(self, response: resumable_upload.UploadMediaResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[resumable_upload.UploadMediaResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for upload_media

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ResumableUploadService server but before it is returned to user code.

        We recommend only using this `post_upload_media_with_metadata`
        interceptor in new development instead of the `post_upload_media` interceptor.
        When both interceptors are used, this `post_upload_media_with_metadata` interceptor runs after the
        `post_upload_media` interceptor. The (possibly modified) response returned by
        `post_upload_media` will be passed to
        `post_upload_media_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class AsyncResumableUploadServiceRestStub:
    _session: AsyncAuthorizedSession
    _host: str
    _interceptor: AsyncResumableUploadServiceRestInterceptor

class AsyncResumableUploadServiceRestTransport(_BaseResumableUploadServiceRestTransport):
    """Asynchronous REST backend transport for ResumableUploadService.

    A service showcasing universal resumable upload protocol
    support.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """
    def __init__(self,
            *,
            host: str = 'localhost:7469',
            credentials: Optional[ga_credentials_async.Credentials] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            url_scheme: str = 'https',
            interceptor: Optional[AsyncResumableUploadServiceRestInterceptor] = None,
            ) -> None:
        """Instantiate the transport.

       NOTE: This async REST transport functionality is currently in a beta
       state (preview). We welcome your feedback via a GitHub issue in
       this library's repository. Thank you!

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'localhost:7469').
            credentials (Optional[google.auth.aio.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            url_scheme (str): the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
            interceptor (Optional[AsyncResumableUploadServiceRestInterceptor]): Interceptor used
                to manipulate requests, request metadata, and responses.
        """
        # Run the base constructor
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=False,
            url_scheme=url_scheme,
            api_audience=None
        )
        self._session = AsyncAuthorizedSession(self._credentials)  # type: ignore
        self._interceptor = interceptor or AsyncResumableUploadServiceRestInterceptor()
        self._wrap_with_kind = True
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        """ Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.upload_media: self._wrap_method(
                self.upload_media,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    class _UploadMedia(_BaseResumableUploadServiceRestTransport._BaseUploadMedia, AsyncResumableUploadServiceRestStub):
        def __hash__(self):
            return hash("AsyncResumableUploadServiceRestTransport.UploadMedia")

        @staticmethod
        async def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = await getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        async def __call__(self,
                    request: resumable_upload.UploadMediaRequest, *,
                    retry: OptionalRetry=gapic_v1.method.DEFAULT,
                    timeout: Optional[float]=None,
                    metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                    ) -> resumable_upload.UploadMediaResponse:
            r"""Call the upload media method over HTTP.

            Args:
                request (~.resumable_upload.UploadMediaRequest):
                    The request object.
                retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resumable_upload.UploadMediaResponse:

            """

            http_options = _BaseResumableUploadServiceRestTransport._BaseUploadMedia._get_http_options()
            request, metadata = await self._interceptor.pre_upload_media(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseResumableUploadServiceRestTransport._BaseUploadMedia,
                    "_BaseUploadMedia__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ResumableUploadServiceClient.UploadMedia",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.ResumableUploadService",
                        "rpcName": "UploadMedia",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = await AsyncResumableUploadServiceRestTransport._UploadMedia._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                content = await response.read()
                payload = json.loads(content.decode('utf-8'))
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
                raise core_exceptions.format_http_response_error(response, method, request_url, payload)  # type: ignore

            # Return the response
            resp = resumable_upload.UploadMediaResponse()
            pb_resp = resumable_upload.UploadMediaResponse.pb(resp)
            content = await response.read()
            # Resumable upload start responses return session metadata in headers with an empty body.
            if content and content.strip():
                json_format.Parse(content, pb_resp, ignore_unknown_fields=True)
            resp = await self._interceptor.post_upload_media(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = await self._interceptor.post_upload_media_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = resumable_upload.UploadMediaResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": "OK", # need to obtain this properly
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ResumableUploadServiceAsyncClient.upload_media",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.ResumableUploadService",
                        "rpcName": "UploadMedia",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )

            return resp

    @property
    def upload_media(self) -> Callable[
            [resumable_upload.UploadMediaRequest],
            resumable_upload.UploadMediaResponse]:
        return self._UploadMedia(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest_asyncio"

    async def close(self):
        await self._session.close()
