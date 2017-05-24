import unittest
import subprocess, os, sys

from google.cloud.bigtable.client import Client
from google.cloud.bigtable.instance import Instance
from google.cloud.bigtable.table import Table

class TestRetry(unittest.TestCase):

    TEST_SCRIPT = "unit_tests/retry_test.txt"

    def test_retry(self):
    	table, server = self.connect_to_server()
        f = open(self.TEST_SCRIPT, 'r')
        for line in f.readlines():
            if line.startswith("CLIENT:"):
                self.process_line(table, line)
    	server.kill()

    def process_line(self, table, line):
        chunks = line.split(" ")
        op = chunks[1]
        if (op == "READ"):
            self.process_read(table, chunks[2])
        elif (op == "WRITE"):
            self.process_write(table, chunks[2])
        elif (op == "SCAN"):
            self.process_scan(table, chunks[2], chunks[3])

    def process_read(self, table, payload):
        pass

    def process_write(self, table, payload):
        pass

    def process_scan(self, table, range, ids):
        range_chunks = range.split(",")
        range_open = range_chunks[0].lstrip("[")
        range_close = range_chunks[1].rstrip(")")
        rows = table.read_rows(range_open, range_close)
        rows.consume_all()

    def connect_to_server(self):
    	server = subprocess.Popen(
    		['./unit_tests/retry', '--script=' + self.TEST_SCRIPT],
    		stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    	)

    	(endpoint, port) = server.stdout.readline().rstrip("\n").split(":")
    	os.environ["BIGTABLE_EMULATOR_HOST"] = endpoint + ":" + port
    	client = Client(project="client", admin=True)
    	instance = Instance("instance", client)
    	table = instance.table("table")
    	return (table, server)
