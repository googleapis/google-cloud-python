# Copyright 2014 Google LLC
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

"""Helper functions for dealing with Cloud Datastore's Protobuf API.

The non-private functions are part of the API.
"""

import datetime
import itertools

from google.protobuf import struct_pb2
from google.type import latlng_pb2
from proto.datetime_helpers import DatetimeWithNanoseconds

from google.cloud._helpers import _datetime_to_pb_timestamp
from google.cloud.datastore_v1.types import datastore as datastore_pb2
from google.cloud.datastore_v1.types import entity as entity_pb2
from google.cloud.datastore.entity import Entity
from google.cloud.datastore.key import Key


def _get_meaning(value_pb, is_list=False):
    """Get the meaning from a protobuf value.

    :type value_pb: :class:`.entity_pb2.Value._pb`
    :param value_pb: The *raw* protobuf value to be checked for an
                     associated meaning.

    :type is_list: bool
    :param is_list: Boolean indicating if the ``value_pb`` contains
                    a list value.

    :rtype: int
    :returns: The meaning for the ``value_pb`` if one is set, else
              :data:`None`. For a list value, if there are disagreeing
              means it just returns a list of meanings. If all the
              list meanings agree, it just condenses them.
    """
    if is_list:

        values = value_pb.array_value.values

        # An empty list will have no values, hence no shared meaning
        # set among them.
        if len(values) == 0:
            return None

        # We check among all the meanings, some of which may be None,
        # the rest which may be enum/int values.
        all_meanings = [_get_meaning(sub_value_pb) for sub_value_pb in values]
        unique_meanings = set(all_meanings)

        if len(unique_meanings) == 1:
            # If there is a unique meaning, we preserve it.
            return unique_meanings.pop()
        else:  # We know len(value_pb.array_value.values) > 0.
            # If the meaning is not unique, just return all of them.
            return all_meanings

    elif value_pb.meaning:  # Simple field (int32).
        return value_pb.meaning

    return None


def _new_value_pb(entity_pb, name):
    """Add (by name) a new ``Value`` protobuf to an entity protobuf.

    :type entity_pb: :class:`.entity_pb2.Entity`
    :param entity_pb: An entity protobuf to add a new property to.

    :type name: str
    :param name: The name of the new property.

    :rtype: :class:`.entity_pb2.Value`
    :returns: The new ``Value`` protobuf that was added to the entity.
    """
    # TODO(microgenerator): shouldn't need this. the issue is that
    # we have wrapped and non-wrapped protos coming here.
    properties = getattr(entity_pb.properties, "_pb", entity_pb.properties)
    return properties.get_or_create(name)


def entity_from_protobuf(pb):
    """Factory method for creating an entity based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`.entity_pb2.Entity`
    :param pb: The Protobuf representing the entity.

    :rtype: :class:`google.cloud.datastore.entity.Entity`
    :returns: The entity derived from the protobuf.
    """
    if isinstance(pb, entity_pb2.Entity):
        pb = pb._pb

    key = None
    if pb.HasField("key"):  # Message field (Key)
        key = key_from_protobuf(pb.key)

    entity_props = {}
    entity_meanings = {}
    exclude_from_indexes = []

    for prop_name, value_pb in pb.properties.items():
        value = _get_value_from_value_pb(value_pb)
        entity_props[prop_name] = value

        # Check if the property has an associated meaning.
        is_list = isinstance(value, list)
        meaning = _get_meaning(value_pb, is_list=is_list)
        if meaning is not None:
            entity_meanings[prop_name] = (meaning, value)

        # Check if ``value_pb`` was excluded from index. Lists need to be
        # special-cased and we require all ``exclude_from_indexes`` values
        # in a list agree.
        if is_list and len(value) > 0:
            exclude_values = set(
                value_pb.exclude_from_indexes
                for value_pb in value_pb.array_value.values
            )
            if len(exclude_values) != 1:
                raise ValueError(
                    "For an array_value, subvalues must either "
                    "all be indexed or all excluded from "
                    "indexes."
                )

            if exclude_values.pop():
                exclude_from_indexes.append(prop_name)
        else:
            if value_pb.exclude_from_indexes:
                exclude_from_indexes.append(prop_name)

    entity = Entity(key=key, exclude_from_indexes=exclude_from_indexes)
    entity.update(entity_props)
    entity._meanings.update(entity_meanings)
    return entity


def _set_pb_meaning_from_entity(entity, name, value, value_pb, is_list=False):
    """Add meaning information (from an entity) to a protobuf.

    :type entity: :class:`google.cloud.datastore.entity.Entity`
    :param entity: The entity to be turned into a protobuf.

    :type name: str
    :param name: The name of the property.

    :type value: object
    :param value: The current value stored as property ``name``.

    :type value_pb: :class:`.entity_pb2.Value`
    :param value_pb: The protobuf value to add meaning / meanings to.

    :type is_list: bool
    :param is_list: (Optional) Boolean indicating if the ``value`` is
                    a list value.
    """
    if name not in entity._meanings:
        return

    meaning, orig_value = entity._meanings[name]
    # Only add the meaning back to the protobuf if the value is
    # unchanged from when it was originally read from the API.
    if orig_value is not value:
        return

    # For lists, we set meaning on each sub-element.
    if is_list:
        if not isinstance(meaning, list):
            meaning = itertools.repeat(meaning)
        val_iter = zip(value_pb.array_value.values, meaning)
        for sub_value_pb, sub_meaning in val_iter:
            if sub_meaning is not None:
                sub_value_pb.meaning = sub_meaning
    else:
        value_pb.meaning = meaning


