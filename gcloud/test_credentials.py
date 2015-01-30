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

import unittest2


class TestCredentials(unittest2.TestCase):

    def test_get_for_service_account_p12_wo_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = b'SEEkR1t'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = credentials.get_for_service_account_p12(
                    CLIENT_EMAIL, file_obj.name)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': None,
        }
        self.assertEqual(client._called_with, expected_called_with)

    def test_get_for_service_account_p12_w_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = b'SEEkR1t'
        SCOPE = 'SCOPE'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = credentials.get_for_service_account_p12(
                    CLIENT_EMAIL, file_obj.name, SCOPE)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)


class Test_generate_signed_url(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.credentials import generate_signed_url
        return generate_signed_url(*args, **kwargs)

    def test_w_expiration_int(self):
        import base64
        from six.moves.urllib.parse import parse_qs
        from six.moves.urllib.parse import urlsplit
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        ENDPOINT = 'http://api.example.com'
        RESOURCE = '/name/path'
        SIGNED = base64.b64encode(b'DEADBEEF')
        CREDENTIALS = _Credentials()

        def _get_signed_query_params(*args):
            credentials, expiration = args[:2]
            return {
                'GoogleAccessId': credentials.service_account_name,
                'Expires': str(expiration),
                'Signature': SIGNED,
            }

        with _Monkey(MUT, _get_signed_query_params=_get_signed_query_params):
            url = self._callFUT(CREDENTIALS, RESOURCE, 1000,
                                api_access_endpoint=ENDPOINT)

        scheme, netloc, path, qs, frag = urlsplit(url)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'api.example.com')
        self.assertEqual(path, RESOURCE)
        params = parse_qs(qs)
        self.assertEqual(len(params), 3)
        # In Py3k, parse_qs gives us text values:
        self.assertEqual(params['Signature'], [SIGNED.decode('ascii')])
        self.assertEqual(params['Expires'], ['1000'])
        self.assertEqual(params['GoogleAccessId'],
                         [_Credentials.service_account_name])
        self.assertEqual(frag, '')


class Test__get_signed_query_params(unittest2.TestCase):

    def _callFUT(self, credentials, expiration, signature_string):
        from gcloud.credentials import _get_signed_query_params
        return _get_signed_query_params(credentials, expiration,
                                        signature_string)

    def test_wrong_type(self):
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        pkcs_v1_5 = _PKCS1_v1_5()
        rsa = _RSA()
        sha256 = _SHA256()

        def _get_pem_key(credentials):
            return credentials

        BAD_CREDENTIALS = None
        EXPIRATION = '100'
        SIGNATURE_STRING = 'dummy_signature'
        with _Monkey(MUT, RSA=rsa, PKCS1_v1_5=pkcs_v1_5,
                     SHA256=sha256, _get_pem_key=_get_pem_key):
            self.assertRaises(NameError, self._callFUT,
                              BAD_CREDENTIALS, EXPIRATION, SIGNATURE_STRING)

    def _run_test_with_credentials(self, credentials, account_name):
        import base64
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        crypt = _Crypt()
        pkcs_v1_5 = _PKCS1_v1_5()
        rsa = _RSA()
        sha256 = _SHA256()

        EXPIRATION = '100'
        SIGNATURE_STRING = b'dummy_signature'
        with _Monkey(MUT, crypt=crypt, RSA=rsa, PKCS1_v1_5=pkcs_v1_5,
                     SHA256=sha256):
            result = self._callFUT(credentials, EXPIRATION, SIGNATURE_STRING)

        if crypt._pkcs12_key_as_pem_called:
            self.assertEqual(crypt._private_key_text,
                             base64.b64encode(b'dummy_private_key_text'))
            self.assertEqual(crypt._private_key_password, 'notasecret')
        self.assertEqual(sha256._signature_string, SIGNATURE_STRING)
        SIGNED = base64.b64encode(b'DEADBEEF')
        expected_query = {
            'Expires': EXPIRATION,
            'GoogleAccessId': account_name,
            'Signature': SIGNED,
        }
        self.assertEqual(result, expected_query)

    def test_signed_jwt_for_p12(self):
        from oauth2client import client

        scopes = []
        ACCOUNT_NAME = 'dummy_service_account_name'
        credentials = client.SignedJwtAssertionCredentials(
            ACCOUNT_NAME, b'dummy_private_key_text', scopes)
        self._run_test_with_credentials(credentials, ACCOUNT_NAME)

    def test_service_account_via_json_key(self):
        from oauth2client import service_account
        from gcloud._testing import _Monkey

        scopes = []

        PRIVATE_TEXT = 'dummy_private_key_pkcs8_text'

        def _get_private_key(private_key_pkcs8_text):
            return private_key_pkcs8_text

        ACCOUNT_NAME = 'dummy_service_account_email'
        with _Monkey(service_account, _get_private_key=_get_private_key):
            credentials = service_account._ServiceAccountCredentials(
                'dummy_service_account_id', ACCOUNT_NAME,
                'dummy_private_key_id', PRIVATE_TEXT, scopes)

        self._run_test_with_credentials(credentials, ACCOUNT_NAME)


