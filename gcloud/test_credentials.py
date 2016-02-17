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


def _setup_appengine_import(test_case, app_identity):
    import sys
    import types

    GOOGLE = types.ModuleType('google')
    GAE = types.ModuleType('appengine')
    GAE_API = types.ModuleType('api')
    GAE_EXT = types.ModuleType('ext')
    GAE_EXT_WEBAPP = types.ModuleType('webapp')
    GAE_EXT_WEBAPP_UTIL = types.ModuleType('util')

    GOOGLE.appengine = GAE
    GAE.api = GAE_API
    GAE.api.app_identity = app_identity
    GAE.api.memcache = None
    GAE.api.users = None
    GAE.ext = GAE_EXT
    GAE.ext.db = _MockDB
    GAE.ext.webapp = GAE_EXT_WEBAPP
    GAE.ext.webapp.util = GAE_EXT_WEBAPP_UTIL
    GAE.ext.webapp.util.login_required = None
    GAE.ext.webapp.util.run_wsgi_app = None

    test_case._PREV_GOOGLE_MODULE = sys.modules['google']

    sys.modules['google'] = GOOGLE
    sys.modules['google.appengine'] = GAE
    sys.modules['google.appengine.api'] = GAE_API
    sys.modules['google.appengine.ext'] = GAE_EXT
    sys.modules['google.appengine.ext.webapp'] = GAE_EXT_WEBAPP
    sys.modules['google.appengine.ext.webapp.util'] = GAE_EXT_WEBAPP_UTIL
    sys.modules['webapp2'] = GAE_EXT_WEBAPP


def _teardown_appengine_import(test_case):
    import sys
    sys.modules.pop('google')
    sys.modules.pop('google.appengine')
    sys.modules.pop('google.appengine.api')
    sys.modules.pop('google.appengine.ext')
    sys.modules.pop('google.appengine.ext.webapp')
    sys.modules.pop('google.appengine.ext.webapp.util')
    sys.modules.pop('webapp2')

    sys.modules['google'] = test_case._PREV_GOOGLE_MODULE


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


class Test_get_for_service_account_p12(unittest2.TestCase):

    def _callFUT(self, client_email, private_key_path, scope=None):
        from gcloud.credentials import get_for_service_account_p12
        return get_for_service_account_p12(client_email, private_key_path,
                                           scope=scope)

    def test_it(self):
        from gcloud import credentials as MUT
        from gcloud._testing import _Monkey

        CLIENT_EMAIL = 'phred@example.com'
        MOCK_FILENAME = 'foo.path'
        MOCK_CRED_CLASS = _MockServiceAccountCredentials()
        with _Monkey(MUT, ServiceAccountCredentials=MOCK_CRED_CLASS):
            found = self._callFUT(CLIENT_EMAIL, MOCK_FILENAME)

        self.assertTrue(found is MOCK_CRED_CLASS._result)
        self.assertEqual(MOCK_CRED_CLASS.p12_called,
                         [(CLIENT_EMAIL, MOCK_FILENAME, None)])

    def test_it_with_scope(self):
        from gcloud import credentials as MUT
        from gcloud._testing import _Monkey

        CLIENT_EMAIL = 'phred@example.com'
        SCOPE = 'SCOPE'
        MOCK_FILENAME = 'foo.path'
        MOCK_CRED_CLASS = _MockServiceAccountCredentials()
        with _Monkey(MUT, ServiceAccountCredentials=MOCK_CRED_CLASS):
            found = self._callFUT(CLIENT_EMAIL, MOCK_FILENAME, SCOPE)

        self.assertTrue(found is MOCK_CRED_CLASS._result)
        self.assertEqual(MOCK_CRED_CLASS.p12_called,
                         [(CLIENT_EMAIL, MOCK_FILENAME, SCOPE)])


class Test_get_for_service_account_json(unittest2.TestCase):

    def _callFUT(self, json_credentials_path, scope=None):
        from gcloud.credentials import get_for_service_account_json
        return get_for_service_account_json(json_credentials_path, scope=scope)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        CREDS = _Credentials()
        _filenames = []

        def get_creds(filename):
            _filenames.append(filename)
            return CREDS

        FILENAME = object()

        renames = {'_get_application_default_credential_from_file': get_creds}
        with _Monkey(MUT, **renames):
            self._callFUT(FILENAME)

        self.assertEqual(_filenames, [FILENAME])
        self.assertFalse(hasattr(CREDS, '_scopes'))

    def test_it_with_scope(self):
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        CREDS = _Credentials()
        _filenames = []

        def get_creds(filename):
            _filenames.append(filename)
            return CREDS

        FILENAME = object()
        SCOPE = object()

        renames = {'_get_application_default_credential_from_file': get_creds}
        with _Monkey(MUT, **renames):
            self._callFUT(FILENAME, scope=SCOPE)

        self.assertEqual(_filenames, [FILENAME])
        self.assertEqual(CREDS._scopes, SCOPE)


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
                'GoogleAccessId': credentials.service_account_name,
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
                         [_Credentials.service_account_name])
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


