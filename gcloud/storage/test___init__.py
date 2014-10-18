import unittest2


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.storage import get_connection
        return get_connection(*args, **kw)

    def test_it(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud.storage import SCOPE
        from gcloud.storage.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey
        PROJECT = 'project'
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as f:
                f.write(PRIVATE_KEY)
                f.flush()
                found = self._callFUT(PROJECT, CLIENT_EMAIL, f.name)
        self.assertTrue(isinstance(found, Connection))
        self.assertEqual(found.project, PROJECT)
        self.assertTrue(found._credentials is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)


class Test_get_bucket(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.storage import get_bucket

        return get_bucket(*args, **kw)

    def test_it(self):
        from tempfile import NamedTemporaryFile
        from gcloud import storage
        from gcloud._testing import _Monkey

        bucket = object()

        class _Connection(object):

            def get_bucket(self, bucket_name):
                self._called_With = bucket_name
                return bucket
        connection = _Connection()
        _called_With = []

        def get_connection(*args, **kw):
            _called_With.append((args, kw))
            return connection
        BUCKET = 'bucket'
        PROJECT = 'project'
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        with _Monkey(storage, get_connection=get_connection):
            with NamedTemporaryFile() as f:
                f.write(PRIVATE_KEY)
                f.flush()
                found = self._callFUT(BUCKET, PROJECT, CLIENT_EMAIL, f.name)
        self.assertTrue(found is bucket)
        self.assertEqual(_called_With,
                         [((PROJECT, CLIENT_EMAIL, f.name), {})])
        self.assertEqual(connection._called_With, BUCKET)
