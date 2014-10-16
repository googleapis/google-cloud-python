import unittest2


class TestCredentials(unittest2.TestCase):

    def test_get_for_service_account_wo_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as f:
                f.write(PRIVATE_KEY)
                f.flush()
                found = credentials.get_for_service_account(
                    CLIENT_EMAIL, f.name)
        self.assertTrue(found is client._signed)
        self.assertEqual(client._called_with,
                         {'service_account_name': CLIENT_EMAIL,
                          'private_key': PRIVATE_KEY,
                          'scope': None,
                          })

    def test_get_for_service_account_w_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        SCOPE = 'SCOPE'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as f:
                f.write(PRIVATE_KEY)
                f.flush()
                found = credentials.get_for_service_account(
                    CLIENT_EMAIL, f.name, SCOPE)
        self.assertTrue(found is client._signed)
        self.assertEqual(client._called_with,
                         {'service_account_name': CLIENT_EMAIL,
                          'private_key': PRIVATE_KEY,
                          'scope': SCOPE,
                          })


class _Client(object):

    def __init__(self):
        self._signed = object()

    def SignedJwtAssertionCredentials(self, **kw):
        self._called_with = kw
        return self._signed
