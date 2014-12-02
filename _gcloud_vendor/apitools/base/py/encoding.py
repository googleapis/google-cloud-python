#!/usr/bin/env python
"""Common code for converting proto to other formats, such as JSON."""

import base64
import collections
import datetime
import json
import logging


from protorpc import message_types
from protorpc import messages
from protorpc import protojson

from apitools.base.py import exceptions

__all__ = [
    'CopyProtoMessage',
    'JsonToMessage',
    'MessageToJson',
    'DictToMessage',
    'MessageToDict',
    'PyValueToMessage',
    'MessageToPyValue',
    'MessageToRepr',
]


_Codec = collections.namedtuple('_Codec', ['encoder', 'decoder'])
CodecResult = collections.namedtuple('CodecResult', ['value', 'complete'])


# TODO(craigcitro): Make these non-global.
_UNRECOGNIZED_FIELD_MAPPINGS = {}
_CUSTOM_MESSAGE_CODECS = {}
_CUSTOM_FIELD_CODECS = {}
_FIELD_TYPE_CODECS = {}


def MapUnrecognizedFields(field_name):
  """Register field_name as a container for unrecognized fields in message."""
  def Register(cls):
    _UNRECOGNIZED_FIELD_MAPPINGS[cls] = field_name
    return cls
  return Register


def RegisterCustomMessageCodec(encoder, decoder):
  """Register a custom encoder/decoder for this message class."""
  def Register(cls):
    _CUSTOM_MESSAGE_CODECS[cls] = _Codec(encoder=encoder, decoder=decoder)
    return cls
  return Register


def RegisterCustomFieldCodec(encoder, decoder):
  """Register a custom encoder/decoder for this field."""
  def Register(field):
    _CUSTOM_FIELD_CODECS[field] = _Codec(encoder=encoder, decoder=decoder)
    return field
  return Register


def RegisterFieldTypeCodec(encoder, decoder):
  """Register a custom encoder/decoder for all fields of this type."""
  def Register(field_type):
    _FIELD_TYPE_CODECS[field_type] = _Codec(encoder=encoder, decoder=decoder)
    return field_type
  return Register


# TODO(craigcitro): Delete this function with the switch to proto2.
def CopyProtoMessage(message):
  codec = protojson.ProtoJson()
  return codec.decode_message(type(message), codec.encode_message(message))


def MessageToJson(message, include_fields=None):
  """Convert the given message to JSON."""
  result = _ProtoJsonApiTools.Get().encode_message(message)
  return _IncludeFields(result, message, include_fields)


def JsonToMessage(message_type, message):
  """Convert the given JSON to a message of type message_type."""
  return _ProtoJsonApiTools.Get().decode_message(message_type, message)


# TODO(craigcitro): Do this directly, instead of via JSON.
def DictToMessage(d, message_type):
  """Convert the given dictionary to a message of type message_type."""
  return JsonToMessage(message_type, json.dumps(d))


def MessageToDict(message):
  """Convert the given message to a dictionary."""
  return json.loads(MessageToJson(message))


def PyValueToMessage(message_type, value):
  """Convert the given python value to a message of type message_type."""
  return JsonToMessage(message_type, json.dumps(value))


def MessageToPyValue(message):
  """Convert the given message to a python value."""
  return json.loads(MessageToJson(message))


