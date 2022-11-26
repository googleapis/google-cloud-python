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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.video.stitcher_v1.types import (
    ad_tag_details,
    cdn_keys,
    sessions,
    slates,
    stitch_details,
    video_stitcher_service,
)

from .base import DEFAULT_CLIENT_INFO, VideoStitcherServiceTransport


class VideoStitcherServiceGrpcTransport(VideoStitcherServiceTransport):
    """gRPC backend transport for VideoStitcherService.

    Video-On-Demand content stitching API allows you to insert
    ads into (VoD) video on demand files. You will be able to render
    custom scrubber bars with highlighted ads, enforce ad policies,
    allow seamless playback and tracking on native players and
    monetize content with any standard VMAP compliant ad server.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "videostitcher.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[grpc.Channel] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
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
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "videostitcher.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def create_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.CreateCdnKeyRequest], cdn_keys.CdnKey]:
        r"""Return a callable for the create cdn key method over gRPC.

        Creates a new CDN key.

        Returns:
            Callable[[~.CreateCdnKeyRequest],
                    ~.CdnKey]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_cdn_key" not in self._stubs:
            self._stubs["create_cdn_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/CreateCdnKey",
                request_serializer=video_stitcher_service.CreateCdnKeyRequest.serialize,
                response_deserializer=cdn_keys.CdnKey.deserialize,
            )
        return self._stubs["create_cdn_key"]

    @property
    def list_cdn_keys(
        self,
    ) -> Callable[
        [video_stitcher_service.ListCdnKeysRequest],
        video_stitcher_service.ListCdnKeysResponse,
    ]:
        r"""Return a callable for the list cdn keys method over gRPC.

        Lists all CDN keys in the specified project and
        location.

        Returns:
            Callable[[~.ListCdnKeysRequest],
                    ~.ListCdnKeysResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_cdn_keys" not in self._stubs:
            self._stubs["list_cdn_keys"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/ListCdnKeys",
                request_serializer=video_stitcher_service.ListCdnKeysRequest.serialize,
                response_deserializer=video_stitcher_service.ListCdnKeysResponse.deserialize,
            )
        return self._stubs["list_cdn_keys"]

    @property
    def get_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.GetCdnKeyRequest], cdn_keys.CdnKey]:
        r"""Return a callable for the get cdn key method over gRPC.

        Returns the specified CDN key.

        Returns:
            Callable[[~.GetCdnKeyRequest],
                    ~.CdnKey]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_cdn_key" not in self._stubs:
            self._stubs["get_cdn_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetCdnKey",
                request_serializer=video_stitcher_service.GetCdnKeyRequest.serialize,
                response_deserializer=cdn_keys.CdnKey.deserialize,
            )
        return self._stubs["get_cdn_key"]

    @property
    def delete_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.DeleteCdnKeyRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete cdn key method over gRPC.

        Deletes the specified CDN key.

        Returns:
            Callable[[~.DeleteCdnKeyRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_cdn_key" not in self._stubs:
            self._stubs["delete_cdn_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/DeleteCdnKey",
                request_serializer=video_stitcher_service.DeleteCdnKeyRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_cdn_key"]

    @property
    def update_cdn_key(
        self,
    ) -> Callable[[video_stitcher_service.UpdateCdnKeyRequest], cdn_keys.CdnKey]:
        r"""Return a callable for the update cdn key method over gRPC.

        Updates the specified CDN key. Only update fields
        specified in the call method body.

        Returns:
            Callable[[~.UpdateCdnKeyRequest],
                    ~.CdnKey]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_cdn_key" not in self._stubs:
            self._stubs["update_cdn_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/UpdateCdnKey",
                request_serializer=video_stitcher_service.UpdateCdnKeyRequest.serialize,
                response_deserializer=cdn_keys.CdnKey.deserialize,
            )
        return self._stubs["update_cdn_key"]

    @property
    def create_vod_session(
        self,
    ) -> Callable[
        [video_stitcher_service.CreateVodSessionRequest], sessions.VodSession
    ]:
        r"""Return a callable for the create vod session method over gRPC.

        Creates a client side playback VOD session and
        returns the full tracking and playback metadata of the
        session.

        Returns:
            Callable[[~.CreateVodSessionRequest],
                    ~.VodSession]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_vod_session" not in self._stubs:
            self._stubs["create_vod_session"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/CreateVodSession",
                request_serializer=video_stitcher_service.CreateVodSessionRequest.serialize,
                response_deserializer=sessions.VodSession.deserialize,
            )
        return self._stubs["create_vod_session"]

    @property
    def get_vod_session(
        self,
    ) -> Callable[[video_stitcher_service.GetVodSessionRequest], sessions.VodSession]:
        r"""Return a callable for the get vod session method over gRPC.

        Returns the full tracking, playback metadata, and
        relevant ad-ops logs for the specified VOD session.

        Returns:
            Callable[[~.GetVodSessionRequest],
                    ~.VodSession]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_vod_session" not in self._stubs:
            self._stubs["get_vod_session"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetVodSession",
                request_serializer=video_stitcher_service.GetVodSessionRequest.serialize,
                response_deserializer=sessions.VodSession.deserialize,
            )
        return self._stubs["get_vod_session"]

    @property
    def list_vod_stitch_details(
        self,
    ) -> Callable[
        [video_stitcher_service.ListVodStitchDetailsRequest],
        video_stitcher_service.ListVodStitchDetailsResponse,
    ]:
        r"""Return a callable for the list vod stitch details method over gRPC.

        Returns a list of detailed stitching information of
        the specified VOD session.

        Returns:
            Callable[[~.ListVodStitchDetailsRequest],
                    ~.ListVodStitchDetailsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_vod_stitch_details" not in self._stubs:
            self._stubs["list_vod_stitch_details"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/ListVodStitchDetails",
                request_serializer=video_stitcher_service.ListVodStitchDetailsRequest.serialize,
                response_deserializer=video_stitcher_service.ListVodStitchDetailsResponse.deserialize,
            )
        return self._stubs["list_vod_stitch_details"]

    @property
    def get_vod_stitch_detail(
        self,
    ) -> Callable[
        [video_stitcher_service.GetVodStitchDetailRequest],
        stitch_details.VodStitchDetail,
    ]:
        r"""Return a callable for the get vod stitch detail method over gRPC.

        Returns the specified stitching information for the
        specified VOD session.

        Returns:
            Callable[[~.GetVodStitchDetailRequest],
                    ~.VodStitchDetail]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_vod_stitch_detail" not in self._stubs:
            self._stubs["get_vod_stitch_detail"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetVodStitchDetail",
                request_serializer=video_stitcher_service.GetVodStitchDetailRequest.serialize,
                response_deserializer=stitch_details.VodStitchDetail.deserialize,
            )
        return self._stubs["get_vod_stitch_detail"]

    @property
    def list_vod_ad_tag_details(
        self,
    ) -> Callable[
        [video_stitcher_service.ListVodAdTagDetailsRequest],
        video_stitcher_service.ListVodAdTagDetailsResponse,
    ]:
        r"""Return a callable for the list vod ad tag details method over gRPC.

        Return the list of ad tag details for the specified
        VOD session.

        Returns:
            Callable[[~.ListVodAdTagDetailsRequest],
                    ~.ListVodAdTagDetailsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_vod_ad_tag_details" not in self._stubs:
            self._stubs["list_vod_ad_tag_details"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/ListVodAdTagDetails",
                request_serializer=video_stitcher_service.ListVodAdTagDetailsRequest.serialize,
                response_deserializer=video_stitcher_service.ListVodAdTagDetailsResponse.deserialize,
            )
        return self._stubs["list_vod_ad_tag_details"]

    @property
    def get_vod_ad_tag_detail(
        self,
    ) -> Callable[
        [video_stitcher_service.GetVodAdTagDetailRequest], ad_tag_details.VodAdTagDetail
    ]:
        r"""Return a callable for the get vod ad tag detail method over gRPC.

        Returns the specified ad tag detail for the specified
        VOD session.

        Returns:
            Callable[[~.GetVodAdTagDetailRequest],
                    ~.VodAdTagDetail]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_vod_ad_tag_detail" not in self._stubs:
            self._stubs["get_vod_ad_tag_detail"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetVodAdTagDetail",
                request_serializer=video_stitcher_service.GetVodAdTagDetailRequest.serialize,
                response_deserializer=ad_tag_details.VodAdTagDetail.deserialize,
            )
        return self._stubs["get_vod_ad_tag_detail"]

    @property
    def list_live_ad_tag_details(
        self,
    ) -> Callable[
        [video_stitcher_service.ListLiveAdTagDetailsRequest],
        video_stitcher_service.ListLiveAdTagDetailsResponse,
    ]:
        r"""Return a callable for the list live ad tag details method over gRPC.

        Return the list of ad tag details for the specified
        live session.

        Returns:
            Callable[[~.ListLiveAdTagDetailsRequest],
                    ~.ListLiveAdTagDetailsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_live_ad_tag_details" not in self._stubs:
            self._stubs["list_live_ad_tag_details"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/ListLiveAdTagDetails",
                request_serializer=video_stitcher_service.ListLiveAdTagDetailsRequest.serialize,
                response_deserializer=video_stitcher_service.ListLiveAdTagDetailsResponse.deserialize,
            )
        return self._stubs["list_live_ad_tag_details"]

    @property
    def get_live_ad_tag_detail(
        self,
    ) -> Callable[
        [video_stitcher_service.GetLiveAdTagDetailRequest],
        ad_tag_details.LiveAdTagDetail,
    ]:
        r"""Return a callable for the get live ad tag detail method over gRPC.

        Returns the specified ad tag detail for the specified
        live session.

        Returns:
            Callable[[~.GetLiveAdTagDetailRequest],
                    ~.LiveAdTagDetail]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_live_ad_tag_detail" not in self._stubs:
            self._stubs["get_live_ad_tag_detail"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetLiveAdTagDetail",
                request_serializer=video_stitcher_service.GetLiveAdTagDetailRequest.serialize,
                response_deserializer=ad_tag_details.LiveAdTagDetail.deserialize,
            )
        return self._stubs["get_live_ad_tag_detail"]

    @property
    def create_slate(
        self,
    ) -> Callable[[video_stitcher_service.CreateSlateRequest], slates.Slate]:
        r"""Return a callable for the create slate method over gRPC.

        Creates a slate.

        Returns:
            Callable[[~.CreateSlateRequest],
                    ~.Slate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_slate" not in self._stubs:
            self._stubs["create_slate"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/CreateSlate",
                request_serializer=video_stitcher_service.CreateSlateRequest.serialize,
                response_deserializer=slates.Slate.deserialize,
            )
        return self._stubs["create_slate"]

    @property
    def list_slates(
        self,
    ) -> Callable[
        [video_stitcher_service.ListSlatesRequest],
        video_stitcher_service.ListSlatesResponse,
    ]:
        r"""Return a callable for the list slates method over gRPC.

        Lists all slates in the specified project and
        location.

        Returns:
            Callable[[~.ListSlatesRequest],
                    ~.ListSlatesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_slates" not in self._stubs:
            self._stubs["list_slates"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/ListSlates",
                request_serializer=video_stitcher_service.ListSlatesRequest.serialize,
                response_deserializer=video_stitcher_service.ListSlatesResponse.deserialize,
            )
        return self._stubs["list_slates"]

    @property
    def get_slate(
        self,
    ) -> Callable[[video_stitcher_service.GetSlateRequest], slates.Slate]:
        r"""Return a callable for the get slate method over gRPC.

        Returns the specified slate.

        Returns:
            Callable[[~.GetSlateRequest],
                    ~.Slate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_slate" not in self._stubs:
            self._stubs["get_slate"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetSlate",
                request_serializer=video_stitcher_service.GetSlateRequest.serialize,
                response_deserializer=slates.Slate.deserialize,
            )
        return self._stubs["get_slate"]

    @property
    def update_slate(
        self,
    ) -> Callable[[video_stitcher_service.UpdateSlateRequest], slates.Slate]:
        r"""Return a callable for the update slate method over gRPC.

        Updates the specified slate.

        Returns:
            Callable[[~.UpdateSlateRequest],
                    ~.Slate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_slate" not in self._stubs:
            self._stubs["update_slate"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/UpdateSlate",
                request_serializer=video_stitcher_service.UpdateSlateRequest.serialize,
                response_deserializer=slates.Slate.deserialize,
            )
        return self._stubs["update_slate"]

    @property
    def delete_slate(
        self,
    ) -> Callable[[video_stitcher_service.DeleteSlateRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete slate method over gRPC.

        Deletes the specified slate.

        Returns:
            Callable[[~.DeleteSlateRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_slate" not in self._stubs:
            self._stubs["delete_slate"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/DeleteSlate",
                request_serializer=video_stitcher_service.DeleteSlateRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_slate"]

    @property
    def create_live_session(
        self,
    ) -> Callable[
        [video_stitcher_service.CreateLiveSessionRequest], sessions.LiveSession
    ]:
        r"""Return a callable for the create live session method over gRPC.

        Creates a new live session.

        Returns:
            Callable[[~.CreateLiveSessionRequest],
                    ~.LiveSession]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_live_session" not in self._stubs:
            self._stubs["create_live_session"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/CreateLiveSession",
                request_serializer=video_stitcher_service.CreateLiveSessionRequest.serialize,
                response_deserializer=sessions.LiveSession.deserialize,
            )
        return self._stubs["create_live_session"]

    @property
    def get_live_session(
        self,
    ) -> Callable[[video_stitcher_service.GetLiveSessionRequest], sessions.LiveSession]:
        r"""Return a callable for the get live session method over gRPC.

        Returns the details for the specified live session.

        Returns:
            Callable[[~.GetLiveSessionRequest],
                    ~.LiveSession]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_live_session" not in self._stubs:
            self._stubs["get_live_session"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.stitcher.v1.VideoStitcherService/GetLiveSession",
                request_serializer=video_stitcher_service.GetLiveSessionRequest.serialize,
                response_deserializer=sessions.LiveSession.deserialize,
            )
        return self._stubs["get_live_session"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("VideoStitcherServiceGrpcTransport",)
