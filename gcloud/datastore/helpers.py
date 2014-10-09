"""Helper methods for dealing with Cloud Datastore's Protobuf API."""
import calendar
from datetime import datetime, timedelta

from google.protobuf.internal.type_checkers import Int64ValueChecker
import pytz

from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key

INT_VALUE_CHECKER = Int64ValueChecker()


def _get_protobuf_attribute_and_value(val):
    """Given a value, return the protobuf attribute name and proper value.

    The Protobuf API uses different attribute names
    based on value types rather than inferring the type.
    This method simply determines the proper attribute name
    based on the type of the value provided
    and returns the attribute name
    as well as a properly formatted value.

    Certain value types need to be coerced into a different type (such as a
    `datetime.datetime` into an integer timestamp, or a
    `gcloud.datastore.key.Key` into a Protobuf representation.
    This method handles that for you.

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

    if isinstance(val, datetime):
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
    elif isinstance(val, basestring):
        name, value = 'string', val
    elif isinstance(val, Entity):
        name, value = 'entity', val
    else:
        raise ValueError("Unknown protobuf attr type %s" % type(val))

    return name + '_value', value


def _get_value_from_protobuf(pb):
    """Given a protobuf for a Property, get the correct value.

    The Cloud Datastore Protobuf API returns a Property Protobuf
    which has one value set and the rest blank.
    This method retrieves the the one value provided.

    Some work is done to coerce the return value into a more useful type
    (particularly in the case of a timestamp value, or a key value).

    :type pb: :class:`gcloud.datastore.datastore_v1_pb2.Property`
    :param pb: The Property Protobuf.

    :returns: The value provided by the Protobuf.
    """

    if pb.value.HasField('timestamp_microseconds_value'):
        microseconds = pb.value.timestamp_microseconds_value
        naive = (datetime.utcfromtimestamp(0) +
                 timedelta(microseconds=microseconds))
        return naive.replace(tzinfo=pytz.utc)

    elif pb.value.HasField('key_value'):
        return Key.from_protobuf(pb.value.key_value)

    elif pb.value.HasField('boolean_value'):
        return pb.value.boolean_value

    elif pb.value.HasField('double_value'):
        return pb.value.double_value

    elif pb.value.HasField('integer_value'):
        return pb.value.integer_value

    elif pb.value.HasField('string_value'):
        return pb.value.string_value

    elif pb.value.HasField('entity_value'):
        return Entity.from_protobuf(pb.value.entity_value)

    else:
        return None


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
    attr, val = _get_protobuf_attribute_and_value(val)
    if attr == 'key_value':
        value_pb.key_value.CopyFrom(val)
    elif attr == 'entity_value':
        e_pb = value_pb.entity_value
        e_pb.Clear()
        key = val.key()
        if key is not None:
            e_pb.key.CopyFrom(key.to_protobuf())
        for k, v in val.items():
            p_pb = e_pb.property.add()
            p_pb.name = k
            _set_protobuf_value(p_pb.value, v)
    else:  # scalar, just assign
        setattr(value_pb, attr, val)
