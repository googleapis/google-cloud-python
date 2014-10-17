import unittest2


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self, client_email, private_key_path):
        from gcloud.datastore import get_connection
        return get_connection(client_email, private_key_path)

    def test_it(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud.datastore import SCOPE
        from gcloud.datastore.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as f:
                f.write(PRIVATE_KEY)
                f.flush()
                found = self._callFUT(CLIENT_EMAIL, f.name)
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)


class Test_get_dataset(unittest2.TestCase):

    def _callFUT(self, dataset_id, client_email, private_key_path):
        from gcloud.datastore import get_dataset
        return get_dataset(dataset_id, client_email, private_key_path)

    def test_it(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud.datastore import SCOPE
        from gcloud.datastore.connection import Connection
        from gcloud.datastore.dataset import Dataset
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        DATASET_ID = 'DATASET'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as f:
                f.write(PRIVATE_KEY)
                f.flush()
                found = self._callFUT(DATASET_ID, CLIENT_EMAIL, f.name)
        self.assertTrue(isinstance(found, Dataset))
        self.assertTrue(isinstance(found.connection(), Connection))
        self.assertEqual(found.id(), DATASET_ID)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)
