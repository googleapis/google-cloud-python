# Copyright 2016 Google Inc.
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


class Sample(object):
    """Representation of an audio sample to be used with Google Speech API.

    :type content: bytes
    :param content: (Optional) Byte stream of audio.

    :type source_uri: str
    :param source_uri: (Optional) URI that points to a file that contains
                       audio data bytes as specified in RecognitionConfig.
                       Currently, only Google Cloud Storage URIs are
                       supported, which must be specified in the following
                       format: ``gs://bucket_name/object_name``.

    :type encoding: str
    :param encoding: encoding of audio data sent in all RecognitionAudio
                     messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                     :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                     :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

    :type sample_rate: int
    :param sample_rate: Sample rate in Hertz of the audio data sent in all
                        requests. Valid values are: 8000-48000. For best
                        results, set the sampling rate of the audio source
                        to 16000 Hz. If that's not possible, use the
                        native sample rate of the audio source (instead of
                        re-sampling).
    """
    default_encoding = Encoding.FLAC
    default_sample_rate = 16000

    def __init__(self, content=None, source_uri=None,
                 encoding=None, sample_rate=None):

        no_source = content is None and source_uri is None
        both_source = content is not None and source_uri is not None
        if no_source or both_source:
            raise ValueError('Supply one of \'content\' or \'source_uri\'')

        self._content = content
        self._source_uri = source_uri

        if sample_rate is not None and not 8000 <= sample_rate <= 48000:
            raise ValueError('The value of sample_rate must be between 8000'
                             ' and 48000.')
        self._sample_rate = sample_rate or self.default_sample_rate

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
        return int(self.sample_rate / 10.0)

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
    def sample_rate(self):
        """Sample rate integer.

        :rtype: int
        :returns: Integer between 8000 and 48,000.
        """
        return self._sample_rate

    @property
    def encoding(self):
        """Audio encoding type

        :rtype: str
        :returns: String value of Encoding type.
        """
        return self._encoding
