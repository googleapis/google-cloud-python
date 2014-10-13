import unittest2


class TestCredentials(unittest2.TestCase):

    @staticmethod
    def _getTargetClass():
        from gcloud.credentials import Credentials
        return Credentials

    def test_get_for_service_account_wo_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        cls = self._getTargetClass()
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = cls.get_for_service_account(CLIENT_EMAIL,
                                                    file_obj.name)
        self.assertTrue(found is client._signed)
        expected_called_with = {'service_account_name': CLIENT_EMAIL,
                                'private_key': PRIVATE_KEY,
                                'scope': None}
        self.assertEqual(client._called_with, expected_called_with)

    def test_get_for_service_account_w_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        SCOPE = 'SCOPE'
        cls = self._getTargetClass()
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = cls.get_for_service_account(CLIENT_EMAIL,
                                                    file_obj.name, SCOPE)
        self.assertTrue(found is client._signed)
        expected_called_with = {'service_account_name': CLIENT_EMAIL,
                                'private_key': PRIVATE_KEY,
                                'scope': SCOPE}
        self.assertEqual(client._called_with, expected_called_with)


class _Client(object):
    def __init__(self):
        self._signed = object()

    def SignedJwtAssertionCredentials(self, **kw):
        self._called_with = kw
        return self._signed


class _Monkey(object):

    # context-manager for replacing module names in the scope of a test.

    def __init__(self, module, **kw):
        self.module = module
        self.to_restore = dict([(key, getattr(module, key)) for key in kw])
        for key, value in kw.items():
            setattr(module, key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key, value in self.to_restore.items():
            setattr(self.module, key, value)
