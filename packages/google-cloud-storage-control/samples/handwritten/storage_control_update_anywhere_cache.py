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

# [START storage_control_update_anywhere_cache]
def update_anywhere_cache(bucket_name: str, anywhere_cache_id: str, admission_policy: str):
    """
    Updates an Anywhere Cache instance. Mutable fields include `ttl` and `admission_policy`.
    """
    # bucket_name = "your-bucket-name"
    # anywhere_cache_id = "your-anywhere-cache-id"
    # admission_policy = "admit-on-second-miss"

    from google.cloud import storage_control_v2
    from google.protobuf import field_mask_pb2

    client = storage_control_v2.StorageControlClient()

    # The resource name of the Anywhere Cache instance to be updated.
    # Format: projects/{project}/buckets/{bucket}/anywhereCaches/{anywhere_cache}
    name = f"projects/_/buckets/{bucket_name}/anywhereCaches/{anywhere_cache_id}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        name=name,
        admission_policy=admission_policy,
    )

    update_mask = field_mask_pb2.FieldMask(paths=["admission_policy"])

    request = storage_control_v2.UpdateAnywhereCacheRequest(
        anywhere_cache=anywhere_cache,
        update_mask=update_mask,
    )

    operation = client.update_anywhere_cache(request=request)

    print(f"Waiting for operation {operation.operation.name} to complete...")
    response = operation.result()

    print(f"Anywhere Cache updated: {response.name}")
    print(f"Admission policy: {response.admission_policy}")
    return response


# [END storage_control_update_anywhere_cache]
