"""Helper functions for dealing with Cloud Datastore's Protobuf API.

The non-private functions are part of the API.
"""
__all__ = ('entity_from_protobuf', 'key_from_protobuf')

import calendar
import datetime

from google.protobuf.internal.type_checkers import Int64ValueChecker
import pytz

from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key

INT_VALUE_CHECKER = Int64ValueChecker()


def entity_from_protobuf(pb, dataset=None):
    """Factory method for creating an entity based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`gcloud.datastore.datastore_v1_pb2.Entity`
    :param pb: The Protobuf representing the entity.

    :rtype: :class:`gcloud.datastore.entity.Entity`
    :returns: The entity derived from the protobuf.
    """
    key = key_from_protobuf(pb.key)
    entity = Entity.from_key(key, dataset)

    for property_pb in pb.property:
        value = _get_value_from_property_pb(property_pb)
        entity[property_pb.name] = value

    return entity


def key_from_protobuf(pb):
    """Factory method for creating a key based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore
    Protobuf API.

    :type pb: :class:`gcloud.datastore.datastore_v1_pb2.Key`
    :param pb: The Protobuf representing the key.

    :rtype: :class:`gcloud.datastore.key.Key`
    :returns: a new `Key` instance
    """
    path = []
    for element in pb.path_element:
        element_dict = {'kind': element.kind}

        if element.HasField('id'):
            element_dict['id'] = element.id

        # This is safe: we expect proto objects returned will only have
        # one of `name` or `id` set.
        if element.HasField('name'):
            element_dict['name'] = element.name

        path.append(element_dict)

    dataset_id = None
    if pb.partition_id.HasField('dataset_id'):
        dataset_id = pb.partition_id.dataset_id
    namespace = None
    if pb.partition_id.HasField('namespace'):
        namespace = pb.partition_id.namespace

    return Key(path, namespace, dataset_id)


def _get_protobuf_attribute_and_value(val):
    """Given a value, return the protobuf attribute name and proper value.

    The Protobuf API uses different attribute names
    based on value types rather than inferring the type.
    This function simply determines the proper attribute name
    based on the type of the value provided
    and returns the attribute name
    as well as a properly formatted value.

    Certain value types need to be coerced into a different type (such as a
    `datetime.datetime` into an integer timestamp, or a
    `gcloud.datastore.key.Key` into a Protobuf representation.
    This function handles that for you.

    .. note::
       Values which are "text" ('unicode' in Python2, 'str' in Python3) map
       to 'string_value' in the datastore;  values which are "bytes"
       ('str' in Python2, 'bytes' in Python3) map to 'blob_value'.

    For example:

    >>> _get_protobuf_attribute_and_value(1234)
    ('integer_value', 1234)
    >>> _get_protobuf_attribute_and_value('my_string')
    ('string_value', 'my_string')

    :type val: `datetime.datetime`, :class:`gcloud.datastore.key.Key`,
               bool, float, integer, string
    :param val: The value to be scrutinized.

    :returns: A tuple of the attribute name and proper value type.
    """

    if isinstance(val, datetime.datetime):
        name = 'timestamp_microseconds'
        # If the datetime is naive (no timezone), consider that it was
        # intended to be UTC and replace the tzinfo to that effect.
        if not val.tzinfo:
            val = val.replace(tzinfo=pytz.utc)
        # Regardless of what timezone is on the value, convert it to UTC.
        val = val.astimezone(pytz.utc)
        # Convert the datetime to a microsecond timestamp.
        value = long(calendar.timegm(val.timetuple()) * 1e6) + val.microsecond
    elif isinstance(val, Key):
        name, value = 'key', val.to_protobuf()
    elif isinstance(val, bool):
        name, value = 'boolean', val
    elif isinstance(val, float):
        name, value = 'double', val
    elif isinstance(val, (int, long)):
        INT_VALUE_CHECKER.CheckValue(val)   # Raise an exception if invalid.
        name, value = 'integer', long(val)  # Always cast to a long.
    elif isinstance(val, unicode):
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

    The Cloud Datastore Protobuf API returns a Property Protobuf
    which has one value set and the rest blank.
    This function retrieves the the one value provided.

    Some work is done to coerce the return value into a more useful type
    (particularly in the case of a timestamp value, or a key value).

    :type value_pb: :class:`gcloud.datastore.datastore_v1_pb2.Value`
    :param value_pb: The Value Protobuf.

    :returns: The value provided by the Protobuf.
    """

    result = None
    if value_pb.HasField('timestamp_microseconds_value'):
        microseconds = value_pb.timestamp_microseconds_value
        naive = (datetime.datetime.utcfromtimestamp(0) +
                 datetime.timedelta(microseconds=microseconds))
        result = naive.replace(tzinfo=pytz.utc)

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

    The Cloud Datastore Protobuf API returns a Property Protobuf
    which has one value set and the rest blank.
    This function retrieves the the one value provided.

    Some work is done to coerce the return value into a more useful type
    (particularly in the case of a timestamp value, or a key value).

    :type property_pb: :class:`gcloud.datastore.datastore_v1_pb2.Property`
    :param property_pb: The Property Protobuf.

    :returns: The value provided by the Protobuf.
    """
    return _get_value_from_value_pb(property_pb.value)


def _set_protobuf_value(value_pb, val):
    """Assign 'val' to the correct subfield of 'value_pb'.

    The Protobuf API uses different attribute names
    based on value types rather than inferring the type.

    Some value types (entities, keys, lists) cannot be directly assigned;
    this function handles them correctly.

    :type value_pb: :class:`gcloud.datastore.datastore_v1_pb2.Value`
    :param value_pb: The value protobuf to which the value is being assigned.

    :type val: `datetime.datetime`, bool, float, integer, string
               :class:`gcloud.datastore.key.Key`,
               :class:`gcloud.datastore.entity.Entity`,
    :param val: The value to be assigned.
    """
    if val is None:
        value_pb.Clear()
        return

    attr, val = _get_protobuf_attribute_and_value(val)
    if attr == 'key_value':
        value_pb.key_value.CopyFrom(val)
    elif attr == 'entity_value':
        e_pb = value_pb.entity_value
        e_pb.Clear()
        key = val.key()
        if key is not None:
            e_pb.key.CopyFrom(key.to_protobuf())
        for item_key, value in val.iteritems():
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
