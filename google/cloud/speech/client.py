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

class Encoding(Object):
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

    :type credentials: :class:`~oauth2client.client.OAuth2Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for the
                        connection owned by this client. If not passed (and
                        if no ``http`` object is passed), falls back to the
                        default inferred from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def syncrecognize(self, audio, encoding, sampleRate, languageCode=None,
                      maxAlternatives=None,profanityFilter=None,
                      SpeechContext=None):
        """Synchronous Speech Recognition.

        See: https://cloud.google.com/speech/reference/\
        rest/v1beta1/speech/syncrecognize

        :type audio: str
        :param audio:   Content or URI.
                        * Content : The content string containing the audio 
                          data bytes encoded as specified in RecognitionConfig. 
                          This is a base64-encoded string
                        * URI : URI that points to a file that contains audio
                          data bytes as specified in RecognitionConfig. 
                          Currently, only Google Cloud Storage URIs are 
                          supported, which must be specified in the following 
                          format: gs://bucket_name/object_name


        :type encoding: str
        :param encoding: encoding of audio data sent in all RecognitionAudio 
                         messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                         :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                         :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

        :type sampleRate: int
        :param sampleRate: Sample rate in Hertz of the audio data sent in all 
                           RecognitionAudio messages. Valid values are: 8000-
                           48000. 16000 is optimal. For best results, set the
                           sampling rate of the audio source to 16000 Hz. 
                           If that's not possible, use the native sample rate
                           of the audio source (instead of re-sampling).

        :type languageCode: str
        :param languageCode: (Optional) The language of the supplied audio as
                             BCP-47 language tag. Example: "en-GB".
                             If omitted, defaults to "en-US". 

        :type maxAlternatives: int
        :param maxAlternatives: (Optional) Maximum number of recognition 
                                hypotheses to be returned. The server may return
                                fewer than maxAlternatives. Valid values are 0-30.
                                A value of 0 or 1 will return a maximum of 1. 
                                If omitted, defaults to 1

        :type profanityFilter: bool
        :param profanityFilter: If set to true, the server will attempt to filter out
                                profanities, replacing all but the initial character 
                                in each filtered word with asterisks, e.g. "f***".
                                If set to false or omitted, profanities won't be 
                                filtered out.

        :type speechContext: list
        :param speechContext: A list of strings (max 50) containing words and phrases 
                              "hints" so that the speech recognition is more likely to 
                              recognize them. This can be used to improve the accuracy
                              for specific words and phrases. This can also be used to 
                              add additional words to the vocabulary of the recognizer. 

        :rtype: list
        :returns: A list of tuples. One tuple for each alternative. Each tuple contains 
                  a transcript text and a confidence value (between 0.0 and 1.0)
        """
        
        
        requiredParams = [('encoding',encoding),('sampleRate',sampleRate)]
        for paramName, param in requiredParams:
            if param is None:
                message = '%r cannot be None' %paramName)
                raise ValueError(message)
        config=dict(requiredParams)
        for paramName, param in [('languageCode',languageCode),
                                 ('maxAlternatives',maxAlternatives),
                                 ('profanityFilter',profanityFilter)]:
            if param is not None:
                config[paramName]=paramName
        if speechContext is not None:
            config["speechContext"]={"phrases"=speechContext}

        data = {
            'audio': audio,
            'config': config
        }
        api_response = self.client.connection.api_request(
            method='POST', path='syncrecognize', data=data)
        
        return api_response["alternatives"]