class Test__get_signature_bytes(unittest2.TestCase):

    def setUp(self):
        SERVICE_ACCOUNT_NAME = 'SERVICE_ACCOUNT_NAME'
        self.APP_IDENTITY = _AppIdentity(SERVICE_ACCOUNT_NAME)
        _setup_appengine_import(self, self.APP_IDENTITY)

    def tearDown(self):
        _teardown_appengine_import(self)

    def _callFUT(self, credentials, string_to_sign):
        from gcloud.credentials import _get_signature_bytes
        return _get_signature_bytes(credentials, string_to_sign)

    def _run_with_fake_crypto(self, credentials, private_key_text,
                              string_to_sign):
        import base64
        import six
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        crypt = _Crypt()
        load_result = object()
        sign_result = object()
        openssl_crypto = _OpenSSLCrypto(load_result, sign_result)

        with _Monkey(MUT, crypt=crypt, crypto=openssl_crypto):
            result = self._callFUT(credentials, string_to_sign)

        if crypt._pkcs12_key_as_pem_called:
            self.assertEqual(crypt._private_key_text, private_key_text)
            self.assertEqual(crypt._private_key_password, 'notasecret')
            self.assertEqual(openssl_crypto._loaded,
                             [(openssl_crypto.FILETYPE_PEM, _Crypt._KEY)])
        else:
            self.assertEqual(openssl_crypto._loaded,
                             [(openssl_crypto.FILETYPE_PEM, private_key_text)])

        if not isinstance(string_to_sign, six.binary_type):
            string_to_sign = string_to_sign.encode('utf-8')
        self.assertEqual(openssl_crypto._signed,
                         [(load_result, string_to_sign, 'SHA256')])

        self.assertEqual(result, sign_result)

    def test_p12_type(self):
        from oauth2client.service_account import ServiceAccountCredentials
        ACCOUNT_NAME = 'dummy_service_account_name'
        PRIVATE_KEY_TEXT = b'dummy_private_key_text'
        STRING_TO_SIGN = b'dummy_signature'
        SIGNER = object()
        CREDENTIALS = ServiceAccountCredentials(
            ACCOUNT_NAME, SIGNER)
        CREDENTIALS._private_key_pkcs12 = PRIVATE_KEY_TEXT
        CREDENTIALS._private_key_password = 'notasecret'
        self._run_with_fake_crypto(CREDENTIALS, PRIVATE_KEY_TEXT,
                                   STRING_TO_SIGN)

    def test_p12_type_non_bytes_to_sign(self):
        from oauth2client.service_account import ServiceAccountCredentials
        ACCOUNT_NAME = 'dummy_service_account_name'
        PRIVATE_KEY_TEXT = b'dummy_private_key_text'
        STRING_TO_SIGN = u'dummy_signature'
        SIGNER = object()
        CREDENTIALS = ServiceAccountCredentials(
            ACCOUNT_NAME, SIGNER)
        CREDENTIALS._private_key_pkcs12 = PRIVATE_KEY_TEXT
        CREDENTIALS._private_key_password = 'notasecret'
        self._run_with_fake_crypto(CREDENTIALS, PRIVATE_KEY_TEXT,
                                   STRING_TO_SIGN)

    def test_json_type(self):
        from oauth2client import service_account
        from gcloud._testing import _Monkey

        PRIVATE_KEY_TEXT = 'dummy_private_key_pkcs8_text'
        STRING_TO_SIGN = b'dummy_signature'
        SIGNER = object()
        CREDENTIALS = service_account.ServiceAccountCredentials(
            'dummy_service_account_email', SIGNER)
        CREDENTIALS._private_key_pkcs8_pem = PRIVATE_KEY_TEXT
        self._run_with_fake_crypto(CREDENTIALS, PRIVATE_KEY_TEXT,
                                   STRING_TO_SIGN)

    def test_gae_type(self):
        # Relies on setUp fixing up App Engine imports.
        from oauth2client.contrib.appengine import AppAssertionCredentials
        from gcloud._testing import _Monkey
        from gcloud import credentials

        APP_IDENTITY = self.APP_IDENTITY
        CREDENTIALS = AppAssertionCredentials([])
        STRING_TO_SIGN = b'STRING_TO_SIGN'

        with _Monkey(credentials, _GAECreds=AppAssertionCredentials,
                     app_identity=APP_IDENTITY):
            signed_bytes = self._callFUT(CREDENTIALS, b'STRING_TO_SIGN')

        self.assertEqual(signed_bytes, STRING_TO_SIGN)
        self.assertEqual(APP_IDENTITY._strings_signed, [STRING_TO_SIGN])

    def test_without_pyopenssl(self):
        from gcloud._testing import _Monkey
        from gcloud import credentials as credentials_mod

        mock_called = []
        credentials = object()

        def mock_pem_key(local_creds):
            mock_called.append(local_creds)

        with _Monkey(credentials_mod, crypto=None, _get_pem_key=mock_pem_key):
            with self.assertRaises(EnvironmentError):
                self._callFUT(credentials, b'STRING_TO_SIGN')
            self.assertEqual(mock_called, [credentials])


