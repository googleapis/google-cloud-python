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
# https://github.com/google/googleapis/blob/master/google/cloud/videointelligence/v1beta1/video_intelligence.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.videointelligence.v1beta1 VideoIntelligenceService API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gapic.longrunning import operations_client
from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.videointelligence_v1beta1.gapic import enums
from google.cloud.videointelligence_v1beta1.gapic import video_intelligence_service_client_config
from google.cloud.videointelligence_v1beta1.proto import video_intelligence_pb2


class VideoIntelligenceServiceClient(object):
    """Service that implements Google Cloud Video Intelligence API."""

    SERVICE_ADDRESS = 'videointelligence.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
            channel (~grpc.Channel): A ``Channel`` instance through
                which to make calls.
            credentials (~google.auth.credentials.Credentials): The authorization
                credentials to attach to requests. These credentials identify this
                application to the service.
            ssl_credentials (~grpc.ChannelCredentials): A
                ``ChannelCredentials`` instance for use with an SSL-enabled
                channel.
            scopes (Sequence[str]): A list of OAuth2 scopes to attach to requests.
            client_config (dict):
                A dictionary for call options for each method. See
                :func:`google.gax.construct_settings` for the structure of
                this data. Falls back to the default config if not specified
                or the specified config is missing data points.
            lib_name (str): The API library software used for calling
                the service. (Unless you are writing an API client itself,
                leave this as default.)
            lib_version (str): The API library software version used
                for calling the service. (Unless you are writing an API client
                itself, leave this as default.)
            metrics_headers (dict): A dictionary of values for tracking
                client library metrics. Ultimately serializes to a string
                (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
                considered private.
        """
        # Unless the calling application specifically requested
        # OAuth scopes, request everything.
        if scopes is None:
            scopes = self._ALL_SCOPES

        # Initialize an empty client config, if none is set.
        if client_config is None:
            client_config = {}

        # Initialize metrics_headers as an ordered dictionary
        # (cuts down on cardinality of the resulting string slightly).
        metrics_headers = collections.OrderedDict(metrics_headers)
        metrics_headers['gl-python'] = platform.python_version()

        # The library may or may not be set, depending on what is
        # calling this client. Newer client libraries set the library name
        # and version.
        if lib_name:
            metrics_headers[lib_name] = lib_version

        # Finally, track the GAPIC package version.
        metrics_headers['gapic'] = pkg_resources.get_distribution(
            'google-cloud-videointelligence', ).version

        # Load the configuration defaults.
        defaults = api_callable.construct_settings(
            'google.cloud.videointelligence.v1beta1.VideoIntelligenceService',
            video_intelligence_service_client_config.config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers, )
        self.video_intelligence_service_stub = config.create_stub(
            video_intelligence_pb2.VideoIntelligenceServiceStub,
            channel=channel,
            service_path=self.SERVICE_ADDRESS,
            service_port=self.DEFAULT_SERVICE_PORT,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self.operations_client = operations_client.OperationsClient(
            service_path=self.SERVICE_ADDRESS,
            channel=channel,
            credentials=credentials,
            ssl_credentials=ssl_credentials,
            scopes=scopes,
            client_config=client_config,
            metrics_headers=metrics_headers, )

        self._annotate_video = api_callable.create_api_call(
            self.video_intelligence_service_stub.AnnotateVideo,
            settings=defaults['annotate_video'])

    # Service calls
    def annotate_video(self,
                       input_uri,
                       features,
                       input_content=None,
                       video_context=None,
                       output_uri=None,
                       location_id=None,
                       options=None):
        """
        Performs asynchronous video annotation. Progress and results can be
        retrieved through the ``google.longrunning.Operations`` interface.
        ``Operation.metadata`` contains ``AnnotateVideoProgress`` (progress).
        ``Operation.response`` contains ``AnnotateVideoResponse`` (results).

        Example:
            >>> from google.cloud import videointelligence_v1beta1
            >>> from google.cloud.videointelligence_v1beta1 import enums
            >>>
            >>> client = videointelligence_v1beta1.VideoIntelligenceServiceClient()
            >>>
            >>> input_uri = ''
            >>> features = []
            >>>
            >>> response = client.annotate_video(input_uri, features)
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
            features (list[~google.cloud.videointelligence_v1beta1.types.Feature]): Requested video annotation features.
            input_content (str): The video data bytes. Encoding: base64. If unset, the input video(s)
                should be specified via ``input_uri``. If set, ``input_uri`` should be unset.
            video_context (Union[dict, ~google.cloud.videointelligence_v1beta1.types.VideoContext]): Additional video context and/or feature-specific parameters.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.videointelligence_v1beta1.types.VideoContext`
            output_uri (str): Optional location where the output (in JSON format) should be stored.
                Currently, only `Google Cloud Storage <https://cloud.google.com/storage/>`_
                URIs are supported, which must be specified in the following format:
                ``gs://bucket-id/object-id`` (other URI formats return
                ``google.rpc.Code.INVALID_ARGUMENT``). For more information, see
                `Request URIs <https://cloud.google.com/storage/docs/reference-uris>`_.
            location_id (str): Optional cloud region where annotation should take place. Supported cloud
                regions: ``us-east1``, ``us-west1``, ``europe-west1``, ``asia-east1``. If no region
                is specified, a region will be determined based on video file location.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.videointelligence_v1beta1.types._OperationFuture` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri,
            features=features,
            input_content=input_content,
            video_context=video_context,
            output_uri=output_uri,
            location_id=location_id)
        return google.gax._OperationFuture(
            self._annotate_video(request, options), self.operations_client,
            video_intelligence_pb2.AnnotateVideoResponse,
            video_intelligence_pb2.AnnotateVideoProgress, options)
