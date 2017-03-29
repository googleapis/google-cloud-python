import unittest
import subprocess, os

from google.cloud.bigtable.client import Client

class TestTable(unittest.TestCase):

    def test_dummy(self):
    	self.connect_to_server()
    	self.assertEqual(1, 2)

    def connect_to_server(self):
	server = subprocess.Popen(
		['./unit_tests/retry', '--script=unit_tests/retry_test.txt'],
		stdout=subprocess.PIPE
	)

	(endpoint, port) = server.stdout.readline().split(":")
	self.set_config(endpoint, port)
	client = Client(admin=True)
	instance = client.instance("test-instance-id", "us-central1-c", "test-instance")
	try:
		instance.create()
	except Exception:
		instance.delete()
		instance.create()
	print instance.list_tables()

    def set_config(self, endpoint, port):
	os.environ["BIGTABLE_RPC_TIMEOUT_MS_KEY"] = "1000"
	os.environ["BIGTABLE_NULL_CREDENTIAL_ENABLE_KEY"] = "true"
	os.environ["BIGTABLE_USE_PLAINTEXT_NEGOTIATION"] = "true"
	os.environ["BIGTABLE_TABLE_ADMIN_HOST_KEY"] = endpoint
	os.environ["BIGTABLE_HOST_KEY"] = endpoint
	os.environ["BIGTABLE_PORT_KEY"] = port
