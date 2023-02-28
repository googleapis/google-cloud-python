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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
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


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.video.stitcher_v1.types import (
    ad_tag_details,
    cdn_keys,
    sessions,
    slates,
    stitch_details,
    video_stitcher_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import VideoStitcherServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class VideoStitcherServiceRestInterceptor:
    """Interceptor for VideoStitcherService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the VideoStitcherServiceRestTransport.

    .. code-block:: python
        class MyCustomVideoStitcherServiceInterceptor(VideoStitcherServiceRestInterceptor):
            def pre_create_cdn_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cdn_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_live_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_live_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_slate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_slate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_vod_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_vod_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cdn_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_slate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_cdn_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cdn_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_live_ad_tag_detail(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_live_ad_tag_detail(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_live_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_live_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_slate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_slate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_vod_ad_tag_detail(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_vod_ad_tag_detail(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_vod_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_vod_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_vod_stitch_detail(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_vod_stitch_detail(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cdn_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cdn_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_live_ad_tag_details(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_live_ad_tag_details(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_slates(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_slates(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_vod_ad_tag_details(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_vod_ad_tag_details(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_vod_stitch_details(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_vod_stitch_details(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cdn_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cdn_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_slate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_slate(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = VideoStitcherServiceRestTransport(interceptor=MyCustomVideoStitcherServiceInterceptor())
        client = VideoStitcherServiceClient(transport=transport)


    """

    def pre_create_cdn_key(
        self,
        request: video_stitcher_service.CreateCdnKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.CreateCdnKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cdn_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_create_cdn_key(self, response: cdn_keys.CdnKey) -> cdn_keys.CdnKey:
        """Post-rpc interceptor for create_cdn_key

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_create_live_session(
        self,
        request: video_stitcher_service.CreateLiveSessionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.CreateLiveSessionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_live_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_create_live_session(
        self, response: sessions.LiveSession
    ) -> sessions.LiveSession:
        """Post-rpc interceptor for create_live_session

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_create_slate(
        self,
        request: video_stitcher_service.CreateSlateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.CreateSlateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_slate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_create_slate(self, response: slates.Slate) -> slates.Slate:
        """Post-rpc interceptor for create_slate

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_create_vod_session(
        self,
        request: video_stitcher_service.CreateVodSessionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.CreateVodSessionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_vod_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_create_vod_session(
        self, response: sessions.VodSession
    ) -> sessions.VodSession:
        """Post-rpc interceptor for create_vod_session

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cdn_key(
        self,
        request: video_stitcher_service.DeleteCdnKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.DeleteCdnKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cdn_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def pre_delete_slate(
        self,
        request: video_stitcher_service.DeleteSlateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.DeleteSlateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_slate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def pre_get_cdn_key(
        self,
        request: video_stitcher_service.GetCdnKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.GetCdnKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cdn_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_cdn_key(self, response: cdn_keys.CdnKey) -> cdn_keys.CdnKey:
        """Post-rpc interceptor for get_cdn_key

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_get_live_ad_tag_detail(
        self,
        request: video_stitcher_service.GetLiveAdTagDetailRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.GetLiveAdTagDetailRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_live_ad_tag_detail

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_live_ad_tag_detail(
        self, response: ad_tag_details.LiveAdTagDetail
    ) -> ad_tag_details.LiveAdTagDetail:
        """Post-rpc interceptor for get_live_ad_tag_detail

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_get_live_session(
        self,
        request: video_stitcher_service.GetLiveSessionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.GetLiveSessionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_live_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_live_session(
        self, response: sessions.LiveSession
    ) -> sessions.LiveSession:
        """Post-rpc interceptor for get_live_session

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_get_slate(
        self,
        request: video_stitcher_service.GetSlateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.GetSlateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_slate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_slate(self, response: slates.Slate) -> slates.Slate:
        """Post-rpc interceptor for get_slate

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_get_vod_ad_tag_detail(
        self,
        request: video_stitcher_service.GetVodAdTagDetailRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.GetVodAdTagDetailRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_vod_ad_tag_detail

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_vod_ad_tag_detail(
        self, response: ad_tag_details.VodAdTagDetail
    ) -> ad_tag_details.VodAdTagDetail:
        """Post-rpc interceptor for get_vod_ad_tag_detail

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_get_vod_session(
        self,
        request: video_stitcher_service.GetVodSessionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.GetVodSessionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_vod_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_vod_session(
        self, response: sessions.VodSession
    ) -> sessions.VodSession:
        """Post-rpc interceptor for get_vod_session

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_get_vod_stitch_detail(
        self,
        request: video_stitcher_service.GetVodStitchDetailRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.GetVodStitchDetailRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_vod_stitch_detail

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_get_vod_stitch_detail(
        self, response: stitch_details.VodStitchDetail
    ) -> stitch_details.VodStitchDetail:
        """Post-rpc interceptor for get_vod_stitch_detail

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_list_cdn_keys(
        self,
        request: video_stitcher_service.ListCdnKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.ListCdnKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_cdn_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_list_cdn_keys(
        self, response: video_stitcher_service.ListCdnKeysResponse
    ) -> video_stitcher_service.ListCdnKeysResponse:
        """Post-rpc interceptor for list_cdn_keys

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_list_live_ad_tag_details(
        self,
        request: video_stitcher_service.ListLiveAdTagDetailsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.ListLiveAdTagDetailsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_live_ad_tag_details

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_list_live_ad_tag_details(
        self, response: video_stitcher_service.ListLiveAdTagDetailsResponse
    ) -> video_stitcher_service.ListLiveAdTagDetailsResponse:
        """Post-rpc interceptor for list_live_ad_tag_details

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_list_slates(
        self,
        request: video_stitcher_service.ListSlatesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.ListSlatesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_slates

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_list_slates(
        self, response: video_stitcher_service.ListSlatesResponse
    ) -> video_stitcher_service.ListSlatesResponse:
        """Post-rpc interceptor for list_slates

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_list_vod_ad_tag_details(
        self,
        request: video_stitcher_service.ListVodAdTagDetailsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.ListVodAdTagDetailsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_vod_ad_tag_details

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_list_vod_ad_tag_details(
        self, response: video_stitcher_service.ListVodAdTagDetailsResponse
    ) -> video_stitcher_service.ListVodAdTagDetailsResponse:
        """Post-rpc interceptor for list_vod_ad_tag_details

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_list_vod_stitch_details(
        self,
        request: video_stitcher_service.ListVodStitchDetailsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        video_stitcher_service.ListVodStitchDetailsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_vod_stitch_details

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_list_vod_stitch_details(
        self, response: video_stitcher_service.ListVodStitchDetailsResponse
    ) -> video_stitcher_service.ListVodStitchDetailsResponse:
        """Post-rpc interceptor for list_vod_stitch_details

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_update_cdn_key(
        self,
        request: video_stitcher_service.UpdateCdnKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.UpdateCdnKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cdn_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_update_cdn_key(self, response: cdn_keys.CdnKey) -> cdn_keys.CdnKey:
        """Post-rpc interceptor for update_cdn_key

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response

    def pre_update_slate(
        self,
        request: video_stitcher_service.UpdateSlateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[video_stitcher_service.UpdateSlateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_slate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VideoStitcherService server.
        """
        return request, metadata

    def post_update_slate(self, response: slates.Slate) -> slates.Slate:
        """Post-rpc interceptor for update_slate

        Override in a subclass to manipulate the response
        after it is returned by the VideoStitcherService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class VideoStitcherServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: VideoStitcherServiceRestInterceptor


class VideoStitcherServiceRestTransport(VideoStitcherServiceTransport):
    """REST backend transport for VideoStitcherService.

    Video-On-Demand content stitching API allows you to insert
    ads into (VoD) video on demand files. You will be able to render
    custom scrubber bars with highlighted ads, enforce ad policies,
    allow seamless playback and tracking on native players and
    monetize content with any standard VMAP compliant ad server.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "videostitcher.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[VideoStitcherServiceRestInterceptor] = None,
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or VideoStitcherServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateCdnKey(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("CreateCdnKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "cdnKeyId": "",
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
            request: video_stitcher_service.CreateCdnKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cdn_keys.CdnKey:
            r"""Call the create cdn key method over HTTP.

            Args:
                request (~.video_stitcher_service.CreateCdnKeyRequest):
                    The request object. Request message for
                VideoStitcherService.createCdnKey.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cdn_keys.CdnKey:
                    Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/cdnKeys",
                    "body": "cdn_key",
                },
            ]
            request, metadata = self._interceptor.pre_create_cdn_key(request, metadata)
            pb_request = video_stitcher_service.CreateCdnKeyRequest.pb(request)
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
            resp = cdn_keys.CdnKey()
            pb_resp = cdn_keys.CdnKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_cdn_key(resp)
            return resp

    class _CreateLiveSession(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("CreateLiveSession")

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
            request: video_stitcher_service.CreateLiveSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sessions.LiveSession:
            r"""Call the create live session method over HTTP.

            Args:
                request (~.video_stitcher_service.CreateLiveSessionRequest):
                    The request object. Request message for
                VideoStitcherService.createLiveSession.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sessions.LiveSession:
                    Metadata for a live session.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/liveSessions",
                    "body": "live_session",
                },
            ]
            request, metadata = self._interceptor.pre_create_live_session(
                request, metadata
            )
            pb_request = video_stitcher_service.CreateLiveSessionRequest.pb(request)
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
            resp = sessions.LiveSession()
            pb_resp = sessions.LiveSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_live_session(resp)
            return resp

    class _CreateSlate(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("CreateSlate")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "slateId": "",
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
            request: video_stitcher_service.CreateSlateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> slates.Slate:
            r"""Call the create slate method over HTTP.

            Args:
                request (~.video_stitcher_service.CreateSlateRequest):
                    The request object. Request message for
                VideoStitcherService.createSlate.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.slates.Slate:
                    Slate object
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/slates",
                    "body": "slate",
                },
            ]
            request, metadata = self._interceptor.pre_create_slate(request, metadata)
            pb_request = video_stitcher_service.CreateSlateRequest.pb(request)
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
            resp = slates.Slate()
            pb_resp = slates.Slate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_slate(resp)
            return resp

    class _CreateVodSession(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("CreateVodSession")

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
            request: video_stitcher_service.CreateVodSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sessions.VodSession:
            r"""Call the create vod session method over HTTP.

            Args:
                request (~.video_stitcher_service.CreateVodSessionRequest):
                    The request object. Request message for
                VideoStitcherService.createVodSession

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sessions.VodSession:
                    Metadata for a VOD session.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/vodSessions",
                    "body": "vod_session",
                },
            ]
            request, metadata = self._interceptor.pre_create_vod_session(
                request, metadata
            )
            pb_request = video_stitcher_service.CreateVodSessionRequest.pb(request)
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
            resp = sessions.VodSession()
            pb_resp = sessions.VodSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_vod_session(resp)
            return resp

    class _DeleteCdnKey(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("DeleteCdnKey")

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
            request: video_stitcher_service.DeleteCdnKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete cdn key method over HTTP.

            Args:
                request (~.video_stitcher_service.DeleteCdnKeyRequest):
                    The request object. Request message for
                VideoStitcherService.deleteCdnKey.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/cdnKeys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_cdn_key(request, metadata)
            pb_request = video_stitcher_service.DeleteCdnKeyRequest.pb(request)
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

    class _DeleteSlate(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("DeleteSlate")

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
            request: video_stitcher_service.DeleteSlateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete slate method over HTTP.

            Args:
                request (~.video_stitcher_service.DeleteSlateRequest):
                    The request object. Request message for
                VideoStitcherService.deleteSlate.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/slates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_slate(request, metadata)
            pb_request = video_stitcher_service.DeleteSlateRequest.pb(request)
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

    class _GetCdnKey(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetCdnKey")

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
            request: video_stitcher_service.GetCdnKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cdn_keys.CdnKey:
            r"""Call the get cdn key method over HTTP.

            Args:
                request (~.video_stitcher_service.GetCdnKeyRequest):
                    The request object. Request message for
                VideoStitcherService.getCdnKey.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cdn_keys.CdnKey:
                    Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/cdnKeys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_cdn_key(request, metadata)
            pb_request = video_stitcher_service.GetCdnKeyRequest.pb(request)
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
            resp = cdn_keys.CdnKey()
            pb_resp = cdn_keys.CdnKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cdn_key(resp)
            return resp

    class _GetLiveAdTagDetail(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetLiveAdTagDetail")

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
            request: video_stitcher_service.GetLiveAdTagDetailRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ad_tag_details.LiveAdTagDetail:
            r"""Call the get live ad tag detail method over HTTP.

            Args:
                request (~.video_stitcher_service.GetLiveAdTagDetailRequest):
                    The request object. Request message for
                VideoStitcherService.getLiveAdTagDetail

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ad_tag_details.LiveAdTagDetail:
                    Container for a live session's ad tag
                detail.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/liveSessions/*/liveAdTagDetails/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_live_ad_tag_detail(
                request, metadata
            )
            pb_request = video_stitcher_service.GetLiveAdTagDetailRequest.pb(request)
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
            resp = ad_tag_details.LiveAdTagDetail()
            pb_resp = ad_tag_details.LiveAdTagDetail.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_live_ad_tag_detail(resp)
            return resp

    class _GetLiveSession(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetLiveSession")

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
            request: video_stitcher_service.GetLiveSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sessions.LiveSession:
            r"""Call the get live session method over HTTP.

            Args:
                request (~.video_stitcher_service.GetLiveSessionRequest):
                    The request object. Request message for
                VideoStitcherService.getSession.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sessions.LiveSession:
                    Metadata for a live session.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/liveSessions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_live_session(
                request, metadata
            )
            pb_request = video_stitcher_service.GetLiveSessionRequest.pb(request)
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
            resp = sessions.LiveSession()
            pb_resp = sessions.LiveSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_live_session(resp)
            return resp

    class _GetSlate(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetSlate")

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
            request: video_stitcher_service.GetSlateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> slates.Slate:
            r"""Call the get slate method over HTTP.

            Args:
                request (~.video_stitcher_service.GetSlateRequest):
                    The request object. Request message for
                VideoStitcherService.getSlate.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.slates.Slate:
                    Slate object
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/slates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_slate(request, metadata)
            pb_request = video_stitcher_service.GetSlateRequest.pb(request)
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
            resp = slates.Slate()
            pb_resp = slates.Slate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_slate(resp)
            return resp

    class _GetVodAdTagDetail(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetVodAdTagDetail")

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
            request: video_stitcher_service.GetVodAdTagDetailRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ad_tag_details.VodAdTagDetail:
            r"""Call the get vod ad tag detail method over HTTP.

            Args:
                request (~.video_stitcher_service.GetVodAdTagDetailRequest):
                    The request object. Request message for
                VideoStitcherService.getVodAdTagDetail

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ad_tag_details.VodAdTagDetail:
                    Information related to the details
                for one ad tag.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/vodSessions/*/vodAdTagDetails/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_vod_ad_tag_detail(
                request, metadata
            )
            pb_request = video_stitcher_service.GetVodAdTagDetailRequest.pb(request)
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
            resp = ad_tag_details.VodAdTagDetail()
            pb_resp = ad_tag_details.VodAdTagDetail.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_vod_ad_tag_detail(resp)
            return resp

    class _GetVodSession(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetVodSession")

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
            request: video_stitcher_service.GetVodSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sessions.VodSession:
            r"""Call the get vod session method over HTTP.

            Args:
                request (~.video_stitcher_service.GetVodSessionRequest):
                    The request object. Request message for
                VideoStitcherService.getVodSession

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sessions.VodSession:
                    Metadata for a VOD session.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/vodSessions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_vod_session(request, metadata)
            pb_request = video_stitcher_service.GetVodSessionRequest.pb(request)
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
            resp = sessions.VodSession()
            pb_resp = sessions.VodSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_vod_session(resp)
            return resp

    class _GetVodStitchDetail(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("GetVodStitchDetail")

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
            request: video_stitcher_service.GetVodStitchDetailRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> stitch_details.VodStitchDetail:
            r"""Call the get vod stitch detail method over HTTP.

            Args:
                request (~.video_stitcher_service.GetVodStitchDetailRequest):
                    The request object. Request message for
                VideoStitcherService.getVodStitchDetail.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.stitch_details.VodStitchDetail:
                    Detailed information related to the
                interstitial of a VOD session.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/vodSessions/*/vodStitchDetails/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_vod_stitch_detail(
                request, metadata
            )
            pb_request = video_stitcher_service.GetVodStitchDetailRequest.pb(request)
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
            resp = stitch_details.VodStitchDetail()
            pb_resp = stitch_details.VodStitchDetail.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_vod_stitch_detail(resp)
            return resp

    class _ListCdnKeys(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("ListCdnKeys")

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
            request: video_stitcher_service.ListCdnKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> video_stitcher_service.ListCdnKeysResponse:
            r"""Call the list cdn keys method over HTTP.

            Args:
                request (~.video_stitcher_service.ListCdnKeysRequest):
                    The request object. Request message for
                VideoStitcherService.listCdnKeys.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.video_stitcher_service.ListCdnKeysResponse:
                    Response message for
                VideoStitcher.ListCdnKeys.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/cdnKeys",
                },
            ]
            request, metadata = self._interceptor.pre_list_cdn_keys(request, metadata)
            pb_request = video_stitcher_service.ListCdnKeysRequest.pb(request)
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
            resp = video_stitcher_service.ListCdnKeysResponse()
            pb_resp = video_stitcher_service.ListCdnKeysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_cdn_keys(resp)
            return resp

    class _ListLiveAdTagDetails(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("ListLiveAdTagDetails")

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
            request: video_stitcher_service.ListLiveAdTagDetailsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> video_stitcher_service.ListLiveAdTagDetailsResponse:
            r"""Call the list live ad tag details method over HTTP.

            Args:
                request (~.video_stitcher_service.ListLiveAdTagDetailsRequest):
                    The request object. Request message for
                VideoStitcherService.listLiveAdTagDetails.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.video_stitcher_service.ListLiveAdTagDetailsResponse:
                    Response message for
                VideoStitcherService.listLiveAdTagDetails.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/liveSessions/*}/liveAdTagDetails",
                },
            ]
            request, metadata = self._interceptor.pre_list_live_ad_tag_details(
                request, metadata
            )
            pb_request = video_stitcher_service.ListLiveAdTagDetailsRequest.pb(request)
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
            resp = video_stitcher_service.ListLiveAdTagDetailsResponse()
            pb_resp = video_stitcher_service.ListLiveAdTagDetailsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_live_ad_tag_details(resp)
            return resp

    class _ListSlates(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("ListSlates")

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
            request: video_stitcher_service.ListSlatesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> video_stitcher_service.ListSlatesResponse:
            r"""Call the list slates method over HTTP.

            Args:
                request (~.video_stitcher_service.ListSlatesRequest):
                    The request object. Request message for
                VideoStitcherService.listSlates.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.video_stitcher_service.ListSlatesResponse:
                    Response message for
                VideoStitcherService.listSlates.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/slates",
                },
            ]
            request, metadata = self._interceptor.pre_list_slates(request, metadata)
            pb_request = video_stitcher_service.ListSlatesRequest.pb(request)
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
            resp = video_stitcher_service.ListSlatesResponse()
            pb_resp = video_stitcher_service.ListSlatesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_slates(resp)
            return resp

    class _ListVodAdTagDetails(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("ListVodAdTagDetails")

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
            request: video_stitcher_service.ListVodAdTagDetailsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> video_stitcher_service.ListVodAdTagDetailsResponse:
            r"""Call the list vod ad tag details method over HTTP.

            Args:
                request (~.video_stitcher_service.ListVodAdTagDetailsRequest):
                    The request object. Request message for
                VideoStitcherService.listVodAdTagDetails.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.video_stitcher_service.ListVodAdTagDetailsResponse:
                    Response message for
                VideoStitcherService.listVodAdTagDetails.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/vodSessions/*}/vodAdTagDetails",
                },
            ]
            request, metadata = self._interceptor.pre_list_vod_ad_tag_details(
                request, metadata
            )
            pb_request = video_stitcher_service.ListVodAdTagDetailsRequest.pb(request)
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
            resp = video_stitcher_service.ListVodAdTagDetailsResponse()
            pb_resp = video_stitcher_service.ListVodAdTagDetailsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_vod_ad_tag_details(resp)
            return resp

    class _ListVodStitchDetails(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("ListVodStitchDetails")

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
            request: video_stitcher_service.ListVodStitchDetailsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> video_stitcher_service.ListVodStitchDetailsResponse:
            r"""Call the list vod stitch details method over HTTP.

            Args:
                request (~.video_stitcher_service.ListVodStitchDetailsRequest):
                    The request object. Request message for
                VideoStitcherService.listVodStitchDetails.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.video_stitcher_service.ListVodStitchDetailsResponse:
                    Response message for
                VideoStitcherService.listVodStitchDetails.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/vodSessions/*}/vodStitchDetails",
                },
            ]
            request, metadata = self._interceptor.pre_list_vod_stitch_details(
                request, metadata
            )
            pb_request = video_stitcher_service.ListVodStitchDetailsRequest.pb(request)
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
            resp = video_stitcher_service.ListVodStitchDetailsResponse()
            pb_resp = video_stitcher_service.ListVodStitchDetailsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_vod_stitch_details(resp)
            return resp

    class _UpdateCdnKey(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("UpdateCdnKey")

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
            request: video_stitcher_service.UpdateCdnKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cdn_keys.CdnKey:
            r"""Call the update cdn key method over HTTP.

            Args:
                request (~.video_stitcher_service.UpdateCdnKeyRequest):
                    The request object. Request message for
                VideoStitcherService.updateCdnKey.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cdn_keys.CdnKey:
                    Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{cdn_key.name=projects/*/locations/*/cdnKeys/*}",
                    "body": "cdn_key",
                },
            ]
            request, metadata = self._interceptor.pre_update_cdn_key(request, metadata)
            pb_request = video_stitcher_service.UpdateCdnKeyRequest.pb(request)
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
            resp = cdn_keys.CdnKey()
            pb_resp = cdn_keys.CdnKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_cdn_key(resp)
            return resp

    class _UpdateSlate(VideoStitcherServiceRestStub):
        def __hash__(self):
            return hash("UpdateSlate")

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
            request: video_stitcher_service.UpdateSlateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> slates.Slate:
            r"""Call the update slate method over HTTP.

            Args:
                request (~.video_stitcher_service.UpdateSlateRequest):
                    The request object. Request message for
                VideoStitcherService.updateSlate.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.slates.Slate:
                    Slate object
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{slate.name=projects/*/locations/*/slates/*}",
                    "body": "slate",
                },
            ]
            request, metadata = self._interceptor.pre_update_slate(request, metadata)
            pb_request = video_stitcher_service.UpdateSlateRequest.pb(request)
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
            resp = slates.Slate()
            pb_resp = slates.Slate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_slate(resp)
            return resp

    @property
    def create_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.CreateCdnKeyRequest], cdn_keys.CdnKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCdnKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_live_session(
        self,
    ) -> Callable[
        [video_stitcher_service.CreateLiveSessionRequest], sessions.LiveSession
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateLiveSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_slate(
        self,
    ) -> Callable[[video_stitcher_service.CreateSlateRequest], slates.Slate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSlate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_vod_session(
        self,
    ) -> Callable[
        [video_stitcher_service.CreateVodSessionRequest], sessions.VodSession
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateVodSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.DeleteCdnKeyRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCdnKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_slate(
        self,
    ) -> Callable[[video_stitcher_service.DeleteSlateRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSlate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.GetCdnKeyRequest], cdn_keys.CdnKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCdnKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_live_ad_tag_detail(
        self,
    ) -> Callable[
        [video_stitcher_service.GetLiveAdTagDetailRequest],
        ad_tag_details.LiveAdTagDetail,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLiveAdTagDetail(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_live_session(
        self,
    ) -> Callable[[video_stitcher_service.GetLiveSessionRequest], sessions.LiveSession]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLiveSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_slate(
        self,
    ) -> Callable[[video_stitcher_service.GetSlateRequest], slates.Slate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSlate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_vod_ad_tag_detail(
        self,
    ) -> Callable[
        [video_stitcher_service.GetVodAdTagDetailRequest], ad_tag_details.VodAdTagDetail
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVodAdTagDetail(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_vod_session(
        self,
    ) -> Callable[[video_stitcher_service.GetVodSessionRequest], sessions.VodSession]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVodSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_vod_stitch_detail(
        self,
    ) -> Callable[
        [video_stitcher_service.GetVodStitchDetailRequest],
        stitch_details.VodStitchDetail,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVodStitchDetail(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_cdn_keys(
        self,
    ) -> Callable[
        [video_stitcher_service.ListCdnKeysRequest],
        video_stitcher_service.ListCdnKeysResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCdnKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_live_ad_tag_details(
        self,
    ) -> Callable[
        [video_stitcher_service.ListLiveAdTagDetailsRequest],
        video_stitcher_service.ListLiveAdTagDetailsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLiveAdTagDetails(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_slates(
        self,
    ) -> Callable[
        [video_stitcher_service.ListSlatesRequest],
        video_stitcher_service.ListSlatesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSlates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_vod_ad_tag_details(
        self,
    ) -> Callable[
        [video_stitcher_service.ListVodAdTagDetailsRequest],
        video_stitcher_service.ListVodAdTagDetailsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVodAdTagDetails(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_vod_stitch_details(
        self,
    ) -> Callable[
        [video_stitcher_service.ListVodStitchDetailsRequest],
        video_stitcher_service.ListVodStitchDetailsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVodStitchDetails(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.UpdateCdnKeyRequest], cdn_keys.CdnKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCdnKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_slate(
        self,
    ) -> Callable[[video_stitcher_service.UpdateSlateRequest], slates.Slate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSlate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("VideoStitcherServiceRestTransport",)
