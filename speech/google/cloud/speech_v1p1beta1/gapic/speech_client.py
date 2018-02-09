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
"""Accesses the google.cloud.speech.v1p1beta1 Speech API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.protobuf_helpers

from google.cloud.speech_v1p1beta1.gapic import enums
from google.cloud.speech_v1p1beta1.gapic import speech_client_config
from google.cloud.speech_v1p1beta1.proto import cloud_speech_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-speech', ).version


class SpeechClient(object):
    """Service that implements Google Cloud Speech API."""

    SERVICE_ADDRESS = 'speech.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.speech.v1p1beta1.Speech'

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=speech_client_config.config,
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
        self.speech_stub = (cloud_speech_pb2.SpeechStub(channel))

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
        self._recognize = google.api_core.gapic_v1.method.wrap_method(
            self.speech_stub.Recognize,
            default_retry=method_configs['Recognize'].retry,
            default_timeout=method_configs['Recognize'].timeout,
            client_info=client_info,
        )
        self._long_running_recognize = google.api_core.gapic_v1.method.wrap_method(
            self.speech_stub.LongRunningRecognize,
            default_retry=method_configs['LongRunningRecognize'].retry,
            default_timeout=method_configs['LongRunningRecognize'].timeout,
            client_info=client_info,
        )
        self._streaming_recognize = google.api_core.gapic_v1.method.wrap_method(
            self.speech_stub.StreamingRecognize,
            default_retry=method_configs['StreamingRecognize'].retry,
            default_timeout=method_configs['StreamingRecognize'].timeout,
            client_info=client_info,
        )

    # Service calls
    def recognize(self,
                  config,
                  audio,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT,
                  metadata=None):
        """
        Performs synchronous speech recognition: receive results after all audio
        has been sent and processed.

        Example:
            >>> from google.cloud import speech_v1p1beta1
            >>> from google.cloud.speech_v1p1beta1 import enums
            >>>
            >>> client = speech_v1p1beta1.SpeechClient()
            >>>
            >>> encoding = enums.RecognitionConfig.AudioEncoding.FLAC
            >>> sample_rate_hertz = 44100
            >>> language_code = 'en-US'
            >>> config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}
            >>> uri = 'gs://bucket_name/file_name.flac'
            >>> audio = {'uri': uri}
            >>>
            >>> response = client.recognize(config, audio)

        Args:
            config (Union[dict, ~google.cloud.speech_v1p1beta1.types.RecognitionConfig]): *Required* Provides information to the recognizer that specifies how to
                process the request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.speech_v1p1beta1.types.RecognitionConfig`
            audio (Union[dict, ~google.cloud.speech_v1p1beta1.types.RecognitionAudio]): *Required* The audio data to be recognized.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.speech_v1p1beta1.types.RecognitionAudio`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.speech_v1p1beta1.types.RecognizeResponse` instance.

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
        request = cloud_speech_pb2.RecognizeRequest(
            config=config,
            audio=audio,
        )
        return self._recognize(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def long_running_recognize(self,
                               config,
                               audio,
                               retry=google.api_core.gapic_v1.method.DEFAULT,
                               timeout=google.api_core.gapic_v1.method.DEFAULT,
                               metadata=None):
        """
        Performs asynchronous speech recognition: receive results via the
        google.longrunning.Operations interface. Returns either an
        ``Operation.error`` or an ``Operation.response`` which contains
        a ``LongRunningRecognizeResponse`` message.

        Example:
            >>> from google.cloud import speech_v1p1beta1
            >>> from google.cloud.speech_v1p1beta1 import enums
            >>>
            >>> client = speech_v1p1beta1.SpeechClient()
            >>>
            >>> encoding = enums.RecognitionConfig.AudioEncoding.FLAC
            >>> sample_rate_hertz = 44100
            >>> language_code = 'en-US'
            >>> config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}
            >>> uri = 'gs://bucket_name/file_name.flac'
            >>> audio = {'uri': uri}
            >>>
            >>> response = client.long_running_recognize(config, audio)
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
            config (Union[dict, ~google.cloud.speech_v1p1beta1.types.RecognitionConfig]): *Required* Provides information to the recognizer that specifies how to
                process the request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.speech_v1p1beta1.types.RecognitionConfig`
            audio (Union[dict, ~google.cloud.speech_v1p1beta1.types.RecognitionAudio]): *Required* The audio data to be recognized.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.speech_v1p1beta1.types.RecognitionAudio`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.speech_v1p1beta1.types._OperationFuture` instance.

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
        request = cloud_speech_pb2.LongRunningRecognizeRequest(
            config=config,
            audio=audio,
        )
        operation = self._long_running_recognize(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            cloud_speech_pb2.LongRunningRecognizeResponse,
            metadata_type=cloud_speech_pb2.LongRunningRecognizeMetadata,
        )

    def streaming_recognize(self,
                            requests,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT,
                            metadata=None):
        """
        Performs bidirectional streaming speech recognition: receive results while
        sending audio. This method is only available via the gRPC API (not REST).

        EXPERIMENTAL: This method interface might change in the future.

        Example:
            >>> from google.cloud import speech_v1p1beta1
            >>>
            >>> client = speech_v1p1beta1.SpeechClient()
            >>>
            >>> request = {}
            >>>
            >>> requests = [request]
            >>> for element in client.streaming_recognize(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|google.cloud.speech_v1p1beta1.proto.cloud_speech_pb2.StreamingRecognizeRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~google.cloud.speech_v1p1beta1.types.StreamingRecognizeRequest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.speech_v1p1beta1.types.StreamingRecognizeResponse].

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
        return self._streaming_recognize(
            requests, retry=retry, timeout=timeout, metadata=metadata)
