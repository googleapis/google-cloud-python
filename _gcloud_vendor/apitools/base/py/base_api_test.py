#!/usr/bin/env python


import datetime
import sys
import urllib

from protorpc import message_types
from protorpc import messages

import unittest2

from apitools.base.py import base_api
from apitools.base.py import http_wrapper


class SimpleMessage(messages.Message):
  field = messages.StringField(1)


class MessageWithTime(messages.Message):
  timestamp = message_types.DateTimeField(1)


class StandardQueryParameters(messages.Message):
  field = messages.StringField(1)


class FakeCredentials(object):

  def authorize(self, _):  # pylint: disable=invalid-name
    return None


class FakeClient(base_api.BaseApiClient):
  MESSAGES_MODULE = sys.modules[__name__]
  _PACKAGE = 'package'
  _SCOPES = ['scope1']
  _CLIENT_ID = 'client_id'
  _CLIENT_SECRET = 'client_secret'


class FakeService(base_api.BaseApiService):

  def __init__(self, client=None):
    client = client or FakeClient(
        'http://www.example.com/', credentials=FakeCredentials())
    super(FakeService, self).__init__(client)


class BaseApiTest(unittest2.TestCase):

  def __GetFakeClient(self):
    return FakeClient('', credentials=FakeCredentials())

  def testUrlNormalization(self):
    client = FakeClient('http://www.googleapis.com', get_credentials=False)
    self.assertTrue(client.url.endswith('/'))

  def testNoCredentials(self):
    client = FakeClient('', get_credentials=False)
    self.assertIsNotNone(client)
    self.assertIsNone(client._credentials)

  def testIncludeEmptyFieldsClient(self):
    msg = SimpleMessage()
    client = self.__GetFakeClient()
    self.assertEqual('{}', client.SerializeMessage(msg))
    with client.IncludeFields(('field',)):
      self.assertEqual('{"field": null}', client.SerializeMessage(msg))

  def testJsonResponse(self):
    method_config = base_api.ApiMethodInfo(response_type_name='SimpleMessage')
    service = FakeService()
    http_response = http_wrapper.Response(
        info={'status': '200'}, content='{"field": "abc"}',
        request_url='http://www.google.com')
    response_message = SimpleMessage(field='abc')
    self.assertEqual(response_message, service.ProcessHttpResponse(
        method_config, http_response))
    with service.client.JsonResponseModel():
      self.assertEqual(http_response.content, service.ProcessHttpResponse(
          method_config, http_response))

  def testAdditionalHeaders(self):
    additional_headers = {'Request-Is-Awesome': '1'}
    client = self.__GetFakeClient()

    # No headers to start
    http_request = http_wrapper.Request('http://www.example.com')
    new_request = client.ProcessHttpRequest(http_request)
    self.assertFalse('Request-Is-Awesome' in new_request.headers)

    # Add a new header and ensure it's added to the request.
    client.additional_http_headers = additional_headers
    http_request = http_wrapper.Request('http://www.example.com')
    new_request = client.ProcessHttpRequest(http_request)
    self.assertTrue('Request-Is-Awesome' in new_request.headers)

  def testQueryEncoding(self):
    method_config = base_api.ApiMethodInfo(
        request_type_name='MessageWithTime', query_params=['timestamp'])
    service = FakeService()
    request = MessageWithTime(
        timestamp=datetime.datetime(2014, 10, 07, 12, 53, 13))
    http_request = service.PrepareHttpRequest(method_config, request)

    url_timestamp = urllib.quote(request.timestamp.isoformat())
    self.assertTrue(http_request.url.endswith(url_timestamp))


if __name__ == '__main__':
  unittest2.main()
