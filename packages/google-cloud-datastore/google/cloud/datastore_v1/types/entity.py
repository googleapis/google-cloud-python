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


from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import latlng_pb2 as latlng  # type: ignore


__protobuf__ = proto.module(
    package="google.datastore.v1",
    manifest={"PartitionId", "Key", "ArrayValue", "Value", "Entity",},
)


class PartitionId(proto.Message):
    r"""A partition ID identifies a grouping of entities. The grouping is
    always by project and namespace, however the namespace ID may be
    empty.

    A partition ID contains several dimensions: project ID and namespace
    ID.

    Partition dimensions:

    -  May be ``""``.
    -  Must be valid UTF-8 bytes.
    -  Must have values that match regex ``[A-Za-z\d\.\-_]{1,100}`` If
       the value of any dimension matches regex ``__.*__``, the
       partition is reserved/read-only. A reserved/read-only partition
       ID is forbidden in certain documented contexts.

    Foreign partition IDs (in which the project ID does not match the
    context project ID ) are discouraged. Reads and writes of foreign
    partition IDs may fail if the project is not in an active state.

    Attributes:
        project_id (str):
            The ID of the project to which the entities
            belong.
        namespace_id (str):
            If not empty, the ID of the namespace to
            which the entities belong.
    """

    project_id = proto.Field(proto.STRING, number=2)

    namespace_id = proto.Field(proto.STRING, number=4)


class Key(proto.Message):
    r"""A unique identifier for an entity.
    If a key's partition ID or any of its path kinds or names are
    reserved/read-only, the key is reserved/read-only.
    A reserved/read-only key is forbidden in certain documented
    contexts.

    Attributes:
        partition_id (~.entity.PartitionId):
            Entities are partitioned into subsets,
            currently identified by a project ID and
            namespace ID. Queries are scoped to a single
            partition.
        path (Sequence[~.entity.Key.PathElement]):
            The entity path. An entity path consists of one or more
            elements composed of a kind and a string or numerical
            identifier, which identify entities. The first element
            identifies a *root entity*, the second element identifies a
            *child* of the root entity, the third element identifies a
            child of the second entity, and so forth. The entities
            identified by all prefixes of the path are called the
            element's *ancestors*.

            An entity path is always fully complete: *all* of the
            entity's ancestors are required to be in the path along with
            the entity identifier itself. The only exception is that in
            some documented cases, the identifier in the last path
            element (for the entity) itself may be omitted. For example,
            the last path element of the key of ``Mutation.insert`` may
            have no identifier.

            A path can never be empty, and a path can have at most 100
            elements.
    """

    class PathElement(proto.Message):
        r"""A (kind, ID/name) pair used to construct a key path.
        If either name or ID is set, the element is complete. If neither
        is set, the element is incomplete.

        Attributes:
            kind (str):
                The kind of the entity. A kind matching regex ``__.*__`` is
                reserved/read-only. A kind must not contain more than 1500
                bytes when UTF-8 encoded. Cannot be ``""``.
            id (int):
                The auto-allocated ID of the entity.
                Never equal to zero. Values less than zero are
                discouraged and may not be supported in the
                future.
            name (str):
                The name of the entity. A name matching regex ``__.*__`` is
                reserved/read-only. A name must not be more than 1500 bytes
                when UTF-8 encoded. Cannot be ``""``.
        """

        kind = proto.Field(proto.STRING, number=1)

        id = proto.Field(proto.INT64, number=2, oneof="id_type")

        name = proto.Field(proto.STRING, number=3, oneof="id_type")

    partition_id = proto.Field(proto.MESSAGE, number=1, message="PartitionId",)

    path = proto.RepeatedField(proto.MESSAGE, number=2, message=PathElement,)


class ArrayValue(proto.Message):
    r"""An array value.

    Attributes:
        values (Sequence[~.entity.Value]):
            Values in the array. The order of values in an array is
            preserved as long as all values have identical settings for
            'exclude_from_indexes'.
    """

    values = proto.RepeatedField(proto.MESSAGE, number=1, message="Value",)


