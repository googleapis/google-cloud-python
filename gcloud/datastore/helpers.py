"""Helper methods for dealing with Cloud Datastore's Protobuf API."""
import calendar
from datetime import datetime, timedelta

import pytz

from gcloud.datastore.key import Key


def get_protobuf_attribute_and_value(val):
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

  >>> get_protobuf_attribute_and_value(1234)
  ('integer_value', 1234)
  >>> get_protobuf_attribute_and_value('my_string')
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
    name, value = 'integer', val
  elif isinstance(val, basestring):
    name, value = 'string', val

  return name + '_value', value


def get_value_from_value_pb(value_pb):
  from entity import Entity
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
  if value_pb.HasField('timestamp_microseconds_value'):
    microseconds = value_pb.timestamp_microseconds_value
    return (datetime.utcfromtimestamp(0) +
            timedelta(microseconds=microseconds))

  elif value_pb.HasField('key_value'):
    return Key.from_protobuf(value_pb.key_value)

  elif value_pb.HasField('boolean_value'):
    return value_pb.boolean_value

  elif value_pb.HasField('double_value'):
    return value_pb.double_value

  elif value_pb.HasField('integer_value'):
    return value_pb.integer_value

  elif value_pb.HasField('string_value'):
    return value_pb.string_value

  elif value_pb.HasField('blob_key_value'):
    return value_pb.blob_key_value

  elif value_pb.HasField('blob_value'):
    return value_pb.blob_value

  elif value_pb.HasField('entity_value'):
    return Entity.from_protobuf(value_pb.entity_value)

  elif value_pb.list_value:
    return [get_value_from_value_pb(k) for k in value_pb.list_value]

  else:
    return None

def get_value_from_protobuf(pb):
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
  return get_value_from_value_pb(pb.value)
