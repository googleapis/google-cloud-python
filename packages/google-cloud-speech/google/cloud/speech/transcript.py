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

"""Transcript representation for Google Speech API"""


class Transcript(object):
    """Representation of Speech Transcripts

    :type result: dict
    :param result: Dictionary of transcript and confidence of recognition.
    """
    def __init__(self, result):
        self._transcript = result.get('transcript')
        self._confidence = result.get('confidence')

    @property
    def transcript(self):
        """Transcript text from audio.

        :rtype: str
        :returns: Text detected in audio.
        """
        return self._transcript

    @property
    def confidence(self):
        """Confidence score for recognized speech.

        :rtype: float
        :returns: Confidence score of recognized speech [0-1].
        """
        return self._confidence
