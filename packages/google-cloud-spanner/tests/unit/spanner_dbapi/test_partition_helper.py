# Copyright 2024 Google LLC All rights reserved.
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

import base64
import datetime
import gzip
import json
import unittest

from google.cloud.spanner_dbapi import partition_helper
from google.cloud.spanner_v1 import BatchTransactionId
from google.cloud.spanner_v1.types import ExecuteSqlRequest


class TestPartitionHelper(unittest.TestCase):
    def test_encode_and_decode_success_query(self):
        btid = BatchTransactionId(
            transaction_id=b"test-txn-123",
            session_id="session-xyz",
            read_timestamp=datetime.datetime(
                2024, 5, 10, 12, 34, 56, tzinfo=datetime.timezone.utc
            ),
        )

        query_options = ExecuteSqlRequest.QueryOptions(
            optimizer_version="2",
            optimizer_statistics_package="package-abc",
        )

        partition_result = {
            "partition": b"partition-token-456",
            "query": {
                "sql": "SELECT * FROM users WHERE age > %s",
                "params": {"age": 21},
                "query_options": query_options,
            },
        }

        encoded = partition_helper.encode_to_string(btid, partition_result)
        self.assertIsInstance(encoded, str)

        decoded = partition_helper.decode_from_string(encoded)
        self.assertIsInstance(decoded, partition_helper.PartitionId)

        # Verify BatchTransactionId
        self.assertEqual(
            decoded.batch_transaction_id.transaction_id, btid.transaction_id
        )
        self.assertEqual(decoded.batch_transaction_id.session_id, btid.session_id)
        self.assertEqual(
            decoded.batch_transaction_id.read_timestamp, btid.read_timestamp
        )

        # Verify partition result
        self.assertEqual(decoded.partition_result["partition"], b"partition-token-456")
        self.assertEqual(
            decoded.partition_result["query"]["sql"],
            "SELECT * FROM users WHERE age > %s",
        )
        self.assertEqual(decoded.partition_result["query"]["params"], {"age": 21})

        # Verify query options (restored to object)
        opts_obj = decoded.partition_result["query"]["query_options"]
        self.assertEqual(opts_obj.optimizer_version, "2")
        self.assertEqual(opts_obj.optimizer_statistics_package, "package-abc")

    def test_encode_and_decode_success_read(self):
        btid = BatchTransactionId(
            transaction_id=b"test-txn-456",
            session_id="session-abc",
            read_timestamp=None,
        )

        partition_result = {
            "partition": b"partition-token-789",
            "read": {
                "table": "users",
                "columns": ["name", "age"],
                "keyset": {"keys": [[1], [2]]},
            },
        }

        encoded = partition_helper.encode_to_string(btid, partition_result)
        decoded = partition_helper.decode_from_string(encoded)

        self.assertEqual(
            decoded.batch_transaction_id.transaction_id, btid.transaction_id
        )
        self.assertEqual(decoded.batch_transaction_id.session_id, btid.session_id)
        self.assertIsNone(decoded.batch_transaction_id.read_timestamp)

        self.assertEqual(decoded.partition_result["partition"], b"partition-token-789")
        self.assertEqual(decoded.partition_result["read"]["table"], "users")
        self.assertEqual(decoded.partition_result["read"]["columns"], ["name", "age"])
        self.assertEqual(
            decoded.partition_result["read"]["keyset"], {"keys": [[1], [2]]}
        )

    def test_insecure_deserialization_failure(self):
        # Malicious payload that attempts to execute pickle.loads under old code
        # (Here, we'll just pass invalid JSON wrapped in gzip + base64, or a pickle payload,
        # and make sure it does NOT get deserialized or execute anything, but raises an error gracefully)

        # A valid pickle payload for some simple object, base64 encoded and compressed
        import pickle

        pickle_bytes = pickle.dumps({"test": "payload"})
        gzip_bytes = gzip.compress(pickle_bytes)
        encoded_pickle = base64.b64encode(gzip_bytes).decode("utf-8")

        # Since we now use json.loads, a pickle payload will fail to decode as UTF-8 / JSON
        with self.assertRaises((json.JSONDecodeError, UnicodeDecodeError)):
            partition_helper.decode_from_string(encoded_pickle)
