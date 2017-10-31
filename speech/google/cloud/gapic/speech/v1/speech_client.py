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
# https://github.com/google/googleapis/blob/master/google/cloud/speech/v1/cloud_speech.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.speech.v1 Speech API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gapic.longrunning import operations_client
from google.gax import api_callable
from google.gax import config
from google.gax import path_template
from google.gax.utils import oneof
import google.gax

from google.cloud.gapic.speech.v1 import enums
from google.cloud.proto.speech.v1 import cloud_speech_pb2


class SpeechClient(object):
    """Service that implements Google Cloud Speech API."""

    SERVICE_ADDRESS = 'speech.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 app_name=None,
                 app_version='',
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.Channel`): A ``Channel`` instance through
            which to make calls.
          credentials (object): The authorization credentials to attach to
            requests. These credentials identify this application to the
            service.
          ssl_credentials (:class:`grpc.ChannelCredentials`): A
            ``ChannelCredentials`` instance for use with an SSL-enabled
            channel.
          scopes (list[string]): A list of OAuth2 scopes to attach to requests.
          client_config (dict):
            A dictionary for call options for each method. See
            :func:`google.gax.construct_settings` for the structure of
            this data. Falls back to the default config if not specified
            or the specified config is missing data points.
          app_name (string): The name of the application calling
            the service. Recommended for analytics purposes.
          app_version (string): The version of the application calling
            the service. Recommended for analytics purposes.
          lib_name (string): The API library software used for calling
            the service. (Unless you are writing an API client itself,
            leave this as default.)
          lib_version (string): The API library software version used
            for calling the service. (Unless you are writing an API client
            itself, leave this as default.)
          metrics_headers (dict): A dictionary of values for tracking
            client library metrics. Ultimately serializes to a string
            (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
            considered private.

        Returns:
          A SpeechClient object.
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
            'google-cloud-speech', ).version

        # Load the configuration defaults.
        default_client_config = json.loads(
            pkg_resources.resource_string(
                __name__, 'speech_client_config.json').decode())
        defaults = api_callable.construct_settings(
            'google.cloud.speech.v1.Speech',
            default_client_config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers, )
        self.speech_stub = config.create_stub(
            cloud_speech_pb2.SpeechStub,
            channel=channel,
            service_path=service_path,
            service_port=port,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self.operations_client = operations_client.OperationsClient(
            service_path=service_path,
            port=port,
            channel=channel,
            credentials=credentials,
            ssl_credentials=ssl_credentials,
            scopes=scopes,
            client_config=client_config,
            metrics_headers=metrics_headers, )

        self._recognize = api_callable.create_api_call(
            self.speech_stub.Recognize, settings=defaults['recognize'])
        self._long_running_recognize = api_callable.create_api_call(
            self.speech_stub.LongRunningRecognize,
            settings=defaults['long_running_recognize'])
        self._streaming_recognize = api_callable.create_api_call(
            self.speech_stub.StreamingRecognize,
            settings=defaults['streaming_recognize'])

    # Service calls
    def recognize(self, config, audio, options=None):
        """
        Performs synchronous speech recognition: receive results after all audio
        has been sent and processed.

        Example:
          >>> from google.cloud.gapic.speech.v1 import speech_client
          >>> from google.cloud.gapic.speech.v1 import enums
          >>> from google.cloud.proto.speech.v1 import cloud_speech_pb2
          >>> client = speech_client.SpeechClient()
          >>> encoding = enums.RecognitionConfig.AudioEncoding.FLAC
          >>> sample_rate_hertz = 44100
          >>> language_code = 'en-US'
          >>> config = cloud_speech_pb2.RecognitionConfig(encoding=encoding, sample_rate_hertz=sample_rate_hertz, language_code=language_code)
          >>> uri = 'gs://bucket_name/file_name.flac'
          >>> audio = cloud_speech_pb2.RecognitionAudio(uri=uri)
          >>> response = client.recognize(config, audio)

        Args:
          config (:class:`google.cloud.proto.speech.v1.cloud_speech_pb2.RecognitionConfig`): *Required* Provides information to the recognizer that specifies how to
            process the request.
          audio (:class:`google.cloud.proto.speech.v1.cloud_speech_pb2.RecognitionAudio`): *Required* The audio data to be recognized.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.speech.v1.cloud_speech_pb2.RecognizeResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = cloud_speech_pb2.RecognizeRequest(config=config, audio=audio)
        return self._recognize(request, options)

    def long_running_recognize(self, config, audio, options=None):
        """
        Performs asynchronous speech recognition: receive results via the
        google.longrunning.Operations interface. Returns either an
        ``Operation.error`` or an ``Operation.response`` which contains
        a ``LongRunningRecognizeResponse`` message.

        Example:
          >>> from google.cloud.gapic.speech.v1 import speech_client
          >>> from google.cloud.gapic.speech.v1 import enums
          >>> from google.cloud.proto.speech.v1 import cloud_speech_pb2
          >>> client = speech_client.SpeechClient()
          >>> encoding = enums.RecognitionConfig.AudioEncoding.FLAC
          >>> sample_rate_hertz = 44100
          >>> language_code = 'en-US'
          >>> config = cloud_speech_pb2.RecognitionConfig(encoding=encoding, sample_rate_hertz=sample_rate_hertz, language_code=language_code)
          >>> uri = 'gs://bucket_name/file_name.flac'
          >>> audio = cloud_speech_pb2.RecognitionAudio(uri=uri)
          >>> response = client.long_running_recognize(config, audio)
          >>>
          >>> def callback(operation_future):
          >>>     # Handle result.
          >>>     result = operation_future.result()
          >>>
          >>> response.add_done_callback(callback)
          >>>
          >>> # Handle metadata.
          >>> metadata = response.metadata()

        Args:
          config (:class:`google.cloud.proto.speech.v1.cloud_speech_pb2.RecognitionConfig`): *Required* Provides information to the recognizer that specifies how to
            process the request.
          audio (:class:`google.cloud.proto.speech.v1.cloud_speech_pb2.RecognitionAudio`): *Required* The audio data to be recognized.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.gax._OperationFuture` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = cloud_speech_pb2.LongRunningRecognizeRequest(
            config=config, audio=audio)
        return google.gax._OperationFuture(
            self._long_running_recognize(request,
                                         options), self.operations_client,
            cloud_speech_pb2.LongRunningRecognizeResponse,
            cloud_speech_pb2.LongRunningRecognizeMetadata, options)

    def streaming_recognize(self, requests, options=None):
        """
        Performs bidirectional streaming speech recognition: receive results while
        sending audio. This method is only available via the gRPC API (not REST).

        EXPERIMENTAL: This method interface might change in the future.

        Example:
          >>> from google.cloud.gapic.speech.v1 import speech_client
          >>> from google.cloud.proto.speech.v1 import cloud_speech_pb2
          >>> client = speech_client.SpeechClient()
          >>> request = cloud_speech_pb2.StreamingRecognizeRequest()
          >>> requests = [request]
          >>> for element in client.streaming_recognize(requests):
          >>>     # process element
          >>>     pass

        Args:
          requests (iterator[:class:`google.cloud.proto.speech.v1.cloud_speech_pb2.StreamingRecognizeRequest`]): The input objects.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          iterator[:class:`google.cloud.proto.speech.v1.cloud_speech_pb2.StreamingRecognizeResponse`].

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        return self._streaming_recognize(requests, options)
