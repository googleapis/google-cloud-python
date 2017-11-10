# Copyright 2016 Google LLC
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

"""Sample class to handle content for Google Cloud Speech API."""

from google.cloud.speech.encoding import Encoding
from google.cloud.speech.result import StreamingSpeechResult


class Sample(object):
    """Representation of an audio sample to be used with Google Speech API.

    :type content: bytes
    :param content: (Optional) Bytes containing audio data.

    :type source_uri: str
    :param source_uri: (Optional) URI that points to a file that contains
                       audio data bytes as specified in RecognitionConfig.
                       Currently, only Google Cloud Storage URIs are
                       supported, which must be specified in the following
                       format: ``gs://bucket_name/object_name``.

    :type stream: file
    :param stream: (Optional) File like object to stream.

    :type encoding: str
    :param encoding: encoding of audio data sent in all RecognitionAudio
                     messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                     :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                     :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

    :type sample_rate_hertz: int
    :param sample_rate_hertz: Sample rate in Hertz of the audio data sent in
                              all requests. Valid values are: 8000-48000. For
                              best results, set the sampling rate of the audio
                              source to 16000 Hz. If that's not possible, use
                              the native sample rate of the audio source
                              (instead of re-sampling).

    :type client: :class:`~google.cloud.speech.client.Client`
    :param client: (Optional) The client that owns this instance of sample.
    """
    default_encoding = Encoding.FLAC

    def __init__(self, content=None, source_uri=None, stream=None,
                 encoding=None, sample_rate_hertz=None, client=None):
        self._client = client

        sources = [content is not None, source_uri is not None,
                   stream is not None]
        if sources.count(True) != 1:
            raise ValueError('Supply exactly one of '
                             '\'content\',  \'source_uri\', \'stream\'')

        self._content = content
        self._source_uri = source_uri
        self._stream = stream
        self._sample_rate_hertz = sample_rate_hertz

        if encoding is not None and getattr(Encoding, encoding, False):
            self._encoding = getattr(Encoding, encoding)
        else:
            raise ValueError('Invalid encoding: %s' % (encoding,))

    @property
    def chunk_size(self):
        """Chunk size to send over gRPC. ~100ms

        :rtype: int
        :returns: Optimized chunk size.
        """
        return int(self.sample_rate_hertz / 10.0)

    @property
    def source_uri(self):
        """Google Cloud Storage URI of audio source.

        :rtype: str
        :returns: Google Cloud Storage URI string.
        """
        return self._source_uri

    @property
    def content(self):
        """Bytes of audio content.

        :rtype: bytes
        :returns: Byte stream of audio content.
        """
        return self._content

    @property
    def sample_rate_hertz(self):
        """Sample rate integer.

        :rtype: int
        :returns: Integer between 8000 and 48,000.
        """
        return self._sample_rate_hertz

    @property
    def stream(self):
        """Stream the content when it is a file-like object.

        :rtype: file
        :returns: File like object to stream.
        """
        return self._stream

    @property
    def encoding(self):
        """Audio encoding type

        :rtype: str
        :returns: String value of Encoding type.
        """
        return self._encoding

    def long_running_recognize(self, language_code, max_alternatives=None,
                               profanity_filter=None, speech_contexts=()):
        """Asychronous Recognize request to Google Speech API.

        .. _long_running_recognize: https://cloud.google.com/speech/reference/\
                                    rest/v1/speech/longrunningrecognize

        See `long_running_recognize`_.

        :type language_code: str
        :param language_code: (Optional) The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-US'``.

        :type max_alternatives: int
        :param max_alternatives: (Optional) Maximum number of recognition
                                 hypotheses to be returned. The server may
                                 return fewer than maxAlternatives.
                                 Valid values are 0-30. A value of 0 or 1
                                 will return a maximum of 1. Defaults to 1

        :type profanity_filter: bool
        :param profanity_filter: If True, the server will attempt to filter
                                 out profanities, replacing all but the
                                 initial character in each filtered word with
                                 asterisks, e.g. ``'f***'``. If False or
                                 omitted, profanities won't be filtered out.

        :type speech_contexts: list
        :param speech_contexts: A list of strings (max 50) containing words and
                                phrases "hints" so that the speech recognition
                                is more likely to recognize them. This can be
                                used to improve the accuracy for specific words
                                and phrases. This can also be used to add new
                                words to the vocabulary of the recognizer.

        :rtype: :class:`~google.cloud.speech.operation.Operation`
        :returns: Operation for asynchronous request to Google Speech API.
        """
        api = self._client.speech_api
        return api.long_running_recognize(
            self, language_code, max_alternatives, profanity_filter,
            speech_contexts)

    def streaming_recognize(self, language_code,
                            max_alternatives=None, profanity_filter=None,
                            speech_contexts=(), single_utterance=False,
                            interim_results=False):
        """Streaming speech recognition.

        .. note::

            Streaming recognition requests are limited to 1 minute of audio.
            See https://cloud.google.com/speech/limits#content

        Yields: Instance of
                :class:`~google.cloud.speech.result.StreamingSpeechResult`
                containing results and metadata from the streaming request.

        :type language_code: str
        :param language_code: The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-US'``.

        :type max_alternatives: int
        :param max_alternatives: (Optional) Maximum number of recognition
                                 hypotheses to be returned. The server may
                                 return fewer than maxAlternatives.
                                 Valid values are 0-30. A value of 0 or 1
                                 will return a maximum of 1. Defaults to 1

        :type profanity_filter: bool
        :param profanity_filter: If True, the server will attempt to filter
                                 out profanities, replacing all but the
                                 initial character in each filtered word with
                                 asterisks, e.g. ``'f***'``. If False or
                                 omitted, profanities won't be filtered out.

        :type speech_contexts: list
        :param speech_contexts: A list of strings (max 50) containing words and
                                phrases "hints" so that the speech recognition
                                is more likely to recognize them. This can be
                                used to improve the accuracy for specific words
                                and phrases. This can also be used to add new
                                words to the vocabulary of the recognizer.

        :type single_utterance: bool
        :param single_utterance: (Optional) If false or omitted, the recognizer
                                 will perform continuous recognition
                                 (continuing to process audio even if the user
                                 pauses speaking) until the client closes the
                                 output stream (gRPC API) or when the maximum
                                 time limit has been reached. Multiple
                                 SpeechRecognitionResults with the is_final
                                 flag set to true may be returned.
                                 If true, the recognizer will detect a single
                                 spoken utterance. When it detects that the
                                 user has paused or stopped speaking, it will
                                 return an END_OF_UTTERANCE event and cease
                                 recognition. It will return no more than one
                                 SpeechRecognitionResult with the is_final flag
                                 set to true.

        :type interim_results: bool
        :param interim_results: (Optional) If true, interim results (tentative
                                hypotheses) may be returned as they become
                                available (these interim results are indicated
                                with the ``is_final=False`` flag). If false or
                                omitted, only is_final=true result(s) are
                                returned.

        :raises: EnvironmentError if gRPC is not available.
        """
        if not self._client._use_grpc:
            raise EnvironmentError('gRPC is required to use this API.')

        api = self._client.speech_api
        responses = api.streaming_recognize(self, language_code,
                                            max_alternatives, profanity_filter,
                                            speech_contexts, single_utterance,
                                            interim_results)
        for response in responses:
            for result in response.results:
                if result.is_final or interim_results:
                    yield StreamingSpeechResult.from_pb(result)

    def recognize(self, language_code, max_alternatives=None,
                  profanity_filter=None, speech_contexts=()):
        """Synchronous Speech Recognition.

        .. _recognize: https://cloud.google.com/speech/reference/\
                       rest/v1/speech/recognize

        See `recognize`_.

        :type language_code: str
        :param language_code: The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-US'``.

        :type max_alternatives: int
        :param max_alternatives: (Optional) Maximum number of recognition
                                 hypotheses to be returned. The server may
                                 return fewer than maxAlternatives.
                                 Valid values are 0-30. A value of 0 or 1
                                 will return a maximum of 1. Defaults to 1

        :type profanity_filter: bool
        :param profanity_filter: If True, the server will attempt to filter
                                 out profanities, replacing all but the
                                 initial character in each filtered word with
                                 asterisks, e.g. ``'f***'``. If False or
                                 omitted, profanities won't be filtered out.

        :type speech_contexts: list
        :param speech_contexts: A list of strings (max 50) containing words and
                                phrases "hints" so that the speech recognition
                                is more likely to recognize them. This can be
                                used to improve the accuracy for specific words
                                and phrases. This can also be used to add new
                                words to the vocabulary of the recognizer.

        :rtype: list
        :returns: A list of dictionaries. One dict for each alternative. Each
                  dictionary typically contains two keys (though not
                  all will be present in all cases)

                  * ``transcript``: The detected text from the audio recording.
                  * ``confidence``: The confidence in language detection, float
                    between 0 and 1.
        """
        api = self._client.speech_api
        return api.recognize(self, language_code, max_alternatives,
                             profanity_filter, speech_contexts)
