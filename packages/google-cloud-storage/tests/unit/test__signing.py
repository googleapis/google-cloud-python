# Copyright 2017 Google LLC
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

import base64
import calendar
import datetime
import time
import unittest

import mock
import six
from six.moves import urllib_parse


class Test_get_expiration_seconds(unittest.TestCase):
    @staticmethod
    def _call_fut(expiration):
        from google.cloud.storage._signing import get_expiration_seconds

        return get_expiration_seconds(expiration)

    @staticmethod
    def _utc_seconds(when):
        return int(calendar.timegm(when.timetuple()))

    def test_w_invalid(self):
        self.assertRaises(TypeError, self._call_fut, object())
        self.assertRaises(TypeError, self._call_fut, None)

    def test_w_int(self):
        self.assertEqual(self._call_fut(123), 123)

    def test_w_long(self):
        if six.PY3:
            raise unittest.SkipTest("No long on Python 3")

        self.assertEqual(self._call_fut(long(123)), 123)  # noqa: F821

    def test_w_naive_datetime(self):
        expiration_no_tz = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(expiration_no_tz)
        self.assertEqual(self._call_fut(expiration_no_tz), utc_seconds)

    def test_w_utc_datetime(self):
        from google.cloud._helpers import UTC

        expiration_utc = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, UTC)
        utc_seconds = self._utc_seconds(expiration_utc)
        self.assertEqual(self._call_fut(expiration_utc), utc_seconds)

    def test_w_other_zone_datetime(self):
        from google.cloud._helpers import _UTC

        class CET(_UTC):
            _tzname = "CET"
            _utcoffset = datetime.timedelta(hours=1)

        zone = CET()
        expiration_other = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, zone)
        utc_seconds = self._utc_seconds(expiration_other)
        cet_seconds = utc_seconds - (60 * 60)  # CET one hour earlier than UTC
        self.assertEqual(self._call_fut(expiration_other), cet_seconds)

    def test_w_timedelta_seconds(self):
        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(seconds=10)

        patch = mock.patch(
            "google.cloud.storage._signing.NOW", return_value=dummy_utcnow
        )
        with patch as utcnow:
            result = self._call_fut(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 10)
        utcnow.assert_called_once_with()

    def test_w_timedelta_days(self):
        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(days=1)

        patch = mock.patch(
            "google.cloud.storage._signing.NOW", return_value=dummy_utcnow
        )
        with patch as utcnow:
            result = self._call_fut(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 86400)
        utcnow.assert_called_once_with()


class Test_get_signed_query_params(unittest.TestCase):
    @staticmethod
    def _call_fut(credentials, expiration, string_to_sign):
        from google.cloud.storage._signing import get_signed_query_params

        return get_signed_query_params(credentials, expiration, string_to_sign)

    def test_it(self):
        sig_bytes = b"DEADBEEF"
        account_name = mock.sentinel.service_account_email
        credentials = _make_credentials(signing=True, signer_email=account_name)
        credentials.sign_bytes.return_value = sig_bytes
        expiration = 100
        string_to_sign = "dummy_signature"
        result = self._call_fut(credentials, expiration, string_to_sign)

        expected = {
            "GoogleAccessId": account_name,
            "Expires": str(expiration),
            "Signature": base64.b64encode(sig_bytes),
        }
        self.assertEqual(result, expected)
        credentials.sign_bytes.assert_called_once_with(string_to_sign)


class Test_generate_signed_url(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.storage._signing import generate_signed_url

        return generate_signed_url(*args, **kwargs)

    def _generate_helper(
        self, response_type=None, response_disposition=None, generation=None
    ):
        endpoint = "http://api.example.com"
        resource = "/name/path"
        credentials = _make_credentials(
            signing=True, signer_email="service@example.com"
        )
        credentials.sign_bytes.return_value = b"DEADBEEF"
        signed = base64.b64encode(credentials.sign_bytes.return_value)
        signed = signed.decode("ascii")

        expiration = 1000
        url = self._call_fut(
            credentials,
            resource,
            expiration,
            api_access_endpoint=endpoint,
            response_type=response_type,
            response_disposition=response_disposition,
            generation=generation,
        )

        # Check the mock was called.
        string_to_sign = "\n".join(["GET", "", "", str(expiration), resource])
        credentials.sign_bytes.assert_called_once_with(string_to_sign)

        scheme, netloc, path, qs, frag = urllib_parse.urlsplit(url)
        self.assertEqual(scheme, "http")
        self.assertEqual(netloc, "api.example.com")
        self.assertEqual(path, resource)
        self.assertEqual(frag, "")

        # Check the URL parameters.
        params = urllib_parse.parse_qs(qs)
        expected_params = {
            "GoogleAccessId": [credentials.signer_email],
            "Expires": [str(expiration)],
            "Signature": [signed],
        }
        if response_type is not None:
            expected_params["response-content-type"] = [response_type]
        if response_disposition is not None:
            expected_params["response-content-disposition"] = [response_disposition]
        if generation is not None:
            expected_params["generation"] = [generation]
        self.assertEqual(params, expected_params)

    def test_w_expiration_int(self):
        self._generate_helper()

    def test_w_custom_fields(self):
        response_type = "text/plain"
        response_disposition = "attachment; filename=blob.png"
        generation = "123"
        self._generate_helper(
            response_type=response_type,
            response_disposition=response_disposition,
            generation=generation,
        )

    def test_with_google_credentials(self):
        resource = "/name/path"
        credentials = _make_credentials()
        expiration = int(time.time() + 5)
        self.assertRaises(
            AttributeError,
            self._call_fut,
            credentials,
            resource=resource,
            expiration=expiration,
        )


def _make_credentials(signing=False, signer_email=None):
    import google.auth.credentials

    if signing:
        credentials = mock.Mock(spec=google.auth.credentials.Signing)
        credentials.signer_email = signer_email
        return credentials
    else:
        return mock.Mock(spec=google.auth.credentials.Credentials)
