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

"""Definition for Google Cloud Natural Language API entities.

An entity is used to describe a proper name extracted from text.
"""

from google.cloud.language.sentiment import Sentiment


class EntityType(object):
    """List of possible entity types."""

    UNKNOWN = 'UNKNOWN'
    """Unknown entity type."""

    PERSON = 'PERSON'
    """Person entity type."""

    LOCATION = 'LOCATION'
    """Location entity type."""

    ORGANIZATION = 'ORGANIZATION'
    """Organization entity type."""

    EVENT = 'EVENT'
    """Event entity type."""

    WORK_OF_ART = 'WORK_OF_ART'
    """Work of art entity type."""

    CONSUMER_GOOD = 'CONSUMER_GOOD'
    """Consumer good entity type."""

    OTHER = 'OTHER'
    """Other entity type (i.e. known but not classified)."""


class MentionType(object):
    """List of possible mention types."""

    TYPE_UNKNOWN = 'TYPE_UNKNOWN'
    """Unknown mention type"""

    PROPER = 'PROPER'
    """Proper name"""

    COMMON = 'COMMON'
    """Common noun (or noun compound)"""


class Mention(object):
    """A Google Cloud Natural Language API mention.

    Represents a mention for an entity in the text. Currently, proper noun
    mentions are supported.
    """
    def __init__(self, text, mention_type):
        self.text = text
        self.mention_type = mention_type

    def __str__(self):
        return str(self.text)

    @classmethod
    def from_api_repr(cls, payload):
        """Convert a Mention from the JSON API into an :class:`Mention`.

        :param payload: dict
        :type payload: The value from the backend.

        :rtype: :class:`Mention`
        :returns: The mention parsed from the API representation.
        """
        text = TextSpan.from_api_repr(payload['text'])
        mention_type = payload['type']
        return cls(text, mention_type)


class TextSpan(object):
    """A span of text from Google Cloud Natural Language API.

    Represents a word or phrase of text, as well as its offset
    from the original document.
    """
    def __init__(self, content, begin_offset):
        self.content = content
        self.begin_offset = begin_offset

    def __str__(self):
        """Return the string representation of this TextSpan.

        :rtype: str
        :returns: The text content
        """
        return self.content

    @classmethod
    def from_api_repr(cls, payload):
        """Convert a TextSpan from the JSON API into an :class:`TextSpan`.

        :param payload: dict
        :type payload: The value from the backend.

        :rtype: :class:`TextSpan`
        :returns: The text span parsed from the API representation.
        """
        content = payload['content']
        begin_offset = payload['beginOffset']
        return cls(content=content, begin_offset=begin_offset)


class Entity(object):
    """A Google Cloud Natural Language API entity.

    Represents a phrase in text that is a known entity, such as a person,
    an organization, or location. The API associates information, such as
    salience and mentions, with entities.

    .. _Entity message: https://cloud.google.com/natural-language/\
                        reference/rest/v1/Entity
    .. _EntityType enum: https://cloud.google.com/natural-language/\
                         reference/rest/v1/Entity#Type

    See `Entity message`_.

    :type name: str
    :param name: The name / phrase identified as the entity.

    :type entity_type: str
    :param entity_type: The type of the entity. See `EntityType enum`_.

    :type metadata: dict
    :param metadata: The metadata associated with the entity.
                     Wikipedia URLs and Knowledge Graph MIDs are
                     provided, if available. The associated keys are
                     "wikipedia_url" and "mid", respectively.

    :type salience: float
    :param salience: The prominence of the entity / phrase within the text
                     containing it.

    :type mentions: list
    :param mentions: List of strings that mention the entity.

    :type sentiment: :class:`~.language.sentiment.Sentiment`
    :params sentiment: The sentiment; sent only on `analyze_entity_sentiment`
                       calls.
    """

    def __init__(self, name, entity_type, metadata, salience, mentions,
                 sentiment):
        self.name = name
        self.entity_type = entity_type
        self.metadata = metadata
        self.salience = salience
        self.mentions = mentions
        self.sentiment = sentiment

    @classmethod
    def from_api_repr(cls, payload):
        """Convert an Entity from the JSON API into an :class:`Entity`.

        :param payload: dict
        :type payload: The value from the backend.

        :rtype: :class:`Entity`
        :returns: The entity parsed from the API representation.
        """
        name = payload['name']
        entity_type = payload['type']
        metadata = payload['metadata']
        salience = payload['salience']
        mentions = [Mention.from_api_repr(val) for val in payload['mentions']]
        sentiment = None
        if payload.get('sentiment'):
            sentiment = Sentiment.from_api_repr(payload['sentiment'])
        return cls(name, entity_type, metadata, salience, mentions, sentiment)
