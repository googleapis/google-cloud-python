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

# [START storage_control_create_anywhere_cache]
def create_anywhere_cache(bucket_name: str, zone: str):
    """
    Creates an Anywhere Cache instance.
    """
    # bucket_name = "your-bucket-name"
    # zone = "us-central1-a"

    from google.cloud import storage_control_v2

    client = storage_control_v2.StorageControlClient()

    # The resource name of the bucket to which this Anywhere Cache belongs.
    parent = f"projects/_/buckets/{bucket_name}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        zone=zone,
    )

    request = storage_control_v2.CreateAnywhereCacheRequest(
        parent=parent,
        anywhere_cache=anywhere_cache,
    )

    operation = client.create_anywhere_cache(request=request)

    print(f"Waiting for operation {operation.operation.name} to complete...")
    response = operation.result()

    print(f"Anywhere Cache created: {response.name}")
    return response


# [END storage_control_create_anywhere_cache]