class Test__get_service_account_name(unittest2.TestCase):

    def setUp(self):
        SERVICE_ACCOUNT_NAME = 'SERVICE_ACCOUNT_NAME'
        self.APP_IDENTITY = _AppIdentity(SERVICE_ACCOUNT_NAME)
        _setup_appengine_import(self, self.APP_IDENTITY)

    def tearDown(self):
        _teardown_appengine_import(self)

    def _callFUT(self, credentials):
        from gcloud.credentials import _get_service_account_name
        return _get_service_account_name(credentials)

    def test_bad_type(self):
        from oauth2client.client import OAuth2Credentials
        CREDENTIALS = OAuth2Credentials('bogus_token', 'bogus_id',
                                        'bogus_secret', 'bogus_refresh',
                                        None, None, None)
        self.assertRaises(ValueError, self._callFUT, CREDENTIALS)

    def test_service_account_type(self):
        from oauth2client import service_account

        SERVICE_ACCOUNT_NAME = 'SERVICE_ACCOUNT_NAME'
        SIGNER = object()
        CREDENTIALS = service_account.ServiceAccountCredentials(
            SERVICE_ACCOUNT_NAME, SIGNER)

        found = self._callFUT(CREDENTIALS)
        self.assertEqual(found, SERVICE_ACCOUNT_NAME)

    def test_gae_type(self):
        # Relies on setUp fixing up App Engine imports.
        from oauth2client.contrib.appengine import AppAssertionCredentials
        from gcloud._testing import _Monkey
        from gcloud import credentials

        APP_IDENTITY = self.APP_IDENTITY
        SERVICE_ACCOUNT_NAME = APP_IDENTITY.service_account_name

        CREDENTIALS = AppAssertionCredentials([])

        with _Monkey(credentials, _GAECreds=AppAssertionCredentials,
                     app_identity=APP_IDENTITY):
            found = self._callFUT(CREDENTIALS)

        self.assertEqual(found, SERVICE_ACCOUNT_NAME)


class Test__get_signed_query_params(unittest2.TestCase):

    def _callFUT(self, credentials, expiration, string_to_sign):
        from gcloud.credentials import _get_signed_query_params
        return _get_signed_query_params(credentials, expiration,
                                        string_to_sign)

    def test_it(self):
        import base64
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        _called_get_sig = []
        SIG_BYTES = b'DEADBEEF'

        def mock_get_sig_bytes(creds, string_to_sign):
            _called_get_sig.append((creds, string_to_sign))
            return SIG_BYTES

        _called_get_name = []
        ACCOUNT_NAME = object()

        def mock_get_name(creds):
            _called_get_name.append((creds,))
            return ACCOUNT_NAME

        CREDENTIALS = object()
        EXPIRATION = 100
        STRING_TO_SIGN = 'dummy_signature'
        with _Monkey(MUT, _get_signature_bytes=mock_get_sig_bytes,
                     _get_service_account_name=mock_get_name):
            result = self._callFUT(CREDENTIALS, EXPIRATION,
                                   STRING_TO_SIGN)

        self.assertEqual(result, {
            'GoogleAccessId': ACCOUNT_NAME,
            'Expires': str(EXPIRATION),
            'Signature': base64.b64encode(b'DEADBEEF'),
        })
        self.assertEqual(_called_get_sig,
                         [(CREDENTIALS, STRING_TO_SIGN)])
        self.assertEqual(_called_get_name, [(CREDENTIALS,)])


