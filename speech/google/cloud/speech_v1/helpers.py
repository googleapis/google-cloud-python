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

from __future__ import absolute_import

import google.api_core.gapic_v1.method


class SpeechHelpers(object):
    """A set of convenience methods to make the Speech client easier to use.

    This class should be considered abstract; it is used as a superclass
    in a multiple-inheritance construction alongside the applicable GAPIC.
    See the :class:`~google.cloud.speech_v1.SpeechClient`.
    """

    def streaming_recognize(
        self,
        config,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
    ):
        """Perform bi-directional speech recognition.

        This method allows you to receive results while sending audio;
        it is only available via. gRPC (not REST).

        .. warning::

            This method is EXPERIMENTAL. Its interface might change in the
            future.

        Example:
          >>> from google.cloud.speech_v1 import enums
          >>> from google.cloud.speech_v1 import SpeechClient
          >>> from google.cloud.speech_v1 import types
          >>> client = SpeechClient()
          >>> config = types.StreamingRecognitionConfig(
          ...     config=types.RecognitionConfig(
          ...         encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
          ...     ),
          ... )
          >>> request = types.StreamingRecognizeRequest(audio_content=b'...')
          >>> requests = [request]
          >>> for element in client.streaming_recognize(config, requests):
          ...     # process element
          ...     pass

        Args:
            config (:class:`~.types.StreamingRecognitionConfig`): The
                configuration to use for the stream.
            requests (Iterable[:class:`~.types.StreamingRecognizeRequest`]):
                The input objects.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
          Iterable[:class:`~.types.StreamingRecognizeResponse`]

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        return super(SpeechHelpers, self).streaming_recognize(
            self._streaming_request_iterable(config, requests),
            retry=retry,
            timeout=timeout,
        )

    def _streaming_request_iterable(self, config, requests):
        """A generator that yields the config followed by the requests.

        Args:
            config (~.speech_v1.types.StreamingRecognitionConfig): The
                configuration to use for the stream.
            requests (Iterable[~.speech_v1.types.StreamingRecognizeRequest]):
                The input objects.

        Returns:
            Iterable[~.speech_v1.types.StreamingRecognizeRequest]): The
                correctly formatted input for
                :meth:`~.speech_v1.SpeechClient.streaming_recognize`.
        """
        yield self.types.StreamingRecognizeRequest(streaming_config=config)
        for request in requests:
            yield request
