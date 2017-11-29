# Copyright 2017, Google LLC All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/cloud/videointelligence/v1beta2/video_intelligence.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.videointelligence.v1beta2 VideoIntelligenceService API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1

from google.cloud.videointelligence_v1beta2.gapic import enums
from google.cloud.videointelligence_v1beta2.gapic import video_intelligence_service_client_config
from google.cloud.videointelligence_v1beta2.proto import video_intelligence_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-videointelligence',
).version


class VideoIntelligenceServiceClient(object):
    """Service that implements Google Cloud Video Intelligence API."""

    SERVICE_ADDRESS = 'videointelligence.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = (
        'google.cloud.videointelligence.v1beta2.VideoIntelligenceService')

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=video_intelligence_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

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

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._annotate_video = google.api_core.gapic_v1.method.wrap_method(
            self.video_intelligence_service_stub.AnnotateVideo,
            default_retry=method_configs['AnnotateVideo'].retry,
            default_timeout=method_configs['AnnotateVideo'].timeout,
            client_info=client_info)

    # Service calls
    def annotate_video(self,
                       input_uri=None,
                       input_content=None,
                       features=None,
                       video_context=None,
                       output_uri=None,
                       location_id=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Performs asynchronous video annotation. Progress and results can be
        retrieved through the ``google.longrunning.Operations`` interface.
        ``Operation.metadata`` contains ``AnnotateVideoProgress`` (progress).
        ``Operation.response`` contains ``AnnotateVideoResponse`` (results).

        Example:
            >>> from google.cloud import videointelligence_v1beta2
            >>>
            >>> client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
            >>>
            >>> response = client.annotate_video()
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
            features (list[~google.cloud.videointelligence_v1beta2.types.Feature]): Requested video annotation features.
            video_context (Union[dict, ~google.cloud.videointelligence_v1beta2.types.VideoContext]): Additional video context and/or feature-specific parameters.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.videointelligence_v1beta2.types.VideoContext`
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

        Returns:
            A :class:`~google.cloud.videointelligence_v1beta2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri,
            input_content=input_content,
            features=features,
            video_context=video_context,
            output_uri=output_uri,
            location_id=location_id)
        operation = self._annotate_video(request, retry=retry, timeout=timeout)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            video_intelligence_pb2.AnnotateVideoResponse,
            metadata_type=video_intelligence_pb2.AnnotateVideoProgress)