def MessageToRepr(msg, multiline=False, **kwargs):
  """Return a repr-style string for a protorpc message.

  protorpc.Message.__repr__ does not return anything that could be considered
  python code. Adding this function lets us print a protorpc message in such
  a way that it could be pasted into code later, and used to compare against
  other things.

  Args:
    msg: protorpc.Message, the message to be repr'd.
    multiline: bool, True if the returned string should have each field
        assignment on its own line.
    **kwargs: {str:str}, Additional flags for how to format the string.

  Known **kwargs:
    shortstrings: bool, True if all string values should be truncated at
        100 characters, since when mocking the contents typically don't matter
        except for IDs, and IDs are usually less than 100 characters.
    no_modules: bool, True if the long module name should not be printed with
        each type.

  Returns:
    str, A string of valid python (assuming the right imports have been made)
    that recreates the message passed into this function.
  """

  # TODO(user): craigcitro suggests a pretty-printer from apitools/gen.

  indent = kwargs.get('indent', 0)

  def IndentKwargs(kwargs):
    kwargs = dict(kwargs)
    kwargs['indent'] = kwargs.get('indent', 0) + 4
    return kwargs

  if isinstance(msg, list):
    s = '['
    for item in msg:
      if multiline:
        s += '\n' + ' '*(indent + 4)
      s += MessageToRepr(
          item, multiline=multiline, **IndentKwargs(kwargs)) + ','
    if multiline:
      s += '\n' + ' '*indent
    s += ']'
    return s

  if isinstance(msg, messages.Message):
    s = type(msg).__name__ + '('
    if not kwargs.get('no_modules'):
      s = msg.__module__ + '.' + s
    names = sorted([field.name for field in msg.all_fields()])
    for name in names:
      field = msg.field_by_name(name)
      if multiline:
        s += '\n' + ' '*(indent + 4)
      value = getattr(msg, field.name)
      s += field.name + '=' + MessageToRepr(
          value, multiline=multiline, **IndentKwargs(kwargs)) + ','
    if multiline:
      s += '\n'+' '*indent
    s += ')'
    return s

  if isinstance(msg, basestring):
    if kwargs.get('shortstrings') and len(msg) > 100:
      msg = msg[:100]

  if isinstance(msg, datetime.datetime):

    class SpecialTZInfo(datetime.tzinfo):

      def __init__(self, offset):
        super(SpecialTZInfo, self).__init__()
        self.offset = offset

      def __repr__(self):
        s = 'TimeZoneOffset(' + repr(self.offset) + ')'
        if not kwargs.get('no_modules'):
          s = 'protorpc.util.' + s
        return s

    msg = datetime.datetime(
        msg.year, msg.month, msg.day, msg.hour, msg.minute, msg.second,
        msg.microsecond, SpecialTZInfo(msg.tzinfo.utcoffset(0)))

  return repr(msg)


def _GetField(message, field_path):
  for field in field_path:
    if field not in dir(message):
      raise KeyError('no field "%s"' % field)
    message = getattr(message, field)
  return message


def _SetField(dictblob, field_path, value):
  for field in field_path[:-1]:
    dictblob[field] = {}
    dictblob = dictblob[field]
  dictblob[field_path[-1]] = value


def _IncludeFields(encoded_message, message, include_fields):
  """Add the requested fields to the encoded message."""
  if include_fields is None:
    return encoded_message
  result = json.loads(encoded_message)
  for field_name in include_fields:
    try:
      value = _GetField(message, field_name.split('.'))
      nullvalue = None
      if isinstance(value, list):
        nullvalue = []
    except KeyError:
      raise exceptions.InvalidDataError(
          'No field named %s in message of type %s' % (
              field_name, type(message)))
    _SetField(result, field_name.split('.'), nullvalue)
  return json.dumps(result)


def _GetFieldCodecs(field, attr):
  result = [
      getattr(_CUSTOM_FIELD_CODECS.get(field), attr, None),
      getattr(_FIELD_TYPE_CODECS.get(type(field)), attr, None),
  ]
  return [x for x in result if x is not None]


