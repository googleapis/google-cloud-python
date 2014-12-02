#!/usr/bin/env python


import base64
import datetime
import json

from protorpc import message_types
from protorpc import messages
from protorpc import util
import unittest2

from apitools.base.py import encoding


class SimpleMessage(messages.Message):
  field = messages.StringField(1)
  repfield = messages.StringField(2, repeated=True)


class BytesMessage(messages.Message):
  field = messages.BytesField(1)
  repfield = messages.BytesField(2, repeated=True)


class TimeMessage(messages.Message):
  timefield = message_types.DateTimeField(3)


@encoding.MapUnrecognizedFields('additional_properties')
class AdditionalPropertiesMessage(messages.Message):

  class AdditionalProperty(messages.Message):
    key = messages.StringField(1)
    value = messages.StringField(2)

  additional_properties = messages.MessageField(
      AdditionalProperty, 1, repeated=True)


class CompoundPropertyType(messages.Message):
  index = messages.IntegerField(1)
  name = messages.StringField(2)


class MessageWithEnum(messages.Message):

  class ThisEnum(messages.Enum):
    VALUE_ONE = 1
    VALUE_TWO = 2

  field_one = messages.EnumField(ThisEnum, 1)
  field_two = messages.EnumField(ThisEnum, 2, default=ThisEnum.VALUE_TWO)
  ignored_field = messages.EnumField(ThisEnum, 3)


@encoding.MapUnrecognizedFields('additional_properties')
class AdditionalMessagePropertiesMessage(messages.Message):

  class AdditionalProperty(messages.Message):
    key = messages.StringField(1)
    value = messages.MessageField(CompoundPropertyType, 2)

  additional_properties = messages.MessageField(
      'AdditionalProperty', 1, repeated=True)


class HasNestedMessage(messages.Message):
  nested = messages.MessageField(AdditionalPropertiesMessage, 1)
  nested_list = messages.StringField(2, repeated=True)


class ExtraNestedMessage(messages.Message):
  nested = messages.MessageField(HasNestedMessage, 1)


