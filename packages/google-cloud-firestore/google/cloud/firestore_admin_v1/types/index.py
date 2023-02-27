# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.admin.v1",
    manifest={
        "Index",
    },
)


class Index(proto.Message):
    r"""Cloud Firestore indexes enable simple and complex queries
    against documents in a database.

    Attributes:
        name (str):
            Output only. A server defined name for this index. The form
            of this name for composite indexes will be:
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{composite_index_id}``
            For single field indexes, this field will be empty.
        query_scope (google.cloud.firestore_admin_v1.types.Index.QueryScope):
            Indexes with a collection query scope
            specified allow queries against a collection
            that is the child of a specific document,
            specified at query time, and that has the same
            collection id.
            Indexes with a collection group query scope
            specified allow queries against all collections
            descended from a specific document, specified at
            query time, and that have the same collection id
            as this index.
        fields (MutableSequence[google.cloud.firestore_admin_v1.types.Index.IndexField]):
            The fields supported by this index.

            For composite indexes, this is always 2 or more fields. The
            last field entry is always for the field path ``__name__``.
            If, on creation, ``__name__`` was not specified as the last
            field, it will be added automatically with the same
            direction as that of the last field defined. If the final
            field in a composite index is not directional, the
            ``__name__`` will be ordered ASCENDING (unless explicitly
            specified).

            For single field indexes, this will always be exactly one
            entry with a field path equal to the field path of the
            associated field.
        state (google.cloud.firestore_admin_v1.types.Index.State):
            Output only. The serving state of the index.
    """

    class QueryScope(proto.Enum):
        r"""Query Scope defines the scope at which a query is run. This is
        specified on a StructuredQuery's ``from`` field.

        Values:
            QUERY_SCOPE_UNSPECIFIED (0):
                The query scope is unspecified. Not a valid
                option.
            COLLECTION (1):
                Indexes with a collection query scope
                specified allow queries against a collection
                that is the child of a specific document,
                specified at query time, and that has the
                collection id specified by the index.
            COLLECTION_GROUP (2):
                Indexes with a collection group query scope
                specified allow queries against all collections
                that has the collection id specified by the
                index.
        """
        QUERY_SCOPE_UNSPECIFIED = 0
        COLLECTION = 1
        COLLECTION_GROUP = 2

    class State(proto.Enum):
        r"""The state of an index. During index creation, an index will be in
        the ``CREATING`` state. If the index is created successfully, it
        will transition to the ``READY`` state. If the index creation
        encounters a problem, the index will transition to the
        ``NEEDS_REPAIR`` state.

        Values:
            STATE_UNSPECIFIED (0):
                The state is unspecified.
            CREATING (1):
                The index is being created.
                There is an active long-running operation for
                the index. The index is updated when writing a
                document. Some index data may exist.
            READY (2):
                The index is ready to be used.
                The index is updated when writing a document.
                The index is fully populated from all stored
                documents it applies to.
            NEEDS_REPAIR (3):
                The index was being created, but something
                went wrong. There is no active long-running
                operation for the index, and the most recently
                finished long-running operation failed. The
                index is not updated when writing a document.
                Some index data may exist.
                Use the google.longrunning.Operations API to
                determine why the operation that last attempted
                to create this index failed, then re-create the
                index.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        NEEDS_REPAIR = 3

    class IndexField(proto.Message):
        r"""A field in an index. The field_path describes which field is
        indexed, the value_mode describes how the field value is indexed.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            field_path (str):
                Can be **name**. For single field indexes, this must match
                the name of the field or may be omitted.
            order (google.cloud.firestore_admin_v1.types.Index.IndexField.Order):
                Indicates that this field supports ordering
                by the specified order or comparing using =, !=,
                <, <=, >, >=.

                This field is a member of `oneof`_ ``value_mode``.
            array_config (google.cloud.firestore_admin_v1.types.Index.IndexField.ArrayConfig):
                Indicates that this field supports operations on
                ``array_value``\ s.

                This field is a member of `oneof`_ ``value_mode``.
        """

        class Order(proto.Enum):
            r"""The supported orderings.

            Values:
                ORDER_UNSPECIFIED (0):
                    The ordering is unspecified. Not a valid
                    option.
                ASCENDING (1):
                    The field is ordered by ascending field
                    value.
                DESCENDING (2):
                    The field is ordered by descending field
                    value.
            """
            ORDER_UNSPECIFIED = 0
            ASCENDING = 1
            DESCENDING = 2

        class ArrayConfig(proto.Enum):
            r"""The supported array value configurations.

            Values:
                ARRAY_CONFIG_UNSPECIFIED (0):
                    The index does not support additional array
                    queries.
                CONTAINS (1):
                    The index supports array containment queries.
            """
            ARRAY_CONFIG_UNSPECIFIED = 0
            CONTAINS = 1

        field_path: str = proto.Field(
            proto.STRING,
            number=1,
        )
        order: "Index.IndexField.Order" = proto.Field(
            proto.ENUM,
            number=2,
            oneof="value_mode",
            enum="Index.IndexField.Order",
        )
        array_config: "Index.IndexField.ArrayConfig" = proto.Field(
            proto.ENUM,
            number=3,
            oneof="value_mode",
            enum="Index.IndexField.ArrayConfig",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query_scope: QueryScope = proto.Field(
        proto.ENUM,
        number=2,
        enum=QueryScope,
    )
    fields: MutableSequence[IndexField] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=IndexField,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