class _ProtoJsonApiTools(protojson.ProtoJson):
  """JSON encoder used by apitools clients."""
  _INSTANCE = None

  @classmethod
  def Get(cls):
    if cls._INSTANCE is None:
      cls._INSTANCE = cls()
    return cls._INSTANCE

  def decode_message(self, message_type, encoded_message):
    if message_type in _CUSTOM_MESSAGE_CODECS:
      return _CUSTOM_MESSAGE_CODECS[message_type].decoder(encoded_message)
    # We turn off the default logging in protorpc. We may want to
    # remove this later.
    old_level = logging.getLogger().level
    logging.getLogger().setLevel(logging.ERROR)
    result = super(_ProtoJsonApiTools, self).decode_message(
        message_type, encoded_message)
    logging.getLogger().setLevel(old_level)
    result = _ProcessUnknownEnums(result, encoded_message)
    result = _ProcessUnknownMessages(result, encoded_message)
    return _DecodeUnknownFields(result, encoded_message)

  def decode_field(self, field, value):
    """Decode the given JSON value.

    Args:
      field: a messages.Field for the field we're decoding.
      value: a python value we'd like to decode.

    Returns:
      A value suitable for assignment to field.
    """
    for decoder in _GetFieldCodecs(field, 'decoder'):
      result = decoder(field, value)
      value = result.value
      if result.complete:
        return value
    if isinstance(field, messages.MessageField):
      field_value = self.decode_message(field.message_type, json.dumps(value))
    elif isinstance(field, messages.EnumField):
      try:
        field_value = super(_ProtoJsonApiTools, self).decode_field(field, value)
      except messages.DecodeError:
        if not isinstance(value, basestring):
          raise
        field_value = None
    else:
      field_value = super(_ProtoJsonApiTools, self).decode_field(field, value)
    return field_value

  def encode_message(self, message):
    if isinstance(message, messages.FieldList):
      return '[%s]' % (', '.join(self.encode_message(x) for x in message))
    if type(message) in _CUSTOM_MESSAGE_CODECS:
      return _CUSTOM_MESSAGE_CODECS[type(message)].encoder(message)
    message = _EncodeUnknownFields(message)
    return super(_ProtoJsonApiTools, self).encode_message(message)

  def encode_field(self, field, value):
    """Encode the given value as JSON.

    Args:
      field: a messages.Field for the field we're encoding.
      value: a value for field.

    Returns:
      A python value suitable for json.dumps.
    """
    for encoder in _GetFieldCodecs(field, 'encoder'):
      result = encoder(field, value)
      value = result.value
      if result.complete:
        return value
    if (isinstance(field, messages.MessageField) and
        not isinstance(field, message_types.DateTimeField)):
      value = json.loads(self.encode_message(value))
    return super(_ProtoJsonApiTools, self).encode_field(field, value)


# TODO(craigcitro): Fold this and _IncludeFields in as codecs.
def _DecodeUnknownFields(message, encoded_message):
  """Rewrite unknown fields in message into message.destination."""
  destination = _UNRECOGNIZED_FIELD_MAPPINGS.get(type(message))
  if destination is None:
    return message
  pair_field = message.field_by_name(destination)
  if not isinstance(pair_field, messages.MessageField):
    raise exceptions.InvalidDataFromServerError(
        'Unrecognized fields must be mapped to a compound '
        'message type.')
  pair_type = pair_field.message_type
  # TODO(craigcitro): Add more error checking around the pair
  # type being exactly what we suspect (field names, etc).
  if isinstance(pair_type.value, messages.MessageField):
    new_values = _DecodeUnknownMessages(
        message, json.loads(encoded_message), pair_type)
  else:
    new_values = _DecodeUnrecognizedFields(message, pair_type)
  setattr(message, destination, new_values)
  # We could probably get away with not setting this, but
  # why not clear it?
  setattr(message, '_Message__unrecognized_fields', {})
  return message


def _DecodeUnknownMessages(message, encoded_message, pair_type):
  """Process unknown fields in encoded_message of a message type."""
  field_type = pair_type.value.type
  new_values = []
  all_field_names = [x.name for x in message.all_fields()]
  for name, value_dict in encoded_message.iteritems():
    if name in all_field_names:
      continue
    value = PyValueToMessage(field_type, value_dict)
    new_pair = pair_type(key=name, value=value)
    new_values.append(new_pair)
  return new_values


