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
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.video.stitcher_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore

from google.cloud.video.stitcher_v1.services.video_stitcher_service import pagers
from google.cloud.video.stitcher_v1.types import (
    ad_tag_details,
    cdn_keys,
    sessions,
    slates,
    stitch_details,
    video_stitcher_service,
)

from .transports.base import DEFAULT_CLIENT_INFO, VideoStitcherServiceTransport
from .transports.grpc import VideoStitcherServiceGrpcTransport
from .transports.grpc_asyncio import VideoStitcherServiceGrpcAsyncIOTransport
from .transports.rest import VideoStitcherServiceRestTransport


class VideoStitcherServiceClientMeta(type):
    """Metaclass for the VideoStitcherService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[VideoStitcherServiceTransport]]
    _transport_registry["grpc"] = VideoStitcherServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = VideoStitcherServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = VideoStitcherServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[VideoStitcherServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class VideoStitcherServiceClient(metaclass=VideoStitcherServiceClientMeta):
    """Video-On-Demand content stitching API allows you to insert
    ads into (VoD) video on demand files. You will be able to render
    custom scrubber bars with highlighted ads, enforce ad policies,
    allow seamless playback and tracking on native players and
    monetize content with any standard VMAP compliant ad server.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "videostitcher.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            VideoStitcherServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            VideoStitcherServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> VideoStitcherServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            VideoStitcherServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def cdn_key_path(
        project: str,
        location: str,
        cdn_key: str,
    ) -> str:
        """Returns a fully-qualified cdn_key string."""
        return "projects/{project}/locations/{location}/cdnKeys/{cdn_key}".format(
            project=project,
            location=location,
            cdn_key=cdn_key,
        )

    @staticmethod
    def parse_cdn_key_path(path: str) -> Dict[str, str]:
        """Parses a cdn_key path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/cdnKeys/(?P<cdn_key>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def live_ad_tag_detail_path(
        project: str,
        location: str,
        live_session: str,
        live_ad_tag_detail: str,
    ) -> str:
        """Returns a fully-qualified live_ad_tag_detail string."""
        return "projects/{project}/locations/{location}/liveSessions/{live_session}/liveAdTagDetails/{live_ad_tag_detail}".format(
            project=project,
            location=location,
            live_session=live_session,
            live_ad_tag_detail=live_ad_tag_detail,
        )

    @staticmethod
    def parse_live_ad_tag_detail_path(path: str) -> Dict[str, str]:
        """Parses a live_ad_tag_detail path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/liveSessions/(?P<live_session>.+?)/liveAdTagDetails/(?P<live_ad_tag_detail>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def live_session_path(
        project: str,
        location: str,
        live_session: str,
    ) -> str:
        """Returns a fully-qualified live_session string."""
        return "projects/{project}/locations/{location}/liveSessions/{live_session}".format(
            project=project,
            location=location,
            live_session=live_session,
        )

    @staticmethod
    def parse_live_session_path(path: str) -> Dict[str, str]:
        """Parses a live_session path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/liveSessions/(?P<live_session>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def slate_path(
        project: str,
        location: str,
        slate: str,
    ) -> str:
        """Returns a fully-qualified slate string."""
        return "projects/{project}/locations/{location}/slates/{slate}".format(
            project=project,
            location=location,
            slate=slate,
        )

    @staticmethod
    def parse_slate_path(path: str) -> Dict[str, str]:
        """Parses a slate path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/slates/(?P<slate>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def vod_ad_tag_detail_path(
        project: str,
        location: str,
        vod_session: str,
        vod_ad_tag_detail: str,
    ) -> str:
        """Returns a fully-qualified vod_ad_tag_detail string."""
        return "projects/{project}/locations/{location}/vodSessions/{vod_session}/vodAdTagDetails/{vod_ad_tag_detail}".format(
            project=project,
            location=location,
            vod_session=vod_session,
            vod_ad_tag_detail=vod_ad_tag_detail,
        )

    @staticmethod
    def parse_vod_ad_tag_detail_path(path: str) -> Dict[str, str]:
        """Parses a vod_ad_tag_detail path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/vodSessions/(?P<vod_session>.+?)/vodAdTagDetails/(?P<vod_ad_tag_detail>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def vod_session_path(
        project: str,
        location: str,
        vod_session: str,
    ) -> str:
        """Returns a fully-qualified vod_session string."""
        return (
            "projects/{project}/locations/{location}/vodSessions/{vod_session}".format(
                project=project,
                location=location,
                vod_session=vod_session,
            )
        )

    @staticmethod
    def parse_vod_session_path(path: str) -> Dict[str, str]:
        """Parses a vod_session path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/vodSessions/(?P<vod_session>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def vod_stitch_detail_path(
        project: str,
        location: str,
        vod_session: str,
        vod_stitch_detail: str,
    ) -> str:
        """Returns a fully-qualified vod_stitch_detail string."""
        return "projects/{project}/locations/{location}/vodSessions/{vod_session}/vodStitchDetails/{vod_stitch_detail}".format(
            project=project,
            location=location,
            vod_session=vod_session,
            vod_stitch_detail=vod_stitch_detail,
        )

    @staticmethod
    def parse_vod_stitch_detail_path(path: str) -> Dict[str, str]:
        """Parses a vod_stitch_detail path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/vodSessions/(?P<vod_session>.+?)/vodStitchDetails/(?P<vod_stitch_detail>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, VideoStitcherServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the video stitcher service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, VideoStitcherServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, VideoStitcherServiceTransport):
            # transport is a VideoStitcherServiceTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def create_cdn_key(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateCdnKeyRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        cdn_key: Optional[cdn_keys.CdnKey] = None,
        cdn_key_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cdn_keys.CdnKey:
        r"""Creates a new CDN key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_create_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.CreateCdnKeyRequest(
                    parent="parent_value",
                    cdn_key_id="cdn_key_id_value",
                )

                # Make the request
                response = client.create_cdn_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.CreateCdnKeyRequest, dict]):
                The request object. Request message for
                VideoStitcherService.createCdnKey.
            parent (str):
                Required. The project in which the CDN key should be
                created, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cdn_key (google.cloud.video.stitcher_v1.types.CdnKey):
                Required. The CDN key resource to
                create.

                This corresponds to the ``cdn_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cdn_key_id (str):
                Required. The ID to use for the CDN
                key, which will become the final
                component of the CDN key's resource
                name.
                This value should conform to RFC-1034,
                which restricts to lower-case letters,
                numbers, and hyphen, with the first
                character a letter, the last a letter or
                a number, and a 63 character maximum.

                This corresponds to the ``cdn_key_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.CdnKey:
                Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, cdn_key, cdn_key_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.CreateCdnKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.CreateCdnKeyRequest):
            request = video_stitcher_service.CreateCdnKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if cdn_key is not None:
                request.cdn_key = cdn_key
            if cdn_key_id is not None:
                request.cdn_key_id = cdn_key_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_cdn_key]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_cdn_keys(
        self,
        request: Optional[
            Union[video_stitcher_service.ListCdnKeysRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCdnKeysPager:
        r"""Lists all CDN keys in the specified project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_list_cdn_keys():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListCdnKeysRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_cdn_keys(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.ListCdnKeysRequest, dict]):
                The request object. Request message for
                VideoStitcherService.listCdnKeys.
            parent (str):
                Required. The project that contains the list of CDN
                keys, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListCdnKeysPager:
                Response message for
                VideoStitcher.ListCdnKeys.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.ListCdnKeysRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.ListCdnKeysRequest):
            request = video_stitcher_service.ListCdnKeysRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_cdn_keys]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCdnKeysPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_cdn_key(
        self,
        request: Optional[Union[video_stitcher_service.GetCdnKeyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cdn_keys.CdnKey:
        r"""Returns the specified CDN key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetCdnKeyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_cdn_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetCdnKeyRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getCdnKey.
            name (str):
                Required. The name of the CDN key to be retrieved, in
                the form of
                ``projects/{project}/locations/{location}/cdnKeys/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.CdnKey:
                Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetCdnKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetCdnKeyRequest):
            request = video_stitcher_service.GetCdnKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_cdn_key]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_cdn_key(
        self,
        request: Optional[
            Union[video_stitcher_service.DeleteCdnKeyRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified CDN key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_delete_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.DeleteCdnKeyRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_cdn_key(request=request)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.DeleteCdnKeyRequest, dict]):
                The request object. Request message for
                VideoStitcherService.deleteCdnKey.
            name (str):
                Required. The name of the CDN key to be deleted, in the
                form of
                ``projects/{project_number}/locations/{location}/cdnKeys/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.DeleteCdnKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.DeleteCdnKeyRequest):
            request = video_stitcher_service.DeleteCdnKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_cdn_key]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_cdn_key(
        self,
        request: Optional[
            Union[video_stitcher_service.UpdateCdnKeyRequest, dict]
        ] = None,
        *,
        cdn_key: Optional[cdn_keys.CdnKey] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cdn_keys.CdnKey:
        r"""Updates the specified CDN key. Only update fields
        specified in the call method body.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_update_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.UpdateCdnKeyRequest(
                )

                # Make the request
                response = client.update_cdn_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.UpdateCdnKeyRequest, dict]):
                The request object. Request message for
                VideoStitcherService.updateCdnKey.
            cdn_key (google.cloud.video.stitcher_v1.types.CdnKey):
                Required. The CDN key resource which
                replaces the resource on the server.

                This corresponds to the ``cdn_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.CdnKey:
                Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([cdn_key, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.UpdateCdnKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.UpdateCdnKeyRequest):
            request = video_stitcher_service.UpdateCdnKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if cdn_key is not None:
                request.cdn_key = cdn_key
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_cdn_key]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("cdn_key.name", request.cdn_key.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_vod_session(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateVodSessionRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        vod_session: Optional[sessions.VodSession] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.VodSession:
        r"""Creates a client side playback VOD session and
        returns the full tracking and playback metadata of the
        session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_create_vod_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                vod_session = stitcher_v1.VodSession()
                vod_session.source_uri = "source_uri_value"
                vod_session.ad_tag_uri = "ad_tag_uri_value"

                request = stitcher_v1.CreateVodSessionRequest(
                    parent="parent_value",
                    vod_session=vod_session,
                )

                # Make the request
                response = client.create_vod_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.CreateVodSessionRequest, dict]):
                The request object. Request message for
                VideoStitcherService.createVodSession
            parent (str):
                Required. The project and location in which the VOD
                session should be created, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            vod_session (google.cloud.video.stitcher_v1.types.VodSession):
                Required. Parameters for creating a
                session.

                This corresponds to the ``vod_session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodSession:
                Metadata for a VOD session.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, vod_session])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.CreateVodSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.CreateVodSessionRequest):
            request = video_stitcher_service.CreateVodSessionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if vod_session is not None:
                request.vod_session = vod_session

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_vod_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_vod_session(
        self,
        request: Optional[
            Union[video_stitcher_service.GetVodSessionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.VodSession:
        r"""Returns the full tracking, playback metadata, and
        relevant ad-ops logs for the specified VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_vod_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetVodSessionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_vod_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetVodSessionRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getVodSession
            name (str):
                Required. The name of the VOD session to be retrieved,
                in the form of
                ``projects/{project_number}/locations/{location}/vodSessions/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodSession:
                Metadata for a VOD session.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetVodSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetVodSessionRequest):
            request = video_stitcher_service.GetVodSessionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_vod_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_vod_stitch_details(
        self,
        request: Optional[
            Union[video_stitcher_service.ListVodStitchDetailsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVodStitchDetailsPager:
        r"""Returns a list of detailed stitching information of
        the specified VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_list_vod_stitch_details():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListVodStitchDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_vod_stitch_details(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.ListVodStitchDetailsRequest, dict]):
                The request object. Request message for
                VideoStitcherService.listVodStitchDetails.
            parent (str):
                Required. The VOD session where the stitch details
                belong to, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListVodStitchDetailsPager:
                Response message for
                VideoStitcherService.listVodStitchDetails.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.ListVodStitchDetailsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.ListVodStitchDetailsRequest):
            request = video_stitcher_service.ListVodStitchDetailsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_vod_stitch_details]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListVodStitchDetailsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_vod_stitch_detail(
        self,
        request: Optional[
            Union[video_stitcher_service.GetVodStitchDetailRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> stitch_details.VodStitchDetail:
        r"""Returns the specified stitching information for the
        specified VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_vod_stitch_detail():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetVodStitchDetailRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_vod_stitch_detail(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetVodStitchDetailRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getVodStitchDetail.
            name (str):
                Required. The name of the stitch detail in the specified
                VOD session, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}/vodStitchDetails/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodStitchDetail:
                Detailed information related to the
                interstitial of a VOD session.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetVodStitchDetailRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetVodStitchDetailRequest):
            request = video_stitcher_service.GetVodStitchDetailRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_vod_stitch_detail]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_vod_ad_tag_details(
        self,
        request: Optional[
            Union[video_stitcher_service.ListVodAdTagDetailsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVodAdTagDetailsPager:
        r"""Return the list of ad tag details for the specified
        VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_list_vod_ad_tag_details():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListVodAdTagDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_vod_ad_tag_details(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsRequest, dict]):
                The request object. Request message for
                VideoStitcherService.listVodAdTagDetails.
            parent (str):
                Required. The VOD session which the ad tag details
                belong to, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListVodAdTagDetailsPager:
                Response message for
                VideoStitcherService.listVodAdTagDetails.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.ListVodAdTagDetailsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.ListVodAdTagDetailsRequest):
            request = video_stitcher_service.ListVodAdTagDetailsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_vod_ad_tag_details]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListVodAdTagDetailsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_vod_ad_tag_detail(
        self,
        request: Optional[
            Union[video_stitcher_service.GetVodAdTagDetailRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ad_tag_details.VodAdTagDetail:
        r"""Returns the specified ad tag detail for the specified
        VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_vod_ad_tag_detail():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetVodAdTagDetailRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_vod_ad_tag_detail(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetVodAdTagDetailRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getVodAdTagDetail
            name (str):
                Required. The name of the ad tag detail for the
                specified VOD session, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}/vodAdTagDetails/{vod_ad_tag_detail}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodAdTagDetail:
                Information related to the details
                for one ad tag.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetVodAdTagDetailRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetVodAdTagDetailRequest):
            request = video_stitcher_service.GetVodAdTagDetailRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_vod_ad_tag_detail]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_live_ad_tag_details(
        self,
        request: Optional[
            Union[video_stitcher_service.ListLiveAdTagDetailsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLiveAdTagDetailsPager:
        r"""Return the list of ad tag details for the specified
        live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_list_live_ad_tag_details():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListLiveAdTagDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_live_ad_tag_details(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsRequest, dict]):
                The request object. Request message for
                VideoStitcherService.listLiveAdTagDetails.
            parent (str):
                Required. The resource parent in the form of
                ``projects/{project}/locations/{location}/liveSessions/{live_session}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListLiveAdTagDetailsPager:
                Response message for
                VideoStitcherService.listLiveAdTagDetails.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.ListLiveAdTagDetailsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.ListLiveAdTagDetailsRequest):
            request = video_stitcher_service.ListLiveAdTagDetailsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_live_ad_tag_details]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListLiveAdTagDetailsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_live_ad_tag_detail(
        self,
        request: Optional[
            Union[video_stitcher_service.GetLiveAdTagDetailRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ad_tag_details.LiveAdTagDetail:
        r"""Returns the specified ad tag detail for the specified
        live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_live_ad_tag_detail():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetLiveAdTagDetailRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_live_ad_tag_detail(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetLiveAdTagDetailRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getLiveAdTagDetail
            name (str):
                Required. The resource name in the form of
                ``projects/{project}/locations/{location}/liveSessions/{live_session}/liveAdTagDetails/{live_ad_tag_detail}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.LiveAdTagDetail:
                Container for a live session's ad tag
                detail.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetLiveAdTagDetailRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetLiveAdTagDetailRequest):
            request = video_stitcher_service.GetLiveAdTagDetailRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_live_ad_tag_detail]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_slate(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateSlateRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        slate: Optional[slates.Slate] = None,
        slate_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> slates.Slate:
        r"""Creates a slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_create_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.CreateSlateRequest(
                    parent="parent_value",
                    slate_id="slate_id_value",
                )

                # Make the request
                response = client.create_slate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.CreateSlateRequest, dict]):
                The request object. Request message for
                VideoStitcherService.createSlate.
            parent (str):
                Required. The project in which the slate should be
                created, in the form of ``projects/{project_number}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            slate (google.cloud.video.stitcher_v1.types.Slate):
                Required. The slate to create.
                This corresponds to the ``slate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            slate_id (str):
                Required. The unique identifier for
                the slate. This value should conform to
                RFC-1034, which restricts to lower-case
                letters, numbers, and hyphen, with the
                first character a letter, the last a
                letter or a number, and a 63 character
                maximum.

                This corresponds to the ``slate_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.Slate:
                Slate object
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, slate, slate_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.CreateSlateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.CreateSlateRequest):
            request = video_stitcher_service.CreateSlateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if slate is not None:
                request.slate = slate
            if slate_id is not None:
                request.slate_id = slate_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_slate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_slates(
        self,
        request: Optional[Union[video_stitcher_service.ListSlatesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSlatesPager:
        r"""Lists all slates in the specified project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_list_slates():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListSlatesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_slates(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.ListSlatesRequest, dict]):
                The request object. Request message for
                VideoStitcherService.listSlates.
            parent (str):
                Required. The project to list slates, in the form of
                ``projects/{project_number}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListSlatesPager:
                Response message for
                VideoStitcherService.listSlates.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.ListSlatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.ListSlatesRequest):
            request = video_stitcher_service.ListSlatesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_slates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSlatesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_slate(
        self,
        request: Optional[Union[video_stitcher_service.GetSlateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> slates.Slate:
        r"""Returns the specified slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetSlateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_slate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetSlateRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getSlate.
            name (str):
                Required. The name of the slate to be retrieved, of the
                slate, in the form of
                ``projects/{project_number}/locations/{location}/slates/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.Slate:
                Slate object
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetSlateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetSlateRequest):
            request = video_stitcher_service.GetSlateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_slate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_slate(
        self,
        request: Optional[
            Union[video_stitcher_service.UpdateSlateRequest, dict]
        ] = None,
        *,
        slate: Optional[slates.Slate] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> slates.Slate:
        r"""Updates the specified slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_update_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.UpdateSlateRequest(
                )

                # Make the request
                response = client.update_slate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.UpdateSlateRequest, dict]):
                The request object. Request message for
                VideoStitcherService.updateSlate.
            slate (google.cloud.video.stitcher_v1.types.Slate):
                Required. The resource with updated
                fields.

                This corresponds to the ``slate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask which
                specifies fields which should be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.Slate:
                Slate object
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([slate, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.UpdateSlateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.UpdateSlateRequest):
            request = video_stitcher_service.UpdateSlateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if slate is not None:
                request.slate = slate
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_slate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("slate.name", request.slate.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_slate(
        self,
        request: Optional[
            Union[video_stitcher_service.DeleteSlateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_delete_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.DeleteSlateRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_slate(request=request)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.DeleteSlateRequest, dict]):
                The request object. Request message for
                VideoStitcherService.deleteSlate.
            name (str):
                Required. The name of the slate to be deleted, in the
                form of
                ``projects/{project_number}/locations/{location}/slates/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.DeleteSlateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.DeleteSlateRequest):
            request = video_stitcher_service.DeleteSlateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_slate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_live_session(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateLiveSessionRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        live_session: Optional[sessions.LiveSession] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.LiveSession:
        r"""Creates a new live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_create_live_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.CreateLiveSessionRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_live_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.CreateLiveSessionRequest, dict]):
                The request object. Request message for
                VideoStitcherService.createLiveSession.
            parent (str):
                Required. The project and location in which the live
                session should be created, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            live_session (google.cloud.video.stitcher_v1.types.LiveSession):
                Required. Parameters for creating a
                live session.

                This corresponds to the ``live_session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.LiveSession:
                Metadata for a live session.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, live_session])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.CreateLiveSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.CreateLiveSessionRequest):
            request = video_stitcher_service.CreateLiveSessionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if live_session is not None:
                request.live_session = live_session

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_live_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_live_session(
        self,
        request: Optional[
            Union[video_stitcher_service.GetLiveSessionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.LiveSession:
        r"""Returns the details for the specified live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            def sample_get_live_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetLiveSessionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_live_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.stitcher_v1.types.GetLiveSessionRequest, dict]):
                The request object. Request message for
                VideoStitcherService.getSession.
            name (str):
                Required. The name of the live session, in the form of
                ``projects/{project_number}/locations/{location}/liveSessions/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.LiveSession:
                Metadata for a live session.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a video_stitcher_service.GetLiveSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, video_stitcher_service.GetLiveSessionRequest):
            request = video_stitcher_service.GetLiveSessionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_live_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("VideoStitcherServiceClient",)
