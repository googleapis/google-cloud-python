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

# [START storage_control_list_anywhere_caches]
def list_anywhere_caches(bucket_name: str):
    """
    Lists Anywhere Cache instances for a given bucket.
    """
    # bucket_name = "your-bucket-name"

    from google.cloud import storage_control_v2

    client = storage_control_v2.StorageControlClient()

    # The bucket to which this Anywhere Cache belongs.
    # Format: projects/{project}/buckets/{bucket}
    parent = f"projects/_/buckets/{bucket_name}"

    request = storage_control_v2.ListAnywhereCachesRequest(
        parent=parent,
    )

    page_result = client.list_anywhere_caches(request=request)

    for anywhere_cache in page_result:
        print(f"Anywhere Cache name: {anywhere_cache.name}")

    return page_result


# [END storage_control_list_anywhere_caches]
