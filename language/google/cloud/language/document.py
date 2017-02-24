# Copyright 2016-2017 Google Inc.
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

"""Definition for Google Cloud Natural Language API documents.

A document is used to hold text to be analyzed and annotated.
"""

import collections

from google.cloud.language import api_responses
from google.cloud.language.entity import Entity
from google.cloud.language.sentiment import Sentiment
from google.cloud.language.sentence import Sentence
from google.cloud.language.syntax import Token


Annotations = collections.namedtuple(
    'Annotations',
    ['sentences', 'tokens', 'sentiment', 'entities', 'language'])
"""Annotations for a document.

:type sentences: list
:param sentences: List of :class:`.Sentence` in a document.

:type tokens: list
:param tokens: List of :class:`.Token` from a document.

:type sentiment: :class:`Sentiment`
:param sentiment: The sentiment of a document.

:type entities: list
:param entities: List of :class:`~.language.entity.Entity`
                 found in a document.

:type language: str
:param language: The language used for the annotation.
"""


class Encoding(object):
    """Document text encoding types."""

    NONE = 'NONE'
    """Unspecified encoding type."""

    UTF8 = 'UTF8'
    """UTF-8 encoding type."""

    UTF16 = 'UTF16'
    """UTF-16 encoding type."""

    UTF32 = 'UTF32'
    """UTF-32 encoding type."""