def entity_to_protobuf(entity):
    """Converts an entity into a protobuf.

    :type entity: :class:`google.cloud.datastore.entity.Entity`
    :param entity: The entity to be turned into a protobuf.

    :rtype: :class:`.entity_pb2.Entity`
    :returns: The protobuf representing the entity.
    """
    entity_pb = entity_pb2.Entity()
    if entity.key is not None:
        key_pb = entity.key.to_protobuf()
        entity_pb._pb.key.CopyFrom(key_pb._pb)

    for name, value in entity.items():
        value_is_list = isinstance(value, list)

        value_pb = _new_value_pb(entity_pb, name)
        # Set the appropriate value.
        _set_protobuf_value(value_pb, value)

        # Add index information to protobuf.
        if name in entity.exclude_from_indexes:
            if not value_is_list:
                value_pb.exclude_from_indexes = True

            for sub_value in value_pb.array_value.values:
                sub_value.exclude_from_indexes = True

        # Add meaning information to protobuf.
        _set_pb_meaning_from_entity(
            entity, name, value, value_pb, is_list=value_is_list
        )

    return entity_pb


def get_read_options(eventual, transaction_id):
    """Validate rules for read options, and assign to the request.

    Helper method for ``lookup()`` and ``run_query``.

    :type eventual: bool
    :param eventual: Flag indicating if ``EVENTUAL`` or ``STRONG``
                     consistency should be used.

    :type transaction_id: bytes
    :param transaction_id: A transaction identifier (may be null).

    :rtype: :class:`.datastore_pb2.ReadOptions`
    :returns: The read options corresponding to the inputs.
    :raises: :class:`ValueError` if ``eventual`` is ``True`` and the
             ``transaction_id`` is not ``None``.
    """
    if transaction_id is None:
        if eventual:
            return datastore_pb2.ReadOptions(
                read_consistency=datastore_pb2.ReadOptions.ReadConsistency.EVENTUAL
            )
        else:
            return datastore_pb2.ReadOptions()
    else:
        if eventual:
            raise ValueError("eventual must be False when in a transaction")
        else:
            return datastore_pb2.ReadOptions(transaction=transaction_id)


def key_from_protobuf(pb):
    """Factory method for creating a key based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`.entity_pb2.Key`
    :param pb: The Protobuf representing the key.

    :rtype: :class:`google.cloud.datastore.key.Key`
    :returns: a new `Key` instance
    """
    path_args = []
    for element in pb.path:
        path_args.append(element.kind)
        if element.id:  # Simple field (int64)
            path_args.append(element.id)
        # This is safe: we expect proto objects returned will only have
        # one of `name` or `id` set.
        if element.name:  # Simple field (string)
            path_args.append(element.name)

    project = None
    if pb.partition_id.project_id:  # Simple field (string)
        project = pb.partition_id.project_id
    namespace = None
    if pb.partition_id.namespace_id:  # Simple field (string)
        namespace = pb.partition_id.namespace_id

    return Key(*path_args, namespace=namespace, project=project)


def _pb_attr_value(val):
    """Given a value, return the protobuf attribute name and proper value.

    The Protobuf API uses different attribute names based on value types
    rather than inferring the type.  This function simply determines the
    proper attribute name based on the type of the value provided and
    returns the attribute name as well as a properly formatted value.

    Certain value types need to be coerced into a different type (such
    as a `datetime.datetime` into an integer timestamp, or a
    `google.cloud.datastore.key.Key` into a Protobuf representation.  This
    function handles that for you.

    .. note::
       Values which are "text" ('unicode' in Python2, 'str' in Python3) map
       to 'string_value' in the datastore;  values which are "bytes"
       ('str' in Python2, 'bytes' in Python3) map to 'blob_value'.

    For example:

    .. testsetup:: pb-attr-value

        from google.cloud.datastore.helpers import _pb_attr_value

    .. doctest:: pb-attr-value

        >>> _pb_attr_value(1234)
        ('integer_value', 1234)
        >>> _pb_attr_value('my_string')
        ('string_value', 'my_string')

    :type val:
        :class:`datetime.datetime`, :class:`google.cloud.datastore.key.Key`,
        bool, float, integer, bytes, str, unicode,
        :class:`google.cloud.datastore.entity.Entity`, dict, list,
        :class:`google.cloud.datastore.helpers.GeoPoint`, NoneType
    :param val: The value to be scrutinized.

    :rtype: tuple
    :returns: A tuple of the attribute name and proper value type.
    """

    if isinstance(val, datetime.datetime):
        name = "timestamp"
        value = _datetime_to_pb_timestamp(val)
    elif isinstance(val, Key):
        name, value = "key", val.to_protobuf()
    elif isinstance(val, bool):
        name, value = "boolean", val
    elif isinstance(val, float):
        name, value = "double", val
    elif isinstance(val, int):
        name, value = "integer", val
    elif isinstance(val, str):
        name, value = "string", val
    elif isinstance(val, bytes):
        name, value = "blob", val
    elif isinstance(val, Entity):
        name, value = "entity", val
    elif isinstance(val, dict):
        entity_val = Entity(key=None)
        entity_val.update(val)
        name, value = "entity", entity_val
    elif isinstance(val, list):
        name, value = "array", val
    elif isinstance(val, GeoPoint):
        name, value = "geo_point", val.to_protobuf()
    elif val is None:
        name, value = "null", struct_pb2.NULL_VALUE
    else:
        raise ValueError("Unknown protobuf attr type", type(val))

    return name + "_value", value


