# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import pytest

def test_object_contexts_lifecycle(shared_bucket, blobs_to_delete):
    blob_name = f"object-contexts-{uuid.uuid4().hex}"
    blob = shared_bucket.blob(blob_name)
    blob.upload_from_string(b"hello world")
    blobs_to_delete.append(blob)

    # 1. Set custom contexts
    blob.contexts.set_custom_context("Department", "HR")
    blob.contexts.set_custom_context("DataClassification", "Confidential")
    blob.patch()

    # 2. Reload and verify
    blob.reload()
    assert blob.contexts.custom["Department"].value == "HR"
    assert blob.contexts.custom["DataClassification"].value == "Confidential"
    assert blob.contexts.custom["Department"].create_time is not None
    assert blob.contexts.custom["Department"].update_time is not None

    # 3. List with filter
    # Match any object that has a context with the specified key attached.
    # filter syntax: contexts."KEY":*
    filter_expr = f'contexts."Department":*'
    blobs = list(shared_bucket.list_blobs(filter_=filter_expr))
    assert any(b.name == blob_name for b in blobs)

    # Match any object that has a context with the specified key and value attached.
    # filter syntax: contexts."KEY"="VALUE"
    filter_expr = f'contexts."Department"="HR"'
    blobs = list(shared_bucket.list_blobs(filter_=filter_expr))
    assert any(b.name == blob_name for b in blobs)

    # Negative match
    filter_expr = f'contexts."Department"="Engineering"'
    blobs = list(shared_bucket.list_blobs(filter_=filter_expr))
    assert not any(b.name == blob_name for b in blobs)

    # 4. Delete a specific context
    blob.contexts.delete_custom_context("Department")
    blob.patch()
    blob.reload()
    assert "Department" not in blob.contexts.custom
    assert blob.contexts.custom["DataClassification"].value == "Confidential"

    # 5. Clear all contexts
    blob.contexts.clear_custom_contexts()
    blob.patch()
    blob.reload()
    assert blob.contexts.custom == {}
