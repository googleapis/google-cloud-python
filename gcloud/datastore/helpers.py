# Copyright 2014 Google Inc. All rights reserved.
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

from google.protobuf.internal.type_checkers import Int64ValueChecker
import six

from gcloud._helpers import _datetime_from_microseconds
from gcloud._helpers import _microseconds_from_datetime
from gcloud.datastore._generated import entity_pb2 as _entity_pb2
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key

__all__ = ('entity_from_protobuf', 'key_from_protobuf')

INT_VALUE_CHECKER = Int64ValueChecker()


def find_true_project(project, connection):
    """Find the true (unaliased) project.

    If the given ID already has a 's~' or 'e~' prefix, does nothing.
    Otherwise, looks up a bogus Key('__MissingLookupKind', 1) and reads the
    true prefixed project from the response (either from found or from
    missing).

    For some context, see:
      github.com/GoogleCloudPlatform/gcloud-python/pull/528
      github.com/GoogleCloudPlatform/google-cloud-datastore/issues/59

    :type project: string
    :param project: The project to un-alias / prefix.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to connect to the project.

    :rtype: string
    :returns: The true / prefixed / un-aliased project.
    """
    if project.startswith('s~') or project.startswith('e~'):
        return project

    # Create the bogus Key protobuf to be looked up and remove
    # the project so the backend won't complain.
    bogus_key_pb = Key('__MissingLookupKind', 1,
                       project=project).to_protobuf()
    bogus_key_pb.partition_id.ClearField('dataset_id')

    found_pbs, missing_pbs, _ = connection.lookup(project, [bogus_key_pb])
    # By not passing in `deferred`, lookup will continue until
    # all results are `found` or `missing`.
    all_pbs = missing_pbs + found_pbs
    # We only asked for one, so should only receive one.
    returned_pb, = all_pbs

    return returned_pb.key.partition_id.dataset_id


def _get_meaning(value_pb, is_list=False):
    """Get the meaning from a protobuf value.

    :type value_pb: :class:`gcloud.datastore._generated.entity_pb2.Value`
    :param value_pb: The protobuf value to be checked for an
                     associated meaning.

    :type is_list: bool
    :param is_list: Boolean indicating if the ``value_pb`` contains
                    a list value.

    :rtype: int
    :returns: The meaning for the ``value_pb`` if one is set, else
              :data:`None`.
    :raises: :class:`ValueError <exceptions.ValueError>` if a list value
             has disagreeing meanings (in sub-elements) or has some
             elements with meanings and some without.
    """
    meaning = None
    if is_list:
        # An empty list will have no values, hence no shared meaning
        # set among them.
        if len(value_pb.list_value) == 0:
            return None

        # We check among all the meanings, some of which may be None,
        # the rest which may be enum/int values.
        all_meanings = set(_get_meaning(sub_value_pb)
                           for sub_value_pb in value_pb.list_value)
        meaning = all_meanings.pop()
        # The value we popped off should have been unique. If not
        # then we can't handle a list with values that have more
        # than one meaning.
        if all_meanings:
            raise ValueError('Different meanings set on values '
                             'within a list_value')
    elif value_pb.meaning:  # Simple field (int32)
        meaning = value_pb.meaning

    return meaning


def _new_value_pb(entity_pb, name):
    """Add (by name) a new ``Value`` protobuf to an entity protobuf.

    :type entity_pb: :class:`gcloud.datastore._generated.entity_pb2.Entity`
    :param entity_pb: An entity protobuf to add a new property to.

    :type name: string
    :param name: The name of the new property.

    :rtype: :class:`gcloud.datastore._generated.entity_pb2.Value`
    :returns: The new ``Value`` protobuf that was added to the entity.
    """
    property_pb = entity_pb.property.add()
    property_pb.name = name
    return property_pb.value


def _property_tuples(entity_pb):
    """Iterator of name, ``Value`` tuples from entity properties.

    :type entity_pb: :class:`gcloud.datastore._generated.entity_pb2.Entity`
    :param entity_pb: An entity protobuf to add a new property to.

    :rtype: :class:`generator`
    :returns: An iterator that yields tuples of a name and ``Value``
              corresponding to properties on the entity.
    """
    for property_pb in entity_pb.property:
        yield property_pb.name, property_pb.value


