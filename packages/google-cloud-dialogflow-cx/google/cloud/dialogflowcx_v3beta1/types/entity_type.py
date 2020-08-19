# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

import proto  # type: ignore


from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "EntityType",
        "ListEntityTypesRequest",
        "ListEntityTypesResponse",
        "GetEntityTypeRequest",
        "CreateEntityTypeRequest",
        "UpdateEntityTypeRequest",
        "DeleteEntityTypeRequest",
    },
)


class EntityType(proto.Message):
    r"""Entities are extracted from user input and represent parameters that
    are meaningful to your application. For example, a date range, a
    proper name such as a geographic location or landmark, and so on.
    Entities represent actionable data for your application.

    When you define an entity, you can also include synonyms that all
    map to that entity. For example, "soft drink", "soda", "pop", and so
    on.

    There are three types of entities:

    -  **System** - entities that are defined by the Dialogflow API for
       common data types such as date, time, currency, and so on. A
       system entity is represented by the ``EntityType`` type.

    -  **Custom** - entities that are defined by you that represent
       actionable data that is meaningful to your application. For
       example, you could define a ``pizza.sauce`` entity for red or
       white pizza sauce, a ``pizza.cheese`` entity for the different
       types of cheese on a pizza, a ``pizza.topping`` entity for
       different toppings, and so on. A custom entity is represented by
       the ``EntityType`` type.

    -  **User** - entities that are built for an individual user such as
       favorites, preferences, playlists, and so on. A user entity is
       represented by the
       [SessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityType]
       type.

    For more information about entity types, see the `Dialogflow
    documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

    Attributes:
        name (str):
            The unique identifier of the entity type. Required for
            [EntityTypes.UpdateEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.UpdateEntityType].
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``.
        display_name (str):
            Required. The human-readable name of the
            entity type, unique within the agent.
        kind (~.gcdc_entity_type.EntityType.Kind):
            Required. Indicates the kind of entity type.
        auto_expansion_mode (~.gcdc_entity_type.EntityType.AutoExpansionMode):
            Indicates whether the entity type can be
            automatically expanded.
        entities (Sequence[~.gcdc_entity_type.EntityType.Entity]):
            The collection of entity entries associated
            with the entity type.
        excluded_phrases (Sequence[~.gcdc_entity_type.EntityType.ExcludedPhrase]):
            Collection of exceptional words and phrases that shouldn't
            be matched. For example, if you have a size entity type with
            entry ``giant``\ (an adjective), you might consider adding
            ``giants``\ (a noun) as an exclusion. If the kind of entity
            type is ``KIND_MAP``, then the phrases specified by entities
            and excluded phrases should be mutually exclusive.
        enable_fuzzy_extraction (bool):
            Enables fuzzy entity extraction during
            classification.
    """

    class Kind(proto.Enum):
        r"""Represents kinds of entities."""
        KIND_UNSPECIFIED = 0
        KIND_MAP = 1
        KIND_LIST = 2
        KIND_REGEXP = 3

    class AutoExpansionMode(proto.Enum):
        r"""Represents different entity type expansion modes. Automated
        expansion allows an agent to recognize values that have not been
        explicitly listed in the entity (for example, new kinds of
        shopping list items).
        """
        AUTO_EXPANSION_MODE_UNSPECIFIED = 0
        AUTO_EXPANSION_MODE_DEFAULT = 1

    class Entity(proto.Message):
        r"""An **entity entry** for an associated entity type. Next Id = 8

        Attributes:
            value (str):
                Required. The primary value associated with this entity
                entry. For example, if the entity type is *vegetable*, the
                value could be *scallions*.

                For ``KIND_MAP`` entity types:

                -  A canonical value to be used in place of synonyms.

                For ``KIND_LIST`` entity types:

                -  A string that can contain references to other entity
                   types (with or without aliases).
            synonyms (Sequence[str]):
                Required. A collection of value synonyms. For example, if
                the entity type is *vegetable*, and ``value`` is
                *scallions*, a synonym could be *green onions*.

                For ``KIND_LIST`` entity types:

                -  This collection must contain exactly one synonym equal to
                   ``value``.
        """

        value = proto.Field(proto.STRING, number=1)

        synonyms = proto.RepeatedField(proto.STRING, number=2)

    class ExcludedPhrase(proto.Message):
        r"""An excluded entity phrase that should not be matched.

        Attributes:
            value (str):
                Required. The word or phrase to be excluded.
        """

        value = proto.Field(proto.STRING, number=1)

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    kind = proto.Field(proto.ENUM, number=3, enum=Kind,)

    auto_expansion_mode = proto.Field(proto.ENUM, number=4, enum=AutoExpansionMode,)

    entities = proto.RepeatedField(proto.MESSAGE, number=5, message=Entity,)

    excluded_phrases = proto.RepeatedField(
        proto.MESSAGE, number=6, message=ExcludedPhrase,
    )

    enable_fuzzy_extraction = proto.Field(proto.BOOL, number=7)


