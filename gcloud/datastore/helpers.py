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
from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key

__all__ = ('entity_from_protobuf', 'key_from_protobuf')

INT_VALUE_CHECKER = Int64ValueChecker()


def find_true_dataset_id(dataset_id, connection):
    """Find the true (unaliased) dataset ID.

    If the given ID already has a 's~' or 'e~' prefix, does nothing.
    Otherwise, looks up a bogus Key('__MissingLookupKind', 1) and reads the
    true prefixed dataset ID from the response (either from found or from
    missing).

    For some context, see:
      github.com/GoogleCloudPlatform/gcloud-python/pull/528
      github.com/GoogleCloudPlatform/google-cloud-datastore/issues/59

    :type dataset_id: string
    :param dataset_id: The dataset ID to un-alias / prefix.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to connection to the dataset.

    :rtype: string
    :returns: The true / prefixed / un-aliased dataset ID.
    """
    if dataset_id.startswith('s~') or dataset_id.startswith('e~'):
        return dataset_id

    # Create the bogus Key protobuf to be looked up and remove
    # the dataset ID so the backend won't complain.
    bogus_key_pb = Key('__MissingLookupKind', 1,
                       dataset_id=dataset_id).to_protobuf()
    bogus_key_pb.partition_id.ClearField('dataset_id')

    found_pbs, missing_pbs, _ = connection.lookup(dataset_id, [bogus_key_pb])
    # By not passing in `deferred`, lookup will continue until
    # all results are `found` or `missing`.
    all_pbs = missing_pbs + found_pbs
    # We only asked for one, so should only receive one.
    returned_pb, = all_pbs

    return returned_pb.key.partition_id.dataset_id


def entity_from_protobuf(pb):
    """Factory method for creating an entity based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`gcloud.datastore._datastore_v1_pb2.Entity`
    :param pb: The Protobuf representing the entity.

    :rtype: :class:`gcloud.datastore.entity.Entity`
    :returns: The entity derived from the protobuf.
    """
    key = None
    if pb.HasField('key'):
        key = key_from_protobuf(pb.key)

    entity_props = {}
    exclude_from_indexes = []

    for property_pb in pb.property:
        value = _get_value_from_property_pb(property_pb)
        entity_props[property_pb.name] = value

        # Check if property_pb.value was indexed. Lists need to be
        # special-cased and we require all `indexed` values in a list agree.
        if isinstance(value, list):
            indexed_values = set(value_pb.indexed
                                 for value_pb in property_pb.value.list_value)
            if len(indexed_values) != 1:
                raise ValueError('For a list_value, subvalues must either all '
                                 'be indexed or all excluded from indexes.')

            if not indexed_values.pop():
                exclude_from_indexes.append(property_pb.name)
        else:
            if not property_pb.value.indexed:
                exclude_from_indexes.append(property_pb.name)

    entity = Entity(key=key, exclude_from_indexes=exclude_from_indexes)
    entity.update(entity_props)
    return entity


