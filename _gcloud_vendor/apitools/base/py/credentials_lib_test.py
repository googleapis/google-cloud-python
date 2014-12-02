#!/usr/bin/env python


import httplib
import re
import StringIO
import urllib2

import mock
import unittest2

from apitools.base.py import credentials_lib
from apitools.base.py import util


def CreateUriValidator(uri_regexp, content=''):
  def CheckUri(uri, headers=None):
    if 'X-Google-Metadata-Request' not in headers:
      raise ValueError('Missing required header')
    if uri_regexp.match(uri):
      message = content
      status = httplib.OK
    else:
      message = 'Expected uri matching pattern %s' % uri_regexp.pattern
      status = httplib.BAD_REQUEST
    return type('HttpResponse', (object,), {'status': status})(), message
  return CheckUri


class CredentialsLibTest(unittest2.TestCase):

  def _GetServiceCreds(self, service_account_name=None, scopes=None):
    scopes = scopes or ['scope1']
    kwargs = {}
    if service_account_name is not None:
      kwargs['service_account_name'] = service_account_name
    service_account_name = service_account_name or 'default'
    with mock.patch.object(urllib2, 'urlopen', autospec=True) as urllib_mock:
      urllib_mock.return_value = StringIO.StringIO(''.join(scopes))
      with mock.patch.object(util, 'DetectGce', autospec=True) as mock_util:
        mock_util.return_value = True
        validator = CreateUriValidator(
            re.compile(r'.*/%s/.*' % service_account_name),
            content='{"access_token": "token"}')
        credentials = credentials_lib.GceAssertionCredentials(scopes, **kwargs)
        self.assertIsNone(credentials._refresh(validator))

  def testGceServiceAccounts(self):
    self._GetServiceCreds()
    self._GetServiceCreds(service_account_name='my_service_account')


if __name__ == '__main__':
  unittest2.main()
