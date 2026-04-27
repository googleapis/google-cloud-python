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
from unittest.mock import Mock
from google.cloud.storage import _grpc_conversions


class Test_blob_to_proto(unittest.TestCase):
    def test_blob_to_proto_all_fields(self):
        from google.cloud.storage.blob import Blob
        from google.cloud.storage.bucket import Bucket

        bucket = Mock(spec=Bucket)
        bucket.name = "bucket-name"
        blob = Blob("blob-name", bucket)
        blob.content_type = "text/plain"
        blob.metadata = {"foo": "bar"}
        blob.kms_key_name = "kms-key-name"
        blob.cache_control = "cache-control"
        blob.content_disposition = "content-disposition"
        blob.content_encoding = "content-encoding"
        blob.content_language = "content-language"

        proto = _grpc_conversions.blob_to_proto(blob)

        self.assertEqual(proto.name, "blob-name")
        self.assertEqual(proto.bucket, "projects/_/buckets/bucket-name")
        self.assertEqual(proto.content_type, "text/plain")
        self.assertEqual(proto.metadata, {"foo": "bar"})
        self.assertEqual(proto.kms_key, "kms-key-name")
        self.assertEqual(proto.cache_control, "cache-control")
        self.assertEqual(proto.content_disposition, "content-disposition")
        self.assertEqual(proto.content_encoding, "content-encoding")
        self.assertEqual(proto.content_language, "content-language")
