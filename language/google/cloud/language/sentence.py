# Copyright 2017 Google Inc.
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

"""Representation of Sentence objects."""

from google.cloud.language.sentiment import Sentiment


class Sentence(object):
    """A Google Cloud Natural Language API sentence object.

    .. _Sentence message: https://cloud.google.com/natural-language/reference\
                          /rest/v1/documents/annotateText#Sentence

    See `Sentence message`_.

    :type content: str
    :param content: The text that the sentence is composed of.

    :type begin: int
    :param begin: The beginning offset of the sentence in the original
                  document according to the encoding type specified
                  in the API request.

    :type sentiment: :class:`~google.cloud.language.sentiment.Sentiment`
    :param sentiment:
        (Optional) For calls to
        :meth:`~google.cloud.language.document.Document.annotate_text` where
        ``include_sentiment`` is set to true, this field will contain the
        sentiment for the sentence.
    """
    def __init__(self, content, begin, sentiment=None):
        self.content = content
        self.begin = begin
        self.sentiment = sentiment

    @classmethod
    def from_api_repr(cls, payload):
        """Convert a sentence from the JSON API into a :class:`Sentence`.

        :param payload: dict
        :type payload: The value from the backend.

        :rtype: :class:`Sentence`
        :returns: The sentence parsed from the API representation.
        """
        text_span = payload['text']

        # The sentence may or may not have a sentiment; only attempt the
        # typecast if one is present.
        sentiment = None
        if payload.get('sentiment') is not None:
            sentiment = Sentiment.from_api_repr(payload['sentiment'])

        # Return a Sentence object.
        return cls(text_span['content'], text_span['beginOffset'],
                   sentiment=sentiment)
