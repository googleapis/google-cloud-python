import unittest2


class Test_get_for_service_account(unittest2.TestCase):

    def test_get_for_service_account_wo_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = credentials.get_for_service_account(CLIENT_EMAIL,
                                                            file_obj.name)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': None,
        }
        self.assertEqual(client._called_with, expected_called_with)

    def test_get_for_service_account_w_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        SCOPE = 'SCOPE'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = credentials.get_for_service_account(
                    CLIENT_EMAIL, file_obj.name, SCOPE)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)


class Test_generate_signed_url(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.credentials import generate_signed_url

        return generate_signed_url(*args, **kw)

    def test__w_expiration_int(self):
        import base64
        import urlparse
        from gcloud._testing import _Monkey
        from gcloud import credentials

        ENDPOINT = 'http://api.example.com'
        RESOURCE = '/name/key'
        SIGNED = base64.b64encode('DEADBEEF')
        crypto = _Crypto()
        rsa = _RSA()
        pkcs_v1_5 = _PKCS1_v1_5()
        sha256 = _SHA256()
        creds = _Credentials()

        with _Monkey(credentials, crypto=crypto, RSA=rsa, PKCS1_v1_5=pkcs_v1_5,
                     SHA256=sha256):
            url = self._callFUT(creds, ENDPOINT, RESOURCE, 1000)

        scheme, netloc, path, qs, frag = urlparse.urlsplit(url)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'api.example.com')
        self.assertEqual(path, RESOURCE)
        params = urlparse.parse_qs(qs)
        self.assertEqual(len(params), 3)
        self.assertEqual(params['Signature'], [SIGNED])
        self.assertEqual(params['Expires'], ['1000'])
        self.assertEqual(params['GoogleAccessId'],
                         [_Credentials.service_account_name])
        self.assertEqual(frag, '')


class Test__get_expiration_seconds(unittest2.TestCase):

    def _callFUT(self, expiration):
        from gcloud.credentials import _get_expiration_seconds

        return _get_expiration_seconds(expiration)

    def _utc_seconds(self, when):
        import calendar

        return int(calendar.timegm(when.timetuple()))

    def test__get_expiration_seconds_w_invalid(self):
        self.assertRaises(TypeError, self._callFUT, object())
        self.assertRaises(TypeError, self._callFUT, None)

    def test__get_expiration_seconds_w_int(self):
        self.assertEqual(self._callFUT(123), 123)

    def test__get_expiration_seconds_w_long(self):
        try:
            long
        except NameError:  # pragma: NO COVER Py3K
            pass
        else:
            self.assertEqual(self._callFUT(long(123)), 123)

    def test__get_expiration_w_naive_datetime(self):
        import datetime

        expiration_no_tz = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(expiration_no_tz)
        self.assertEqual(self._callFUT(expiration_no_tz), utc_seconds)

    def test__get_expiration_w_utc_datetime(self):
        import datetime
        import pytz

        expiration_utc = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, pytz.utc)
        utc_seconds = self._utc_seconds(expiration_utc)
        self.assertEqual(self._callFUT(expiration_utc), utc_seconds)

    def test__get_expiration_w_other_zone_datetime(self):
        import datetime
        import pytz

        zone = pytz.timezone('CET')
        expiration_other = datetime.datetime(2004, 8, 19, 0, 0, 0, 0, zone)
        utc_seconds = self._utc_seconds(expiration_other)
        cet_seconds = utc_seconds - (60 * 60)  # CET one hour earlier than UTC
        self.assertEqual(self._callFUT(expiration_other), cet_seconds)

    def test__get_expiration_seconds_w_timedelta_seconds(self):
        import datetime
        from gcloud import credentials
        from gcloud._testing import _Monkey

        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(seconds=10)

        with _Monkey(credentials, _utcnow=lambda: dummy_utcnow):
            result = self._callFUT(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 10)

    def test__get_expiration_seconds_w_timedelta_days(self):
        import datetime
        from gcloud import credentials
        from gcloud._testing import _Monkey

        dummy_utcnow = datetime.datetime(2004, 8, 19, 0, 0, 0, 0)
        utc_seconds = self._utc_seconds(dummy_utcnow)
        expiration_as_delta = datetime.timedelta(days=1)

        with _Monkey(credentials, _utcnow=lambda: dummy_utcnow):
            result = self._callFUT(expiration_as_delta)

        self.assertEqual(result, utc_seconds + 86400)


class _Client(object):
    def __init__(self):
        self._signed = object()

    def SignedJwtAssertionCredentials(self, **kw):
        self._called_with = kw
        return self._signed


class _Credentials(object):

    service_account_name = 'testing@example.com'

    @property
    def private_key(self):
        import base64
        return base64.b64encode('SEEKRIT')


class _Crypto(object):

    FILETYPE_PEM = 'pem'
    _loaded = _dumped = None

    def load_pkcs12(self, buffer, passphrase):
        self._loaded = (buffer, passphrase)
        return self

    def get_privatekey(self):
        return '__PKCS12__'

    def dump_privatekey(self, type, pkey, cipher=None, passphrase=None):
        self._dumped = (type, pkey, cipher, passphrase)
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
        return 'DEADBEEF'


class _SHA256(object):

    _signature_string = None

    def new(self, signature_string):
        self._signature_string = signature_string
        return self
