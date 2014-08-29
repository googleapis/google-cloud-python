import unittest2

from gcloud.storage.bucket import Bucket
from gcloud.storage.connection import Connection
from gcloud.storage.key import Key


class TestKey(unittest2.TestCase):

  def setUp(self):
    # Mock Connection.api_request with a method that just stores the HTTP
    # method, path and query params in an instance variable for later
    # inspection.
    # TODO: It'd be better to make the Connection talk to a local HTTP server
    # that we can inspect, but a simple test using a mock is certainly better
    # than no tests.
    self.connection = Connection('project-name')
    self.connection.api_request = self.mock_api_request
    self.api_request_calls = []

  def mock_api_request(self, method, path=None, query_params=None,
                       data=None, content_type=None,
                       api_base_url=None, api_version=None,
                       expect_json=True):
    self.api_request_calls.append([method, path, query_params])

  def test_rename(self):
    bucket = Bucket(self.connection, 'bucket')
    key = Key(bucket, 'key')
    orig_key_path = key.path
    key.rename('new-name')
    expected = [
        ['POST', orig_key_path + '/copyTo/b/bucket/o/new-name', None],
        ['DELETE', orig_key_path, None]]
    self.assertEqual(key.name, 'new-name')
    self.assertEqual(self.api_request_calls, expected)