class Test__get_pem_key(unittest2.TestCase):

    def _callFUT(self, credentials):
        from gcloud.credentials import _get_pem_key
        return _get_pem_key(credentials)

    def test_bad_argument(self):
        self.assertRaises(TypeError, self._callFUT, None)

    def test_signed_jwt_for_p12(self):
        from oauth2client import service_account
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        PRIVATE_KEY = b'dummy_private_key_text'
        SIGNER = object()
        credentials = service_account.ServiceAccountCredentials(
            'dummy_service_account_email', SIGNER)
        credentials._private_key_pkcs12 = PRIVATE_KEY
        credentials._private_key_password = password = 'password-nope'

        crypt = _Crypt()
        load_result = object()
        openssl_crypto = _OpenSSLCrypto(load_result, None)

        with _Monkey(MUT, crypt=crypt, crypto=openssl_crypto):
            result = self._callFUT(credentials)

        self.assertEqual(crypt._private_key_text, PRIVATE_KEY)
        self.assertEqual(crypt._private_key_password, password)
        self.assertEqual(result, load_result)
        self.assertEqual(openssl_crypto._loaded,
                         [(openssl_crypto.FILETYPE_PEM, _Crypt._KEY)])
        self.assertEqual(openssl_crypto._signed, [])

    def test_service_account_via_json_key(self):
        from oauth2client import service_account
        from gcloud._testing import _Monkey
        from gcloud import credentials as MUT

        scopes = []

        PRIVATE_TEXT = 'dummy_private_key_pkcs8_text'
        SIGNER = object()
        credentials = service_account.ServiceAccountCredentials(
            'dummy_service_account_email', SIGNER, scopes=scopes)
        credentials._private_key_pkcs8_pem = PRIVATE_TEXT

        load_result = object()
        openssl_crypto = _OpenSSLCrypto(load_result, None)

        with _Monkey(MUT, crypto=openssl_crypto):
            result = self._callFUT(credentials)

        self.assertEqual(result, load_result)
        self.assertEqual(openssl_crypto._loaded,
                         [(openssl_crypto.FILETYPE_PEM, PRIVATE_TEXT)])
        self.assertEqual(openssl_crypto._signed, [])

    def test_without_pyopenssl(self):
        from oauth2client import service_account
        from gcloud._testing import _Monkey
        from gcloud import credentials as credentials_mod

        PRIVATE_TEXT = 'dummy_private_key_pkcs8_text'
        SIGNER = object()

        credentials = service_account.ServiceAccountCredentials(
            'dummy_service_account_email', SIGNER)
        credentials._private_key_pkcs8_pem = PRIVATE_TEXT

        with _Monkey(credentials_mod, crypto=None):
            with self.assertRaises(EnvironmentError):
                self._callFUT(credentials)


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


class _Crypt(object):

    _pkcs12_key_as_pem_called = False
    _KEY = '__PEM__'

    def pkcs12_key_as_pem(self, private_key_text, private_key_password):
        self._pkcs12_key_as_pem_called = True
        self._private_key_text = private_key_text
        self._private_key_password = private_key_password
        return self._KEY


class _OpenSSLCrypto(object):

    FILETYPE_PEM = object()

    def __init__(self, load_result, sign_result):
        self._loaded = []
        self._load_result = load_result
        self._signed = []
        self._sign_result = sign_result

    def load_privatekey(self, key_type, key_text):
        self._loaded.append((key_type, key_text))
        return self._load_result

    def sign(self, pkey, to_sign, sign_algo):
        self._signed.append((pkey, to_sign, sign_algo))
        return self._sign_result


class _AppIdentity(object):

    def __init__(self, service_account_name):
        self._strings_signed = []
        self.service_account_name = service_account_name

    def get_service_account_name(self):
        return self.service_account_name

    def sign_blob(self, string_to_sign):
        self._strings_signed.append(string_to_sign)
        throwaway = object()
        return throwaway, string_to_sign


class _MockDB(object):

    Model = object
    Property = object
    StringProperty = object
    _stored = []

    @staticmethod
    def non_transactional(*args, **kwargs):
        _MockDB._stored.append((args, kwargs))  # To please lint.

        def do_nothing_wrapper(func):
            return func
        return do_nothing_wrapper


class _MockServiceAccountCredentials(object):

    def __init__(self):
        self.p12_called = []
        self._result = _Credentials()

    def from_p12_keyfile(self, email, path, scopes=None):
        self.p12_called.append((email, path, scopes))
        return self._result