class Test__get_pem_key(unittest2.TestCase):

    def _callFUT(self, credentials):
        from gcloud.credentials import _get_pem_key
        return _get_pem_key(credentials)

    def test_bad_argument(self):
        self.assertRaises(TypeError, self._callFUT, None)

    def test_signed_jwt_for_p12(self):
        import base64
        from oauth2client import client
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        scopes = []
        PRIVATE_KEY = b'dummy_private_key_text'
        credentials = client.SignedJwtAssertionCredentials(
            'dummy_service_account_name', PRIVATE_KEY, scopes)
        crypt = _Crypt()
        rsa = _RSA()
        with _Monkey(MUT, crypt=crypt, RSA=rsa):
            result = self._callFUT(credentials)

        self.assertEqual(crypt._private_key_text,
                         base64.b64encode(PRIVATE_KEY))
        self.assertEqual(crypt._private_key_password, 'notasecret')
        self.assertEqual(result, 'imported:__PEM__')

    def test_service_account_via_json_key(self):
        from oauth2client import service_account
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        scopes = []

        PRIVATE_TEXT = 'dummy_private_key_pkcs8_text'

        def _get_private_key(private_key_pkcs8_text):
            return private_key_pkcs8_text

        with _Monkey(service_account, _get_private_key=_get_private_key):
            credentials = service_account._ServiceAccountCredentials(
                'dummy_service_account_id', 'dummy_service_account_email',
                'dummy_private_key_id', PRIVATE_TEXT, scopes)

        rsa = _RSA()
        with _Monkey(MUT, RSA=rsa):
            result = self._callFUT(credentials)

        expected = 'imported:%s' % (PRIVATE_TEXT,)
        self.assertEqual(result, expected)


class Test__get_expiration_seconds(unittest2.TestCase):

    def _callFUT(self, expiration):
        from gcloud.credentials import _get_expiration_seconds
        return _get_expiration_seconds(expiration)

    def _utc_seconds(self, when):
        import calendar
        return int(calendar.timegm(when.timetuple()))

    def test_w_invalid(self):
        self.assertRaises(TypeError, self._callFUT, object())
        self.assertRaises(TypeError, self._callFUT, None)

    def test_w_int(self):
        self.assertEqual(self._callFUT(123), 123)

    def test_w_long(self):
        try:
            long
        except NameError:  # pragma: NO COVER Py3K
            pass
        else:
            self.assertEqual(self._callFUT(long(123)), 123)

    def test_w_naive_datetime(self):
        import datetime

        expiration_no_tz = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(expiration_no_tz)
        self.assertEqual(self._callFUT(expiration_no_tz), utc_seconds)

    def test_w_utc_datetime(self):
        import datetime
        import pytz

        expiration_utc = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, pytz.utc)
        utc_seconds = self._utc_seconds(expiration_utc)
        self.assertEqual(self._callFUT(expiration_utc), utc_seconds)

    def test_w_other_zone_datetime(self):
        import datetime
        import pytz

        zone = pytz.timezone('CET')
        expiration_other = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, zone)
        utc_seconds = self._utc_seconds(expiration_other)
        cet_seconds = utc_seconds - (60 * 60)  # CET one hour earlier than UTC
        self.assertEqual(self._callFUT(expiration_other), cet_seconds)

    def test_w_timedelta_seconds(self):
        import datetime
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(seconds=10)

        with _Monkey(MUT, _utcnow=lambda: dummy_utcnow):
            result = self._callFUT(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 10)

    def test_w_timedelta_days(self):
        import datetime
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(days=1)

        with _Monkey(MUT, _utcnow=lambda: dummy_utcnow):
            result = self._callFUT(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 86400)


class _Credentials(object):

    service_account_name = 'testing@example.com'

    def create_scoped(self, scopes):
        self._scopes = scopes
        return self


class _Client(object):
    def __init__(self):
        self._signed = _Credentials()

        class GoogleCredentials(object):
            @staticmethod
            def get_application_default():
                self._get_app_default_called = True
                return self._signed

        self.GoogleCredentials = GoogleCredentials

    def SignedJwtAssertionCredentials(self, **kw):
        self._called_with = kw
        return self._signed


class _Crypt(object):

    _pkcs12_key_as_pem_called = False

    def pkcs12_key_as_pem(self, private_key_text, private_key_password):
        self._pkcs12_key_as_pem_called = True
        self._private_key_text = private_key_text
        self._private_key_password = private_key_password
        return '__PEM__'


class _RSA(object):

    _imported = None

    def importKey(self, pem):
        self._imported = pem
        return 'imported:%s' % pem


class _PKCS1_v1_5(object):

    _pem_key = _signature_hash = None

    def new(self, pem_key):
        self._pem_key = pem_key
        return self

    def sign(self, signature_hash):
        self._signature_hash = signature_hash
        return b'DEADBEEF'


class _SHA256(object):

    _signature_string = None

    def new(self, signature_string):
        self._signature_string = signature_string
        return self