class ListEntityTypesRequest(proto.Message):
    r"""The request message for
    [EntityTypes.ListEntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityTypes.ListEntityTypes].

    Attributes:
        parent (str):
            Required. The agent to list all entity types for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        language_code (str):
            The language to list entity types for. The following fields
            are language dependent:

            -  ``EntityType.entities.value``
            -  ``EntityType.entities.synonyms``
            -  ``EntityType.excluded_phrases.value``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListEntityTypesResponse(proto.Message):
    r"""The response message for
    [EntityTypes.ListEntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityTypes.ListEntityTypes].

    Attributes:
        entity_types (Sequence[~.gcdc_entity_type.EntityType]):
            The list of entity types. There will be a maximum number of
            items returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    entity_types = proto.RepeatedField(proto.MESSAGE, number=1, message=EntityType,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetEntityTypeRequest(proto.Message):
    r"""The request message for
    [EntityTypes.GetEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.GetEntityType].

    Attributes:
        name (str):
            Required. The name of the entity type. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``.
        language_code (str):
            The language to retrieve the entity type for. The following
            fields are language dependent:

            -  ``EntityType.entities.value``
            -  ``EntityType.entities.synonyms``
            -  ``EntityType.excluded_phrases.value``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    name = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)


class CreateEntityTypeRequest(proto.Message):
    r"""The request message for
    [EntityTypes.CreateEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.CreateEntityType].

    Attributes:
        parent (str):
            Required. The agent to create a entity type for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        entity_type (~.gcdc_entity_type.EntityType):
            Required. The entity type to create.
        language_code (str):
            The language of the following fields in ``entity_type``:

            -  ``EntityType.entities.value``
            -  ``EntityType.entities.synonyms``
            -  ``EntityType.excluded_phrases.value``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1)

    entity_type = proto.Field(proto.MESSAGE, number=2, message=EntityType,)

    language_code = proto.Field(proto.STRING, number=3)


class UpdateEntityTypeRequest(proto.Message):
    r"""The request message for
    [EntityTypes.UpdateEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.UpdateEntityType].

    Attributes:
        entity_type (~.gcdc_entity_type.EntityType):
            Required. The entity type to update.
        language_code (str):
            The language of the following fields in ``entity_type``:

            -  ``EntityType.entities.value``
            -  ``EntityType.entities.synonyms``
            -  ``EntityType.excluded_phrases.value``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
        update_mask (~.field_mask.FieldMask):
            The mask to control which fields get updated.
    """

    entity_type = proto.Field(proto.MESSAGE, number=1, message=EntityType,)

    language_code = proto.Field(proto.STRING, number=2)

    update_mask = proto.Field(proto.MESSAGE, number=3, message=field_mask.FieldMask,)


class DeleteEntityTypeRequest(proto.Message):
    r"""The request message for
    [EntityTypes.DeleteEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.DeleteEntityType].

    Attributes:
        name (str):
            Required. The name of the entity type to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``.
        force (bool):
            This field has no effect for entity type not being used. For
            entity types that are used by intents or pages:

            -  If ``force`` is set to false, an error will be returned
               with message indicating the referencing resources.
            -  If ``force`` is set to true, Dialogflow will remove the
               entity type, as well as any references to the entity type
               (i.e. Page
               [parameter][google.cloud.dialogflow.cx.v3beta1.Form.Parameter]
               of the entity type will be changed to '@sys.any' and
               intent
               [parameter][google.cloud.dialogflow.cx.v3beta1.Intent.Parameter]
               of the entity type will be removed).
    """

    name = proto.Field(proto.STRING, number=1)

    force = proto.Field(proto.BOOL, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
