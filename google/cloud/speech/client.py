# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Basic client for Google Cloud Speech API."""

from google.cloud import client as client_module
from google.cloud.speech.connection import Connection


class Encoding(object):
    """Audio encoding types."""

    LINEAR16 = 'LINEAR16'
    """LINEAR16 encoding type."""

    FLAC = 'FLAC'
    """FLAC encoding type."""

    MULAW = 'MULAW'
    """MULAW encoding type."""

    AMR = 'AMR'
    """AMR encoding type."""

    AMR_WB = 'AMR_WB'
    """AMR_WB encoding type."""


class Client(client_module.Client):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a dataset / job.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def syncrecognize(self, content, uri, encoding, sample_rate,
                      language_code=None, max_alternatives=None,
                      profanity_filter=None,
                      speech_context=None):
        """Synchronous Speech Recognition.

        See: https://cloud.google.com/speech/reference/\
        rest/v1beta1/speech/syncrecognize

        :type content: str
        :param content: The content string containing the audio
                      data bytes encoded as specified in RecognitionConfig.
                      This is a base64-encoded string

        :type uri: str
        :param uri: URI that points to a file that contains audio
                      data bytes as specified in RecognitionConfig.
                      Currently, only Google Cloud Storage URIs are
                      supported, which must be specified in the following
                      format: gs://bucket_name/object_name

        :type encoding: str
        :param encoding: encoding of audio data sent in all RecognitionAudio
                         messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                         :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                         :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

        :type sample_rate: int
        :param sample_rate: Sample rate in Hertz of the audio data sent in all
                           RecognitionAudio messages. Valid values are: 8000-
                           48000. 16000 is optimal. For best results, set the
                           sampling rate of the audio source to 16000 Hz.
                           If that's not possible, use the native sample rate
                           of the audio source (instead of re-sampling).

        :type language_code: str
        :param language_code: (Optional) The language of the supplied audio as
                             BCP-47 language tag. Example: "en-GB".
                             If omitted, defaults to "en-US".

        :type max_alternatives: int
        :param max_alternatives: (Optional) Maximum number of recognition
                                hypotheses to be returned. The server may
                                return fewer than maxAlternatives.
                                Valid values are 0-30. A value of 0 or 1
                                will return a maximum of 1. Defaults to 1

        :type profanity_filter: bool
        :param profanity_filter: If True, the server will attempt to filter
                                out profanities, replacing all but the
                                initialcharacter in each filtered word with
                                asterisks, e.g. "f***". If False or omitted,
                                profanities won't be filtered out.

        :type speech_context: list
        :param speech_context: A list of strings (max 50) containing words and
                              phrases "hints" so that the speech recognition
                              is more likely to recognize them. This can be
                              used to improve the accuracy for specific words
                              and phrases. This can also be used to add new
                              words to the vocabulary of the recognizer.

        :rtype: list
        :returns: A list of tuples. One tuple for each alternative. Each tuple
                  contains a transcript text and a confidence value (between
                  0.0 and 1.0)
        """

        if (content is None) and (uri is None):
            message = 'content and uri cannot be both equal to None'
            raise ValueError(message)

        if (content is not None) and (uri is not None):
            message = 'content and uri cannot be both different from None'
            raise ValueError(message)

        if content is not None:
            audio = {'content': content}
        else:
            audio = {'uri': uri}

        required_params = [('encoding', encoding), ('sampleRate', sample_rate)]
        for param_name, param in required_params:
            if param is None:
                message = '%r cannot be None' % (param_name)
                raise ValueError(message)
        config = dict(required_params)
        for param_name, param in [
                ('languageCode', language_code),
                ('maxAlternatives', max_alternatives),
                ('profanityFilter', profanity_filter)]:
            if param is not None:
                config[param_name] = param
        if speech_context is not None:
            config["speechContext"] = {"phrases": speech_context}

        data = {
            'audio': audio,
            'config': config
        }
        api_response = self.connection.api_request(
            method='POST', path='syncrecognize', data=data)

        return api_response['results'][0]['alternatives']