class Document(object):
    """Document to send to Google Cloud Natural Language API.

    Represents either plain text or HTML, and the content is either
    stored on the document or referred to in a Google Cloud Storage
    object.

    :type client: :class:`~google.cloud.language.client.Client`
    :param client: A client which holds credentials and other
                   configuration.

    :type content: str
    :param content: (Optional) The document text content (either plain
                    text or HTML).

    :type gcs_url: str
    :param gcs_url: (Optional) The URL of the Google Cloud Storage object
                    holding the content. Of the form
                    ``gs://{bucket}/{blob-name}``.

    :type doc_type: str
    :param doc_type: (Optional) The type of text in the document.
                     Defaults to plain text. Can be one of
                     :attr:`~.Document.PLAIN_TEXT` or
                     or :attr:`~.Document.HTML`.

    :type language: str
    :param language: (Optional) The language of the document text.
                     Defaults to None (auto-detect).

    :type encoding: str
    :param encoding: (Optional) The encoding of the document text.
                     Defaults to UTF-8. Can be one of
                     :attr:`~.Encoding.UTF8`, :attr:`~.Encoding.UTF16`
                     or :attr:`~.Encoding.UTF32`.

    :raises: :class:`~exceptions.ValueError` both ``content`` and ``gcs_url``
             are specified or if neither are specified.
    """

    TYPE_UNSPECIFIED = 'TYPE_UNSPECIFIED'
    """Unspecified document type."""

    PLAIN_TEXT = 'PLAIN_TEXT'
    """Plain text document type."""

    HTML = 'HTML'
    """HTML document type."""

    def __init__(self, client, content=None, gcs_url=None, doc_type=PLAIN_TEXT,
                 language=None, encoding=Encoding.UTF8):
        if content is not None and gcs_url is not None:
            raise ValueError('A Document cannot contain both local text and '
                             'a link to text in a Google Cloud Storage object')
        if content is None and gcs_url is None:
            raise ValueError('A Document must contain either local text or a '
                             'link to text in a Google Cloud Storage object')
        self.client = client
        self.content = content
        self.gcs_url = gcs_url
        self.doc_type = doc_type
        self.language = language
        self.encoding = encoding

    def _to_dict(self):
        """Helper to convert the current document into a dictionary.

        To be used when constructing requests.

        :rtype: dict
        :returns: The Document value as a JSON dictionary.
        """
        info = {
            'type': self.doc_type,
        }
        if self.language is not None:
            info['language'] = self.language
        if self.content is not None:
            info['content'] = self.content
        elif self.gcs_url is not None:
            info['gcsContentUri'] = self.gcs_url
        return info

    def analyze_entities(self):
        """Analyze the entities in the current document.

        Finds named entities (currently finds proper names as of August 2016)
        in the text, entity types, salience, mentions for each entity, and
        other properties.

        .. _analyzeEntities: https://cloud.google.com/natural-language/\
                             reference/rest/v1/documents/analyzeEntities

        See `analyzeEntities`_.

        :rtype: :class:`~.language.entity.EntityResponse`
        :returns: A representation of the entity response.
        """
        data = {
            'document': self._to_dict(),
            'encodingType': self.encoding,
        }
        api_response = self.client._connection.api_request(
            method='POST', path='analyzeEntities', data=data)
        return api_responses.EntityResponse.from_api_repr(api_response)

    def analyze_sentiment(self):
        """Analyze the sentiment in the current document.

        .. _analyzeSentiment: https://cloud.google.com/natural-language/\
                              reference/rest/v1/documents/analyzeSentiment

        See `analyzeSentiment`_.

        :rtype: :class:`.SentimentResponse`
        :returns: A representation of the sentiment response.
        """
        data = {'document': self._to_dict()}
        api_response = self.client._connection.api_request(
            method='POST', path='analyzeSentiment', data=data)
        return api_responses.SentimentResponse.from_api_repr(api_response)

    def analyze_syntax(self):
        """Analyze the syntax in the current document.

        .. _analyzeSyntax: https://cloud.google.com/natural-language/\
                              reference/rest/v1/documents/analyzeSyntax

        See `analyzeSyntax`_.

        :rtype: list
        :returns: A list of :class:`~.language.syntax.Token` returned from
                  the API.
        """
        data = {
            'document': self._to_dict(),
            'encodingType': self.encoding,
        }
        api_response = self.client._connection.api_request(
            method='POST', path='analyzeSyntax', data=data)
        return api_responses.SyntaxResponse.from_api_repr(api_response)

    def annotate_text(self, include_syntax=True, include_entities=True,
                      include_sentiment=True):
        """Advanced natural language API: document syntax and other features.

        Includes the full functionality of :meth:`analyze_entities` and
        :meth:`analyze_sentiment`, enabled by the flags
        ``include_entities`` and ``include_sentiment`` respectively.

        In addition ``include_syntax`` adds a new feature that analyzes
        the document for semantic and syntacticinformation.

        .. note::

            This API is intended for users who are familiar with machine
            learning and need in-depth text features to build upon.

        .. _annotateText: https://cloud.google.com/natural-language/\
                          reference/rest/v1/documents/annotateText

        See `annotateText`_.

        :type include_syntax: bool
        :param include_syntax: (Optional) Flag to enable syntax analysis
                               of the current document.

        :type include_entities: bool
        :param include_entities: (Optional) Flag to enable entity extraction
                                 from the current document.

        :type include_sentiment: bool
        :param include_sentiment: (Optional) Flag to enable sentiment
                                  analysis of the current document.

        :rtype: :class:`Annotations`
        :returns: A tuple of each of the four values returned from the API:
                  sentences, tokens, sentiment and entities.
        """
        features = {}
        if include_syntax:
            features['extractSyntax'] = True
        if include_entities:
            features['extractEntities'] = True
        if include_sentiment:
            features['extractDocumentSentiment'] = True

        data = {
            'document': self._to_dict(),
            'features': features,
            'encodingType': self.encoding,
        }
        api_response = self.client._connection.api_request(
            method='POST', path='annotateText', data=data)

        sentences = [Sentence.from_api_repr(sentence)
                     for sentence in api_response['sentences']]
        tokens = [Token.from_api_repr(token)
                  for token in api_response['tokens']]
        sentiment_info = api_response.get('documentSentiment')
        if sentiment_info is None:
            sentiment = None
        else:
            sentiment = Sentiment.from_api_repr(sentiment_info)
        entities = [Entity.from_api_repr(entity)
                    for entity in api_response['entities']]
        annotations = Annotations(
            entities=entities,
            language=api_response.get('language'),
            sentences=sentences,
            sentiment=sentiment,
            tokens=tokens,
        )
        return annotations