def _DecodeUnrecognizedFields(message, pair_type):
  """Process unrecognized fields in message."""
  new_values = []
  for unknown_field in message.all_unrecognized_fields():
    # TODO(craigcitro): Consider validating the variant if
    # the assignment below doesn't take care of it. It may
    # also be necessary to check it in the case that the
    # type has multiple encodings.
    value, _ = message.get_unrecognized_field_info(unknown_field)
    value_type = pair_type.field_by_name('value')
    if isinstance(value_type, messages.MessageField):
      decoded_value = DictToMessage(value, pair_type.value.message_type)
    else:
      decoded_value = value
    new_pair = pair_type(key=str(unknown_field), value=decoded_value)
    new_values.append(new_pair)
  return new_values


def _EncodeUnknownFields(message):
  """Remap unknown fields in message out of message.source."""
  source = _UNRECOGNIZED_FIELD_MAPPINGS.get(type(message))
  if source is None:
    return message
  result = CopyProtoMessage(message)
  pairs_field = message.field_by_name(source)
  if not isinstance(pairs_field, messages.MessageField):
    raise exceptions.InvalidUserInputError(
        'Invalid pairs field %s' % pairs_field)
  pairs_type = pairs_field.message_type
  value_variant = pairs_type.field_by_name('value').variant
  pairs = getattr(message, source)
  for pair in pairs:
    if value_variant == messages.Variant.MESSAGE:
      encoded_value = MessageToDict(pair.value)
    else:
      encoded_value = pair.value
    result.set_unrecognized_field(pair.key, encoded_value, value_variant)
  setattr(result, source, [])
  return result


def _SafeEncodeBytes(field, value):
  """Encode the bytes in value as urlsafe base64."""
  try:
    if field.repeated:
      result = [base64.urlsafe_b64encode(byte) for byte in value]
    else:
      result = base64.urlsafe_b64encode(value)
    complete = True
  except TypeError:
    result = value
    complete = False
  return CodecResult(value=result, complete=complete)


def _SafeDecodeBytes(unused_field, value):
  """Decode the urlsafe base64 value into bytes."""
  try:
    result = base64.urlsafe_b64decode(str(value))
    complete = True
  except TypeError:
    result = value
    complete = False
  return CodecResult(value=result, complete=complete)


def _ProcessUnknownEnums(message, encoded_message):
  """Add unknown enum values from encoded_message as unknown fields.

  ProtoRPC diverges from the usual protocol buffer behavior here and
  doesn't allow unknown fields. Throwing on unknown fields makes it
  impossible to let servers add new enum values and stay compatible
  with older clients, which isn't reasonable for us. We simply store
  unrecognized enum values as unknown fields, and all is well.

  Args:
    message: Proto message we've decoded thus far.
    encoded_message: JSON string we're decoding.

  Returns:
    message, with any unknown enums stored as unrecognized fields.
  """
  if not encoded_message:
    return message
  decoded_message = json.loads(encoded_message)
  for field in message.all_fields():
    if (isinstance(field, messages.EnumField) and
        field.name in decoded_message and
        message.get_assigned_value(field.name) is None):
      message.set_unrecognized_field(field.name, decoded_message[field.name],
                                     messages.Variant.ENUM)
  return message


def _ProcessUnknownMessages(message, encoded_message):
  """Store any remaining unknown fields as strings.

  ProtoRPC currently ignores unknown values for which no type can be
  determined (and logs a "No variant found" message). For the purposes
  of reserializing, this is quite harmful (since it throws away
  information). Here we simply add those as unknown fields of type
  string (so that they can easily be reserialized).

  Args:
    message: Proto message we've decoded thus far.
    encoded_message: JSON string we're decoding.

  Returns:
    message, with any remaining unrecognized fields saved.
  """
  if not encoded_message:
    return message
  decoded_message = json.loads(encoded_message)
  message_fields = [x.name for x in message.all_fields()] + list(
      message.all_unrecognized_fields())
  missing_fields = [x for x in decoded_message.iterkeys()
                    if x not in message_fields]
  for field_name in missing_fields:
    message.set_unrecognized_field(field_name, decoded_message[field_name],
                                   messages.Variant.STRING)
  return message


RegisterFieldTypeCodec(_SafeEncodeBytes, _SafeDecodeBytes)(messages.BytesField)
