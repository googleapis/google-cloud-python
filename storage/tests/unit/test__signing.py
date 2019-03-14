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
import binascii
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
        credentials = _make_credentials(signer_email=account_name)
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


class Test_get_canonical_headers(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.storage._signing import get_canonical_headers

        return get_canonical_headers(*args, **kwargs)

    def test_w_none(self):
        headers = None
        expected = []
        self.assertEqual(self._call_fut(headers), expected)

    def test_w_dict(self):
        headers = {"foo": "Foo 1.2.3", "Bar": " baz,bam,qux   "}
        expected = ["bar:baz,bam,qux", "foo:Foo 1.2.3"]
        self.assertEqual(self._call_fut(headers), expected)

    def test_w_list_and_multiples(self):
        headers = [
            ("foo", "Foo 1.2.3"),
            ("Bar", " baz"),
            ("Bar", "bam"),
            ("Bar", "qux   "),
        ]
        expected = ["bar:baz,bam,qux", "foo:Foo 1.2.3"]
        self.assertEqual(self._call_fut(headers), expected)

    # TODO:  handle folded line values?


class Test_canonicalize(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.storage._signing import canonicalize

        return canonicalize(*args, **kwargs)

    def test_wo_headers_or_query_parameters(self):
        method = "GET"
        resource = "/bucket/blob"
        canonical = self._call_fut(method, resource, None, None)
        self.assertEqual(canonical.method, method)
        self.assertEqual(canonical.resource, resource)
        self.assertEqual(canonical.query_parameters, [])
        self.assertEqual(canonical.headers, [])

    def test_w_headers_and_resumable(self):
        method = "RESUMABLE"
        resource = "/bucket/blob"
        headers = [("x-goog-extension", "foobar")]
        canonical = self._call_fut(method, resource, None, headers)
        self.assertEqual(canonical.method, "POST")
        self.assertEqual(canonical.resource, resource)
        self.assertEqual(canonical.query_parameters, [])
        self.assertEqual(
            canonical.headers, ["x-goog-extension:foobar", "x-goog-resumable:start"]
        )

    def test_w_query_paramters(self):
        method = "GET"
        resource = "/bucket/blob"
        query_parameters = {"foo": "bar", "baz": "qux"}
        canonical = self._call_fut(method, resource, query_parameters, None)
        self.assertEqual(canonical.method, method)
        self.assertEqual(canonical.resource, "{}?baz=qux&foo=bar".format(resource))
        self.assertEqual(canonical.query_parameters, [("baz", "qux"), ("foo", "bar")])
        self.assertEqual(canonical.headers, [])


class Test_generate_signed_url_v2(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.storage._signing import generate_signed_url_v2

        return generate_signed_url_v2(*args, **kwargs)

    def _generate_helper(
        self,
        api_access_endpoint="",
        method="GET",
        content_md5=None,
        content_type=None,
        response_type=None,
        response_disposition=None,
        generation=None,
        headers=None,
        query_parameters=None,
    ):
        from six.moves.urllib.parse import urlencode

        resource = "/name/path"
        credentials = _make_credentials(signer_email="service@example.com")
        credentials.sign_bytes.return_value = b"DEADBEEF"
        signed = base64.b64encode(credentials.sign_bytes.return_value)
        signed = signed.decode("ascii")

        expiration = 1000
        url = self._call_fut(
            credentials,
            resource,
            expiration,
            api_access_endpoint=api_access_endpoint,
            method=method,
            content_md5=content_md5,
            content_type=content_type,
            response_type=response_type,
            response_disposition=response_disposition,
            generation=generation,
            headers=headers,
            query_parameters=query_parameters,
        )

        # Check the mock was called.
        method = method.upper()

        if headers is None:
            headers = []
        elif isinstance(headers, dict):
            headers = sorted(headers.items())

        elements = []
        expected_resource = resource
        if method == "RESUMABLE":
            elements.append("POST")
            headers.append(("x-goog-resumable", "start"))
        else:
            elements.append(method)

        if query_parameters is not None:
            normalized_qp = {
                key.lower(): value and value.strip() or ""
                for key, value in query_parameters.items()
            }
            expected_qp = urlencode(sorted(normalized_qp.items()))
            expected_resource = "{}?{}".format(resource, expected_qp)

        elements.append(content_md5 or "")
        elements.append(content_type or "")
        elements.append(str(expiration))
        elements.extend(["{}:{}".format(*header) for header in headers])
        elements.append(expected_resource)

        string_to_sign = "\n".join(elements)

        credentials.sign_bytes.assert_called_once_with(string_to_sign)

        scheme, netloc, path, qs, frag = urllib_parse.urlsplit(url)
        expected_scheme, expected_netloc, _, _, _ = urllib_parse.urlsplit(
            api_access_endpoint
        )
        self.assertEqual(scheme, expected_scheme)
        self.assertEqual(netloc, expected_netloc)
        self.assertEqual(path, resource)
        self.assertEqual(frag, "")

        # Check the URL parameters.
        params = dict(urllib_parse.parse_qsl(qs, keep_blank_values=True))

        self.assertEqual(params["GoogleAccessId"], credentials.signer_email)
        self.assertEqual(params["Expires"], str(expiration))
        self.assertEqual(params["Signature"], signed)

        if response_type is not None:
            self.assertEqual(params["response-content-type"], response_type)

        if response_disposition is not None:
            self.assertEqual(
                params["response-content-disposition"], response_disposition
            )

        if generation is not None:
            self.assertEqual(params["generation"], str(generation))

        if query_parameters is not None:
            for key, value in query_parameters.items():
                value = value.strip() if value else ""
                self.assertEqual(params[key].lower(), value)

    def test_w_expiration_int(self):
        self._generate_helper()

    def test_w_endpoint(self):
        api_access_endpoint = "https://api.example.com"
        self._generate_helper(api_access_endpoint=api_access_endpoint)

    def test_w_method(self):
        method = "POST"
        self._generate_helper(method=method)

    def test_w_method_resumable(self):
        method = "RESUMABLE"
        self._generate_helper(method=method)

    def test_w_response_type(self):
        response_type = "text/plain"
        self._generate_helper(response_type=response_type)

    def test_w_response_disposition(self):
        response_disposition = "attachment; filename=blob.png"
        self._generate_helper(response_disposition=response_disposition)

    def test_w_generation(self):
        generation = "123"
        self._generate_helper(generation=generation)

    def test_w_custom_headers_dict(self):
        self._generate_helper(headers={"x-goog-foo": "bar"})

    def test_w_custom_headers_list(self):
        self._generate_helper(headers=[("x-goog-foo", "bar")])

    def test_w_custom_query_parameters_w_string_value(self):
        self._generate_helper(query_parameters={"bar": "/"})

    def test_w_custom_query_parameters_w_none_value(self):
        self._generate_helper(query_parameters={"qux": None})

    def test_with_google_credentials(self):
        resource = "/name/path"
        credentials = _make_credentials()
        expiration = int(time.time() + 5)
        with self.assertRaises(AttributeError):
            self._call_fut(credentials, resource=resource, expiration=expiration)


class Test_generate_signed_url_v4(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.storage._signing import generate_signed_url_v4

        return generate_signed_url_v4(*args, **kwargs)

    def _generate_helper(
        self,
        expiration=1000,
        api_access_endpoint="",
        method="GET",
        content_type=None,
        content_md5=None,
        response_type=None,
        response_disposition=None,
        generation=None,
        headers=None,
        query_parameters=None,
    ):
        now = datetime.datetime(2019, 2, 26, 19, 53, 27)
        resource = "/name/path"
        signer_email = "service@example.com"
        credentials = _make_credentials(signer_email=signer_email)
        credentials.sign_bytes.return_value = b"DEADBEEF"

        with mock.patch("google.cloud.storage._signing.NOW", lambda: now):
            url = self._call_fut(
                credentials,
                resource,
                expiration,
                api_access_endpoint=api_access_endpoint,
                method=method,
                content_type=content_type,
                content_md5=content_md5,
                response_type=response_type,
                response_disposition=response_disposition,
                generation=generation,
                headers=headers,
                query_parameters=query_parameters,
            )

        # Check the mock was called.
        credentials.sign_bytes.assert_called_once()

        scheme, netloc, path, qs, frag = urllib_parse.urlsplit(url)

        expected_scheme, expected_netloc, _, _, _ = urllib_parse.urlsplit(
            api_access_endpoint
        )
        self.assertEqual(scheme, expected_scheme)
        self.assertEqual(netloc, expected_netloc)
        self.assertEqual(path, resource)
        self.assertEqual(frag, "")

        # Check the URL parameters.
        params = dict(urllib_parse.parse_qsl(qs, keep_blank_values=True))
        self.assertEqual(params["X-Goog-Algorithm"], "GOOG4-RSA-SHA256")

        now_date = now.date().strftime("%Y%m%d")
        expected_cred = "{}/{}/auto/storage/goog4_request".format(
            signer_email, now_date
        )
        self.assertEqual(params["X-Goog-Credential"], expected_cred)

        now_stamp = now.strftime("%Y%m%dT%H%M%SZ")
        self.assertEqual(params["X-Goog-Date"], now_stamp)
        self.assertEqual(params["X-Goog-Expires"], str(expiration))

        signed = binascii.hexlify(credentials.sign_bytes.return_value).decode("ascii")
        self.assertEqual(params["X-Goog-Signature"], signed)

        if response_type is not None:
            self.assertEqual(params["response-content-type"], response_type)

        if response_disposition is not None:
            self.assertEqual(
                params["response-content-disposition"], response_disposition
            )

        if generation is not None:
            self.assertEqual(params["generation"], str(generation))

        if query_parameters is not None:
            for key, value in query_parameters.items():
                value = value.strip() if value else ""
                self.assertEqual(params[key].lower(), value)

    def test_w_expiration_too_long(self):
        with self.assertRaises(ValueError):
            self._generate_helper(expiration=datetime.timedelta(days=8))

    def test_w_defaults(self):
        self._generate_helper()

    def test_w_api_access_endpoint(self):
        self._generate_helper(api_access_endpoint="http://api.example.com")

    def test_w_method(self):
        self._generate_helper(method="PUT")

    def test_w_content_type(self):
        self._generate_helper(content_type="text/plain")

    def test_w_content_md5(self):
        self._generate_helper(content_md5="FACEDACE")

    def test_w_response_type(self):
        self._generate_helper(response_type="application/octets")

    def test_w_response_disposition(self):
        self._generate_helper(response_disposition="attachment")

    def test_w_generation(self):
        self._generate_helper(generation=12345)

    def test_w_custom_headers(self):
        self._generate_helper(headers={"x-goog-foo": "bar"})

    def test_w_custom_query_parameters_w_string_value(self):
        self._generate_helper(query_parameters={"bar": "/"})

    def test_w_custom_query_parameters_w_none_value(self):
        self._generate_helper(query_parameters={"qux": None})


def _make_credentials(signer_email=None):
    import google.auth.credentials

    if signer_email:
        credentials = mock.Mock(spec=google.auth.credentials.Signing)
        credentials.signer_email = signer_email
        return credentials
    else:
        return mock.Mock(spec=google.auth.credentials.Credentials)
