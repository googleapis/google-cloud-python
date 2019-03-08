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
"""Accesses the google.cloud.speech.v1p1beta1 Speech API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.protobuf_helpers
import grpc

from google.cloud.speech_v1p1beta1.gapic import enums
from google.cloud.speech_v1p1beta1.gapic import speech_client_config
from google.cloud.speech_v1p1beta1.gapic.transports import speech_grpc_transport
from google.cloud.speech_v1p1beta1.proto import cloud_speech_pb2
from google.cloud.speech_v1p1beta1.proto import cloud_speech_pb2_grpc
from google.longrunning import operations_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-speech").version


class SpeechClient(object):
    """Service that implements Google Cloud Speech API."""

    SERVICE_ADDRESS = "speech.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.speech.v1p1beta1.Speech"

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
            SpeechClient: The constructed client.
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
            transport (Union[~.SpeechGrpcTransport,
                    Callable[[~.Credentials, type], ~.SpeechGrpcTransport]): A transport
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
            client_config = speech_client_config.config

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
                    default_class=speech_grpc_transport.SpeechGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = speech_grpc_transport.SpeechGrpcTransport(
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
    def recognize(
        self,
        config,
        audio,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "recognize" not in self._inner_api_calls:
            self._inner_api_calls[
                "recognize"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.recognize,
                default_retry=self._method_configs["Recognize"].retry,
                default_timeout=self._method_configs["Recognize"].timeout,
                client_info=self._client_info,
            )

        request = cloud_speech_pb2.RecognizeRequest(config=config, audio=audio)
        return self._inner_api_calls["recognize"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def long_running_recognize(
        self,
        config,
        audio,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Performs asynchronous speech recognition: receive results via the
        google.longrunning.Operations interface. Returns either an
        ``Operation.error`` or an ``Operation.response`` which contains a
        ``LongRunningRecognizeResponse`` message.

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
        # Wrap the transport method to add retry and timeout logic.
        if "long_running_recognize" not in self._inner_api_calls:
            self._inner_api_calls[
                "long_running_recognize"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.long_running_recognize,
                default_retry=self._method_configs["LongRunningRecognize"].retry,
                default_timeout=self._method_configs["LongRunningRecognize"].timeout,
                client_info=self._client_info,
            )

        request = cloud_speech_pb2.LongRunningRecognizeRequest(
            config=config, audio=audio
        )
        operation = self._inner_api_calls["long_running_recognize"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            cloud_speech_pb2.LongRunningRecognizeResponse,
            metadata_type=cloud_speech_pb2.LongRunningRecognizeMetadata,
        )

    def streaming_recognize(
        self,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "streaming_recognize" not in self._inner_api_calls:
            self._inner_api_calls[
                "streaming_recognize"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.streaming_recognize,
                default_retry=self._method_configs["StreamingRecognize"].retry,
                default_timeout=self._method_configs["StreamingRecognize"].timeout,
                client_info=self._client_info,
            )

        return self._inner_api_calls["streaming_recognize"](
            requests, retry=retry, timeout=timeout, metadata=metadata
        )
