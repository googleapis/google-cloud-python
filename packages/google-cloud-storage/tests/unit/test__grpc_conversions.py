# Copyright 2026 Google LLC
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

import unittest
from unittest import mock


class Test_blob_to_proto(unittest.TestCase):
    def _call_fut(self, blob):
        from google.cloud.storage._grpc_conversions import blob_to_proto

        return blob_to_proto(blob)

    def test_w_contexts(self):
        from google.cloud.storage.blob import Blob, ObjectContexts
        from google.cloud.storage.bucket import Bucket

        blob_name = "blob-name"
        bucket_name = "bucket-name"
        bucket = mock.Mock(spec=Bucket)
        bucket.name = bucket_name
        blob = mock.Mock(spec=Blob)
        blob.name = blob_name
        blob.bucket = bucket
        blob.content_type = None
        blob.metadata = None
        blob.kms_key_name = None

        contexts = ObjectContexts(blob)
        contexts.update({"custom": {"foo": {"value": "bar"}}})
        blob.contexts = contexts

        proto = self._call_fut(blob)

        self.assertEqual(proto.name, blob_name)
        self.assertEqual(proto.bucket, f"projects/_/buckets/{bucket_name}")
        self.assertEqual(proto.contexts.custom["foo"].value, "bar")