class EncodingTest(unittest2.TestCase):

  def testCopyProtoMessage(self):
    msg = SimpleMessage(field='abc')
    new_msg = encoding.CopyProtoMessage(msg)
    self.assertEqual(msg.field, new_msg.field)
    msg.field = 'def'
    self.assertNotEqual(msg.field, new_msg.field)

  def testBytesEncoding(self):
    b64_str = 'AAc+'
    b64_msg = '{"field": "%s"}' % b64_str
    urlsafe_b64_str = 'AAc-'
    urlsafe_b64_msg = '{"field": "%s"}' % urlsafe_b64_str
    data = base64.b64decode(b64_str)
    msg = BytesMessage(field=data)
    self.assertEqual(msg, encoding.JsonToMessage(BytesMessage, urlsafe_b64_msg))
    self.assertEqual(msg, encoding.JsonToMessage(BytesMessage, b64_msg))
    self.assertEqual(urlsafe_b64_msg, encoding.MessageToJson(msg))

    enc_rep_msg = '{"repfield": ["%(b)s", "%(b)s"]}' % {
        'b': urlsafe_b64_str,
    }
    rep_msg = BytesMessage(repfield=[data, data])
    self.assertEqual(rep_msg, encoding.JsonToMessage(BytesMessage, enc_rep_msg))
    self.assertEqual(enc_rep_msg, encoding.MessageToJson(rep_msg))

  def testIncludeFields(self):
    msg = SimpleMessage()
    self.assertEqual('{}', encoding.MessageToJson(msg))
    self.assertEqual(
        '{"field": null}',
        encoding.MessageToJson(msg, include_fields=['field']))
    self.assertEqual(
        '{"repfield": []}',
        encoding.MessageToJson(msg, include_fields=['repfield']))

  def testNestedIncludeFields(self):
    msg = HasNestedMessage(
        nested=AdditionalPropertiesMessage(
            additional_properties=[]))
    self.assertEqual(
        '{"nested": null}',
        encoding.MessageToJson(msg, include_fields=['nested']))
    self.assertEqual(
        '{"nested": {"additional_properties": []}}',
        encoding.MessageToJson(
            msg, include_fields=['nested.additional_properties']))
    msg = ExtraNestedMessage(nested=msg)
    self.assertEqual(
        '{"nested": {"nested": null}}',
        encoding.MessageToJson(msg, include_fields=['nested.nested']))
    self.assertEqual(
        '{"nested": {"nested_list": []}}',
        encoding.MessageToJson(msg, include_fields=['nested.nested_list']))
    self.assertEqual(
        '{"nested": {"nested": {"additional_properties": []}}}',
        encoding.MessageToJson(
            msg, include_fields=['nested.nested.additional_properties']))

  def testAdditionalPropertyMapping(self):
    msg = AdditionalPropertiesMessage()
    msg.additional_properties = [
        AdditionalPropertiesMessage.AdditionalProperty(
            key='key_one', value='value_one'),
        AdditionalPropertiesMessage.AdditionalProperty(
            key='key_two', value='value_two'),
    ]

    encoded_msg = encoding.MessageToJson(msg)
    self.assertEqual(
        {'key_one': 'value_one', 'key_two': 'value_two'},
        json.loads(encoded_msg))

    new_msg = encoding.JsonToMessage(type(msg), encoded_msg)
    self.assertEqual(
        set(('key_one', 'key_two')),
        set([x.key for x in new_msg.additional_properties]))
    self.assertIsNot(msg, new_msg)

    new_msg.additional_properties.pop()
    self.assertEqual(1, len(new_msg.additional_properties))
    self.assertEqual(2, len(msg.additional_properties))

  def testAdditionalMessageProperties(self):
    json_msg = '{"input": {"index": 0, "name": "output"}}'
    result = encoding.JsonToMessage(
        AdditionalMessagePropertiesMessage, json_msg)
    self.assertEqual(1, len(result.additional_properties))
    self.assertEqual(0, result.additional_properties[0].value.index)

  def testNestedFieldMapping(self):
    nested_msg = AdditionalPropertiesMessage()
    nested_msg.additional_properties = [
        AdditionalPropertiesMessage.AdditionalProperty(
            key='key_one', value='value_one'),
        AdditionalPropertiesMessage.AdditionalProperty(
            key='key_two', value='value_two'),
    ]
    msg = HasNestedMessage(nested=nested_msg)

    encoded_msg = encoding.MessageToJson(msg)
    self.assertEqual(
        {'nested': {'key_one': 'value_one', 'key_two': 'value_two'}},
        json.loads(encoded_msg))

    new_msg = encoding.JsonToMessage(type(msg), encoded_msg)
    self.assertEqual(
        set(('key_one', 'key_two')),
        set([x.key for x in new_msg.nested.additional_properties]))

    new_msg.nested.additional_properties.pop()
    self.assertEqual(1, len(new_msg.nested.additional_properties))
    self.assertEqual(2, len(msg.nested.additional_properties))

  def testValidEnums(self):
    message_json = '{"field_one": "VALUE_ONE"}'
    message = encoding.JsonToMessage(MessageWithEnum, message_json)
    self.assertEqual(MessageWithEnum.ThisEnum.VALUE_ONE, message.field_one)
    self.assertEqual(MessageWithEnum.ThisEnum.VALUE_TWO, message.field_two)
    self.assertEqual(json.loads(message_json),
                     json.loads(encoding.MessageToJson(message)))

  def testIgnoredEnums(self):
    json_with_typo = '{"field_one": "VALUE_OEN"}'
    message = encoding.JsonToMessage(MessageWithEnum, json_with_typo)
    self.assertEqual(None, message.field_one)
    self.assertEqual(('VALUE_OEN', messages.Variant.ENUM),
                     message.get_unrecognized_field_info('field_one'))
    self.assertEqual(json.loads(json_with_typo),
                     json.loads(encoding.MessageToJson(message)))

    empty_json = ''
    message = encoding.JsonToMessage(MessageWithEnum, empty_json)
    self.assertEqual(None, message.field_one)

  def testIgnoredEnumsWithDefaults(self):
    json_with_typo = '{"field_two": "VALUE_OEN"}'
    message = encoding.JsonToMessage(MessageWithEnum, json_with_typo)
    self.assertEqual(MessageWithEnum.ThisEnum.VALUE_TWO, message.field_two)
    self.assertEqual(json.loads(json_with_typo),
                     json.loads(encoding.MessageToJson(message)))

  def testUnknownNestedRoundtrip(self):
    json_message = '{"field": "abc", "submessage": {"a": 1, "b": "foo"}}'
    message = encoding.JsonToMessage(SimpleMessage, json_message)
    self.assertEqual(json.loads(json_message),
                     json.loads(encoding.MessageToJson(message)))

  def testJsonDatetime(self):
    msg = TimeMessage(timefield=datetime.datetime(
        2014, 7, 2, 23, 33, 25, 541000,
        tzinfo=util.TimeZoneOffset(datetime.timedelta(0))))
    self.assertEqual(
        '{"timefield": "2014-07-02T23:33:25.541000+00:00"}',
        encoding.MessageToJson(msg))

  def testMessageToRepr(self):
    # pylint:disable=bad-whitespace, Using the same string returned by
    # MessageToRepr, with the module names fixed.
    msg = SimpleMessage(field='field',repfield=['field','field',],)
    self.assertEqual(
        encoding.MessageToRepr(msg),
        r"%s.SimpleMessage(field='field',repfield=['field','field',],)" % (
            __name__,))
    self.assertEqual(
        encoding.MessageToRepr(msg, no_modules=True),
        r"SimpleMessage(field='field',repfield=['field','field',],)")

  def testMessageToReprWithTime(self):
    msg = TimeMessage(timefield=datetime.datetime(
        2014, 7, 2, 23, 33, 25, 541000,
        tzinfo=util.TimeZoneOffset(datetime.timedelta(0))))
    self.assertEqual(
        encoding.MessageToRepr(msg, multiline=True),
        # pylint:disable=line-too-long, Too much effort to make MessageToRepr
        # wrap lines properly.
        """\
%s.TimeMessage(
    timefield=datetime.datetime(2014, 7, 2, 23, 33, 25, 541000, tzinfo=protorpc.util.TimeZoneOffset(datetime.timedelta(0))),
)""" % __name__)
    self.assertEqual(
        encoding.MessageToRepr(msg, multiline=True, no_modules=True),
        # pylint:disable=line-too-long, Too much effort to make MessageToRepr
        # wrap lines properly.
        """\
TimeMessage(
    timefield=datetime.datetime(2014, 7, 2, 23, 33, 25, 541000, tzinfo=TimeZoneOffset(datetime.timedelta(0))),
)""")


if __name__ == '__main__':
  unittest2.main()
