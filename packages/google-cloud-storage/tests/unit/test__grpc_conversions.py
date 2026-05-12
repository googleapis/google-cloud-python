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

import datetime
from unittest import mock

from google.cloud import _storage_v2
from google.cloud.storage import _grpc_conversions


def test_blob_to_proto_simple_fields():
    blob = mock.Mock(
        spec=[
            "name",
            "bucket",
            "content_type",
            "metadata",
            "kms_key_name",
            "cache_control",
            "content_disposition",
            "content_encoding",
            "content_language",
            "temporary_hold",
            "event_based_hold",
            "custom_time",
            "acl",
            "retention",
        ]
    )
    blob.name = "blob-name"
    blob.bucket.name = "bucket-name"
    blob.content_type = "text/plain"
    blob.metadata = {"key": "value"}
    blob.kms_key_name = "kms-key"
    blob.cache_control = "no-cache"
    blob.content_disposition = "attachment"
    blob.content_encoding = "gzip"
    blob.content_language = "en"
    blob.temporary_hold = True
    blob.event_based_hold = False
    blob.custom_time = None
    blob.acl = None
    blob.retention = None

    proto = _grpc_conversions.blob_to_proto(blob)

    assert proto.name == "blob-name"
    assert proto.bucket == "projects/_/buckets/bucket-name"
    assert proto.content_type == "text/plain"
    assert proto.metadata == {"key": "value"}
    assert proto.kms_key == "kms-key"
    assert proto.cache_control == "no-cache"
    assert proto.content_disposition == "attachment"
    assert proto.content_encoding == "gzip"
    assert proto.content_language == "en"
    assert proto.temporary_hold is True
    assert proto.event_based_hold is False


def test_blob_to_proto_custom_time():
    blob = mock.Mock(spec=["name", "bucket", "custom_time", "acl", "retention"])
    blob.name = "blob-name"
    blob.bucket.name = "bucket-name"
    blob.custom_time = datetime.datetime(
        2025, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
    )
    blob.acl = None
    blob.retention = None
    # ensure other fields don't cause issues if missing
    for attr in _grpc_conversions._BLOB_ATTR_TO_PROTO_FIELD:
        setattr(blob, attr, None)

    proto = _grpc_conversions.blob_to_proto(blob)

    assert int(proto.custom_time.timestamp()) == int(blob.custom_time.timestamp())


def test_blob_to_proto_acl():
    blob = mock.Mock(spec=["name", "bucket", "acl", "custom_time", "retention"])
    blob.name = "blob-name"
    blob.bucket.name = "bucket-name"

    acl_mock = mock.MagicMock()
    acl_mock.loaded = True
    acl_mock.__iter__.return_value = iter(
        [
            {"role": "READER", "entity": "allUsers"},
            {"role": "OWNER", "entity": "user-123"},
        ]
    )
    blob.acl = acl_mock

    blob.custom_time = None
    blob.retention = None
    for attr in _grpc_conversions._BLOB_ATTR_TO_PROTO_FIELD:
        setattr(blob, attr, None)

    proto = _grpc_conversions.blob_to_proto(blob)

    assert len(proto.acl) == 2
    assert proto.acl[0].role == "READER"
    assert proto.acl[0].entity == "allUsers"
    assert proto.acl[1].role == "OWNER"
    assert proto.acl[1].entity == "user-123"


def test_blob_to_proto_retention():
    blob = mock.Mock(spec=["name", "bucket", "retention", "custom_time", "acl"])
    blob.name = "blob-name"
    blob.bucket.name = "bucket-name"

    retain_until_time = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
    blob.retention = {"mode": "Locked", "retain_until_time": retain_until_time}

    blob.custom_time = None
    blob.acl = None
    for attr in _grpc_conversions._BLOB_ATTR_TO_PROTO_FIELD:
        setattr(blob, attr, None)

    proto = _grpc_conversions.blob_to_proto(blob)

    assert proto.retention.mode == _storage_v2.Object.Retention.Mode.LOCKED
    assert int(proto.retention.retain_until_time.timestamp()) == int(
        retain_until_time.timestamp()
    )

def test_blob_to_proto_contexts():
    blob = mock.Mock(spec=["name", "bucket", "contexts", "custom_time", "acl", "retention"])
    blob.name = "blob-name"
    blob.bucket.name = "bucket-name"

    from google.cloud.storage.blob import ObjectContexts, ObjectCustomContextPayload
    create_time = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
    payload = ObjectCustomContextPayload(value="val", create_time=create_time)
    blob.contexts = ObjectContexts(blob, custom={"key": payload})

    blob.custom_time = None
    blob.acl = None
    blob.retention = None
    for attr in _grpc_conversions._BLOB_ATTR_TO_PROTO_FIELD:
        setattr(blob, attr, None)

    proto = _grpc_conversions.blob_to_proto(blob)

    assert "key" in proto.contexts.custom
    assert proto.contexts.custom["key"].value == "val"
    assert int(proto.contexts.custom["key"].create_time.timestamp()) == int(
        create_time.timestamp()
    )


def test_proto_to_blob_contexts():
    from google.cloud.storage.blob import Blob
    bucket = mock.Mock()
    blob = Blob("blob-name", bucket=bucket)

    from google.protobuf import timestamp_pb2
    create_time = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
    create_time_proto = timestamp_pb2.Timestamp()
    create_time_proto.FromDatetime(create_time)

    proto = _storage_v2.Object(
        name="blob-name",
        contexts=_storage_v2.ObjectContexts(
            custom={
                "key": _storage_v2.ObjectCustomContextPayload(
                    value="val", create_time=create_time_proto
                )
            }
        )
    )

    _grpc_conversions.proto_to_blob(proto, blob)

    assert "contexts" in blob._properties
    assert "key" in blob._properties["contexts"]["custom"]
    assert blob._properties["contexts"]["custom"]["key"]["value"] == "val"
    assert blob.contexts.custom["key"].create_time == create_time


def test_get_update_mask_contexts():
    blob = mock.Mock(spec=["contexts"])
    from google.cloud.storage.blob import ObjectContexts, ObjectCustomContextPayload

    # Partial updates
    blob.contexts = ObjectContexts(blob, custom={"k1": ObjectCustomContextPayload(value="v1"), "k2": ObjectCustomContextPayload(value="v2")})
    mask = _grpc_conversions.get_update_mask(blob, ["contexts"])
    assert "contexts.custom.k1" in mask.paths
    assert "contexts.custom.k2" in mask.paths
    assert len(mask.paths) == 2

    # Clear all
    blob.contexts = None
    mask = _grpc_conversions.get_update_mask(blob, ["contexts"])
    assert "contexts.custom" in mask.paths
    assert len(mask.paths) == 1

    # Mixed
    mask = _grpc_conversions.get_update_mask(blob, ["contexts", "metadata", "customTime"])
    assert "contexts.custom" in mask.paths
    assert "metadata" in mask.paths
    assert "custom_time" in mask.paths