def _get_value_from_value_pb(pb):
    """Given a protobuf for a Value, get the correct value.

    The Cloud Datastore Protobuf API returns a Property Protobuf which
    has one value set and the rest blank.  This function retrieves the
    the one value provided.

    Some work is done to coerce the return value into a more useful type
    (particularly in the case of a timestamp value, or a key value).

    :type pb: :class:`.entity_pb2.Value._pb`
    :param pb: The *raw* Value Protobuf.

    :rtype: object
    :returns: The value provided by the Protobuf.
    :raises: :class:`ValueError <exceptions.ValueError>` if no value type
             has been set.
    """
    value_type = pb.WhichOneof("value_type")

    if value_type == "timestamp_value":
        result = DatetimeWithNanoseconds.from_timestamp_pb(pb.timestamp_value)

    elif value_type == "key_value":
        result = key_from_protobuf(pb.key_value)

    elif value_type == "boolean_value":
        result = pb.boolean_value

    elif value_type == "double_value":
        result = pb.double_value

    elif value_type == "integer_value":
        result = pb.integer_value

    elif value_type == "string_value":
        result = pb.string_value

    elif value_type == "blob_value":
        result = pb.blob_value

    elif value_type == "entity_value":
        result = entity_from_protobuf(pb.entity_value)

    elif value_type == "array_value":
        result = [
            _get_value_from_value_pb(item_value) for item_value in pb.array_value.values
        ]

    elif value_type == "geo_point_value":
        result = GeoPoint(pb.geo_point_value.latitude, pb.geo_point_value.longitude,)

    elif value_type == "null_value":
        result = None

    else:
        raise ValueError("Value protobuf did not have any value set")

    return result


def _set_protobuf_value(value_pb, val):
    """Assign 'val' to the correct subfield of 'value_pb'.

    The Protobuf API uses different attribute names based on value types
    rather than inferring the type.

    Some value types (entities, keys, lists) cannot be directly
    assigned; this function handles them correctly.

    :type value_pb: :class:`.entity_pb2.Value`
    :param value_pb: The value protobuf to which the value is being assigned.

    :type val: :class:`datetime.datetime`, boolean, float, integer, string,
               :class:`google.cloud.datastore.key.Key`,
               :class:`google.cloud.datastore.entity.Entity`
    :param val: The value to be assigned.
    """
    attr, val = _pb_attr_value(val)
    if attr == "key_value":
        value_pb.key_value.CopyFrom(val._pb)
    elif attr == "timestamp_value":
        value_pb.timestamp_value.CopyFrom(val)
    elif attr == "entity_value":
        entity_pb = entity_to_protobuf(val)
        value_pb.entity_value.CopyFrom(entity_pb._pb)
    elif attr == "array_value":
        if len(val) == 0:
            array_value = entity_pb2.ArrayValue(values=[])._pb
            value_pb.array_value.CopyFrom(array_value)
        else:
            l_pb = value_pb.array_value.values
            for item in val:
                i_pb = l_pb.add()
                _set_protobuf_value(i_pb, item)
    elif attr == "geo_point_value":
        value_pb.geo_point_value.CopyFrom(val)
    else:  # scalar, just assign
        setattr(value_pb, attr, val)


class GeoPoint(object):
    """Simple container for a geo point value.

    :type latitude: float
    :param latitude: Latitude of a point.

    :type longitude: float
    :param longitude: Longitude of a point.
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def to_protobuf(self):
        """Convert the current object to protobuf.

        :rtype: :class:`google.type.latlng_pb2.LatLng`.
        :returns: The current point as a protobuf.
        """
        return latlng_pb2.LatLng(latitude=self.latitude, longitude=self.longitude)

    def __eq__(self, other):
        """Compare two geo points for equality.

        :rtype: bool
        :returns: True if the points compare equal, else False.
        """
        if not isinstance(other, GeoPoint):
            return NotImplemented

        return self.latitude == other.latitude and self.longitude == other.longitude

    def __ne__(self, other):
        """Compare two geo points for inequality.

        :rtype: bool
        :returns: False if the points compare equal, else True.
        """
        return not self == other
