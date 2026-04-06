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

# [START storage_control_resume_anywhere_cache]
def resume_anywhere_cache(bucket_name: str, anywhere_cache_id: str):
    """
    Resumes a disabled or paused Anywhere Cache instance.
    """
    # bucket_name = "your-bucket-name"
    # anywhere_cache_id = "your-anywhere-cache-id"

    from google.cloud import storage_control_v2

    client = storage_control_v2.StorageControlClient()

    # The resource name of the Anywhere Cache instance.
    # Format: projects/{project}/buckets/{bucket}/anywhereCaches/{anywhere_cache}
    name = f"projects/_/buckets/{bucket_name}/anywhereCaches/{anywhere_cache_id}"

    request = storage_control_v2.ResumeAnywhereCacheRequest(
        name=name,
    )

    response = client.resume_anywhere_cache(request=request)

    print(f"Anywhere Cache resumed: {response.name}")
    print(f"Anywhere Cache state: {response.state}")
    return response


# [END storage_control_resume_anywhere_cache]
