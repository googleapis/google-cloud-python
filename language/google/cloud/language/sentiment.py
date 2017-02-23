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

"""Definition for Google Cloud Natural Language API sentiment.

Sentiment is the response to an ``analyzeSentiment`` request.
"""


class Sentiment(object):
    """A Google Cloud Natural Language API sentiment object.

    .. _Sentiment message: https://cloud.google.com/natural-language/\
                           reference/rest/v1/Sentiment
    .. _Sentiment basics: https://cloud.google.com/natural-language/\
                          docs/basics#sentiment-analysis-values

    See `Sentiment message`_ and `Sentiment basics`_.

    :type score: float
    :param score: Score of the sentiment in the ``[-1.0, 1.0]`` range.
                     Larger numbers represent more positive sentiments.

    :type magnitude: float
    :param magnitude: A non-negative number in the ``[0, +inf)`` range, which
                      represents the absolute magnitude of sentiment
                      regardless of score (positive or negative).
    """

    def __init__(self, score, magnitude):
        self.score = score
        self.magnitude = magnitude

    @classmethod
    def from_api_repr(cls, payload):
        """Convert a Sentiment from the JSON API into a :class:`Sentiment`.

        :param payload: dict
        :type payload: The value from the backend.

        :rtype: :class:`Sentiment`
        :returns: The sentiment parsed from the API representation.
        """
        score = payload['score']
        magnitude = payload['magnitude']
        return cls(score, magnitude)
