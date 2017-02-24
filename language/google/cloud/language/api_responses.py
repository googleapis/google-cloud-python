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

"""Response types from the Natural Language API."""

from google.cloud.language.entity import Entity
from google.cloud.language.sentence import Sentence
from google.cloud.language.sentiment import Sentiment
from google.cloud.language.syntax import Token


class EntityResponse(object):
    """Object representation of entity responses.

    A representation of a response sent back from the
    ``analyzeEntites`` request to the Google Natural language API.

    :type entities: list
    :param entities: A list of :class:`~.language.entity.Entity` objects.

    :type language: str
    :param language: The language used for analysis.
    """
    def __init__(self, entities, language):
        self.entities = entities
        self.language = language

    @classmethod
    def from_api_repr(cls, payload):
        """Return an entity response from a JSON representation.

        :type payload: dict
        :param payload: A dictionary representing the response.

        :rtype: :class:`~.language.entity.Entity`
        :returns: An ``Entity`` object.
        """
        return cls(
            entities=[Entity.from_api_repr(i) for i in payload['entities']],
            language=payload['language'],
        )


class SentimentResponse(object):
    """Object representation of sentiment responses.

    A representation of a response to an ``analyzeSentiment`` request
    to the Google Natural Language API.

    :type sentiment: :class:`~.language.sentiment.Sentiment`
    :param sentiment: A Sentiment object.

    :type language: str
    :param language: The language used for analyzing sentiment.

    :type sentences: list
    :param sentences: A list of :class:`~.language.syntax.Sentence` objects.
    """
    def __init__(self, sentiment, language, sentences):
        self.sentiment = sentiment
        self.language = language
        self.sentences = sentences

    @classmethod
    def from_api_repr(cls, payload):
        """Return an sentiment response from a JSON representation.

        :type payload: dict
        :param payload: A dictionary representing the response.

        :rtype: `~.language.sentiment.Sentiment`
        :returns: A ``Sentiment`` object.
        """
        return cls(
            language=payload.get('language'),
            sentences=[Sentence.from_api_repr(sentence) for sentence
                       in payload.get('sentences', ())],
            sentiment=Sentiment.from_api_repr(payload['documentSentiment']),
        )


class SyntaxResponse(object):
    """Object representation of syntax responses.

    A representation of a response to an ``analyzeSyntax`` request
    to the Google Natural Language API.

    :type tokens: list
    :param tokens: A list of :class:`~.language.syntax.Token` objects.

    :type language: str
    :param language: The language used for analyzing sentiment.

    :type sentences: list
    :param sentences: A list of :class:`~.language.syntax.Sentence` objects.
    """
    def __init__(self, tokens, language, sentences):
        self.tokens = tokens
        self.language = language
        self.sentences = sentences

    @classmethod
    def from_api_repr(cls, payload):
        """Return an syntax response from a JSON representation.

        :type payload: dict
        :param payload: A dictionary representing the response.

        :rtype: `~.language.syntax.Syntax`
        :returns: A ``Syntax`` object.
        """
        return cls(
            language=payload.get('language'),
            sentences=[Sentence.from_api_repr(sentence) for sentence in
                       payload.get('sentences', ())],
            tokens=[Token.from_api_repr(token) for token in
                    payload.get('tokens', ())]
        )