def key_from_protobuf(pb):
    """Factory method for creating a key based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :param pb: The Protobuf representing the key.

    :rtype: :class:`gcloud.datastore.key.Key`
    :returns: a new `Key` instance
    """
    path_args = []
    for element in pb.path_element:
        path_args.append(element.kind)
        if element.HasField('id'):
            path_args.append(element.id)
        # This is safe: we expect proto objects returned will only have
        # one of `name` or `id` set.
        if element.HasField('name'):
            path_args.append(element.name)

    dataset_id = None
    if pb.partition_id.HasField('dataset_id'):
        dataset_id = pb.partition_id.dataset_id
    namespace = None
    if pb.partition_id.HasField('namespace'):
        namespace = pb.partition_id.namespace

    return Key(*path_args, namespace=namespace, dataset_id=dataset_id)


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

    :type value_pb: :class:`gcloud.datastore._datastore_v1_pb2.Value`
    :param value_pb: The Value Protobuf.

    :returns: The value provided by the Protobuf.
    """
    result = None
    if value_pb.HasField('timestamp_microseconds_value'):
        microseconds = value_pb.timestamp_microseconds_value
        result = _datetime_from_microseconds(microseconds)

    elif value_pb.HasField('key_value'):
        result = key_from_protobuf(value_pb.key_value)

    elif value_pb.HasField('boolean_value'):
        result = value_pb.boolean_value

    elif value_pb.HasField('double_value'):
        result = value_pb.double_value

    elif value_pb.HasField('integer_value'):
        result = value_pb.integer_value

    elif value_pb.HasField('string_value'):
        result = value_pb.string_value

    elif value_pb.HasField('blob_value'):
        result = value_pb.blob_value

    elif value_pb.HasField('entity_value'):
        result = entity_from_protobuf(value_pb.entity_value)

    elif value_pb.list_value:
        result = [_get_value_from_value_pb(x) for x in value_pb.list_value]

    return result


def _get_value_from_property_pb(property_pb):
    """Given a protobuf for a Property, get the correct value.

    The Cloud Datastore Protobuf API returns a Property Protobuf which
    has one value set and the rest blank.  This function retrieves the
    the one value provided.

    Some work is done to coerce the return value into a more useful type
    (particularly in the case of a timestamp value, or a key value).

    :type property_pb: :class:`gcloud.datastore._datastore_v1_pb2.Property`
    :param property_pb: The Property Protobuf.

    :returns: The value provided by the Protobuf.
    """
    return _get_value_from_value_pb(property_pb.value)


def _set_protobuf_value(value_pb, val):
    """Assign 'val' to the correct subfield of 'value_pb'.

    The Protobuf API uses different attribute names based on value types
    rather than inferring the type.

    Some value types (entities, keys, lists) cannot be directly
    assigned; this function handles them correctly.

    :type value_pb: :class:`gcloud.datastore._datastore_v1_pb2.Value`
    :param value_pb: The value protobuf to which the value is being assigned.

    :type val: :class:`datetime.datetime`, boolean, float, integer, string,
               :class:`gcloud.datastore.key.Key`,
               :class:`gcloud.datastore.entity.Entity`,
    :param val: The value to be assigned.
    """
    if val is None:
        value_pb.Clear()
        return

    attr, val = _pb_attr_value(val)
    if attr == 'key_value':
        value_pb.key_value.CopyFrom(val)
    elif attr == 'entity_value':
        e_pb = value_pb.entity_value
        e_pb.Clear()
        key = val.key
        if key is not None:
            e_pb.key.CopyFrom(key.to_protobuf())
        for item_key, value in val.items():
            p_pb = e_pb.property.add()
            p_pb.name = item_key
            _set_protobuf_value(p_pb.value, value)
    elif attr == 'list_value':
        l_pb = value_pb.list_value
        for item in val:
            i_pb = l_pb.add()
            _set_protobuf_value(i_pb, item)
    else:  # scalar, just assign
        setattr(value_pb, attr, val)


def _prepare_key_for_request(key_pb):
    """Add protobuf keys to a request object.

    :type key_pb: :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :param key_pb: A key to be added to a request.

    :rtype: :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :returns: A key which will be added to a request. It will be the
              original if nothing needs to be changed.
    """
    if key_pb.partition_id.HasField('dataset_id'):
        # We remove the dataset_id from the protobuf. This is because
        # the backend fails a request if the key contains un-prefixed
        # dataset ID. The backend fails because requests to
        #     /datastore/.../datasets/foo/...
        # and
        #     /datastore/.../datasets/s~foo/...
        # both go to the datastore given by 's~foo'. So if the key
        # protobuf in the request body has dataset_id='foo', the
        # backend will reject since 'foo' != 's~foo'.
        new_key_pb = datastore_pb.Key()
        new_key_pb.CopyFrom(key_pb)
        new_key_pb.partition_id.ClearField('dataset_id')
        key_pb = new_key_pb
    return key_pb
