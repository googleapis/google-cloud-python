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

from google.cloud import _storage_v2

# Map Python Blob attributes to GCS V2 Object proto field names.
_BLOB_ATTR_TO_PROTO_FIELD = {
    "content_type": "content_type",
    "metadata": "metadata",
    "kms_key_name": "kms_key",
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

    # Handle contexts
    contexts = getattr(blob, "contexts", None)
    if contexts:
        custom_proto = {}
        for key, payload in contexts.custom.items():
            # In the REST SDK, deletions are marked by setting the key to None in the "custom" dict.
            # However, the ObjectContexts.custom property filters out None values.
            # If we are in blob_to_proto, we likely only want to include active contexts.
            p_dict = {"value": payload.value}
            if payload.create_time:
                p_dict["create_time"] = payload.create_time
            if payload.update_time:
                p_dict["update_time"] = payload.update_time
            custom_proto[key] = p_dict

        if custom_proto:
            resource_params["contexts"] = {"custom": custom_proto}

    return _storage_v2.Object(**resource_params)
