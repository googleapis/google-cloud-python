# Copyright 2018 Google LLC
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

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1

from google.cloud.videointelligence_v1p1beta1.gapic import enums
from google.cloud.videointelligence_v1p1beta1.gapic import video_intelligence_service_client_config
from google.cloud.videointelligence_v1p1beta1.proto import video_intelligence_pb2
from google.longrunning import operations_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-videointelligence', ).version


class VideoIntelligenceServiceClient(object):
    """Service that implements Google Cloud Video Intelligence API."""

    SERVICE_ADDRESS = 'videointelligence.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.videointelligence.v1p1beta1.VideoIntelligenceService'

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=video_intelligence_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.video_intelligence_service_stub = (
            video_intelligence_pb2.VideoIntelligenceServiceStub(channel))

        # Operations client for methods that return long-running operations
        # futures.
        self.operations_client = (
            google.api_core.operations_v1.OperationsClient(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._annotate_video = google.api_core.gapic_v1.method.wrap_method(
            self.video_intelligence_service_stub.AnnotateVideo,
            default_retry=method_configs['AnnotateVideo'].retry,
            default_timeout=method_configs['AnnotateVideo'].timeout,
            client_info=client_info,
        )

    # Service calls
    def annotate_video(self,
                       input_uri=None,
                       input_content=None,
                       features=None,
                       video_context=None,
                       output_uri=None,
                       location_id=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
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
            input_uri (str): Input video location. Currently, only
                `Google Cloud Storage <https://cloud.google.com/storage/>`_ URIs are
                supported, which must be specified in the following format:
                ``gs://bucket-id/object-id`` (other URI formats return
                ``google.rpc.Code.INVALID_ARGUMENT``). For more information, see
                `Request URIs <https://cloud.google.com/storage/docs/reference-uris>`_.
                A video URI may include wildcards in ``object-id``, and thus identify
                multiple videos. Supported wildcards: '*' to match 0 or more characters;
                '?' to match 1 character. If unset, the input video should be embedded
                in the request as ``input_content``. If set, ``input_content`` should be unset.
            input_content (bytes): The video data bytes.
                If unset, the input video(s) should be specified via ``input_uri``.
                If set, ``input_uri`` should be unset.
            features (list[~google.cloud.videointelligence_v1p1beta1.types.Feature]): Requested video annotation features.
            video_context (Union[dict, ~google.cloud.videointelligence_v1p1beta1.types.VideoContext]): Additional video context and/or feature-specific parameters.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.videointelligence_v1p1beta1.types.VideoContext`
            output_uri (str): Optional location where the output (in JSON format) should be stored.
                Currently, only `Google Cloud Storage <https://cloud.google.com/storage/>`_
                URIs are supported, which must be specified in the following format:
                ``gs://bucket-id/object-id`` (other URI formats return
                ``google.rpc.Code.INVALID_ARGUMENT``). For more information, see
                `Request URIs <https://cloud.google.com/storage/docs/reference-uris>`_.
            location_id (str): Optional cloud region where annotation should take place. Supported cloud
                regions: ``us-east1``, ``us-west1``, ``europe-west1``, ``asia-east1``. If no region
                is specified, a region will be determined based on video file location.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri,
            input_content=input_content,
            features=features,
            video_context=video_context,
            output_uri=output_uri,
            location_id=location_id,
        )
        operation = self._annotate_video(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            video_intelligence_pb2.AnnotateVideoResponse,
            metadata_type=video_intelligence_pb2.AnnotateVideoProgress,
        )