def entity_from_protobuf(pb):
    """Factory method for creating an entity based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`gcloud.datastore._generated.entity_pb2.Entity`
    :param pb: The Protobuf representing the entity.

    :rtype: :class:`gcloud.datastore.entity.Entity`
    :returns: The entity derived from the protobuf.
    """
    key = None
    if pb.HasField('key'):  # Message field (Key)
        key = key_from_protobuf(pb.key)

    entity_props = {}
    entity_meanings = {}
    exclude_from_indexes = []

    for prop_name, value_pb in _property_tuples(pb):
        value = _get_value_from_value_pb(value_pb)
        entity_props[prop_name] = value

        # Check if the property has an associated meaning.
        is_list = isinstance(value, list)
        meaning = _get_meaning(value_pb, is_list=is_list)
        if meaning is not None:
            entity_meanings[prop_name] = (meaning, value)

        # Check if ``value_pb`` was indexed. Lists need to be special-cased
        # and we require all ``indexed`` values in a list agree.
        if is_list:
            indexed_values = set(value_pb.indexed
                                 for value_pb in value_pb.list_value)
            if len(indexed_values) != 1:
                raise ValueError('For a list_value, subvalues must either all '
                                 'be indexed or all excluded from indexes.')

            if not indexed_values.pop():
                exclude_from_indexes.append(prop_name)
        else:
            if not value_pb.indexed:
                exclude_from_indexes.append(prop_name)

    entity = Entity(key=key, exclude_from_indexes=exclude_from_indexes)
    entity.update(entity_props)
    entity._meanings.update(entity_meanings)
    return entity


def entity_to_protobuf(entity):
    """Converts an entity into a protobuf.

    :type entity: :class:`gcloud.datastore.entity.Entity`
    :param entity: The entity to be turned into a protobuf.

    :rtype: :class:`gcloud.datastore._generated.entity_pb2.Entity`
    :returns: The protobuf representing the entity.
    """
    entity_pb = _entity_pb2.Entity()
    if entity.key is not None:
        key_pb = entity.key.to_protobuf()
        entity_pb.key.CopyFrom(key_pb)

    for name, value in entity.items():
        value_is_list = isinstance(value, list)
        if value_is_list and len(value) == 0:
            continue

        value_pb = _new_value_pb(entity_pb, name)
        # Set the appropriate value.
        _set_protobuf_value(value_pb, value)

        # Add index information to protobuf.
        if name in entity.exclude_from_indexes:
            if not value_is_list:
                value_pb.indexed = False

            for sub_value in value_pb.list_value:
                sub_value.indexed = False

        # Add meaning information to protobuf.
        if name in entity._meanings:
            meaning, orig_value = entity._meanings[name]
            # Only add the meaning back to the protobuf if the value is
            # unchanged from when it was originally read from the API.
            if orig_value is value:
                # For lists, we set meaning on each sub-element.
                if value_is_list:
                    for sub_value_pb in value_pb.list_value:
                        sub_value_pb.meaning = meaning
                else:
                    value_pb.meaning = meaning

    return entity_pb


def key_from_protobuf(pb):
    """Factory method for creating a key based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`gcloud.datastore._generated.entity_pb2.Key`
    :param pb: The Protobuf representing the key.

    :rtype: :class:`gcloud.datastore.key.Key`
    :returns: a new `Key` instance
    """
    path_args = []
    for element in pb.path_element:
        path_args.append(element.kind)
        if element.id:  # Simple field (int64)
            path_args.append(element.id)
        # This is safe: we expect proto objects returned will only have
        # one of `name` or `id` set.
        if element.name:  # Simple field (string)
            path_args.append(element.name)

    project = None
    if pb.partition_id.dataset_id:  # Simple field (string)
        project = pb.partition_id.dataset_id
    namespace = None
    if pb.partition_id.namespace:  # Simple field (string)
        namespace = pb.partition_id.namespace

    return Key(*path_args, namespace=namespace, project=project)


def _pb_attr_value(val):
    """Given a value, return the protobuf attribute name and proper value.

    The Protobuf API uses different attribute names based on value types
    rather than inferring the type.  This function simply determines the
    proper attribute name based on the type of the value provided and
    returns the attribute name as well as a properly formatted value.

    Certain value types need to be coerced into a different type (such
    as a `datetime.datetime` into an integer timestamp, or a
    `gcloud.datastore.key.Key` into a Protobuf representation.  This
    function handles that for you.

    .. note::
       Values which are "text" ('unicode' in Python2, 'str' in Python3) map
       to 'string_value' in the datastore;  values which are "bytes"
       ('str' in Python2, 'bytes' in Python3) map to 'blob_value'.

    For example:

    >>> _pb_attr_value(1234)
    ('integer_value', 1234)
    >>> _pb_attr_value('my_string')
    ('string_value', 'my_string')

    :type val: `datetime.datetime`, :class:`gcloud.datastore.key.Key`,
               bool, float, integer, string
    :param val: The value to be scrutinized.

    :returns: A tuple of the attribute name and proper value type.
    """

    if isinstance(val, datetime.datetime):
        name = 'timestamp_microseconds'
        value = _microseconds_from_datetime(val)
    elif isinstance(val, Key):
        name, value = 'key', val.to_protobuf()
    elif isinstance(val, bool):
        name, value = 'boolean', val
    elif isinstance(val, float):
        name, value = 'double', val
    elif isinstance(val, six.integer_types):
        INT_VALUE_CHECKER.CheckValue(val)   # Raise an exception if invalid.
        name, value = 'integer', int(val)  # Always cast to an integer.
    elif isinstance(val, six.text_type):
        name, value = 'string', val
    elif isinstance(val, (bytes, str)):
        name, value = 'blob', val
    elif isinstance(val, Entity):
        name, value = 'entity', val
    elif isinstance(val, list):
        name, value = 'list', val
    else:
        raise ValueError("Unknown protobuf attr type %s" % type(val))

    return name + '_value', value


