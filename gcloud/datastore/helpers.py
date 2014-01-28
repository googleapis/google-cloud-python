"""Helper methods for dealing with Cloud Datastore's Protobuf API."""
from datetime import datetime

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
    name, value = 'timestamp_microseconds', time.mktime(val.timetuple())
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

  if pb.value.HasField('timestamp_microseconds_value'):
    timestamp = pb.value.timestamp_microseconds_value / 1e6
    return datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)

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

  else:
    # TODO(jjg): Should we raise a ValueError here?
    return None
