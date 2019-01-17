# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.cloud.videointelligence.v1p1beta1 VideoIntelligenceService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import grpc

from google.cloud.videointelligence_v1p1beta1.gapic import enums
from google.cloud.videointelligence_v1p1beta1.gapic import (
    video_intelligence_service_client_config,
)
from google.cloud.videointelligence_v1p1beta1.gapic.transports import (
    video_intelligence_service_grpc_transport,
)
from google.cloud.videointelligence_v1p1beta1.proto import video_intelligence_pb2
from google.cloud.videointelligence_v1p1beta1.proto import video_intelligence_pb2_grpc
from google.longrunning import operations_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-videointelligence"
).version


class VideoIntelligenceServiceClient(object):
    """Service that implements Google Cloud Video Intelligence API."""

    SERVICE_ADDRESS = "videointelligence.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = (
        "google.cloud.videointelligence.v1p1beta1.VideoIntelligenceService"
    )

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            VideoIntelligenceServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.VideoIntelligenceServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.VideoIntelligenceServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = video_intelligence_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=video_intelligence_service_grpc_transport.VideoIntelligenceServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = video_intelligence_service_grpc_transport.VideoIntelligenceServiceGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def annotate_video(
        self,
        input_uri=None,
        input_content=None,
        features=None,
        video_context=None,
        output_uri=None,
        location_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Performs asynchronous video annotation. Progress and results can be
        retrieved through the ``google.longrunning.Operations`` interface.
        ``Operation.metadata`` contains ``AnnotateVideoProgress`` (progress).
        ``Operation.response`` contains ``AnnotateVideoResponse`` (results).

        Example:
            >>> from google.cloud import videointelligence_v1p1beta1
            >>> from google.cloud.videointelligence_v1p1beta1 import enums
            >>>
            >>> client = videointelligence_v1p1beta1.VideoIntelligenceServiceClient()
            >>>
            >>> input_uri = 'gs://demomaker/cat.mp4'
            >>> features_element = enums.Feature.LABEL_DETECTION
            >>> features = [features_element]
            >>>
            >>> response = client.annotate_video(input_uri=input_uri, features=features)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            input_uri (str): Input video location. Currently, only `Google Cloud
                Storage <https://cloud.google.com/storage/>`__ URIs are supported, which
                must be specified in the following format: ``gs://bucket-id/object-id``
                (other URI formats return ``google.rpc.Code.INVALID_ARGUMENT``). For
                more information, see `Request
                URIs <https://cloud.google.com/storage/docs/reference-uris>`__. A video
                URI may include wildcards in ``object-id``, and thus identify multiple
                videos. Supported wildcards: '\*' to match 0 or more characters; '?' to
                match 1 character. If unset, the input video should be embedded in the
                request as ``input_content``. If set, ``input_content`` should be unset.
            input_content (bytes): The video data bytes. If unset, the input video(s) should be specified
                via ``input_uri``. If set, ``input_uri`` should be unset.
            features (list[~google.cloud.videointelligence_v1p1beta1.types.Feature]): Requested video annotation features.
            video_context (Union[dict, ~google.cloud.videointelligence_v1p1beta1.types.VideoContext]): Additional video context and/or feature-specific parameters.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.videointelligence_v1p1beta1.types.VideoContext`
            output_uri (str): Optional location where the output (in JSON format) should be stored.
                Currently, only `Google Cloud
                Storage <https://cloud.google.com/storage/>`__ URIs are supported, which
                must be specified in the following format: ``gs://bucket-id/object-id``
                (other URI formats return ``google.rpc.Code.INVALID_ARGUMENT``). For
                more information, see `Request
                URIs <https://cloud.google.com/storage/docs/reference-uris>`__.
            location_id (str): Optional cloud region where annotation should take place. Supported
                cloud regions: ``us-east1``, ``us-west1``, ``europe-west1``,
                ``asia-east1``. If no region is specified, a region will be determined
                based on video file location.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.videointelligence_v1p1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "annotate_video" not in self._inner_api_calls:
            self._inner_api_calls[
                "annotate_video"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.annotate_video,
                default_retry=self._method_configs["AnnotateVideo"].retry,
                default_timeout=self._method_configs["AnnotateVideo"].timeout,
                client_info=self._client_info,
            )

        request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri,
            input_content=input_content,
            features=features,
            video_context=video_context,
            output_uri=output_uri,
            location_id=location_id,
        )
        operation = self._inner_api_calls["annotate_video"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            video_intelligence_pb2.AnnotateVideoResponse,
            metadata_type=video_intelligence_pb2.AnnotateVideoProgress,
        )