class Value(proto.Message):
    r"""A message that can hold any of the supported value types and
    associated metadata.

    Attributes:
        null_value (~.struct.NullValue):
            A null value.
        boolean_value (bool):
            A boolean value.
        integer_value (int):
            An integer value.
        double_value (float):
            A double value.
        timestamp_value (~.timestamp.Timestamp):
            A timestamp value.
            When stored in the Datastore, precise only to
            microseconds; any additional precision is
            rounded down.
        key_value (~.entity.Key):
            A key value.
        string_value (str):
            A UTF-8 encoded string value. When ``exclude_from_indexes``
            is false (it is indexed), may have at most 1500 bytes.
            Otherwise, may be set to at most 1,000,000 bytes.
        blob_value (bytes):
            A blob value. May have at most 1,000,000 bytes. When
            ``exclude_from_indexes`` is false, may have at most 1500
            bytes. In JSON requests, must be base64-encoded.
        geo_point_value (~.latlng.LatLng):
            A geo point value representing a point on the
            surface of Earth.
        entity_value (~.entity.Entity):
            An entity value.
            - May have no key.
            - May have a key with an incomplete key path. -
            May have a reserved/read-only key.
        array_value (~.entity.ArrayValue):
            An array value. Cannot contain another array value. A
            ``Value`` instance that sets field ``array_value`` must not
            set fields ``meaning`` or ``exclude_from_indexes``.
        meaning (int):
            The ``meaning`` field should only be populated for backwards
            compatibility.
        exclude_from_indexes (bool):
            If the value should be excluded from all
            indexes including those defined explicitly.
    """

    null_value = proto.Field(
        proto.ENUM, number=11, oneof="value_type", enum=struct.NullValue,
    )

    boolean_value = proto.Field(proto.BOOL, number=1, oneof="value_type")

    integer_value = proto.Field(proto.INT64, number=2, oneof="value_type")

    double_value = proto.Field(proto.DOUBLE, number=3, oneof="value_type")

    timestamp_value = proto.Field(
        proto.MESSAGE, number=10, oneof="value_type", message=timestamp.Timestamp,
    )

    key_value = proto.Field(proto.MESSAGE, number=5, oneof="value_type", message="Key",)

    string_value = proto.Field(proto.STRING, number=17, oneof="value_type")

    blob_value = proto.Field(proto.BYTES, number=18, oneof="value_type")

    geo_point_value = proto.Field(
        proto.MESSAGE, number=8, oneof="value_type", message=latlng.LatLng,
    )

    entity_value = proto.Field(
        proto.MESSAGE, number=6, oneof="value_type", message="Entity",
    )

    array_value = proto.Field(
        proto.MESSAGE, number=9, oneof="value_type", message="ArrayValue",
    )

    meaning = proto.Field(proto.INT32, number=14)

    exclude_from_indexes = proto.Field(proto.BOOL, number=19)


class Entity(proto.Message):
    r"""A Datastore data object.

    An entity is limited to 1 megabyte when stored. That *roughly*
    corresponds to a limit of 1 megabyte for the serialized form of this
    message.

    Attributes:
        key (~.entity.Key):
            The entity's key.

            An entity must have a key, unless otherwise documented (for
            example, an entity in ``Value.entity_value`` may have no
            key). An entity's kind is its key path's last element's
            kind, or null if it has no key.
        properties (Sequence[~.entity.Entity.PropertiesEntry]):
            The entity's properties. The map's keys are property names.
            A property name matching regex ``__.*__`` is reserved. A
            reserved property name is forbidden in certain documented
            contexts. The name must not contain more than 500
            characters. The name cannot be ``""``.
    """

    key = proto.Field(proto.MESSAGE, number=1, message="Key",)

    properties = proto.MapField(proto.STRING, proto.MESSAGE, number=3, message="Value",)


__all__ = tuple(sorted(__protobuf__.manifest))
