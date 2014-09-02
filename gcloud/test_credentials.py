import unittest2

class TestCredentials(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.credentials import Credentials
        return Credentials

    def test_get_for_service_account_wo_scope(self):
        from tempfile import NamedTemporaryFile
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        signed = object()
        class Client(object):
            def SignedJwtAssertionCredentials(self, **kw):
                self._called_with = kw
                return signed
        cls = self._getTargetClass()
        cls._CLIENT = client = Client()
        with NamedTemporaryFile() as f:
            f.write(PRIVATE_KEY)
            f.flush()
            found = cls.get_for_service_account(CLIENT_EMAIL, f.name)
        self.assertTrue(found is signed)
        self.assertEqual(client._called_with,
                         {'service_account_name': CLIENT_EMAIL,
                          'private_key': PRIVATE_KEY,
                          'scope': None,
                         })

    def test_get_for_service_account_w_scope(self):
        from tempfile import NamedTemporaryFile
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        SCOPE = 'SCOPE'
        signed = object()
        class Client(object):
            def SignedJwtAssertionCredentials(self, **kw):
                self._called_with = kw
                return signed
        cls = self._getTargetClass()
        cls._CLIENT = client = Client()
        with NamedTemporaryFile() as f:
            f.write(PRIVATE_KEY)
            f.flush()
            found = cls.get_for_service_account(CLIENT_EMAIL, f.name, SCOPE)
        self.assertTrue(found is signed)
        self.assertEqual(client._called_with,
                         {'service_account_name': CLIENT_EMAIL,
                          'private_key': PRIVATE_KEY,
                          'scope': SCOPE,
                         })
