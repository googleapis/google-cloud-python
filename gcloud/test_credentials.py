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


class Test_get_credentials(unittest2.TestCase):

    def _callFUT(self):
        from gcloud import credentials
        return credentials.get_credentials()

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        client = _Client()
        with _Monkey(MUT, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, _Credentials))
        self.assertTrue(found is client._signed)
        self.assertTrue(client._get_app_default_called)


class Test_generate_signed_url(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.credentials import generate_signed_url
        return generate_signed_url(*args, **kwargs)

    def _generate_helper(self, response_type=None, response_disposition=None,
                         generation=None):
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
                'GoogleAccessId': credentials.service_account_email,
                'Expires': str(expiration),
                'Signature': SIGNED,
            }

        with _Monkey(MUT, _get_signed_query_params=_get_signed_query_params):
            url = self._callFUT(CREDENTIALS, RESOURCE, 1000,
                                api_access_endpoint=ENDPOINT,
                                response_type=response_type,
                                response_disposition=response_disposition,
                                generation=generation)

        scheme, netloc, path, qs, frag = urlsplit(url)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'api.example.com')
        self.assertEqual(path, RESOURCE)
        params = parse_qs(qs)
        # In Py3k, parse_qs gives us text values:
        self.assertEqual(params.pop('Signature'), [SIGNED.decode('ascii')])
        self.assertEqual(params.pop('Expires'), ['1000'])
        self.assertEqual(params.pop('GoogleAccessId'),
                         [CREDENTIALS.service_account_email])
        if response_type is not None:
            self.assertEqual(params.pop('response-content-type'),
                             [response_type])
        if response_disposition is not None:
            self.assertEqual(params.pop('response-content-disposition'),
                             [response_disposition])
        if generation is not None:
            self.assertEqual(params.pop('generation'), [generation])
        # Make sure we have checked them all.
        self.assertEqual(len(params), 0)
        self.assertEqual(frag, '')

    def test_w_expiration_int(self):
        self._generate_helper()

    def test_w_custom_fields(self):
        response_type = 'text/plain'
        response_disposition = 'attachment; filename=blob.png'
        generation = '123'
        self._generate_helper(response_type=response_type,
                              response_disposition=response_disposition,
                              generation=generation)


class Test_generate_signed_url_exception(unittest2.TestCase):
    def test_with_google_credentials(self):
        import time
        from gcloud.credentials import generate_signed_url
        RESOURCE = '/name/path'

        credentials = _GoogleCredentials()
        expiration = int(time.time() + 5)
        self.assertRaises(AttributeError, generate_signed_url, credentials,
                          resource=RESOURCE, expiration=expiration)


class Test__get_signed_query_params(unittest2.TestCase):

    def _callFUT(self, credentials, expiration, string_to_sign):
        from gcloud.credentials import _get_signed_query_params
        return _get_signed_query_params(credentials, expiration,
                                        string_to_sign)

    def test_it(self):
        import base64

        SIG_BYTES = b'DEADBEEF'
        ACCOUNT_NAME = object()
        CREDENTIALS = _Credentials(sign_result=SIG_BYTES,
                                   service_account_email=ACCOUNT_NAME)
        EXPIRATION = 100
        STRING_TO_SIGN = 'dummy_signature'
        result = self._callFUT(CREDENTIALS, EXPIRATION,
                               STRING_TO_SIGN)

        self.assertEqual(result, {
            'GoogleAccessId': ACCOUNT_NAME,
            'Expires': str(EXPIRATION),
            'Signature': base64.b64encode(b'DEADBEEF'),
        })
        self.assertEqual(CREDENTIALS._signed, [STRING_TO_SIGN])


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
        from gcloud._helpers import UTC

        expiration_utc = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, UTC)
        utc_seconds = self._utc_seconds(expiration_utc)
        self.assertEqual(self._callFUT(expiration_utc), utc_seconds)

    def test_w_other_zone_datetime(self):
        import datetime
        from gcloud._helpers import _UTC

        class CET(_UTC):
            _tzname = 'CET'
            _utcoffset = datetime.timedelta(hours=1)

        zone = CET()
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

        with _Monkey(MUT, _NOW=lambda: dummy_utcnow):
            result = self._callFUT(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 10)

    def test_w_timedelta_days(self):
        import datetime
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(days=1)

        with _Monkey(MUT, _NOW=lambda: dummy_utcnow):
            result = self._callFUT(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 86400)


class _Credentials(object):

    def __init__(self, service_account_email='testing@example.com',
                 sign_result=''):
        self.service_account_email = service_account_email
        self._sign_result = sign_result
        self._signed = []

    def sign_blob(self, bytes_to_sign):
        self._signed.append(bytes_to_sign)
        return None, self._sign_result


class _GoogleCredentials(object):

    def __init__(self, service_account_email='testing@example.com'):
        self.service_account_email = service_account_email


class _Client(object):

    def __init__(self):
        self._signed = _Credentials()

        class GoogleCredentials(object):
            @staticmethod
            def get_application_default():
                self._get_app_default_called = True
                return self._signed

        self.GoogleCredentials = GoogleCredentials
