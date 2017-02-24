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

    :type salience: float
    :param salience: The prominence of the entity / phrase within the text
                     containing it.

    :type mentions: list
    :param mentions: List of strings that mention the entity.
    """

    def __init__(self, name, entity_type, metadata, salience, mentions):
        self.name = name
        self.entity_type = entity_type
        self.metadata = metadata
        self.salience = salience
        self.mentions = mentions

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
        mentions = [value['text']['content']
                    for value in payload['mentions']]
        return cls(name, entity_type, metadata, salience, mentions)
