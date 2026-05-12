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

from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

from google.cloud import _storage_v2

# Map Python Blob attributes to GCS V2 Object proto field names.
_BLOB_ATTR_TO_PROTO_FIELD = {
    "content_type": "content_type",
    "metadata": "metadata",
    "kms_key_name": "kms_key",
    "cache_control": "cache_control",
    "content_disposition": "content_disposition",
    "content_encoding": "content_encoding",
    "content_language": "content_language",
    "temporary_hold": "temporary_hold",
    "event_based_hold": "event_based_hold",
}


def blob_to_proto(blob):
    """Converts a Blob instance to a GCS V2 Object proto message."""

    resource_params = {
        "name": blob.name,
    }

    if blob.bucket:
        resource_params["bucket"] = f"projects/_/buckets/{blob.bucket.name}"

    for attr_name, proto_field in _BLOB_ATTR_TO_PROTO_FIELD.items():
        value = getattr(blob, attr_name, None)
        if value is not None:
            resource_params[proto_field] = value

    custom_time = getattr(blob, "custom_time", None)
    if custom_time is not None:
        custom_time_proto = timestamp_pb2.Timestamp()
        custom_time_proto.FromDatetime(custom_time)
        resource_params["custom_time"] = custom_time_proto

    acl = getattr(blob, "acl", None)
    if acl is not None and getattr(acl, "loaded", False):
        acl_entries = []
        for entry in acl:
            acl_entries.append(
                _storage_v2.ObjectAccessControl(
                    role=entry["role"],
                    entity=entry["entity"],
                )
            )
        if acl_entries:
            resource_params["acl"] = acl_entries

    retention = getattr(blob, "retention", None)
    if retention:
        mode_str = retention.get("mode")
        mode = _storage_v2.Object.Retention.Mode.MODE_UNSPECIFIED
        if mode_str:
            # GCS retention modes are 'Locked' or 'Unlocked'
            mode = getattr(
                _storage_v2.Object.Retention.Mode,
                mode_str.upper(),
                _storage_v2.Object.Retention.Mode.MODE_UNSPECIFIED,
            )

        retain_until_time_proto = None
        retain_until_time = retention.get("retain_until_time")
        if retain_until_time is not None:
            retain_until_time_proto = timestamp_pb2.Timestamp()
            retain_until_time_proto.FromDatetime(retain_until_time)

        resource_params["retention"] = _storage_v2.Object.Retention(
            mode=mode,
            retain_until_time=retain_until_time_proto,
        )

    contexts = getattr(blob, "contexts", None)
    if contexts:
        custom_contexts = {}
        for key, payload in contexts.custom.items():
            payload_params = {"value": payload.value}
            if payload.create_time is not None:
                create_time_proto = timestamp_pb2.Timestamp()
                create_time_proto.FromDatetime(payload.create_time)
                payload_params["create_time"] = create_time_proto
            if payload.update_time is not None:
                update_time_proto = timestamp_pb2.Timestamp()
                update_time_proto.FromDatetime(payload.update_time)
                payload_params["update_time"] = update_time_proto

            custom_contexts[key] = _storage_v2.ObjectCustomContextPayload(
                **payload_params
            )

        resource_params["contexts"] = _storage_v2.ObjectContexts(custom=custom_contexts)

    return _storage_v2.Object(**resource_params)


def proto_to_blob(proto, blob):
    """Updates a Blob instance from a GCS V2 Object proto message."""
    from google.cloud._helpers import _datetime_to_rfc3339

    blob._properties["name"] = proto.name
    if proto.bucket:
        # Assuming bucket name is the last part of the resource name
        blob._properties["bucket"] = proto.bucket.split("/")[-1]

    for attr_name, proto_field in _BLOB_ATTR_TO_PROTO_FIELD.items():
        value = getattr(proto, proto_field, None)
        if value:
            blob._properties[attr_name] = value

    if "custom_time" in proto:
        blob._properties["customTime"] = _datetime_to_rfc3339(proto.custom_time)

    if proto.acl:
        acl_entries = []
        for entry in proto.acl:
            acl_entries.append({"role": entry.role, "entity": entry.entity})
        blob._properties["acl"] = acl_entries

    if "retention" in proto:
        retention = {"mode": _storage_v2.Object.Retention.Mode.Name(proto.retention.mode)}
        if "retain_until_time" in proto.retention:
            retention["retainUntilTime"] = _datetime_to_rfc3339(proto.retention.retain_until_time)
        blob._properties["retention"] = retention

    if "contexts" in proto:
        custom = {}
        for key, payload_proto in proto.contexts.custom.items():
            payload = {"value": payload_proto.value}
            if "create_time" in payload_proto:
                payload["createTime"] = _datetime_to_rfc3339(payload_proto.create_time)
            if "update_time" in payload_proto:
                payload["updateTime"] = _datetime_to_rfc3339(payload_proto.update_time)
            custom[key] = payload
        blob._properties["contexts"] = {"custom": custom}

    return blob


def get_update_mask(blob, changes):
    """Generates a FieldMask for gRPC update operations."""
    paths = []
    for change in changes:
        if change == "contexts":
            contexts = getattr(blob, "contexts", None)
            if contexts is None or not contexts.custom:
                paths.append("contexts.custom")
            else:
                for key in contexts.custom:
                    paths.append(f"contexts.custom.{key}")
        else:
            proto_field = _BLOB_ATTR_TO_PROTO_FIELD.get(change)
            if proto_field:
                paths.append(proto_field)
            elif change == "customTime":
                paths.append("custom_time")
            elif change == "retention":
                paths.append("retention")

    return field_mask_pb2.FieldMask(paths=paths)