def _get_value_from_value_pb(value_pb):
    """Given a protobuf for a Value, get the correct value.

    The Cloud Datastore Protobuf API returns a Property Protobuf which
    has one value set and the rest blank.  This function retrieves the
    the one value provided.

    Some work is done to coerce the return value into a more useful type
    (particularly in the case of a timestamp value, or a key value).

    :type value_pb: :class:`gcloud.datastore._generated.entity_pb2.Value`
    :param value_pb: The Value Protobuf.

    :returns: The value provided by the Protobuf.
    """
    result = None
    # Simple field (int64)
    if value_pb.HasField('timestamp_microseconds_value'):
        microseconds = value_pb.timestamp_microseconds_value
        result = _datetime_from_microseconds(microseconds)

    elif value_pb.HasField('key_value'):  # Message field (Key)
        result = key_from_protobuf(value_pb.key_value)

    elif value_pb.HasField('boolean_value'):  # Simple field (bool)
        result = value_pb.boolean_value

    elif value_pb.HasField('double_value'):  # Simple field (double)
        result = value_pb.double_value

    elif value_pb.HasField('integer_value'):  # Simple field (int64)
        result = value_pb.integer_value

    elif value_pb.HasField('string_value'):  # Simple field (string)
        result = value_pb.string_value

    elif value_pb.HasField('blob_value'):  # Simple field (bytes)
        result = value_pb.blob_value

    elif value_pb.HasField('entity_value'):  # Message field (Entity)
        result = entity_from_protobuf(value_pb.entity_value)

    elif value_pb.list_value:
        result = [_get_value_from_value_pb(value)
                  for value in value_pb.list_value]

    return result


def _set_protobuf_value(value_pb, val):
    """Assign 'val' to the correct subfield of 'value_pb'.

    The Protobuf API uses different attribute names based on value types
    rather than inferring the type.

    Some value types (entities, keys, lists) cannot be directly
    assigned; this function handles them correctly.

    :type value_pb: :class:`gcloud.datastore._generated.entity_pb2.Value`
    :param value_pb: The value protobuf to which the value is being assigned.

    :type val: :class:`datetime.datetime`, boolean, float, integer, string,
               :class:`gcloud.datastore.key.Key`,
               :class:`gcloud.datastore.entity.Entity`
    :param val: The value to be assigned.
    """
    if val is None:
        value_pb.Clear()
        return

    attr, val = _pb_attr_value(val)
    if attr == 'key_value':
        value_pb.key_value.CopyFrom(val)
    elif attr == 'entity_value':
        entity_pb = entity_to_protobuf(val)
        value_pb.entity_value.CopyFrom(entity_pb)
    elif attr == 'list_value':
        l_pb = value_pb.list_value
        for item in val:
            i_pb = l_pb.add()
            _set_protobuf_value(i_pb, item)
    else:  # scalar, just assign
        setattr(value_pb, attr, val)


def _prepare_key_for_request(key_pb):
    """Add protobuf keys to a request object.

    :type key_pb: :class:`gcloud.datastore._generated.entity_pb2.Key`
    :param key_pb: A key to be added to a request.

    :rtype: :class:`gcloud.datastore._generated.entity_pb2.Key`
    :returns: A key which will be added to a request. It will be the
              original if nothing needs to be changed.
    """
    if key_pb.partition_id.dataset_id:  # Simple field (string)
        # We remove the dataset_id from the protobuf. This is because
        # the backend fails a request if the key contains un-prefixed
        # project. The backend fails because requests to
        #     /datastore/.../datasets/foo/...
        # and
        #     /datastore/.../datasets/s~foo/...
        # both go to the datastore given by 's~foo'. So if the key
        # protobuf in the request body has dataset_id='foo', the
        # backend will reject since 'foo' != 's~foo'.
        new_key_pb = _entity_pb2.Key()
        new_key_pb.CopyFrom(key_pb)
        new_key_pb.partition_id.ClearField('dataset_id')
        key_pb = new_key_pb
    return key_pb
