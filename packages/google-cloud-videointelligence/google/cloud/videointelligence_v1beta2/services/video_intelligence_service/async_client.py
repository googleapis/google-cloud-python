# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.videointelligence_v1beta2.types import video_intelligence
from .transports.base import VideoIntelligenceServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import VideoIntelligenceServiceGrpcAsyncIOTransport
from .client import VideoIntelligenceServiceClient


class VideoIntelligenceServiceAsyncClient:
    """Service that implements Google Cloud Video Intelligence API."""

    _client: VideoIntelligenceServiceClient

    DEFAULT_ENDPOINT = VideoIntelligenceServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = VideoIntelligenceServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        VideoIntelligenceServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        VideoIntelligenceServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(VideoIntelligenceServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        VideoIntelligenceServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        VideoIntelligenceServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        VideoIntelligenceServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        VideoIntelligenceServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        VideoIntelligenceServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        VideoIntelligenceServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        VideoIntelligenceServiceClient.parse_common_location_path
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
            VideoIntelligenceServiceAsyncClient: The constructed client.
        """
        return VideoIntelligenceServiceClient.from_service_account_info.__func__(VideoIntelligenceServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            VideoIntelligenceServiceAsyncClient: The constructed client.
        """
        return VideoIntelligenceServiceClient.from_service_account_file.__func__(VideoIntelligenceServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> VideoIntelligenceServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            VideoIntelligenceServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(VideoIntelligenceServiceClient).get_transport_class,
        type(VideoIntelligenceServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, VideoIntelligenceServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the video intelligence service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.VideoIntelligenceServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
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

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = VideoIntelligenceServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def annotate_video(
        self,
        request: video_intelligence.AnnotateVideoRequest = None,
        *,
        input_uri: str = None,
        features: Sequence[video_intelligence.Feature] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Performs asynchronous video annotation. Progress and results can
        be retrieved through the ``google.longrunning.Operations``
        interface. ``Operation.metadata`` contains
        ``AnnotateVideoProgress`` (progress). ``Operation.response``
        contains ``AnnotateVideoResponse`` (results).

        Args:
            request (:class:`google.cloud.videointelligence_v1beta2.types.AnnotateVideoRequest`):
                The request object. Video annotation request.
            input_uri (:class:`str`):
                Input video location. Currently, only `Google Cloud
                Storage <https://cloud.google.com/storage/>`__ URIs are
                supported, which must be specified in the following
                format: ``gs://bucket-id/object-id`` (other URI formats
                return
                [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT]).
                For more information, see `Request
                URIs <https://cloud.google.com/storage/docs/request-endpoints>`__.
                A video URI may include wildcards in ``object-id``, and
                thus identify multiple videos. Supported wildcards: '*'
                to match 0 or more characters; '?' to match 1 character.
                If unset, the input video should be embedded in the
                request as ``input_content``. If set, ``input_content``
                should be unset.

                This corresponds to the ``input_uri`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            features (:class:`Sequence[google.cloud.videointelligence_v1beta2.types.Feature]`):
                Required. Requested video annotation
                features.

                This corresponds to the ``features`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.videointelligence_v1beta2.types.AnnotateVideoResponse` Video annotation response. Included in the response
                   field of the Operation returned by the GetOperation
                   call of the google::longrunning::Operations service.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([input_uri, features])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_intelligence.AnnotateVideoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if input_uri is not None:
            request.input_uri = input_uri
        if features:
            request.features.extend(features)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.annotate_video,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=120.0,
                multiplier=2.5,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            video_intelligence.AnnotateVideoResponse,
            metadata_type=video_intelligence.AnnotateVideoProgress,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-videointelligence",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("VideoIntelligenceServiceAsyncClient",)
